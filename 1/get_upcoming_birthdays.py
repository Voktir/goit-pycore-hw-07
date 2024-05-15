
from datetime import datetime, timedelta
import re

def get_upcoming_birthdays(users):    

    today = datetime.today()
    print(today)
    b_users = []

    for user in users:
        user_year = str(datetime.strptime(user["birthday"], "%Y.%m.%d").date().year)
        year_now = str(today.year)
        user_data = str(datetime.strptime(user["birthday"], "%Y.%m.%d").date())
        print(user_data)
        last_birthday = re.sub(user_year, year_now, user_data)
        last_birthday_to_data = datetime.strptime(last_birthday, "%Y-%m-%d")
        print((last_birthday_to_data - today).days)
        if -1 <= (last_birthday_to_data - today).days < 6:

            match last_birthday_to_data.weekday():
                case 5:
                    last_birthday_to_data = last_birthday_to_data + timedelta(days=2)
                case 6:
                    last_birthday_to_data = last_birthday_to_data + timedelta(days=1)
       
            b_users.append({"name": user["name"], "congratulation_date": last_birthday_to_data.strftime("%Y.%m.%d")})
    return b_users

         



users = [
    {"name": "John Doe", "birthday": "1985.04.22"},
    {"name": "Jane Smith", "birthday": "1990.04.29"}
]

upcoming_birthdays = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming_birthdays)