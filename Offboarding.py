import subprocess
import os
import sys
import time

input_user = input("Enter email address of user to be offboarded: ")

try:
    # Run GAM command to print users
    list_users = subprocess.run(
        ['gam', 'print', 'users'],
        capture_output=True,
        text=True,
        check=True,
    )
    
    output = list_users.stdout  # Capture output of GAM command

    # Collect all matching users within your domain
    matching_users = [line for line in output.splitlines() if input_user in line]

    if matching_users:
        print(f"Found {len(matching_users)} user(s) matching '{input_user}':")
        
        # Display matching users
        for idx, user in enumerate(matching_users, 1):
            print(f"{idx}. {user}")

        # Ask user to choose which account to offboard
        user_choice = input(f"Please choose the user number (1-{len(matching_users)}): ")

        # Confirmation ofu ser choice
        try:
            user_choice = int(user_choice)
            if 1 <= user_choice <= len(matching_users):
                selected_user = matching_users[user_choice - 1]
                print(f"You selected: {selected_user}")
                
            else:
                print("Invalid choice. Exiting.")
                sys.exit(1)
        except ValueError:
            print("Invalid input. Please enter a number. Exiting.")
            sys.exit(1)
        
    else:
        print(f"No users found matching '{input_user}'")
        sys.exit(1)  # Exit the script if no user is found

except subprocess.CalledProcessError as e:
    # Handle the case when GAM command fails
    print(f"Error running the GAM command: {e}")
    sys.exit(1)

except FileNotFoundError:
    # Handle case where GAM is not installed or not found in PATH
    print("GAM command not found. Please ensure GAM is installed.")
    sys.exit(1)

time.sleep(1.5)

print(f"Unsuspending {selected_user}...")
subprocess.run(f"gam unsuspend user {selected_user}", shell=True)

def Calendar():
    selection = input(f"Delete {selected_user} calendar events? (y/n)?: ")
    if selection.lower() == "y":
        print(f"Deleting {selected_user} calendar events ")
        subprocess.run(f"gam calendar {selected_user} wipe events", shell=True)         
    else:  
        print(f"{selected_user} calendar events will be kept")

Calendar()


class Session:
    def __init__(self, selected_user):
        self.selected_user = selected_user  

    def Tokens_Passwords(self):
        "Reset GSuite tokens and user passwords."
        try:
            print(f'Resetting GSuite tokens for {self.selected_user}...')
            subprocess.run(["gam", "user", self.selected_user, "deprovision"], check=True)
            subprocess.run(["gam", "user", self.selected_user, "update", "backupcodes"], check=True)

            print(f"Resetting {self.selected_user}'s password...")
            subprocess.run(["gam", "update", "user", self.selected_user, "password", "blocklogin"], check=True)

            print("Refreshing cookies and sign-in sessions...")
            subprocess.run(["gam", "user", self.selected_user, "signout"], check=True)

            print("Turning off 2fa")
            subprocess.run(["gam", "user", self.selected_user, "turnoff2sv"])

            print(f"All actions completed for {self.selected_user}.")

        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess execution: {e}")
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            

session = Session(selected_user)  # Create a Session instance for a user
session.Tokens_Passwords()


def remove_groups(selected_user):
    groups = input(f"Remove {selected_user} from all groups? (y/n): ").strip()
    if groups.lower() == "y":
        try:
            subprocess.run(["gam", "user", selected_user, "delete", "groups"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error removing groups for {selected_user}: {e}")
    else:
        print(f"{selected_user} groups will not be deleted")


import subprocess

def Ownership(selected_user):
    manager = input(f"Do you want to transfer Google Drive files for {selected_user} to their manager? (y/n/skip): ").lower()
    
    if manager == "y":
        try:
            get_manager = input(f"Who is {selected_user}'s manager? ")
            print(f"Transferring {selected_user}'s Drive files to {get_manager}...")
            subprocess.run(["gam", "user", selected_user, "transfer", "drive", get_manager], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to transfer {selected_user}'s Drive files to {get_manager}: {e}")
    
    elif manager == "n":
        try:
            confirm_transfer = input(f"Have the files already been transferred? (y/n): ").lower()
            if confirm_transfer == "y":
                print("Skipping file transfer as confirmed.")
            else:
                print("No action taken. Please ensure the files are properly handled.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    elif manager == "skip":
        print(f"Skipping the ownership transfer process for {selected_user}.")
    
    else:
        try:
            print(f"Transferring {selected_user}'s files to admin account...")
            subprocess.run(["gam", "user", selected_user, "transfer", "drive", "], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to transfer {selected_user}'s Drive files to youremailhere@email.com: {e}")

Ownership(selected_user)


time.sleep(2)

def Gmail(selected_user):
    backup = input(f"Backup {selected_user} emails? (y/n)")
    if backup.lower() == "y":
        try:
            print(f"Backing up {selected_user}'s gmail")
            subprocess.run(["gyb", "--email", selected_user, "--service-account", "--local-folder", f"C:\\Your Drive\path to file location\\{selected_user}"], check=True)
        except Exception as e:
            print(f"Error backing up emails: {e}")
    else: 
        print(f"skipping gmail backup")
Gmail(selected_user)


print(f"Suspending {selected_user}...")
subprocess.run(['gam', 'suspend', 'user', selected_user])


delete = input("Do you want to delete this user? (y/n): ").strip()
if delete.lower() == "y":
    try:
        subprocess.run(["gam", "delete", "user", selected_user], check=True)
        print(f"{selected_user} has been deleted. The license is now available, and the account will be permanently deleted in 20 days.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to delete {selected_user}: {e}")
else:
    print(f"{selected_user} will not be deleted.")

time.sleep(5)


print(f"Offboarding for {selected_user} has been completed")

time.sleep(5)

