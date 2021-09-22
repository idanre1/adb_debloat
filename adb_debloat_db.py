import subprocess
import shlex
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", help="refresh bloatware file", action='store_true')
args = parser.parse_args()


# Config adb command
# This is WSL1, for WSL2 some adjustments are needed. visit the README.md
adb='/mnt/c/Program Files (x86)/Minimal ADB and Fastboot/adb.exe'
def exe(cmd):
    cmd_ = shlex.split(cmd)
    cmd_.insert(0, adb)
    ps = subprocess.Popen(cmd_,
                      stdout = subprocess.PIPE,
                      stderr = subprocess.STDOUT)
    output, err = ps.communicate()
    assert err is None, err
    return output.decode('utf-8')

# config bloatware list
bloat='https://raw.githubusercontent.com/khlam/debloat-samsung-android/master/commands.txt'
if args.refresh:
    print('Updating new bloatware list...')
    cmd=f'wget -O commands.txt {bloat}'
    ps = subprocess.Popen(shlex.split(cmd),
                      stdout = subprocess.PIPE,
                      stderr = subprocess.STDOUT)
    output, err = ps.communicate()
    assert err is None, err
    print('Done (quitting)')
    quit()

############################################################
# List devices
############################################################
print(exe('devices'))
# Test for connected device
out = exe('shell pm list package')
err = re.search("error: no devices.emulators found", out)
assert err is None, 'FATAL: No device is connected to adb'

