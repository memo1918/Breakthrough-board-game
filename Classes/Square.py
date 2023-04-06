from pygame import Rect,draw

class Square():
    """
    A class to represent Squares.

    ...

    Attributes
    ----------
    x : int
            x coordinate of left top corner of square 

    y : int
            y coordinate of left top corner of square 

    width : int
            width of the square

    height : int
            height of the square

    location : tuple
            contains row and column values

    occupiedPiece : Piece or None
            piece on the square or None

    isHighlight : bool
            true if square being Highlighted

    color : tuple
            has RGB values
    
    pieceRadius : int
            radius of the piece to draw

    rect : Rect
            pygame.Rect object contains information to draw square 
    """
    def __init__(self,x: int, y: int, width: int, height: int, location: tuple):
        """
        Constructs all the necessary attributes for the Square object.

        Parameters
        ----------
        x : int
            x coordinate of left top corner of square 
        y : int
            y coordinate of left top corner of square 
        width : int
            width of the square
        height : int
            height of the square
        location : tuple
            contains row and column values
        """
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.location = location #location(row,column)
        self.occupiedPiece = None
        self.isHighlight = False
        
        self.color = (209, 139, 71) if (location[0] + location[1]) % 2 == 0 else (255, 206, 158)				 
        self.pieceRadius = int((self.width/2)-(0.1*self.width))
        self.rect = Rect(self.x,self.y,width,height)
    
    def getCoordinates(self) -> tuple:
        """
        Returns:
            coordinates (tuple) : coordinates(x,y)
        """
        return (self.x,self.y)

    def getCenter(self) -> tuple:
        """
        Returns: 
            center coordinates (tuple): center of the Square (x,y).
        """
        return (self.x+self.width/2,self.y+self.height/2)

    def draw(self,screen) -> None:
        """
        Handels the drawing of the Squares and Pieces on the game window.
        
        Parameters:
                screen (pygame.surface): window to draw
        """

        if self.isHighlight:
            draw.rect(screen,(159, 255, 158),self.rect)
        else:
            draw.rect(screen,self.color,self.rect)

        if self.occupiedPiece != None:

            if self.occupiedPiece.isBlack:
                draw.circle(screen,center = self.getCenter(),radius = self.pieceRadius, color= "black")
            else:
                draw.circle(screen,center = self.getCenter(),radius = self.pieceRadius, color= "white")
