#!/usr/bin/env python
# -*- coding:utf-8 -*-
class LinkManager:
    links=[ ('/', 'главная') ]
    currentlink = tuple()
    
    def update(self):
        if self.currentlink in self.links:
            self.links = self.links[:self.links.index( self.currentlink ) + 1]
        else:
            self.links.append( self.currentlink )

    def __init__( self, links=[ ('/', 'главная') ], currentlink=( '/', 'главная' ) ):
        self.links = links
        self.currentlink = currentlink
        self.update() 

    def add_link( self, link ):
        self.currentlink = link
        self.update()
        
    def get_currentlink( self ):
        return self.currentlink

    def get_links( self ):
        return self.links

    def get_render_links( self ):
        result = ''
        for link in self.links:
            result += '<a href="' + link[0] + '">/' + link[1] + '</a>'
        return result



        
