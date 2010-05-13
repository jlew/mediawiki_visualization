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
            self._pages[page] = [self._g.newVertex( label=page ), []]

        if user not in self._pages[page][1]:
            self._pages[page][1].append(self._g.newEdge(self._pages[page][0],self._users[user]))
