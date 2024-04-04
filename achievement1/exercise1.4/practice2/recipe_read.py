import pickle

with open('recipe_binary.bin', 'rb') as my_file:
  tea_recipe = pickle.load(my_file)

ingredients_string = ", ".join(tea_recipe['ingredients'])

print("Recipe for " + tea_recipe['name'])
print("Ingredients: " + ingredients_string)
print("Cooking time: " + str(tea_recipe['cooking time (mins)']) + " minutes")
print("Difficulty: " + tea_recipe['difficulty'])

my_file.close()