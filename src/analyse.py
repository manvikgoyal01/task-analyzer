"""
- Analysis and display the task data
- Outlier tasks are ignored
- Analyse asks user for task type and importance to analyse (select multiple)
- Detailed analysis displays the analysis of each task+importance combination as well
- Asks user if they want to export the analysis to a json file
"""

import pandas as pd
from utils import consent
from datetime import timedelta


class Analyse:

    def __init__(self, login_object):
        self.login_object = login_object
        self.userdata = login_object.userdata
        self.userstats = login_object.userstats

    def analyse(self):
        """
        - Asks user for task type + importance (multiple or 'all') to analyse
        - Analyses the given in following fields:
            - No of tasks
            - No of tasks in other category (ie if task type then shows no of tasks of that type in different importances)
            - Tasks completed on time
            - Late completed tasks
            - On time rate
            - Consistency (standard deviation btw deadline and completion)
            - Average duration
            - Average early completion time
            - Average late completion time

        - The selected types and importances are added to the asked_combo dict
        - Then the database is iterrated and analysis is given for all the selected importances and then types
        - The user is given the option to export the output to an external json file
        """

        ask_imp = []
        ask_type = []

        # adds unique types and importance to lists
        category_importance = self.userdata["Task Importance"].unique()
        category_tasks = self.userdata["Task Type"].unique()

        # asks user if they want analysis on type/importance or both
        print("\nDo you want analysis based on :")
        print("\n 1. Task Importance \n 2. Task Type \n 3. Both")

        while True:
            ask_cat = input("Enter the code of analysis type : ").strip()

            if ask_cat not in ["1", "2", "3"]:
                print("\nEnter a valid category code")

            else:
                break

        # if user enters importance or both
        if ask_cat != "2":
            print()

            # displays all importance categories
            for i in category_importance:
                print(i, end=" ")

            # asks user to enter importance seperated by ',' or all
            while True:
                ask_imp = input("\nEnter the fields you want to analyse (seperated by ',' or 'all') : ")

                if ask_imp.lower().strip() == "all":
                    ask_imp = category_importance
                    break

                # converted to set to drop duplicates
                ask_imp = ask_imp.split(",")
                ask_imp = set(j.strip().title() for j in ask_imp)
                ask_imp = list(ask_imp)

                # since for is used to validate importances, esc is used to break while loop
                esc = False

                for j in ask_imp:
                    if j not in category_importance:

                        print(f"\n{j} is not a valid category")
                        esc = True
                        break

                # if all importances are valid, esc is never set true, thus loop breaks
                if not esc:
                    break

        # if user chooses type or both
        if ask_cat != "1":
            print()

            # prints all task types in database
            for i in category_tasks:
                print(i, end=" ")

            # asks user to enter types seperated by ',' or all
            while True:
                ask_type = input("\nEnter the fields you want to analyse (seperated by ',' or 'all') : ")

                if ask_type.lower().strip() == "all":
                    ask_type = category_tasks
                    break

                # converted to set to drop duplicates
                ask_type = ask_type.split(",")
                ask_type = set(j.strip().title() for j in ask_type)
                ask_type = list(ask_type)

                # since for is used to validate types, esc is used to break while loop
                esc = False
                for j in ask_type:
                    if j not in category_tasks:

                        print(f"\n{j} is not a valid category")
                        esc = True
                        break

                # if all types are valid, esc is never set true, thus loop breaks
                if not esc:
                    break

        # asked types and importances are added to the dict
        asked_combo = {"Task Importance": ask_imp, "Task Type": ask_type}

        # copy is made of centralised userdata
        # outliers are dropped
        userdata = self.userdata.copy()
        userdata.drop(userdata[userdata["Is Outlier"] == True].index, inplace=True)

        data = pd.DataFrame(columns=["Category", "Field", "Parameter", "Value"])

        # the for loop gives the task_category : asked_values (eg: cattitle - task importance, catvalues - [medium,hard])
        for index, (cattitle, catvalues) in enumerate(asked_combo.items()):

            # this for loop picks value from the catvalues (eg : value - medium)
            for value in catvalues:

                duration = 0
                exp_duration = 0
                early = 0
                late = 0
                no_early = 0
                no_late = 0
                std_dev_list = []

                # userdata where only rows where cattitle = value is there
                filtered_userdata = userdata[userdata[cattitle] == value]
                # filtered userdata where tasks are completed
                completed_filtered_userdata = filtered_userdata[filtered_userdata["Completed On"] != "Ongoing"]

                # length of completed filtered userdata is checked to prevent errors due to zero tasks found
                if len(completed_filtered_userdata) > 0:

                    # iterates row index in completed filtered userdata
                    for index in completed_filtered_userdata.index:

                        delta = (completed_filtered_userdata.loc[index, "Completed On"] - completed_filtered_userdata.loc[index, "Start Time"])
                        exp_delta = (completed_filtered_userdata.loc[index, "Deadline"] - completed_filtered_userdata.loc[index, "Start Time"])

                        duration += delta.total_seconds()
                        exp_duration += exp_delta.total_seconds()

                        was_late = completed_filtered_userdata.loc[index, "Was Late"]

                        comp_dead_delta = (completed_filtered_userdata.loc[index, "Completed On"] - completed_filtered_userdata.loc[index, "Deadline"]).total_seconds()
                        std_dev_list.append(comp_dead_delta)

                        if was_late:
                            no_late += 1
                            late += comp_dead_delta
                        else:
                            no_early += 1
                            early -= comp_dead_delta

                    avg_duration = timedelta(seconds=(duration / len(completed_filtered_userdata)))
                    avg_exp_duration = timedelta(seconds=(exp_duration / len(completed_filtered_userdata)))

                    # try except is used to prevent errors due to zero such tasks
                    try:
                        avg_late = timedelta(seconds=late / no_late)
                    except:
                        avg_late = timedelta(seconds=0)

                    try:
                        avg_early = timedelta(seconds=early / no_early)
                    except:
                        avg_early = timedelta(seconds=0)

                    # since std dev cannot run on only one value
                    if len(std_dev_list) > 1:
                        std_dev = timedelta(seconds=(pd.Series(std_dev_list).std()))
                        std_dev -= timedelta(microseconds=std_dev.microseconds)
                    else:
                        std_dev = timedelta(seconds=0)

                    # helps assignment of the opposite category and its values (all unique not asked)
                    # helps in calculation of no of tasks of each asked category + opposite category values
                    if cattitle == "Task Importance":
                        cat = "Task Type"
                        catvals = category_tasks

                    else:
                        cat = "Task Importance"
                        catvals = category_importance

                    # adds an empty row for visual purposes
                    data.loc[len(data), :] = ["", "", "", ""]
                    data.loc[len(data), :] = [cattitle, value, "No. of Tasks", len(filtered_userdata)]

                    # number of tasks which match current type + value and opposite type + value
                    # eg if current cattitle is task type, value is work, then cat = task importance, catvals = [medium,hard], q will be medium
                    for q in catvals:
                        data.loc[len(data), :] = [cattitle, value, f"No of {q} Tasks", len(filtered_userdata[filtered_userdata[cat] == q])]

                    on_time = len(
                        completed_filtered_userdata[completed_filtered_userdata["Was Late"] == False])
                    data.loc[len(data), :] = [cattitle, value, "On-Time Tasks", on_time]
                    data.loc[len(data), :] = [cattitle, value, "Late Tasks", len(completed_filtered_userdata[completed_filtered_userdata["Was Late"] == True])]
                    data.loc[len(data), :] = [cattitle, value, "On-Time (%)", on_time * 100 / len(completed_filtered_userdata)]
                    data.loc[len(data), :] = [cattitle, value, "Consistency (Std)", std_dev]
                    data.loc[len(data), :] = [cattitle, value, "Average Duration", avg_duration]
                    data.loc[len(data), :] = [cattitle, value, "Average Expected Duration", avg_exp_duration]
                    data.loc[len(data), :] = [cattitle, value, "Average Early Completion", avg_early]
                    data.loc[len(data), :] = [cattitle, value, "Average Late Completion", avg_late]

        print(data)

        # asks user if they want to export the analysis to an external json file
        print("\nDo you want to export this data to an external json file?")
        ask = consent()

        if ask:
            self.login_object.custom_export(data)

    def detailed_analysis(self):
        """
        - Runs on almost the same exact logic as analysis()
        - Except, here the analysis is done for all type + importance combinations in the database instead
        """

        category_importance = self.userdata["Task Importance"].unique()
        category_tasks = self.userdata["Task Type"].unique()
        category_combo = {"Task Importance": category_importance, "Task Type": category_tasks}

        userdata = self.userdata.copy()
        userdata.drop(userdata[userdata["Is Outlier"] == True].index, inplace=True)

        data = pd.DataFrame(columns=["Category", "Primary Field", "Secondary Field", "Parameter", "Value"])

        # the for loop gives the task_category : asked_values (eg: cattitle - task importance, catvalues - [medium,hard])
        for index, (cattitle, catvalues) in enumerate(category_combo.items()):

            # helps in setting in opposite/secondary category
            if index == 0:
                seccat = "Task Type"
            else:
                seccat = "Task Importance"

            # this for loop picks value from the catvalues (eg : value - medium)
            for value in catvalues:

                # this loop chooses a value from the secondary category values (eg medium from [easy,medium,hard])
                for seccatvalue in category_combo[seccat]:

                    duration = 0
                    exp_duration = 0
                    early = 0
                    late = 0
                    no_early = 0
                    no_late = 0
                    std_dev_list = []

                    # userdata where only rows which match both primary and secondary categories' chosen (by the loop) values
                    filtered_userdata = userdata[userdata[cattitle] == value]
                    filtered_userdata = filtered_userdata[filtered_userdata[seccat] == seccatvalue]
                    # filtered data where only completed tasks are present
                    completed_filtered_userdata = filtered_userdata[filtered_userdata["Completed On"] != "Ongoing"]

                    # to prevent any errors if zero such tasks are found
                    if len(completed_filtered_userdata) > 0:

                        # iterates over the row index in completed filtered data
                        for index in completed_filtered_userdata.index:

                            delta = (completed_filtered_userdata.loc[index, "Completed On"] - completed_filtered_userdata.loc[index, "Start Time"])
                            exp_delta = (completed_filtered_userdata.loc[index, "Deadline"] - completed_filtered_userdata.loc[index, "Start Time"])

                            duration += delta.total_seconds()
                            exp_duration += exp_delta.total_seconds()

                            was_late = completed_filtered_userdata.loc[index, "Was Late"]

                            comp_dead_delta = (completed_filtered_userdata.loc[index, "Completed On"] - completed_filtered_userdata.loc[index, "Deadline"]).total_seconds()
                            std_dev_list.append(comp_dead_delta)

                            if was_late:
                                no_late += 1
                                late += comp_dead_delta
                            else:
                                no_early += 1
                                early -= comp_dead_delta

                        avg_duration = timedelta(seconds=(duration / len(completed_filtered_userdata)))
                        avg_exp_duration = timedelta(seconds=(exp_duration / len(completed_filtered_userdata)))

                        # try except is used to prevent errors due to zero such tasks
                        try:
                            avg_late = timedelta(seconds=late / no_late)
                        except:
                            avg_late = timedelta(seconds=0)

                        try:
                            avg_early = timedelta(seconds=early / no_early)
                        except:
                            avg_early = timedelta(seconds=0)

                        # since std dev cannot run on only one value
                        if len(std_dev_list) > 1:
                            std_dev = timedelta(seconds=(pd.Series(std_dev_list).std()))
                            std_dev -= timedelta(microseconds=std_dev.microseconds)
                        else:
                            std_dev = timedelta(seconds=0)

                        # adds an empty row for visual purposes
                        data.loc[len(data), :] = ["", "", "", "", ""]
                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "No. of Tasks", len(filtered_userdata)]

                        on_time = len(completed_filtered_userdata[completed_filtered_userdata["Was Late"] == False])

                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "On-Time Tasks", on_time]
                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "Late Tasks", len(completed_filtered_userdata[completed_filtered_userdata["Was Late"] == True])]
                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "On-Time (%)", on_time * 100 / len(completed_filtered_userdata)]
                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "Consistency (Std)", std_dev]
                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "Average Duration", avg_duration]
                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "Average Expected Duration", avg_exp_duration]
                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "Average Early Completion", avg_early,]
                        data.loc[len(data), :] = [cattitle, value, seccatvalue, "Average Late Completion", avg_late]

        print(data)

        # asks user if they want to export analysis to external json file
        print("\nDo you want to export this data to an external json file?")
        ask = consent()

        if ask:
            self.login_object.custom_export(data)
