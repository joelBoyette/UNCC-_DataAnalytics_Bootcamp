import os
import csv

voter = []
county = []
candidate = []
voter_count = 0
candidate_summary = []
candidate_count = 0
candidate_wins = []
calc_percent = 0.00
votes_percent = []
winner = ""
final_list = []

election_csv_path = os.path.join("election_data_2.csv")

with open(election_csv_path, newline="") as csvfile:
    
    csvreader = csv.reader(csvfile, delimiter=",")
    csv_header = next(csvreader)
    
    for row in csvreader:
        voter.append(row[0])
        #get x to its own list
        county.append(row[1])
        #assign x to its own list
        candidate.append(row[2])

candidate.sort()


for x in range(len(voter)):
    voter_count += 1


for x in range(len(candidate)):
  
  if candidate[x] != candidate[x-1]:
      candidate_summary.append(candidate[x])



for candidates in candidate_summary:
    
    for x in range(len(candidate)):
        if candidates == candidate[x]:
            candidate_count+=1
    
    candidate_wins.append(candidate_count)
    calc_percent = (candidate_count / voter_count) * 100
    votes_percent.append(float("{0:.2f}".format(calc_percent)))
    candidate_count = 0


for x in range(len(candidate_wins)):
    if candidate_wins[x] > candidate_wins[x-1]:
        winner = candidate_summary[x]
        
for x in range(len(candidate_summary)):
    final_list.append(candidate_summary[x] + ": " + str(votes_percent[x]) + "% (" + str(candidate_wins[x]) + ")"  )

print("Election Results")
print("------------------------")
print("Total Votes: " + str(voter_count))
print("------------------------")

for row in final_list:
    print(row)

print("------------------------")
print("Winner: " + winner)
print("------------------------")


# Specify the file to write to
output_path = os.path.join("election_data_2_new.csv")

# Open the file using "write" mode. Specify the variable to hold the contents
with open(output_path, 'w', newline='') as csvfile:

    # Initialize csv.writer
    csvwriter = csv.writer(csvfile, delimiter=',')

    
    csvwriter.writerow(["Election Results"])
    csvwriter.writerow(["------------------------"])
    csvwriter.writerow(["Total Votes: " + str(voter_count)])
    csvwriter.writerow(["------------------------"])
    
    for row in final_list:
        csvwriter.writerow([row]) 
    
    csvwriter.writerow(["------------------------"])
    csvwriter.writerow(["Winner: " + winner])
    csvwriter.writerow(["------------------------"])

        
    





