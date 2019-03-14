	#a map function to look at the whole map, to check if move function works
	elif "MAP" in command:
		tiles = planet.get_tiles()
		for y in range(len(tiles)):
			for x in range(len(tiles[y])):
				the_tile_elevation = tiles[y][x].get_elevation()
				if rover.x == x and rover.y == y:
					print("|H",end="")	
				elif tiles[y][x].is_shaded():
					print("| ",end="")
				else:
					print("|#",end="")
			print("|\n",end="")
