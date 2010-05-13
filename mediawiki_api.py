from twisted.web.client import getPage
import json

class api_call:
    def __init__(self, api_url, param="?action=query&format=json&list=recentchanges&rclimit=500&rcprop=timestamp|user|title|flags|loginfo"):
        self._api_base_url = api_url
        self._param_list = param
        self._last_sceen = ""

    def schedule_page_request(self):
        return getPage( "%s%s" % (self._api_base_url, self.get_api_param() ) ).addCallbacks(
            callback=self._page_received, errback=self._page_error)

    def _page_received(self, page):
        data = json.loads( page )

        updates = data['query']['recentchanges']
        self._last_seen = updates[-1]
        print "PAGE RECIEVED"
        return updates

    def _page_error(self, error):
        print "api_call: page_error:", error

    def get_api_param(self):
        if self._last_sceen != "":
            print "LAST SEEN:", self._last_sceen
            return "%s&rcdir=newer&rcstart=%s" % (self._param_list,self._last_sceen)
        else:
            print "NO LAST SEEN"
            return self._param_list

