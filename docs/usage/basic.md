# Basic

**python-mecab-ko** provides simple APIs inspired by [KoNLPy](https://github.com/konlpy/konlpy).

- [`MeCab.morphs()`][mecab.MeCab.morphs]: Extracts morphemes in a given sentence
- [`MeCab.nouns()`][mecab.MeCab.nouns]: Extracts nouns in a given sentence
- [`MeCab.pos()`][mecab.MeCab.pos]: Extracts `(morpheme, part-of-speech tag)` pairs in a given sentence

To use these APIs, you need to make a MeCab instance first.

```pycon
>>> from mecab import MeCab
>>> mecab = MeCab()
```

To extract morphemes in a given sentence, use [`mecab.morphs()`][mecab.MeCab.morphs]:

```pycon
>>> mecab.morphs("영등포구청역에 있는 맛집 좀 알려주세요.")
["영등포구청역", "에", "있", "는", "맛집", "좀", "알려", "주", "세요", "."]
```

To extract nouns in a given sentence, use [`mecab.nouns()`][mecab.MeCab.nouns]:

```pycon
>>> mecab.nouns("우리나라에는 무릎 치료를 잘하는 정형외과가 없는가!")
["우리", "나라", "무릎", "치료", "정형외과"]
```

To extract `(morpheme, part-of-speech tag)` pairs in a given sentence, use [`mecab.pos()`][mecab.MeCab.pos]:

```pycon
>>> mecab.pos("자연주의 쇼핑몰은 어떤 곳인가?")
[("자연주의", "NNG"), ("쇼핑몰", "NNG"), ("은", "JX"), ("어떤", "MM"), ("곳", "NNG"), ("인가", "VCP+EF"), ("?", "SF")]
```
