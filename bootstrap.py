#!/usr/local/bin/python3
# ===================================== #
# NAME      : bootstrap.py
# LANGUAGE  : Python
# VERSION   : 3
# AUTHOR    : Bryan Dady
# UPDATED   : 11/4/2019 - added persistent variables output (see line 113)
# INTRO     : To be loaded / dot-sourced from a python profile script, to establish (bootstrap) baseline consistent environment variables,
#             regardless of version, or operating system
# ===================================== #

import argparse
import os
import platform
import sys
import sysconfig
import time
from pathlib import Path

IsVerbose = False
SleepTime = 5

# MyScriptInfo
MyCommandPath = sys.argv[0]
MyCommandName = Path(MyCommandPath).name # requires 'from pathlib import Path'

print('\n ! Start {}: {}'.format(MyCommandName, time.strftime('%Y %m %d %H:%M:%S %Z', time.localtime())))

# format output with some whitespace
# print('\n # # Initiating python environment bootstrap #')
# print(' ... from {}\n'.format(sys.argv[0]))

# http://www.effbot.org/librarybook/os.htm : where are we?
# pwd = os.getcwd()
#print('')
#print('PWD is: ', pwd)

# Region HostOS
# Setup common variables for the shell/host environment

""" # comment block#
    Get-Variable -Name Is* -Exclude ISERecent | FT

    Name                           Value
    ----                           -----
    IsAdmin                        False
    IsCoreCLR                      True
    IsLinux                        False
    IsMacOS                        True
    IsWindows                      False
""" # end of comment block#

IsWindows = False
IsLinux = False
IsMacOS = False
IsAdmin = False
IsServer = False

# Setup OS and version variables
COMPUTERNAME=platform.node()

hostOS = platform.system()
print(' < Platform / hostOS is \'{}\' >'.format(hostOS))
hostOSCaption = platform.platform(aliased=1, terse=1)
print(' < Platform / hostOSCaption (?) is \'{}\' >'.format(hostOSCaption))

if sys.platform == "win32":
    # hostOS = 'Windows'
    IsWindows = True

    #if hostOSCaption -like '*Windows Server*':
    #    IsServer = True

    HOME = os.environ['USERPROFILE']

    # Check admin rights / role; same approach as Test-LocalAdmin function in Sperry module
    #IsAdmin = (([security.principal.windowsprincipal] [security.principal.windowsidentity]::GetCurrent()).isinrole([Security.Principal.WindowsBuiltInRole] 'Administrator'))

elif sys.platform == "mac" or sys.platform == "macos" or sys.platform == "darwin":
    IsMacOS = True
    hostOS = 'macOS'

    #if platform.mac_ver()[0].__len__():
    # Get the macOS major and minor version numbers (first 5 characters of first item in mac_ver dictionary)
    macOS_ver = platform.mac_ver()[0][0:5]
    # https://en.m.wikipedia.org/wiki/List_of_Apple_operating_systems#macOS
    macOS_names = dict({'10.15': 'Catalina', '10.14': 'Mojave', '10.13': "High Sierra", '10.12': 'Sierra', '10.11': 'El Capitan', '10.10': 'Yosemite'})
    hostOSCaption = 'Mac OS X {} {}'.format(macOS_ver, macOS_names[macOS_ver])

    HOME = os.environ['HOME']

    # Check root or sudo
    #IsAdmin =~ ?

else:
    IsLinux = True
    #hostOS = 'Linux'
    hostOSCaption = '{} {}'.format(platform.linux_distribution()[0], platform.linux_distribution()[1])

    HOME = os.environ['HOME']

    # Check root or sudo
    #IsAdmin =~ ?

print(' < HOME is \'{}\' >'.format(HOME))

# if we ever need to confirm that the path is available on the filesystem, use: path.exists(HOME)
py_version =sysconfig.get_config_var('py_version')
print('\n # Python {} on {} - {} #'.format(py_version, hostOSCaption, COMPUTERNAME))

#print('Setting environment HostOS to {}'.format(hostOS)
# Save what we've determined here in shell/system environment variables, so they can be easily referenced from other py scripts/functions
print('\n Here are the persistent variables to import into the next script: ... ')
print('from bootstrap import HOME')
print('from bootstrap import COMPUTERNAME')
print('from bootstrap import hostOS')
print('from bootstrap import hostOSCaption')
print('from bootstrap import IsWindows')
print('from bootstrap import IsLinux')
print('from bootstrap import IsMacOS')

#print('\n # # Python Environment Bootstrap Complete #\n')

"""
    # Get the current locals().items() into a variable, as otherwise it changes during the subsequent for loop
    varList = dict(locals())
    # but remove varList as a key from itself
    #del varList['varList']

    print('List of final variables (locals()):')
    for k, v in varList.items():
        print(f'{k}={v}')
 """

# Uncomment the following line for testing / pausing between profile/bootstrap scripts
#time.sleep( SleepTime )

print('\nEnd : {}\n'.format(time.strftime('%Y %m %d %H:%M:%S %Z', time.localtime())))

#sys.exit(0)
