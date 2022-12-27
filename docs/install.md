# Install

To install **python-mecab-ko**, simply use pip:

```console
$ pip install python-mecab-ko
```

Since **python-mecab-ko** provides wheel distributions bundled with external shared libraries for most platforms and architectures, you do not need to manually install [mecab-ko](https://bitbucket.org/eunjeon/mecab-ko) if you install with pip.

## Install from the source

However, if you are using unsupported platforms or would like to install from the source, you need the following prerequisites:

- C++14 compatible compiler
- Python header files

First, you need to install [mecab-ko](https://bitbucket.org/eunjeon/mecab-ko) manullay or using [the convenience script](https://raw.githubusercontent.com/jonghwanhyeon/python-mecab-ko/main/scripts/install_mecab_ko.py) provided by this library.

```console
$ wget https://raw.githubusercontent.com/jonghwanhyeon/python-mecab-ko/main/scripts/install_mecab_ko.py
$ python3 install_mecab_ko.py
```

Then, you can install **python-mecab-ko** from the source as follows:

```console
$ pip install git+https://github.com/jonghwanhyeon/python-mecab-ko
```