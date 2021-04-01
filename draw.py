## SCRIPT - GRAPH DRAWING

# Script for graph drawing.

#______________________________________________________________________________

# ------ IMPORTS ------ #

from modules.graph import Graph
from modules.read import read_graph
from modules.layout import Layout
import argparse as argp

#______________________________________________________________________________

# ------ MAIN ------ #

def main():
  """ Main function for graph drawing. """
  # Parse the command line arguments
  args = parse_arguments()
  # Create a graph and read from given file
  graph = read_graph(args.file,Graph(not args.d))
  # Execute the layout of the graph with the given command line options
  Layout(graph,args.m,args.a,args.n,args.w,args.v,args.f,args.e).layout()

#______________________________________________________________________________

# ------ FUNCTIONS ------ #

def parse_arguments():
  """ Parse command line arguments. """
  # Initialize allowed command line arguments
  parser = argp.ArgumentParser(description="Draws the given graph.")
  # Define mandatory arguments
  parser.add_argument("file",help="file that contains the graph")
  # Define optional arguments
  parser.add_argument("-d","--directed",action="store_true",dest="d",
  help="determine if the graph is directed")
  parser.add_argument("-m","--multiplier",action="store_true",dest="m",
  help="determine if the weights affect the attraction")
  parser.add_argument("-a","--animate",action="store_true",dest="a",
  help="show how the graph reaches its final configuration")
  parser.add_argument("-n","--nodes",action="store_true",dest="n",
  help="show the names of each node")
  parser.add_argument("-w","--weights",action="store_true",dest="w",
  help="show the weight of each edge")
  parser.add_argument("-v","--verbose",action="store_true",dest="v",
  help="show additional information during execution")
  parser.add_argument("-f","--finish",action="store_true",dest="f",
  help="finish execution after finding the layout")
  parser.add_argument("-e","--extra",action="count",default=0,dest="e",
  help="number of additional executions")
  # Return parsed arguments
  return parser.parse_args()

#______________________________________________________________________________

# ------ EXECUTION ------ #

if __name__ == '__main__':
  # Execute main function
  main()

#______________________________________________________________________________
