
# Heroes of Pymoli Data Analysis
Observed Trend 1: 81% of players purchasing items are male, and the average purchase price for males is $2.95 vs the average purchase price for females at $2.82.
Observed Trend 2: 65.1% of players are between the ages of 15 & 25. These two age groups also makes up 62.7% of total purchases and 62.6% of total revenue.
Observed Trend 3: Three of the most popular items were each purchased 9 times. The top most profitable item was also purchased 9 times. Further analysis could be done to determine if the prices of the most popular items could be marginally increased while still maintining popularity to drive revenue growth. 



```python
import pandas as pd
import os
```


```python
purchase_data = os.path.join("purchase_data.json")
purchase_data_pd = pd.read_json(purchase_data)
```


```python
purchase_data_pd.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Age</th>
      <th>Gender</th>
      <th>Item ID</th>
      <th>Item Name</th>
      <th>Price</th>
      <th>SN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>38</td>
      <td>Male</td>
      <td>165</td>
      <td>Bone Crushing Silver Skewer</td>
      <td>3.37</td>
      <td>Aelalis34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>21</td>
      <td>Male</td>
      <td>119</td>
      <td>Stormbringer, Dark Blade of Ending Misery</td>
      <td>2.32</td>
      <td>Eolo46</td>
    </tr>
    <tr>
      <th>2</th>
      <td>34</td>
      <td>Male</td>
      <td>174</td>
      <td>Primitive Blade</td>
      <td>2.46</td>
      <td>Assastnya25</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>Male</td>
      <td>92</td>
      <td>Final Critic</td>
      <td>1.36</td>
      <td>Pheusrical25</td>
    </tr>
    <tr>
      <th>4</th>
      <td>23</td>
      <td>Male</td>
      <td>63</td>
      <td>Stormfury Mace</td>
      <td>1.27</td>
      <td>Aela59</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Player Count (Total Number of Players)
player_count = len(purchase_data_pd["SN"].unique())
player_count_summary = pd.DataFrame({"Total Players": [player_count]})
player_count_summary
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>573</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Purchasing Analysis (Total)
#Number of Unique Items
#Average Purchase Price
#Total Number of Purchases
#Total Revenue

unique_items = len(purchase_data_pd["Item ID"].unique())
average_price = purchase_data_pd["Price"].mean()
total_purchase_count = len(purchase_data_pd)
total_revenue = purchase_data_pd["Price"].sum()

purchasing_analysis = pd.DataFrame({"Number of Unique Items": [unique_items], 
                                    "Average Price": [average_price], 
                                    "Number of Purchases": [total_purchase_count], 
                                    "Total Revenue": [total_revenue]})

purchasing_analysis["Average Price"] = purchasing_analysis["Average Price"].map("${0:,.2f}".format)
purchasing_analysis["Total Revenue"] = purchasing_analysis["Total Revenue"].map("${0:,.2f}".format)

purchasing_analysis = purchasing_analysis[["Number of Unique Items", "Average Price", "Number of Purchases", "Total Revenue"]]
purchasing_analysis
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Number of Unique Items</th>
      <th>Average Price</th>
      <th>Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>183</td>
      <td>$2.93</td>
      <td>780</td>
      <td>$2,286.33</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Gender Demographics
#Percentage and Count of Male Players
#Percentage and Count of Female Players
#Percentage and Count of Other / Non-Disclosed

player_group_count = purchase_data_pd.groupby(["SN", "Gender"]).count()
player_group_count.reset_index(inplace=True)

total_gender = player_group_count["Gender"].count()
male = player_group_count["Gender"].value_counts()['Male']
female = player_group_count["Gender"].value_counts()['Female']
non_gender_specific = total_gender - male - female
perc_male = (male/total_gender) * 100
perc_female = (female/total_gender) * 100
perc_non_gender_specific = (non_gender_specific/total_gender) * 100

gender_demographic_df = pd.DataFrame({
    "Gender": ["Male", "Female", "Other / Non-Disclosed"],
    "Percentage of Players": [perc_male, perc_female, perc_non_gender_specific],
    "Total Count": [male, female, non_gender_specific]
})
gender_demographic_df["Percentage of Players"] = gender_demographic_df["Percentage of Players"].map("{0:,.2f}".format)
gender_demographic_df = gender_demographic_df.set_index("Gender")
gender_demographic_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>81.15</td>
      <td>465</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>17.45</td>
      <td>100</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>1.40</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Purchasing Analysis (Gender) 
#The below each broken by gender
#Purchase Count
#Average Purchase Price
#Total Purchase Value
#Normalized Totals

purchasing_gender_group = purchase_data_pd.groupby(['Gender']).agg({'Item ID':'count', 'Price':['mean', 'sum']})

gender_purchasing_df = pd.DataFrame({"Purchase Count": purchasing_gender_group["Item ID"]["count"], 
                                    "Average Purchase Price": purchasing_gender_group["Price"]["mean"], 
                                    "Total Purchase Value": purchasing_gender_group["Price"]["sum"]})

total_gender_counts = pd.DataFrame(gender_demographic_df["Total Count"])
gender_purchasing_df = gender_purchasing_df.join(total_gender_counts)
gender_purchasing_df["Normalized Totals"] = gender_purchasing_df["Total Purchase Value"] / gender_purchasing_df["Total Count"]
gender_purchasing_df = gender_purchasing_df.drop("Total Count", axis=1)

gender_purchasing_df=gender_purchasing_df[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Normalized Totals"]]
gender_purchasing_df["Average Purchase Price"] = gender_purchasing_df["Average Purchase Price"].map("${0:,.2f}".format)
gender_purchasing_df["Total Purchase Value"] = gender_purchasing_df["Total Purchase Value"].map("${0:,.2f}".format)
gender_purchasing_df["Normalized Totals"] = gender_purchasing_df["Normalized Totals"].map("${0:,.2f}".format)
gender_purchasing_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>136</td>
      <td>$2.82</td>
      <td>$382.91</td>
      <td>$3.83</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>633</td>
      <td>$2.95</td>
      <td>$1,867.68</td>
      <td>$4.02</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>11</td>
      <td>$3.25</td>
      <td>$35.74</td>
      <td>$4.47</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Age Demographics
bins = [0,10,15,20,25,30,35,40,100]
group_labels = ["<10","10-14","15-19","20-24","25-29","30-34",
                "35-39","40+"]

unique_screenname = purchase_data_pd.groupby(['SN']).max()

player_age_df = unique_screenname.groupby(pd.cut(unique_screenname["Age"], bins, labels=group_labels))
player_age_df = pd.DataFrame(player_age_df.size())
player_age_df.columns = ["Total Count"] 
player_age_df["Percentage of Players"] = player_age_df["Total Count"] / player_age_df["Total Count"].sum() * 100        
player_age_df["Percentage of Players"] = player_age_df["Percentage of Players"].map("{0:,.2f}".format)  
player_age_df = player_age_df[["Percentage of Players", "Total Count"]]
player_age_df

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
    <tr>
      <th>Age</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>3.84</td>
      <td>22</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>9.42</td>
      <td>54</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>24.26</td>
      <td>139</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>40.84</td>
      <td>234</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>9.08</td>
      <td>52</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>7.68</td>
      <td>44</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>4.36</td>
      <td>25</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>0.52</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Age Demographics
#The below each broken into bins of 4 years (i.e. <10, 10-14, 15-19, etc.) 
#Purchase Count
#Average Purchase Price
#Total Purchase Value
#Normalized Totals

bins = [0,10,15,20,25,30,35,40,100]
group_labels = ["<10","10-14","15-19","20-24","25-29","30-34",
                "35-39","40+"]

age_purchase_group = purchase_data_pd.groupby(pd.cut(purchase_data_pd["Age"], bins, labels=group_labels))
age_purchase_group = age_purchase_group.agg({'Item ID':'count', 'Price':['mean', 'sum']})

age_summary = pd.DataFrame({"Purchase Count": age_purchase_group["Item ID"]["count"], 
                                    "Average Purchase Price": age_purchase_group["Price"]["mean"], 
                                    "Total Purchase Value": age_purchase_group["Price"]["sum"]})

total_age_counts = pd.DataFrame(player_age_df["Total Count"])
age_summary = age_summary.join(total_age_counts)
age_summary["Normalized Totals"] = age_summary["Total Purchase Value"] / age_summary["Total Count"]
age_summary = age_summary.drop("Total Count", axis=1)

age_summary=age_summary[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Normalized Totals"]]
age_summary["Average Purchase Price"] = age_summary["Average Purchase Price"].map("${0:,.2f}".format)
age_summary["Total Purchase Value"] = age_summary["Total Purchase Value"].map("${0:,.2f}".format)
age_summary["Normalized Totals"] = age_summary["Normalized Totals"].map("${0:,.2f}".format)
age_summary
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Age</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>32</td>
      <td>$3.02</td>
      <td>$96.62</td>
      <td>$4.39</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>78</td>
      <td>$2.87</td>
      <td>$224.15</td>
      <td>$4.15</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>184</td>
      <td>$2.87</td>
      <td>$528.74</td>
      <td>$3.80</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>305</td>
      <td>$2.96</td>
      <td>$902.61</td>
      <td>$3.86</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>76</td>
      <td>$2.89</td>
      <td>$219.82</td>
      <td>$4.23</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>58</td>
      <td>$3.07</td>
      <td>$178.26</td>
      <td>$4.05</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>44</td>
      <td>$2.90</td>
      <td>$127.49</td>
      <td>$5.10</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>3</td>
      <td>$2.88</td>
      <td>$8.64</td>
      <td>$2.88</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Top Spenders
#Identify the the top 5 spenders in the game by total purchase value, then list (in a table):
#SN
#Purchase Count
#Average Purchase Price
#Total Purchase Value

top_spenders = purchase_data_pd.groupby(['SN'])
top_spenders_group = top_spenders.agg({'Item ID':'count', 'Price':['mean', 'sum']})

top_spenders_group = pd.DataFrame({"Purchase Count": top_spenders_group["Item ID"]["count"], 
                                    "Average Purchase Price": top_spenders_group["Price"]["mean"], 
                                    "Total Purchase Value": top_spenders_group["Price"]["sum"]})
top_spenders_group=top_spenders_group[["Purchase Count", "Average Purchase Price", "Total Purchase Value"]]
top_spenders_group["Average Purchase Price"] = top_spenders_group["Average Purchase Price"].map("${0:,.2f}".format)
top_spenders_group["Total Purchase Value"] = top_spenders_group["Total Purchase Value"].map("${0:,.2f}".format)

top_spenders_group = top_spenders_group.sort_values(["Total Purchase Value"], ascending=False)
top_spenders_group.head(5)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Qarwen67</th>
      <td>4</td>
      <td>$2.49</td>
      <td>$9.97</td>
    </tr>
    <tr>
      <th>Sondim43</th>
      <td>3</td>
      <td>$3.13</td>
      <td>$9.38</td>
    </tr>
    <tr>
      <th>Tillyrin30</th>
      <td>3</td>
      <td>$3.06</td>
      <td>$9.19</td>
    </tr>
    <tr>
      <th>Lisistaya47</th>
      <td>3</td>
      <td>$3.06</td>
      <td>$9.19</td>
    </tr>
    <tr>
      <th>Tyisriphos58</th>
      <td>2</td>
      <td>$4.59</td>
      <td>$9.18</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Most Popular Items
#Identify the 5 most popular items by purchase count, then list (in a table):
#Item ID
#Item Name
#Purchase Count
#Item Price
#Total Purchase Value

popular_items = purchase_data_pd.groupby(['Item ID'])
popular_items_group = popular_items.agg({'Item Name':'max', 'SN':'count','Price':['max', 'sum']})

popular_items_group = pd.DataFrame({"Item Name": popular_items_group["Item Name"]["max"],
                                    "Purchase Count": popular_items_group["SN"]["count"], 
                                    "Item Price": popular_items_group["Price"]["max"], 
                                    "Total Purchase Value": popular_items_group["Price"]["sum"]})
popular_items_group=popular_items_group[["Item Name","Purchase Count", "Item Price", "Total Purchase Value"]]
popular_items_group = popular_items_group.sort_values(["Purchase Count"], ascending=False)
popular_items_group["Item Price"] = popular_items_group["Item Price"].map("${0:,.2f}".format)
popular_items_group["Total Purchase Value"] = popular_items_group["Total Purchase Value"].map("${0:,.2f}".format)

popular_items_group.head(5)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item Name</th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <td>Betrayal, Whisper of Grieving Widows</td>
      <td>11</td>
      <td>$2.35</td>
      <td>$25.85</td>
    </tr>
    <tr>
      <th>84</th>
      <td>Arcane Gem</td>
      <td>11</td>
      <td>$2.23</td>
      <td>$24.53</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Trickster</td>
      <td>9</td>
      <td>$2.07</td>
      <td>$18.63</td>
    </tr>
    <tr>
      <th>175</th>
      <td>Woeful Adamantite Claymore</td>
      <td>9</td>
      <td>$1.24</td>
      <td>$11.16</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Serenity</td>
      <td>9</td>
      <td>$1.49</td>
      <td>$13.41</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Most Profitable Items
#Identify the 5 most profitable items by total purchase value, then list (in a table):
#Item ID
#Item Name
#Purchase Count
#Item Price
#Total Purchase Value

profit_items = purchase_data_pd.groupby(['Item ID'])
profit_items_group = profit_items.agg({'Item Name':'max', 'SN':'count','Price':['max', 'sum']})

profit_items_group = pd.DataFrame({"Item Name": profit_items_group["Item Name"]["max"],
                                    "Purchase Count": profit_items_group["SN"]["count"], 
                                    "Item Price": profit_items_group["Price"]["max"], 
                                    "Total Purchase Value": profit_items_group["Price"]["sum"]})
profit_items_group=profit_items_group[["Item Name","Purchase Count", "Item Price", "Total Purchase Value"]]
profit_items_group = profit_items_group.sort_values(["Total Purchase Value"], ascending=False)
profit_items_group["Item Price"] = profit_items_group["Item Price"].map("${0:,.2f}".format)
profit_items_group["Total Purchase Value"] = profit_items_group["Total Purchase Value"].map("${0:,.2f}".format)

profit_items_group.head(5)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item Name</th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34</th>
      <td>Retribution Axe</td>
      <td>9</td>
      <td>$4.14</td>
      <td>$37.26</td>
    </tr>
    <tr>
      <th>115</th>
      <td>Spectral Diamond Doomblade</td>
      <td>7</td>
      <td>$4.25</td>
      <td>$29.75</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Orenmir</td>
      <td>6</td>
      <td>$4.95</td>
      <td>$29.70</td>
    </tr>
    <tr>
      <th>103</th>
      <td>Singed Scalpel</td>
      <td>6</td>
      <td>$4.87</td>
      <td>$29.22</td>
    </tr>
    <tr>
      <th>107</th>
      <td>Splitter, Foe Of Subtlety</td>
      <td>8</td>
      <td>$3.61</td>
      <td>$28.88</td>
    </tr>
  </tbody>
</table>
</div>


