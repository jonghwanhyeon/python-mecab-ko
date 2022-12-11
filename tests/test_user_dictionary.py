import subprocess
import uuid
from pathlib import Path
from typing import List, NamedTuple, Optional

import mecab_ko_dic
import pytest

from mecab import Feature, MeCab


class Word(NamedTuple):
    surface: str
    feature: Feature
    # Lower cost has higher priority
    cost: Optional[int] = None

    def __str__(self):
        # Format:
        # <surface>,*,*,<cost>,<pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
        return ",".join(
            [
                self.surface,
                "",  # left context id
                "",  # right context id
                str(self.cost) if self.cost is not None else "",
                str(self.feature),
            ]
        )


def number_of_dictionaries(mecab: MeCab):
    count = 0

    dictionary_info = mecab._tagger.dictionary_info()
    while dictionary_info is not None:
        count += 1
        dictionary_info = dictionary_info.next

    return count


def build_user_dictionary(words: List[Word], output_path: Path) -> Path:
    csv_path = output_path / f"{uuid.uuid4()}.csv"
    dictionary_path = csv_path.with_suffix(".dic")

    # First, create user dictionary from words as CSV format
    with open(csv_path, "w") as output_file:
        for word in words:
            print(str(word), file=output_file)

    # Then, build user dictionary to output_path
    subprocess.run(
        [
            "python3",
            "-m",
            "mecab",
            "dict-index",
            "--model",
            str(mecab_ko_dic.model_path),
            "--userdic",
            str(dictionary_path),
            csv_path,
        ],
        check=True,
    )

    return dictionary_path


@pytest.fixture
def twitch_user_dictionary_path(tmp_path: Path):
    return build_user_dictionary(
        [
            Word("트위치", Feature(pos="NNP", has_jongseong=False)),
        ],
        tmp_path,
    )


@pytest.fixture
def platform_user_dictionary_path(tmp_path: Path):
    return build_user_dictionary(
        [
            Word("플랫폼", Feature(pos="NNG", has_jongseong=True)),
        ],
        tmp_path,
    )


def test_single_user_dictionary(mecab: MeCab, twitch_user_dictionary_path: Path):
    assert number_of_dictionaries(mecab) == 1
    assert mecab.pos("트위치는 양방향 생방송 플랫폼입니다") == [
        ("트", "NNG"),
        ("위치", "NNG"),
        ("는", "JX"),
        ("양방향", "NNG"),
        ("생방송", "NNG"),
        ("플랫", "NNG"),
        ("폼", "NNG"),
        ("입니다", "VCP+EC"),
    ]

    mecab_with_user_dictionary = MeCab(user_dictionay_path=twitch_user_dictionary_path)
    assert number_of_dictionaries(mecab_with_user_dictionary) == 2
    assert mecab_with_user_dictionary.pos("트위치는 양방향 생방송 플랫폼입니다") == [
        ("트위치", "NNP"),
        ("는", "JX"),
        ("양방향", "NNG"),
        ("생방송", "NNG"),
        ("플랫", "NNG"),
        ("폼", "NNG"),
        ("입니다", "VCP+EC"),
    ]


def test_multiple_user_dictionary(
    mecab: MeCab, twitch_user_dictionary_path: Path, platform_user_dictionary_path: Path
):
    assert number_of_dictionaries(mecab) == 1
    assert mecab.pos("트위치는 양방향 생방송 플랫폼입니다") == [
        ("트", "NNG"),
        ("위치", "NNG"),
        ("는", "JX"),
        ("양방향", "NNG"),
        ("생방송", "NNG"),
        ("플랫", "NNG"),
        ("폼", "NNG"),
        ("입니다", "VCP+EC"),
    ]

    mecab_with_user_dictionary = MeCab(
        user_dictionay_path=[twitch_user_dictionary_path, platform_user_dictionary_path]
    )
    assert number_of_dictionaries(mecab_with_user_dictionary) == 3
    assert mecab_with_user_dictionary.pos("트위치는 양방향 생방송 플랫폼입니다") == [
        ("트위치", "NNP"),
        ("는", "JX"),
        ("양방향", "NNG"),
        ("생방송", "NNG"),
        ("플랫폼", "NNG"),
        ("입니다", "VCP+EC"),
    ]
