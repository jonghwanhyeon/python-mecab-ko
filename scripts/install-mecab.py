import os
import subprocess
import sys

from tempfile import TemporaryDirectory
from urllib.parse import urlparse

MECAB_KO_URL = 'https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz'
MECAB_KO_DIC_URL = 'https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.3-20170922.tar.gz'


def print_title(text):
    print('\033[1m',  # bold
          '\033[32m',  # green foreground
          text,
          '\033[0m',  # reset
          sep='')


def directory_of(filename, base):
    for directory, _, filenames in os.walk(base):
        if filename in filenames:
            return directory

    raise ValueError('File {} not found'.format(filename))


def prepare(url, base):
    components = urlparse(url)
    filename = os.path.basename(components.path)

    subprocess.check_call([
        'wget',
        '--progress=dot:binary',
        '--output-document={}'.format(filename),
        url,
    ], cwd=base)
    subprocess.check_call(['tar', '-xzf', filename], cwd=base)


def configure(*args, base):
    path = directory_of('configure', base=base)

    subprocess.check_call([
        os.path.join(path, 'configure'),
        *args,
    ], cwd=path)


def install(base):
    path = directory_of('Makefile', base=base)

    subprocess.check_call(['make'], cwd=path)
    subprocess.check_call(['make', 'install'], cwd=path)


print_title('Installing mecab-ko...')
with TemporaryDirectory() as working_directory:
    prepare(MECAB_KO_URL, base=working_directory)
    configure('--prefix={}'.format(sys.prefix),
              '--enable-utf8-only',
              base=working_directory)
    install(base=working_directory)

print_title('Installing mecab-ko-dic...')
with TemporaryDirectory() as working_directory:
    mecab_config_path = os.path.join(sys.prefix, 'bin', 'mecab-config')

    prepare(MECAB_KO_DIC_URL, base=working_directory)
    configure('--prefix={}'.format(sys.prefix),
              '--with-charset=utf8',
              '--with-mecab-config={}'.format(mecab_config_path),
              base=working_directory)
    install(base=working_directory)
