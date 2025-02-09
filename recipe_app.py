#!/usr/bin/env python3
import os
import threading
import sqlite3
import openai
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

# Configure your OpenAI API key (alternatively use env variable OPENAI_API_KEY)
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

DB_FILE = "recipes.db"

def init_db():
    """Initialize SQLite database if not exists."""
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

class RecipeApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="ChatGPT Recipe Book")
        self.set_default_size(800, 600)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        # Tab 1: Recipe Generator
        self.generator_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.generator_box.set_border_width(10)
        self.notebook.append_page(self.generator_box, Gtk.Label(label="Generate Recipe"))
        self.create_generator_tab()

        # Tab 2: Recipe Book
        self.book_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.book_box.set_border_width(10)
        self.notebook.append_page(self.book_box, Gtk.Label(label="Recipe Book"))
        self.create_recipe_book_tab()

    def create_generator_tab(self):
        self.output_view = Gtk.TextView()
        self.output_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.output_buffer = self.output_view.get_buffer()
        scrolled_output = Gtk.ScrolledWindow()
        scrolled_output.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_output.add(self.output_view)
        self.generator_box.pack_start(scrolled_output, True, True, 0)

        self.prompt_entry = Gtk.Entry()
        self.prompt_entry.set_placeholder_text("Enter recipe prompt or modifications...")
        self.generator_box.pack_start(self.prompt_entry, False, False, 0)

        button_box = Gtk.Box(spacing=10)
        self.generate_button = Gtk.Button(label="Generate Recipe")
        self.generate_button.connect("clicked", self.on_generate_recipe)
        button_box.pack_start(self.generate_button, True, True, 0)

        self.save_button = Gtk.Button(label="Save Recipe")
        self.save_button.connect("clicked", self.on_save_recipe)
        button_box.pack_start(self.save_button, True, True, 0)
        self.generator_box.pack_start(button_box, False, False, 0)

    def create_recipe_book_tab(self):
        search_box = Gtk.Box(spacing=10)
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search by name or ingredient")
        self.search_entry.connect("changed", self.on_search_changed)
        search_box.pack_start(self.search_entry, True, True, 0)

        self.filter_cal_entry = Gtk.Entry()
        self.filter_cal_entry.set_placeholder_text("Max calories (optional)")
        self.filter_cal_entry.connect("changed", self.on_search_changed)
        search_box.pack_start(self.filter_cal_entry, True, True, 0)

        self.book_box.pack_start(search_box, False, False, 0)

        self.recipe_liststore = Gtk.ListStore(int, str, int)
        self.treeview = Gtk.TreeView(model=self.recipe_liststore)

        renderer_text = Gtk.CellRendererText()
        column_name = Gtk.TreeViewColumn("Recipe Name", renderer_text, text=1)
        self.treeview.append_column(column_name)
        renderer_cal = Gtk.CellRendererText()
        column_cal = Gtk.TreeViewColumn("Calories", renderer_cal, text=2)
        self.treeview.append_column(column_cal)

        self.treeview.get_selection().connect("changed", self.on_recipe_selected)
        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_tree.add(self.treeview)
        self.book_box.pack_start(scrolled_tree, True, True, 0)

        self.detail_view = Gtk.TextView()
        self.detail_view.set_editable(False)
        self.detail_view.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled_detail = Gtk.ScrolledWindow()
        scrolled_detail.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_detail.set_min_content_height(150)
        scrolled_detail.add(self.detail_view)
        self.book_box.pack_start(scrolled_detail, False, False, 0)

        self.load_recipes()

    def on_generate_recipe(self, widget):
        prompt = self.prompt_entry.get_text().strip()
        if not prompt:
            self.show_message("Please enter a recipe prompt or modification instruction.")
            return
        self.generate_button.set_sensitive(False)
        self.output_buffer.insert(self.output_buffer.get_end_iter(), "\nGenerating recipe...\n")
        threading.Thread(target=self.generate_recipe_api, args=(prompt,)).start()

    def generate_recipe_api(self, prompt):
        messages = [
            {"role": "system", "content": "You are a recipe generating assistant."},
            {"role": "user", "content": prompt},
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            recipe_text = response.choices[0].message.content.strip()
        except Exception as e:
            recipe_text = f"Error generating recipe: {e}"
        GLib.idle_add(self.update_output, recipe_text)

    def update_output(self, text):
        self.output_buffer.insert(self.output_buffer.get_end_iter(), text + "\n")
        self.generate_button.set_sensitive(True)

    def on_save_recipe(self, widget):
        start, end = self.output_buffer.get_bounds()
        recipe_text = self.output_buffer.get_text(start, end, True).strip()
        if not recipe_text:
            self.show_message("No recipe available to save.")
            return

        dialog = Gtk.Dialog(title="Save Recipe", parent=self, flags=0)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
        )
        box = dialog.get_content_area()
        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin=10)
        box.add(grid)

        name_label = Gtk.Label(label="Recipe Name:")
        grid.attach(name_label, 0, 0, 1, 1)
        name_entry = Gtk.Entry()
        grid.attach(name_entry, 1, 0, 1, 1)

        ingredients_label = Gtk.Label(label="Ingredients (comma-separated):")
        grid.attach(ingredients_label, 0, 1, 1, 1)
        ingredients_entry = Gtk.Entry()
        grid.attach(ingredients_entry, 1, 1, 1, 1)

        cal_label = Gtk.Label(label="Estimated Calories:")
        grid.attach(cal_label, 0, 2, 1, 1)
        cal_entry = Gtk.Entry()
        grid.attach(cal_entry, 1, 2, 1, 1)

        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = name_entry.get_text().strip() or "Unnamed Recipe"
            ingredients = ingredients_entry.get_text().strip()
            try:
                calories = int(cal_entry.get_text().strip())
            except ValueError:
                calories = 0
            self.save_recipe_to_db(name, ingredients, recipe_text, calories)
        dialog.destroy()

    def save_recipe_to_db(self, name, ingredients, recipe_text, calories):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO recipes (name, ingredients, recipe_text, calories) VALUES (?, ?, ?, ?)",
                  (name, ingredients, recipe_text, calories))
        conn.commit()
        conn.close()
        self.show_message("Recipe saved successfully!")
        self.load_recipes()

    def load_recipes(self):
        self.recipe_liststore.clear()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        query = "SELECT id, name, calories, ingredients FROM recipes WHERE 1=1"
        params = []
        search_text = self.search_entry.get_text().strip()
        if search_text:
            query += " AND (name LIKE ? OR ingredients LIKE ? OR recipe_text LIKE ?)"
            like_param = f"%{search_text}%"
            params.extend([like_param, like_param, like_param])
        max_cal = self.filter_cal_entry.get_text().strip()
        if max_cal.isdigit():
            query += " AND calories <= ?"
            params.append(int(max_cal))
        c.execute(query, params)
        for row in c.fetchall():
            self.recipe_liststore.append([row[0], row[1], row[2]])
        conn.close()

    def on_search_changed(self, widget):
        self.load_recipes()

    def on_recipe_selected(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is None:
            return
        recipe_id = model[treeiter][0]
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT recipe_text FROM recipes WHERE id = ?", (recipe_id,))
        row = c.fetchone()
        conn.close()
        if row:
            detail_buffer = self.detail_view.get_buffer()
            detail_buffer.set_text(row[0])

    def show_message(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()

def main():
    init_db()
    win = RecipeApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
