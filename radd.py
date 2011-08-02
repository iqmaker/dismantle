import os
extensions = [ 'html', 'py', 'js' ]
for e in extensions:
    command = 'find -name "*.%s" | xargs git add' % e
    print command
    os.system( command )
