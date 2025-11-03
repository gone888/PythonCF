import pickle

def display_recipe(recipe: dict):
  print("Recipe: " + str(recipe["name"] + "\n"),
        "Cooking time:",recipe["cooking_time"], "\n",
        "Ingredients:"
        )
  for ingredients in recipe["ingredients"]: 
    print(ingredients)
  print(
    "Difficulty level:", recipe["difficulty"]
  )

def search_ingredient(data):
  all_ingredients = data["all_ingredients"]
  for i, ingredient in enumerate(all_ingredients):
    print(f"{i+1}. {ingredient}")

  while True:
    try:
      index = int(input("Select an ingredient by its number: "))
    except ValueError:
      print("Please choose a valid option using its corresponding number.")
    else:
      ingredient_choice = data["all_ingredients"][index - 1]
      print(f"The ingredient you selected was: {ingredient_choice}")
      break


  found = False
  for recipe in data["recipes_list"]:
    if ingredient_choice in recipe["ingredients"]:
      display_recipe(recipe)
      found = True
  if not found:
      print(f"There were no recipes found that contained the ingredient: '{ingredient_choice}'.")

  return ingredient_choice

while True:
  user_file = input("Enter the file that contains your recipes: ")

  try:
    with open(user_file, 'rb') as file:
      data = pickle.load(file)
  except FileNotFoundError:
    print("File doesn't exist please try again.")
  else:
    search_ingredient(data)
    break