import mysql.connector
import re

# Establishing a connection to MySQL
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="contact"
)
cursor = connection.cursor()

create_database_query = "CREATE DATABASE IF NOT EXISTS contact"
cursor.execute(create_database_query)
connection.commit()

# Switching to the 'contact' database
connection.database = "contact"


# Creating the contacts table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS contacts (
    name VARCHAR(255) PRIMARY KEY,
    phone VARCHAR(20),
    email VARCHAR(255)
);
"""
cursor.execute(create_table_query)
connection.commit()


# Function to add a new contact to the database
def add_contact():
    name = input("Enter the contact's name: ")

    while True:
        phone = input("Enter the contact's phone number (integers only): ")
        if phone.isdigit():
            break
        else:
            print("Invalid phone number. Please enter integers only.")

    while True:
        email = input("Enter the contact's email (e.g., zogata@gmail.com): ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        else:
            print("Invalid email format. Please enter a valid email address.")

    # Inserting contact into the database
    insert_query = "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (name, phone, email))
    connection.commit()

    print(f"{name} has been added to the contact book.")


# Function to view a contact from the database
def view_contact():
    name = input("Enter the name of the contact you want to view: ")

    # Retrieving contact from the database
    select_query = "SELECT * FROM contacts WHERE name = %s"
    cursor.execute(select_query, (name,))
    result = cursor.fetchone()

    if result:
        print(f"Name: {result[0]}")
        print(f"Phone: {result[1]}")
        print(f"Email: {result[2]}")
    else:
        print(f"{name} not found in the contact book.")


# Function to update a contact in the database
def update_contact():
    name = input("Enter the name of the contact you want to update: ")

    while True:
        phone = input("Enter the new phone number: ")
        if phone.isdigit():
            break
        else:
            print("Invalid phone number. Please enter integers only.")

    while True:
        email = input("Enter the new email: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        else:
            print("Invalid email format. Please enter a valid email address.")

    # Updating contact in the database
    update_query = "UPDATE contacts SET phone = %s, email = %s WHERE name = %s"
    cursor.execute(update_query, (phone, email, name))
    connection.commit()

    print(f"{name}'s information has been updated.")


# Function to delete a contact from the database
def delete_contact():
    name = input("Enter the name of the contact you want to delete: ")

    # Deleting contact from the database
    delete_query = "DELETE FROM contacts WHERE name = %s"
    cursor.execute(delete_query, (name,))
    connection.commit()

    print(f"{name} has been deleted from the contact book.")


# Function to search contacts by letter
def search_contacts_by_letter(letter):
    select_query = "SELECT name FROM contacts WHERE name LIKE %s"
    cursor.execute(select_query, (letter + '%',))
    matches = cursor.fetchall()

    if matches:
        print(f"Contacts starting with letter '{letter}':")
        for match in matches:
            print(match[0])
    else:
        print(f"No contacts found starting with letter '{letter}'.")


# Main menu
while True:
    print("\nWelcome to your Contact Book Menu:")
    print("1. Add a contact")
    print("2. View a contact")
    print("3. Update a contact")
    print("4. Delete a contact")
    print("5. Search a contact by Letter")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_contact()
    elif choice == '2':
        view_contact()
    elif choice == '3':
        update_contact()
    elif choice == '4':
        delete_contact()
    elif choice == '5':
        letter = input("Enter the letter to search for contacts: ")
        search_contacts_by_letter(letter.upper())
    elif choice == '6':
        print("Exiting the Contact Book. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# Don't forget to close the cursor and connection when you're done
cursor.close()
connection.close()