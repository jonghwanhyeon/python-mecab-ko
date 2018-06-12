import subprocess
import sys
import os

from setuptools import setup, find_packages
from setuptools import Extension
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext

# Based on https://github.com/pybind/python_example

base_path = os.path.abspath(os.path.dirname(__file__))

class InstallCommand(install):
    def run(self):
        cwd = os.path.join(base_path, 'scripts')
        subprocess.check_call([
            sys.executable,
            os.path.join(cwd, 'install-mecab.py')
        ], cwd=cwd)

        super().run()


    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

#  Helper classes to postpone importing pybind11 until it is actually installed
class get_pybind_include:
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

#  Helper classes to postpone running mecab-config until it is actually installed
class get_mecab_include_directory:
    def __str__(self):
        return subprocess.check_output(['mecab-config', '--inc-dir']).decode('utf-8').strip()

class get_mecab_library_directory:
    def __str__(self):
        return subprocess.check_output(['mecab-config', '--libs-only-L']).decode('utf-8').strip()

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

extensions = [
    Extension(
        name='_mecab',
        sources=[
            'mecab/pybind/_mecab.cpp'
        ],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            get_mecab_include_directory(),
        ],
        libraries=[
            'mecab',
        ],
        library_dirs=[
            get_mecab_library_directory(),
        ],
        runtime_library_dirs=[
            get_mecab_library_directory(),
        ],
        language='c++',
    ),
]

# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def _has_flag(compiler, flag):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as output_file:
        output_file.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([output_file.name], extra_postargs=[flag])
        except setuptools.distutils.errors.CompileError:
            return False

    return True

def _cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available).
    """
    if _has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif _has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support is needed!')

class BuildExtensionCommand(build_ext):
    compiler_options = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        compiler_options['unix'] += [
            '-stdlib=libc++',
            '-mmacosx-version-min=10.7',
        ]

    def build_extensions(self):
        compiler_type = self.compiler.compiler_type
        options = self.compiler_options.get(compiler_type, [])

        if compiler_type == 'unix':
            options.append('-DVERSION_INFO="{}"'.format(self.distribution.get_version()))
            options.append(_cpp_flag(self.compiler))

            if _has_flag(self.compiler, '-fvisibility=hidden'):
                options.append('-fvisibility=hidden')
        elif compiler_type == 'msvc':
            options.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())

        for extension in self.extensions:
            extension.extra_compile_args = options

        super().build_extensions()

setup(
    name='python-mecab-ko',
    version='1.0.0',
    url='https://github.com/hyeon0145/python-mecab-ko',
    author='Jonghwan Hyeon',
    author_email='hyeon0145@gmail.com',
    description='A python binding for mecab-ko',
    license='BSD',
    keywords='mecab mecab-ko',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Korean',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    zip_safe=False,
    install_requires=[
        'pybind11 ~= 2.0'
    ],
    python_requires='>=3',
    packages=find_packages(),
    data_files=[('scripts', ['scripts/install-mecab.py'])],
    ext_modules=extensions,
    cmdclass={
        'install': InstallCommand,
        'build_ext': BuildExtensionCommand
    },
)