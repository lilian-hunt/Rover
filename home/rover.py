class Rover:	
	def __init__(self, List): #get them from different file\):
		self.x = int(List[0])
		self.y = int(List[1])
		self.battery = 100	
		self.tiles_explored_set = set()
		#the rover has explored the first time it is on
		self.tiles_explored_set.add((self.x,self.y))	
	
	def update_next_tile(self,direction,height,width):
		if direction == "S":
			next_y = (self.y+1)%height
			next_x = self.x
		elif direction == "N":
			next_y = (self.y-1)%height
			next_x = self.x
		elif direction == "E":
			next_y = self.y
			next_x = (self.x +1)%width
		elif direction == "W":
			next_y = self.y
			next_x = (self.x-1)%width
		return next_y,next_x
	def move(self, direction, cycles,planet):
		planet_tiles = planet.get_tiles()
		#find the terrain that the rover is on
		rov_terrain = planet_tiles[self.y][self.x].get_elevation()
		height,width = planet.get_height(), planet.get_width()
		next_y,next_x = self.update_next_tile(direction,height,width)
		stop = True
		for cycle in range(int(cycles)):
			#check if the battery is greater than one 
			#check the terrain of the next tile
			next_tile_elv = planet_tiles[next_y][next_x].get_elevation()
			#check if not sloped
			does_rover_move = False
			if len(rov_terrain) == 1:
				if rov_terrain[0] in next_tile_elv:
					does_rover_move = True
			elif len(rov_terrain) == 2:
				if rov_terrain[0] in next_tile_elv or rov_terrain[1] in next_tile_elv:
					does_rover_move = True
			if does_rover_move:
				#check if the rover is able to move to the next tile
				self.y,self.x = next_y, next_x
				next_y,next_x = self.update_next_tile(direction,height,width)
				self.set_tiles_explored((self.x,self.y))
				#will not stop, will move to the next iteration
				stop = False
				#if it's shaded, lose battery
				if planet_tiles[self.y][self.x].is_shaded():
					self.battery -=1 
						#if the rover is on a sloped tile
			if stop:
				break
					
	def wait(self, cycles):
		"""
		The rover will wait for the specified cycles
		"""
		self.battery += int(cycles)
		#the battery cannot be more than 100, so reduce to 100
		if self.battery > 100:
			self.battery = 100
	
	def get_rover_cor(self):
		return (self.x,self.y)
	
	def rover_x(self):
		return self.x
	
	def rover_y(self):
		return self.y
	
	#the length of the set is equal to the number of tiles
	def get_num_explored(self):
		return len(self.tiles_explored_set)
	
	def get_battery(self):
		return self.battery
	
	def set_tiles_explored(self, tile_cor):
		self.tiles_explored_set.add(tile_cor)
