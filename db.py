import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.connection.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone_number TEXT,
            address TEXT
        )''')
        self.connection.commit()

    def all_users(self):
        user = self.cursor.execute("SELECT * FROM users").fetchall()
        return user

    def add_user(self, telegram_id):
        try:
            self.cursor.execute(
                "INSERT INTO users (id) VALUES (?);",
                (telegram_id,)
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")

    def delete_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS users")

    def update_user(self, id, name, phone_number, address):
        print(id, name, phone_number, address)
        try:
            self.cursor.execute(
                "UPDATE users SET name=?, phone_number=?, address=? "
                "WHERE id=?;", (name, phone_number, address, id)
            )
            self.connection.commit()
            print("User updated successfully")
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")

    def get_user(self, id):
        try:
            user = self.cursor.execute("SELECT * FROM users WHERE id=?;", (id,))
            return user.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting user: {e}")


    def close_connection(self):
        self.cursor.close()
        self.connection.close()
