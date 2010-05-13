from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from mediawiki_api import api_call

update = 60

def scheudle_request():
    global api
    api.schedule_page_request().addCallback(page_received).addErrback(page_error)

def page_received( page ):
    print "PAGE OBJECT",page

def page_error( error ):
    print error

api = api_call( "http://www.rit.edu/studentaffairs/ritpedia/w/api.php" )

lc = LoopingCall(scheudle_request).start(update)

reactor.run()
