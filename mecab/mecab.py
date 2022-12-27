from __future__ import annotations

from pathlib import Path
from typing import NamedTuple, Optional, Union

import mecab_ko_dic

import _mecab
from mecab.utils import create_lattice, ensure_list, to_csv

PathLike = Union[str, Path]

mecabrc_path = Path(__file__).absolute().parent / "mecabrc"
_rcfile_option = ["--rcfile", str(mecabrc_path)]


class Span(NamedTuple):
    """Represents a span of the morpheme

    Attributes:
        start (int): A start index of the morpheme
        end (int): An end index of the morpheme
    """

    start: int
    end: int


class Feature(NamedTuple):
    """Represents a feature of the morpheme. For more information, please refer to
       [https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY](https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY)

    Attributes:
        pos (str): A part-of-speech tag of the morpheme
        semantic (Optional[str], optional): A semantic category of the morpheme
        has_jongseong (Optional[bool], optional): Whether the last syllable of `reading` has jongseong or not
        reading (Optional[str], optional): A reading of the morpheme
        type (Optional[str], optional): A type of the morpheme (`Inflect`, `Compound`, `Preanalysis`, or `None`)
        start_pos (Optional[str], optional): A first part-of-speech tag of the morpheme
        end_pos (Optional[str], optional): A last part-of-speech tag of the morpheme
        exprssion (Optional[str], optional): An expression of the morpheme
    """

    pos: str
    semantic: Optional[str] = None
    has_jongseong: Optional[bool] = None
    reading: Optional[str] = None
    type: Optional[str] = None
    start_pos: Optional[str] = None
    end_pos: Optional[str] = None
    exprssion: Optional[str] = None

    @classmethod
    def _from_feature(cls, feature: str) -> Feature:
        # Reference:
        # - http://taku910.github.io/mecab/learn.html
        # - https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
        # - https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/utils/dictionary/lexicon.py

        # feature = <pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
        values = feature.split(",")
        assert len(values) == 8

        feature = {field: value if value != "*" else None for field, value in zip(Feature._fields, values)}

        if feature["has_jongseong"] == "T":
            feature["has_jongseong"] = True
        elif feature["has_jongseong"] == "F":
            feature["has_jongseong"] = False

        return cls(**feature)

    def __str__(self) -> str:
        feature = {key: value if value is not None else "*" for key, value in self._asdict().items()}

        # True -> T / False -> F / * -> *
        feature["has_jongseong"] = str(feature["has_jongseong"])[0]
        return ",".join(feature.values())


class Morpheme(NamedTuple):
    """Represents a morpheme

    Attributes:
        span (Span): A span of the morpheme
        surface (str): A surface of the morpheme
        feature (Feature): A feature of the morpheme
    """

    span: Span
    surface: str
    feature: Feature

    @property
    def pos(self) -> str:
        """Returns a part-of-speech tag of the morpheme"""
        return self.feature.pos

    @classmethod
    def _from_node(cls, span: tuple[int, int], node: _mecab.Node) -> Morpheme:
        return cls(surface=node.surface, feature=Feature._from_feature(node.feature), span=Span(*span))


class MeCabError(Exception):
    """Raised if an error occurred from MeCab"""

    pass


class MeCab:  # APIs are inspired by KoNLPy
    def __init__(
        self,
        dictionary_path: Optional[PathLike] = None,
        user_dictionay_path: Optional[Union[PathLike, list[PathLike]]] = None,
    ):
        """
        Args:
            dictionary_path (Optional[PathLike], optional): Dictionary path for MeCab. If `dictionary_path` is None, `mecab-ko-dic` is used.
            user_dictionay_path (Optional[Union[PathLike, list[PathLike]]], optional): User dictionary paths for MeCab. Defaults to None.
        """
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

    def parse(self, sentence: str) -> list[Morpheme]:
        """Performs a morpheme analysis on a given sentence and returns a list of `Morpheme` which contains detailed information about each morpheme

        Args:
            sentence (str): A sentence to analyze

        Returns:
            list[Morpheme]: A list of `Morpheme` in a given sentence
        """
        lattice = create_lattice(sentence)
        if not self._tagger.parse(lattice):
            raise MeCabError(self._tagger.what())

        return [Morpheme._from_node(span, node) for span, node in lattice]

    def pos(self, sentence: str) -> list[tuple[str, str]]:
        """Extracts `(surface, part-of-speech tag)` pairs in a given sentence

        Args:
            sentence (str): A sentence to analyze

        Returns:
            list[Tuple[str, str]]: A list of `(surface, part-of-speech tag)` pair in a given sentence
        """
        return [(morpheme.surface, morpheme.pos) for morpheme in self.parse(sentence)]

    def morphs(self, sentence: str) -> list[str]:
        """Extracts morphemes in a given sentence

        Args:
            sentence (str): A sentence to analyze

        Returns:
            list[str]: A list of morphemes in a given sentence
        """
        return [morpheme.surface for morpheme in self.parse(sentence)]

    def nouns(self, sentence: str) -> list[str]:
        """Extracts nouns in a given sentence

        Args:
            sentence (str): A sentence to analyze

        Returns:
            list[str]:  A list of nouns in a given sentence
        """
        return [morpheme.surface for morpheme in self.parse(sentence) if morpheme.pos.startswith("N")]
