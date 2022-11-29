import argparse
import os
import subprocess
import sys
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict
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
def change_directory(directory: str):
    original = os.path.abspath(os.getcwd())

    os.chdir(directory)
    yield

    os.chdir(original)


def path_of(filename: str) -> str:
    for path, _, filenames in os.walk(os.getcwd()):
        if filename in filenames:
            return path

    raise ValueError("File {} not found".format(filename))


def retrieve(url: str, filename: str):
    print("Downloading", url, file=sys.stderr, flush=True)
    response = urllib.request.urlopen(url)
    content_length = response.getheader("Content-Length")
    if content_length is not None:
        content_length = int(content_length)

    with open(filename, "wb") as output_file:
        downloaded = 0
        progress_time = time.time()
        while True:
            block = response.read(8192)
            if not block:
                break

            output_file.write(block)
            downloaded += len(block)

            # Report progress every 0.5 seconds
            interval = time.time() - progress_time
            if interval > 0.5:
                if content_length is not None:
                    print(
                        f"> {downloaded} bytes / {content_length} bytes "
                        f"({(downloaded / content_length) * 100:.2f}%)",
                        end="\r",
                        file=sys.stderr,
                    )
                progress_time = time.time()
        print(file=sys.stderr, flush=True)


def install(url: str, *args, environment: Dict[str, str] = None):
    def download(url: str):
        components = urlparse(url)
        filename = os.path.basename(components.path)

        retrieve(url, filename)
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

    print("Installing mecab-ko...", file=sys.stderr, flush=True)
    install(
        MECAB_KO_URL.format(
            mecab_version=arguments.mecab_version,
            mecab_ko_version=arguments.mecab_ko_version,
        ),
        f"--prefix={prefix_path}",
        "--enable-utf8-only",
    )

    print("Installing mecab-ko-dic...", file=sys.stderr, flush=True)
    install(
        MECAB_KO_DIC_URL.format(mecab_ko_dic_version=arguments.mecab_ko_dic_version),
        f"--prefix={prefix_path}",
        "--with-charset=utf8",
        f"--with-mecab-config={prefix_path / 'bin' / 'mecab-config'}",
        environment={
            "LD_LIBRARY_PATH": f"{prefix_path / 'lib'}",
        },
    )
