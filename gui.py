import Tkinter as tk
#from board import Board
#from csp import CSP

class GameBoard():
    def __init__(self, parent, cross, solution, length, numFontSize, letterFontSize, color1="white", color2="black"):
        '''size is the size of a square, in pixels'''

        self.board= cross.board
        self.numFontSize= str(numFontSize)
        self.letterFontSize= str(letterFontSize)
        self.rows = len(cross.board)
        self.solution= solution
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
                    self.canvas.create_text(x1+self.size/32+21/2,y1+self.size/16+21/2,text=str(self.board[row][col]), font="Times "+self.numFontSize, tags="nums")
                self.canvas.create_text(x1+self.size/2,y1+self.size/2+4,text=str(self.solution[row][col]), font="Times "+self.letterFontSize, tags="nums")
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
        acrossList= sorted(enumerate(across),key=lambda x: x[1])
        #print acrossList
        for ind,(i,ac) in enumerate(acrossList):
            self.text.insert(float(ind+3), "%d. %s\n" % (ac, across[ac].strip()))
        self.text.insert(float(5+len(across)), "\n\n\nDOWN\n\n")
        downList= sorted(enumerate(down),key=lambda x: x[1])
        #print downList
        for ind,(j,do) in enumerate(downList):
            #print (do, down[do])
            self.text.insert(float(ind+7+len(across)), "%d. %s\n" % (do, down[do].strip()))

if __name__ == "__main__":
    cross_size= 15
    cross= Board(cross_size)
    csp_cross= CSP()
    #define board
    cross.board[0][5] = None
    cross.board[14][5] = None
    cross.board[0][9] = None
    cross.board[14][9] = None

    cross.board[6][6] = None
    cross.board[8][6] = None
    cross.board[6][8] = None
    cross.board[8][8] = None

    cross.board[6][0] = None
    cross.board[6][14] = None
    cross.board[10][0] = None
    cross.board[10][14] = None

    cross.board[1][1] = None
    cross.board[1][2] = None
    cross.board[1][3] = None
    cross.board[1][4] = None
    cross.board[1][5] = None
    cross.board[2][1] = None
    cross.board[3][1] = None
    cross.board[4][1] = None
    cross.board[5][1] = None

    cross.board[1][9] = None
    cross.board[1][10] = None   
    cross.board[1][11] = None
    cross.board[1][12] = None
    cross.board[1][13] = None
    cross.board[2][13] = None
    cross.board[3][13] = None
    cross.board[4][13] = None
    cross.board[5][13] = None


    cross.board[9][1] = None
    cross.board[10][1] = None
    cross.board[11][1] = None
    cross.board[12][1] = None
    cross.board[13][1] = None
    cross.board[13][2] = None
    cross.board[13][3] = None
    cross.board[13][4] = None
    cross.board[13][5] = None

    cross.board[1][9] = None
    cross.board[1][10] = None
    cross.board[1][11] = None
    cross.board[1][12] = None
    cross.board[1][13] = None
    cross.board[2][13] = None
    cross.board[3][13] = None
    cross.board[4][13] = None
    cross.board[5][13] = None

    cross.board[3][3] = None
    cross.board[3][4] = None
    cross.board[3][5] = None
    cross.board[4][3] = None

    cross.board[3][9] = None
    cross.board[3][10] = None
    cross.board[3][11] = None
    cross.board[4][11] = None

    cross.board[11][3] = None
    cross.board[11][4] = None
    cross.board[11][5] = None
    cross.board[10][3] = None

    cross.board[11][9] = None
    cross.board[11][10] = None
    cross.board[11][11] = None
    cross.board[10][11] = None

    cross.board[7][1] = None
    cross.board[7][2] = None
    cross.board[7][3] = None
    cross.board[7][4] = None
    cross.board[7][5] = None
    cross.board[6][3] = None
    cross.board[7][3] = None
    cross.board[8][3] = None

    cross.board[7][9] = None
    cross.board[7][10] = None
    cross.board[7][11] = None
    cross.board[7][12] = None
    cross.board[7][13] = None
    cross.board[6][11] = None
    cross.board[7][11] = None
    cross.board[8][11] = None

    cross.board[1][7] = None
    cross.board[2][7] = None
    cross.board[3][7] = None
    cross.board[4][7] = None
    cross.board[5][7] = None

    cross.board[9][7] = None
    cross.board[10][7] = None
    cross.board[11][7] = None
    cross.board[12][7] = None
    cross.board[13][7] = None

    cross.board[5][5] = None
    cross.board[5][9] = None
    cross.board[9][5] = None
    cross.board[9][9] = None

    cross.board[9][13] = None
    cross.board[10][13] = None
    cross.board[11][13] = None
    cross.board[12][13] = None
    cross.board[13][13] = None

    cross.board[13][9] = None
    cross.board[13][10] = None
    cross.board[13][11] = None
    cross.board[13][12] = None

    cross.acrossClues= {} #{1:"one", 2:"twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo", 3: "Three"}
    cross.downClues= {} #{4:"one", 5:"twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo twotwotwotwo", 6: "Three"}
    #print cross.board
    cross.genWordsFromBoard(csp_cross)
    cross.setWordNumbers(csp_cross)
    cross.calcIntersections(csp_cross)
    
    root = tk.Tk()
    root.resizable(False, False)
    leftFrame= tk.Frame(root)
    rightFrame= tk.Frame(root)
    board = GameBoard(leftFrame, cross, [], cross_size*50)
    clues= Clues(rightFrame, cross.acrossClues, cross.downClues, cross_size*4)

    leftFrame.pack(side="left")
    rightFrame.pack(side="right")
    board.canvas.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    clues.text.pack(side="right")
    root.mainloop()
