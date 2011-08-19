#!/usr/bin/env python
import os
os.system( "mysql -u root --execute='drop database dismantle'" )
os.system( "mysql -u root --execute='create database dismantle'" )
os.system( "(cd ../; ./manage.py syncdb)" )
os.system( "python init.py" )

