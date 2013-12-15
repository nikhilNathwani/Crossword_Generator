
class Node:
  def __init__(self, num, len, coords):
      self.num= num
      self.coords= coords
      self.len= len
      self.word= ["?" for _ in xrange(len)]
      self.intersections= [None]*len 
      self.possibleWords= []
      self.parents = []
      self.children=[]


