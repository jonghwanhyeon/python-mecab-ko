import argparse
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

MECAB_KO_URL = "https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-{mecab_version}-ko-{mecab_ko_version}.tar.gz"
MECAB_KO_DIC_URL = "https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-{mecab_ko_dic_version}.tar.gz"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--mecab_version", default="0.996")
    parser.add_argument("--mecab_ko_version", default="0.9.2")
    parser.add_argument("--mecab_ko_dic_version", default="2.1.1-20180720")

    return parser.parse_args()


@contextmanager
def change_directory(directory):
    original = os.path.abspath(os.getcwd())

    os.chdir(directory)
    yield

    os.chdir(original)


def path_of(filename):
    for path, _, filenames in os.walk(os.getcwd()):
        if filename in filenames:
            return path

    raise ValueError("File {} not found".format(filename))


def install(url, *args, environment=None):
    def download(url):
        components = urlparse(url)
        filename = os.path.basename(components.path)

        subprocess.run(
            [
                "wget",
                "--progress=dot:binary",
                "--output-document={}".format(filename),
                url,
            ],
            check=True,
        )
        subprocess.run(["tar", "-xzf", filename], check=True)

    def configure(*args):
        with change_directory(path_of("configure")):
            try:
                subprocess.run(["./autogen.sh"])
            except:
                pass

            subprocess.run(["./configure", *args], check=True)

    def make():
        with change_directory(path_of("Makefile")):
            subprocess.run(["make"], check=True, env=environment)
            subprocess.run(["make", "install"], check=True, env=environment)

    with TemporaryDirectory() as directory:
        with change_directory(directory):
            download(url)
            configure(*args)
            make()


if __name__ == "__main__":
    arguments = parse_arguments()

    prefix_path = Path(arguments.prefix)
    prefix_path.mkdir(parents=True, exist_ok=True)

    print("Installing mecab-ko...")
    install(
        MECAB_KO_URL.format(
            mecab_version=arguments.mecab_version,
            mecab_ko_version=arguments.mecab_ko_version,
        ),
        f"--prefix={prefix_path}",
        "--enable-utf8-only",
    )

    print("Installing mecab-ko-dic...")
    install(
        MECAB_KO_DIC_URL.format(mecab_ko_dic_version=arguments.mecab_ko_dic_version),
        f"--prefix={prefix_path}",
        "--with-charset=utf8",
        f"--with-mecab-config={prefix_path / 'bin' / 'mecab-config'}",
        environment={
            "LD_LIBRARY_PATH": f"{prefix_path / 'lib'}",
        },
    )
