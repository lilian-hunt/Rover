from planet import Planet
from rover import Rover
from terrain import Tile
import os 

def load_level(filename):
	#check whether the score file can be found
	scorepath = os.path.abspath(str(filename))
	#checking if the file exists
	if os.path.exists(scorepath) == False:
		print("\nLevel file could not be found\n")
		return False
	with open(filename,"r") as the_file:
		data = the_file.readlines()
	#use the checker to make sure all the specifications are met
	#if something is wrong it will be changed to False
	counter =0 
	checker = True
	#extract the data from the file
	#check if data is structured properly
	if data[-1] == "\n":
		data = data[0:-1]
		#print(data)
	if data[6] != "[tiles]\n" or data[0] != "[planet]\n":
		print("\nUnable to load level file\n")
		return False
	if data[1].startswith("name,"):
		name = data[1][5:].rstrip()
	if data[2].startswith("width,"):
		width = int(data[2].strip("width,").strip("\n"))
		#width and height must be 5 or greater
		if width <5:
			print("\nUnable to load level file\n")
			return False
	if data[3].startswith("height,"):
		height = int(data[3].strip("height,").strip("\n"))
		if height < 5:
			print("\nUnable to load level file\n")
			return False
	if data[4].startswith("rover,"):
		rover = data[4].strip("rover,").strip("\n")
		rover = rover.split(",")
	if int(rover[0]) <0 or int(rover[1])<0 or int(rover[0])>=(width) or int(rover[1]) >=(height):
		print("\nUnable to load level file\n")
		return False
	num_tiles = int(width)*int(height)
	#check if data for all the tiles has been given
	if len(data) != 7+num_tiles:
		print("\nUnable to load level file\n")
		return False
	tiles = [[" " for _ in range(width)]for _ in range(height)]
	y_cor = 0
	x_cor =0 
	#initialise the tiles, with the [<type>,<highest elevation>,(<lowest elevation>)]
	for x in range(7,7+num_tiles):
		tiles[y_cor][x_cor] = Tile(data[x].strip().split(","))
		tile_data = (data[x].strip().split(","))
		#print(tiles[y_cor][x_cor].is_shaded())
		#check to see if the tile is sloped
		if len(tile_data) == 3:
			#check to make sure that the highest elevation is strictly greater than lowest elevation
			if (int(tile_data[1]) - int(tile_data[2])) != 1:
				print("\nUnable to load level file\n")
				return False
		if x_cor == width-1:
			x_cor = -1
			y_cor += 1
		x_cor += 1
	#only if the file is structured correctly return the variables
	#make the objects in this file to return
	the_planet = Planet(name,width,height,tiles)
	the_rover = Rover(rover)
	#returns the objects as a tuple
	return (the_planet, the_rover)
