recipes_list = []
ingredients_list = []

def take_recipe():
  name = input("Enter the name of your recipe: ")
  cooking_time = int(input("Enter the cooking time in minutes: "))
  ingredients = input("Enter ingredients (separated by a comma): ").split(", ")
  recipe = {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients
  }
  return recipe

n = int(input("How many recipes would you like to submit? "))

for i in range(0, n):
  recipe = take_recipe()

  for ingredient in recipe['ingredients']:
    if not ingredient in ingredients_list:
      ingredients_list.append(ingredient)
  
  recipes_list.append(recipe)

for recipe in recipes_list:
  if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
    difficulty = "Easy"

  elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
    difficulty = 'Medium'

  elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
    difficulty = 'Intermediate'

  elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
    difficulty = 'Hard'
  
  print("Recipe:", recipe['name'])
  print("Cooking Time (min):", recipe['cooking_time'])
  print("Ingredients:")
  for ingredient in recipe['ingredients']:
    print(ingredient.capitalize())
  print("Difficulty Level:", difficulty) 

ingredients_list.sort()

print("Ingredients Available Across All Recipes")
print("----------------------------------------")
for ingredient in ingredients_list:
  print(ingredient.capitalize())