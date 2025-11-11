from login import Login
from tasks import Tasks
from analyse import Analyse
import os


def main():
    """
    - Asking user to login/create new account
    - Importing/creating database file of the user
    - Presenting user with various features they can use:
      1. View Profile
      2. Quick View Tasks
      3. Detailed View Tasks
      4. Analyse Tasks
      5. Detailed Analyse Tasks
      6. Add a Task
      7. Edit a Task
      8. Delete a Task
      9. Change Username
      10. Change Password
      11. Delete Account
      0. Exit
    """

    os.system("cls")

    # prompts user to login/signup and loads database
    user = Login()

    tasks = Tasks(user)
    analyse = Analyse(user)

    # options which user can use
    print_options = "\n 1. View Profile \n 2. Quick View Tasks \n 3. Detailed View Tasks \n 4. Analyse Tasks \n 5. Detailed Analyse Tasks \n 6. Add a Task \n 7. Edit a Task \n 8. Delete a Task \n 9. Change Username \n 10. Change Password \n 11. Delete Account \n 0. Exit"

    print("\nHere are all the features you can use :")
    print(print_options)

    # loop allows user to run the program unlimited times without having to log-in each time
    while True:

        # asks user to select option code from the menu, or 'x' to view the option menu
        choice = input("\nEnter the code of option (or 'x' to view options): ").strip().lower()

        match choice:

            # view the user's profile
            case "1":
                tasks.view_profile()

            # view task either by id or all tasks (automatically sorted) & option to export it
            case "2":
                tasks.quick_view_tasks()

            # allow users to give sort and filter instructions before viewing tasks & option to export it
            case "3":
                tasks.view_tasks()

            # allows users to view analysis on tasks & option to export it
            case "4":
                analyse.analyse()

            # allows users to view a detailed analysis & option to export it
            case "5":
                analyse.detailed_analysis()

            # allows user to add a task
            case "6":
                tasks.add_task()

            # allows user to edit a task and also mark it as completed
            case "7":
                tasks.edit_task()

            # allows user to permanently delete a task from database
            case "8":
                tasks.del_task()

            # allows user to change their username
            case "9":
                user.change_username()

            # allows user to change their password
            case "10":
                user.change_password()

            # allows user to permanently delete their account
            case "11":
                user.delete_user()

            # exiting the program
            case "0":
                return

            # printing the options menu
            case "x":
                print(print_options)

            # user enters an invalid code
            case _:
                print("\nEnter a valid option code")


if __name__ == "__main__":
    main()