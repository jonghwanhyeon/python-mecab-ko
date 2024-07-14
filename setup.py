import os
import platform
import shutil
import site
import subprocess
import sys
from glob import glob
from pathlib import Path
from typing import Optional

from pybind11.setup_helpers import Pybind11Extension, build_ext
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
        if self.executable is None:
            raise RuntimeError(f"{self._command} not found")

        return subprocess.check_output([self.executable, *args], encoding="utf-8").strip()

    def exists(self) -> bool:
        return self.executable is not None

    @property
    def executable(self) -> Optional[str]:
        paths = [str(path / "bin") for path in prefix_paths]
        paths.append(os.environ["PATH"])
        return shutil.which(self._command, path=os.pathsep.join(paths))


class unix_build_ext(build_ext):
    def build_extension(self, extension):
        if extension.name == "_mecab":
            mecab_config = Executable("mecab-config")

            extension.include_dirs.append(mecab_config("--inc-dir"))
            extension.library_dirs.append(mecab_config("--libs-only-L"))
            extension.libraries.append("mecab")

        super().build_extension(extension)


class windows_ext(build_ext):
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
            cxx_std=14,
        ),
    ],
)
