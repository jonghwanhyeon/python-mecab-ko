import pytest

from mecab import MeCab


@pytest.fixture
def mecab():
    return MeCab()