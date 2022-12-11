# python-mecab-ko
A python binding for mecab-ko


## Installation
Using `pip`:
```bash
$ pip install python-mecab-ko
```

This library currently provides binary wheels on Linux and macOS platforms. If you are using other platforms, you need the following prerequisites to build from source:
- C++14 compatible compiler
- Python header files
- mecab-ko
  - This repository provides a convenience script at  `scripts/install_mecab_ko.py` to install `mecab-ko`


## Usage
```python
import mecab
mecab = mecab.MeCab()

mecab.morphs('영등포구청역에 있는 맛집 좀 알려주세요.')
# ['영등포구청역', '에', '있', '는', '맛집', '좀', '알려', '주', '세요', '.']

mecab.nouns('우리나라에는 무릎 치료를 잘하는 정형외과가 없는가!')
# ['우리', '나라', '무릎', '치료', '정형외과']

mecab.pos('자연주의 쇼핑몰은 어떤 곳인가?')
# [('자연주의', 'NNG'), ('쇼핑몰', 'NNG'), ('은', 'JX'), ('어떤', 'MM'), ('곳', 'NNG'), ('인가', 'VCP+EF'), ('?', 'SF')]

mecab.parse('즐거운 하루 보내세요!')
# [
#     ('즐거운', Feature(
#         pos='VA+ETM', semantic=None, has_jongseong=True, reading='즐거운',
#         type='Inflect', start_pos='VA', end_pos='ETM',
#         expression='즐겁/VA/*+ᆫ/ETM/*')),
#     ('하루', Feature(
#         pos='NNG', semantic=None, has_jongseong=False, reading='하루',
#         type=None, start_pos=None, end_pos=None,
#         expression=None)),
#     ('보내', Feature(
#         pos='VV', semantic=None, has_jongseong=False, reading='보내',
#         type=None, start_pos=None, end_pos=None,
#         expression=None)),
#     ('세요', Feature(
#         pos='EP+EF', semantic=None, has_jongseong=False, reading='세요',
#         type='Inflect', start_pos='EP', end_pos='EF',
#         expression='시/EP/*+어요/EF/*')),
#     ('!', Feature(
#         pos='SF', semantic=None, has_jongseong=None, reading=None,
#         type=None, start_pos=None, end_pos=None,
#         expression=None))
# ]
```

### CLI
The library also provides a proxy for several command-line interfaces provided by mecab. These interfaces can be used to add vocabulary to a user dictonary.
- `python3 -m mecab`
- `python3 -m mecab dict-index`
- `python3 -m mecab dict-gen`
- `python3 -m mecab cost-train`

### User Dictionary
You can build a user dictionary using the above command-line interface:
```bash
$ python3 -m mecab dict-index \
    --userdic=user.dic \
    user.csv
```
> **NOTE**
> - The CSV file must be in the following format:
>   - `<surface>,*,*,<cost>,<pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>`
> - Example:
>   - `트위치,,,,NNP,*,F,트위치,*,*,*,*`
>   - `플랫폼,,,,NNG,*,T,플랫폼,*,*,*,*`

Then, you can add the built user dictionary as follows:
```python
from mecab import MeCab
mecab = MeCab(user_dictionary_path="user.dic")

# If there are multiple dictionaries:
mecab = MeCab(user_dictionary_path=["nnp.dic", "nng.dic"])
```

Fore more detailed information, please refer to [`examples/user_dictionary.py`](https://github.com/jonghwanhyeon/python-mecab-ko/tree/main/examples/user_dictionary.py).

## Acknowledgments
- APIs are inspired by [`KoNLPy`](https://github.com/konlpy/konlpy/)
