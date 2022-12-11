import sys
from typing import List, Optional, Tuple

import mecab_ko_dic

import _mecab
from mecab import mecabrc_path

rcfile_argument = ["--rcfile", str(mecabrc_path)]
dicdir_argument = ["--dicdir", str(mecab_ko_dic.dictionary_path)]
model_argument = ["--model", str(mecab_ko_dic.model_path)]

def parse_arguments() -> Tuple[Optional[str], List[str]]:
    arguments = sys.argv[1:]
    if not arguments:
        return None, []

    tasks = {"dict-index", "dict-gen", "cost-train"}
    if arguments[0] in tasks:
        return arguments[0], arguments[1:]

    return None, arguments


def mecab_dict_index(arguments: List[str]) -> int:
    return _mecab.cli.dict_index([*dicdir_argument, *model_argument, *arguments])


def mecab_dict_gen(arguments: List[str]) -> int:
    return _mecab.cli.dict_gen([*dicdir_argument, *model_argument, *arguments])


def mecab_cost_train(arguments: List[str]) -> int:
    return _mecab.cli.cost_train([*dicdir_argument, *arguments])


def mecab(arguments: List[str]) -> int:
    return _mecab.cli.mecab([*rcfile_argument, *dicdir_argument, *arguments])


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
