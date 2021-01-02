#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# pip install pandas
# First install BeautifulSoup4 - pip install BeautifulSoup4

# library importing
import json
import platform
import time
import matplotlib
import nltk
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# scrapping libraries importing
from collections import OrderedDict  # dictionary subclass that remembers the order in which its contents are added
from bs4 import BeautifulSoup  # scrape information from web pages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from statistics import mean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # sentiment analysis
from wordcloud import WordCloud, ImageColorGenerator


# Gathering of reviews
def merging_comment(html, filename):
    soup = BeautifulSoup(html, 'html.parser')
    h3 = soup.find_all('h3')
    user_review = None
    for head in h3:
        if 'User reviews' in str(head):
            user_review = head

    user_review_parent = user_review.find_parent()
    review_area = user_review_parent.find('div', recursive=False)
    reviews = review_area.find_all('div', recursive=False)

    all_comments = []
    for review in reviews:
        text = review.find_all('div')[-1]
        if text.text == 'Full Review':
            text = review.find_all('div')[-2]

        comment = text.text.strip()
        comment = ' '.join(comment.split())
        all_comments.append(comment)

    # Sentiment analysis
    analyzer = SentimentIntensityAnalyzer()
    negative_group = []
    neutral_group = []
    positive_group = []
    sentiment_results = ''
    all_percentage = []
    for sentence in all_comments:
        vs = analyzer.polarity_scores(sentence)
        negative_score = vs['neg']
        neutral_score = vs['neu']
        positive_score = vs['pos']
        dict_percentage = {
            'negative': negative_score * 100,
            'neutral': neutral_score * 100,
            'positive': positive_score * 100
        }
        all_percentage.append(dict_percentage)

        # Conditioning & defining the 3 types of reviews: Negative, Neutral, Positive
        if negative_score > neutral_score and negative_score > positive_score:
            negative_group.append(sentence)
        if neutral_score > negative_score and neutral_score > positive_score:
            neutral_group.append(sentence)
        if positive_score > negative_score and positive_score > neutral_score:
            positive_group.append(sentence)

        sentiment_results += sentence
        sentiment_results += '\n'
        sentiment_results += 'Negative: {}, Neutral: {}, Positive: {}'.format(round(negative_score*100,2),
                                                                              round(neutral_score*100,2),
                                                                              round(positive_score*100,2))
        sentiment_results += '\n=========================================================\n'

    f = open('static/results/{}.txt'.format(filename + ' analyze results'), 'w+', encoding='utf-8')
    f.write(sentiment_results)
    f.close()

    merged_negative_group = ' '.join(negative_group)
    merged_neutral_group = ' '.join(neutral_group)
    merged_positive_group = ' '.join(positive_group)

    return merged_negative_group, merged_neutral_group, merged_positive_group, all_percentage


# Organize string from big to small and alphabetically
def word_count(str):
    counts = dict()
    words = str.split()

    # Count the occurrences of each word in a given sentence
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def get_mask_file(mask):
    if mask == "heart":
        return "img/heart.png"
    elif mask == "cloud":
        return "img/cloud.png"
    elif mask == "android":
        return "img/android.png"
    elif mask == "comment":
        return "img/comment.png"
    elif mask == "diamond":
        return "img/diamond.png"
    elif mask == "like":
        return "img/like.png"
    elif mask == "location":
        return "img/location.png"
    elif mask == "star":
        return "img/star.png"
    elif mask == "user":
        return "img/user.png"
    else:
        return "img/heart.png"


# creating the wordcloud
def create_wordcloud(config, final_words, filename, mask, color, font, maxwords, corpus, custom_blocked_words):
    print('creating wordcloud.....')

    final_words_updated = []
    for word in final_words:
        word = word.replace('.', '').replace(',', '').replace('?', '').replace('!', '').lower()
        final_words_updated.append(word)

    # Filtering word by blocked words
    f = open("blocked.txt", "r")
    blocked_words = [line.replace('\n', '') for line in f.readlines() if line != '\n']
    blocked_words.extend(custom_blocked_words)
    blocked_words.extend(nltk.corpus.stopwords.words(corpus))
    final_words = [word for word in final_words_updated if word not in blocked_words]

    # Defining dimensions of wordcloud
    mask = get_mask_file(mask)
    background_color = config['background_color']
    max_words = config['max_words']
    words = ' '.join(final_words[0:max_words])
    if mask is not None:
        mask = np.array(Image.open(mask))

    # Generate a word cloud image
    wordcloud = WordCloud(background_color=background_color, max_words=maxwords, mask=mask, width=1920, font_path=font, height=1080).generate(words)

    if mask is not None:
        image_colors = ImageColorGenerator(mask)
        plt.figure(figsize=(20, 10), facecolor='k')
        if color is None:
            plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        else:
            plt.imshow(wordcloud.recolor(colormap=color))
        plt.axis("off")
        plt.tight_layout(pad=0)
    else:
        plt.figure(figsize=(20, 10), facecolor='k')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)

    # store to file
    plt.savefig("static/results/{}.png".format(filename), facecolor='k', bbox_inches='tight')

    print('image saved')
    return f"static/results/{filename}.png"


def histogram_generator(all_percentage, filename):
    print('creating histogram....')
    negative_average = round(mean([data['negative'] for data in all_percentage]), 1)
    neutral_average = round(mean([data['neutral'] for data in all_percentage]), 1)
    positive_average = round(mean([data['positive'] for data in all_percentage]), 1)

    labels = []
    numbers = []

    analize_results = {
        'negative': negative_average,
        'neutral': neutral_average,
        'positive': positive_average
    }

    for key, value in analize_results.items():
        labels.append(key)
        numbers.append(value)

    index = np.arange(len(labels))
    plt.figure(figsize=(10, 5))
    plt.barh(index, numbers)
    for i, v in enumerate(numbers):
        plt.text(v + 0.2, i, str(v), color='black')
    plt.yticks(index, labels, fontsize=10, rotation=0)
    plt.xlabel('Percentage', fontsize=10)
    plt.title("total comments: {}".format(len(all_percentage)))

    plt.savefig("static/results/{}.png".format(filename + ' percentage'))
    
    return f"static/results/{filename} percentage.png"


def run_analysis(app_link, filename, mask, color, font, maxwords, corpus, custom_blocked_words, data_response={}, change_mask=False):
    # opening config.json
    # To view open in folder config.json - location of the app link and wordcloud info
    # For HTML link for config.json: In Chrome access developer Tools function of the browser provides us access to the HTML structure of a web page. To access the developer tool function, right-click on whatever element you want to examine, select inspect, and it will take you right to the HTML tag of that element.
    final_result = {}
    with open('config.json') as f:
        config = json.load(f)

    if change_mask:
        final_words_response = data_response['final_words']
        histogram_response = data_response['search_results']['histogram_image']

        try:
            final_result["negative_wordcloud_image"] = create_wordcloud(config, final_words_response['negative'], filename + '_negative', mask, color, font, maxwords, corpus, custom_blocked_words)
        except:
            pass

        try:
            final_result["neutral_wordcloud_image"] = create_wordcloud(config, final_words_response['neutral'],  filename + '_neutral', mask, color, font, maxwords, corpus, custom_blocked_words)
        except:
            pass

        try:
            final_result["positive_wordcloud_image"] = create_wordcloud(config, final_words_response['positive'],  filename + '_positive', mask, color, font, maxwords, corpus, custom_blocked_words)
        except:
            pass

        try:
            final_result["histogram_image"] = histogram_response
        except:
            pass

        return final_words_response, final_result


    # OS Chrome usage on MAC, Windows and Linux - vital for automatic scrolling when scrapping reviews
    operating_system = platform.system()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    try:
        if operating_system == 'Linux':
            driver = webdriver.Chrome('./chromedriver-linux', options=chrome_options)
        if operating_system == 'Darwin':
            driver = webdriver.Chrome('./chromedriver-mac', options=chrome_options)
        if operating_system == 'Windows':
            driver = webdriver.Chrome('./chromedriver-windows.exe', options=chrome_options)

        # scrolling in Chrome
        driver.maximize_window()
        driver.get(app_link)
        SCROLL_PAUSE_TIME = 5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        show_more_count = config['show_more_count']
        count = 0
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            print('wait 5 seconds to next scroll')

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                show_more = driver.find_elements_by_xpath("//*[contains(text(), 'Show More')]")
                if len(show_more)>0:
                    show_more = show_more[-1]
                    if count >= show_more_count:
                        break
                    show_more.click()
                    count += 1
                    continue

                break

            last_height = new_height

        html = driver.page_source
        driver.close()
    except Exception:
        driver.close()
        raise

    merged_negative, merged_neutral, merged_positive, all_percentage = merging_comment(html, filename)


    final_words_group = {}
    # negative process
    print('negative process....')
    results = word_count(merged_negative)
    d_sorted_by_value = OrderedDict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    final_words = []
    for k, v in d_sorted_by_value.items():
        final_words.append(k)
    try:
        final_result["negative_wordcloud_image"] = create_wordcloud(config, final_words, filename + '_negative', mask, color, font, maxwords, corpus, custom_blocked_words)
    except Exception:
        pass
    final_words_group['negative'] = final_words

    # neutral process
    print('neutral process....')
    results = word_count(merged_neutral)
    d_sorted_by_value = OrderedDict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    final_words = []
    for k, v in d_sorted_by_value.items():
        final_words.append(k)
    try:
        final_result["neutral_wordcloud_image"] = create_wordcloud(config, final_words, filename + '_neutral', mask, color, font, maxwords, corpus, custom_blocked_words)
    except Exception:
        pass
    final_words_group['neutral'] = final_words

    # positive process
    print('positive process....')
    results = word_count(merged_positive)
    d_sorted_by_value = OrderedDict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    final_words = []
    for k, v in d_sorted_by_value.items():
        final_words.append(k)
    try:
        final_result["positive_wordcloud_image"] = create_wordcloud(config, final_words, filename + '_positive', mask, color, font, maxwords, corpus, custom_blocked_words)
    except Exception:
        pass
    final_words_group['positive'] = final_words

    # Generate histogram
    final_result["histogram_image"] = histogram_generator(all_percentage, filename)

    return final_words_group, final_result

