from .Square import Square
from .Piece import Piece

class Board():
    """
    A class to represent game board.

    ...

    Attributes
    ----------
    width : int
            width of the board

    height : int
            height of the board

    size : int
            size of the board

    genSquares : bool
            if true, starts generating squares

    selectedPiece : Piece
            Current selected piece

    turn : bool
            True if black's turn, False if white's turn

    depth : int
            depth of N-step look ahead algorithm

    squares : list
            contains all square objects. squares[row][column]

    blackPieces : list
            all black pieces on the board

    whitePieces : list 
            all white pieces on the board

    """
    def __init__(self, width: int, height: int, size: int, genSquares: bool = True):
        """
        Constructs all the necessary attributes for the Board object.

        Parameters
        ----------
        width : int
            width of the board
        height : int
            height of the board
        size : int
            size of the board
        genSquares: bool
            if true, starts generating squares

        """
        self.width = width
        self.height = height
        self.size = size
        self.selectedPiece = None
        self.turn = False #true means black's turn
        self.depth = 3

        if genSquares:self.squares = self.genSquares()
        else: self.squares = None

    def boardCalc(self) -> list:
        '''
        Calculates the square coordinates and sizes. Returns list containing coordinates, respect to width and height, and location.

        Returns:
                coordinate (list): Contains x,y coordinate and location for each square (x,y(row,column))
        '''
        
        coordinate = []
        
        self.increment_h = int(self.height/self.size)
        self.increment_w = int(self.width/self.size)
    
        y = 0
        for i in range(self.size):
            x = 0
            for j in range(self.size):
                coordinate.append((x,y,(i,j)))#location(row,column)
                x+=self.increment_w
            y+=self.increment_h
        return coordinate

    def genSquares(self) -> list:
        '''
        Generates squares based on boardCalc() return. Returns lists within list containing Square objects.

        Returns:
                squares (list): Contains Square objects.
        '''
        squares = []
        coordinates = self.boardCalc()
        
        for j,coordinate in enumerate(coordinates):
            if j%self.size==0:
                squares.append([])

            squares[-1].append(Square(coordinate[0],coordinate[1],self.increment_w,self.increment_h,coordinate[2]))

        return squares
    
    def getSquare(self,mx: int, my: int) -> Square:
        '''
            Returns Square object based on mouse coordinates.

            Parameters:
                    mx (int): x coordinate
                    my (int): y coordinate

            Returns:
                    square (Square): square object.
         '''
        y = my//self.increment_h
        x = mx//self.increment_w
        return self.squares[y][x]

    def startPos(self) -> None:
        '''
            Configures the Board to its start state with Piece objects.
        '''
        for j in [0,1,-1,-2]:
            for square in self.squares[j]:
                if j>=0:
                    square.occupiedPiece = Piece(True,square.location)
                else:
                    square.occupiedPiece = Piece(False,square.location)

    def draw(self,screen) -> None:
        """
        Initiates draw sequence within Square objects.
        
        Parameters:
                screen (pygame.surface): window to draw
        """
        if self.selectedPiece != None:
            for square in self.selectedPiece.posMoves(self):
                square.isHighlight = True

        for row in self.squares:
            for square in row:
                square.draw(screen)

    def pieceUpdate(self) -> None:
        '''
            Updates the list blackPieces and whitePieces.
        '''
        self.blackPieces = []
        self.whitePieces = []

        for row in self.squares:
            for square in row:
                if square.occupiedPiece != None:
                    piece = square.occupiedPiece
                    if piece.isBlack == True:
                        self.blackPieces.append(piece)
                    else:
                        self.whitePieces.append(piece)

    def click(self,mx,my) -> None:
        '''
            Handels mouse click on the game window.

            Parameters:
                    mx (int): x coordinate
                    my (int): y coordinate
         '''
        
        if not self.turn:
            clickedSquare = self.getSquare(mx,my)

            if clickedSquare != None:
                if clickedSquare.occupiedPiece != None and clickedSquare.occupiedPiece.isBlack == self.turn :
                    for row in self.squares:
                        for square in row:
                            square.isHighlight = False

                    if clickedSquare.occupiedPiece.isBlack ==  self.turn:
                        self.selectedPiece = clickedSquare.occupiedPiece

                elif clickedSquare.isHighlight and self.selectedPiece != None:
                    self.selectedPiece.move(self,clickedSquare)
                else:
                    for row in self.squares:
                        for square in row:
                            square.isHighlight = False
                    self.selectedPiece = None
        
    def isWin(self) -> str or bool:
        """
        Checks for wining states. Returns False or Winners color as string.
        
        Returns:
                'White' (str): if white is winning
                'Black' (str): if black is winning
                 False   (bool): no winning condition
        
        """
        for square in self.squares[0]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == False:
                    return "White"

        for square in self.squares[-1]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == True:
                    return "Black"     
                
        self.pieceUpdate()
        if not self.blackPieces:return "White"
        if not self.whitePieces:return "Black"

        return False
    
    def computerMove(self,computer) -> None:
        '''
            Starts the computer's turn.

            Parameters:
                computer (Computer): Computer object
         '''
        self.pieceUpdate()
        computer.move(self.depth)
