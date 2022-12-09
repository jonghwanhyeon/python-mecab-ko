from mecab import MeCab


def test_morphs(mecab: MeCab):
    assert mecab.morphs("") == []

    assert mecab.morphs("나의 꿈은 맑은 바람이 되어서") == [
        "나",
        "의",
        "꿈",
        "은",
        "맑",
        "은",
        "바람",
        "이",
        "되",
        "어서",
    ]
