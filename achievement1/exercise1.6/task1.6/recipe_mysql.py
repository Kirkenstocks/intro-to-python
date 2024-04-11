# setup MySQL connection to this script
import mysql.connector
conn = mysql.connector.connect(
  host='localhost',
  user='cf-python',
  passwd='password'
)
cursor = conn.cursor()

# setup the database and Recipes table
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database;")
cursor.execute("USE task_database;")
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  ingredients VARCHAR(255),
  cooking_time INT,
  difficulty VARCHAR(20)                                       
);''')

# main menu for the user to navigate
def main_menu(conn, cursor):
  choice = ""
  print("\nWelcome to the Recipe App!\n")
  print("Main Menu")
  print(20*"=" + "\n")
  
  # define options for the user to select from
  while (choice != 'exit'):
    print("Type the number of the option you want:\n")
    print("     1. Create a new recipe")
    print("     2. Search for a recipe by ingredient")
    print("     3. Update an existing recipe")
    print("     4. Delete a recipe \n")
    print("Type 'exit' to close the program\n")
    choice = input("Your choice: ")

    if choice == '1':
      create_recipe(conn, cursor)
    elif choice == '2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      cursor.execute("SELECT COUNT(*) FROM Recipes;")
      recipe_count = cursor.fetchone()
      if recipe_count[0] == 0:
        print("\nThere are no recipes in the database to delete.\n")
      else:
        delete_recipe(conn, cursor)
    elif choice == 'exit':
      print("Thank you for using the recipe app!\n")
      break
    else:
      print("Invalid input. Type a number 1-4 corresponding to your choice, or 'exit' to close the program.")
      print("Restarting app...")
      print(20*"-")
      main_menu(conn, cursor)
  
  conn.close()
  
# creates a recipe and stores in database
def create_recipe(conn, cursor):
  print("\n" + 20*"-")
  print("Create a new recipe!\n")

  name = input("Enter the recipe name: ").capitalize().strip()
  ingredient_input = input("Enter ingredients, separated by a comma: ").split(",")
  ingredient_input = [ingredient.strip().lower() for ingredient in ingredient_input]
  ingredients = ", ".join(ingredient_input)

  while True:
    try:
      cooking_time = int(input("Enter the cooking time in minutes: "))
      break
    except ValueError:
      print("Invalid input. Try again, entering an integer this time.")

  difficulty = calculate_difficulty(cooking_time, ingredient_input)

  # SQL query adding recipe to database
  sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s);'
  val = (name, ingredients, cooking_time, difficulty)
  cursor.execute(sql, val)

  print("\nRecipe added successfully!\n")

  conn.commit()


  
  
# searches for recipes by ingredient
def search_recipe(conn, cursor):
  all_ingredients = []
  cursor.execute("SELECT ingredients FROM Recipes;")
  ingredients = cursor.fetchall()

  if not ingredients:
    print("\nNo recipes found. Create a recipe then try again.\n")
    return
  
  # takes each row of ingredients as string, splits into a list, and adds each ingredient to all_ingredients
  for ingredient in ingredients:
    ingredient_list = ingredient[0].split(", ")
    for item in ingredient_list:
      item = str(item).capitalize()
      if not item in all_ingredients:
        all_ingredients.append(item)
  
  # prints list of all ingredients and stores the user selected ingredient
  print("\nAll Ingredients")
  print(20*"-")

  all_ingredients.sort()
  ingredient_number = 1
  for ingredient in all_ingredients:
    print(str(ingredient_number) + ". " + ingredient)
    ingredient_number += 1

  while True:
    try:
      search_index = int(input("Choose an ingredient by number: ")) - 1
      search_ingredient = all_ingredients[search_index]
      break
    except ValueError:
      print("\nInvalid input. Try again, entering an integer this time.\n")
    except IndexError:
      print("\nInvalid input. Choose one of the listed ingredients by number.\n")
  
  # SQL query to return recipes with the searched ingredient
  cursor.execute('SELECT * FROM Recipes WHERE ingredients LIKE %s', ('%' + search_ingredient+ '%',))
  search_results = cursor.fetchall()
  
  print("\nHere are all the recipes with your selected ingredient:")
  for row in search_results:
    print("\nRecipe for " + row[1])
    print(20*"-")
    print("Ingredients: " + row[2])
    print("Cooking time in minutes: " + str(row[3]))
    print("Difficulty: " + row[4])
    print(20*"-" + "\n")

# updates a recipe's data
def update_recipe(conn, cursor):
  view_all_recipes()
  
  # updates the difficulty of a recipe after ingredients or cooking time is changed
  def update_difficulty(update_id):
    cursor.execute("SELECT * FROM Recipes WHERE id = %s;", (update_id,))
    recipe_data = cursor.fetchall()

    cooking_time = recipe_data[0][3]
    ingredients = recipe_data[0][2].split(", ")

    updated_difficulty = calculate_difficulty(cooking_time, ingredients)
    cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s;", (updated_difficulty, update_id))

  # displays the updated recipe after update is complete
  def display_updated_recipe(update_id):
    print("\nUpdated recipe:")
    cursor.execute("SELECT * FROM Recipes WHERE id = %s;", (update_id,))
    recipe = cursor.fetchall()
    for row in recipe:
      print("\nRecipe for " + row[1])
      print("----------------------------")
      print("Ingredients: " + row[2])
      print("Cooking time in minutes: " + str(row[3]))
      print("Difficulty: " + row[4])
      print("Recipe ID: " + str(row[0]) + "\n")

  # user selects a recipe by ID and specifies the column to change
  while True:
    try:
      update_id = int(input("\nEnter the ID of the recipe you want to modify: "))
      cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (update_id,))
      result = cursor.fetchone()
      if result[0] >= 1:
        break
      else:
        print("\nRecipe not found. Select a recipe from the list above and try again.")
    except ValueError:
      print("\nInvalid input. Try again, entering an integer this time.")

  update_column = (input("You can modify the recipe's name, ingredients, or cooking time. \nEnter your choice: ")).lower().strip()
  
  # updates the recipe name
  if update_column == 'name':
    update_name = input("Enter the new name for the recipe: ").capitalize().strip()
    cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (update_name, update_id))
    print("\nRecipe name updated successfully!")
    display_updated_recipe(update_id)
  
  # updates the recipe ingredients
  elif update_column == 'ingredients':
    update_ingredients = input("Enter the updated list of ingredients, separated by commas: ")
    update_ingredients = update_ingredients.split(",")
    update_ingredients = [ingredient.strip().lower() for ingredient in update_ingredients]
    update_ingredients = ", ".join(update_ingredients)

    cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s;", (update_ingredients, update_id))
    print("\nIngredients updated successfully!")

    update_difficulty(update_id)
    print("\nRecipe difficulty updated too!")

    display_updated_recipe(update_id)

  # updates the cooking time of the recipe
  elif update_column == 'cooking time':
    update_column = 'cooking_time'
    while True:
      try:
        update_time = int(input("Enter the updated cooking time: "))
        break
      except ValueError:
        print("\nInvalid input. Try again, entering an integer this time.")
      
    cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s;", (update_time, update_id))
    print("\nCooking time updated successfully!")

    update_difficulty(update_id)
    print("\nRecipe difficulty updated too!")

    display_updated_recipe(update_id)

  else:
    print("Enter a valid option. Type 'name', 'cooking time', or 'ingredients'.")
  
  conn.commit()

# deletes a recipe
def delete_recipe(conn, cursor):
  view_all_recipes()

  while True:
    try:
      delete_id = int(input("\nEnter the ID of the recipe you want to delete: "))
      cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (delete_id,))
      result = cursor.fetchone()
      if result[0] >= 1:
        break
      else:
        print("\nRecipe not found. Select a recipe from the list above and try again.")
    except ValueError:
      print("\nInvalid input. Try again, entering an integer this time.")

  cursor.execute('DELETE FROM Recipes WHERE id = %s', (delete_id,))
  conn.commit()

  print("\nRecipe deleted successfully!\n")

# sets difficulty based on cooking time and ingredients
def calculate_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    difficulty = 'Easy'
  elif cooking_time < 10 and len(ingredients) >= 4:
    difficulty = 'Medium'
  elif cooking_time >= 10 and len(ingredients) < 4:
    difficulty = 'Intermediate'
  else:
    difficulty = 'Hard'

  return difficulty

# displays all recipes to the user
def view_all_recipes():
  cursor.execute("SELECT * FROM Recipes;")
  recipes = cursor.fetchall()
  for recipe in recipes:
    print("\nRecipe for " + recipe[1])
    print(20*"-")
    print("Ingredients: " + recipe[2])
    print("Cooking time in minutes: " + str(recipe[3]))
    print("Difficulty: " + recipe[4])
    print("Recipe ID: " + str(recipe[0]))
    print(20*"-" + "\n")
  return recipes

main_menu(conn, cursor)