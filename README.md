# CookbookManager.Mod6
This project helps you manage a collection of hipster cookbooks using a SQLite database. You can add cookbooks, tag them, and get insights about your collection.

Features
Add Cookbooks:

Add new cookbooks with details like title, author, year, rating, and more.

Tag Recipes:

Add tags to cookbooks (e.g., 'gluten-free', 'plant-based').

Get Insights:

See the average rating of all cookbooks.

Check how ratings change over the years.

Find years where you have fewer than 2 cookbooks.

How to Run
Make sure you have Python installed.

Copy the code into a file namedpython cookbook_manager.py

Open a terminal and run:

bash
Copy
python cookbook_manager.py
The program will:

Create a database (hipster_cookbook.db).

Add sample cookbooks and tags.

Show the cookbooks and analytics.

Known Issues
Input Errors:

The program doesn’t check if you enter invalid data (like text instead of numbers).

No GUI:

Everything works in the terminal; there’s no graphical interface.

Fixed Database:

If you want to add new fields or tables, you’ll need to update the code.

Extra Features
Sample Data: The program adds example cookbooks to show how it works.

Comments: The code has explanations to help you understand it.
