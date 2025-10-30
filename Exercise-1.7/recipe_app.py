# Importing packages
from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker

# Creating the engine object
engine = create_engine('mysql://cf-python:password@localhost/task_database')

# Creating the base object
Base = declarative_base()

# Creating the session object so changes can be made to the database
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
  __tablename__ = "final_recipes"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  # Method that shows a quick representation of the recipe
  def __repr__(self):
    return f"<Recipe ID: {self.id} - Name: {self.name} - Difficulty: {self.difficulty}>"

  # Method that prints a well-formatted version of the recipe
  def __str__(self):
    return (
      f"Recipe List: \n"
      f"ID: {self.id}\n"
      f"Name: {self.name}\n"
      f"Ingredients: {self.ingredients}\n"
      f"Cooking Time: {self.cooking_time} Minutes\n"
      f"Difficulty: {self.difficulty}\n"
    )
  
  def calculate_difficulty(self):
    num_ingredients = len(self.return_ingredients_as_list())
    if self.cooking_time < 10 and num_ingredients < 4:
      self.difficulty = "Easy"
    elif self.cooking_time < 10 and num_ingredients >= 4:
      self.difficulty = "Medium"
    elif self.cooking_time >= 10 and num_ingredients < 4:
      self.difficulty = "Intermediate"
    else:
      self.difficulty = "Hard"

  def return_ingredients_as_list(self):
    if not self.ingredients:
      return []
    return [ingredient.strip() for ingredient in self.ingredients.split(",") if ingredient.strip()]
    
Base.metadata.create_all(engine)

# Function 1: create_recipe()
def create_recipe():
  # Collecting input from the user for the name of the recipe and validating said input
  while True:
    name = input("What is the name of this recipe (maximum of 50 characters): ").strip()
    if len(name) == 0:
      print("You must enter a name for this recipe, please try again")
    elif len(name) > 50:
      print("The name you have inputted exceeds 50 characters, please try again")
    elif not name.replace(" ", "").isalnum():
      print("The the name you have inputted does not contain valid characters, please try again only using alphanumeric characters")
    else:
      break

  # Collecting input from the user for the cooking time and validating that it is a number
  while True:
    cooking_time = input("What is the cooking time in minutes: ").strip()
    if not cooking_time.isnumeric():
      print("The cooking time must be a number, please try again")
    else:
      cooking_time = int(cooking_time)
      break

  # Initial empty list of ingredients
  ingredients = []
  while True:
    ingredients = input("Enter a list of ingredients that are seperated by a comma: ").strip()
    if not ingredients:
      print("You must enter atleast one ingredient, please try again")
    else:
      ingredients = ", ".join([i.strip() for i in ingredients.split(",")])
      break

  # Recipe Object
  recipe_entry = Recipe(
    name=name,
    ingredients=ingredients,
    cooking_time=cooking_time
  )

  # Calculating difficulty of recipe
  recipe_entry.calculate_difficulty()

  # Adding recipe to DB and commiting it
  session.add(recipe_entry)
  session.commit()

  # Notifying the user that the recipe was successfully added to the DB
  print("The recipe was successfully added to the database")

# Function 2: view_all_recipes()
def view_all_recipes():
  # Querying for recipe
  recipes = session.query(Recipe).all()

  # If there are no recipes notify to user
  if not recipes:
    print("There were no recipes found.")

  # Else print recipes
  else:
    for recipe in recipes:
      print(recipe)

# Function 3: search_by_ingredients()
def search_by_ingredients():
  # Query if there are any recipes available in the database
  if session.query(Recipe).count() == 0:
    print("There are no recipes available")
    return None

  # Query only for the recipe ingredients
  results = session.query(Recipe.ingredients).all()

  # Initial empty list of all ingredients
  all_ingredients = set() 

  for row in results:
    ingredients_str = row[0]
    ingredients_list = [ingredient.strip() for ingredient in ingredients_str.split(", ")]
    all_ingredients.update(ingredients_list)

  all_ingredients = list(all_ingredients) 

  # Display a list of ingredients to the user
  print("Ingredients List: ")
  for index, ingredient in enumerate(all_ingredients, 1):
    print(index, ":", ingredient.strip())

  # Ask user for selection
  user_input = input("Enter which ingredients you wish to search for by their numbers and seperate them with spaces: ").strip()

  # Validate user input
  if not user_input:
    print("Please enter a which ingredients you wish to search for by their numbers")
    return None

  try:
    user_numbers = [int(num) for num in user_input.split()]
  except ValueError:
    print("Invalid input. Please enter numbers only.")
    return None
  
  if any(num < 1 or num > len(all_ingredients) for num in user_numbers):
    print("Input numbers are out of range.")
    return None

  search_ingredients = [all_ingredients[num - 1] for num in user_numbers]

  condition = []
  for ing in search_ingredients:
    like_term = f"%{ing}%"
    condition.append(Recipe.ingredients.like(like_term))

  # Query database 
  recipes = session.query(Recipe).filter(or_(*condition)).all()

  # Display results to the user
  if recipes:
    print("Recipes that match your selected ingredients:\n")
    for r in recipes:
      print(r)
  else:
    print("There are no recipes that match the ingredients you selected.")


# Function 4: edit_recipe()
def edit_recipe():
  if session.query(Recipe).count() == 0:
    print("There were no recipes found in the database.")
    return

  # Query for all recipes by their name and ID and then display them to the user
  recipes = session.query(Recipe.id, Recipe.name).all()
  print("Recipe List:")
  for recipe in recipes:
    print(f"ID: {recipe.id} - Name: {recipe.name}")

  # Prompt user to select recipe by ID
  try:
    choice_id = int(input("Select an the recipe you wish to update by its ID: "))
  except ValueError:
    print("Please choose a valid option using its corresponding ID.")
    return

  recipe_ids = [r.id for r in recipes]
  if choice_id not in recipe_ids:
    print("Please choose a valid option using its corresponding ID.")
    return

  # Query the database for the selected recipe by the inputted ID
  recipe = session.query(Recipe).filter_by(id=choice_id).one()

  # Display to the user the details of the recipe
  print("Please choose what you would like to update about this recipe: ")
  print(f"\n1. Name: {recipe.name}")
  print(f"\n2. Ingredients: {recipe.ingredients}")
  print(f"\n3. Cooking Time: {recipe.cooking_time} minutes")

  # Ask user which detail they wish to update
  detail_choice = input("Please enter the number corresponding to the detail you wish to update: ")

  if detail_choice == "1":
    new_name = input("Enter new recipe name:  ").strip()
    if len(new_name) > 50:
      print("Name must not be longer than 50 characters, please try again")
      return None
    elif not all(char.isalnum() or char.isspace() for char in new_name):
      print("You must only enter letters, numbers, or spaces, please try again")
      return None
    recipe.name = new_name

  elif detail_choice == "2":
    try:
      num_ingredients = int(input("Enter numerically how many ingredients the recipe has: "))
    except ValueError:
      print("Please enter a valid number")
      return

    new_ingredients = []
    for i in range(num_ingredients):
      ingredient = input(f"Enter new ingredient:  {i+1}: ").strip()
      new_ingredients.append(ingredient)
        
    recipe.ingredients = ", ".join(new_ingredients)

  elif detail_choice == "3":
    new_time = input("Enter new cooking time (minutes): ").strip()
    if not new_time.isdigit():
      print("Error: Cooking time must be a number.")
      return
    recipe.cooking_time = int(new_time)

  else:
    print("Invalid choice, please enter a valid number")
    return

  # Recalculating difficulty
  recipe.difficulty = recipe.calculate_difficulty()

  # Committing and notifying the user of the successful update
  session.commit()
  print("Recipe updated successfully!")



# Function 5: delete_recipe()
def delete_recipe():
  # First check that there are recipes in the database
  recipes = session.query(Recipe).all()
  if not recipes:
    print("There were no recipes found in the database.")
    return None

  # Then fetch and display recipes
  recipes = session.query(Recipe.id, Recipe.name).all()
  print("Recipes:")
  for recipe in recipes:
    print(f"ID: {recipe.id}\nName: {recipe.name}")

  # Next ask the user for the ID of the recipe they would like to delete
  try:
    choice_id = int(input("Enter the ID of the recipe you wish to delete: "))
  except ValueError:
    print("Please choose a valid option using its corresponding ID.")
    return


  # Here we are verifying that a recipe with chosen ID exists
  recipe_ids = [r.id for r in recipes]
  if choice_id not in recipe_ids:
    print("Please choose a valid option using its corresponding ID.")
    return

  # Grabbing the recipe by the users chosen ID
  recipe = session.query(Recipe).filter_by(id=choice_id).one()

  # We then confirm that the user would like to proceed with the deletion
  confirmation = input(f"Type yes if you are sure you would like to delete '{recipe.name}' ").strip().lower()

  if confirmation == "yes":
    session.delete(recipe)
    session.commit()
    print(f"The recipe has been deleted successfully.")
  else:
    print("The deletion has been cancelled")

# Main menu function
def main_menu():
  choice = ''
  while (choice != 'quit'):
    print('Main Menu')
    print("", 25*"-")
    print("Options:\n")
    print("1. Create a new recipe\n")
    print("2. View all recipes\n")
    print("3. Search for a recipe by ingredient\n")
    print("4. Update an existing recipe\n")
    print("5. Delete a recipe\n")
    print("Type 'quit' to exit the program.\n")
    choice = input("Please enter the number corresponding to the option you wish to select: ")

    # List of choices for the user
    if choice == "1":
      create_recipe()
    elif choice == "2":
      view_all_recipes()
    elif choice == "3":
      search_by_ingredients()
    elif choice == "4":
      edit_recipe()
    elif choice == "5":
      delete_recipe()
    elif choice != "quit":  
      print("\nPlease pick one of those options!")
    elif choice == "quit":
      session.close()

  # Ensures that the session and engine are properly closed
  session.close()
  engine.dispose()

# Calls and starts the main menu  
main_menu()