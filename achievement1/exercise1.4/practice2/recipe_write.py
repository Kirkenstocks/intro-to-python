import pickle

tea_recipe = {
  'name': 'Tea',
  'ingredients': ['Tea leaves', 'Water', 'Sugar'],
  'cooking time (mins)': 5,
  'difficulty': 'Easy'
}

my_file = open('recipe_binary.bin', 'wb')
pickle.dump(tea_recipe, my_file)
my_file.close()