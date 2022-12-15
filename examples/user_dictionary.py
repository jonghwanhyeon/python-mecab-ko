import subprocess
import sys
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, NamedTuple, Optional

from mecab import Feature, MeCab


class Word(NamedTuple):
    surface: str
    feature: Feature
    # Lower cost has higher priority
    cost: Optional[int] = None

    def __str__(self):
        # Format:
        # <surface>,<left_context_id>,<right_context_id>,<cost>,<pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
        return ",".join(
            [
                self.surface,
                "",  # left context id
                "",  # right context id
                str(self.cost) if self.cost is not None else "",
                str(self.feature),
            ]
        )


def build_user_dictionary(words: List[Word], output_path: Path) -> Path:
    csv_path = output_path / f"{uuid.uuid4()}.csv"
    dictionary_path = csv_path.with_suffix(".dic")

    # First, create user dictionary from words as CSV format
    print("Creating user dictionary as CSV format...")
    with open(csv_path, "w", encoding="utf-8") as output_file:
        for word in words:
            print(str(word), file=output_file)
    print(csv_path.read_text(encoding="utf-8"))

    # Then, build user dictionary to output_path
    print("Building user dictionary...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "mecab",
            "dict-index",
            "--userdic",
            str(dictionary_path),
            str(csv_path),
        ],
        check=True,
    )
    print()

    return dictionary_path


def mecab_pos(mecab: MeCab, sentence: str):
    print("Input:", sentence)
    print("Output:")
    for surface, feature in mecab.parse(sentence):
        print(surface, feature, sep="\t")


def main():
    with TemporaryDirectory() as working_directory:
        working_path = Path(working_directory)

        print("# Using vanilla MeCab...")
        mecab = MeCab()
        mecab_pos(mecab, "트위치는 양방향 생방송 플랫폼입니다")
        # Input: 트위치는 양방향 생방송 플랫폼입니다
        # Output:
        # 트      NNG,*,F,트,*,*,*,*
        # 위치    NNG,*,F,위치,*,*,*,*
        # 는      JX,*,T,는,*,*,*,*
        # 양방향  NNG,*,T,양방향,Compound,*,*,양/NNG/*+방향/NNG/*
        # 생방송  NNG,*,T,생방송,Compound,*,*,생/NNG/*+방송/NNG/*
        # 플랫    NNG,*,T,플랫,*,*,*,*
        # 폼      NNG,*,T,폼,*,*,*,*
        # 입니다  VCP+EC,*,F,입니다,Inflect,VCP,EC,이/VCP/*+ᄇ니다/EC/*
        print()

        print("# Using MeCab with single user dictionary...")
        twitch_user_dictionary_path = build_user_dictionary(
            [Word("트위치", Feature(pos="NNP", has_jongseong=False))],
            working_path,
        )
        mecab = MeCab(user_dictionay_path=twitch_user_dictionary_path)
        mecab_pos(mecab, "트위치는 양방향 생방송 플랫폼입니다")
        # Input: 트위치는 양방향 생방송 플랫폼입니다
        # Output:
        # 트위치  NNP,*,F,*,*,*,*,*
        # 는      JX,*,T,는,*,*,*,*
        # 양방향  NNG,*,T,양방향,Compound,*,*,양/NNG/*+방향/NNG/*
        # 생방송  NNG,*,T,생방송,Compound,*,*,생/NNG/*+방송/NNG/*
        # 플랫    NNG,*,T,플랫,*,*,*,*
        # 폼      NNG,*,T,폼,*,*,*,*
        # 입니다  VCP+EC,*,F,입니다,Inflect,VCP,EC,이/VCP/*+ᄇ니다/EC/*
        print()

        print("# Using MeCab with multiple user dictionaries...")
        twitch_user_dictionary_path = build_user_dictionary(
            [Word("트위치", Feature(pos="NNP", has_jongseong=False))],
            working_path,
        )
        platform_user_dictionary_path = build_user_dictionary(
            [Word("플랫폼", Feature(pos="NNG", has_jongseong=True))],
            working_path,
        )
        mecab = MeCab(
            user_dictionay_path=[
                twitch_user_dictionary_path,
                platform_user_dictionary_path,
            ]
        )
        mecab_pos(mecab, "트위치는 양방향 생방송 플랫폼입니다")
        # Input: 트위치는 양방향 생방송 플랫폼입니다
        # Output:
        # 트위치  NNP,*,F,*,*,*,*,*
        # 는      JX,*,T,는,*,*,*,*
        # 양방향  NNG,*,T,양방향,Compound,*,*,양/NNG/*+방향/NNG/*
        # 생방송  NNG,*,T,생방송,Compound,*,*,생/NNG/*+방송/NNG/*
        # 플랫폼  NNG,*,T,*,*,*,*,*
        # 입니다  VCP+EC,*,F,입니다,Inflect,VCP,EC,이/VCP/*+ᄇ니다/EC/*
        print()

        print("# Using MeCab with single user dictionary with multiple words...")
        twitch_and_platform_user_dictionary_path = build_user_dictionary(
            [Word("트위치", Feature(pos="NNP", has_jongseong=False)), Word("플랫폼", Feature(pos="NNG", has_jongseong=True))],
            working_path,
        )
        mecab = MeCab(user_dictionay_path=[twitch_and_platform_user_dictionary_path])
        mecab_pos(mecab, "트위치는 양방향 생방송 플랫폼입니다")
        # Input: 트위치는 양방향 생방송 플랫폼입니다
        # Output:
        # 트위치  NNP,*,F,*,*,*,*,*
        # 는      JX,*,T,는,*,*,*,*
        # 양방향  NNG,*,T,양방향,Compound,*,*,양/NNG/*+방향/NNG/*
        # 생방송  NNG,*,T,생방송,Compound,*,*,생/NNG/*+방송/NNG/*
        # 플랫폼  NNG,*,T,*,*,*,*,*
        # 입니다  VCP+EC,*,F,입니다,Inflect,VCP,EC,이/VCP/*+ᄇ니다/EC/*
        print()


if __name__ == "__main__":
    main()
