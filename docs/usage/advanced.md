# Advanced

If you would like to utilize more detailed information about each morpheme, you can use [`MeCab.parse()`][mecab.MeCab.parse] which returns a list of [`Morpheme`][mecab.Morpheme].

A [`Morpheme`][mecab.Morpheme] contains the following information:

- `span`: A span of the morpheme
- `surface`: A surface of the morpheme
- `feature`: A feature of the morpheme
- `pos`: A part-of-speech tag of the morpheme

```pycon
>>> mecab.parse("즐거운 하루 보내세요!")
[
    Morpheme(span=Span(start=0, end=3), surface="즐거운",
             feature=Feature(
             pos="VA+ETM", semantic=None, has_jongseong=True, reading="즐거운",
             type="Inflect", start_pos="VA", end_pos="ETM", expression="즐겁/VA/*+ᆫ/ETM/*",
        ),
    ),
    Morpheme(span=Span(start=4, end=6), surface="하루",
             feature=Feature(
             pos="NNG", semantic=None, has_jongseong=False, reading="하루",
             type=None, start_pos=None, end_pos=None, expression=None,
        ),
    ),
    Morpheme(span=Span(start=7, end=9), surface="보내",
             feature=Feature(
             pos="VV", semantic=None, has_jongseong=False, reading="보내",
             type=None, start_pos=None, end_pos=None, expression=None,
        ),
    ),
    Morpheme(span=Span(start=9, end=11), surface="세요",
             feature=Feature(
             pos="EP+EF", semantic=None, has_jongseong=False, reading="세요",
             type="Inflect", start_pos="EP", end_pos="EF", expression="시/EP/*+어요/EF/*",
        ),
    ),
    Morpheme(span=Span(start=11, end=12), surface="!",
             feature=Feature(
             pos="SF", semantic=None, has_jongseong=None, reading=None,
             type=None, start_pos=None, end_pos=None, expression=None,
        ),
    ),
]
```