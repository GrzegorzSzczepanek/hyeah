import sqlite3
from datetime import datetime

class HistoryManager:
    def __init__(self, db_name="chat_history.db"):
        """Initialize the connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Create tables for users, sessions, and chat history if they don't exist."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL
                )
            ''')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_name TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')

    def create_user(self, username):
        """Create a new user with the given username."""
        try:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO users (username) VALUES (?)
                ''', (username,))
            print(f"User '{username}' created successfully.")
        except sqlite3.IntegrityError:
            print(f"User '{username}' already exists.")

    def create_session(self, username, session_name):
        """Create a new chat session for a specific user."""
        user_id = self.get_user_id(username)
        if user_id:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO sessions (user_id, session_name) VALUES (?, ?)
                ''', (user_id, session_name))
            print(f"Session '{session_name}' created for user '{username}'.")
        else:
            print(f"User '{username}' does not exist.")

    def add_message(self, username, session_name, message):
        """Add a new message to the chat history for a specific user and session."""
        session_id = self.get_session_id(username, session_name)
        if session_id:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO chat_history (session_id, message) VALUES (?, ?)
                ''', (session_id, message))
            print(f"Message added for session '{session_name}' of user '{username}'.")
        else:
            print(f"Session '{session_name}' or user '{username}' does not exist.")

    def get_user_id(self, username):
        """Retrieve the user ID based on the username."""
        cursor = self.conn.execute('''
            SELECT user_id FROM users WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_session_id(self, username, session_name):
        """Retrieve the session ID for a specific user and session name."""
        user_id = self.get_user_id(username)
        if user_id:
            cursor = self.conn.execute('''
                SELECT session_id FROM sessions WHERE user_id = ? AND session_name = ?
            ''', (user_id, session_name))
            result = cursor.fetchone()
            return result[0] if result else None
        return None

    def get_chat_history(self, username, session_name, limit=10):
        """Retrieve the chat history of a specific user and session."""
        session_id = self.get_session_id(username, session_name)
        if session_id:
            cursor = self.conn.execute('''
                SELECT message, timestamp FROM chat_history
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (session_id, limit))
            records = cursor.fetchall()
            return records
        else:
            print(f"Session '{session_name}' or user '{username}' does not exist.")
            return []

    def delete_user(self, username):
        """Delete a user and all their associated chat history and sessions."""
        user_id = self.get_user_id(username)
        if user_id:
            with self.conn:
                # First delete chat history, sessions, and then the user
                self.conn.execute('DELETE FROM chat_history WHERE session_id IN (SELECT session_id FROM sessions WHERE user_id = ?)', (user_id,))
                self.conn.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
                self.conn.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            print(f"User '{username}' and all their sessions and chat history deleted.")
        else:
            print(f"User '{username}' does not exist.")

    def clear_session(self, username, session_name):
        """Clear all messages in a specific session for a user."""
        session_id = self.get_session_id(username, session_name)
        if session_id:
            with self.conn:
                self.conn.execute('DELETE FROM chat_history WHERE session_id = ?', (session_id,))
            print(f"All messages cleared for session '{session_name}' of user '{username}'.")
        else:
            print(f"Session '{session_name}' or user '{username}' does not exist.")

    def update_message(self, chat_id, new_message):
        """Update a specific message in the chat history."""
        with self.conn:
            self.conn.execute('''
                UPDATE chat_history
                SET message = ?, timestamp = ?
                WHERE chat_id = ?
            ''', (new_message, datetime.now(), chat_id))
        print(f"Message with chat_id '{chat_id}' updated.")

    def close(self):
        """Close the connection to the database."""
        self.conn.close()

# Example Usage:
def exampleUsage():
    manager = HistoryManager()

    # Create users
    manager.create_user("john_doe")
    manager.create_user("alice")

    # Create sessions for users
    manager.create_session("john_doe", "Session 1")
    manager.create_session("alice", "Session A")

    # Add messages for users in their respective sessions
    manager.add_message("john_doe", "Session 1", "Hello, how can I help you today?")
    manager.add_message("john_doe", "Session 1", "Do you need assistance with your taxes?")
    manager.add_message("alice", "Session A", "I need help with filing my taxes.")

    # Retrieve chat history for a specific session of a user
    john_history = manager.get_chat_history("john_doe", "Session 1", limit=5)
    print("Chat history for john_doe in Session 1:")
    for message, timestamp in john_history:
        print(f"[{timestamp}] {message}")

    # Clear chat history for a specific session
    manager.clear_session("john_doe", "Session 1")

    # Delete a user and their history
    manager.delete_user("alice")

    # Close the manager
    manager.close()
