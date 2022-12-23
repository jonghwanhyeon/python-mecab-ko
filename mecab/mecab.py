from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple, Optional, Tuple, Union

import mecab_ko_dic

import _mecab
from mecab.utils import create_lattice, ensure_list, to_csv

PathLike = Union[str, Path]

mecabrc_path = Path(__file__).absolute().parent / "mecabrc"
_rcfile_option = ["--rcfile", str(mecabrc_path)]


class Span(NamedTuple):
    start: int
    end: int


class Feature(NamedTuple):
    pos: str
    semantic: Optional[str] = None
    has_jongseong: Optional[bool] = None
    reading: Optional[str] = None
    type: Optional[str] = None
    start_pos: Optional[str] = None
    end_pos: Optional[str] = None
    exprssion: Optional[str] = None
    span: Optional[Span] = None

    @classmethod
    def _from_node(cls, span: Tuple[int, int], node: _mecab.Node) -> Feature:
        # Reference:
        # - http://taku910.github.io/mecab/learn.html
        # - https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
        # - https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/utils/dictionary/lexicon.py

        # feature = <pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
        values = node.feature.split(",")
        assert len(values) == 8

        feature = {field: value if value != "*" else None for field, value in zip(Feature._fields, values)}

        if feature["has_jongseong"] == "T":
            feature["has_jongseong"] = True
        elif feature["has_jongseong"] == "F":
            feature["has_jongseong"] = False

        return cls(**feature, span=Span(*span))

    def __str__(self) -> str:
        feature = {key: value if value is not None else "*" for key, value in self._asdict().items()}
        del feature["span"]  # mecab feature does not include span

        # True -> T / False -> F / * -> *
        feature["has_jongseong"] = str(feature["has_jongseong"])[0]
        return ",".join(feature.values())


class MeCabError(Exception):
    pass


class MeCab:  # APIs are inspired by KoNLPy
    def __init__(
        self,
        dictionary_path: Optional[PathLike] = None,
        user_dictionay_path: Optional[Union[PathLike, List[PathLike]]] = None,
    ):
        if dictionary_path is None:
            dictionary_path = mecab_ko_dic.dictionary_path

        user_dictionay_path = ensure_list(user_dictionay_path)

        dictionary_option = ["--dicdir", str(dictionary_path)]
        user_dictionay_option = ["--userdic", to_csv(user_dictionay_path)] if user_dictionay_path else []

        options = [
            *_rcfile_option,
            *dictionary_option,
            *user_dictionay_option,
        ]
        self._tagger = _mecab.Tagger(options)

    def parse(self, sentence: str) -> List[Tuple[str, Feature]]:
        lattice = create_lattice(sentence)
        if not self._tagger.parse(lattice):
            raise MeCabError(self._tagger.what())

        return [(node.surface, Feature._from_node(span, node)) for span, node in lattice]

    def pos(self, sentence: str) -> List[Tuple[str, str]]:
        return [(surface, feature.pos) for surface, feature in self.parse(sentence)]

    def morphs(self, sentence: str) -> List[str]:
        return [surface for surface, _ in self.parse(sentence)]

    def nouns(self, sentence: str) -> List[str]:
        return [surface for surface, feature in self.parse(sentence) if feature.pos.startswith("N")]
