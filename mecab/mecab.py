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
        user_dictionary_path: Optional[Union[PathLike, list[PathLike]]] = None,
    ):
        """
        Parameters:
            dictionary_path: Path to the system dictionary to use. If not provided, the default mecab-ko-dic dictionary will be used.
            user_dictionary_path: Path or list of paths to user dictionaries to use. If not provided, no user dictionaries will be used.
        """
        if dictionary_path is None:
            dictionary_path = mecab_ko_dic.dictionary_path

        user_dictionary_path = ensure_list(user_dictionary_path)

        dictionary_option = ["--dicdir", str(dictionary_path)]
        user_dictionay_option = ["--userdic", to_csv(user_dictionary_path)] if user_dictionary_path else []

        options = [
            *_rcfile_option,
            *dictionary_option,
            *user_dictionay_option,
        ]
        self._tagger = _mecab.Tagger(options)

    def parse(self, sentence: str) -> list[Morpheme]:
        """Perform morpheme analysis on a given sentence.

        Parameters:
            sentence: A sentence to analyze

        Returns:
            A list of `Morpheme` objects representing each morpheme in the given sentence.
        """
        lattice = create_lattice(sentence)
        if not self._tagger.parse(lattice):
            raise MeCabError(self._tagger.what())

        return [Morpheme._from_node(span, node) for span, node in lattice]

    def pos(self, sentence: str) -> list[tuple[str, str]]:
        """Extract `(surface, part-of-speech tag)` pairs from a given sentence.

        Parameters:
            sentence: A sentence to analyze

        Returns:
            A list of `(surface, part-of-speech tag)` pairs representing each morpheme in the given sentence.
        """
        return [(morpheme.surface, morpheme.pos) for morpheme in self.parse(sentence)]

    def morphs(self, sentence: str) -> list[str]:
        """Extract morphemes from a given sentence.

        Parameters:
            sentence: A sentence to analyze

        Returns:
            A list of morphemes in the given sentence.
        """
        return [morpheme.surface for morpheme in self.parse(sentence)]

    def nouns(self, sentence: str) -> list[str]:
        """Extract nouns from a given sentence

        Parameters:
            sentence: A sentence to analyze

        Returns:
            A list of nouns in the given sentence
        """
        return [morpheme.surface for morpheme in self.parse(sentence) if morpheme.pos.startswith("N")]

    @property
    def dictionary(self) -> list[Dictionary]:
        """Returns the currently loaded dictionaries.

        Returns:
            A list of `Dictionary` objects representing the dictionaries currently loaded.
        """
        return Dictionary._from_dictionary_info(self._tagger.dictionary_info())
