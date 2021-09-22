import subprocess
import shlex
import re
import argparse
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", help="refresh bloatware file", action='store_true')
args = parser.parse_args()

# usleep
usleep = lambda x: time.sleep(x/1000000.0)
def rand_sleep():
    randusec=random.randint(100,300)
    randmsec=random.randint(133,333)
    randsec=random.randint(3,5)
    usec=randusec+randmsec*1000+randsec*1000*1000
    print('Waiting for %suSec' % usec)
    usleep(usec)

# config bloatware list
bloat_url='https://raw.githubusercontent.com/khlam/debloat-samsung-android/master/commands.txt'
if args.refresh:
    print('Updating new bloatware list...')
    cmd=f'wget -O bloat_list.txt {bloat_url}'
    ps = subprocess.Popen(shlex.split(cmd),
                      stdout = subprocess.PIPE,
                      stderr = subprocess.STDOUT)
    output, err = ps.communicate()
    assert err is None, err
    print('Done (quitting)')
    quit()

############################################################
# Filter list
############################################################
pkg = re.compile('com.*\.\w*')

filter=[]
with open('filter_list.txt') as fp:
    file_contents = fp.read()
    filter_db=file_contents.splitlines()
    for x in filter_db:
        try:
            m=pkg.search(x).group()
        except:
            pass
    # Found a match
    if m is not None:
        filter.append(m)
print(f'Filter list: {filter}')

############################################################
# DB handling
############################################################
def get_pkt_name(name):
    rand_sleep()
    try:
        response = urllib.request.urlopen(f'https://play.google.com/store/apps/details?id={name}')
        html = response.read()
        soup = BeautifulSoup(html, features="lxml")
        title = soup.title.string.split('-')
        return title[0]
    except:
        return "Unknown"

# init DB
try:
    df = pd.read_csv('bloat_db.csv', header=0, index_col=0)
except:
    df = pd.DataFrame(index=['id'], columns=['desc'])

############################################################
# Bloatware list
############################################################
with open('bloat_list.txt') as fp:
    file_contents = fp.read()
    bloat_list=file_contents.splitlines()

for x in bloat_list:
    try:
        m=pkg.search(x).group()
    except:
        pass
    # Found a match
    if m is not None:
        if m not in filter:
            if m not in df.index:
                name = get_pkt_name(m)
                df.loc[m] = name
                df.to_csv('bloat_db.csv')

