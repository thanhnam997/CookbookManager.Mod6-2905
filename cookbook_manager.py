# Use the SQLite database
import sqlite3
from sqlite3 import Error 

# Function to create a connection to the database 
def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('hipster_cookbook.db')
        print(f"Successfully connected to SQLite {sqlite3.version}")
        return conn
    except Error as e:
        # Print an error message if the connection fails
        print(f"Error establishing connection with the void: {e}")
        return None

# Function to create a table for storing the cookbooks
def create_table(conn):
    """Create the cookbooks table if it doesn't already exist."""
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # SQL command to create the cookbooks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cookbooks (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           title TEXT NOT NULL,
           author TEXT NOT NULL,
           year_published INTEGER,
           aesthetic_rating INTEGER,
           instagram_worthy BOOLEAN,
           cover_color TEXT
        );
        """)

        # SQL command to create the tags table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """)

        # SQL command to create the cookbook_tags table 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cookbook_tags (
            cookbook_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (cookbook_id) REFERENCES cookbooks(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (cookbook_id, tag_id)
        );
        """)

        print("Successfully created all tables")
    except Error as e:
        # Print an error message if the table creation fails
        print(f"Error creating table: {e}")

# Function to insert a new cookbook record into the database table 
def insert_cookbook(conn, cookbook):
    """Add a new cookbook to the database."""
    # SQL command to insert a new cookbook
    sql = '''INSERT INTO cookbooks(title, author, year_published, aesthetic_rating, instagram_worthy, cover_color) VALUES(?,?,?,?,?,?)'''
    
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # Execute the SQL command with the provided cookbook data
        cursor.execute(sql, cookbook)
        # Commit the transaction to save changes
        conn.commit()
        print(f"Successfully curated cookbook with the id: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        # Print an error message if the insertion fails
        print(f"Error adding to collection: {e}")
        return None
        
# Function to retrieve all cookbooks from the database 
def get_all_cookbooks(conn):
    """Retrieve and display all cookbooks in the database."""
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # Execute the SQL command to select all cookbooks
        cursor.execute("SELECT * FROM cookbooks")
        # Fetch all results from the query
        books = cursor.fetchall()
        # Display the details of each cookbook
        for book in books:
            print(f"ID: {book[0]}")
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Published: {book[3]}")
            print(f"Aesthetic Rating: {'xx' * book[4]}")
            print(f"Instagram Worthy: {'@@ yes' if book[5] else ' not aesthetic enough'}")
            print(f"Cover Color: {book[6]}")
            print("---")
        return books
    except Error as e:
        # Print an error message if the retrieval fails
        print(f"Error retrieving collection: {e}")
        return []

# Function to add tags to a cookbook
def add_recipe_tags(conn, cookbook_id, tags):
    """Add tags to a cookbook."""
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Insert tags into the tags table (if they don't already exist)
        for tag in tags:
            cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))

        # Get tag IDs for the provided tags
        tag_ids = []
        for tag in tags:
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag,))
            tag_id = cursor.fetchone()[0]
            tag_ids.append(tag_id)

        # Insert cookbook-tag relationships into the cookbook_tags table
        for tag_id in tag_ids:
            cursor.execute("INSERT OR IGNORE INTO cookbook_tags (cookbook_id, tag_id) VALUES (?, ?)", (cookbook_id, tag_id))

        # Commit the transaction to save changes
        conn.commit()
        print(f"Successfully added tags to cookbook {cookbook_id}")
    except Error as e:
        # Print an error message if the tag addition fails
        print(f"Error adding tags: {e}")

# Function to generate cookbook analytics
def generate_collection_analytics(conn):
    """Generate insights about your cookbook collection."""
    try:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # 1. Calculate the average aesthetic rating of all cookbooks
        cursor.execute("SELECT AVG(aesthetic_rating) FROM cookbooks")
        avg_rating = cursor.fetchone()[0]
        print(f"Average Aesthetic Rating: {avg_rating:.2f}")

        # 2. Track aesthetic trends by year (average rating per year)
        cursor.execute("""
        SELECT year_published, AVG(aesthetic_rating) 
        FROM cookbooks 
        GROUP BY year_published 
        ORDER BY year_published
        """)
        trends = cursor.fetchall()
        print("\nAesthetic Trends by Year:")
        for year, avg_rating in trends:
            print(f"Year: {year}, Average Rating: {avg_rating:.2f}")

        # 3. Identify gaps in your collection (years with fewer than 2 cookbooks)
        cursor.execute("""
        SELECT year_published 
        FROM cookbooks 
        GROUP BY year_published 
        HAVING COUNT(*) < 2 
        ORDER BY year_published
        """)
        gaps = cursor.fetchall()
        print("\nGaps in Your Collection (Years with Fewer than 2 Cookbooks):")
        for year in gaps:
            print(f"Year: {year[0]}")

    except Error as e:
        # Print an error message if the analytics generation fails
        print(f"Error generating analytics: {e}")

# Main function is called when the program executes
def main():
    """Main function to manage the cookbook database."""
    # Establish connection to our cookbook database
    conn = create_connection()

    # Test if the connection is viable
    if conn is not None:
        # Create our table 
        create_table(conn)

        # Insert some carefully curated sample cookbooks
        cookbooks = [
            ('Foraged & Found: A Guide to Pretending You Know About Mushrooms',
             'Oak Wavelength', 2023, 5, True, 'Forest Green'),
            ('Small Batch: 50 Recipes You Will Never Actually Make',
             'Sage Moonbeam', 2022, 4, True, 'Raw Linen'),
            ('The Artistic Toast: Advanced Avocado Techniques',
             'River Wildflower', 2023, 5, True, 'Recycled Brown'),
            ('Fermented Everything', 'Jim Kombucha', 2021, 3, True, 'Denim'),
            ('The Deconstructed Sandwich: Making Simple Things Complicated',
             'Juniper Vinegar-Smith', 2023, 5, True, 'Beige')
        ]

        # Display our list of books
        print("\nCurating your cookbook collection...")
        for cookbook in cookbooks:
            cookbook_id = insert_cookbook(conn, cookbook)
            # Add tags to the first cookbook as an example
            if cookbook_id == 1:
                add_recipe_tags(conn, cookbook_id, ['gluten-free', 'plant-based', 'artisanal'])
        
        # Get the cookbooks from the database
        print("\nYour carefully curated collection:")
        get_all_cookbooks(conn)

        # Generate cookbook analytics
        print("\nGenerating cookbook analytics...")
        generate_collection_analytics(conn)

        # Close the database connection
        conn.close()
        print("\nDatabase connection closed")
   
    else:
        print("Error! The universe is not aligned for database connections right now.")

if __name__ == '__main__':
    main()