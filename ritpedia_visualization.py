from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from mediawiki_api import api_call
from ubi_draw import ubi_draw

update = 60

def scheudle_request():
    global api
    api.schedule_page_request().addCallback(page_object_received).addErrback(page_error)

def page_object_received( page_data ):
    if page_data != []:
        global ubi
        for edit in page_data:
            ubi.add_edit( edit['user'], edit['title'] )

def page_error( error ):
    print error

api = api_call( "http://www.rit.edu/studentaffairs/ritpedia/w/api.php" )
ubi = ubi_draw()
lc = LoopingCall(scheudle_request).start(update)

reactor.run()
