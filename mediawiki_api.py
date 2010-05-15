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
#    I would like to thank Fran Rogers <fran@dumetella.net> for api support.

from twisted.web.client import getPage
from twisted.internet import defer
import json
import os
from time import time

CHANGE_PARAM = "?action=query&format=json&list=recentchanges&rclimit=500&rcprop=timestamp|user|title|flags|loginfo"
LINK_PARAM = "?action=query&format=json&prop=links&titles=%s&pllimit=50"
class api_call:
    def __init__(self, api_url, cache="./cache"):
        self._api_base_url = api_url
        self._last_scene = ""

        # Ensure that the cache directory exists
        self._cache = {
                'edits':os.path.join( cache, "page_edits" ),
                'links':os.path.join( cache, "page_links" ),
                }

        if not os.path.isdir( cache ):
            os.mkdir( cache )

        for key in self._cache:
            if not os.path.isdir( self._cache[key] ):
                os.mkdir( self._cache[key] )

    def schedule_change_request(self):
        """
        gets the page from the api, and then passes the data the _page_received
        callback.

        Returns a deferred object which _page_received will use as a callback
        """
        d = defer.Deferred()
        getPage( "%s%s" % (self._api_base_url, self.get_api_param() )).addCallback(self._change_received, d ).addErrback(self._page_error, d)
        return d

    def schedule_link_request(self, links):
        link_list = str("|".join(links))
        d = defer.Deferred()
        getPage( "%s%s" % (self._api_base_url, LINK_PARAM % link_list )).addCallback(self._link_received, d ).addErrback(self._page_error, d)
        return d


    def _change_received(self, page, defered_chain):
        """
        returns the update data to the deferred_chain as a callback.  If no new
        data was found it will pass an empty list to the callback.
        """
        data = json.loads( page )

        updates = data['query']['recentchanges']

        if len( updates ) != 0:
            self._last_scene = str(updates[0]['timestamp'])

            self._cache_add( 'edits', page )
            defered_chain.callback( updates )
        else:
            # This means it is the same update we have seen, send empty array chain
            defered_chain.callback( [] )

    def _link_received(self, page, defered_chain):
        data = json.loads( page )

        self._cache_add( 'links', page )

        defered_chain.callback( data['query']['pages'] )

    def _page_error(self, error, defered_chain):
        """
        Error handler for getPage.  Passes the error as an errback on the deferred_chain
        """
        defered_chain.errback( error )

    def get_api_param(self):
        """
        returns the current param list string
        """
        if self._last_scene != "":
            return "%s&rcdir=newer&rcstart=%s" % (CHANGE_PARAM,self._last_scene)
        else:
            return CHANGE_PARAM

    def _cache_add(self, type, page_data):
        assert( self._cache.has_key( type ) )
        u = 0
        t = time()

        while os.path.exists( os.path.join( self._cache[type], "%s_%d" % (t,u) ) ):
            u = u + 1

        f = file( os.path.join( self._cache[type], "%s_%d" % (t,u) ), 'w')
        f.write( page_data )
        f.close()
