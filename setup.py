import os
import shutil
import site
import subprocess
import sys
from glob import glob
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from pybind11.setup_helpers import Pybind11Extension
from pybind11.setup_helpers import build_ext as _build_ext
from setuptools import find_packages, setup

prefix_paths = [
    Path(sys.prefix),
    Path(site.getuserbase()),
    Path.home() / ".local",
]


def is_writable(path: Path) -> bool:
    # If path is not directory, find closest parent direcotry
    while not path.is_dir():
        parent = path.parent
        if path == parent:
            break
        path = parent

    return os.access(path, os.W_OK)


def guess_prefix() -> Path:
    for path in prefix_paths:
        if is_writable(path):
            return path.absolute()

    raise RuntimeError("All prefix candidates are not writable")


class Executable:
    def __init__(self, command: str):
        self._command = command

    def __call__(self, *args) -> str:
        return subprocess.check_output(
            [self.executable, *args], encoding="utf-8"
        ).strip()

    def exists(self) -> bool:
        return self.executable is not None

    @property
    def executable(self) -> Optional[str]:
        paths = [str(path / "bin") for path in prefix_paths]
        paths.append(os.environ["PATH"])
        return shutil.which(self._command, path=os.pathsep.join(paths))


class build_ext(_build_ext):
    def build_extension(self, extension):
        if extension.name == "_mecab":
            mecab_config = Executable("mecab-config")
            if not mecab_config.exists():
                self._install_mecab()

            extension.include_dirs.append(mecab_config("--inc-dir"))
            extension.library_dirs.append(mecab_config("--libs-only-L"))
            extension.libraries.append("mecab")

        super().build_extension(extension)

    def _install_mecab(self):
        setup_path = Path(__file__).parent.absolute()
        script_path = setup_path / "scripts" / "install-mecab-ko.py"

        with TemporaryDirectory() as working_directory:
            subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--prefix",
                    str(guess_prefix()),
                ],
                cwd=working_directory,
                check=True,
            )


with open("README.md", "r", encoding="utf-8") as input_file:
    long_description = input_file.read()

setup(
    name="python-mecab-ko",
    version="1.2.4",
    url="https://github.com/jonghwanhyeon/python-mecab-ko",
    author="Jonghwan Hyeon",
    author_email="hyeon0145@gmail.com",
    description="A python binding for mecab-ko",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="mecab mecab-ko",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: Korean",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
    ],
    zip_safe=False,
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=["mecab_ko_dic"],
    package_data={"mecab": ["mecabrc"]},
    data_files=[("scripts", ["scripts/install-mecab-ko.py"])],
    cmdclass={"build_ext": build_ext},
    ext_modules=[
        Pybind11Extension(
            name="_mecab",
            sources=sorted(glob("mecab/pybind/**/*.cpp", recursive=True)),
            include_dirs=["mecab/pybind/_mecab"],
        ),
    ],
)
