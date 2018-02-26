import pandas as pd
import os
import csv

data_csv = os.path.join('election_data_1.csv')
data2_csv = os.path.join('election_data_2.csv')

data_df = pd.read_csv(data_csv)
data2_df = pd.read_csv(data2_csv)

alldata_df = data_df.append(data2_df)

total_rows = len(alldata_df.index)
total_rows2 = str(total_rows)

vote_counts = alldata_df["Candidate"].value_counts()
sumvotes_df = pd.DataFrame(vote_counts)

sumvotes_df.columns = ["Votes"]

sumvotes_df["Perc_Votes"] = (sumvotes_df["Votes"] / total_rows) *100

sumvotes_df.reset_index(level=0, inplace=True)

sumvotes_df.columns = ["Candidates", "Votes", "Perc_Votes"]

sumvotes_df = sumvotes_df[['Candidates', 'Perc_Votes', 'Votes']]

sumvotes_df['Perc_Votes'] = sumvotes_df['Perc_Votes'].apply(lambda x: round(x,1))
sumvotes_df['Perc_Votes'] = sumvotes_df['Perc_Votes'].astype(str)
sumvotes_df['Perc_Votes'] = sumvotes_df['Perc_Votes'] + "%"

winning_votes = sumvotes_df['Votes'].max()
winner_df = sumvotes_df.loc[sumvotes_df['Votes'] == winning_votes,:]
winner = winner_df['Candidates'].iloc[0]


print ("Election Results")
print("------------------------")
print("Total Votes: " + total_rows2)
print("------------------------")

for row in sumvotes_df.itertuples():
    print(row.Candidates + ": " + row.Perc_Votes + " (" + str(row.Votes) + ")")

print("------------------------")
print("Winner: " + winner)
print("------------------------")

output_path = os.path.join("main.txt")
with open(output_path, "w") as txtfile:
    txtfile.write("Election Results\n")
    txtfile.write("------------------------\n")
    txtfile.write("Total Votes: " + total_rows2 + "\n")
    txtfile.write("------------------------\n")

    for row in sumvotes_df.itertuples():
        txtfile.write(row.Candidates + ": " + row.Perc_Votes + " (" + str(row.Votes) + ")\n")

    txtfile.write("------------------------\n")
    txtfile.write("Winner: " + winner + "\n")
    txtfile.write("------------------------")
