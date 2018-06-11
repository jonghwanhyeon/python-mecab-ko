# python-mecab-ko
A python binding for mecab-ko

## Prerequisites
- python3-dev

## Installation
Using `pip`:

    # Use the -v option to check the progress of MeCab installation
    pip install -v python-mecab-ko

## Usage

    import mecab
    mecab = mecab.MeCab()

    mecab.morphs('영등포구청역에 있는 맛집 좀 알려주세요.')
    # ['영등포구청역', '에', '있', '는', '맛집', '좀', '알려', '주', '세요', '.']

    mecab.nouns('우리나라에는 무릎 치료를 잘하는 정형외과가 없는가!')
    # ['우리', '나라', '무릎', '치료', '정형외과']

    mecab.pos('자연주의 쇼핑몰은 어떤 곳인가?')
    # [('자연주의', 'NNG'), ('쇼핑몰', 'NNG'), ('은', 'JX'), ('어떤', 'MM'), ('곳', 'NNG'), ('인가', 'VCP+EF'), ('?', 'SF')]

## Acknowledgments
- APIs are inspired by [`KoNLPy`](https://github.com/konlpy/konlpy/)