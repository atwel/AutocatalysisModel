import pyglet
import math


class Cell(object):

    	def __init__(self, radius, skew, text, position=None):
    		self.verts = []
    		self.text = text
    		self.rules = {}
    		for i in range(360):
			rads =  (6.28318531*i)/360.
			self.verts.append((int(radius*skew*math.cos(rads)), 
				int(radius* math.sin(rads)))) 
			self.verts.append((int((radius*skew-1)*math.cos(rads)), 
				int((radius-1)* math.sin(rads))))
		self.x, self.y = (0, 0)
		if position != None:
        			self.translate(position[0], position[1])


	def add_rule(self, rule):
		self.rules["-".join([str(rule.get_input()), str(rule.get_output())])] = rule

	def count_rules(self):
		return len(self.rules.keys())
      	def remove_rule(self, rule):
      		del self.rules["-".join([str(rule.get_input()), str(rule.get_output())])]

	def translate(self, dx, dy):
		self.x += dx
		self.y += dy
		for i in range(len(self.verts)):
			x,y = self.verts[i] 
			self.verts[i] = (x + dx, y + dy)



class Link(object):

    	def __init__(self, start, end, s2=None, e2=None):
    		if s2 == None:
    			self.verts = []
    			x_inc = (end[0] - start[0])/100.
    			y_inc = (end[1] - start[1])/100.

    			for i in range(100):
    				self.verts.append((int(i*x_inc+start[0]), int(i*y_inc+start[1])))

    		else:
    			self.verts = []
    			x_inc = (end[0] - start[0])/50.
    			y_inc = (end[1] - start[1])/50.

    			for i in range(50):
    				self.verts.append((int(i*x_inc+start[0]), int(i*y_inc+start[1])))

    			x_inc = (e2[0] - s2[0])/50.
    			y_inc = (e2[1] - s2[1])/50.

    			for i in range(50):
    				self.verts.append((int(i*x_inc+s2[0]), int(i*y_inc+s2[1])))


    		#print self.verts

    		


class Product(object):

	def __init__(self, verts, type, position=None):
		self.verts = verts
		if position is None:
			position = (0, 0)
		self.x, self.y = position
		self.type = type


class Network(object):

	def __init__(self, nXnet,win):
		self.win = win
		self.cells = {}
		self.links = {}

		radius = int(self.win.width/12.)*1.3
		origin = ((self.win.width/24.), (self.win.height/24.))
		x_inc = self.win.width/12.
		y_inc = self.win.height/12.
		skew = self.win.width/float(self.win.height)
		text = "No Rules"
		rule_locs = []


		for rule in nXnet.net.nodes():
			# the nodes in this network are product (net) rules.
			
			if not rule.owner.id in self.cells.keys():
				x_cell = int(rule.owner.location[0]*x_inc + origin[0])
				y_cell = int(rule.owner.location[1]*x_inc + origin[1])
				newCell = Cell(radius/3., skew, text, (x_cell, y_cell))
				newCell.add_rule(rule)
				self.cells[rule.owner.id] = newCell
				rule_locs.append((x_cell,y_cell))

			else:
				self.cells[rule.owner.id].add_rule(rule)

		edge_locs = []
		for rule1, rule2 in nXnet.net.edges():
			if rule1.owner.id not in self.cells.keys():
				x_cell = int(rule1.owner.location[0]*x_inc + origin[0])
				y_cell = int(rule1.owner.location[1]*y_inc + origin[1])
				newCell = Cell(radius/3., skew, text, (x_cell, y_cell))
				self.cells[rule1.owner.id] = newCell
			if rule2.owner.id not in self.cells.keys():
				x_cell = int(rule2.owner.location[0]*x_inc + origin[0])
				y_cell = int(rule2.owner.location[1]*y_inc + origin[1])
				newCell = Cell(radius/3., skew, text, (x_cell, y_cell))
				self.cells[rule2.owner.id] = newCell

			x1, y1 = int(rule1.owner.location[0]* x_inc+ origin[0]), int(rule1.owner.location[1]* y_inc+ origin[1])
			x2, y2 = int(rule2.owner.location[0]* x_inc+ origin[0]), int(rule2.owner.location[1]* y_inc+ origin[1])
			edge_locs.append(((x1,y1),(x2,y2)))
			#print abs(x1 - x2 ), 1. *x_inc
			if abs(x1- x2)  <= 1.5 * x_inc and abs(y1 - y2) <= 1.5 * y_inc:
				self.links[rule1, rule2] = Link((x1,y1), (x2, y2))
			else:
				if abs(x1- x2)  <= 1.1 * x_inc:
					max_y = max(y1,y2)
					if max_y == y1:
						max_x = x1
						min_y = y2
						min_x = x2
					else:
						max_x = x2
						min_y = y1
						min_x = x1
					self.links[rule1, rule2] = Link((max_x,max_y), 
						(max_x +(min_x-max_x)/2., max_y + y_inc/2.), 
						(min_x,min_y), 
						(min_x + (max_x - min_x)/2., min_y - y_inc/2.))

				elif abs(y1 - y2) <= 1.1 * y_inc:
					max_x = max(x1,x2)
					if max_x == x1:
						max_y = y1
						min_y = y2
						min_x = x2
					else:
						max_y = y2
						min_y = y1
						min_x = x1
					self.links[rule1, rule2] = Link((max_x, max_y), 
						(max_x +x_inc/2., max_y + (min_y-max_y)/2.), 
						(min_x,min_y), 
						(min_x - x_inc/2., min_y + (max_y - min_y)/2.))
				else: 
					if max(x1,x2) == x1:
						if  max(y1,y2) == y1:
							self.links[rule1, rule2] = Link((x1, y1), 
								(x1 +x_inc/2., y1 + y_inc/2.), 
								(x2,y2), 
								(x2 - x_inc/2., y2 - y_inc/2.))
						else:
							self.links[rule1, rule2] = Link((x1,y1), 
								(x1 + x_inc/2., y1 - y_inc/2.), 
								(x2,y2), 
								(x2 - x_inc/2., y2 + y_inc/2.))
					else:
						if max(y1,y2) == y1:
							self.links[rule1, rule2] = Link((x1, y1), 
								(x1 - x_inc/2., y1 + y_inc/2.), 
								(x2,y2), 
								(x2 + x_inc/2., y2 - y_inc/2.))
						else:
							self.links[rule1, rule2] = Link((x1,y1), 
								(x1 - x_inc/2., y1 - y_inc/2.), 
								(x2,y2), 
								(x2 + x_inc/2., y2 + y_inc/2.))

		batch = pyglet.graphics.Batch()

		for link in self.links.values():
			color = (0,255,255)
			for vert in link.verts:
				batch.add(1, pyglet.gl.GL_POINTS,None,('v2i', vert),('c3B', color))
		for cell in self.cells.values():

			color = (0,int(cell.count_rules()*1.275),255)
			for vert in cell.verts:
				batch.add(1, pyglet.gl.GL_POINTS,None,('v2i', vert),('c3B', color))

		self.batch = batch


	def remove_link(self, link):
		pass

	def remove_cell(self, cell):
		pass

