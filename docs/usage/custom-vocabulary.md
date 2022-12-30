# Custom Vocabulary

Let's look at the following example.
```pycon
>>> from mecab import MeCab
>>> mecab = MeCab()
>>> mecab.pos("트위치는 양방향 생방송 플랫폼입니다.")
[('트', 'NNG'), ('위치', 'NNG'), ('는', 'JX'), ('양방향', 'NNG'), ('생방송', 'NNG'), ('플랫', 'NNG'), ('폼', 'NNG'), ('입니다', 'VCP+EF'), ('.', 'SF')]
```

As shown, the nouns `트위치` and `플랫폼` were separated into morphemes. To solve this issue, [MeCab](https://taku910.github.io/mecab/) supports adding custom vocabulary via user dictionaries.

To create a user dictionary, you first need to create a CSV file in the following format:

```csv
<surface>,<left_context_id>,<right_context_id>,<cost>,<pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
```


!!! note
    For more information about each column, please refer to [https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY/edit#gid=1718487366](https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY/edit#gid=1718487366).


For example, if you would like to add `트위치` as a proper noun (`NNP`) and `플랫폼` as a common noun (`NNG`), you can write a CSV file like this:

```csv title="nouns.csv"
트위치,,,,NNP,*,F,트위치,*,*,*,*
플랫폼,,,,NNG,*,T,플랫폼,*,*,*,*
```

Then, you need to compile the CSV file as a binary dictionary file using `mecab-dict-index`. As it stands, you would need to install [MeCab](https://taku910.github.io/mecab/) to use `mecab-dict-index`. However, for convenience, **python-mecab-ko** provides a proxy interface for `mecab-dict-index` so that the installation of mecab is no longer required.


```console
$ python3 -m mecab dict-index --userdic nouns.dic nouns.csv
```

Now, the user dictionary is successfully compiled and ready to use. To use the user dictionary, simply pass it as `user_dictionary_path` when initializing MeCab.

```pycon
>>> from mecab import MeCab
>>> mecab = MeCab(user_dictionary_path="nouns.dic")
>>> mecab.dictionary
[Dictionary(path=PosixPath('mecab_ko_dic/dictionary/sys.dic'), number_of_words=816283, type=<Type.SYSTEM: 0>, version=102),
 Dictionary(path=PosixPath('nouns.dic'), number_of_words=2, type=<Type.USER: 1>, version=102)]
>>> mecab.pos("트위치는 양방향 생방송 플랫폼입니다.")
[('트위치', 'NNP'), ('는', 'JX'), ('양방향', 'NNG'), ('생방송', 'NNG'), ('플랫폼', 'NNG'), ('입니다', 'VCP+EF'), ('.', 'SF')]
```

As you can see, the nouns `트위치` and `플랫폼` are now correctly identified as proper and common nouns, respectively.


!!! note
    If there are multiple user dictionaries, you can pass them as a list:

    ```pycon
    >>> from mecab import MeCab
    >>> mecab = MeCab(user_dictionary_path=["nnp.dic", "nng.dic"])
    >>> mecab.dictionary
    [Dictionary(path=PosixPath('mecab_ko_dic/dictionary/sys.dic'), number_of_words=816283, type=<Type.SYSTEM: 0>, version=102),
    Dictionary(path=PosixPath('nnp.dic'), number_of_words=1, type=<Type.USER: 1>, version=102),
    Dictionary(path=PosixPath('nng.dic'), number_of_words=1, type=<Type.USER: 1>, version=102)]
    ```