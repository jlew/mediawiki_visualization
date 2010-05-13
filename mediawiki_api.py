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

from twisted.web.client import getPage
from twisted.internet import defer
import json

CHANGE_PARAM = "?action=query&format=json&list=recentchanges&rclimit=500&rcprop=timestamp|user|title|flags|loginfo"
LINK_PARAM = "?action=query&format=json&prop=links&titles=%s&pllimit=50"
class api_call:
    def __init__(self, api_url):
        self._api_base_url = api_url
        self._last_scene = ""

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
        returns the update data to the defered_chain as a callback.  If no new
        data was found it will pass an empty list to the callback.
        """
        data = json.loads( page )

        updates = data['query']['recentchanges']

        if len( updates ) != 0:
            self._last_scene = updates[-1]

            defered_chain.callback( updates )
        else:
            # This means it is the same update we have seen, send empty array chain
            defered_chain.callback( [] )

    def _link_received(self, page, defered_chain):
        data = json.loads( page )

        defered_chain.callback( data['query']['pages'] )

    def _page_error(self, error, defered_chain):
        """
        Error handler for getPage.  Passes the error as an errback on the defered_chain
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

