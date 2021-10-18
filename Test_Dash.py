import datetime
import time
# date_format = "%m/%d/%Y"

# now = datetime.now()
# dt_string = now.strftime("%m/%d/%Y %H:%M:%S").split(" ")[0]
t = time.localtime()
current_time = time.strftime("%H:%M:%S",t)
start_date = datetime.date.today()
end_date = datetime.date(2021,10,19)

print(current_time)
print(int((end_date-start_date).days/7))