import subprocess
import shlex
import re

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

############################################################
# List devices
############################################################
print(exe('devices'))
# Test for connected device
out = exe('shell pm list package')
err = re.search("error: no devices.emulators found", out)
assert err is None, 'FATAL: No device is connected to adb'

############################################################
# Remove
############################################################
with open('removal_list.txt') as fp:
    file_contents = fp.read()
    db=file_contents.splitlines()
    for pkg in db:
        out=exe('shell pm uninstall -k --user 0 %s' % pkg)
        print(f'{pkg} {out}')