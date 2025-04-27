# A class for modeling a point as a location in 2D space
class Point:
   # A constructor that creates a point at a given location as x and y values
   # (The default values for the given location are set as x = 0 and y = 0.)
   def __init__(self, x=0, y=0):
      self.x = x
      self.y = y

   # Moves this point by dx along the x-axis and by dy along the y-axis
   def translate(self, dx, dy):
      self.x += dx
      self.y += dy

   # Moves this point to a given location (x, y)
   def move(self, x, y):
      self.x = x
      self.y = y

   # Overloaded __str__ method (automatically invoked when printing a point)
   def __str__(self):
      return "(" + str(self.x) + ", " + str(self.y) + ")"
