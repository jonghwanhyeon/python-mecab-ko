import argparse
import os
import platform
import subprocess
import sys
import time
import urllib.request
from typing import Optional

MECAB_KO_URL = "https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-{mecab_version}-ko-{mecab_ko_version}.tar.gz"
CONFIG_GUESS_URL = "http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD"
CONFIG_SUB_URL = (
    "http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD"
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix")
    parser.add_argument("--mecab_version", default="0.996")
    parser.add_argument("--mecab_ko_version", default="0.9.2")

    return parser.parse_args()


def download(url: str, filename: str):
    def progress(current: int, total: Optional[int] = None):
        sys.stderr.write(f"> {current} bytes")
        if total is not None:
            sys.stderr.write(f" / {total} bytes")
            sys.stderr.write(f"({(current / total) * 100:.2f}%)")
        sys.stderr.write("\r")

    sys.stderr.write(f"Downloading {url}\n")
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
                progress(downloaded, content_length)
                progress_time = time.time()

        progress(downloaded, content_length)
        sys.stderr.write("\n")


def configure(*args):
    subprocess.run(["./configure", *args], check=True)


def make(*args):
    subprocess.run(["make", *args], check=True)


def fetch(url: str):
    download(url, "mecab-ko.tar.gz")
    subprocess.run(
        ["tar", "-xz", "--strip-components=1", "-f", "mecab-ko.tar.gz"], check=True
    )

    download(CONFIG_GUESS_URL, "config.guess")
    download(CONFIG_SUB_URL, "config.sub")


def build(prefix: Optional[str] = None):
    configure_options = ["--enable-utf8-only"]
    if prefix is not None:
        configure_options.append(f"--prefix={prefix}")
    configure(*configure_options)

    build_options = ["--jobs", str(os.cpu_count())]
    if platform.system() == "Darwin":
        # Add -arch options to support universal binary
        build_options.append("CXXFLAGS=-O3 -Wall -arch x86_64 -arch arm64")
    make(*build_options)


def install():
    make("install")


if __name__ == "__main__":
    arguments = parse_arguments()

    sys.stderr.write("Downloading mecab-ko...\n")
    fetch(
        MECAB_KO_URL.format(
            mecab_version=arguments.mecab_version,
            mecab_ko_version=arguments.mecab_ko_version,
        )
    )

    sys.stderr.write("Building mecab-ko...\n")
    build(arguments.prefix)

    sys.stderr.write("Installing mecab-ko...\n")
    install()
