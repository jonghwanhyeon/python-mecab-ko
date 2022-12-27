from __future__ import annotations

from typing import NamedTuple, Optional

import _mecab


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
