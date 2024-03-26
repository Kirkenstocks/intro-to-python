# Exercise 1.2

## Exercise Goals
- Explain variables and data types in Python
- Summarize the use of objects in Python
- Create a data structure for my Recipe app

## Exercise Deliverables
- Screenshots showing the completion of a nested data struture for 5 recipes
- Learning journal entry for this exercise
- This README.md

## Question 1 Rationale
I would structure recipe_1 (and all subsequent recipes) as a dictionary. The data to be stored in the recipe is given as key-value pairs, and dictionaries naturally store data as key-value pairs, therefore structuring it as a dictionary makes intuitive sense. It also allows for data manipulation via the built-in methods provided by Python for use on dictionaries.

## Question 3 Rationale
The instructions specify that the outer structure, all_recipes, should be sequential in nature and allow multiple recipes to be stored and modified. It doesn't need to be structured in key-value pairs (so a dictionary isn't needed) and the inner data needs to be mutable (so a tuple won't work), therfore I structured all_recipes as a list. This will allow the storage of multiple recipes of any data type, and allow me to mutate the data as needed.