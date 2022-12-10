import argparse
import os
import platform
import subprocess


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--wheel-dir")
    parser.add_argument("--require-archs")

    parser.add_argument("wheel")

    return parser.parse_args()


def mecab_config(*args) -> str:
    return subprocess.check_output(["mecab-config", *args], encoding="utf-8").strip()


if __name__ == "__main__":
    arguments = parse_arguments()

    options = []
    if arguments.verbose:
        options.extend(["--verbose"])

    if arguments.wheel_dir is not None:
        options.extend(["--wheel-dir", arguments.wheel_dir])

    if arguments.require_archs is not None:
        options.extend(["--require-archs", arguments.require_archs])

    options.append(arguments.wheel)

    if platform.system() == "Linux":
        LD_LIBRARY_PATH = os.environ["LD_LIBRARY_PATH"]
        LD_LIBRARY_PATH += f":{mecab_config('--libs-only-L')}"
        subprocess.run(
            ["auditwheel", "repair", *options],
            env={**os.environ, "LD_LIBRARY_PATH": LD_LIBRARY_PATH},
        )
    elif platform.system() == "Darwin":
        subprocess.run(["delocate-wheel", *options])
