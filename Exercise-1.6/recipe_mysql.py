import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    password='password')

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
cursor.execute("""
  CREATE TABLE IF NOT EXISTS Recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
  )
""")


def create_recipe(conn, cursor):
  name = str(input("What is the name of this recipe: "))
  cooking_time =  int(input("What is the cooking time in minutes: "))
  ingredients_input = input("Enter a list of ingredients that are seperated by a comma: ").strip()
  ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",") if ingredient.strip()]
  difficulty = calculate_difficulty(cooking_time, ingredients)

  cursor.execute("""
    INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
    VALUES (%s, %s, %s, %s)
  """, (name, ", ".join(ingredients), cooking_time, difficulty))  
  conn.commit()
  print("The recipe was successfully added to the database")

def calculate_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    difficulty = "Easy"
  elif cooking_time < 10 and len(ingredients) >= 4:
    difficulty = "Medium"
  elif cooking_time >= 10 and len(ingredients) < 4:
    difficulty = "Intermediate"
  else:
    difficulty = "Hard"  
  return difficulty

def search_recipe(conn, cursor):
  cursor.execute("SELECT ingredients FROM Recipes")
  results = cursor.fetchall()

  all_ingredients = set()

  for row in results:
    recipe_ingredients = [i.strip().lower() for i in row[0].split(',')]
    all_ingredients.update(recipe_ingredients)
  
  all_ingredients = list(all_ingredients)
  all_ingredients.sort()

  print("List of all ingredients: ")
  for i, ingredient in enumerate(all_ingredients, start=1):
    print(f"{i}. {ingredient}")

  while True:
    try:
      index = int(input("Select an ingredient by its number: "))
    except ValueError:
      print("Please choose a valid option using its corresponding number.")
    else:
      ingredient_choice = all_ingredients[index - 1]
      print(f"The ingredient you selected was: {ingredient_choice}")
      break 
  
  query = "SELECT * FROM Recipes WHERE ingredients LIKE %s" 
  cursor.execute(query, (f"%{ingredient_choice}%",))
  results = cursor.fetchall()
  if results:
    print(f"Here is a list of recipes with {ingredient_choice}: ")
    for recipe in results:  
      print(f"ID: {recipe[0]}, Recipe: {recipe[1]}, Ingredients: {recipe[2]}, Cooking Time: {recipe[3]} minutes, Difficulty: {recipe[4]}")
      found = True
  if not found:
      print(f"There were no recipes found that contained the ingredient: '{ingredient_choice}'.")

def update_recipe(conn, cursor):
  cursor.execute("SELECT * FROM Recipes")
  results = cursor.fetchall()

  for recipe in results:
    print("Recipe List: \n")
    print(f"ID: {recipe[0]}")
    print(f"Name: {recipe[1]}")
    print(f"Ingredients: {recipe[2]}")
    print(f"Cooking Time: {recipe[3]} minutes")
    print(f"Difficulty: {recipe[4]}\n")
  
  choice_id = input("Select an the recipe you wish to update by its ID: ")
  if not choice_id:
    print("Please choose a valid option using its corresponding ID.")
    return
  print("Please choose what you would like to update about this recipe: ")
  print("1. Name" \
        "\n2. Ingredients" \
        "\n3. Cooking Time")
  choice = input("Please enter the number corresponding to the thing you wish to update: ")

  if choice == "1":
    new_name = input("Enter new recipe name: ")
    cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, choice_id))
  elif choice == "2":
    new_ingredients = input("Enter new ingredients (comma separated): ")
    cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_ingredients, choice_id))
  elif choice == "3":
    new_time = int(input("Enter new cooking time (minutes): "))
    cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_time, choice_id))
  else:
    print("Invalid choice.")
    return

  conn.commit()
  print("The recipe has been updated successfully.")

def delete_recipe(conn, cursor):
  cursor.execute("SELECT * FROM Recipes")
  results = cursor.fetchall()

  for recipe in results:
    print("Recipe List: \n")
    print(f"ID: {recipe[0]}")
    print(f"Name: {recipe[1]}")
    print(f"Ingredients: {recipe[2]}")
    print(f"Cooking Time: {recipe[3]} minutes")
    print(f"Difficulty: {recipe[4]}\n")

  choice_id = input("Enter the ID of the recipe you wish to delete: ")
  cursor.execute("DELETE FROM Recipes WHERE id = %s", (choice_id,))
  conn.commit()
  print("The recipe has been deleted successfully.")

def main_menu(conn, cursor):
  choice = ''
  while (choice != 'quit'):
    print('Main Menu')
    print("", 20*"-")
    print("Options:\n")
    print("1. Create a new recipe\n")
    print("2. Search for a recipe by ingredient\n")
    print("3. Update an existing recipe\n")
    print("4. Delete a recipe\n")
    print("Type 'quit' to exit the program.\n")
    choice = input("Please enter the number corresponding to the option you wish to select: ")

    if choice == "1":
        create_recipe(conn, cursor)
    elif choice == "2":
        search_recipe(conn, cursor)
    elif choice == "3":
        update_recipe(conn, cursor)
    elif choice == "4":
        delete_recipe(conn, cursor)
    elif choice == "quit":
        conn.commit()
        conn.close()
        print("The recipe has been saved successfully.")

main_menu(conn, cursor)
cursor.close()
conn.close()