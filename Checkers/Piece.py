import pygame

class Piece:
  def __init__(self,row,col,color):
    self.row = row
    self.col = col
    self.color = color
    self.isKing = False
    self.x = 100*col + 50
    self.y = 100*row + 50

  def makeKing(self):
    self.isKing = True


  def move(self,row,col):
    self.row = row
    self.col = col
    self.x = 100*col + 50
    self.y = 100*row + 50
    

    
  def drawPiece(self,window):
    pygame.draw.circle(window,self.color,(self.x,self.y), 40)
    if self.isKing == True:
      pygame.draw.circle(window,(225,225,0),(self.x,self.y), 15)

