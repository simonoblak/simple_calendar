import datetime


class KoledarUtils:
    def __init__(self, days_of_week):
        self.days_of_week = days_of_week

    def get_month(self, year=datetime.datetime.today().year, month=datetime.datetime.today().month):
        """
        Returns Nx7 grid od a month. Missing dates are filled with '0'
        Default values for get_month() method are the current year and month
        :param year: default value is current year
        :param month: default value is current month
        :return: Returns Nx7 grid od a month.
        """
        calendar = []
        first_day = datetime.datetime.today().replace(year=year, month=month, day=1).weekday()
        days_in_month = self.get_days_in_month(year, month)
        day_counter = 1
        calendar_full = False
        for w in range(len(self.days_of_week)):
            if day_counter > days_in_month:
                break
            calendar.append([])

            for d in range(len(self.days_of_week)):
                if day_counter > days_in_month:
                    calendar_full = True
                if w == 0 and d < first_day or calendar_full:
                    calendar[w].append(0)
                else:
                    calendar[w].append(day_counter)
                    day_counter += 1

        return calendar

    def get_days_in_month(self, year, month):
        end_of_year = 0
        next_year_month = 0
        if month == 12:
            end_of_year = 1
        else:
            next_year_month = month
        return (datetime.date(year + end_of_year, next_year_month + 1, 1) - datetime.date(year, month, 1)).days

    def validate_file_input(self, row):
        row_format = row.split(":")
        if len(row_format) != 2:
            return "Date must contain a date and if it is repeating ('r', 'n') separated with ':'"

        date_format, repeating = row_format

        if repeating != 'r' and repeating != 'n':
            return "Repeating date should only contain 'r' or 'n'"

        return self.validate_date_format(date_format)

    def validate_date_format(self, date_format):
        error_message = "Date '" + date_format + "' is not in correct format(DD.MM.YYYY)."
        date = date_format.split(".")
        if len(date) != 3:
            return error_message

        day_str, month_str, year_str = date
        if not year_str.isdigit() or not month_str.isdigit() or not day_str.isdigit():
            return error_message + "\nShould contain only positive numbers"

        year = int(year_str)
        month = int(month_str)
        day = int(day_str)

        if month < 1 or month > 12:
            return error_message + "\nMonth must be between 1 and 12"

        days_in_month = self.get_days_in_month(year, month)

        if day < 1 or day > days_in_month:
            return error_message + "\nDay must be between 1 and " + str(days_in_month)

        return None
