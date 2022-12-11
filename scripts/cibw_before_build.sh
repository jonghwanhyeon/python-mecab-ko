#!/usr/bin/env bash

set -ex

PROJECT="$1"
PLATFORM=$(python -c "import platform; print(platform.system())")

prepare_linux() {
    python ${PROJECT}/scripts/install_mecab_ko.py
}

prepare_darwin() {
    sudo python ${PROJECT}/scripts/install_mecab_ko.py
}

prepare_windows() {
    if [[ $CIBW_ARCHS == "x86" ]]; then
        architecture="x86"
    elif [[ $CIBW_ARCHS == "AMD64" ]]; then
        architecture="x64"
    fi

    curl \
        --location \
        --output "libmecab-ko.zip" \
        "https://github.com/jonghwanhyeon/mecab-ko/releases/download/0.996-ko-0.9.2/libmecab-0.996-ko-0.9.2-windows-${architecture}.zip"
    unzip -o "libmecab-ko.zip" -d "${MECAB_PATH}"
}

if [[ $PLATFORM == "Linux" ]]; then
    prepare_linux
elif [[ $PLATFORM == "Darwin" ]]; then
    prepare_darwin
elif [[ $PLATFORM == "Windows" ]]; then
    prepare_windows
fi