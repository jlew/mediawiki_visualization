from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from mediawiki_api import api_call

update = 60


def page_received( page ):
    print "PAGE OBJECT",page

def page_error( error ):
    print error

api = api_call( "http://www.rit.edu/studentaffairs/ritpedia/w/api.php" )

lc = LoopingCall(api.schedule_page_request).start(update).addCallbacks(
            callback=page_received, errback=page_error)

reactor.run()
