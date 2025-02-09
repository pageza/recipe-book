import re

def format_recipe(recipe_data):
    """Return a formatted recipe string given the recipe JSON data."""
    # Format the ingredients: one per line.
    ingredients = recipe_data.get('ingredients', '')
    ingredients_list = [ingredient.strip() for ingredient in ingredients.split(',')]
    formatted_ingredients = "\n".join(ingredients_list)
    
    # Format the instructions: ensure each numbered step starts on a new line.
    instructions = recipe_data.get('recipe_text', '').strip()
    formatted_instructions = re.sub(r'\s*(\d+\.)', r'\n\1', instructions).strip()
    
    formatted_text = (
        f"Recipe Name: {recipe_data.get('name', '')}\n\n"
        "Ingredients:\n" + formatted_ingredients + "\n\n"
        f"Calories: {recipe_data.get('calories', '')}\n\n"
        "Instructions:\n" + formatted_instructions
    )
    return formatted_text
