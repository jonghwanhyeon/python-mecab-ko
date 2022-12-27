from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import mecab_ko_dic

import _mecab
from mecab.types import Dictionary, Morpheme
from mecab.utils import create_lattice, ensure_list, to_csv

PathLike = Union[str, Path]

mecabrc_path = Path(__file__).absolute().parent / "mecabrc"
_rcfile_option = ["--rcfile", str(mecabrc_path)]


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
        Parameters:
            dictionary_path: Dictionary path for MeCab. If `dictionary_path` is None, `mecab-ko-dic` is used.
            user_dictionay_path: User dictionary paths for MeCab. Defaults to None.
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

        Parameters:
            sentence: A sentence to analyze

        Returns:
            A list of `Morpheme` in a given sentence
        """
        lattice = create_lattice(sentence)
        if not self._tagger.parse(lattice):
            raise MeCabError(self._tagger.what())

        return [Morpheme._from_node(span, node) for span, node in lattice]

    def pos(self, sentence: str) -> list[tuple[str, str]]:
        """Extracts `(surface, part-of-speech tag)` pairs in a given sentence

        Parameters:
            sentence: A sentence to analyze

        Returns:
            A list of `(surface, part-of-speech tag)` pair in a given sentence
        """
        return [(morpheme.surface, morpheme.pos) for morpheme in self.parse(sentence)]

    def morphs(self, sentence: str) -> list[str]:
        """Extracts morphemes in a given sentence

        Parameters:
            sentence: A sentence to analyze

        Returns:
            A list of morphemes in a given sentence
        """
        return [morpheme.surface for morpheme in self.parse(sentence)]

    def nouns(self, sentence: str) -> list[str]:
        """Extracts nouns in a given sentence

        Parameters:
            sentence: A sentence to analyze

        Returns:
            A list of nouns in a given sentence
        """
        return [morpheme.surface for morpheme in self.parse(sentence) if morpheme.pos.startswith("N")]

    @property
    def dictionary(self) -> list[Dictionary]:
        """Returns currently loaded dictionaries

        Returns:
            a list of loaded `Dictionary`
        """
        return Dictionary._from_dictionary_info(self._tagger.dictionary_info())
