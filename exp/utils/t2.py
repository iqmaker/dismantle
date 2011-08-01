lines = open( 't', 'r' ).readlines()
temp = open( 'template', 'r' ).read()

for i in lines:
    res = temp.replace( '%s', i.strip() )
    print res
