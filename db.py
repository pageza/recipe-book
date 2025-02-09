import sqlite3

DB_FILE = "recipes.db"

def init_db():
    """Create the database and table if not already present."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    ingredients TEXT,
                    recipe_text TEXT,
                    calories INTEGER
                )''')
    conn.commit()
    conn.close()

def save_recipe(name, ingredients, recipe_text, calories):
    """Insert a new recipe into the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO recipes (name, ingredients, recipe_text, calories) VALUES (?, ?, ?, ?)",
        (name, ingredients, recipe_text, calories)
    )
    conn.commit()
    conn.close()

def load_recipes(search_text="", max_cal=None):
    """Return a list of recipes, optionally filtered by search criteria."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT id, name, calories, ingredients FROM recipes WHERE 1=1"
    params = []
    if search_text:
        query += " AND (name LIKE ? OR ingredients LIKE ? OR recipe_text LIKE ?)"
        like_param = f"%{search_text}%"
        params.extend([like_param, like_param, like_param])
    if max_cal is not None:
        query += " AND calories <= ?"
        params.append(max_cal)
    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    return results

def delete_recipe(recipe_id):
    """Delete the recipe with the given ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
