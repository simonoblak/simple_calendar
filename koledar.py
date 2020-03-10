
import tkinter as tk
import tkinter.ttk as tkk
from koledar_utils import *

file_name = "holidays.txt"
light_blue = "#add8e6"

window_width = "400"
window_height = "320"

default_error_color = "red"
default_color = "black"
default_calendar_width = 5
default_width = 10


calendar_names = ([datetime.date(datetime.datetime.today().year, i, 1).strftime('%B') for i in range(1, 13)])
calendar_indexes = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

days_of_week = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
calendar_days = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}

holidays = []


def clear_calendar_view():
    for w in range(len(days_of_week) + 1):
        for d in range(len(days_of_week)):
            day = tk.Label(calendar_frame, text="", width=default_calendar_width, background=light_blue)
            day.grid(column=d, row=w + 1)


def get_label_color(year, month, day):
    if day != 0:
        # Check if Sunday
        if datetime.datetime.today().replace(year=year, month=month, day=day).weekday() == 6:
            return default_error_color
        # Check for holiday
        for date, repeating in holidays:
            if month == date.month and day == date.day and (repeating == 'r' or year == date.year):
                return default_error_color

    return default_color


def show_calendar(year_str=None, month=None):
    """
    Generates the calendar for a specific year and month. Year must be as String while month is as Integer
    :param year_str: default is None
    :param month: default is None
    """
    month = calendar_indexes[month_combobox.get()] if month is None else month
    year_str = year_input.get().strip() if year_str is None else year_str
    if year_str.startswith('-'):
        info_label.configure(text="Only positive years are allowed")
        return
    try:
        year = int(year_str)
        calendar = koledar.get_month(year, month)
        clear_calendar_view()
        for i in range(len(days_of_week)):
            day_label = tk.Label(calendar_frame, text=days_of_week[i], width=default_calendar_width, background=light_blue)
            day_label.grid(column=i, row=0)

        for w in range(len(calendar)):
            for d in range(len(calendar[w])):
                label_color = get_label_color(year, month, calendar[w][d])
                day_text = calendar[w][d] if calendar[w][d] != 0 else ""
                day = tk.Label(calendar_frame, text=day_text, width=default_calendar_width, background=light_blue, foreground=label_color)
                day.grid(column=d, row=w + 1)

        info_label.configure(text="")
    except ValueError:
        info_label.configure(text="Please insert only positive numbers between 1 and 9999", foreground=default_error_color)


def import_holidays():
    """
    Imports holidays into the calendar for the duration till the program closes.
    If any date is in wrong format then no dates will be imported.
    If a holiday is repeating then it has 'r' mark at the end of line.
    """
    global holidays
    date_list = []
    try:
        rows = [line.rstrip('\n') for line in open(file_name, 'r', encoding='utf8')]
    except FileNotFoundError:
        info_label.configure(text="File 'holidays.txt' is missing", foreground=default_error_color)
        return

    if len(rows) == 0:
        info_label.configure(text="File 'holidays.txt' is empty", foreground=default_error_color)
        return

    for row in rows:
        if row == "":
            continue

        error_message = koledar.validate_file_input(row)

        if error_message is not None:
            info_label.configure(text=error_message, foreground=default_error_color)
            return

        row_format = row.split(":")
        date_format, repeating = row_format

        day_str, month_str, year_str = date_format.split(".")

        year = int(year_str)
        month = int(month_str)
        day = int(day_str)

        date_list.append((datetime.date(year, month, day), repeating))

    # Only now we add the dates into holidays
    holidays += date_list
    show_calendar()
    info_label.configure(text="Import Successful", foreground="green")


def go_to_date():
    """
    Sets the month of the date inserted into the field
    """
    user_date = input_date.get().strip()
    error_message = koledar.validate_date_format(user_date)

    if error_message is not None:
        info_label.configure(text=error_message, foreground=default_error_color)
        return

    day, month, year = user_date.split(".")
    show_calendar(year, int(month))

    month_combobox.set(calendar_names[int(month) - 1])
    year_input.delete(0, tk.END)
    year_input.insert(tk.END, str(year))


koledar = KoledarUtils(days_of_week)
window = tk.Tk()
window.title("The Simple Calendar")
window.geometry(window_width + "x" + window_height)
window.configure(background=light_blue)

settings_frame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg=light_blue)
settings_frame.pack()
calendar_frame = tk.Frame(window, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg=light_blue)
calendar_frame.pack(side=tk.BOTTOM)

info_label = tk.Label(window, text="", background=light_blue)
info_label.place(relx=0.0, rely=1.0, anchor='sw')

# ---------------------------------------------------------------------------------------------
# ------------------------------------CALENDAR FUNCTIONS---------------------------------------
# ---------------------------------------------------------------------------------------------

month_frame = tk.Frame(settings_frame, bg=light_blue)
month_frame.pack()

month_label = tk.Label(month_frame, text="Month", anchor='w', bg=light_blue)
month_label.pack(side=tk.LEFT)

month_combobox = tkk.Combobox(month_frame, state='readonly', width=default_width)
month_combobox['values'] = calendar_names
month_combobox.current(datetime.datetime.today().month - 1)  # set the selected item
month_combobox.pack(side=tk.RIGHT)

year_frame = tk.Frame(settings_frame, bg=light_blue)
year_frame.pack()

year_label = tk.Label(year_frame, text="Year", anchor='w', bg=light_blue)
year_label.pack(side=tk.LEFT)

year_input = tk.Entry(year_frame, width=default_width)
year_input.insert(tk.END, str(datetime.datetime.today().year))
year_input.pack(side=tk.RIGHT)

functions_frame = tk.Frame(settings_frame, bg=light_blue)
functions_frame.pack()

import_button = tk.Button(functions_frame, text="Import holidays", command=import_holidays)
import_button.pack(side=tk.LEFT)

calendar_button = tk.Button(functions_frame, text="Get calendar", command=show_calendar)
calendar_button.pack(side=tk.RIGHT)


# ---------------------------------------------------------------------------------------------
# -----------------------------------GO TO DATE FUNCTIONS--------------------------------------
# ---------------------------------------------------------------------------------------------

date_frame = tk.Frame(settings_frame, bg=light_blue)
date_frame.pack()

date_label = tk.Label(date_frame, text="Date", bg=light_blue)
date_label.pack(side=tk.LEFT)

input_date = tk.Entry(date_frame, width=default_width)
input_date.pack(side=tk.RIGHT)

go_date_frame = tk.Frame(settings_frame, bg=light_blue)
go_date_frame.pack()

go_date = tk.Button(go_date_frame, text="Go to Date", command=go_to_date)
go_date.pack(side=tk.LEFT)

window.mainloop()
