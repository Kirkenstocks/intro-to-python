# defining a class for recipes
class Recipe:
  all_ingredients = []

  # initialization method, takes a name attribute as a parameter 
  def __init__(self, name):
    self.name = str(name)
    self.cooking_time = 0
    self.ingredients = []
    self.difficulty = ""

  # getter method for name
  def get_name(self):
    output = "Name: " + self.name
    return output
  
  # setter method for name
  def set_name(self, name):
    self.name = name

  # getter method for cooking time
  def get_cooking_time(self):
    output = "Cooking time in minutes: " + str(self.cooking_time)
    return output

  # setter method for cooking time  
  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time

  # method to add ingredients to recipe and the all_ingredients class variable
  def add_ingredients(self, *ingredients):
    for ingredient in ingredients:
      self.ingredients.append(ingredient)
      self.update_all_ingredients()

  # getter method for an object's ingredients
  def get_ingredients(self):
    return self.ingredients
  
  # getter method for the all_ingredients class variable
  def get_all_ingredients():
    return Recipe.all_ingredients

  # method to calculate the difficulty of a recipe
  def calculate_difficulty(self, cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
      self.difficulty = 'Easy'
    if cooking_time < 10 and len(ingredients) >= 4:
      self.difficulty = 'Medium'
    if cooking_time >= 10 and len(ingredients) < 4:
      self.difficulty = 'Intermediate'
    if cooking_time >= 10 and len(ingredients) >= 4:
      self.difficulty = 'Hard'

  # getter method for difficulty, invokes a difficulty calculation if no difficulty set
  def get_difficulty(self):
    if (self.difficulty == 'Easy' or self.difficulty == 'Medium' 
      or self.difficulty == 'Intermediate' or self.difficulty =='Hard'):
      return self.difficulty
    else:
      self.calculate_difficulty(self.cooking_time, self.ingredients)
      return self.difficulty

  # method to search for an ingredient in a recipe object   
  def search_ingredient(self, ingredient):
    if ingredient in self.ingredients:
      return True
    else:
      return False

  # method to update the all_ingredients class variable, invoked by add_ingredients()  
  def update_all_ingredients(self):
    for ingredient in self.ingredients:
      if ingredient not in Recipe.all_ingredients:
        Recipe.all_ingredients.append(ingredient)

  # string representation of a recipe object  
  def __str__(self):
    output = "\n" + self.name + \
      "\n--------------------------" + \
      "\nCooking time: " + str(self.cooking_time) + " minutes" + \
      "\nIngredients:\n" + str(self.ingredients) + \
      "\nDifficulty level: " + str(self.difficulty)
    return output

  # method to search for recipes that have a specified ingredient and print the matching recipes  
  def recipe_search(data, search_term):
    for recipe in data:
      if recipe.search_ingredient(search_term):
        print(recipe)

recipes_list = []

# defining a tea object and adding to recipes_list
tea = Recipe("Tea")
tea.add_ingredients("Tea leaves", "Sugar", "Water")
tea.set_cooking_time(5)
tea.get_difficulty()
recipes_list.append(tea)

# defining a coffee object and adding to recipes_list
coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee powder", "Sugar", "Water")
coffee.set_cooking_time(5)
coffee.get_difficulty()
recipes_list.append(coffee)

# defining a cake object and adding to recipes_list
cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla essence",
  "Flour", "Baking powder", "Milk")
cake.set_cooking_time(50)
cake.get_difficulty()
recipes_list.append(cake)

# defining a banana smoothie object and adding to recipes_list
banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut butter", "Sugar", "Ice cubes")
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()
recipes_list.append(banana_smoothie)

# prints each recipe in the recipes_list
print("\nRecipes List")
for recipe in recipes_list:
  print(recipe)

# prints all recipes that use the ingredients specified in search_ingredients
search_ingredients = ["Water", "Sugar", "Bananas"]
print("\n\nLet's search for recipes now!")
for ingredient in search_ingredients:
  print("\n\nHere are the recipe(s) that contain", ingredient + ":")
  Recipe.recipe_search(recipes_list, ingredient)

# prints the all_ingredients list, sorted alphabetically
print("\n\nList of all ingredients:")
print("------------------------")
ingredients_list = Recipe.get_all_ingredients()
ingredients_list.sort()
for ingredient in ingredients_list:
  print(ingredient)
  







    
  