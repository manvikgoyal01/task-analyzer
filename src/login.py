"""
- Handles login/signup of a user
- Importing/Creating data file of a user
- Changing username/password of a user
- Deleting account of the user
- Exporting the users datafile and user individual datafile
- Custom exporting passed data to a input path
"""

import pandas as pd
import json
import sys
import os

from utils import consent

# file path of where the users data file is stored
USERS_FILE = "database/users.csv"
# directory name where user's individual files are stored
DATABASE = "database"


class Login:

    def __init__(self):

        try:
            with open(USERS_FILE, "r") as f:
                self.users_database = pd.read_csv(f)

        except FileNotFoundError:
            print("\nUsers file could not be found")
            sys.exit()

        # initiates user login/signup process
        self.login_user()

    def login_user(self):
        """
        - Asks user for username or 'new' to signup (returns create user method)
        - Asks for password and verifies
        - Loads and formats the user individual file data
        """

        # asks user for their username, or 'new' to begin signup process
        username = input("\nPlease enter your username (or 'new') : ").strip().lower()

        if username == "new":
            # returns the new user method to initiate account creation
            return self.new_user()

        # asks and verifies user's password
        if username in self.users_database["username"].values:
            password = input("\nPlease enter your password : ").strip()

            if (password == self.users_database[self.users_database["username"] == username]["password"].values):

                try:
                    # attempt to open user's individual datafile
                    with open(f"database/{username}.json", "r") as f:
                        data = json.load(f)

                        self.username = username
                        self.userid = self.users_database[self.users_database["username"] == self.username].index
                        self.userstats = data["userstats"]

                        if len(data["userdata"]) > 0:
                            # if userdata exists then loads and formats it
                            # conversion of dates in string to datetime object
                            # conversion of nan to pd.NA

                            self.userdata = pd.DataFrame.from_dict(data["userdata"], orient="index")
                            self.userdata["Start Time"] = pd.to_datetime(self.userdata["Start Time"])
                            self.userdata["Deadline"] = pd.to_datetime(self.userdata["Deadline"])

                            for i in self.userdata.index:
                                if self.userdata.loc[i, "Completed On"] != "Ongoing":
                                    self.userdata.loc[i, "Completed On"] = (pd.to_datetime(self.userdata.loc[i, "Completed On"]))

                            self.userdata.index = self.userdata.index.astype(int)

                            for i in self.userdata.index:
                                if self.userdata.loc[i, "Was Late"] is None:
                                    self.userdata.loc[i, "Was Late"] = pd.NA
                                if self.userdata.loc[i, "Duration"] is None:
                                    self.userdata.loc[i, "Duration"] = pd.NA

                        # if no data exists in userdata then a new dataframe is created
                        else:
                            self.userdata = pd.DataFrame(
                                columns=["Task Name", "Task Type", "Task Importance", "Start Time", "Deadline", "Completed On", "Was Late", "Duration", "Is Outlier", "Notes"])

                        print("\nLogged in successfully")
                        return

                # if user's individual file cannot be found
                except FileNotFoundError:
                    print("\nThe data file couldn't be found.")
                    sys.exit()

            # if user enters an invalid password
            else:
                print("\nInvalid Password.")

        # if user enters an invalid username
        else:
            print("\nUser not found")

        sys.exit()

    def new_user(self):
        """
        - Creates a new account for user in the database
        - Asks for username and password
        - Updates the database and saves the changes
        """

        username = input("\nEnter your username : ").strip().lower()
        username = username.replace(" ", "_")

        # user cannot user username or new as username
        if username in ["username", "new"]:
            print("\nYou cannot choose this username")
            return self.create_user()

        # checks if the username already exists in the database
        # if exists, returns login user method
        if username in self.users_database["username"].values:
            print("\nUser already exists. Please login or use different username.")
            return self.login_user()

        password = input("\nEnter your password : ").strip()

        # confirms if user wants to create the account
        print(f"\nYou are creating a new user : \n Username - {username} \n Password - {password}")
        ask = consent()

        if ask:
            # if user agrees, the users database is updated
            # a new individual user file is created

            if len(self.users_database) == 0:
                self.users_database.loc[1, :] = [username, password]
            else:
                self.users_database.loc[max(self.users_database.index) + 1, :] = [username, password]

            d1 = {"Username": username, "Total Tasks": 0, "Completed Tasks": 0, "Ongoing Tasks": 0, "Late Tasks": 0, "On-Time Rate (%)": 0}
            d2 = pd.DataFrame()
            self.username = username
            self.export_data(d21=d1, d22=d2)

            print("\nAccount created successfully")
            sys.exit()

        else:
            # if user doesn't agree to create a new account
            print("\nCancelling add new user")
            sys.exit("\nExiting...\n")

    def change_password(self):
        """
        - Allows user to change their password
        - Asks for current password and verifies
        - If verified asks for new password
        """

        old = input("\nEnter your current password : ").strip()

        # checks if the passwords match
        if old == self.users_database.loc[self.userid, "password"].values:
            new = input("\nEnter your new password : ").strip()

            print("\nAre you sure you want to change your password?")
            ask = consent()

            if ask:
                # if user agrees to create the account, users file database is updated and saved
                self.users_database.loc[self.userid, "password"] = new
                self.export_data()
                print("\nPassword changed successfully.")

            else:
                # if user doesn't agree to create new account
                print("\nCancelling change password command.")
                return

        else:
            print("\nWrong password entered.")

    def change_username(self):

        passw = input("\nEnter your password : ").strip()

        if passw == self.users_database.loc[self.userid, "password"].values:
            new = input("\nEnter new username : ").strip().lower()
            new = new.replace(" ", "_")

            print(f"\nAre you sure you want to change username to {new} ?")
            ask = consent()

            if ask:
                try:
                    os.rename(f"database/{self.username}.json", f"database/{new}.json")

                except:
                    print("\nError renaming the user file.")
                    return

                self.users_database.loc[self.userid, "username"] = new
                self.userstats["Username"] = new
                self.username = new
                self.export_data()
                print("Username changed successfully")

            else:
                print("\nCancelling change username command.")
        else:
            print("\nWrong password entered.")

    def delete_user(self):

        passw = input("\nEnter your password : ").strip()

        if passw == self.users_database.loc[self.userid, "password"].values:
            print("\nAre you sure you want to permanently delete all your account?")
            ask = consent()

            if ask:
                try:
                    os.remove(f"database/{self.username}.json")
                except:
                    print("\nError removing user file.")
                    return

                self.users_database.drop(self.userid, inplace=True)
                self.export_data(f2=False)

                print("\nAccount deleted successfully.")
                sys.exit()

            else:
                print("\nCancelling delete account command.")
        else:
            print("\nWrong password entered.")

    def export_data(self, d21=None, d22=None, f1=True, f2=True):
        """
        - Allows for updating the database files quickly
        - Users data file is exported (f1)
        - d21 and d22 are userstats and userdata pandas dataframes by default
        - d21 and d22 are zipped and exported to user's individual datafile (f2)
        - f1 and f2 can be set to true (default) or false depending on which is to be exported

        """

        if d21 is None:
            d21 = self.userstats

        if d22 is None:
            # a copy is made so as to not alter the database in use
            d22 = self.userdata.copy()

            # formatting the userdata, converting datetime objects into string
            d22["Start Time"] = d22["Start Time"].astype(str)
            d22["Deadline"] = d22["Deadline"].astype(str)
            d22["Completed On"] = d22["Completed On"].astype(str)

        if f1:
            # if the users data file is to be exported
            try:
                with open(USERS_FILE, "w") as f:
                    self.users_database.to_csv(f, index=False)

            except:
                print("\nError saving users database file.")

        if f2:
            # if the userstats and userdata is to be
            try:
                with open(f"{DATABASE}/{self.username}.json", "w") as f:

                    json.dump({"userstats": d21, "userdata": d22.to_dict(orient="index")}, f, indent=4)

            except:
                print("\nError saving user datafile.")
                sys.exit()

    def custom_export(self, data):
        """
        - Allows exporting of data (pandas dataframe) to a target json datafile
        - User is asked the path of the file destination without extension
        """

        while True:

            destination = input("\nEnter the full file path (incl name without extension) or 'cancel' : ").strip()

            if destination.lower() == "cancel":
                return

            # extension is added to the destination specified by the user
            destination = destination + ".json"

            if os.path.exists(destination):
                # if a file already exists at the path, user is asked if they want to replace it

                print("\nA file already exists with this name, do you want to replace it?")

                ask = consent()
                if not ask:
                    continue

            try:

                with open(destination, "w") as f:
                    data = data.copy()

                    # try-except is used incase the data passed doesn't have these columns
                    # converts datetime objects into strings for export
                    try:
                        data["Start Time"] = data["Start Time"].astype(str)
                    except KeyError:
                        pass

                    try:
                        data["Deadline"] = data["Deadline"].astype(str)
                    except KeyError:
                        pass

                    try:
                        data["Completed On"] = data["Completed On"].astype(str)
                    except KeyError:
                        pass

                    json.dump(data.to_dict(orient="index"), f, indent=4)

                print(f"Data exported successfully - {destination}")
                return

            except PermissionError as E:
                print(E)

            except Exception as E:
                print(E)