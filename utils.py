import sqlite3
import os

def get_topic(ticket_id: int) -> str:
    """
    Get the topic from the ticket ID.
    
    This function retrieves the topic associated with a specific ticket ID.
    """
    # Define the database path
    db_path = os.path.join(os.getcwd(), "ticket_topics.db")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query the database for the topic
    cursor.execute("SELECT topic FROM ticket_topics WHERE ticket_id = ?", (ticket_id,))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # Return the topic if found, otherwise return "Unknown Topic"
    return result[0] if result else "Unknown Topic"