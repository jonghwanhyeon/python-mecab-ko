from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import NamedTuple, Optional

import _mecab


class Span(NamedTuple):
    """Represents a span of the morpheme in a text.

    Attributes:
        start: A start index of the morpheme
        end: An end index of the morpheme
    """

    start: int
    end: int


class Feature(NamedTuple):
    """Represents a feature of the morpheme. For more information, please refer to the link:
       [https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY](https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY)

    Attributes:
        pos: A part-of-speech tag of the morpheme
        semantic: A semantic category of the morpheme
        has_jongseong: Whether the last syllable of `reading` has jongseong or not
        reading: A reading of the morpheme
        type: A type of the morpheme (`Inflect`, `Compound`, `Preanalysis`, or `None`)
        start_pos: The first part-of-speech tag of the morpheme
        end_pos: The last part-of-speech tag of the morpheme
        expression: An expression of the morpheme
    """

    pos: str
    semantic: Optional[str] = None
    has_jongseong: Optional[bool] = None
    reading: Optional[str] = None
    type: Optional[str] = None
    start_pos: Optional[str] = None
    end_pos: Optional[str] = None
    expression: Optional[str] = None

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
        span: A span of the morpheme in a text
        surface: A surface of the morpheme
        feature: A feature of the morpheme
    """

    span: Span
    surface: str
    feature: Feature

    @property
    def pos(self) -> str:
        """Returns the part-of-speech tag of the morpheme"""
        return self.feature.pos

    @classmethod
    def _from_node(cls, span: tuple[int, int], node: _mecab.Node) -> Morpheme:
        return cls(surface=node.surface, feature=Feature._from_feature(node.feature), span=Span(*span))


class Dictionary(NamedTuple):
    """Represents a dictionary information

    Attributes:
        path: A path to the dictionary
        number_of_words: The number of words in the dictionary
        type: A type of the dictionary
        version: A version of the dictionary
    """

    class Type(Enum):
        SYSTEM = _mecab.MECAB_SYS_DIC
        USER = _mecab.MECAB_USR_DIC
        UNNOWN = _mecab.MECAB_UNK_DIC

    path: Path
    number_of_words: int
    type: Type
    version: int

    @classmethod
    def _from_dictionary_info(cls, dictionary_info: _mecab.dictionary_info) -> list[Dictionary]:
        list_of_dictionary = []

        while dictionary_info is not None:
            list_of_dictionary.append(
                cls(
                    path=Path(dictionary_info.filename),
                    number_of_words=dictionary_info.size,
                    type=cls.Type(dictionary_info.type),
                    version=dictionary_info.version,
                )
            )
            dictionary_info = dictionary_info.next

        return list_of_dictionary
