"""
- Contains several different helper functions
"""

from datetime import datetime


def consent(prompt="\nPlease enter 'Yes'/'No' : "):
    """
    - Asks user whether to confirm to decline
    - Helper function paired with another to confirm if user really wants to do something
    - prompt allows to change the default message
    """

    ask = input(prompt).strip().lower()

    if ask in ["y", "yes"]:
        return True

    elif ask in ["n", "no"]:
        return False

    else:
        # if neither yes/no is selected the function is looped
        return consent(prompt)


def to_time(prompt="Enter time (hh:mm am/pm) or enter for current : "):
    """
    - Allows conversion of time string in hh:mm am/pm format into datetime object
    - prompt allows to change the default message
    """

    time = input(prompt).strip().lower()

    # if user presses enter then current time is used
    if time == "":
        return datetime.today().replace(microsecond=0)

    # if user forgets to add a space between minute and am/pm allows automatic conversion instead of re-asking input
    try:
        return datetime.strptime(time, "%I:%M %p")

    except:
        try:
            return datetime.strptime(time, "%I:%M%p")

        except:
            # if user enters in neither of above two formats, function is looped
            print("\nPlease enter time in correct format (hh:mm am/pm)")
            return to_time(prompt)


def to_date(prompt="Enter date (dd/mm/yyyy) or enter for today : "):
    """
    - Allows conversion of date string in dd/mm/yyyy format into datetime object
    - prompt allows change of default message
    """

    date = input(prompt).strip().lower()

    # if user simply enters, current date is used
    if date == "":
        return datetime.today().replace(microsecond=0)

    # allows to convert into datetime regardless of if user enters in yyyy or just yy format instead of reasking input
    try:
        return datetime.strptime(date, "%d/%m/%y")

    except:
        try:
            return datetime.strptime(date, "%d/%m/%Y")

        except:
            # if user enters in neither of above two formats,function is looped
            print("\nPlease enter time in correct format (dd/mm/yy)")
            return to_date(prompt)


def comb_datetime(date, time):
    """
    - Allows combining date and time into one datetime object
    """
    return datetime.strptime(f"{date.date()} {time.time()}", "%Y-%m-%d %H:%M:%S")