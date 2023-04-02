class Computer():
    def __init__(self,board):
        """Computer init."""
        self.board = board
        self.squares = self.board.squares
        
    def score(self,move)->int:
        """Calculates the score of possible move and returns as intiger."""
        score = 0
        loc = move.location #move is a square object
        
        if loc[0] == 4:
            score+=10
        elif loc[0] == 5:
            score+=1000

        if loc[0] != 5:
            for i in [1,-1]:
                if loc[1]+i < 0 or loc[1]+i > self.board.size-1: 
                    continue

                diagPiece = self.squares[loc[0]+1][loc[1]+i].occupiedPiece
                if diagPiece !=None:
                    if not diagPiece.isBlack:
                        score -= 10
                        break 
        
        for square in self.squares[1]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == False and loc != square.location:
                    score -= 900
        
        return score

    def move(self,moveTuple):
        piece = moveTuple[0]
        targetSquare = moveTuple[1]

        piece.move(self.board,targetSquare)



    
