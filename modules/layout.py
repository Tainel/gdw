## MODULE - READ LAYOUT

# Module with graph drawing implementation.

#______________________________________________________________________________

# ------ IMPORTS ------ #

import numpy as np
import matplotlib.pyplot as plt

#______________________________________________________________________________

# ------ CLASES ------ #

class Layout:
  """ Necessary information to draw the graph. """
  # Initialization
  def __init__(self, graph, m, a, n, w, v, f, e):
    """ Initialize the information necessary to draw the graph. """
    # Store the graph
    self.graph = graph
    # Store the given options
    self.multiplier = m
    self.animate = a
    self.nodes = n
    self.weights = w
    self.verbose = v
    self.finish = f
    self.extra = e
    # Initialize important constants
    self.dim = 1000
    self.eps = 0.05
    self.temp = 100
    self.cool = 0.96
    # Initialize animation constants
    self.time = 0.025
    self.rfsh = 2
    self.faster = 50
    # Initialize the figure and frame fields
    self.figure = self.frame = None
    # Initialize the optimal dispersion and the margin
    self.k = self.dim/np.math.sqrt(graph.n) if graph.n else 1
    self.margin = self.dim*0.36
    # Initialize the displacement and coordinates of each node
    self.disp = {}
    self.coords = {}
    self.maxr = self.eps
    for node in graph.adj:
      self.disp[node] = np.zeros(2)
      pos = np.random.uniform(-self.dim*0.5,self.dim*0.5,2)
      self.coords[node] = pos
      self.maxr = max(self.maxr,np.linalg.norm(pos))
  # Functions
  def layout(self):
    """ Get the layout of the graph. """
    # Start the execution of the algorithm
    if self.verbose:
      print("Start the algorithm.")
      print("Program options:")
      print("  directed:    %s"%(not self.graph.undirected))
      print("  multiplier:  %s"%self.multiplier)
      print("  animate:     %s"%self.animate)
      print("  nodes:       %s"%self.nodes)
      print("  weights:     %s"%self.weights)
      print("  verbose:     %s"%self.verbose)
      print("  finish:      %s"%self.finish)
      print("  extra:       %d"%self.extra)
      print("Program constants:")
      print("  size of frame:        %d"%self.dim)
      print("  minimum distance:     %g"%self.eps)
      print("  initial temperature:  %g"%self.temp)
      print("  cooling factor:       %g"%self.cool)
      print("Graph information:")
      print("  number of nodes:        %d"%self.graph.n)
      print("  number of drawn edges:  %d"%(self.graph.dm-self.graph.loops))
    # Initialize the figure and frame if necessary
    if self.animate or not self.finish:
      self.figure = plt.figure("Layout",figsize=(6,6))
      self.figure.set_facecolor("#073642")
      self.figure.subplots_adjust(0,0,1,1,0,0)
      self.frame = self.figure.gca()
      self.frame.get_xaxis().set_visible(False)
      self.frame.get_yaxis().set_visible(False)
    # Draw the initial graph
    if self.animate:
      print("Draw the initial graph.") if self.verbose else None
      self.draw()
    # Iterate until the graph is in equilibrium
    if self.verbose:
      print("Iterate until the graph cools down.")
      if self.extra:
        print("Execute the iteration %d times."%(self.extra+1))
      if self.animate:
        print("Do not close \"Layout\" in the meantime.")
    for _ in range(self.extra+1):
      temp = self.temp
      rfsh = self.rfsh
      it = 0
      while self.temp >= self.eps:
        it += 1
        # Compute attractive forces
        self.compute_attraction()
        # Compute repulsive forces
        self.compute_repulsion()
        # Compute gravitational forces
        self.compute_gravity()
        # Update the coordinates of each node
        self.update_coords()
        # Update the drawing if necessary
        if self.animate:
          self.draw() if it%rfsh == 0 else None
          rfsh *= 2 if it%self.faster == 0 else 1
      # Set the temperature to its original value
      self.temp = temp
    # Scale the coordinates to fit inside the frame
    for node in self.graph.adj:
      self.coords[node] *= self.margin/self.maxr
    self.maxr = self.margin
    # Make sure that the last version is shown
    if not self.finish:
      print("Draw the final graph.") if self.verbose else None
      self.draw()
      # Display the final result
      print("Close \"Layout\" when done.") if self.verbose else None
      plt.show()
    # Close the image if necessary
    if self.animate or not self.finish:
      plt.close(self.figure)
      self.figure = self.frame = None
    # End the execution of the algorithm
    print("Finish the algorithm.") if self.verbose else None
  # Auxiliaries
  def compute_attraction(self):
    """ Compute the attractive forces between all neighbours. """
    # For each edge, calculate the attractive forces between both ends
    for edge in self.graph.edges:
      # Calculate the direction and distance
      dif = self.coords[edge[0]]-self.coords[edge[1]]
      dist = np.linalg.norm(dif)
      # Attract only if the nodes are not to close to each other
      if dist >= self.eps:
        atrv = (dist*dif)/self.k
        if self.multiplier:
          atrv *= self.graph.edges[edge][0]
        self.disp[edge[0]] -= atrv
        self.disp[edge[1]] += atrv
  def compute_repulsion(self):
    """ Compute the repulsive forces between all pairs of nodes. """
    # Calculate the repulsion forces between each pair
    used = set()
    for node in self.graph.adj:
      used.add(node)
      # Visit every node that hasn't been completed before
      for other in self.graph.adj:
        if other not in used:
          # Calculate the direction and distance
          dif = self.coords[node]-self.coords[other]
          dist = np.linalg.norm(dif)
          direc = dif
          # If the distance is to small, repel the nodes in a randomly
          if dist < self.eps:
            dist = self.eps
            direc = np.random.uniform(-1,1,2)
            if abs(direc[0]) < self.eps:
              direc[1] = 1
            direc /= np.linalg.norm(direc)
          # Else, normalize the direction
          else:
            direc /= dist
          # Calculate the repulsion force
          repv = (self.k**2*direc)/dist
          self.disp[node] += repv
          self.disp[other] -= repv
  def compute_gravity(self):
    """ Compute the gravitational force in each node. """
    # Calculate the magnitude of gravity
    magn = self.eps
    for node in self.graph.adj:
      magn += np.linalg.norm(self.disp[node])
    magn = max(self.eps,magn/(self.graph.n+1))*0.1
    # Attract each node to the centre of the frame
    for node in self.graph.adj:
      # Calculate the direction and distance
      dif = -self.coords[node]
      dist = np.linalg.norm(dif)
      # Attract only if the node is not to close to the centre
      if dist >= self.eps:
        self.disp[node] += magn*dif/dist
  def update_coords(self):
    """ Update the coordinates of each node. """
    # Initialize the maximum radius
    self.maxr = self.eps
    # For each node, update its position
    for node in self.graph.adj:
      u = self.coords[node]
      disp = self.disp[node]
      magn = np.linalg.norm(disp)
      # Limit the final displacement according to the temperature
      disp *= self.temp/magn if magn > self.temp else 1
      # Update the position of the node
      u += disp
      # Update the maximum radius
      self.maxr = max(self.maxr,np.linalg.norm(u))
      # Reset the displacement to zero
      disp *= 0
    # Update the temperature
    self.temp *= self.cool
  def draw(self):
    """ Draw the graph. """
    # Restart the frame
    self.frame.cla()
    self.frame.axis([-self.dim*0.5,self.dim*0.5,-self.dim*0.5,self.dim*0.5])
    self.frame.set_facecolor("#002B36")
    # Draw the nodes in red
    for node in self.graph.adj:
      u = self.coords[node]*self.margin/self.maxr
      self.frame.scatter(u[0],u[1],color="#DC322F")
      # Write the name of the node if necessary
      if self.nodes:
        self.frame.text(u[0],u[1],node,color="#839496",font="Monospace")
    # Draw the edges in green
    for edge in self.graph.edges:
      if edge[0] != edge[1]:
        arc = {"color":"#859900"}
        arc["arrowstyle"] = "-" if self.graph.undirected else "->"
        u = self.coords[edge[0]]*self.margin/self.maxr
        v = self.coords[edge[1]]*self.margin/self.maxr
        self.frame.annotate("",v,u,arrowprops=arc,annotation_clip=False)
        # Write the total weight of the edge if necessary
        if self.weights:
          w = self.graph.edges[edge][0]
          pos = (u+v)*0.5 if self.graph.undirected else (u+(u+v)*0.5)*0.5
          self.frame.text(pos[0],pos[1],w,color="#839496",font="Monospace")
    # Wait an interval of time after drawing
    plt.pause(self.time)

#______________________________________________________________________________
