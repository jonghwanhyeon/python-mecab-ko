from mecab import Feature, MeCab, Morpheme, Span


def test_parse(mecab: MeCab):
    assert mecab.parse("") == []

    assert mecab.parse("나의 꿈은 맑은 바람이 되어서") == [
        Morpheme(span=Span(0, 1), surface="나", feature=Feature(pos="NP", has_jongseong=False, reading="나")),
        Morpheme(span=Span(1, 2), surface="의", feature=Feature(pos="JKG", has_jongseong=False, reading="의")),
        Morpheme(
            span=Span(3, 4), surface="꿈", feature=Feature(pos="NNG", semantic="행위", has_jongseong=True, reading="꿈")
        ),
        Morpheme(span=Span(4, 5), surface="은", feature=Feature(pos="JX", has_jongseong=True, reading="은")),
        Morpheme(span=Span(6, 7), surface="맑", feature=Feature(pos="VA", has_jongseong=True, reading="맑")),
        Morpheme(span=Span(7, 8), surface="은", feature=Feature(pos="ETM", has_jongseong=True, reading="은")),
        Morpheme(span=Span(9, 11), surface="바람", feature=Feature(pos="NNG", has_jongseong=True, reading="바람")),
        Morpheme(span=Span(11, 12), surface="이", feature=Feature(pos="JKS", has_jongseong=False, reading="이")),
        Morpheme(span=Span(13, 14), surface="되", feature=Feature(pos="VV", has_jongseong=False, reading="되")),
        Morpheme(span=Span(14, 16), surface="어서", feature=Feature(pos="EC", has_jongseong=False, reading="어서")),
    ]

    assert mecab.parse("흙에서 자란 내 마음 파아란 하늘빛") == [
        Morpheme(span=Span(0, 1), surface="흙", feature=Feature(pos="NNG", has_jongseong=True, reading="흙")),
        Morpheme(span=Span(1, 3), surface="에서", feature=Feature(pos="JKB", has_jongseong=False, reading="에서")),
        Morpheme(
            span=Span(4, 6),
            surface="자란",
            feature=Feature(
                pos="VV+ETM",
                has_jongseong=True,
                reading="자란",
                type="Inflect",
                start_pos="VV",
                end_pos="ETM",
                expression="자라/VV/*+ᆫ/ETM/*",
            ),
        ),
        Morpheme(
            span=Span(7, 8), surface="내", feature=Feature(pos="MM", semantic="~명사", has_jongseong=False, reading="내")
        ),
        Morpheme(span=Span(9, 11), surface="마음", feature=Feature(pos="NNG", has_jongseong=True, reading="마음")),
        Morpheme(
            span=Span(12, 15),
            surface="파아란",
            feature=Feature(
                pos="VA+ETM",
                has_jongseong=True,
                reading="파아란",
                type="Inflect",
                start_pos="VA",
                end_pos="ETM",
                expression="파아랗/VA/*+ᆫ/ETM/*",
            ),
        ),
        Morpheme(
            span=Span(16, 19),
            surface="하늘빛",
            feature=Feature(
                pos="NNG", has_jongseong=True, reading="하늘빛", type="Compound", expression="하늘/NNG/*+빛/NNG/*"
            ),
        ),
    ]
