#    Mediawiki Visulization is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenVideoChat is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OpenVideoChat.  If not, see <http://www.gnu.org/licenses/>.
#
#    Author: Justin Lewis  <jlew.blackout@gmail.com>

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
