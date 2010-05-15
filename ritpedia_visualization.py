#    Mediawiki Visualization is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MediaWiki Visualization is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MediaWiki Visualization.  If not, see <http://www.gnu.org/licenses/>.
#
#    Author: Justin Lewis  <jlew.blackout@gmail.com>
#
#    I would like to thank Taylor Rose <tjr1351@rit.edu> for initial jumpstart
#    of twisted reactor.
#
#    This project was inspired by Remy DeCausemaker <remyd@civx.us> and
#    John Shull <jon.schull@rit.edu> of the Student Innovation Center @ RIT

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from optparse import OptionParser

from mediawiki_api import api_call
from ubi_draw import ubi_draw

def schedule_request():
    global api
    api.schedule_change_request().addCallback(page_object_received).addErrback(page_error)

def page_object_received( page_data ):

    global ubi
    ubi.do_label_clear()
    if page_data != []:
        global options

        page_links = []

        for edit in page_data:
            if options.show_users:
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


parser = OptionParser()
parser.add_option("-a", "--api", dest="api_link", help="API Url",
    metavar="URL", default="http://www.rit.edu/studentaffairs/ritpedia/w/api.php")

parser.add_option("-u", "--ubi_server", dest="ubi_server",
    help="ubidraw server url", metavar="URL", default="http://localhost:20738/RPC2")

parser.add_option("-i", "--interval", dest="interval", type="int",
    help="Minutes between api calls", metavar="MIN", default=5)

parser.add_option("","--no-users", dest="show_users", action="store_false", default=True,
                  help="Hide users from visualization")

(options, args) = parser.parse_args()

api = api_call( options.api_link )

try:
    ubi = ubi_draw( options.ubi_server )
except:
    print "ubigraph server doesn't appear to be running"
    import sys
    sys.exit(1)

lc = LoopingCall(schedule_request).start(options.interval * 60)

reactor.run()


