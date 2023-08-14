import json, datetime
from plyer import notification

def addBirthday(birthday_details):
    name = input("Enter name: ")
    day_month = input("Enter birthday (dd-mm): ")
    birth_year = int(input("Enter birth year: "))

    birthday_details.append({
        "name": name,
        "birthday": day_month,
        "year": birth_year
    })

    saveBirthday(birthday_details)
    notification_title = "Birthday Reminder"
    notification_message = f"Added {name}'s birthday on {day_month}."
    notification.notify(title=notification_title, message=notification_message)

def calculate_age(birth_year, birth_day, birth_month):
    today = datetime.date.today()
    current_year = today.year

    if (birth_month, birth_day) > (today.month, today.day):
        age = current_year - birth_year - 1
    else:
        age = current_year - birth_year

    return age

def notify_upcoming_birthdays(birthday_details):
    today = datetime.date.today()
    for entry in birthday_details:
        name = entry["name"]
        day_month = entry["birthday"]
        birth_year = entry["year"]
        birth_day, birth_month = map(int, day_month.split("-"))

        days_remaining = (datetime.date(today.year, birth_month, birth_day) - today).days

        if 0 <= days_remaining <= 7:
            age = calculate_age(birth_year, birth_day, birth_month)
            notification_title = "Upcoming Birthday Reminder"
            notification_message = f"{name}'s {age}th birthday is in {days_remaining} days! Don't forget to wish them."
            notification.notify(title=notification_title, message=notification_message)

def updateBirthday(birthday_details):
    name_to_update = input("Enter the name to update the birthday: ")

    found = False
    for entry in birthday_details:
        if entry["name"] == name_to_update:
            day_month = input("Enter the updated birthday (dd-mm): ")
            birth_year = int(input("Enter birth year: "))
            entry["birthday"] = day_month
            entry["year"] = birth_year

            found = True
            break

    if not found:
        print(f"{name_to_update} not found in the birthday details.")
    else:
        saveBirthday(birthday_details)
        notification_title = "Birthday Reminder"
        notification_message = f"Updated {name_to_update}'s birthday."
        notification.notify(title=notification_title, message=notification_message)

def deleteBirthday(birthday_details):
    name_to_delete = input("Enter the name of the person whose birthday you want to delete: ")

    # Remove the entry with the specified name
    birthday_details = [entry for entry in birthday_details if entry["name"] != name_to_delete]

    # Save the updated birthday details to the file
    saveBirthday(birthday_details)
    notification_title = "Birthday Reminder"
    notification_message = f"{name_to_delete}'s birthday has been deleted from the birthday details."
    notification.notify(title=notification_title, message=notification_message)

def user_input(user_choice, birthday_details):
    if user_choice == "a" or user_choice == "A":
        addBirthday(birthday_details)
    elif user_choice == "u" or user_choice == "U":
        updateBirthday(birthday_details)
    elif user_choice == "d" or user_choice == "D":
        deleteBirthday(birthday_details)
    elif user_choice == "n" or user_choice == "N":
        notify_upcoming_birthdays(birthday_details)
    elif user_choice == "c" or user_choice == "C":
        calculate_age_of_person(birthday_details)

def input_err():
    user_choice = input("Please choose a valid option\nA - Add Birthday\nU - Update Birthday\nD - Delete Birthday\nN - Notify Upcoming Birthdays\nC - Calculate Age\nE - Exit\n")
    user_input(user_choice, birthday_details)

def calculate_age_of_person(birthday_details):
    name_to_calculate_age = input("Enter the name to calculate the age: ")

    for entry in birthday_details:
        if entry["name"] == name_to_calculate_age:
            birth_year = entry["year"]
            birth_day, birth_month = map(int, entry["birthday"].split("-"))

            age = calculate_age(birth_year, birth_day, birth_month)
            print(f"{name_to_calculate_age}'s age is: {age} years")
            return

    print(f"{name_to_calculate_age} not found in the birthday details.")

def loadBirthday():
    try:
        with open("birthdays.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def saveBirthday(birthday_details):
    with open("birthdays.json", "w") as file:
        json.dump(birthday_details, file, indent=2)

if __name__ == "__main__":
    birthday_details = loadBirthday()

    while True:
        user_choice = input("What would you like to do?\nA - Add Birthday\nU - Update Birthday\nD - Delete Birthday\nN - Notify Upcoming Birthdays\nC - Calculate Age\nE - Exit\n")
        if user_choice == "e" or user_choice == "E":
            break  # Exit the loop and end the program
        elif user_choice == "n" or user_choice == "N":
            notify_upcoming_birthdays(birthday_details)
        else:
            try:
                user_input(user_choice, birthday_details)
            except KeyboardInterrupt:
                print("\nExiting...")
                break  # Exit the loop if the user presses Ctrl+C
            else:
                input_err()

    # Save the updated birthday details to the file before exiting
    saveBirthday(birthday_details)