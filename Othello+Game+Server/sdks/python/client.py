#!/usr/bin/python

import sys
import json
import socket

BOARD_SIZE = 8


def num_outflanks(row, column, player, board):
  # check all adjacent paths
  directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
  flips = 0
  
  for dir in directions:
    r, c = row + dir[0], column + dir[1]

    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
      continue
    if board[r][c] == 0 or board[r][c] == player:
      continue

    # Keep moving in this direction until we find our player's piece or an empty spot
    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] != 0:
      if board[r][c] == player:
        return flips
      flips += 1
      r, c = r + dir[0], c + dir[1]
 
  return 0
    
def get_best_move(player, board):
  possible_moves = []
  flips = []
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      if board[i][j] == 0:
        if num_outflanks(i, j, player, board) != 0:
          possible_moves.append([i, j])
          flips.append(num_outflanks(i, j, player, board))       
  max_flips_move = possible_moves[max(range(len(flips)), key=flips.__getitem__)]
  return max_flips_move


def get_move(player, board):
  return get_best_move(player, board)
  
        
def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
