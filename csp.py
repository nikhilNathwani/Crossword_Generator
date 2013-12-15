import board
import node
import random
import gui
import scrape
import Tkinter as tk


class CSP:
  def __init__(self):
      self.across= {}
      self.down= {}
      self.allWords= {'a': self.across, 'd': self.down}
      self.needWords= []
      self.gotWords= []
      self.root= None

  #direc: 'a'= across, 'd'=down
  def addNode(self, node, direc):
      if direc in ['a','d']:
      	self.allWords[direc][node.num]= node
      self.needWords += [(direc,node.num)]




  #just picks words randomly, no backtracking or anything
  #if a word gets filled up before being chosen, doesn't confirm whether it's actually a word (e.g. "AAG")
  def solveCSP(self):
    while(len(self.needWords)!=0):
      direc,wordNum= random.choice(self.needWords) #!!!!!
      opposite= 'd' if direc=='a' else 'a'
      node= self.allWords[direc][wordNum]
      self.root= node
      if node.word==[" " for _ in xrange(node.len)]:
        index= random.randint(0,node.len-1)
        node.word[index]= 'a'
      query= ''.join(node.word)
      possibleWords= scrape.getPossibleWords(query)
      while possibleWords==[]: 
        print query,"oh noooo"
        for inter in node.intersections:
          if inter:
            num, intPoint= inter 
            if (opposite,num) in self.gotWords:
              prolemNode= self.allWords[opposite][num]
              allIntPoints= [i for (i,val) in enumerate(problemNode.intersections) if val!=None]





      else: 
        print possibleWords
        node.possibleWords= possibleWords
        node.word= list(random.choice(node.possibleWords))   #!!!!!
        for ind,inter in enumerate(node.intersections):
          if inter!=None: 
            num,spot= inter
            interNode= self.allWords[opposite][num]
            interNode.word[spot]= node.word[ind]
      self.needWords.remove((direc,wordNum))
      self.gotWords += [(direc,wordNum)]
    
  def printWordsToGui(self,board):
    for direc,wordNum in self.gotWords:
      node= self.allWords[direc][wordNum]
      xCoord= node.coords[0]
      yCoord= node.coords[1]
      print node.word
      if direc=='a':
        board.acrossClues[wordNum]= scrape.getClue(''.join(map(str, node.word)))
        for i in range(node.len):
          board.solution[xCoord][yCoord+i]= node.word[i]
      else: 
        board.downClues[wordNum]= scrape.getClue(''.join(map(str, node.word)))
        for i in range(node.len):
          board.solution[xCoord+i][yCoord]= node.word[i]
    for row in board.solution: 
      print row

    
def main():
    cross= board.Board(7)
    csp_cross= CSP()
    #define board
    cross.board[0][1] = None
    cross.board[1][1] = None
    cross.board[2][1] = None
    cross.board[4][0] = None
    cross.board[4][1] = None
    cross.board[4][2] = None
    cross.board[4][3] = None
    cross.board[5][1] = None
    cross.board[5][3] = None
    cross.board[3][3] = None
    cross.board[2][3] = None
    cross.board[2][4] = None
    cross.board[2][5] = None
    cross.board[2][6] = None
    cross.board[1][3] = None
    cross.board[1][5] = None
    cross.board[6][5] = None
    cross.board[5][5] = None
    cross.board[4][5] = None
    #print cross.board
    cross.genWordsFromBoard(csp_cross)
    cross.setWordNumbers(csp_cross)
    cross.calcIntersections(csp_cross)
    print "Board:", cross.board
    print "Num-to-coord map:", cross.numToCoord_Map
    print "Across:" 
    for k,v in csp_cross.across.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", inters=", v.intersections
    print "Down:"
    for k,v in csp_cross.down.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", inters=", v.intersections

    print "Solving CSP:"
    #csp_cross.solveCSP()
    print "Across:" 
    for k,v in csp_cross.across.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", intersections=", v.intersections
    print "Down:"
    for k,v in csp_cross.down.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", intersections=", v.intersections
    print "\n\n"
    #csp_cross.printWordsToGui(cross)


#GUI STUFF
    root = tk.Tk()
    root.resizable(False, False)
    leftFrame= tk.Frame(root)
    rightFrame= tk.Frame(root)
    gameboard = gui.GameBoard(leftFrame, cross, cross.solution, 7*80)
    clues= gui.Clues(rightFrame, cross.acrossClues, cross.downClues, 7*6)

    leftFrame.pack(side="left")
    rightFrame.pack(side="right")
    gameboard.canvas.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    clues.text.pack(side="right")
    root.mainloop()
    
if __name__=="__main__":
      main()