from __future__ import annotations

import gc
import os
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import psutil

from mecab import MeCab, Morpheme

tests_path = Path(__file__).parent.absolute()
corpus_path = tests_path / "corpus.txt"


@dataclass
class MemoryUsage:
    start: int = 0
    end: int = 0

    @property
    def leaked(self) -> int:
        return self.end - self.start


@contextmanager
def trace_memory_usage():
    process = psutil.Process(os.getpid())
    memory_usage = MemoryUsage()

    gc.collect()
    memory_usage.start = process.memory_info().rss

    yield memory_usage

    gc.collect()
    memory_usage.end = process.memory_info().rss


def readlines(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").strip()
    return lines.splitlines()


def parse_corpus(corpus_path: Path) -> list[Morpheme]:
    mecab = MeCab()  # Create a MeCab instance each time.

    morphemes = []
    for line in readlines(corpus_path):
        morphemes.extend(mecab.parse(line))
    return morphemes


def test_memory_leak():
    number_of_tries = 10

    list_of_number_of_morphemes = [0] * number_of_tries

    with trace_memory_usage() as total_memory_usage:
        for index in range(number_of_tries):
            with trace_memory_usage() as memory_usage:
                list_of_number_of_morphemes[index] = len(parse_corpus(corpus_path))
            assert memory_usage.leaked < (5 * 1024 * 1024)
    assert total_memory_usage.leaked < (5 * 1024 * 1024)

    assert len(set(list_of_number_of_morphemes)) == 1
