#!/usr/bin/python

class Vector2:
	def __init__(self, (x, y)):
		self.x = x
		self.y = y

	def sum(self):
		return self.x + self.y

	def clone(self):
		return Vector2((self.x, self.y))

	def add(self, v):
		self.x += v.x
		self.y += v.y
		return self

	def sub(self, v):
		self.x -= v.x
		self.y -= v.y
		return self

	def subScalar(self, s):
		self.x -= s
		self.y -= s
		return self
	
	def addScalar(self, s):
		self.x += s
		self.y += s
		return self

	def multiply(self, v):
		self.x *= v.x
		self.y *= v.y 
		return self

	def multiplyScalar(self, s):
		self.x *= s
		self.y *= s
		return self

	def divide(self, v):
		self.x /= v.x
		self.y /= v.y
		return self

	def divideScalar(self, s):
		self.x /= s
		self.y /= s
		return self

class Box2:
	def __init__(self, (min, max)):
		self.min = min
		self.max = max
		self.center = self.max.clone().sub(self.min).divideScalar(2)