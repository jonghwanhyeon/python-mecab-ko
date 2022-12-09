from mecab import MeCab


def test_nouns(mecab: MeCab):
    assert mecab.nouns("") == []

    assert mecab.nouns("나의 꿈은 맑은 바람이 되어서") == [
        "나",
        "꿈",
        "바람",
    ]
