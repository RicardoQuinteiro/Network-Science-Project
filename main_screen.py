import pygame
from screen import screen
from text_box import text_box
from button import button
import sys
vec = pygame.math.Vector2

class main_screen(screen):

	def __init__(self, width, height, window):

		self.width = width
		self.height = height
		self.window = window

		self.running = True
		self.traits_ready = False
		self.text_boxes = []
		self.buttons = []
		self.buttons_dic = dict()
		#self.screen_type = screen_type

		#Adding Text Boxes
		self.text_boxes += [text_box(1000, 100, 100, 20, title="Minimum Neighbours (%)", border=1, is_float=True)]
		self.text_boxes += [text_box(1000, 150, 100, 20, title="Maximum Neighbours (%)", border=1, is_float=True)]
		self.text_boxes += [text_box(1000, 200, 100, 20, title="Empty Spots (%)", border=1, is_float=True)]
		self.text_boxes += [text_box(1000, 250, 100, 20, title="Width", border=1, is_int=True)]
		self.text_boxes += [text_box(1000, 300, 100, 20, title="Height", border=1, is_int=True)]

		self.inputs = dict()
		self.inputs["Traits"] = 0

		#Adding Buttons
		self.start_button = button(925, 400, 100, 40, text="Run", hor_space=50, ver_space=2)
		self.buttons += [button(850, 100, 20, 20, text="2", border=2, text_size=10, hor_space=15, ver_space=4)]
		self.buttons_dic["2"] = False
		self.buttons += [button(875, 100, 20, 20, text="3", border=2, text_size=10, hor_space=15, ver_space=4)]
		self.buttons_dic["3"] = False
		self.buttons += [button(900, 100, 20, 20, text="4", border=2, text_size=10, hor_space=16, ver_space=4)]
		self.buttons_dic["4"] = False
		self.buttons += [button(925, 100, 20, 20, text="5", border=2, text_size=10, hor_space=15, ver_space=4)]
		self.buttons_dic["5"] = False

		#Message settings
		self.intro_font = pygame.font.SysFont("times new roman", 40, bold=True)
		self.intro_text_colour = (0,51,102)
		self.intro_message = "Set the parameters"
		self.intro_pos = vec(self.width//10, self.height//5)

		#Traits text settings
		self.trait_font = pygame.font.SysFont("times new roman", 12, bold=True)
		self.trait_text_colour = (0,51,102)
		self.trait_message = "Number of Traits"
		self.trait_pos = vec(850, 80)

	def run(self):
		#Showing message and button text
		text_surface = self.intro_font.render(self.intro_message, False, self.intro_text_colour)
		self.window.blit(text_surface, self.intro_pos)
		text_surface = self.trait_font.render(self.trait_message, False, self.trait_text_colour)
		self.window.blit(text_surface, self.trait_pos)

		#Update number of extra boxes
		self.add_boxes()

		#Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			#Check where the mouse clicks
			if event.type == pygame.MOUSEBUTTONDOWN:
				for box in self.text_boxes:
					box.check_click(pygame.mouse.get_pos())
				for button in self.buttons:
					button.check_click(pygame.mouse.get_pos())
					if button.active:
						self.buttons_dic[button.text] = True
						self.inputs["Traits"] = int(button.text)
						for but in self.buttons_dic:
							if but != button.text:
								self.buttons_dic[button.text] = False
					if not self.buttons_dic[button.text]:
						button.deactivate()
				self.start_button.check_click(pygame.mouse.get_pos())
				if self.start_button.active:		
					for box in self.text_boxes:	
						self.inputs[box.title] = box.return_value()
					if self.inputs_ready():
						self.running = False
					else:
						self.start_button.active = False					
			if event.type == pygame.KEYDOWN:
				#Close window when ESC key is pressed
				if event.key == 27:
					pygame.quit()
					sys.exit()
				#Configuring TAB key to change to the next text box
				elif event.key == 9:
					for i in range(len(self.text_boxes)):
						if self.text_boxes[i].active:
							self.text_boxes[i].active = False
							if i == len(self.text_boxes)-1:
								self.text_boxes[0].active = True
								break
							else:
								self.text_boxes[i+1].active = True
								break
				else:	
					#Write text in active boxes
					for box in self.text_boxes:
						if box.active:
							box.add_text(event.key)

		#Drawing boxes and buttons			
		for box in self.text_boxes:
			box.draw(self.window)
			box.draw_title(self.window)
		self.start_button.draw(self.window)
		for button in self.buttons:
			button.draw(self.window)

	def inputs_ready(self):
		try:
			return (self.inputs["Width"] != "" and self.inputs["Height"] != "")
		except:
			return False
	
	def return_inputs(self):
		inps = dict()
		inps["min"] = self.inputs["Minimum Neighbours (%)"]/100
		inps["max"] = self.inputs["Maximum Neighbours (%)"]/100
		inps["traits"] = self.inputs["Traits"]
		inps["empty"] = self.inputs["Empty Spots (%)"]/100
		inps["size"] = [self.inputs["Width"], self.inputs["Height"]]
		inps["percent"] = []
		for i in range(inps["traits"]):
			inps["percent"] += [self.inputs["Percentage " + str(i+1)]/100]
		return inps

	def add_boxes(self):
		k = len(self.text_boxes) - 5
		while k != self.inputs["Traits"]:
			if self.inputs["Traits"] > k:
				self.text_boxes += [text_box(850, 150 + k*50, 100, 20, title="Percentage " + str(k+1), border=1, is_float=True)]
			else:
				self.text_boxes.pop()
			k = len(self.text_boxes) - 5
		return


