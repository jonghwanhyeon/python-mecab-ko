from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple, Optional, Tuple

import _mecab

_mecabrc_path = Path(__file__).parent / "mecabrc"


def _create_lattice(sentence: str) -> _mecab.Lattice:
    lattice = _mecab.Lattice()
    lattice.add_request_type(_mecab.MECAB_ALLOCATE_SENTENCE)  # Required
    lattice.set_sentence(sentence)

    return lattice


class Feature(NamedTuple):
    pos: str
    semantic: Optional[str]
    has_jongseong: Optional[bool]
    reading: Optional[str]
    type: Optional[str]
    start_pos: Optional[str]
    end_pos: Optional[str]
    exprssion: Optional[str]

    @classmethod
    def _from_node(cls, node: _mecab.Node) -> Feature:
        # Reference:
        # - http://taku910.github.io/mecab/learn.html
        # - https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
        # - https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/utils/dictionary/lexicon.py

        # feature = <pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
        values = node.feature.split(",")
        assert len(values) == 8

        feature = {
            field: value if value != "*" else None
            for field, value in zip(Feature._fields, values)
        }

        if feature["has_jongseong"] == "T":
            feature["has_jongseong"] = True
        elif feature["has_jongseong"] == "F":
            feature["has_jongseong"] = False

        return cls(**feature)


class MeCabError(Exception):
    pass


class MeCab:  # APIs are inspired by KoNLPy
    def __init__(self, dictionary_directory: Optional[str] = None):
        if dictionary_directory is None:
            try:
                import mecab_ko_dic

                dictionary_directory = mecab_ko_dic.DICDIR
            except ImportError:
                raise MeCabError(
                    "`mecab_ko_dic` not found. Please run `pip install mecab_ko_dic`"
                )

        arguments = [
            "--rcfile",
            str(_mecabrc_path),
            "--dicdir",
            dictionary_directory,
        ]

        self.tagger = _mecab.Tagger(arguments)

    def parse(self, sentence: str) -> List[Tuple[str, Feature]]:
        lattice = _create_lattice(sentence)
        if not self.tagger.parse(lattice):
            raise MeCabError(self.tagger.what())

        return [(node.surface, Feature._from_node(node)) for node in lattice]

    def pos(self, sentence: str) -> List[Tuple[str, str]]:
        return [(surface, feature.pos) for surface, feature in self.parse(sentence)]

    def morphs(self, sentence: str) -> List[str]:
        return [surface for surface, _ in self.parse(sentence)]

    def nouns(self, sentence: str) -> List[str]:
        return [
            surface
            for surface, feature in self.parse(sentence)
            if feature.pos.startswith("N")
        ]
