import sqlite3

# A class that helps to store the generated passwords into a local database file called 'passwords.db'
class Password_Database_Controller:
    def __init__(self):
        # Connect to the database or create one if it does not exist
        self._password_database = sqlite3.connect('passwords.db')
        self._p_cursor = self._password_database.cursor()

        # Create a table in the database for storing passwords
        self._p_cursor.execute('CREATE TABLE IF NOT EXISTS passwords(password TEXT)')
        self.__close_database__()

    # Insert new password to the database:
    def insert_new_password(self, new_password):
        self.__connect_database__()
        self._p_cursor.execute('INSERT INTO passwords VALUES(:password)', {'password': new_password})
        self.__close_database__()

    # Find and return the password in the database associated with the given id:
    def get_password(self, id):
        self.__connect_database__()
        self._p_cursor.execute("SELECT password FROM passwords WHERE oid = " + str(id))
        query_password = self._p_cursor.fetchone() 
        self.__close_database__()

        # Return a 2-element tuple where first elem is the password and the second elem is the id
        return query_password

    # Return all of the passwords that are stored in the database:
    def get_all_previous_passwords(self):
        self.__connect_database__()
        self._p_cursor.execute("SELECT *, oid FROM passwords")
        passwords = self._p_cursor.fetchall()
        self.__close_database__() 

        return passwords
    
    # Convert the tuple returned by 'get_password' function to a string in a format of: "id)   password"
    def get_passwords_in_string(self, passwords):
        prev_passwords = ''
        for password in passwords:
            prev_passwords += str(password[1]) + ")\t" + password[0] + '\n'

        return prev_passwords

    # Delete the password that associated with the given id from the database:
    def delete_password(self, id):
        self.__connect_database__()
        self._p_cursor.execute("DELETE FROM passwords WHERE oid = " + str(id)) 
        self.__close_database__()

    # Delete all of the passwords stored in the database:
    def delete_all_passwords(self):
        self.__connect_database__()
        self._p_cursor.execute("DELETE FROM passwords")
        self.__close_database__()
    
    # Check if there is a password in the database that associated with the given id 
    def does_id_exist(self, id):
        self.__connect_database__()
        self._p_cursor.execute("SELECT password FROM passwords WHERE oid = " + str(id))
        temp = self._p_cursor.fetchone()
        self.__close_database__()

        return temp != None
    
    # Return the total number of passwords stored in the database:
    def get_number_of_passwords(self):
        self.__connect_database__()
        size = self._p_cursor.execute("SELECT COUNT() FROM passwords").fetchone()[0]
        self.__close_database__()

        return size

    # Private helper function to connect to the database:
    def __connect_database__(self):
        self._password_database = sqlite3.connect('passwords.db')
        self._p_cursor = self._password_database.cursor()

    # Private helper function to close the connection to the database:
    def __close_database__(self):
        self._password_database.commit()
        self._p_cursor.close()
        self._password_database.close()
