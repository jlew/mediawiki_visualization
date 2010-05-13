from twisted.web.client import getPage
from twisted.internet import defer
import json

class api_call:
    def __init__(self, api_url, param="?action=query&format=json&list=recentchanges&rclimit=500&rcprop=timestamp|user|title|flags|loginfo"):
        self._api_base_url = api_url
        self._param_list = param
        self._last_scene = ""

    def schedule_page_request(self):
        d = defer.Deferred()
        getPage( "%s%s" % (self._api_base_url, self.get_api_param() )).addCallback(self._page_received, d ).addErrback(self._page_error, d)
        return d

    def _page_received(self, page, defered_chain):
        data = json.loads( page )

        updates = data['query']['recentchanges']

        if len( updates ) != 0:
            self._last_scene = updates[-1]

            defered_chain.callback( updates )
        else:
            # This means it is the same update we have seen, send empty array chain
            defered_chain.callback( [] )

    def _page_error(self, error, defered_chain):
        defered_chain.errback( error )

    def get_api_param(self):
        if self._last_scene != "":
            return "%s&rcdir=newer&rcstart=%s" % (self._param_list,self._last_scene)
        else:
            return self._param_list

