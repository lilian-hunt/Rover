class Tile:
	def __init__(self,info):
		"""
		Initialises the terrain tile and attributes
		"""
		self.slope= False
		#the default is that there is no slope
		#type is either shaded or not shaded
		self.type = info[0]
		self.highest_elevation = int(info[1])
		# if there are 3 arguments assign the lowest_elevation 
		if len(info)== 3:
			self.lowest_elevation = int(info[2])
			self.slope = True
			
	def get_elevation(self):
		"""
		Returns an integer value of the elevation number 
		of the terrain object
		"""
		#check if it is a slope or not to make sure we are accessing 
		#an element that exists for the instance	
		if not self.slope:
			return [self.highest_elevation]
		else:
			return [self.highest_elevation,self.lowest_elevation]
		
	def is_shaded(self):
		"""
		Returns True if the terrain tile is shaded, otherwise False
		"""
		if self.type == "shaded":
			return True
		return False
