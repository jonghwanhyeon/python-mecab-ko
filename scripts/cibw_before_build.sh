#!/usr/bin/env bash

set -ex

PLATFORM="$(uname -s)"

PROJECT="$1"
INSTALL_MECAB_KO=${PROJECT}/scripts/install_mecab_ko.py

if [[ $PLATFORM == "Linux" ]] ; then
    python ${INSTALL_MECAB_KO}
elif [[ $PLATFORM == "Darwin" ]]; then
    sudo python ${INSTALL_MECAB_KO}
fi