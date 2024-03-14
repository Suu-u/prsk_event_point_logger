import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates

BORDER_FILEPATH = "border.csv"
# BORDER_HEADER = ["date", "point"]
START_TIME = datetime.datetime.fromisoformat("2024-03-11 20:00:00.000000")
DAYS = 3
PER_DAY = [0, 7906376, 16120834, 29700222]

try:
    with open(BORDER_FILEPATH, "r") as file_object:
        reader = csv.reader(file_object)
        csv_list = list(reader)
        csv_list.pop(0) # remove header
except Exception as e:
    raise Exception(e)

x = [START_TIME]
end_time = START_TIME + datetime.timedelta(days=DAYS)
y_actual = [0]
for line in csv_list:
    x.append(datetime.datetime.fromisoformat((line[0])))
    y_actual.append(int(line[1]))
    
x_ticks = [START_TIME]
x_label = [START_TIME.strftime('%m-%d %H:%M')]
for i in range(1, DAYS+1):
    time = START_TIME + datetime.timedelta(days=i)
    x_ticks.append(time)
    x_label.append(time.strftime('%m-%d %H:%M'))


plt.figure()
plt.plot(x, y_actual, marker='.', color='limegreen')
plt.scatter(x_ticks, PER_DAY, marker='o', color='limegreen')
plt.xlim(START_TIME, end_time)
plt.ylim(0, 45000000)
plt.xticks(x_ticks, x_label)
plt.grid()
for i in range(1, DAYS+1):
    plt.text(x_ticks[i], PER_DAY[i], str(PER_DAY[i]), ha='right')
plt.show()
