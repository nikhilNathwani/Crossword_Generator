
class Node:
  def __init__(self, num, length, coords):
      self.num= num
      self.coords= coords
      self.len= length
      self.word= ["?" for _ in xrange(length)]
      self.intersections= [None]*length 
      self.possibleWords= []
      self.ratio= (0,len(self.word))
      self.num_retry = 1
      self.priority = 1

  def addLetter(self,index, letter):
    self.word[index]= letter
    fil,unfil= self.ratio
    self.ratio= (fil+1,len(self.word))

