#!/usr/bin/env bash

set -ex

PROJECT="$1"
PLATFORM=$(python -c "import platform; print(platform.system())")

linux_install_mecab() {
    python ${PROJECT}/scripts/install_mecab_ko.py
}

darwin_install_mecab() {
    sudo python ${PROJECT}/scripts/install_mecab_ko.py
}

windows_install_mecab() {
    if [[ $CIBW_ARCHS == "x86" ]]; then
        architecture="x86"
    elif [[ $CIBW_ARCHS == "AMD64" ]]; then
        architecture="x64"
    elif [[ $CIBW_ARCHS == "ARM64" ]]; then
        architecture="arm64"
    fi

    curl \
        --location \
        --output "libmecab-ko.zip" \
        "https://github.com/jonghwanhyeon/mecab-ko/releases/download/0.996-ko-0.9.2/libmecab-0.996-ko-0.9.2-windows-${architecture}.zip"
    unzip -o "libmecab-ko.zip" -d "${MECAB_PATH}"
}

if [[ $PLATFORM == "Linux" ]]; then
    linux_install_mecab
elif [[ $PLATFORM == "Darwin" ]]; then
    darwin_install_mecab
elif [[ $PLATFORM == "Windows" ]]; then
    windows_install_mecab
fi