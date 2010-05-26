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

import networkx as nx

USER_COLOR="#ff0000"
USER_SHAPE="octahedron"

PAGE_NEW_COLOR="#ffff00"
PAGE_EDIT_COLOR="#00ff00"
PAGE_IDLE_COLOR="#ffffff"
PAGE_SHAPE="sphere"

EDGE_EDIT_COLOR="#ffffff"
EDGE_LINK_COLOR="#0000ff"

class graph:
    def __init__(self):
        self.__graph = nx.Graph()
        self.__node_updated = []

    def connect_ubigraph(self, server=None):
        self.__graph = nx.UbiGraph(self.__graph, ubigraph_server=server)
        self.__graph.node_labels()

    def add_edit(self, user, page):
        # ADD USER
        if user not in self.__graph:
            self.__graph.add_node( user, color=USER_COLOR, shape=USER_SHAPE )
            self.__graph[user]['ndtype'] = "USER"
        #else:
        #    self.__graph.set_node_attr( user, label=str(user) )
        #self.__node_updated.append(user)

        # Add Page
        if page not in self.__graph:
            self.__graph.add_node( page, color=PAGE_NEW_COLOR, shape=PAGE_SHAPE )
            self.__graph[page]['ndtype'] = "PAGE"
        else:
            self.__graph.set_node_attr( page, label=str(user), color=PAGE_EDIT_COLOR )
        self.__node_updated.append(page)
        
        # Add Edge
        self.__graph.add_edge( user, page, "EDIT", color=EDGE_EDIT_COLOR )
        
    def add_edge( self, a, b ):
        self.__graph.add_edge(a, b)

    def add_links(self, a, b):
        if a not in self.__graph:
            self.__graph.add_node( a, color=PAGE_NEW_COLOR, shape=PAGE_SHAPE )
            self.__graph[a]['ndtype'] = "PAGE"
        else:
            self.__graph.set_node_attr( a, label=str(a), color=PAGE_EDIT_COLOR )
        self.__node_updated.append(a)

        for link in b:
            if link not in self.__graph:
                self.__graph.add_node( link, color=PAGE_IDLE_COLOR, shape=PAGE_SHAPE )
                self.__graph[link]['ndtype'] = "PAGE"
            else:
                self.__graph.set_node_attr( link, label=str(link), color=PAGE_EDIT_COLOR )
            self.__node_updated.append(link)
            self.__graph.add_edge( a, link, "LINK", color=EDGE_LINK_COLOR )

    def do_label_clear(self):
        for node in self.__node_updated:
            self.__graph.set_node_attr( node, label="" )

            if self.__graph[node]['ndtype'] == "PAGE":
                self.__graph.set_node_attr( node, color=PAGE_IDLE_COLOR )
            
        self._node_clear = []
