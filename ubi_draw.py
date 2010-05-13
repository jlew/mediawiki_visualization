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
#    along with MediaWiki Visualization, see <http://www.gnu.org/licenses/>.
#
#    Author: Justin Lewis  <jlew.blackout@gmail.com>

import ubigraph

class ubi_draw:
    def __init__(self, server="http://localhost:20738/RPC2"):
        self._g = ubigraph.Ubigraph(server)
        self._g.clear()
        self._users = {}
        self._pages = {}

    def add_edit(self, user, page):

        if not self._users.has_key( user ):
            self._users[user] = self._g.newVertex(shape="octahedron", color="#ff0000", label=user)

        if not self._pages.has_key(page):
            self._pages[page] = [self._g.newVertex( label=page ), [], []]

        if user not in self._pages[page][1]:
            self._pages[page][1].append(self._g.newEdge(self._pages[page][0],self._users[user], color="#ffffff", width=2.0))

    def add_page_links(self, page, links):
        for link in links:
            self.page_to_page( page, link['title'] )


    def page_to_page( self, a, b ):
        if not self._pages.has_key(a):
            self._pages[a] = [self._g.newVertex( label=a ), [], []]

        if not self._pages.has_key(b):
            self._pages[b] = [self._g.newVertex( label=b ), [], []]

        if  self._pages[b][0] not in self._pages[a][2]:
            self._pages[a][2].append(self._g.newEdge( self._pages[a][0], self._pages[b][0], color="#ffff00", width=2.0))
