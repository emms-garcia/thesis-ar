#!/usr/bin/python
# -*- coding: utf-8

#Simple class used to do some vector calculations
class Vector2:
	def __init__(self, (x, y)):
		self.x = x
		self.y = y

  #Sum the vector values and return the result
	def sum(self):
		return self.x + self.y

  #Clone the vector object
	def clone(self):
		return Vector2((self.x, self.y))

  #Add another vector into this vector and return the changed vector
	def add(self, v):
		self.x += v.x
		self.y += v.y
		return self

  #Substract another vector from this vector and return the changed vector
	def sub(self, v):
		self.x -= v.x
		self.y -= v.y
		return self

  #Substract a scalar value from every value in this vector and return the changed vector
	def subScalar(self, s):
		self.x -= s
		self.y -= s
		return self
    
	#Add a scalar value from every value in this vector and return the changed vector
	def addScalar(self, s):
		self.x += s
		self.y += s
		return self

  #Multiply two vectors, storing the results in this vector and return the changed vector
	def multiply(self, v):
		self.x *= v.x
		self.y *= v.y 
		return self

  #Multiply every value from this vector with a scalar value and return the changed vector
	def multiplyScalar(self, s):
		self.x *= s
		self.y *= s
		return self

  #Divide this vector by another vector and return the changed vector
	def divide(self, v):
		self.x /= v.x
		self.y /= v.y
		return self

  #Divide every value in this vector by a scalar and return the changed vector
	def divideScalar(self, s):
		self.x /= s
		self.y /= s
		return self

#Box class to define a square and calculate its centroid and other useful data given two vertices
class Box2:
 
  def __init__(self, min = None, max = None):
    self.min = min or Vector2((1e100, 1e100))
    self.max = max or Vector2((-1e100, -1e100))
    self.center = self.max.clone().add(self.min).divideScalar(2)
    
  def setFromVectors(self, v_list):
    for v in v_list:
      if v.x > self.max.x: self.max.x = v.x
      if v.x < self.min.x: self.min.x = v.x
      if v.y > self.max.y: self.max.y = v.y
      if v.y < self.min.y: self.min.y = v.y
    self.center = self.max.clone().add(self.min).divideScalar(2)
    return