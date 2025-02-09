#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

from db import init_db
from gui import RecipeApp
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def main():
    init_db()
    app = RecipeApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
