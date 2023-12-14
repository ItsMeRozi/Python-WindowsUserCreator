"""
User Account Creation Program in Python for Windows operating systems.
Latest update: 23.06.2023
A console-based program that creates a user with the provided parameters.
Created users are stored in a file text Users.txt
"""

# Import necessary modules
import ctypes
import sys
import time
import os
import string
import random
import subprocess

# Get the current directory path and create a path for the Users.txt file
folder_path = os.path.dirname(os.path.abspath(__file__))
logins_path = os.path.join(folder_path, 'CreatedUsers', 'Users.txt')

# Create 'CreatedUsers' folder if it doesn't exist
if not os.path.exists(os.path.join(folder_path, 'CreatedUsers')):
    os.makedirs(os.path.join(folder_path, 'CreatedUsers'))

file = open(logins_path, 'a')

# Generate a unique username.
def unique_username(generated_usernames, prefixuser=''):
    while True:
        number1 = random.randint(1000, 9999)
        letters = ''.join(random.choice(string.ascii_letters) for _ in range(2))
        rusername = f"{prefixuser}{letters}{number1}"
        if rusername not in generated_usernames:
            generated_usernames.add(rusername)
            return rusername

# Write username and password to the Users.txt file.
def write_logins(i, username, password):
    i += 1
    print(f"Your username is: {username}, and the password is: {password}\n")
    file.write(f"{i}. Username: {username} Password: {password}\n")

# Write a line of dashes to the Users.txt file.
def lines():
    file.write("----------------------------------------------------------\n")
    file.close()

# Create a new user using the net user command.
def create_user(username, password):
    process = subprocess.Popen(f'net user {username} {password} /add', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        return True
    else:
        return False

# Main function to execute the user account creation process.
def main():
    # Check if the script is run with administrator privileges
    if ctypes.windll.shell32.IsUserAnAdmin():
        try:
            choice = input("Do you want the username to be generated randomly? (y/n): ").lower()
            if choice == "n":
                i = 0
                username = input("Enter the username: ")
                password = input("Enter the account password: ")
                if create_user(username, password):
                    print("\nAccount created successfully.\n")
                    time.sleep(0.5)
                    write_logins(i, username, password)
                    lines()
                else:
                    print("\nSomething went wrong.\n")
            elif choice == "y":
                choice2 = input("Do you want to apply a custom prefix? (y/n): ").lower()
                if choice2 == "n":
                    quantity = int(input("How many users to generate: "))
                    generated_usernames = set()
                    for i in range(quantity):
                        rusername = unique_username(generated_usernames, prefixuser="User")
                        rpassword = f"Pass{random.randint(1000, 9999)}"
                        if create_user(rusername, rpassword):
                            write_logins(i, rusername, rpassword)
                            lines()
                        else:
                            print("Something went wrong.")
                elif choice2 == "y":
                    prefixuser = input("Enter the prefix for the username: ")
                    prefixpass = input("Enter the prefix for the password: ")
                    quantity = int(input("How many users to generate: "))
                    generated_usernames = set()
                    for i in range(quantity):
                        rusername = unique_username(generated_usernames, prefixuser=prefixuser)
                        rpassword = f"{prefixpass}{random.randint(1000, 9999)}"
                        if create_user(rusername, rpassword):
                            write_logins(i, rusername, rpassword)
                            lines()
                        else:
                            print("Something went wrong.")
        except:
            print("Something went wrong.")

    else:
        # If not run as admin, attempt to run the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

# Execute the main function in a loop to generate more users if desired
while True:
    try:
        main()
        choice = input("Generate more users? (y/n): ")
        if choice == "n":
            break
        elif choice == "y":
            continue
        else:
            break
    except KeyboardInterrupt:
        print("\nScript stopped.")
        break
