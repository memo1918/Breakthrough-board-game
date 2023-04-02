from Square import Square
from Piece import Piece

class Board():
    def __init__(self,width,height,size = 6,gap = 0):
        """Board init."""
        self.width = width
        self.height = height
        self.gap = gap
        self.size = size
        self.squares = self.genSquares()
        self.selectedPiece = None
        self.turn = False #true means black's turn

    def boardCalc(self) -> list:
        """Calculates the square coordinates and sizes. Returns list containing coordinates, respect to width and height, and location."""
        coordinate = []
        
        self.increment_h = int(self.height/self.size)
        self.increment_w = int(self.width/self.size)
    
        y = self.gap
        for i in range(self.size):
            x = self.gap
            for j in range(self.size):
                coordinate.append([x,y,[i,j]])#location(y,x)
                x+=self.increment_w
            y+=self.increment_h
        return coordinate

    def genSquares(self) -> list:
        """Generates squares based on boardCalc() return. Returns lists within list containing Square objects."""
        squares = []
        coordinates = self.boardCalc()
        
        for j,coordinate in enumerate(coordinates):
            if j%self.size==0:
                squares.append([])

            squares[-1].append(Square(coordinate[0],coordinate[1],self.increment_w-2*self.gap,self.increment_h-2*self.gap,coordinate[2]))

        return squares
    
    def getSquare(self,mx,my) -> Square:
        """Returns Square object based on mouse coordinates."""
        y = my//self.increment_h
        x = mx//self.increment_w
        return self.squares[y][x]

    def draw(self,screen):
        """Initiates draw sequence within Square objects."""
        if self.selectedPiece != None:
            for square in self.selectedPiece.posMoves(self):
                square.isHighlight = True

        for row in self.squares:
            for square in row:
                square.draw(screen)
        

    def startPos(self):
        """Configures the Board to its start state with Piece objects."""
        for j in [0,1,-1,-2]:
            for square in self.squares[j]:
                if j>=0:
                    square.occupiedPiece = Piece(True,square.location)
                else:
                    square.occupiedPiece = Piece(False,square.location)

    def click(self,mx,my):
        """Handels mouse click on the game window."""
        clickedSquare = self.getSquare(mx,my)

        if clickedSquare.occupiedPiece != None and clickedSquare.occupiedPiece.isBlack == self.turn :
            for row in self.squares:
                for square in row:
                    square.isHighlight = False

            if clickedSquare.occupiedPiece.isBlack ==  self.turn:
                self.selectedPiece = clickedSquare.occupiedPiece

        elif clickedSquare.isHighlight:
            if clickedSquare.occupiedPiece != None:
                self.selectedPiece.move(self,clickedSquare)
            else:
                self.selectedPiece.move(self,clickedSquare)
        else:
            self.selectedPiece = None
       
    def isWin(self) -> str or bool:
        """Checks for wining states. Returns False or Winners color as string"""
        for square in self.squares[0]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == False:
                    return "White"

        for square in self.squares[-1]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == True:
                    return "Black"     
        return False
            
            