# database setup and connection to script
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import Integer, String
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine("mysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# defining the Recipe class that structures each entry to the database
class Recipe(Base):
  __tablename__ = 'final_recipes'

  # defining columns for the recipe entry
  id = Column(Integer, primary_key = True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))
    
  # brief description of the recipe
  def __repr__(self):
    return "<Recipe ID: " + str(self.id) + " - Name: " + self.name + " - Difficulty: " + self.difficulty + ">"
  
  # full description of the recipe
  def __str__(self):
    print("\nRecipe for " + self.name)
    print("-"* 30)

    print("Ingredients:")
    recipe_ingredients = Recipe.return_ingredients_as_list(self.ingredients)
    for ingredient in recipe_ingredients:
      print("  " + ingredient)

    print("Cooking time in minutes: " + str(self.cooking_time))
    print("Difficulty level: " + self.difficulty)
    print("ID: " + str(self.id))
    print("-" * 30 + "\n")

  # method to calculate the difficulty of a recipe
  def calculate_difficulty(cooking_time, ingredients):
    ingredient_list = Recipe.return_ingredients_as_list(ingredients)

    if cooking_time < 10 and len(ingredient_list) < 4:
      difficulty = 'Easy'
    if cooking_time < 10 and len(ingredient_list) >= 4:
      difficulty = 'Medium'
    if cooking_time >= 10 and len(ingredient_list) < 4:
      difficulty = 'Intermediate'
    if cooking_time >= 10 and len(ingredient_list) >= 4:
      difficulty = 'Hard'
    
    return difficulty

  # split the ingredients string into a list
  def return_ingredients_as_list(ingredients): 
    if not ingredients:
      return []
    else:
      return ingredients.split(", ")


# create table based on defined schema
Base.metadata.create_all(engine)


# create a recipe from user input
def create_recipe():
  # user enters a name, 50 character limit checked
  while True:
    name = input("Enter the recipe name: ").title().strip()
    if 0 < len(name) <= 50:
      break
    else:
      print("\nEnter a valid recipe name between 1-50 characters")

  # calls the ingredient entry function
  ingredients = ingredient_entry()

  if not ingredients:
    print("\nNo ingredients saved. Please try again.")
    return

  # user enters cooking time, type checked for integer
  while True:
    try:
      cooking_time = int(input("Enter the cooking time in minutes: "))
      if cooking_time > 0:
        break
    except ValueError:
      print("\nEnter a valid cooking time, must be an integer greater than 0")

  difficulty = Recipe.calculate_difficulty(cooking_time, ingredients)

  # recipe data is collected into an object and added to the database
  recipe_entry = Recipe(name = name, ingredients = ingredients, cooking_time = cooking_time, difficulty = difficulty)
  try:
    session.add(recipe_entry)
    session.commit()
    print("\n*** Recipe created successfully! ***")
    print("---------------------------------")
  except SQLAlchemyError as err:
    print(f"\nAn error occurred while adding the recipe to the database: {err}")

  pause()


# retrieves and displays all recipes to the user
def view_all_recipes():
  try:
    recipes_list = session.query(Recipe).all()
  except SQLAlchemyError as err:
    print(f"\nAn error occurred while retrieving recipes from the database: {err}")

  # check if there are any recipes already
  if not recipes_list:
    print("\nNo recipes found in the database")
    return None

  print("All Recipes")
  print("=" * 30)
  # prints the string representation of each recipe
  for recipe in recipes_list:
    Recipe.__str__(recipe)

  pause()


# allows user to search for recipes by a given ingredient
def search_by_ingredients():
  # check if there are any recipes already
  try:
    recipe_count = session.query(Recipe).count()
  except SQLAlchemyError as err:
    print(f"\nAn error occurred while getting a count of all recipes in the database: {err}")
  if not recipe_count:
    print("\nNo recipes found. Enter a recipe before searching for ingredients.")
    return None
  
  # retrieve and store a list of all ingredients
  try:
    results = session.query(Recipe.ingredients).all()
  except SQLAlchemyError as err:
    print(f"\nAn error occurred while retrieving a list of ingredients from all recipes: {err}")
  
  all_ingredients = []
  search_ingredients = []

  # breaks down ingredients from each recipe into a list and adds ingredients to all_ingredients
  for result in results:
    ingredients = result[0].split(", ")
    for item in ingredients:
      if not item in all_ingredients:
        all_ingredients.append(item)

  # sort, capitalize, number, and display all_ingredients
  all_ingredients.sort()
  print("\nAll Ingredients")
  print("-" * 30)
  for count, ingredient in enumerate(all_ingredients, start=1):
    print(f"{count}. {str(ingredient).capitalize()}")

  # ask the user to choose ingredients and verify user input
  while True:
    try:
      search_input = input("\nEnter the number of the ingredient(s) you want to search by.\nIf selecting multiple ingredients, separate them with a space: ").split()
      search_indices = [int(index) for index in search_input]
      if all(0 < index <= len(all_ingredients) for index in search_indices):
        break
      else:
        print("\nInvalid input. Choose one or more number corresponding to the ingredient(s) you want to search with.")
    except ValueError:
      print("\nInvalid input. Please enter one or more of the ingredient numbers.")

  # add the chosen ingredients to search_ingredients
  search_ingredients = [all_ingredients[index - 1] for index in search_indices]

  # initialize conditions list and add matching ingredients to it
  conditions = []
  for search_ingredient in search_ingredients:
    like_term = f"%{search_ingredient}%"
    conditions.append(Recipe.ingredients.like(like_term))

  # retrieve matching recipes and display them
  search_recipes = []
  try:
    search_recipes = session.query(Recipe).filter(*conditions).all()
  except SQLAlchemyError as err:
    print(f"\nAn error ocurred while retrieving recipes that match the search criteria: {err}")
  except Exception as err:
    print(f"\nError: {err}")

  if not search_recipes:
    print("\nNo recipes found with those ingredients.\n")
  else:
    print("\nRecipes that match your search criteria:")

  for recipe in search_recipes:
    Recipe.__str__(recipe)

  pause()


# allows the user to edit an existing recipe
def edit_recipe():
  # displays recipe summaries and stores the chosen recipe in choice
  choice = choose_one_recipe()

  # retrieves the recipe from the database by ID
  try:
    recipe_to_edit = session.query(Recipe).filter(Recipe.id == choice).one()
  except SQLAlchemyError as err:
    print(f"\nAn error occurred while retrieving the recipe you chose: {err}")
    return
  
  # displays the chosen recipe without difficulty level
  print("\nHere's the original recipe:")
  print("-"* 30)
  print("1.  Name: " + recipe_to_edit.name)
  print("2.  Ingredients:")
  ingredients = Recipe.return_ingredients_as_list(recipe_to_edit.ingredients)
  for ingredient in ingredients:
    print("\t"+ ingredient)
  print("3.  Cooking time: " + str(recipe_to_edit.cooking_time))
  print("-" * 30)

  # user chooses an attribute to edit
  attr_to_edit = input("\nEnter the number corresponding to the recipe attribute you want to edit: ").strip()

  # edits the recipe name
  if attr_to_edit == '1':
    while True:
      recipe_to_edit.name = input("\nEnter a new name for the recipe: ").strip().title()
      if 0 < len(recipe_to_edit.name) <= 50:
        break
      else:
        print("\nEnter a valid recipe name between 1-50 characters")

  # edits the ingredients
  elif attr_to_edit == '2':
    recipe_to_edit.ingredients = ingredient_entry()
    if not recipe_to_edit.ingredients:
      print("\nNo ingredients saved. Please try again.")
      return
    recipe_to_edit.difficulty = Recipe.calculate_difficulty(recipe_to_edit.cooking_time, recipe_to_edit.ingredients)
  
  # edits the cooking time
  elif attr_to_edit == '3':
    while True:
      try:
        recipe_to_edit.cooking_time = int(input("Enter the cooking time in minutes: "))
        if recipe_to_edit.cooking_time > 0:
          break
        else:
          print("\nCooking time must be a positive integer.")
      except ValueError:
        print("\nEnter a valid cooking time, must be an integer greater than 0")

      recipe_to_edit.difficulty = Recipe.calculate_difficulty(recipe_to_edit.cooking_time, recipe_to_edit.ingredients)
  else:
    print("\nInvalid entry. Try again and enter 1, 2, or 3.")
  
  # gathers the changes into a dictionary
  updated_recipe = {
      "name": recipe_to_edit.name,
      "ingredients": recipe_to_edit.ingredients,
      "cooking_time": recipe_to_edit.cooking_time,
      "difficulty": recipe_to_edit.difficulty
    }
  # update the recipe in the database
  try:
    session.query(Recipe).filter(Recipe.id == choice).update(updated_recipe)
    session.commit()
    print("\n*** Recipe Updated Successfully! ***")
    print("----------------------------------\n")
  except SQLAlchemyError as err:
    print(f"\nAn error occurred while updating the recipe in the database: {err}")

  pause()


# deletes a recipe from the database
def delete_recipe():
  # displays recipe summaries and stores the chosen recipe in choice
  choice = choose_one_recipe()

  # retrieves the recipe from the database by ID
  try:
    recipe_to_delete = session.query(Recipe).filter(Recipe.id == choice).one()
  except SQLAlchemyError as err:
    print(f"\nAn error occurred while retrieving the recipe you chose: {err}")
    return
  
  # confirm that user wants to delete this recipe
  confirm_delete = input("Are you sure you want to delete this recipe? Enter 'yes' if you're sure: ").strip().lower()
  while True:
    if confirm_delete == 'yes':
      try:
        session.delete(recipe_to_delete)
        session.commit()
        print("\n*** Recipe deleted successfully ***")
        print("---------------------------------")
        break
      except SQLAlchemyError as err:
        print(f"\nAn error occurred while trying to delete the recipe: {err}")
    else:
      print("\nRecipe not deleted")
      return None

# prompts user through entering ingredients  
def ingredient_entry():
  ingredient_list = []
  # asks the user how many ingredients they want to enter
  while True:
    try:
      num_of_ingredients = int(input("\nHow many ingredients would you like to enter: "))
      if num_of_ingredients > 0:
        break
      else:
        print("\nThe number of ingredients must be a positive integer")
    except ValueError:
      print("\nPlease enter an integer greater than 0")

  print()
  # user inputs ingredients one at a time
  for i in range(num_of_ingredients):
    while True:
      try:
        ingredient = input("Enter an ingredient: ").strip().lower()
        if ingredient not in ingredient_list:
          ingredient_list.append(ingredient)
          break
      except:
        print("\nSomething went wrong, please try again.")
  
  ingredients = ", ".join(ingredient_list)
  if len(ingredients) > 255:
    print("Your ingredients list is too long! The maximum number of characters is 255. Please try again.")
    return
  else:
    return ingredients


# retrieves the id and name of all recipes and displays them to the user
def choose_one_recipe():
  # retrieves recipe info from the database
  try:
    recipes = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
  except SQLAlchemyError as err:
    print(f"\nAn error occurred while retrieving recipes: {err}")

  # check if any recipes are returned
  if not recipes:
    print("\nNo recipes found. Please add a recipe and try again.")
    return None
  
  # store the name and id of each recipe into results, then display to user
  results = []
  ids = []
  for recipe in recipes:
    id = int(recipe.id)
    name = recipe.name
    results.append((id, name))
    ids.append(id)
  
  # prints the ID and name of all recipes in the database
  print("\nAll Recipes")
  print("-" * 30)
  for result in results:
    print(f"ID: {result[0]}, Name: {result[1]}")
  
  # user chooses a recipe by ID
  while True:
    try:
      choice = int(input("\nEnter the ID of the recipe you want: "))
      if choice not in ids:
        raise IndexError
      break
    except ValueError:
      print("\nInvalid input. Please enter a number.")
    except IndexError:
      print("\nInvalid ID. Choose one of the listed recipe IDs and try again.")
  
  return choice
  

# requires user input prior to restarting the main menu loop
def pause():
  input("\nPress enter when you are ready to go back to the main menu\n")


# main menu for the user to navigate
def main_menu():
  choice = ""
  print("\n" + 30 * "=" +"\n\nWelcome to the Recipe App!\n")
  
  # define options for the user to select from
  while (choice != 'quit'):
    print("\nType the number of the option you want\n")
    print("\t1. Create a new recipe")
    print("\t2. View all recipes")
    print("\t3. Search for recipes by ingredients")
    print("\t4. Update an existing recipe")
    print("\t5. Delete a recipe \n")
    print("Or type 'quit' to close the program\n")
    choice = input("Your choice: ")

    # calls the appropriate function based on user input
    if choice == '1':
      create_recipe()
    elif choice == '2':
      view_all_recipes()
    elif choice == '3':
      search_by_ingredients()
    elif choice == '4':
      edit_recipe()
    elif choice == '5':
      delete_recipe()
    elif choice == 'quit':
      print("\nThank you for using the recipe app!\n")
      session.close()
      engine.dispose()
      break
    else:
      print("\nInvalid input. Type a number 1-5 corresponding to your choice, or 'quit' to close the program.")
      print(30 * "=" + "\n")

main_menu()