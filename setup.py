import os
import shutil
import subprocess
import sys
from glob import glob
from pathlib import Path

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import find_packages, setup

system_prefix_path = Path(sys.prefix)
user_prefix_path = Path.home() / ".local"


def get_mecab_include_directory() -> str:
    return subprocess.check_output(
        ["mecab-config", "--inc-dir"], encoding="utf-8"
    ).strip()

def get_mecab_library_directory() -> str:
    return subprocess.check_output(
        ["mecab-config", "--libs-only-L"], encoding="utf-8"
    ).strip()


class EnsureMeCabThenBuild(Pybind11Extension):
    def __init__(self, *args, **kwargs):
        self._configure_path()

        if not self._is_mecab_installed():
            self._install_mecab()

        kwargs["include_dirs"] = [get_mecab_include_directory()]
        kwargs["library_dirs"] = [get_mecab_library_directory()]
        kwargs["libraries"] = ["mecab"]
        kwargs["runtime_library_dirs"] = [get_mecab_library_directory()]
        super().__init__(*args, **kwargs)

    def _configure_path(self):
        prefix_paths = [
            system_prefix_path / "bin",
            user_prefix_path / "bin",
        ]
        for path in prefix_paths:
            os.environ["PATH"] += f"{os.pathsep}{path}"

    def _is_mecab_installed(self) -> bool:
        return shutil.which("mecab") is not None

    def _install_mecab(self):
        setup_path = Path(__file__).parent.absolute()
        scripts_path = setup_path / "scripts"
        install_script_path = scripts_path / "install-mecab-ko.py"
        subprocess.check_call(
            [sys.executable, str(install_script_path)], cwd=scripts_path
        )


with open("README.md", "r", encoding="utf-8") as input_file:
    long_description = input_file.read()


setup(
    name="python-mecab-ko",
    version="1.0.14",
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
    data_files=[("scripts", ["scripts/install-mecab-ko.py"])],
    cmdclass={"build_ext": build_ext},
    ext_modules=[
        EnsureMeCabThenBuild(
            name="_mecab",
            sources=sorted(glob("mecab/pybind/**/*.cpp", recursive=True)),
        ),
    ],
)
