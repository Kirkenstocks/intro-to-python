import pickle

recipes_list = []
all_ingredients = []

# prompts the user to input a recipe and returns recipe as a dictionary
def take_recipe(recipe_num):
  name = input("Enter the name of the recipe: ")
  cooking_time = int(input("Enter the cooking time in minutes: "))
  ingredients = input("Enter the ingredients needed (separated by a comma): ").split(", ")

  difficulty = calc_difficulty(cooking_time, len(ingredients))

  recipe = {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients,
    'difficulty': difficulty
  }
  return recipe

# calculates the recipe difficulty based on cooking time and number of ingredients
def calc_difficulty(cooking_time, num_ingredients):
  if cooking_time < 10 and num_ingredients < 4:
    difficulty = 'Easy'
  elif cooking_time < 10 and num_ingredients >= 4:
    difficulty = 'Medium'
  elif cooking_time >= 10 and num_ingredients < 4:
    difficulty = 'Intermediate'
  elif cooking_time >=10 and num_ingredients >= 4:
    difficulty = 'Hard'
  return difficulty

# loads recipe and ingredient data from a user specified file and saves it to variables
filename = input("Enter the desired filename: ")
try: 
  with open(filename, 'rb') as requested_file:
    data = pickle.load(requested_file)
except FileNotFoundError: 
  data = {
    'recipes_list': [],
    'all_ingredients': []
  }
except:
  print("An unexpected error occurred, please try again")
  data = {
    'recipes_list': [],
    'all_ingredients': []
  }
else: 
  requested_file.close()
finally:
  recipes_list = data['recipes_list']
  all_ingredients = data['all_ingredients']

# ask user how many recipes they want to enter and call take_recipe() for each one
num_recipes = int(input("How many recipes do you want to enter? "))
for i in range(0, num_recipes):
  recipe = take_recipe(i)
  recipes_list.append(recipe)
# add ingredients to all_ingredients if not already there
  for ingredient in recipe['ingredients']:
    if not ingredient in all_ingredients:
      all_ingredients.append(ingredient)

#prepare recipes_list and all_ingredients to be stored in a file
data = {
  'recipes_list': recipes_list,
  'all_ingredients': all_ingredients
}

# add data to a binary file
with open(filename, 'wb') as file:
  pickle.dump(data, file)

print("\n Recipes saved!")


