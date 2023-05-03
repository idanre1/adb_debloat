import subprocess
import shlex
import re
import argparse
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# Process:
# run adb_debloat_db.py --refresh      to update bloat_list.txt and appname_list.txt
# run adb_debloat_db.py                to update bloat_db.csv

# Live Databases:
# bloat_list.txt: Bloat list from github live database
# appname_list.txt : List of apps from adb package list
# Manual databases:
# filter_list.txt: Don't remove apps which exists in that list
# Final database of bloatware:
#   bloat_db.csv - id, desc
#   All bloarware with description after passing the filter

# Actual debloat:
# Manually edit app_remove_list.txt
# run adb_debloat_execute.py

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
    print('Done')
    
    print('Updating appname_list.txt from adb package list...')
    adb='/mnt/c/Program Files (x86)/Minimal ADB and Fastboot/adb.exe'
    cmd_ = shlex.split('shell pm list packages -f')
    cmd_.insert(0, adb)
    ps = subprocess.Popen(cmd_,
                      stdout = subprocess.PIPE,
                      stderr = subprocess.STDOUT)
    output, err = ps.communicate()
    assert err is None, err
    
    with open ('appname_list.txt', 'w') as fp:
        fp.write(output.decode('utf-8'))
    
    print('Done (quitting)')

    quit()

############################################################
# Filter list
############################################################
pkg = re.compile('com\w*\.[\w.]*')
appname=re.compile('app/(\w*)/.*\.apk=([\w.]*)')
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
def get_pkg_name(name):
    try:
        return appname_dict[name]
    except KeyError:
        print(f'Quering google for: {name}')
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
    print('INFO: New bloat_db')
    df = pd.DataFrame(index=['id'], columns=['desc'])

############################################################
# Fallback list
############################################################
appname_dict={}
with open('appname_list.txt') as fp:
    file_contents = fp.read()
    appname_list=file_contents.splitlines()
    for name in appname_list:
        s=appname.search(name)
        try:
            appname_dict[s.group(1)]=s.group(2)
        except:
            # Weird names are bypassed
            # e.g. package:/data/app/~~JqssgF-sdhI3iEpU-lY8kg==/com.google.android.youtube-2H0efwML7LMn_1G9pgMV6w==/base.apk=com.google.android.youtube
            pass

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
            try:
                if df.loc[m]['desc'] == 'Unknown':
                    name=get_pkg_name(m)
                    df.loc[m]=name
                    df.to_csv('bloat_db.csv')
            except KeyError:
                name=get_pkg_name(m)
                df.loc[m]=name
                df.to_csv('bloat_db.csv')

