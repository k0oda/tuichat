#!python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'tuichat==0.6.3','console_scripts','tuiserver'
__requires__ = 'tuichat==0.6.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('tuichat==0.6.3', 'console_scripts', 'tuiserver')()
    )
