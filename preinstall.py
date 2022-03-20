import os
import sys
# import subprocess
import pkg_resources
# import platform

required = {'pygame', 'pytmx'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

def install_python_package(package):
    os.system(f'python -m pip install {package}')

if missing:
    for module in missing:
        install_python_package(module)

import main
sys.exit()
