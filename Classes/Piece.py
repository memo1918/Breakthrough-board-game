class Piece():
    def __init__(self,isBlack,location):
        """Piece init."""
        self.isBlack = isBlack
        self.location = location#location(y,x)

    def posMoves(self,board) -> list:
        """Finds the possible moves for the Piece object. Returns list containing Square objects."""
        output = []
        front_ax = self.location[0]+1 if self.isBlack else self.location[0]-1
        self.moves = [[front_ax,self.location[1]+1],[front_ax,self.location[1]],[front_ax,self.location[1]-1]]
        
        for move in self.moves:
            try:
                if move[1]<0:continue

                square = board.squares[move[0]][move[1]]

                if square.occupiedPiece != None:
                    if self.moves[1] != move:
                        if square.occupiedPiece.isBlack != self.isBlack:
                            output.append(square)
                else:
                    output.append(square)
            except:
                continue

        return output

    def move(self,board,targetSquare):
        """Handels the move of the Piece."""
        currentSquare = board.squares[self.location[0]][self.location[1]]
        
        targetSquare.occupiedPiece = self
        self.location = targetSquare.location
        
        currentSquare.occupiedPiece = None
        board.selectedPiece = None
        
        for row in board.squares:
            for square in row:
                square.isHighlight = False

        board.turn = not board.turn
