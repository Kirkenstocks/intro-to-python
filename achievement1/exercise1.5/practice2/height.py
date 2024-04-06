class Height(object):
  def __init__(self, feet, inches):
    self.feet = feet
    self.inches = inches

  def __str__(self):
    output = str(self.feet) + " feet, " + str(self.inches) + " inches"
    return output
  
  def __add__(self, other):
    height_A_inches = self.feet * 12 + self.inches
    height_B_inches = other.feet * 12 + other.inches

    total_height_inches = height_A_inches + height_B_inches

    output_feet = total_height_inches / 12
    output_inches = total_height_inches - (output_feet * 12)

    return Height(output_feet, output_inches)
  
  def __sub__(self, other): 
    height_C_inches = self.feet * 12 + self.inches
    height_D_inches = other.feet * 12 + other.inches

    difference_height_inches = height_C_inches - height_D_inches

    output_feet_diff = int(difference_height_inches / 12)
    output_inches_diff = difference_height_inches % 12

    return Height(output_feet_diff, output_inches_diff)
  
height_1 = Height(5, 10)
height_2 = Height(3, 9)
height_difference = height_1 - height_2

print("Height difference:", height_difference)

