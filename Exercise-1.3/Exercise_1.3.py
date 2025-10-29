recipes_list = []
ingredients_list = []

def take_recipe():
  while True: 
    name = str(input("What is the name of this recipe: "))
    if name == "": 
      print("Recipe name cant be blank")
    else: 
      break
    
  while True: 
    cooking_time = int(input("What is the cooking time in minutes: "))
    if cooking_time <= 0:
      print("Cooking time must be greater than zero")
    else: 
      break


  while True:
    ingredients = input("Enter a list of ingredients that are seperated by a comma: ").split(",")
    if all(not ingredient.strip() for ingredient in ingredients):
      print("You must enter atleast one ingredient")
    else:
      break


  recipe = {"name": name, "cooking_time": cooking_time, "ingredients": ingredients}

  return recipe

n = input("How many recipes would you like to enter: ")

for i in range(int(n)):
  recipe = take_recipe()

  for ingredient in recipe["ingredients"]:
    ingredients_stripped = ingredient.strip()
    if ingredients_stripped not in ingredients_list:
      ingredients_list.append(ingredients_stripped)

  recipes_list.append(recipe)

for recipe in recipes_list:
  cooking_time = recipe["cooking_time"]
  number_of_ingredients = len(recipe["ingredients"])

  if cooking_time < 10 and number_of_ingredients < 4:
    recipe["difficulty"] = "Easy"
  if cooking_time < 10 and number_of_ingredients >= 4:
    recipe["difficulty"] = "Medium"
  if cooking_time >= 10 and number_of_ingredients < 4:
    recipe["difficulty"] = "Intermediate"
  if cooking_time >= 10 and number_of_ingredients >= 4:
    recipe["difficulty"] = "Hard"


for recipe in recipes_list:
  print("Recipe: " + str(recipe["name"] + "\n"),
        "Cooking time:",recipe["cooking_time"], "\n",
        "Ingredients:"
        )
  for ingredients in recipe["ingredients"]: 
    print(ingredients)

  print(
    "Difficulty level:", recipe["difficulty"]
  )

print(" Ingredients Available Across All Recipes\n", 
      "----------------------------------------")
ingredients_list.sort()
for ingredients in ingredients_list: 
  print(ingredients)