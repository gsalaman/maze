# Maze game
#
# Each room is defined as a list of 4 "next rooms"...north, south, east, west.
# 0 means no path that direction.
# non-zero is the room id of the room for that direction.

maze = \
{ \
  1:[0,0,2,0], \
  2:[0,6,0,1], \
  3:[0,7,4,0], \
  4:[0,8,0,3], \
  5:[0,9,0,0], \
  6:[2,10,0,0], \
  7:[3,11,0,0], \
  8:[4,12,0,0], \
  9:[5,0,10,0], \
  10:[6,14,0,9], \
  11:[7,15,0,0], \
  12:[8,16,0,0], \
  13:[0,0,14,0], \
  14:[10,0,15,13], \
  15:[11,0,0,14], \
  16:[12,0,0,0] \
}

current_room = 1
dest_room = 16

def getch():
  import sys, tty, termios
  old_settings = termios.tcgetattr(0)
  new_settings = old_settings[:]
  new_settings[3] &= ~termios.ICANON # & ~termios.ECHO
  try:
    termios.tcsetattr(0, termios.TCSANOW, new_settings)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(0, termios.TCSANOW, old_settings)
  return ch 
  
def print_exits():
  print "current room: ", current_room
  print "exits:",
  if maze[current_room][0]:
    print "north",
  if maze[current_room][1]:
    print "south",
  if maze[current_room][2]:
    print "east",
  if maze[current_room][3]:
    print "west",
  print
  print "n, s, e, or w"

def get_next_room(cur_room):
  dir_char = getch()
  if dir_char == 'n':
    next_room_index = 0
  elif dir_char == 's':
    next_room_index = 1
  elif dir_char == 'e':
    next_room_index = 2
  elif dir_char == 'w':
    next_room_index = 3
  else:
    print "I don't understand ", dir_char
    return cur_room

  next_room = maze[cur_room][next_room_index]
  if (next_room != 0):
    print "entering room ", next_room
    return next_room
  else:
    print "You can't go that way"
    return cur_room
  
while current_room != dest_room:
  print_exits()
  current_room = get_next_room(current_room)
print "Yay!  You won!" 

