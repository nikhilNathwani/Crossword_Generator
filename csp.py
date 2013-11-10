import board
import node

class CSP:
  def __init__(self):
      self.across= {}
      self.down= {}
      self.inters= {} #might not need this

  #direc: 'a'= across, 'd'=down
  def addNode(self, node, direc):
      if direc=='a': self.across[node.num]= node
      if direc=='d': self.down[node.num]= node

  
      
    
