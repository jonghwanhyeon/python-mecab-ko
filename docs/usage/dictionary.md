# Dictionary
[MeCab](https://taku910.github.io/mecab/) uses [two types of dictionaries](https://taku910.github.io/mecab/dic.html):

- **System dictionary**: A dictionary trained using a large corpus which contains a large number of common words and phrases.
- **User dictionary**: A dictionary that allows you to add a small number of custom words or morphemes

For Korean language, there are several system dictionaries as follows:

- [`mecab-ko-dic`](https://bitbucket.org/eunjeon/mecab-ko-dic)
- [`openkorpos`](https://github.com/openkorpos/model-mecab)


## System dictionary
**python-mecab-ko** uses `mecab-ko-dic` as default system dictionary. However, if you would like to use other system dictionaries, you can pass `dictionary_path` when initializing [MeCab][mecab.MeCab].


!!! note
    When using other system dictionaries, they must already be compiled into binary files using `mecab-dict-index`.


For example, to use `openkorpos` system dictionary, first install `openkorpos-dic` using pip:

```consol
$ pip install openkorpos-dic
```

Then, initialize [MeCab][mecab.MeCab] by passing `dictionary_path` as follows:

```pycon
>>> import openkorpos_dic
>>> from mecab import MeCab
>>> mecab = MeCab(dictionary_path=openkorpos_dic.DICDIR)
>>> mecab.pos("아버지가방에들어가신다")
[('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어가', 'VV'), ('신다', 'EP+EF+VCP')]
```

If you would like to check which dictionary MeCab is currently using, inspect [MeCab.dictionary][mecab.MeCab.dictionary] property.
```pycon
>>> mecab.dictionary
[Dictionary(path=PosixPath('openkorpos_dic/dicdir/sys.dic'), number_of_words=816283, type=<Type.SYSTEM: 0>, version=102)]
```

## User dictionary
**python-mecab-ko** also supports user dictionary. When initializing [MeCab][mecab.MeCab], you can add multiple user dictionaries by passing `user_dictionary_path` as follows:

```pycon
>>> from mecab import MeCab
>>> # mecab = MeCab(user_dictionary_path="nnp.dic") # When adding one user dictionary
>>> mecab = MeCab(user_dictionary_path=["nnp.dic", "nng.dic"]) # When adding multiple user dictionaries
>>> mecab.dictionary
[Dictionary(path=PosixPath('mecab_ko_dic/dictionary/sys.dic'), number_of_words=816283, type=<Type.SYSTEM: 0>, version=102),
 Dictionary(path=PosixPath('nnp.dic'), number_of_words=1, type=<Type.USER: 1>, version=102),
 Dictionary(path=PosixPath('nng.dic'), number_of_words=1, type=<Type.USER: 1>, version=102)]
```

Please refer to [Custom Vocabulary](custom-vocabulary.md) documentation for instructions on how to create a user dictionary.