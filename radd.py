#!/usr/bin/env python
import os
#find -type d -exec git add {} \; 
extensions = [ 'html', 'py', 'js', 'png' ]
for e in extensions:
    command = 'find -name "*.$e" -exec git add {} \;'
    os.system( command )
