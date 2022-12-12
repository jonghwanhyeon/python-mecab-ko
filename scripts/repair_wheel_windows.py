import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List

# Reference: https://github.com/actions/runner-images/blob/main/images/win/Windows2019-Readme.md
VISUAL_STUDIO_PATH = r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--architecture", required=True)
    parser.add_argument("--add-path")
    parser.add_argument("--wheel-dir")

    parser.add_argument("wheel")

    arguments = parser.parse_args()

    architecture_table = {"x86": "x86", "AMD64": "x64", "ARM64": "arm64"}
    arguments.architecture = architecture_table[arguments.architecture]

    return arguments


def run(arguments: List[str]):
    print(*arguments, file=sys.stderr, flush=True)
    subprocess.run(arguments, check=True)


def find_msvc_runtime_paths(architecture: str) -> List[str]:
    # Reference: https://learn.microsoft.com/en-us/cpp/windows/choosing-a-deployment-method
    pattern = f"VC/Redist/MSVC/*/{architecture}/**/vcruntime*.dll"
    paths = {path.parent for path in Path(VISUAL_STUDIO_PATH).rglob(pattern)}
    return [str(path) for path in paths]


if __name__ == "__main__":
    arguments = parse_arguments()

    options = []
    if arguments.verbose:
        options.extend(["-v"])

    paths = find_msvc_runtime_paths(arguments.architecture)
    if arguments.add_path is not None:
        paths.append(arguments.add_path)

    add_path_option = ["--add-path", os.pathsep.join(paths)]
    options.extend(add_path_option)

    if arguments.wheel_dir is not None:
        options.extend(["--wheel-dir", arguments.wheel_dir])

    run(["pip", "install", "delvewheel"])
    run(["delvewheel", "show", *add_path_option, arguments.wheel])
    run(["delvewheel", "repair", *options, arguments.wheel])
