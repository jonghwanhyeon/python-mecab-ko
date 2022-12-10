import subprocess
from pathlib import Path

import mecab_ko_dic
import pytest

from mecab import MeCab


def number_of_dictionaries(mecab: MeCab):
    count = 0

    dictionary_info = mecab._tagger.dictionary_info()
    while dictionary_info is not None:
        count += 1
        dictionary_info = dictionary_info.next

    return count


def build_user_dictionary(
    user_dictionary_path: Path, surface: str, pos, has_jongseong: bool
) -> Path:
    user_dictionary_path.write_text(
        f"{surface},,,,{pos},*,{str(has_jongseong)[0]},{surface},*,*,*,*"
    )

    built_user_dictionary_path = user_dictionary_path.with_suffix(".dic")
    subprocess.run(
        [
            "python3",
            "-m",
            "mecab",
            "dict-index",
            "--model",
            str(mecab_ko_dic.model_path),
            "--userdic",
            str(built_user_dictionary_path),
            str(user_dictionary_path),
        ]
    )

    return built_user_dictionary_path


@pytest.fixture
def twitch_user_dictionary_path(tmp_path: Path):
    return build_user_dictionary(
        tmp_path / "twitch.csv", "트위치", pos="NNP", has_jongseong=False
    )


@pytest.fixture
def platform_user_dictionary_path(tmp_path: Path):
    return build_user_dictionary(
        tmp_path / "platform.csv", "플랫폼", pos="NNG", has_jongseong=True
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
