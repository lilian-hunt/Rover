class Planet:
	def __init__(self, name, width, height,tiles):
		self.name = name
		self.width = int(width)
		self.height = int(height)
		self.tiles = tiles #tiles are a matrix, each is an instance of the Tile class
	
	def get_tiles(self):
		return self.tiles
	
	def get_height(self):
		return self.height
	
	def get_width(self):
		return self.width
	
	def get_num_tiles(self):
		return int(self.width*self.height)
	
	def get_name(self):
		return self.name
