# adb_debloat
Remove bloatware from Android devices without root using python
# Wrapper tools
This repo gets its bloat list from: https://github.com/khlam/debloat-samsung-android
Kudos for making the list live and up to date.
The wrapper tools are tested on samsung phones but can easily adapted to other makers.
Mainly the repo filters bloat list and try to keep description of every software ID.
# WSL 1
The wrapper tools is written in python using WSL1, why?
1. You have native linux python
2. WSL1 can execute adb.exe file
## WSL2 howto
ADB is actually 2 components, and daemon that does the device communication and a client that talks to the daemon over a local network socket.
So first install the exact same version of ADB in both Windows and WSL, then start the ADB daemon in Windows (just by running 'adb devices'). Then in ADB in WSL it should automatically use the already running daemon and be able to talk to your devices normally.
# ADB mini driver
You don't have to instal full andoroid SDK for only debloat.
https://androidmtk.com/download-minimal-adb-and-fastboot-tool
