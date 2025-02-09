import os
import json
import re
import openai
from gi.repository import GLib

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_recipe(prompt, callback):
    """Generate a recipe from the given prompt and call the callback with the formatted text and parsed data."""
    messages = [
        {"role": "system", "content": (
            "You are a recipe generating assistant. When given a prompt, generate a recipe "
            "as a JSON object with the following keys: 'name' (string), "
            "'ingredients' (a comma-separated string), 'calories' (an integer), "
            "and 'recipe_text' (string with full instructions). Ensure the JSON is valid."
        )},
        {"role": "user", "content": prompt},
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        raw_text = response.choices[0].message.content.strip()
        try:
            recipe_data = json.loads(raw_text)
            # Use our formatting utility.
            from utils import format_recipe
            formatted_text = format_recipe(recipe_data)
        except json.JSONDecodeError:
            recipe_data = None
            formatted_text = raw_text  # Fallback if JSON parsing fails
    except Exception as e:
        formatted_text = f"Error generating recipe: {e}"
        recipe_data = None
    # Pass the result to the callback on the main thread.
    GLib.idle_add(callback, formatted_text, recipe_data)
