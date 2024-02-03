# %%
import nltk
import pandas as pd
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
# nltk.download('averaged_perceptron_tagger')
# import googlescraper as sc
# from bs4 import BeautifulSoup
# from selenium import webdriver
# import time
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from googleapiclient.discovery import build
from furl import furl
import re
import json
# import operator
from nltk import word_tokenize

# nltk.download('punkt')


API_KEY = 'AIzaSyC1N29nzjJn-A6qMynPaF1nwIZWvYtLEjs'

def get_video_id(video_url):   
    url = furl(video_url)
    return url.args['v']

def get_video_info(video_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    return response['items'][0]['snippet']

def get_video_title(video_info):
    return video_info['title']

def get_channel_title(video_info):
    return video_info['channelTitle']

def get_all_comments(video_id, max_comments):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=max_comments)
    response = request.execute()
    comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response['items']]
    comments = [i for i in comments if len(i)<499]
    return comments

def scrape(video_site):
    MAX_COMMENTS = 50 * 10  
    
    video_url = video_site
    video_id = get_video_id(video_url)
    video_info = get_video_info(video_id)

    video_title = get_video_title(video_info)
    channel_title = get_channel_title(video_info)

    clean_title = re.sub(r'[^\w\s]+', '', video_title)
    filename = f'{channel_title} - {clean_title[:30]} - {video_id}'

    # Top Level Comments
    comments = get_all_comments(video_id, MAX_COMMENTS)

    # Print Top Level Comments
    return comments



# %%

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# %%

def roberta_scores(example):
    encoded_text = tokenizer(example, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_dict = {
        'negative' : scores[0],
        'neutral' : scores[1],
        'positive' : scores[2]
    }
    v = list(scores_dict.values())
 
# taking list of car keys in v
    k = list(scores_dict.keys())
 
    return(k[v.index(max(v))])

# %%
def mainfunction(video_site):
    comments = scrape(video_site=video_site)
    keys = [roberta_scores(i) for i in comments]
    # output_dict = {k:v for (k,v) in zip(keys,comments)}

    count = []
    neg_count,pos_count,neu_count = 0,0,0
    for i in keys:
        if i=="negative":
            neg_count += 1
        elif i=="positive":
            pos_count += 1
        else:
            neu_count += 1
    total = neg_count+pos_count+neu_count
    count.append((neg_count/total)*100)
    count.append((pos_count/total)*100)
    count.append((neu_count/total)*100) ## negative positive neutral
    label = np.argmax(count)
    if label == 0 :
        overall_sentiment = "Negative"
    if label == 1:
        overall_sentiment = "Positive"
    if label == 2:
        overall_sentiment = "Neutral"
    

    words = wordslist(comments)
    adjectives = []
    l1 = words
    for i in range(len(l1[0])):
        adjectives.append(l1[0][i][0])
    adjectives = list(set(adjectives))
    
    summary = f"Viewers express {overall_sentiment} sentiments, emphasizing aspects with adjectives like {', '.join(adjectives)}."
    dict = {'percentages':count,'important_keywords':words,'description':summary}
    json_body = json.dumps(dict)
    return json_body


def wordslist(comments):
    
    imp_words = []
    tagged = [nltk.pos_tag(word_tokenize(i)) for i in comments]
    for i in tagged:
        for j in i:
            if(j[1] == "JJ" or j[1] == "RB"):
                imp_words.append(j[0].lower())


    freq = {}
    for items in imp_words:
        freq[items] = imp_words.count(items)
    keys = [x for x in imp_words]
    values = [imp_words.count(items) for items in imp_words]
    freq = {'Words':keys,"frequency":values}
    df = pd.DataFrame(freq)
    df['sentiment'] = [roberta_scores(i) for i in keys]
    df = df[df.sentiment != 'neutral']
    words = df[['Words','sentiment']]
    word_list = words.values.tolist()
    unique_list = []
    for item in word_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


# print(mainfunction("https://www.youtube.com/watch?v=-uaAa9DszAU"))