from terrain import Tile
from planet import Planet
from loader import load_level
from rover import Rover

def quit_game():
	quit()

def menu_help():
	print("\nSTART <level file> - Starts the game with a provided file.\nQUIT - Quits the game\nHELP - Shows this message\n")

def menu_start_game(filepath):
	# start the game with the given file path
	file_info = (load_level(filepath))
	if file_info == False:
		return False
	else:
		planet, rover = file_info[0],file_info[1]
		return (planet,rover)
	
def finish():
	explored = int((rover.get_num_explored()/planet.get_num_tiles())*100)
	print("You explored {}% of {}\n".format(explored,planet.get_name()))

def scan_shade(rover,planet):
	#center the matrix
	x_cor,y_cor = rover.x, rover.y
	#print the closest 4 rows/columns around the rover 
	range_rows = list(map(lambda p: p%planet.width,[(x_cor-2),(x_cor-1),(x_cor),(x_cor+1),(x_cor+2)]))
	range_columns = list(map(lambda p:p%planet.height,[(y_cor-2),(y_cor-1),(y_cor),(y_cor+1),(y_cor+2)]))
	new_matrix = [[" " for _ in range(5)]for _ in range(5)]
	xx,yy = 0,0
	#make a new matrix to print
	for y in range_columns:
		for x in range_rows:
			new_matrix[yy][xx] = planet.tiles[y][x]
			rover.set_tiles_explored((x,y))
			xx +=1
		xx = 0
		yy+=1
	#these are used to check when to print the rover
	for y in range(len(new_matrix)):
		for x in range(len(new_matrix[y])):
			if y == 2 and x == 2:
				print("|H",end="")
			elif new_matrix[y][x].is_shaded():
				print("|#",end="")
			else:
				print("| ",end="")
		print("|\n",end="")
	
def scan_elevation(rover,planet):
	#center the matrix
	x_cor,y_cor = rover.get_rover_cor()[0],rover.get_rover_cor()[1]
	rov_elevation = (planet.tiles[y_cor][x_cor]).get_elevation()
	#print the closest 4 rows/columns around the rover 
	#mod by the width or height to account for "overflow"
	range_rows = list(map(lambda p: p%planet.width,[(x_cor-2),(x_cor-1),(x_cor),(x_cor+1),(x_cor+2)]))
	range_columns = list(map(lambda p:p%planet.height,[(y_cor-2),(y_cor-1),(y_cor),(y_cor+1),(y_cor+2)]))
	new_matrix = [[" " for _ in range(5)]for _ in range(5)]
	#xx, yy the new coordinates for the matrix to print 
	xx,yy = 0,0
	#make the new matrix
	#iterate through the column and row list created above
	for y in range_columns:
		for x in range_rows:
			new_matrix[yy][xx] = planet.tiles[y][x]
			rover.set_tiles_explored((x,y))
			xx +=1
		xx = 0
		yy+=1
	#since everything is relative to the rover, must retrive the rov_elevation
	if len(rov_elevation) == 1:
		rov_elevation = rov_elevation[0]
		for y in range(len(new_matrix)):
			for x in range(len(new_matrix[y])):
				the_tile_elevation = new_matrix[y][x].get_elevation()
				# since the rover has been centered 
				# if check_y and check_x are equal to 2
				# then these are the coordinates of the rover 
				if y == 2 and x == 2:
					print("|H",end="")	
				elif len(the_tile_elevation) == 2:
					#if the highest tile elevation is equal to the rovers elevation
					#it will be a downslope
					if int(the_tile_elevation[0]) == int(rov_elevation):
						print("|\\",end="")
					#if the lowest elevation would is equal to the rover then it is an upslope
					elif int(the_tile_elevation[1]) == int(rov_elevation):
							print("|/",end="")
					#if highest elevation lower than rov elevation, then can't move on  
					elif int(the_tile_elevation[0]) < int(rov_elevation):
						print("|-",end="")
					elif int(the_tile_elevation[1]) > int(rov_elevation):
						print("|+",end="")
				elif len(the_tile_elevation) == 1:
					if the_tile_elevation[0] == rov_elevation:
						print("| ",end="")
					elif the_tile_elevation[0] > rov_elevation:
						print("|+",end="")
					else:
						print("|-",end="")
			print("|\n",end="")
	# if the rover is on a slope
	else:
		high,low = rov_elevation[0], rov_elevation[1]
		for y in range(len(new_matrix)):
			for x in range(len(new_matrix[y])):
				the_tile_elevation = new_matrix[y][x].get_elevation()
				if y == 2 and x == 2:
					print("|H",end="")	
				elif len(the_tile_elevation) == 2:
					if int(the_tile_elevation[0]) == int(low):
						print("|\\",end="")
					elif int(the_tile_elevation[1]) == int(high):
						print("|/",end="")
					elif int(the_tile_elevation[1]) > int(high):
						print("|+",end="")
					elif int(the_tile_elevation[0]) < int(low):
						print("|-",end="")	
					else:
						print("| ",end="")
				elif len(the_tile_elevation) == 1:
					if high == the_tile_elevation[0] or low == the_tile_elevation[0]:
						print("| ",end="")
					elif the_tile_elevation[0] > high:
						print("|+",end="")
					else:
						print("|-",end="")
			print("|\n",end="")
	
def wait(cycles):
	if not planet.tiles[rover.y][rover.x].is_shaded():
		rover.wait(cycles)
		
def stats():
	explored = int((rover.get_num_explored()/planet.get_num_tiles())*100)
	print("\nExplored: {}%".format(explored))
	print("Battery: {}/100\n".format(rover.get_battery()))
	
while True:
	command = input()
	list_command = command.split()
	if "QUIT" in command:
		quit_game()
	elif "START" in command:
		if len(list_command) == 2:
			# if the file is not correct/doesn't exist the planet,rover is not returned
			if menu_start_game(list_command[1]):
				planet,rover = menu_start_game(list_command[1])
				break
		else:
			print("\nNo menu item\n")
	elif "HELP" in command:
		menu_help()
	else:
		print('\nNo menu item\n')
	
def rover_in_shade():
	tile = planet.get_tiles()[rover.rover_y()][rover.rover_x()].is_shaded()
	return tile

#actually starting the game, using the functions defined above
while True:
	command = input()
	list_command = command.split()
	#the rover has no battery and in the shade the rover can't continue
	#scan command 
	if "SCAN" in command:
		print("\n",end="")
		if len(list_command) == 1:
			print("No menu item")
		elif list_command[1] == "shade":
			scan_shade(rover,planet)
		elif list_command[1] == "elevation":
			scan_elevation(rover,planet)
		else:
			print("No menu item")
		print("\n",end="")
	elif "MOVE" in command:
		if len(list_command) == 3:
			rover.move(list_command[1],list_command[2],planet)
		else:
			print("\nNo menu item\n")
	elif "WAIT" in command:
		if len(list_command) ==2:
			wait(list_command[1])
	elif "STATS" == command:
		stats()
	elif "FINISH" == command:
		print("\n",end="")
		finish()
	elif "QUIT" == command:
		quit()
	else:
		print("\nNo menu item\n")
