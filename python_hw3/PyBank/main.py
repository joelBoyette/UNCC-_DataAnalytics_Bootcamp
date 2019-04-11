import os
import csv


revenue = []
month = []
day=[]
sum_revenue = 0
count_months = 0
chg_calc = 0
chg_months = []
avgChg = 0
max_chg_num = float(0)
max_chg_month = ""
max_chg_day = 0
min_chg_num = float(0)
min_chg_month = ""
min_chg_day = 0


budget1_csv_path = os.path.join("budget_data_2.csv")

with open(budget1_csv_path, newline="") as csvfile:
    
    csvreader = csv.reader(csvfile, delimiter=",")
    csv_header = next(csvreader)
    
    for row in csvreader:
        #seperate full date into month and day
        split_date = row[0].split("-")
        #get month to its own list
        month.append(split_date[0])
        #get day to its own list
        day.append(split_date[1])
        #assign revenue to its own list
        revenue.append(int(row[1]))

#sum the revenue and count the number of months
for x in range(len(revenue)):
    sum_revenue += revenue[x]
    count_months += 1

# calculate the change between months
for x in range(len(revenue)-1):
    chg_calc = revenue[x+1] - (revenue[x])
    chg_months.append(chg_calc)

# calculate the average change between months
avgChg = sum(chg_months) / (count_months-1)

# find the max monthly change
for x in range(len(chg_months)):
    if chg_months[x] > max_chg_num:
        max_chg_num = chg_months[x]
        max_chg_month = month[x+1]
        max_chg_day = day[x+1]

# find the min monthly change   
for x in range(len(chg_months)):
    if chg_months[x] < min_chg_num:
        min_chg_num = chg_months[x]
        min_chg_month = month[x+1]
        min_chg_day = day[x+1]        

print("Financial Analysis")
print("---------------------------")
print("Total Months: " + str(count_months))
print("Total Revenue: " + "$"+ str(sum_revenue))
print("Average Revenue Change: " + str(int(avgChg)))
print("Greatest Increase in Revenue: " + max_chg_month + "-" + str(max_chg_day) + " " + "($" + str(max_chg_num) + ")" )
print("Greatest Decrease in Revenue: " + min_chg_month + "-" + str(min_chg_day) + " " + "($" + str(min_chg_num) +")"  )

# Specify the file to write to
output_path = os.path.join("budget_data_2_new.csv")

# Open the file using "write" mode. Specify the variable to hold the contents
with open(output_path, 'w', newline='') as csvfile:

    # Initialize csv.writer
    csvwriter = csv.writer(csvfile, delimiter=',')

   
    csvwriter.writerow(['Financial Analysis'])
    csvwriter.writerow(['------------------------------------'])
    csvwriter.writerow(["Total Months: " + "$" + str(count_months)])
    csvwriter.writerow(["Total Revenue: " + str(sum_revenue)])
    csvwriter.writerow(["Average Revenue Change: " + str(int(avgChg))])  
    csvwriter.writerow(["Greatest Increase in Revenue: " + max_chg_month + "-" + str(max_chg_day) + " " + "($" + str(max_chg_num) + ")"])
    csvwriter.writerow(["Greatest Decrease in Revenue: " + min_chg_month + "-" + str(min_chg_day) + " " + "($" + str(min_chg_num) + ")"])

    