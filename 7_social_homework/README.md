
## Observable Trends

1) There is a high concentration of individual tweets with neutral polarity for all media sources.

2) CBS and BBC had the most positive tweet polarity, while CNN and Fox News had the most negative tweet polarity. 

3) Out of the total individual tweets gathered, there is a fairly equal distribution of both positive and negative tweets. 


```python
#Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import tweepy
import time
import datetime
import seaborn as sns
import os
from dateutil.parser import parse

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
```


```python
#Keys
file_name = "/Users/acollier/Documents/api_keys.json"
data = json.load(open(file_name))

consumer_key = data['twitter_consumer_key']
consumer_secret = data['twitter_consumer_secret']
access_token = data['twitter_access_token']
access_token_secret = data['twitter_access_token_secret']
```


```python
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
```


```python
target_user = ("@BBC", "@CBS", "@CNN", "@FoxNews", "@nytimes")
```


```python
compound_list = []
positive_list = []
negative_list = []
neutral_list = []
text_list = []
source_list = []
date_list = []
tweet_count = []
```


```python
for user in target_user:
    counter = 0
    # Loop through 5 pages of tweets (total 100 tweets)
    for x in range(5):

        # Get all tweets from home feed
        public_tweets = api.user_timeline(user, page=x)

        # Loop through all tweets
        for tweet in public_tweets:

            # Run Vader Analysis on each tweet
            compound = analyzer.polarity_scores(tweet["text"])["compound"]
            pos = analyzer.polarity_scores(tweet["text"])["pos"]
            neu = analyzer.polarity_scores(tweet["text"])["neu"]
            neg = analyzer.polarity_scores(tweet["text"])["neg"]

            # Add each value to the appropriate array
            compound_list.append(compound)
            positive_list.append(pos)
            negative_list.append(neg)
            neutral_list.append(neu)
            text_list.append(tweet['text'])
            date_list.append(parse(tweet['created_at']))
            source_list.append(user)
            tweet_count.append(counter)
            counter += 1
```


```python
news_tweets = {"Date": date_list,
              "User": source_list,
              "Tweet Text": text_list,
              "Compound": compound_list,
              "Positive": positive_list,
              "Neutral": negative_list,
              "Negative": neutral_list,
              "Tweet Count": tweet_count
             }
```


```python
news_tweets_pd = pd.DataFrame.from_dict(news_tweets)
news_tweets_pd.head()
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
      <th>Compound</th>
      <th>Date</th>
      <th>Negative</th>
      <th>Neutral</th>
      <th>Positive</th>
      <th>Tweet Count</th>
      <th>Tweet Text</th>
      <th>User</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0000</td>
      <td>2018-02-02 20:04:03+00:00</td>
      <td>1.00</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>0</td>
      <td>A young woman investigates the historic disapp...</td>
      <td>@BBC</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.0000</td>
      <td>2018-02-02 19:32:04+00:00</td>
      <td>1.00</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>1</td>
      <td>Tonight, @NigelSlater cooks and eats with the ...</td>
      <td>@BBC</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0000</td>
      <td>2018-02-02 19:00:07+00:00</td>
      <td>1.00</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>2</td>
      <td>🤼 Ever heard of the Russian martial art 'Syste...</td>
      <td>@BBC</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.4588</td>
      <td>2018-02-02 18:30:06+00:00</td>
      <td>0.85</td>
      <td>0.0</td>
      <td>0.15</td>
      <td>3</td>
      <td>🍞😋 When toast gets really tasty...\n\nHere are...</td>
      <td>@BBC</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.0000</td>
      <td>2018-02-02 17:31:01+00:00</td>
      <td>1.00</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>4</td>
      <td>'Oh hey............ man.'\n\n😂 When you run in...</td>
      <td>@BBC</td>
    </tr>
  </tbody>
</table>
</div>




```python
news_tweets_pd = news_tweets_pd[["User", "Tweet Count", "Tweet Text", "Date", "Compound", "Positive", "Neutral", "Negative"]]
news_tweets_pd.head()
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
      <th>User</th>
      <th>Tweet Count</th>
      <th>Tweet Text</th>
      <th>Date</th>
      <th>Compound</th>
      <th>Positive</th>
      <th>Neutral</th>
      <th>Negative</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>@BBC</td>
      <td>0</td>
      <td>A young woman investigates the historic disapp...</td>
      <td>2018-02-02 20:04:03+00:00</td>
      <td>0.0000</td>
      <td>0.00</td>
      <td>0.0</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>@BBC</td>
      <td>1</td>
      <td>Tonight, @NigelSlater cooks and eats with the ...</td>
      <td>2018-02-02 19:32:04+00:00</td>
      <td>0.0000</td>
      <td>0.00</td>
      <td>0.0</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>@BBC</td>
      <td>2</td>
      <td>🤼 Ever heard of the Russian martial art 'Syste...</td>
      <td>2018-02-02 19:00:07+00:00</td>
      <td>0.0000</td>
      <td>0.00</td>
      <td>0.0</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>@BBC</td>
      <td>3</td>
      <td>🍞😋 When toast gets really tasty...\n\nHere are...</td>
      <td>2018-02-02 18:30:06+00:00</td>
      <td>0.4588</td>
      <td>0.15</td>
      <td>0.0</td>
      <td>0.85</td>
    </tr>
    <tr>
      <th>4</th>
      <td>@BBC</td>
      <td>4</td>
      <td>'Oh hey............ man.'\n\n😂 When you run in...</td>
      <td>2018-02-02 17:31:01+00:00</td>
      <td>0.0000</td>
      <td>0.00</td>
      <td>0.0</td>
      <td>1.00</td>
    </tr>
  </tbody>
</table>
</div>




```python
news_tweets_pd.to_csv("news_tweets.csv", index=False)
```


```python
sns.set_style('darkgrid')
today_date = datetime.datetime.now().strftime('%m/%d/%y')
user_type = news_tweets_pd["User"].unique()
colors = ["lightskyblue", "green", "red", "blue", "yellow"]

tweets_facetgrid = sns.FacetGrid(data=news_tweets_pd, hue="User", hue_order=user_type, palette=colors)
tweets_facetgrid.map(plt.scatter, 'Tweet Count', 'Compound', alpha=0.5, marker='o', edgecolors="black", linewidth=1)
tweets_facetgrid.fig.set_size_inches(8,5)


plt.title("Sentiment Analysis of Media Tweets (" + today_date + ")")
plt.xlabel("Tweets Ago")
plt.ylabel("Tweet Polarity")
plt.legend(bbox_to_anchor=(1, 1), title="Media Sources")
plt.show()
```


![png](output_11_0.png)



```python
avg_sentiment = news_tweets_pd.groupby(['User']).agg({'Compound':'mean'})
avg_sentiment = avg_sentiment.reset_index()
avg_sentiment
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
      <th>User</th>
      <th>Compound</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>@BBC</td>
      <td>0.208463</td>
    </tr>
    <tr>
      <th>1</th>
      <td>@CBS</td>
      <td>0.341264</td>
    </tr>
    <tr>
      <th>2</th>
      <td>@CNN</td>
      <td>-0.042276</td>
    </tr>
    <tr>
      <th>3</th>
      <td>@FoxNews</td>
      <td>-0.036477</td>
    </tr>
    <tr>
      <th>4</th>
      <td>@nytimes</td>
      <td>0.022969</td>
    </tr>
  </tbody>
</table>
</div>




```python
sentiment_plot = sns.barplot(data=avg_sentiment, palette=colors, x="User", y="Compound")

plt.title("Overall Media Sentiment based on Twitter (" + today_date + ")")
plt.xlabel("")
plt.ylabel("Tweet Polarity")

plt.show()
plt.gcf().clear()
```


![png](output_13_0.png)

