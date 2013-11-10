
class Node:
  def __init__(self, num, len):
      self.num= num
      self.len= len
      self.word= [" " for _ in xrange(len)]
      self.inters= [None]*len #might not need this


