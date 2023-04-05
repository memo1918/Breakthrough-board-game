from pygame import Rect,draw

class Square():
    def __init__(self,x,y,width,height,location):
        """Square init."""
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.location = location #location(y,x)
        self.occupiedPiece = None
        self.isHighlight = False
        self.pieceRadius = int((self.width/2)-(0.1*self.width))

        self.rect = Rect(self.x,self.y,width,height)
        self.color = (209, 139, 71) if (location[0] + location[1]) % 2 == 0 else (255, 206, 158)				 

    def info(self) -> tuple:
        """Returns preselected information in a tuple."""
        return (self.location,self.occupiedPiece,self.isHighlight)
    
    def getCoordinates(self) -> tuple:
        """Returns coordinates(x,y) in a tuple."""
        return (self.x,self.y)

    def getCenter(self) -> tuple:
        """Returns center coordinates of the Square in a tuple."""
        return (self.x+self.width/2,self.y+self.height/2)

    def draw(self,screen):
        """Handels the drawing of the Squares and Pieces on the game window."""
        if self.isHighlight:
            draw.rect(screen,(159, 255, 158),self.rect)
        else:
            draw.rect(screen,self.color,self.rect)

        if self.occupiedPiece != None:

            if self.occupiedPiece.isBlack:
                draw.circle(screen,center = self.getCenter(),radius = self.pieceRadius, color= "black")
            else:
                draw.circle(screen,center = self.getCenter(),radius = self.pieceRadius, color= "white")
