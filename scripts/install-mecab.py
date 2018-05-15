import os
import subprocess
import sys

from urllib.request import urlopen

MECAB_KO_URL = 'https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz'
MECAB_KO_DIC_URL = 'https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.3-20170922.tar.gz'

base_path = os.path.abspath(os.path.dirname(__file__))

print('Installing mecab-ko...')
subprocess.check_call(['wget', '--progress=dot:binary', MECAB_KO_URL])
subprocess.check_call(['tar', 'xvfz', 'mecab-0.996-ko-0.9.2.tar.gz'])

cwd = os.path.join(base_path, 'mecab-0.996-ko-0.9.2')
subprocess.check_call([
    os.path.join(cwd, 'configure'),
    '--prefix={}'.format(sys.prefix),
    '--enable-utf8-only'
], cwd=cwd)
subprocess.check_call(['make'], cwd=cwd)
subprocess.check_call(['make', 'install'], cwd=cwd)

print('Installing mecab-ko-dic...')
subprocess.check_call(['wget', '--progress=dot:binary', MECAB_KO_DIC_URL])
subprocess.check_call(['tar', 'xvfz', 'mecab-ko-dic-2.0.3-20170922.tar.gz'])

cwd = os.path.join(base_path, 'mecab-ko-dic-2.0.3-20170922')
subprocess.check_call([
    os.path.join(cwd, 'configure'),
    '--prefix={}'.format(sys.prefix),
    '--with-charset=utf8',
    '--with-mecab-config={}'.format(os.path.join(sys.prefix, 'bin', 'mecab-config')),
], cwd=cwd)
subprocess.check_call(['make'], cwd=cwd)
subprocess.check_call(['make', 'install'], cwd=cwd)