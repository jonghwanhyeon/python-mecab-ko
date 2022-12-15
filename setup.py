import os
import platform
import shutil
import site
import subprocess
import sys
from glob import glob
from pathlib import Path
from typing import Optional

from pybind11.setup_helpers import Pybind11Extension
from pybind11.setup_helpers import build_ext as _build_ext
from setuptools import setup

is_windows = platform.system() == "Windows"

prefix_paths = [
    Path(sys.prefix),
    Path(site.getuserbase()),
    Path.home() / ".local",
]


class Executable:
    def __init__(self, command: str):
        self._command = command

    def __call__(self, *args) -> str:
        return subprocess.check_output([self.executable, *args], encoding="utf-8").strip()

    def exists(self) -> bool:
        return self.executable is not None

    @property
    def executable(self) -> Optional[str]:
        paths = [str(path / "bin") for path in prefix_paths]
        paths.append(os.environ["PATH"])
        return shutil.which(self._command, path=os.pathsep.join(paths))


class unix_build_ext(_build_ext):
    def build_extension(self, extension):
        if extension.name == "_mecab":
            mecab_config = Executable("mecab-config")
            if not mecab_config.exists():
                sys.stderr.write("==================================================\n")
                sys.stderr.write("You need mecab-ko to build the extension.\n")
                sys.stderr.write("Please install mecab-ko as follows:\n")
                sys.stderr.write(
                    "$ wget https://raw.githubusercontent.com/jonghwanhyeon/python-mecab-ko/main/scripts/install_mecab_ko.py\n"
                )
                sys.stderr.write("$ python3 install_mecab_ko.py\n")
                sys.stderr.write("==================================================\n")
                raise RuntimeError("mecab-ko not found")

            extension.include_dirs.append(mecab_config("--inc-dir"))
            extension.library_dirs.append(mecab_config("--libs-only-L"))
            extension.libraries.append("mecab")

        super().build_extension(extension)


class windows_ext(_build_ext):
    def build_extension(self, extension):
        if extension.name == "_mecab":
            extension.include_dirs.append(r"C:\mecab")
            extension.library_dirs.append(r"C:\mecab")
            extension.libraries.append("libmecab")

        super().build_extension(extension)


setup(
    cmdclass={"build_ext": unix_build_ext if not is_windows else windows_ext},
    ext_modules=[
        Pybind11Extension(
            name="_mecab",
            sources=sorted(glob("mecab/pybind/**/*.cpp", recursive=True)),
            include_dirs=["mecab/pybind/_mecab"],
        ),
    ],
)
