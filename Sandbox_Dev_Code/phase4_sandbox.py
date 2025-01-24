from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# end_date = 
last_day = datetime.today() - timedelta(days=8)
end_date = datetime.today() + timedelta(days=8)
start_date = datetime.today() - timedelta(days=15)
print(f"Start Date: {start_date}")
print(f"End Date: {end_date}")
print(f"Last day: {last_day}, the day is {last_day.day}")

dates_init = []

for i in range(1, (last_day - start_date).days + 1):
    dates_init.append((start_date + timedelta(days=i)).strftime("%Y-%m-%d"))
    
print(dates_init)

df = pd.DataFrame({"Test": dates_init})

test = df["Test"]

print(df)
print("*****Going to the code to fix*****")
dates = df["Test"][0:]
print(dates)

for i in range(1, (end_date - start_date).days + 1):
    print(f"================={test}")
    dates = np.append(dates, [(last_day + timedelta(days=i)).strftime("%Y-%m-%d")])

print("*****This is with the additions*****")
print(dates)

print("**************ARGHGGHGHGHGHGHGHGHG**************")
print(datetime.today())
print(datetime.today().timestamp())
hmmm = "2025-01-23"
print(hmmm)
print(datetime.strptime(hmmm, "%Y-%m-%d"))

dates = ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", ]
print(dates)

df = pd.DataFrame({"Test": dates})

print(df)

print((last_day + timedelta(days=1)))
print((last_day + timedelta(days=1)))
print(datetime.strptime((last_day + timedelta(days=1)).strftime("%Y-%m-%d"), "%Y-%m-%d"))
