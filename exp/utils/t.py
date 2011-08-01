lines = open( 't', 'r' ).readlines()

for i in lines:
    res = "'%s':d.%s," %  (i.strip(), i.strip() )
    print res
