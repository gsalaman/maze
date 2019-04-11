# Maze game
#
# Each room is defined as a list of 4 "next rooms"...north, south, east, west.
# 0 means no path that direction.
# non-zero is the room id of the room for that direction.

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw

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

########################################################
# some globals.  Where do we start, and where are we going?
#######################################################
current_room = 1
dest_room = 16

########################################################
# Display constants
########################################################
matrix_size = 64
room_size = 16
wall_color = (255,0,0)

########################################################
# Matrix configuration
########################################################
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64 
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

########################################################
# show_room
#
# Displays a given room in our matrix.  
########################################################
def show_room(room, corner_x, corner_y):
  
  # I'm going to start by defining an image that is the size of a room.
  # I'll then check the maze data to draw top, bottom, left, and right walls.
  # Then I'll render the image to the proper corner.

  temp_image = Image.new("RGB", (room_size, room_size))
  temp_draw = ImageDraw.Draw(temp_image)

  # draw the walls
  if maze[room][0] == 0:
    # north wall is on top
    temp_draw.line((0,0,room_size-1,0), fill=wall_color)
  if maze[room][1] == 0:
    # south wall is on bottom
    temp_draw.line((0,room_size-1, room_size-1, room_size-1), fill=wall_color) 
  if maze[room][2] == 0:
    #east wall is on right
    temp_draw.line((room_size-1,0, room_size-1, room_size-1), fill=wall_color) 
  if maze[room][3] == 0:
    # west wall is on left
    temp_draw.line((0,0,0,room_size-1), fill=wall_color) 

  # display our room at the right point.
  matrix.SetImage(temp_image, corner_x, corner_y)

########################################################
# getch()
#
#   Get single character
########################################################
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
  
#######################################################
# print_exits()
#
# Print out which ways you can go from the current room
#######################################################
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

########################################################
# get_next_room()
#
# takes a character as input.
# looks into the maze array to confirm you can go that way.
# if so, it'll set current room to the new room
# if not, current room stays the same, and you get an error message.
# also confirms input is a correct direction.
######################################################## 
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

###################################################
# show_maze()
#
# Displays the whole maze...only called once.
################################################### 
def show_maze():
  for room in maze.keys():
     x_corn = ((room - 1) % 4) * room_size
     y_corn = ((room - 1) / 4) * room_size
     show_room(room, x_corn, y_corn)
     print room, x_corn, y_corn
      
###################################################
# Our main loop.  
################################################## 
show_maze()
while current_room != dest_room:
  print_exits()
  current_room = get_next_room(current_room)
print "Yay!  You won!" 

