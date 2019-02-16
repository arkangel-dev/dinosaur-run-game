import pygame
class Blockade:
	def __init__(self, name, position):
		self.x = 286
		self.y = 900
		self.rect = name.get_rect()
		self.position = name.get_rect().move(900,286)
		self.name = name
		
		
		
	def Move(self, speed):
		self.position = self.position.move(speed,0)
		return(self.position)
		
	def GetRect(self):
		self.position = self.position
		return(self.position)
	