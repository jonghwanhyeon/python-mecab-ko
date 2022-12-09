from mecab import MeCab


def test_pos(mecab: MeCab):
    assert mecab.pos("") == []

    assert mecab.pos("나의 꿈은 맑은 바람이 되어서") == [
        ("나", "NP"),
        ("의", "JKG"),
        ("꿈", "NNG"),
        ("은", "JX"),
        ("맑", "VA"),
        ("은", "ETM"),
        ("바람", "NNG"),
        ("이", "JKS"),
        ("되", "VV"),
        ("어서", "EC"),
    ]
