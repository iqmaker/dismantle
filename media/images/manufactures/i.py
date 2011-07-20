import os

for j, i in enumerate(open( "makes.txt", "r" )):
    i = i.replace( "-", "_" ).strip().lower()
    #print "result #%s = %s" % ( j, i )
    i = '_'.join( i.split( ' ' ) )
    fin, fout = os.popen4( "find ./big -name '*%s*'" % i )
    fin1, fout1 = os.popen4( "find ./big -name '%s.png'" % i )
    data = fout.read().strip()
    data1 = fout1.read().strip()

    if data and not data1:
        print "%s" % i
#        print data
    #if result != 0:
    #    print "%s not found" % i.strip()
