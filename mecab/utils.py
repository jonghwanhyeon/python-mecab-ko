from typing import Any, List

import _mecab


def create_lattice(sentence: str) -> _mecab.Lattice:
    lattice = _mecab.Lattice()
    lattice.add_request_type(_mecab.MECAB_ALLOCATE_SENTENCE)  # Required
    lattice.set_sentence(sentence)

    return lattice


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []

    if not isinstance(value, list):
        value = [value]

    return value


def to_csv(items: List[Any]) -> str:
    return ",".join(f'"{item}"' for item in items)
