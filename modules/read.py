## MODULE - READ GRAPH

# Module with graph reading implementation.

#______________________________________________________________________________

# ------ IMPORTS ------ #

from .graph import Graph
import sys

#______________________________________________________________________________

# ------ FUNCTIONS ------ #

def read_graph(filePath, graph=None):
  """ Read a graph from a file that contains its nodes and edges. """
  # Initialize the graph if necessary
  if graph is None:
    graph = Graph()
  # Try reading the graph
  try:
    with open(filePath) as fp:
      # Read each line of the file
      l = 1
      for line in fp:
        # Split the line
        parts = line.split()
        num = len(parts)
        # If line is not empty, parse it
        if num:
          # If the line has only one part, it's a node
          if num == 1:
            # If the node is unique, add it to the graph
            if parts[0] not in graph.adj:
              graph.add_node(parts[0],False)
            # Else, treat the error
            else:
              sys.exit("ERROR: Node in line %d is repeated."%l)
          # Else, if the line has at most three parts, it's an edge
          elif num <= 3:
            # If the edge has no weight, it's weight is 1
            parts.append(1.) if num == 2 else None
            # Try converting the weight to a number
            try:
              parts[2] = float(parts[2])
            # If it's not a number, treat the error
            except ValueError:
              sys.exit("ERROR: weight in line %d is invalid."%l)
            # Add the edge if it's valid
            if parts[0] in graph.adj and parts[1] in graph.adj:
              graph.add_edge(parts[0],parts[1],parts[2],False)
            # Else, treat the error
            else:
              sys.exit("ERROR: Edge in line %d is invalid."%l)
          # Else, treat the error
          else:
            sys.exit("ERROR: Line %d is invalid."%l)
        l += 1
  # Treat the error if file couldn't be open
  except OSError:
    sys.exit("ERROR: File cannot be opened.")
  # Return the graph
  return graph

#______________________________________________________________________________

