import pickle

def take_recipe():
  while True: 
    name = str(input("What is the name of this recipe: "))
    if name == "": 
      print("Recipe name cant be blank")
    else: 
      break

  while True: 
    cooking_time =  int(input("What is the cooking time in minutes: "))
    if cooking_time <= 0:
      print("Cooking time must be greater than zero")
    else: 
      break

  while True:
    ingredients_input = input("Enter a list of ingredients that are seperated by a comma: ").strip()
    ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",") if ingredient.strip()]
    if ingredients:
      break

  difficulty = calc_difficulty(cooking_time, ingredients)

  recipe = {"name": name, "cooking_time": cooking_time, "ingredients": ingredients, "difficulty": difficulty}
  return recipe

def calc_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    return "Easy"
  elif cooking_time < 10 and len(ingredients) >= 4:
    return "Medium"
  elif cooking_time >= 10 and len(ingredients) < 4:
    return "Intermediate"
  else:
    return "Hard"

user_file = str(input("Enter a filename: "))

try:
  file = open(user_file, 'rb')
  data = pickle.load(file)
except FileNotFoundError:
  print("File doesn't exist please try again.")
  data = {"recipes_list": [], "all_ingredients": []}
except:
  print("There has been an unexpected error, please try again.")
  data = {"recipes_list": [], "all_ingredients": []}
else:
  file.close()
finally:
  recipes_list = data["recipes_list"]
  all_ingredients = data["all_ingredients"]

n = input("How many recipes would you like to enter: ")

for i in range(int(n)):
  recipe = take_recipe()

  for ingredient in recipe["ingredients"]:
    ingredients_stripped = ingredient.strip()
    if ingredients_stripped not in all_ingredients:
      all_ingredients.append(ingredients_stripped)

  recipes_list.append(recipe)

data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

with open(user_file, 'wb') as file:
  pickle.dump(data, file)