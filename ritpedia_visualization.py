from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from mediawiki_api import api_call
from ubi_draw import ubi_draw

update = 60

def scheudle_request():
    global api
    api.schedule_change_request().addCallback(page_object_received).addErrback(page_error)

def page_object_received( page_data ):
    if page_data != []:
        global ubi

        page_links = []
        for edit in page_data:
            ubi.add_edit( edit['user'], edit['title'] )
            page_links.append( edit['title'] )

        link_set = list( set( page_links ) )

        global api
        for x in range(0, len( link_set ), 10):
            api.schedule_link_request( link_set[x:x+10] ).addCallback( page_link_received ).addErrback(page_error)

def page_link_received( links_map ):
    global ubi
    for page in links_map.values():
        if page.has_key('links'):
            ubi.add_page_links( page['title'], page['links'] )


def page_error( error ):
    print error

api = api_call( "http://www.rit.edu/studentaffairs/ritpedia/w/api.php" )
try:
    ubi = ubi_draw()
except:
    print "ubigraph server doesn't appear to be running"
    import sys
    sys.exit(1)

lc = LoopingCall(scheudle_request).start(update)

reactor.run()
