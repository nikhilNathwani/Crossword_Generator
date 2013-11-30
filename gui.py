import Tkinter as tk
from board import Board
from csp import CSP

class GameBoard():
    def __init__(self, parent, cross, length, color1="white", color2="black"):
        '''size is the size of a square, in pixels'''

        self.board= cross.board
        self.rows = len(cross.board)
        self.columns = len(cross.board[0]) if len(cross.board)>0 else 0
        self.size = length/len(cross.board)
        self.color1 = color1
        self.color2 = color2
        self.canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0,
                                width=length, height=length, background="white")

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)


    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        self.canvas.delete("nums")
        for row in range(self.rows):
            for col in range(self.columns):
                color = self.color1 if self.board[row][col]!=None else self.color2
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                if self.board[row][col]!=None and self.board[row][col]!=0:
                    self.canvas.create_text(x1+self.size/32+21/2,y1+self.size/16+21/2,text=str(self.board[row][col]), font="Times 21", tags="nums")
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


class Clues():
    def __init__(self, parent, across, down, cross_len):
        self.across= across
        self.down= down
        self.text= tk.Text(parent, width=40, height=cross_len, background="#BFE8D4")
        self.text.tag_config("a", justify="left")
        self.text.insert(1.0, "ACROSS\n\n")
        for i,ac in enumerate(across):
            self.text.insert(float(i+3), "%d. %s\n" % (ac, across[ac]))
        self.text.insert(float(5+len(across)), "\n\n\nDOWN\n\n")
        for j,do in enumerate(down):
            self.text.insert(float(i+7+len(across)), "%d. %s\n" % (do, down[do]))

if __name__ == "__main__":
    cross_size= 4
    cross= Board(cross_size)
    csp_cross= CSP()
    #define board
    cross.board[0][0]= None
    cross.board[0][1]= None
    cross.board[1][3]= None
    #cross.board[1][4]= None
    cross.board[2][2]= None
    cross.board[2][3]= None
    cross.board[3][2]= None
    cross.board[3][3]= None
    #cross.board[4][1]= None
    #cross.board[4][2]= None
    #cross.board[5][4]= None
    #cross.board[5][5]= None
    cross.acrossClues= {1:"one", 2:"twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo", 3: "Three"}
    cross.downClues= {4:"one", 5:"twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo", 6: "Three"}
    #print cross.board
    cross.genWordsFromBoard(csp_cross)
    cross.setWordNumbers(csp_cross)
    cross.calcIntersections(csp_cross)
    
    root = tk.Tk()
    root.resizable(False, False)
    leftFrame= tk.Frame(root)
    rightFrame= tk.Frame(root)
    board = GameBoard(leftFrame, cross, cross_size*80)
    clues= Clues(rightFrame, cross.acrossClues, cross.downClues, cross_size*6)

    leftFrame.pack(side="left")
    rightFrame.pack(side="right")
    board.canvas.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    clues.text.pack(side="right")
    root.mainloop()
