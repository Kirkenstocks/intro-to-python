class ShoppingList(object):
  def __init__(self, list_name):
    self.list_name = list_name
    shopping_list = []
    self.shopping_list = shopping_list
  
  def add_item(self, item):
    if not item in self.shopping_list:
      self.shopping_list.append(item)
      print(f"{item} added to shopping list")
    else: 
      print(f"{item} is already in shopping list")
  
  def remove_item(self, item):
    if item in self.shopping_list:
      self.shopping_list.remove(item)
      print(f"{item} removed from shopping list")
    else:
      print(f"{item} not found in shopping list")

  def view_list(self):
    print(self.list_name)
    print("-------------------------")
    for item in self.shopping_list:
      print(f"- {item}")
  
pet_store_list = ShoppingList("Pet Store Shopping List")

pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

pet_store_list.remove_item("flea collars")

pet_store_list.add_item("frisbee")

pet_store_list.view_list()

  
  