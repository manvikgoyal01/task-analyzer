"""
- Handles task functions
- View profile : view profile/user stats
- Quick view tasks : Either a task id or all, pre-sorted (Completed on - descending, deadline - ascending)
- View tasks : allows user to filter and sort, and view tasks
- Add task : allows user to add task
- Edit task : allows user to edit task fields and mark as complete,outlier by task id
- Delete task : allows user to permanently delete the task from database by task id
"""

import pandas as pd
from datetime import datetime

from utils import to_time, to_date, comb_datetime, consent

# task categories and importance categories user can select from
taskcategories = ["Work", "Study", "Health", "Social", "Rest", "Personal", "Others"]
importancecategories = ["Low", "Medium", "High"]


class Tasks:

    def __init__(self, login_object):

        # database is stored centrally to update everywhere
        self.userdata = login_object.userdata
        self.userstats = login_object.userstats
        self.io = login_object

    def view_profile(self):
        """
        Shows user stats - total tasks, completed on, etc
        """
        print("\nProfile Stats :")

        for key, value in self.userstats.items():
            print(f"{key} - {value}")

    def quick_view_tasks(self):
        """
        - Shows user profile stats
        - Shows user task either by id or all tasks
        - Tasks are pre-sorted : completed on - descending, deadline - ascending
        - Asks user if they want to export the output data to a json file
        """

        self.view_profile()

        # if no tasks are in database, function is returned
        if len(self.userdata) == 0:
            print("You do not have any tasks added")
            return

        # asks for task id or all to view all tasks
        task_id = input("Enter the task id (or 'all') : ").strip().lower()

        if task_id == "all":

            # userdata copy is made so as to not affect centralised data
            userdata = self.userdata.copy()
            # userdata is sorted by default
            userdata = userdata.sort_values(by=["Completed On", "Deadline"], ascending=[False, True])

            print(userdata)

            # asks user if they want to export this data to an external json file
            print("\nDo you want to export this data to an external json file?")
            ask = consent()

            if ask:
                self.io.custom_export(userdata)
            return

        try:
            print(self.userdata.loc[task_id, :])

        except:
            # if task id entered is invalid
            print("\nInvalid task id entered")

    def view_tasks(self):
        """
        - Shows user profile stats
        - Asks user if they want to filter out certain task types and importances
        - Asks user to choose a primary and secondary sorters and asc/dsc for both
        - Asks user if they want to export the output data to a json file
        """

        # shows user profile/stats
        self.view_profile()

        # if no tasks are added to the database
        if len(self.userdata) == 0:
            print("\nYou do not have any tasks added")
            return

        # userdata copy is made to ensure centralised data is not affected
        userdata = self.userdata.copy()

        ask_imp = []
        ask_type = []

        # task importance and type in the database are added to list
        category_importance = self.userdata["Task Importance"].unique()
        category_tasks = self.userdata["Task Type"].unique()

        # shows the task importance user can filter IN
        print("\nYou can filter by task importance :")
        for i in category_importance:
            print(i, end=" ")

        while True:
            # user can add task importance to filter IN, seperated by ',' or all to view all
            ask_imp = input("\nEnter the fields to keep (seperated by ',' or 'all') : ")

            if ask_imp.lower().strip() == "all":
                ask_imp = category_importance
                break

            # a set is made to ensure duplicate values are removed
            ask_imp = ask_imp.split(",")
            ask_imp = set(j.strip().title() for j in ask_imp)
            ask_imp = list(ask_imp)

            # since for loop is user, esc is used to break the while loop
            esc = False

            # validates if all importances added are valid
            for j in ask_imp:

                if j not in category_importance:
                    print(f"\n{j} is not a valid field")
                    esc = True
                    break

            # if all importances are valid, esc is not set true and while loop breaks
            if not esc:
                break

        # shows task types to filter in
        print("\nYou can filter by task type :")
        for i in category_tasks:
            print(i, end=" ")

        while True:
            # user can enter task types seperated by ',' or 'all' to add all
            ask_type = input("\nEnter the fields to keep (seperated by ',' or 'all') : ")

            if ask_type.lower().strip() == "all":
                ask_type = category_tasks
                break

            # set is made to drop duplicate values
            ask_type = ask_type.split(",")
            ask_type = set(j.strip().title() for j in ask_type)
            ask_type = list(ask_type)

            # since for loop is used to validate types added, esc is used to break while loop
            esc = False

            # validates if all task types added by user is valid
            for j in ask_type:
                if j not in category_tasks:
                    print(f"\n{j} is not a valid field")
                    esc = True
                    break

            # if all task types are valid, esc is not set true and thus loop breaks
            if not esc:
                break

        # filters out the data as per user's input
        userdata = userdata[userdata["Task Importance"].isin(ask_imp)]
        userdata = userdata[userdata["Task Type"].isin(ask_type)]

        # presents user with sort options
        sort_options = {"1": "Task Type", "2": "Task Importance", "3": "Start Time", "4": "Deadline", "5": "Completed On", "6": "Task Name",}

        print("\nChoose the sorter : ")
        for i, j in sort_options.items():
            print(f" {i}.  {j}")

        # asks user their primary sorter preferance
        while True:
            primary_preferance = input("Enter the code of the primary sorter : ").strip()

            if primary_preferance not in sort_options.keys():
                print("\nInvalid sorter code")

            else:
                break

        # asks user if primary sorter should sort ascending/descending
        while True:
            primary_order = input("\nShould the primary sorter sort ascending or descending ('asc'/'dsc') : ").lower().strip()

            if primary_order in ["asc", "dsc"]:
                primary_order = True if primary_order == "asc" else False
                break

            else:
                print("\nPlease enter 'asc'/'dsc'")

        # asks user their secondary sorter preferance
        while True:
            secondary_preferance = input("\nEnter the code of the secondary sorter : ").strip()

            if secondary_preferance not in sort_options.keys():
                print("\nInvalid sorter code")

            # checks if secondary and primary preferance are same
            elif secondary_preferance == primary_preferance:
                print("\nPrimary and Secondary sorter cannot be the same")

            else:
                break

        # asks user if secondary sorter should sort ascending/descending
        while True:
            secondary_order = input("\nShould the secondary sorter sort ascending or descending ('asc'/'dsc') : ").lower().strip()

            if secondary_order in ["asc", "dsc"]:
                secondary_order = True if secondary_order == "asc" else False
                break

            else:
                print("\nPlease enter 'asc'/'dsc'")

        primary_preferance = sort_options[primary_preferance]
        secondary_preferance = sort_options[secondary_preferance]

        # sorts the data as per user's preferance
        userdata = userdata.sort_values(by=[primary_preferance, secondary_preferance], ascending=[primary_order, secondary_order])

        # asks user which tasks they want to view
        while True:
            print("\nYou can view task list in following ways :")
            print(" 1. All Tasks \n 2. Ongoing Tasks \n 3. Ongoing Late Tasks \n 4. Completed Tasks \n 5. On-Time Completed Tasks \n 6. Late Completed Tasks \n 7. Outlier Tasks \n 0. Exit")

            view_type = input("\nEnter the code of view type : ")

            match view_type:

                case "1":
                    # shows all tasks
                    output = userdata

                case "2":
                    # shows all ongoing tasks
                    output = userdata[userdata["Completed On"] == "Ongoing"]

                case "3":
                    # shows all ongoing + late tasks
                    output = userdata[userdata["Completed On"] == "Ongoing" & userdata["Deadline"] < datetime.today().replace(microsecond=0)]

                case "4":
                    # shows all completed tasks
                    output = userdata[userdata["Completed On"] != "Ongoing"]

                case "5":
                    # shows all tasks completed on time
                    output = userdata[userdata["Completed On"] != "Ongoing" & userdata["Was Late"] == False]

                case "6":
                    # shows all tasks completed late
                    output = userdata[userdata["Completed On"] != "Ongoing" & userdata["Was Late"] == True]

                case "7":
                    # shows all the outlier tasks
                    output = userdata[userdata["Is Outlier"] == True]

                case "0":
                    # if user wants to exit
                    return

                case _:
                    # if user enters a invalid code
                    print("\nEnter a valid code")
                    continue

            # if no tasks are found matching user's preferances
            if len(output) == 0:
                print("No such tasks found")

            else:
                print()
                print(output)

                # asks user if they want to export the data to an external file
                print("\nDo you want to export this data to an external json file?")
                ask = consent()

                if ask:
                    self.io.custom_export(output)

    def add_task(self):
        """
        - Allows user to add a task to the database
        - User can set start and deadline datetime
        - User can enter to use current datetime
        """

        # sets task id for the new task
        if len(self.userdata) < 1:
            taskid = 1
        else:
            taskid = max(self.userdata.index) + 1

        taskname = input("\nEnter name of the task : ").strip().capitalize()

        # shows task type categories user can select from
        while True:
            print("\nTask categories :")
            for i in taskcategories:
                print(f"{i} ", end="")

            tasktype = input("\nChoose the task type : ").strip().capitalize()

            # verifies if task type is valid
            if tasktype not in taskcategories:
                print("\nPlease choose a valid task type.")
                continue
            break

        # shows task importance categories user can select from
        while True:
            print("\nImportance Categories :")
            for i in importancecategories:
                print(f"{i} ", end="")

            importance = input("\nEnter the task importance : ").strip().capitalize()

            # verifies if task importance is valid
            if importance not in importancecategories:
                continue
            break

        # asks user to enter start date and time (or enter to use current)
        start_date = to_date("\nEnter start date (dd/mm/yy) or enter for today : ")
        start_time = to_time("\nEnter start time (hh:mm am/pm) or enter for current : ")
        start_datetime = comb_datetime(start_date, start_time)

        # asks user the deadline date and time (or enter to use current)
        while True:
            deadline_date = to_date("\nEnter deadline date (dd/mm/yy) or enter for today : ")
            deadline_time = to_time("\nEnter deadline time (hh:mm am/pm) or enter for current : ")
            deadline_datetime = comb_datetime(deadline_date, deadline_time)

            # checks if deadline is after start time
            if deadline_datetime >= start_datetime:
                break

            else:
                print("\nDeadline Date-Time cannot be older than Start Date-Time")

        self.userdata.loc[taskid, "Deadline"] = deadline_datetime

        # allows user to add notes for the task, or enter to skip
        notes = input("\nEnter notes for the task (optional) : ")

        # confirms if user wants to add the task
        print("\nYou are about to add a new task with details :")
        print(f" - Task Name : {taskname} \n - Task Type : {tasktype} \n - Importance : {importance} \n - Start Time : {start_datetime} \n - Deadline : {deadline_datetime} \n - Notes : {notes}")

        ask = consent()

        if ask:
            # if user agrees, task is added to database and userstats is updated
            self.userdata.loc[taskid, :] = [taskname, tasktype, importance, start_datetime, deadline_datetime, "Ongoing", pd.NA, pd.NA, False, notes]

            self.userstats["Ongoing Tasks"] += 1
            self.userstats["Total Tasks"] += 1

            # udpated the userdata and userstats in the datafile
            self.io.export_data()

            print(f"\nTask added successfully with ID - {taskid}")
            print("Use edit task command to mark as complete or edit.")

        else:
            # if user does not agree to add the task
            print("Cancelling add task command.")
            return

    def edit_task(self):
        """
        - Allows user to edit task name, type, importance, start/deadline datetime, notes
        - Allows user to mark a task as outlier
        - Allows user to mark a task as completed and set completed datetime (or enter for current)
        """

        # if no tasks are in the database
        if len(self.userdata) == 0:
            print("You do not have any tasks added")
            return

        taskid = input("\nEnter task id : ").strip()

        # validates task id entered
        if taskid not in self.userdata.index.astype(str):
            print("\nTask not found")
            return

        taskid = int(taskid)

        # shows the current field values of the task
        print("\nTask Info :")
        print(self.userdata.loc[taskid, :])

        # shows user which field they can edit
        print("\nYou can edit the following fields : ")
        print(" 1. Task Name \n 2. Task Type \n 3. Task Importance \n 4. Start time \n 5. Deadline \n 6. Completed On \n 7. Is Outlier \n 8. Notes \n 0. Save & Exit")

        while True:

            choice = input("\nEnter the code of field to edit : ").strip()

            match choice:

                case "1":
                    # allows user to change task name
                    taskname = input("\nEnter new name of the task : ").strip().capitalize()
                    self.userdata.loc[taskid, "Task Name"] = taskname

                case "2":
                    # allows user to change task type
                    while True:
                        print("\nTask categories :")

                        # prints task categories user can choose from
                        for i in taskcategories:
                            print(f"{i} ", end="")

                        tasktype = input("\nChoose the task type : ").strip().capitalize()

                        # validates if task type is valid
                        if tasktype not in taskcategories:
                            print("\nPlease choose a valid task type.")
                            continue
                        break

                    self.userdata.loc[taskid, "Task Type"] = tasktype

                case "3":
                    # allows user to change task importance
                    while True:
                        print("\nImportance Categories :")

                        # prints all importance categories available
                        for i in importancecategories:
                            print(f"{i} ", end="")

                        importance = input("\nEnter the task importance : ").strip().capitalize()

                        # checks if importance entered is valid
                        if importance not in importancecategories:
                            continue
                        break

                    self.userdata.loc[taskid, "Task Importance"] = importance

                case "4":
                    # allows user to change start date and time (or enter for current)
                    while True:

                        start_date = to_date("\nEnter new start date (dd/mm/yy) or enter for today : ")
                        start_time = to_time("\nEnter new start time (hh:mm am/pm) or enter for current : ")
                        start_datetime = comb_datetime(start_date, start_time)

                        # validates if start time is before deadline
                        if start_datetime <= self.userdata.loc[taskid, "Deadline"]:

                            # checks if task is completed
                            if self.userdata.loc[taskid, "Completed On"] != "Ongoing":

                                # if task is completed, checks if start time is before complesion date
                                if (start_datetime <= self.userdata.loc[taskid, "Completed On"]):
                                    break

                                else:
                                    # if start time is younger than completion date
                                    print("\nStart date must be older than completion date")
                            else:
                                break
                        else:
                            # if start time is younger than deadline
                            print("\nStart date must be older than deadline")

                    self.userdata.loc[taskid, "Start Time"] = start_datetime
                    self.userdata.loc[taskid, "Duration"] = str(self.userdata.loc[taskid, "Completed On"] - self.userdata.loc[taskid, "Start Time"])

                case "5":
                    # allows user to edit the deadline
                    while True:

                        deadline_date = to_date("\nEnter new deadline date (dd/mm/yy) or enter for today : ")
                        deadline_time = to_time("\nEnter new deadline time (hh:mm am/pm) or enter for current : ")
                        deadline_datetime = comb_datetime(deadline_date, deadline_time)

                        # checks if deadline is after start time
                        if deadline_datetime >= self.userdata.loc[taskid, "Start Time"]:
                            break
                        else:
                            print("\nDeadline Date-Time cannot be older than Start Date-Time")

                    self.userdata.loc[taskid, "Deadline"] = deadline_datetime

                    # changes the userstats and userdata depending on if the update changed the was late statud
                    if self.userdata.loc[taskid, "Completed On"] != "Ongoing":

                        # checks if completion was before the deadline
                        if (self.userdata.loc[taskid, "Completed On"] <= deadline_datetime):

                            # if deadline caused change of was late status from true to false
                            if self.userdata.loc[taskid, "Was Late"]:
                                self.userstats["Late Tasks"] -= 1
                                self.userdata.loc[taskid, "Was Late"] = False

                        # if completion was after the deadline
                        else:
                            # if deadline caused change of was late status from false to true
                            if not self.userdata.loc[taskid, "Was Late"]:
                                self.userstats["Late Tasks"] += 1
                                self.userdata.loc[taskid, "Was Late"] = True

                    # updated on time rate userstat
                    try:
                        self.userstats["On-Time Rate (%)"] = ((self.userstats["Total Tasks"] - self.userstats["Late Tasks"])* 100 / self.userstats["Total Tasks"])

                    except ZeroDivisionError:
                        self.userstats["On-Time Rate (%)"] = 0

                case "6":
                    # allows user to change completion status and set datetime

                    print("Has the task been completed?")
                    ask = consent()

                    if ask:
                        while True:

                            # if task has been completed, asks for completion date and time, or enter for current
                            completed_date = to_date("\nEnter task completed date (dd/mm/yy) or enter for today : ")
                            completed_time = to_time("\nEnter task completed time (hh:mm am/pm) or enter for current : ")
                            completed_datetime = comb_datetime(completed_date, completed_time)

                            # checks if completion datetime is after start time
                            if (completed_datetime >= self.userdata.loc[taskid, "Start Time"]):
                                break
                            else:
                                print("\nCompleted Date-Time cannot be older than Start Date-Time")

                        # if orignal completed status was ongoing, updates the userstats and userdata
                        if self.userdata.loc[taskid, "Completed On"] == "Ongoing":
                            self.userstats["Completed Tasks"] += 1
                            self.userstats["Ongoing Tasks"] -= 1
                        self.userdata.loc[taskid, "Completed On"] = completed_datetime

                        # checks if the completion is after deadline
                        if (self.userdata.loc[taskid, "Completed On"] > self.userdata.loc[taskid, "Deadline"]):

                            # if task is late and orignal status was not True, userstats are updated
                            if str(self.userdata.loc[taskid, "Was Late"]) != str(True):
                                self.userdata.loc[taskid, "Was Late"] = True
                                self.userstats["Late Tasks"] += 1

                        # if completion was before deadline
                        else:

                            # if task was early but was late status was not set to false
                            if str(self.userdata.loc[taskid, "Was Late"]) != str(False):
                                self.userdata.loc[taskid, "Was Late"] = False
                                self.userstats["Late Tasks"] -= 1

                        # updates the task duration
                        self.userdata.loc[taskid, "Duration"] = str(self.userdata.loc[taskid, "Completed On"] - self.userdata.loc[taskid, "Start Time"])

                        # update user on time rate userstat
                        try:
                            self.userstats["On-Time Rate (%)"] = ((self.userstats["Completed Tasks"] - self.userstats["Late Tasks"])* 100 / self.userstats["Total Tasks"])
                        except ZeroDivisionError:
                            self.userstats["On-Time Rate (%)"] = 0

                    else:
                        # if completion status of task if ongoing

                        # if orignal completion status was completed, userstats are updated
                        if self.userdata.loc[taskid, "Completed On"] != "Ongoing":

                            self.userstats["Ongoing Tasks"] += 1
                            self.userstats["Completed Tasks"] -= 1
                            if str(self.userdata.loc[taskid, "Was Late"]) == str(True):
                                self.userstats["Late Tasks"] -= 1

                            # was late status is set to NA
                            self.userdata.loc[taskid, "Was Late"] = pd.NA

                        # on-completion rate userstat is updated
                        try:
                            self.userstats["On-Time Rate (%)"] = (
                                (self.userstats["Completed Tasks"] - self.userstats["Late Tasks"])* 100 / self.userstats["Total Tasks"])
                        except ZeroDivisionError:
                            self.userstats["On-Time Rate (%)"] = 0

                        # completion status is set to ongoing
                        self.userdata.loc[taskid, "Completed On"] = "Ongoing"

                case "7":
                    # allows user to set outlier status to true/false
                    # if true, this task wont be used for analysis

                    print("\nIs this task an outlier (won't count to stats)?")
                    ask = consent()

                    if ask:
                        outlier = True
                    else:
                        outlier = False

                    self.userdata.loc[taskid, "Is Outlier"] = outlier

                case "8":
                    # allows user to edit the notes

                    notes = input("\nEnter new notes for the task (optional) : ")
                    self.userdata.loc[taskid, "Notes"] = notes

                case "0":
                    # exits and saved the changes
                    self.io.export_data()

                    # prints the updated task info
                    print("\nUpdated Task Info :")
                    print(self.userdata.loc[taskid, :])
                    return

                case _:
                    # if user enters an invalid code
                    print("\nEnter a valid code")

    def del_task(self):
        """
        - Allows user to delete the task from the database
        - Updates userstats accordingly
        """

        # if no tasks are in the database
        if len(self.userdata) == 0:
            print("You do not have any tasks added")
            return

        taskid = input("\nEnter task id : ").strip()

        # validates the task id
        if taskid not in self.userdata.index.astype(str):
            print("\nTask not found")
            return

        taskid = int(taskid)

        # confirms if the user wants to delete the task and prints task details
        print("\nAre you sure you want to permanently delete this task from the database?")
        print(self.userdata.loc[taskid, :])
        ask = consent()

        if ask:
            # if user wants to delete the task
            # userstats are updated

            self.userstats["Total Tasks"] -= 1

            # checks if task was ongoing and if yes, reduces it by one
            if self.userdata.loc[taskid, "Completed On"] == "Ongoing":
                self.userstats["Ongoing Tasks"] -= 1

            else:
                # if task was completed, reduces completed tasks by one
                self.userstats["Completed Tasks"] -= 1

                # if task was completed late, reduces it by one
                if self.userdata.loc[taskid, "Was Late"]:
                    self.userstats["Late Tasks"] -= 1

            # updates on time rate userstat
            try:
                self.userstats["On-Time Rate (%)"] = ((self.userstats["Completed Tasks"] - self.userstats["Late Tasks"])* 100 / self.userstats["Total Tasks"])
            except ZeroDivisionError:
                self.userstats["On-Time Rate (%)"] = 0

            # removes the tasks and saves the data to the datafile
            self.userdata.drop(taskid, inplace=True)
            self.io.export_data()
            print("\nTask deleted successfully")

        else:
            # if user does not want to delete the task
            print("\nCancelling delete task command.")