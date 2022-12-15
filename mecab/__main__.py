import sys
from typing import List, Optional, Tuple

import mecab_ko_dic

import _mecab
from mecab import mecabrc_path

_rcfile_option = ["--rcfile", str(mecabrc_path)]
_dicdir_option = ["--dicdir", str(mecab_ko_dic.dictionary_path)]
_model_option = ["--model", str(mecab_ko_dic.model_path)]


def parse_arguments() -> Tuple[Optional[str], List[str]]:
    arguments = sys.argv[1:]
    if not arguments:
        return None, []

    tasks = {"dict-index", "dict-gen", "cost-train"}
    if arguments[0] in tasks:
        return arguments[0], arguments[1:]

    return None, arguments


def mecab_dict_index(arguments: List[str]) -> int:
    return _mecab.cli.dict_index([*_dicdir_option, *_model_option, *arguments])


def mecab_dict_gen(arguments: List[str]) -> int:
    return _mecab.cli.dict_gen([*_dicdir_option, *_model_option, *arguments])


def mecab_cost_train(arguments: List[str]) -> int:
    return _mecab.cli.cost_train([*_dicdir_option, *arguments])


def mecab(arguments: List[str]) -> int:
    return _mecab.cli.mecab([*_rcfile_option, *_dicdir_option, *arguments])


def main() -> int:
    task, arguments = parse_arguments()

    if task == "dict-index":
        return mecab_dict_index(arguments)
    elif task == "dict-gen":
        return mecab_dict_gen(arguments)
    elif task == "cost-train":
        return mecab_cost_train(arguments)
    else:
        return mecab(arguments)


if __name__ == "__main__":
    sys.exit(main())
