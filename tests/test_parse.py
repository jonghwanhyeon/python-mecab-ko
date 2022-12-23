from mecab import Feature, MeCab, Span


def test_parse(mecab: MeCab):
    assert mecab.parse("") == []

    assert mecab.parse("나의 꿈은 맑은 바람이 되어서") == [
        ("나", Feature(pos="NP", has_jongseong=False, reading="나", span=Span(0, 1))),
        ("의", Feature(pos="JKG", has_jongseong=False, reading="의", span=Span(1, 2))),
        ("꿈", Feature(pos="NNG", semantic="행위", has_jongseong=True, reading="꿈", span=Span(3, 4))),
        ("은", Feature(pos="JX", has_jongseong=True, reading="은", span=Span(4, 5))),
        ("맑", Feature(pos="VA", has_jongseong=True, reading="맑", span=Span(6, 7))),
        ("은", Feature(pos="ETM", has_jongseong=True, reading="은", span=Span(7, 8))),
        ("바람", Feature(pos="NNG", has_jongseong=True, reading="바람", span=Span(9, 11))),
        ("이", Feature(pos="JKS", has_jongseong=False, reading="이", span=Span(11, 12))),
        ("되", Feature(pos="VV", has_jongseong=False, reading="되", span=Span(13, 14))),
        ("어서", Feature(pos="EC", has_jongseong=False, reading="어서", span=Span(14, 16))),
    ]

    assert mecab.parse("흙에서 자란 내 마음 파아란 하늘빛") == [
        ("흙", Feature(pos="NNG", has_jongseong=True, reading="흙", span=Span(0, 1))),
        ("에서", Feature(pos="JKB", has_jongseong=False, reading="에서", span=Span(1, 3))),
        (
            "자란",
            Feature(
                pos="VV+ETM",
                has_jongseong=True,
                reading="자란",
                type="Inflect",
                start_pos="VV",
                end_pos="ETM",
                exprssion="자라/VV/*+ᆫ/ETM/*",
                span=Span(4, 6),
            ),
        ),
        (
            "내",
            Feature(
                pos="MM",
                semantic="~명사",
                has_jongseong=False,
                reading="내",
                span=Span(7, 8),
            ),
        ),
        ("마음", Feature(pos="NNG", has_jongseong=True, reading="마음", span=Span(9, 11))),
        (
            "파아란",
            Feature(
                pos="VA+ETM",
                has_jongseong=True,
                reading="파아란",
                type="Inflect",
                start_pos="VA",
                end_pos="ETM",
                exprssion="파아랗/VA/*+ᆫ/ETM/*",
                span=Span(12, 15),
            ),
        ),
        (
            "하늘빛",
            Feature(
                pos="NNG",
                has_jongseong=True,
                reading="하늘빛",
                type="Compound",
                exprssion="하늘/NNG/*+빛/NNG/*",
                span=Span(16, 19),
            ),
        ),
    ]
