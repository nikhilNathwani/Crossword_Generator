
class Node:
  def __init__(self, num, length, coords):
      self.num= num
      self.coords= coords
      self.len= length
      self.word= ["?" for _ in xrange(length)]
      self.intersections= [None]*length 
      self.possibleWords= []
      self.ratio= (0,len(self.word))

  def addLetter(self,index, letter):
    #numQs= sum([1 for letter in self.word if letter=="?"])
    self.word[index]= letter
    fil,denom= self.ratio
    #numQsNew= sum([1 for letter in self.word if letter=="?"])
    #if numQs != numQsNew: 
    self.ratio= (fil+1,len(self.word))

  def resetNode(self):
    interIndices= [i for i,tup in enumerate(self.intersections) if tup!=None]
    for index, letter in enumerate(self.word):
      if index in interIndices:
        self.word[index]= "?"

