import random
import pygame
from .Board import Board

class Game: 
  def __init__(self,window):
    self.selected = None
    self.board = Board()
    self.turn = (225,0,0)
    self.validMoves = {}
    self.window = window
    self.policy = [1.0,0.2,0.5]
    self.prevPolicy = [1.0,0.2,0.5]

  def update(self):
    self.board.draw(self.window)
    self.drawValidMoves(self.validMoves)
    pygame.display.update()

  def reset(self):
    self.selected = None
    self.board = Board(self.policy)
    self.turn = (225,0,0)
    self.validMoves = {}
  def winner(self):
    return self.board.winner()

  def select(self, row, col):
    if self.selected:
      result = self.move(row,col)
      if not result:
        self.selected = None
        self.select(row,col)
    
    piece = self.board.getpiece(row,col)
    if piece != 0 and piece.color == self.turn:
      self.selected = piece
      self.validMoves = self.board.getValidMoves(piece)
      return True
        
    return False
    
  def move(self, row, col):
    piece = self.board.getpiece(row,col)
    if self.selected and piece == 0 and (row,col) in self.validMoves:
      self.board.move(self.selected, row, col)
      skipped = self.validMoves[(row,col)]
      if skipped: 
        self.board.remove(skipped)
      self.nextTurn()
    else: 
      return False
    return True 

  def drawValidMoves(self,moves):
    for move in moves:
      row,col = move
      pygame.draw.circle(self.window, (0,225,0), (col*100+50,row*100+50),20)


  
  def nextTurn(self):
    self.validMoves = {}
    if self.turn == (225, 0, 0):
      
      self.turn = (0,0,225)
      
    else:
      self.turn = (225,0,0)

  def getBoard(self):
    return self.board

  def aiMove(self, newBoard):
    self.board = newBoard
    self.nextTurn()