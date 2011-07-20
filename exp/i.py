lines = open( 'o.html', 'r' ).readlines()
for i in lines:
    print 'UPDATE core_city SET core_city.regional_center="1" WHERE core_city.title="%s";' % i.strip()
