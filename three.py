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
  
  def __init__(self, min = None, max = None):
    self.min = min or Vector2((1e100, 1e100))
    self.max = max or Vector2((-1e100, -1e100))
    self.center = self.max.clone().sub(self.min).divideScalar(2)
    
  def setFromVectors(self, v_list):
    for v in v_list:
      if v.x > self.max.x: self.max.x = v.x
      if v.x < self.min.x: self.min.x = v.x
      if v.y > self.max.y: self.max.y = v.y
      if v.y < self.min.y: self.min.y = v.y
    self.center = Vector2(((self.max.x - self.min.x)/2.0, (self.max.y - self.min.y)/2.0))
    return