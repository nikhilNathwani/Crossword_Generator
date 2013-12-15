import board
import node
import random
import gui
import scrape
import Tkinter as tk
import time

alphabet= ['A','E','O','S','T','I']
 
scrabble_val = {'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,
            'J':8,'K':5,'L':1, 'M':3,'N':1,'O':1,'P':3,'Q':10,'R': 1,
            'S': 1,'T': 1, 'U': 1, 'V': 4,'W': 4,'X': 8,'Y': 4,'Z':10}

class CSP:
  def __init__(self):
      self.across= {}
      self.down= {}
      self.allWords= {'a': self.across, 'd': self.down}
      self.needWords= []
      self.gotWords= []
      self.usedWords= []


  def pick_optimal_word(self,node, poss_words):
    min_word = None
    min_val = 9999999
    poss_words= [w for w in poss_words if w not in self.usedWords]
    for word in poss_words:
      index = 0
      char_list = list(word)
      value = 0; 
      for inter in node.intersections:
        if inter != None:
          value += scrabble_val[char_list[index]]; 
        index += 1
      if (value < min_val):
        min_word = word
    self.usedWords += [list(min_word)]
    return list(min_word)


  #direc: 'a'= across, 'd'=down
  def addNode(self, node, direc):
      if direc in ['a','d']:
      	self.allWords[direc][node.num]= node
      self.needWords += [(direc,node.num)]



  def nextWord(self):
    ratios= []
    for (direc, wordNum) in self.needWords: 
      node= self.allWords[direc][wordNum]
      ratios += [((float(node.ratio[0])/float(node.ratio[1])+node.len/4),direc,wordNum)]
    print ratios
    maxInds= [i for (i,val) in enumerate(ratios) if val[0]==max(ratios)[0]]
    if len(maxInds)>0:
      lengths= []
      for elem in maxInds:
        r,d,w= ratios[elem]
        node= self.allWords[d][w]
        lengths += [(node.len,d,w)]
      print "NEXT if", max(lengths)[1], max(lengths)[2]
      return max(lengths)[1], max(lengths)[2]
    else:
      m= maxInds[0]
      print "NEXT else", ratios[m][1], ratios[m][2]
      return ratios[m][1], ratios[m][2]



  def intersectionToChange(self,lst, opposite):
    lst= [(i,elem[0], elem[1]) for (i, elem) in enumerate(lst) if elem!=None]
    '''maxValNode= (0,None,None,None)
    for (i, num, ind) in lst:
      node= self.allWords[opposite][num]
      itsIntersections= [elem for elem in node.intersections if elem!=None]
      if len(itsIntersections)>maxValNode[0]:  
        maxValNode= (len(itsIntersections), i, num, ind)'''
    lengths= [(float(1)/float(self.allWords[opposite][num].len),j) for (j,(i,num,ind)) in enumerate(lst)]

    minLen,ind= min(lengths)
    return lst[ind]



  #just picks words randomly, no backtracking or anything
  #if a word gets filled up before being chosen, doesn't confirm whether it's actually a word (e.g. "AAG")

  #when picking intersection to change, pick the one with fewest intersections
  #when picking word to set, pick one with largest unfilled:filled ratio 
  def solveCSP(self):
    while(len(self.needWords)!=0):
      print "\n\n\nNeedWords\n", self.needWords
      direc,wordNum= self.nextWord() #!!!!!
      opposite= 'd' if direc=='a' else 'a'
      node= self.allWords[direc][wordNum]
      if node.word==["?" for _ in xrange(node.len)]:
        index= random.randint(0,node.len-1)
        node.addLetter(index,'a')
      query= ''.join(node.word)
      possibleWords= scrape.getPossibleWords(query)
      successful= True
      if possibleWords==[]: 
        print query,"oh noooo"
        k, num, intPoint= self.intersectionToChange(node.intersections, opposite)
        print opposite, num
        problemNode= self.allWords[opposite][num]
        allIntPoints= [i for (i,val) in enumerate(problemNode.intersections) if val!=None]
        if problemNode.word in self.usedWords: 
          self.usedWords.remove(problemNode.word)
        for j,letter in enumerate(problemNode.word):
          if j==intPoint: 
            problemNode.addLetter(j,random.choice(alphabet))
            node.addLetter(k,random.choice(alphabet))
          elif j in allIntPoints:
            pass
          else: 
            problemNode.addLetter(j,'?')
        problemNode.possibleWords= []
        if (opposite,num) in self.gotWords: 
          self.gotWords.remove((opposite,num))
        if (opposite,num) not in self.needWords: 
          self.needWords += [(opposite,num)]
        successful= False
      else: 
        print possibleWords
        node.possibleWords= possibleWords
        node.word= self.pick_optimal_word(node,node.possibleWords)  #!!!!!
        print "Chose word", ''.join(node.word), "for", direc, wordNum
        for ind,inter in enumerate(node.intersections):
          if inter!=None: 
            num,spot= inter
            interNode= self.allWords[opposite][num]
            interNode.addLetter(spot,node.word[ind])
      if successful:
        self.needWords.remove((direc,wordNum))
        self.gotWords += [(direc,wordNum)]
      time.sleep(1)


#Invariants: 
# 1) All w that have children, have been populated such that they satisfy their parents and grandparents 
# 2) If w is a problem node, first backtrack to its parents, then to its siblings


    
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
    cross= board.Board(11)
    csp_cross= CSP()
    #define board
    cross.board[0][3] = None
    cross.board[1][3] = None
    cross.board[2][3] = None
    cross.board[1][2] = None
    cross.board[0][7] = None
    cross.board[1][7] = None
    cross.board[2][7] = None
    cross.board[1][8] = None
    cross.board[4][0] = None
    cross.board[4][1] = None
    cross.board[4][6] = None
    cross.board[4][8] = None
    cross.board[4][9] = None
    cross.board[4][10] = None
    cross.board[5][4] = None
    cross.board[5][5] = None
    cross.board[5][6] = None
    cross.board[6][0] = None
    cross.board[6][1] = None
    cross.board[6][2] = None
    cross.board[6][4] = None
    cross.board[6][9] = None
    cross.board[6][10] = None
    cross.board[8][3] = None
    cross.board[9][2] = None
    cross.board[10][3] = None
    cross.board[8][7] = None
    cross.board[9][7] = None
    cross.board[9][8] = None
    cross.board[10][7] = None
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
    csp_cross.solveCSP()
    print "Across:" 
    for k,v in csp_cross.across.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", intersections=", v.intersections
    print "Down:"
    for k,v in csp_cross.down.iteritems():
      print k, ": len=", v.len, ", word=", v.word, ", intersections=", v.intersections
    print "\n\n"
    csp_cross.printWordsToGui(cross)


#GUI STUFF
    root = tk.Tk()
    root.resizable(False, False)
    leftFrame= tk.Frame(root)
    rightFrame= tk.Frame(root)
    gameboard = gui.GameBoard(leftFrame, cross, cross.solution, 11*80)
    clues= gui.Clues(rightFrame, cross.acrossClues, cross.downClues, 11*6)

    leftFrame.pack(side="left")
    rightFrame.pack(side="right")
    gameboard.canvas.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    clues.text.pack(side="right")
    root.mainloop()
    
if __name__=="__main__":
      main()