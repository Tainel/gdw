## MODULE - GRAPH

# Module with graph implementation.

#______________________________________________________________________________

# ------ CLASES ------ #

class Graph:
  """ General graph. """
  # Initialization
  def __init__(self, undirected=True):
    """ Initialize an empty graph. """
    # Initialize the type of graph
    self.undirected = undirected
    # Initialize the size of the graph and distinct edges and loops
    self.n = self.m = self.dm = self.loops = 0
    # Initialize the adjacency list
    self.adj = {}
    # Initialize the edges
    self.edges = {}
  # Functions
  def add_node(self, node, check=True):
    """ Add a new node. """
    # Check if the edge is new if asked
    if not check or not node in self.adj:
      # Increase the number of nodes
      self.n += 1
      # Add the new node
      self.adj[node] = set()
  def add_edge(self, u, v, w=1., check=True):
    """ Add a new edge. """
    # Check if the edge is valid if asked
    if not check or (u in self.adj and v in self.adj):
      # Increase the number of edges
      self.m += 1
      # Update the adjacency list
      self.adj[u].add(v)
      self.adj[v].add(u) if self.undirected else None
      # Update the edge map
      tup = (u,v)
      if self.undirected and v < u:
        tup = (v,u)
      if tup not in self.edges:
        self.dm += 1
        self.loops += 1 if u == v else 0
        self.edges[tup] = [0,[]]
      info = self.edges[tup]
      info[0] += w
      info[1].append(w)

#______________________________________________________________________________

