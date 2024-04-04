import pickle

# displays a selected recipe
def display_recipe(recipe):
  print("\nRecipe with the selected ingredient")
  print("----------------------------------------")
  print("Name: " + recipe['name'])
  print("Cooking time in minutes: " + str(recipe['cooking_time']))
  print("Ingredients: " + str(recipe['ingredients']))
  print("Difficulty: " + recipe['difficulty'])

# allows user to search for ingredients
def search_ingredient(data):
  ingredients = list(enumerate(data['all_ingredients'], 1))
  print("\nAll ingredients:")
  print("----------------")
  for ingredient in ingredients:
    print(str(ingredient[0]) + ". " + ingredient[1])
  
  try:
    index = int(input("\nChoose an ingredient by number: ")) - 1
    ingredient_searched = ingredients[index]
  except ValueError: 
    print("Invalid input. Select a valid number.")
  except IndexError:
    print("No matching ingredient number. Pick a listed ingredient.")
  except:
    print("An unknown error occurred. Maybe try again?")
  else:
    for recipe in data['recipes_list']:
      if ingredient_searched[1] in recipe['ingredients']:
        display_recipe(recipe)

# beginning of script execution
filename = input("Enter the name of the file that holds the recipe data: ")

# opens the user specified file
try:
  with open(filename, 'rb') as file:
    data = pickle.load(file)
except FileNotFoundError:
  print("File not found. Check for typos and try again")
except:
  print("Unforeseen error. Maybe try again?")
else:
  search_ingredient(data)

