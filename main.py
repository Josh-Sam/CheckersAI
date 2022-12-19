import pygame
from Checkers.game import Game
import random
import pickle
from copy import deepcopy
from Roman.Algorithm import miniMax, transTable

Window = pygame.display.set_mode((800,800))

def clickToPos(click):
  x,y = click
  row = y//100
  col = x//100
  return row,col


def main():
  run = True
  clock = pygame.time.Clock()
  game = Game(Window)
  game.update()
  
  while run:
    clock.tick(60)
    # Uncomment to allow a random player to play
    
    # if game.turn == (225,0,0) and gamesplayed<100:
    #   None
    #   game.aiMove(random.choice(game.board.getAllMoves((225,0,0))))
    if game.turn == (0,0,225):
      value, newBoard = miniMax(game.board,3,True,float('-inf'),float('inf'))
      game.aiMove(newBoard)
      
    if game.winner() != None:
      print(len(transTable))
      with open('Data.pickle', 'wb') as handle:
        pickle.dump(transTable, handle, protocol=pickle.HIGHEST_PROTOCOL)
      game.reset()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        row,col = clickToPos(pygame.mouse.get_pos())
        game.select(row,col)
        

    
    game.update()

main()