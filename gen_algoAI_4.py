import pygame
import time
from random import randint
pygame.init()
pygame.font.init()
pygame.mixer.init()

# setup the window variables...
screen_height = 550
screen_width = 900
spritegroup = pygame.sprite.Group()

# color variables...
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

# setup the screen...
(screenHeight, screenWidth) = (550, 900)
canvas = pygame.Surface((900, 550))
screen = pygame.display.set_mode((screenWidth, screenHeight))
p1_camera = pygame.Rect(0,0,900, 200)
p2_camera = pygame.Rect(0,200,900,350)

hud = canvas.subsurface(p1_camera)
SimulationScreen = canvas.subsurface(p2_camera)
hud.fill(white)
beep = pygame.mixer.Sound('beep.wav')

# define fonts...
myfont = pygame.font.SysFont('System', 20)
hudfont = pygame.font.SysFont('System', 20)

print(format(time.gmtime()))
# ===========[ Game Elements ]===================================
# setup the player...
player = pygame.image.load('player1.bmp').convert()
player.set_colorkey(white)
position = player.get_rect()
position = position.move(50, 286)
SimulationScreen.blit(player, position)
playerRect = player.get_rect()
playerMask = pygame.mask.from_surface(player)
pygame.display.update()
	

# setup the blockades
blockade = pygame.image.load('blockade.bmp').convert()
blockade.set_colorkey(white)
bposition = blockade.get_rect()
SimulationScreen.blit(blockade, bposition)
blockadeMask = pygame.mask.from_surface(blockade)
pygame.display.update()

# setup the floating blockades
Fblockade = pygame.image.load('floating_blockades1.bmp').convert()
Fblockade.set_colorkey(white)
Fbposition = Fblockade.get_rect()
SimulationScreen.blit(Fblockade, Fbposition)
FblockadeMask = pygame.mask.from_surface(Fblockade)
pygame.display.update()


# boolean variables...
Progress = True
jump = False
accend = False
ducked = False
AIducked = False
AIDucking = False
animationRunning = False
AIJump = False
ManualAIActive = True
consoleOpened = False

# array variables...
objectsMasterNames = []
objectsMasterNames = []
blockades = []
Fblockades = []
HiddenNode = []
HiddenNodex = []
HiddenNodey = []
ConnectionsStartx = []
ConnectionsStarty = []
ConnectionsEndx = []
ConnectionsEndy = []
Connections = []
Coordinates = []
NodeActivated = [False, False, False, False, False, False, False, False, False, False, False, False, False]

# string variables...
downButton = pygame.K_DOWN
upButton = pygame.K_UP
AIActionOutput = 'NA'

# init increment variables...
animCount = 0
animTCount = 0
fitness = 0
onScreenObjectCount = 0
blockSpace = 0
FblockSpace = 0
speed = -14
FblockadeShortest = 5000
blockadeShortest = 5000
shortestFinal = 5000
delayTime = 5
AIDuckingWait = 0
nextObjectIndex = 0
FblockadeIntroDist = 500
speedIncrease = 0
step = 1
birdStep = 1

SimulationScreen.fill(white)
pygame.draw.line(SimulationScreen, black, (0,510), (600,510), 10)
screen.blit(SimulationScreen, (0, 200))
pygame.display.update()

# ======================[ definitons start here ]======================================

def update():
	pygame.draw.line(SimulationScreen, black, (0,330), (1200,330), 3) #draw the line...
	pygame.draw.line(SimulationScreen, black, (0,0), (1200,0), 3) #draw the line...
	SimulationScreen.blit(player, position) # draw player...
	# text elements...
	SimulationScreen.blit(fitnessPrint,(90,25)) # update fitness...
	SimulationScreen.blit(nextBlockDistance,(160,50)) # update distance...
	SimulationScreen.blit(speedDisp, (85, 75)) # update speed
	SimulationScreen.blit(nextObjectName, (390, 25)) # update next object name...
	SimulationScreen.blit(nextObjectHeight, (430, 50)) # update next object height...
	SimulationScreen.blit(AIAction, (430, 75)) # update the AI's current action...
	SimulationScreen.blit(fitnessHeading,(25,25)) # update fitness heading...
	SimulationScreen.blit(nextBlockDistanceHeading,(25,50)) # update distance heading...
	SimulationScreen.blit(speedHeading, (25, 75)) # update speed heading...
	SimulationScreen.blit(nextObjectHeading, (300, 25)) # update object name heading...
	SimulationScreen.blit(nextObjectHeightHeading, (300, 50)) # update next object hight heading...
	SimulationScreen.blit(AIActionHeading, (300, 75)) # update the AI's action heading...

# update the screen
def updateScreen():
	screen.blit(hud, (0,0))
	screen.blit(SimulationScreen, (0, 200))
	pygame.display.update() # update SimulationScreen...
	
# birds...
class FloatBlockade:
	def __init__(self, name, position):
		self.x = 120
		self.y = 500
		self.rect = name.get_rect()
		self.position = name.get_rect().move(900,randint(200, 290))
		self.name = name
	def FloatMove(self, speed):
		self.position = self.position.move((speed - 3),0)
		return(self.position)
		
	def GetRect(self):
		self.position = self.position
		return(self.position)

# normal cactus blocks...
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
		
def MakeConnection(coord1, coord2, color, width):
	Connections.append(pygame.draw.line(hud, color,coord1, coord2, width))



# =====================[ definitons end here ]===========================================

# ==========================[ make the neural network ]====================================


# make initial variables...
for i in range (8):
	HiddenNode.append(pygame.image.load('network_node.bmp').convert())
Coordinates.append((220,25))
Coordinates.append((220,50))
Coordinates.append((220,75))
Coordinates.append((220,100))
for i in range (0,4):
	Coordinates.append((420, ((i * 25) + 25)))
for i in range (4,8):
	Coordinates.append((620, ((i - 4) * 25 + 25)))
Coordinates.append((820,50))
Coordinates.append((820,75))



# right now there just a few inputs for the neural network to work with...
# 1. Distance From Next Obstacle (230, 30)
# 2. Height Of Obstacle (230, 55)
# 3. Bias (230, 80)
#
# the outputs are as follows...
# 1. Jump (680, 55)
# 2. Duck (680, 60)

DFNONode = pygame.image.load('network_node.bmp').convert()
HONONode = pygame.image.load('network_node.bmp').convert()
SpeedNode = pygame.image.load('network_node.bmp').convert()
BiasNode = pygame.image.load('network_node.bmp').convert()
JumpNode = pygame.image.load('network_node.bmp').convert()
DuckNode = pygame.image.load('network_node.bmp').convert()


TextDFNO = hudfont.render('Distance From Next Obstacle', True, black)
TextHONO = hudfont.render('Height Of Obstacle', True, black)
TextSpeed = hudfont.render('Speed', True, black)
TextBias = hudfont.render('Bias', True, black)
TextJump = hudfont.render('Jump', True, black)
TextDuck = hudfont.render('Duck', True, black)



MakeConnection(Coordinates[0], Coordinates[6], red, 3)
MakeConnection(Coordinates[1], Coordinates[5], red, 2)
MakeConnection(Coordinates[3], Coordinates[5], blue, 2)
MakeConnection(Coordinates[1], Coordinates[6], blue, 2)
MakeConnection(Coordinates[5], Coordinates[12], red, 2)
MakeConnection(Coordinates[6], Coordinates[13], red, 3)
MakeConnection(Coordinates[3], Coordinates[6], blue, 3)



for i in range (0,4):
	hud.blit(HiddenNode[i], (420, ((i * 25) + 22)))
	HiddenNodex.append(420)
	HiddenNodey.append((i * 25 + 25))
for i in range (4,8):
	hud.blit(HiddenNode[i], (620, ((i - 4) * 25 + 22)))
	HiddenNodex.append(620)
	HiddenNodey.append((i - 4) * 25 + 25)
	
# for i in range (0,7):
	# ConnectionsEndx.append(HiddenNodex[i])
	# ConnectionsEndy.append(HiddenNodey[i] + 2)
	# MakeConnection(220, 25, HiddenNodex[i], HiddenNodey[i], blue, randint(1,4))

for i in (Connections):
		i

hud.blit(TextDFNO, (25, 22))
hud.blit(TextHONO, (25, 47))
hud.blit(TextBias, (25, 72))
hud.blit(TextSpeed, (25, 97))
hud.blit(TextJump, (850, 47))
hud.blit(TextDuck, (850, 72))

updateScreen()
hud.blit(DFNONode, (220, 22))
hud.blit(HONONode, (220, 47))
hud.blit(BiasNode, (220, 72))
hud.blit(SpeedNode, (220, 97))
hud.blit(JumpNode, (820, 47))
hud.blit(DuckNode, (820, 72))




beep.play()
# =====================[ reloading the screen starts here ]===============================
# =====================[ Simulation Engine Starts Here ]==================================
while Progress:
	# Global increments...
	speed = speed - 0.00005
	fitness = fitness + 1
	speedIncrease = speedIncrease + 0.00005
	onScreenObjectCount = 0
	for o in objectsMasterNames:
		onScreenObjectCount = onScreenObjectCount + 1
	
	# Texts...
	SimulationScreen.fill(white) # redraw the background for the simulation...
	fitnessHeading = myfont.render('Fitness :', True, (0, 0, 0))
	speedHeading = myfont.render('Speed :', True, (0, 0, 0))
	nextBlockDistanceHeading = myfont.render('Next Block Distance :', True, (0, 0, 0))
	nextObjectHeading = myfont.render('Next Object :', True, (0, 0, 0))
	nextObjectHeightHeading = myfont.render('Next Object Height:', True, (0, 0, 0))
	AIActionHeading = myfont.render('AIs Input:', True, (0, 0, 0))
		
	if (shortestFinal == 9999):
		nextBlockDistance = myfont.render('NA', True, (0, 0, 0))
	else:
		nextBlockDistance = myfont.render(str(shortestFinal), True, (0, 0, 0))
	if (onScreenObjectCount > 0):
		nextObjectName = myfont.render(str(objectsMasterNames[nextObjectIndex]), True, (0, 0, 0))
	else:
		nextObjectName = myfont.render('NA', True, (0, 0, 0))
	if (onScreenObjectCount > 0):
		nextObjectHeight = myfont.render(str(objectsMasterNames[nextObjectIndex].GetRect().y), True, (0, 0, 0))
	else:
		nextObjectHeight = myfont.render('NA', True, (0, 0, 0))
	AIAction = myfont.render(AIActionOutput, True, (0, 0, 0))
	fitnessPrint = myfont.render(str(fitness), True, (0, 0, 0))
	speedDisp = myfont.render(str(speed), True, (0,0,0))
	
	pressedkey = pygame.key.get_pressed() # get an array of pressedkeys...
	for event in pygame.event.get(): # key input check segment...
		if (event.type == pygame.QUIT):	# close windows...
			Progress = False

# ====================================[ input and control segment ]=========================
	if (pressedkey[pygame.K_SLASH] == 1) and (consoleOpened == False):
		consoleOpened = True
		command = input('/geo_runner/dev/>')
		if (command == 'setManualAI(deactive)'):
			ManualAIActive = False
			print('[+] Manual AI deactivated...')
		elif (command == 'setManualAI(active)'):
			ManualAIActive = True
			print('[+] Manual AI activated...')
		elif (command == 'setDelay'):
			delayInput = input('/geo_runner/dev/setDelay/>')
			delayTime = int(delayInput)
			print('[+] delaying screen by', delayInput,'...')
		else:
			print('[!] command unrecognised...')
	else:
		consoleOpened = False

	# CHEATER!!...
	if (ManualAIActive == True):
		if (((shortestFinal <= (145 + speedIncrease)) and (shortestFinal > 20)) and (objectsMasterNames[nextObjectIndex].GetRect().y > 270))  and (animationRunning == False):
			AIJump = True
			accend = True
			jump = True
		elif (shortestFinal <= (135 + speedIncrease)) and (objectsMasterNames[nextObjectIndex].GetRect().y <= 270):
			AIDucking = True
		else:
			AIDucking = False
			AIJump = False
	
	# #this is for testing the AI's input interface...
	# if (pressedkey[pygame.K_LEFT] == 1):
		# AIDucking = True
	# elif (pressedkey[pygame.K_RIGHT] == 1) and (animationRunning == False):
		# AIJump = True
		# accend = True
		# jump = True
	# else:
		# AIDucking = False
		# AIJump = False
		
	if (animationRunning == False): # detect the jump function...
		if (pressedkey[pygame.K_UP] == 1):
			jump = True
			accend = True
			
	if (jump == True):	# checking if jump function has been invoked...
		animationRunning = True
		animTCount = animTCount + 1
		if (accend == True):	
			animCount = animCount + 1
			position = position.move(0, (-1 * (animCount * 5))) # accending mecha...
		else:
			animCount = animCount + 1 # falling mecha...
			position = position.move(0, (animCount * 5))
		if (animCount == 5):
			animCount = 0
			accend = False
		if (animTCount == 10):
			jump = False
			animTCount = 0
			animationRunning = False
			# end of jumping function...
			
	if (AIducked == False): # if the AI is ducking... the user cannot duck...
			# ducking function...	
		if (ducked == False) and (pressedkey[pygame.K_DOWN] == 1):
				position = position.move(0, 19)
				ducked = True
		elif (ducked == True) and (pressedkey[pygame.K_DOWN] == 0):
				position = position.move(0, -19)
				ducked = False
			
			
		# ducking function for the AI...
	if ((AIDucking == True) and (AIducked == False)):
			position = position.move(0, 19)
			AIducked = True
	elif (AIDucking == False) and (AIducked == True):
			AIDuckingWait = AIDuckingWait + 1
			
	if (AIDuckingWait == 10):
		position = position.move(0, -19)
		AIducked = False
		AIDuckingWait = 0
		

# =====================================[ block spawning segment ]===========================
	
	# block printing mech...
	blockSpace = blockSpace + 1
	if (blockSpace == 25): # make sure that there is enough gap between to land...
		blockSpace = 0
		choice = randint(0, 1)
		if (choice == 1):
			typeChoice = randint(0, 1) # select the type of block to spawn...
			if (typeChoice == 1): # 1 is floating block...
					o = Blockade(blockade, blockade.get_rect())
					blockades.append(o)
					objectsMasterNames.append(o)
			elif (typeChoice == 0): # 0 is normal block...
					o = FloatBlockade(blockade, blockade.get_rect())
					Fblockades.append(o)
					objectsMasterNames.append(o)
						

				
	for o in blockades:
		SimulationScreen.blit(blockade, o.Move(speed))
		blockadeRect = o.GetRect()
		playerRect = position
		offset_x, offset_y = (blockadeRect.left - position.left), (blockadeRect.top - position.top)
		if (playerMask.overlap(blockadeMask, (offset_x, offset_y)) != None): # check if the user has collided with the block...
			Progress = False # if so kill the simulation...	
		if (blockadeRect.x <= 0): # if the block reaches rect.x of 0...
			blockades.remove(o) # remove it from the array...
			objectsMasterNames.remove(o)

	for o in Fblockades:
		SimulationScreen.blit(Fblockade, o.FloatMove(speed))
		FblockadeRect = o.GetRect()
		playerRect = position
		offset_x, offset_y = (FblockadeRect.left - position.left), (FblockadeRect.top - position.top)
		if (playerMask.overlap(FblockadeMask, (offset_x, offset_y)) != None):
			update()
			updateScreen()
			Progress = False 
		if (FblockadeRect.x <= 0):
			Fblockades.remove(o)
			objectsMasterNames.remove(o)
	
	shortestFinal = 9999 # magic number...
	
	count = 0
	for o in objectsMasterNames:
		blockDist = (o.GetRect().x)
		if (blockDist < shortestFinal):
			shortestFinal = blockDist
			nextObjectIndex = count
		count = count + 1
	
	# Debug the AI's input...
	if (AIDucking == True):
		AIActionOutput = 'ducking'
	elif (AIJump == True):
		AIActionOutput = 'jumping'
	else:
		AIActionOutput = 'NA'
		
	# animate the normal running sequence...
	if (ducked != True) and (AIducked != True):
		if (step == 1) and (animationRunning == False):
			player = pygame.image.load('player1.bmp').convert()
			player.set_colorkey(white)
			playerMask = pygame.mask.from_surface(player)
			step = 2
		elif (step == 2) and (animationRunning == False):
			player = pygame.image.load('player2.bmp').convert()
			player.set_colorkey(white)
			playerMask = pygame.mask.from_surface(player)
			step = 1
	# animate the bird sequence
	if (birdStep == 1):
		Fblockade = pygame.image.load('floating_blockades2.bmp').convert()
		birdStep = 2
	elif (birdStep == 2):
		Fblockade = pygame.image.load('floating_blockades1.bmp').convert()
		birdStep = 1
		
	# animate the ducking sequence...
	if (ducked == True) or (AIducked == True):
		if (step == 1) and (animationRunning == False):
			player = pygame.image.load('player_ducking1.bmp').convert()
			player.set_colorkey(white)
			playerMask = pygame.mask.from_surface(player)
			step = 2
		elif (step == 2) and (animationRunning == False):
			player = pygame.image.load('player_ducking2.bmp').convert()
			player.set_colorkey(white)
			playerMask = pygame.mask.from_surface(player)
			step = 1
	if (animationRunning == True):
		player = pygame.image.load('player_jumping.bmp').convert()
		player.set_colorkey(white)
		playerMask = pygame.mask.from_surface(player)
# =============================[ screen refresh segment ]==================================
		

	update()
	updateScreen()
	pygame.time.delay(delayTime)	# delay 1/10 th of a second...
	
# ==========================[ Simulation Engine Ends Here ]===============================
print('[+] simulation ended...')
print('[+] died at', fitness,'...')
print('[+] press enter to exit...')
print(format(time.gmtime()))
beep.play()
input()
