#!/bin/bash

c++ \
  -O3 \
  -Wall \
  -shared \
  -std=c++14 \
  -undefined dynamic_lookup \
  $(python3 -m pybind11 --includes) \
  -I/Users/jonghwanhyeon/Development/python-mecab-ko/scripts/mecab-0.996-ko-0.9.2/src \
  _mecab/_mecab.cpp \
  _mecab/dictionaryinfo.cpp \
  _mecab/lattice.cpp \
  _mecab/node.cpp \
  _mecab/path.cpp \
  _mecab/tagger.cpp \
  _mecab/utils.cpp \
  /Users/jonghwanhyeon/Development/python-mecab-ko/scripts/mecab-0.996-ko-0.9.2/src/.libs/libmecab.a \
  -o _mecab$(python3-config --extension-suffix) \
&& python3 run.py