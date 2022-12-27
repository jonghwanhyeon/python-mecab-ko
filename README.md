# python-mecab-ko
A python binding for mecab-ko

## Help
See [documentation](https://python-mecab-ko.readthedocs.io) for more details.

## Installation
Using `pip`:
```console
$ pip install python-mecab-ko
```

## Usage
To perform morpheme analysis, you need to make a MeCab instance first:
```python
>>> from mecab import MeCab
>>> mecab = MeCab()
```

To extract morphemes in a given sentence, use `mecab.morphs()`:
```python
>>> mecab.morphs('영등포구청역에 있는 맛집 좀 알려주세요.')
['영등포구청역', '에', '있', '는', '맛집', '좀', '알려', '주', '세요', '.']
```

To extract nouns in a given sentence, use `mecab.nouns()`:
```python
>>> mecab.nouns('우리나라에는 무릎 치료를 잘하는 정형외과가 없는가!')
['우리', '나라', '무릎', '치료', '정형외과']
```

To perform a morpheme analysis on a given sentence, use `mecab.pos()`:
```python
>>> mecab.pos('자연주의 쇼핑몰은 어떤 곳인가?')
[('자연주의', 'NNG'), ('쇼핑몰', 'NNG'), ('은', 'JX'), ('어떤', 'MM'), ('곳', 'NNG'), ('인가', 'VCP+EF'), ('?', 'SF')]
```

If you would like to obtain detailed morpheme analysis results, use `mecab.parse()`:
```python
>>> mecab.parse('즐거운 하루 보내세요!')
[
    Morpheme(span=Span(start=0, end=3), surface="즐거운",
        feature=Feature(
            pos="VA+ETM", semantic=None, has_jongseong=True, reading="즐거운",
            type="Inflect", start_pos="VA", end_pos="ETM", exprssion="즐겁/VA/*+ᆫ/ETM/*",
        ),
    ),
    Morpheme(span=Span(start=4, end=6), surface="하루",
        feature=Feature(
            pos="NNG", semantic=None, has_jongseong=False, reading="하루",
            type=None, start_pos=None, end_pos=None, exprssion=None,
        ),
    ),
    Morpheme(
        span=Span(start=7, end=9), surface="보내",
        feature=Feature(
            pos="VV", semantic=None, has_jongseong=False, reading="보내",
            type=None, start_pos=None, end_pos=None, exprssion=None,
        ),
    ),
    Morpheme(
        span=Span(start=9, end=11), surface="세요",
        feature=Feature(
            pos="EP+EF", semantic=None, has_jongseong=False, reading="세요",
            type="Inflect", start_pos="EP", end_pos="EF", exprssion="시/EP/*+어요/EF/*",
        ),
    ),
    Morpheme(
        span=Span(start=11, end=12), surface="!",
        feature=Feature(
            pos="SF", semantic=None, has_jongseong=None, reading=None,
            type=None, start_pos=None, end_pos=None, exprssion=None,
        ),
    ),
]
```

## Acknowledgments
- APIs are inspired by [`KoNLPy`](https://github.com/konlpy/konlpy/)
