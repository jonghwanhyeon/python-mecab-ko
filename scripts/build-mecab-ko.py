import argparse
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict
from urllib.parse import urlparse

MECAB_KO_URL = "https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-{mecab_version}-ko-{mecab_ko_version}.tar.gz"
CONFIG_GUESS_URL = "http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD"
CONFIG_SUB_URL = "http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD"

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--mecab_version", default="0.996")
    parser.add_argument("--mecab_ko_version", default="0.9.2")

    return parser.parse_args()


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


def build(url: str, *args):
    components = urlparse(url)
    filename = os.path.basename(components.path)
    retrieve(url, filename)

    subprocess.run(["tar", "-xz", "--strip-components=1", "-f", filename], check=True)
    retrieve(CONFIG_GUESS_URL, "config.guess")
    retrieve(CONFIG_SUB_URL, "config.sub")

    subprocess.run(["./configure", *args], check=True)
    subprocess.run(["make", "--jobs", str(os.cpu_count())], check=True)


if __name__ == "__main__":
    arguments = parse_arguments()

    prefix_path = Path(arguments.prefix)
    prefix_path.mkdir(parents=True, exist_ok=True)

    print("Building mecab-ko...", file=sys.stderr, flush=True)
    build(
        MECAB_KO_URL.format(
            mecab_version=arguments.mecab_version,
            mecab_ko_version=arguments.mecab_ko_version,
        ),
        f"--prefix={prefix_path}",
        "--with-pic",
        "--enable-utf8-only",
    )
