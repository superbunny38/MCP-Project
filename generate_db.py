# Python
import sqlite3
import os

# Define the database path
db_path = os.path.join(os.getcwd(), "ticket_topics.db")

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table to store ticket ID and related topics
cursor.execute("""
CREATE TABLE IF NOT EXISTS ticket_topics (
    ticket_id INTEGER PRIMARY KEY,
    topic TEXT NOT NULL
)
""")

# Insert sample data
sample_data = [
    (1, "Data Analysis"),
    (2, "Machine Learning"),
    (3, "Web Development"),
    (4, "Data Visualization"),
    (5, "Natural Language Processing"),
    (6, "Cybersecurity"),
    (7, "Cloud Computing"),
    (8, "Mobile App Development"),
    (9, "Game Development"),
    (10, "Artificial Intelligence"),
    (11, "DevOps"),
    (12, "Database Management"),
    (13, "E-commerce Solutions"),
    (14, "Blockchain Technology"),
    (15, "Internet of Things"),
    (16, "Software Testing"),
    (17, "UI/UX Design"),
    (18, "Big Data"),
    (19, "Digital Marketing"),
    (20, "IT Support")
]

cursor.executemany("INSERT OR IGNORE INTO ticket_topics (ticket_id, topic) VALUES (?, ?)", sample_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database created at: {db_path}")