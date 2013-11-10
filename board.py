import csp
import node

#coordinate system: (0,0) top left
class Board:
  def __init__(self, s):
    self.length= s
    self.board= [[([],[])]*s for _ in xrange(s)] #board full of spaces
    self.numToCoord_Map= {} #maps the number of a word to its coordinate in "board"
    self.acrossClues= {} #maps number of word to is across clue
    self.downClues= {} #maps number of word to its down clue
    self.solution= [[0]*s for _ in xrange(s)] #contains all the words in proper placement

  
  def genWordsFromBoard(self, csp_cross):
    #Find the beginnings of across words, set their value to (['a'],len of word)
    blanks= False
    curr= None
    count= 0
    for x in range(self.length):
        for y in range(self.length):
            #print "curr", curr
            if self.board[x][y] != None:
                count += 1
                if not(blanks):
                  if y!=self.length-1 and self.board[x][y+1] != None:
                    curr=(x,y)
                    blanks= True
                  else: count= 0
            else:
                blanks= False
                if curr != None:
                    (a,b)= self.board[curr[0]][curr[1]]
                    self.board[curr[0]][curr[1]]= (a+['a'], b+[count])
                    #print "just set board entry (", curr[0], ",", curr[1], ") to", (a+['a'], b+[count])
                    curr= None
                    count= 0
        blanks= False
        if curr != None:
            (a,b)= self.board[curr[0]][curr[1]]
            self.board[curr[0]][curr[1]]= (a+['a'], b+[count])
            #print "just set board entry (", curr[0], ",", curr[1], ") to", (a+['a'], b+[count])
        curr= None
        count= 0

    #Find the beginnings of down words, set their value to (['d'],len of word)
    #If word is also the beginning of a down word, then set value to (['a','d'],len of word)
    blanks= False
    curr= None
    count= 0
    for y in range(self.length):
        for x in range(self.length):
            #print "curr", curr
            if self.board[x][y] != None:
                count += 1
                if not(blanks):
                  if x!=self.length-1 and self.board[x+1][y] != None:
                    curr=(x,y)
                    blanks= True
                  else: count= 0
            else:
                blanks= False
                if curr != None:
                    (a,b)= self.board[curr[0]][curr[1]]
                    self.board[curr[0]][curr[1]]= (a+['d'], b+[count])
                    #print "just set board entry (", curr[0], ",", curr[1], ") to", (a+['d'], b+[count])
                    curr= None
                    count= 0
        blanks= False
        if curr != None:
            (a,b)= self.board[curr[0]][curr[1]]
            self.board[curr[0]][curr[1]]= (a+['d'], b+[count])
            #print "just set board entry (", curr[0], ",", curr[1], ") to", (a+['d'], b+[count])
        curr= None
        count= 0
    #print "before setting word numbers"
    #print self.board


  #Must be called right after genWordsFromBoard
  def setWordNumbers(self, csp_cross):
    #The following nested for loop will:
    #(1) Assign numbers n for each cell that begins a word,
    #(2) Populate numToCoord_Map
    #(3) Add to CSP's across list a node with number n and word length
    #(4) Same as (3) but with down list
    count= 1
    for x in range(self.length):
        for y in range(self.length):
            if self.board[x][y] != None:
                if self.board[x][y][0] != []:
                    self.numToCoord_Map[count]= (x,y)
                    #print self.board[x][y]
                    (a,b)= self.board[x][y]
                    for i in range(len(a)):
                        csp_cross.addNode(node.Node(count,b[i]), a[i])
                        #print "added Node", (count,b[i]), "to", a[i]
                    self.board[x][y]= count
                    count += 1
                else: self.board[x][y]= 0
    #print "num to coord map:", self.numToCoord_Map
    #print "across", csp_cross.across
    #for elem,v in csp_cross.across.iteritems():
      #print v.num, v.len, v.word, v.inters
    #print "down", csp_cross.down
    #for elem,v in csp_cross.down.iteritems():
      #print v.num, v.len, v.word, v.inters


  def calcIntersections(self, csp_cross):
    #Given a board with numbers in proper places, find all intersection points,
    #and for each word number, generate the corresponding constraints and place
    #it in CSP's (and/or the node's) inters field. Can decided whether inters
    #should be a global thing for the whole CSP, or have local inters for each node
    board_copy= [[0]*self.length for _ in xrange(self.length)]
    for key in csp_cross.across:
      (x,y)= self.numToCoord_Map[key]
      count= 0
      while y != self.length and self.board[x][y] != None:
        board_copy[x][y]= (key, count)
        count += 1
        y += 1
    #print board_copy  
    for key in csp_cross.down:
      (x,y)= self.numToCoord_Map[key]
      count= 0
      while x!= self.length and self.board[x][y] != None:
        if(board_copy[x][y] != 0):
          (acr_num, ind)= board_copy[x][y]
          csp_cross.down[key].inters[count]= (acr_num,ind)
          csp_cross.across[acr_num].inters[ind]= (key, count)
        count += 1
        x += 1
    #print "Across:"
    #for elem,v in csp_cross.across.iteritems():
      #print v.num, v.len, v.word, v.inters
    #print "Down:"
    #for elem,v in csp_cross.down.iteritems():
      #print v.num, v.len, v.word, v.inters

    
def main():
    cross= Board(4)
    csp_cross= csp.CSP()
    #define board
    cross.board[0][0]= None
    cross.board[0][2]= None
    cross.board[1][2]= None
    cross.board[2][1]= None
    cross.board[3][1]= None
    cross.board[3][3]= None
    #print cross.board
    cross.genWordsFromBoard(csp_cross)
    cross.setWordNumbers(csp_cross)
    cross.calcIntersections(csp_cross)
    print "Board:", cross.board
    print "Num-to-coord map:", cross.numToCoord_Map
    print "Across:" 
    for k,v in csp_cross.across.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", inters=", v.inters
    print "Down:"
    for k,v in csp_cross.down.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", inters=", v.inters

    print "\n\n~~~NEW BOARD 4x4~~~\n"
    cross= Board(5)
    csp_cross= csp.CSP()
    #define board
    cross.board[0][1]= None
    cross.board[1][1]= None
    cross.board[1][3]= None
    cross.board[1][4]= None
    cross.board[3][0]= None
    cross.board[3][1]= None
    cross.board[3][3]= None
    cross.board[4][3]= None
    #print cross.board
    cross.genWordsFromBoard(csp_cross)
    cross.setWordNumbers(csp_cross)
    cross.calcIntersections(csp_cross)
    print "Board:", cross.board
    print "Num-to-coord map:", cross.numToCoord_Map
    print "Across:" 
    for k,v in csp_cross.across.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", inters=", v.inters
    print "Down:"
    for k,v in csp_cross.down.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", inters=", v.inters
    
    print "\n\n~~~NEW BOARD 6x6~~~\n"
    cross= Board(6)
    csp_cross= csp.CSP()
    #define board
    cross.board[0][0]= None
    cross.board[0][1]= None
    cross.board[1][3]= None
    cross.board[1][4]= None
    cross.board[2][2]= None
    cross.board[2][3]= None
    cross.board[3][2]= None
    cross.board[3][3]= None
    cross.board[4][1]= None
    cross.board[4][2]= None
    cross.board[5][4]= None
    cross.board[5][5]= None
    #print cross.board
    cross.genWordsFromBoard(csp_cross)
    cross.setWordNumbers(csp_cross)
    cross.calcIntersections(csp_cross)
    print "Board:", cross.board
    print "Num-to-coord map:", cross.numToCoord_Map
    print "Across:" 
    for k,v in csp_cross.across.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", inters=", v.inters
    print "Down:"
    for k,v in csp_cross.down.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", inters=", v.inters

    
if __name__=="__main__":
      main()
      
