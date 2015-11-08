import sys
import os
from distutils.sysconfig import get_python_lib
import subprocess


if getattr(sys, "real_prefix", None) is None:
    print("You should run this script only form virtual environment.")
    sys.exit()

try:
    appcfg_path = subprocess.check_output(['which', 'appcfg.py'])
except subprocess.CalledProcessError:
    print(
        "appcfg.py script was not found. GAE SDK is not installed or "
        "not configured correctly."
    )
    sys.exit()

print("Installing lib requirements.")
print(subprocess.check_output(
    ['pip', 'install', '--upgrade', '-r', 'lib_requirements.txt', '-t',
     'src/lib/']
))

print("Creating local datastore directory.")
subprocess.call(['mkdir', '-p', 'datastore'])

print("Linking project dependencies to your virtual environment.")
site_packages_dir = get_python_lib()
gae = os.path.dirname(appcfg_path)
current_dir = os.path.dirname(os.path.realpath(__file__))
extra_pth = {
    'gae': gae,
    'django': os.path.join(gae, 'lib', 'django-1.5'),
    'project-src': os.path.join(current_dir, 'src'),
    'project-lib': os.path.join(current_dir, 'src', 'lib'),
}

for key, value in extra_pth.items():
    file_name = os.path.join(site_packages_dir, key + '.pth')
    print("'{}' path was written to '{}' file.".format(value, file_name))
    with open(file_name, 'w') as f:
        f.write(value)
        f.write('\n')

print("\n\nSuccess!")
