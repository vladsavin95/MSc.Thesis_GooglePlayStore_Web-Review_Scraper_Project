# Start with loading all necessary libraries
import glob
import json
import os
import numpy as np
import requests

from bs4 import BeautifulSoup
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import nltk
import matplotlib.pyplot as plt


def generate_wordcloud():
    final_words = ['the', 'I', 'and', 'game', 'to', 'a', 'it', 'you', 'is', 'but', 'this', 'ads', 'so', 'have', 'like',
                   'of', 'for', 'i', 'good', 'get', 'in', 'level', 'that', 'not', 'fun', 'my', 'guns', 'are', 'can', 'just',
                   'because', 'really', 'on', 'when', 'play', 'be', 'ha', 'more', 'with', 'if', 'love', "don't", 'game.',
                   'This', "it's", 'very', 'one', 'was', 'would', 'The', 'an', 'watch', 'nerf', 'me', 'do', 'ad', 'add',
                   'no', 'see', 'at', 'all', 'even', 'after', 'there', 'should', 'time', 'your', 'cool', 'It', 'people',
                   'or', 'game,', 'much', 'its', 'many', 'But', 'only', 'still', 'out', 'as', 'first', 'got', 'they',
                   'some', 'we', 'then', 'too', 'little', 'star', 'fix', 'over', "It's", "I'm", 'also', 'will', 'bad',
                   'pretty', '5', 'gun', 'stars', 'now', 'than', 'levels', 'let', 'new', 'why', 'other', 'make', 'amazing',
                   'has', 'great', 'give', 'playing', 'am', 'Nerf', 'problem', '1', 'about', 'easy', 'update', 'u', 'free',
                   'Please', 'want', 'gets', 'app', 'every', 'had', 'shoot', 'please', 'nice', 'start', 'always', 'never',
                   'last', 'And', 'go', 'from', 'ads.', 'he', '3', 'everything', 'while', '.', 'how', 'up', 'So', 'maybe',
                   "won't", 'who', 'five', 'few', 'which', 'lot', 'phone', 'same', 'what', 'Fun', 'win', 'next', 'know',
                   'im', 'Its', 'stuff', 'graphics', 'thought', 'played', 'pranks', 'them', 'rate', 'awesome', 'keeps',
                   'Ads', "I've", '10', 'take', "that's", 'enjoy', '&', 'going', 'There', 'nothing', 'it.', 'better', 'any',
                   'ok', 'hard', 'that,', 'things', 'thing', 'it,', 'were', 'friends', 'stars.', 'keep', 'work', 'reached',
                   'freezes', 'old', 'gun.', 'Good', 'fast', 'having', 'lag', 'reset', 'enough', 'skins', 'My', 'back',
                   'game!', 'again.', 'getting', 'games', 'unlock', 'needs', 'character', 'sometimes', 'saying',
                   'downloaded', 'sad', 'think', 'our', 'adds', 'real', 'expensive', 'remove', 'plz', "there's", 'signal',
                   'On', 'died', 'once', "doesn't", 'hit', 'until', 'tried', 'load']

    final_words_updated = []
    for word in final_words:
        word = word.replace('.', '').replace(',', '').replace('?', '').replace('!', '').lower()
        final_words_updated.append(word)

    # Filtering word by blocked words
    f = open("blocked.txt", "r")
    blocked_words = [line.replace('\n', '') for line in f.readlines() if line != '\n']
    final_words = [word for word in final_words_updated if word not in blocked_words]

    print(final_words)

    words = ' '.join(final_words[0:200])

    # opening config.json
    with open('config.json') as f:
        config = json.load(f)

    mask = 'img/heart.png'
    background_color = 'white'
    max_words = config['max_words']
    if mask is not None:
        mask = np.array(Image.open(mask))

    colors = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap',
              'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r',
              'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2',
              'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r',
              'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn',
              'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r',
              'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r',
              'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr',
              'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r',
              'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r',
              'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern',
              'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray',
              'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r',
              'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism',
              'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r',
              'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r',
              'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis',
              'viridis_r', 'winter', 'winter_r']


    colormap = None
    font_path = None
    colormap = 'Oranges'
    font_path = 'font/FrankRuhlHofshi-Bold.otf'

    # Generate a word cloud image
    wordcloud = WordCloud(background_color=background_color, colormap=colormap, max_words=max_words, mask=mask, font_path=font_path).generate(
        words)

    if mask is not None:
        image_colors = ImageColorGenerator(mask)
        plt.figure(figsize=(20, 10), facecolor='k')
        # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
    else:
        plt.figure(figsize=(20, 10), facecolor='k')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)

    # store to file
    plt.savefig("test.png", facecolor='k', bbox_inches='tight')
    print('image saved')

def nltk_test():
    stoplist = nltk.corpus.stopwords.words('english')
    raise Exception(stoplist)

    text = '''
    In computing, stop words are words which are filtered out before or after 
    processing of natural language data (text). Though "stop words" usually 
    refers to the most common words in a language, there is no single universal 
    list of stop words used by all natural language processing tools, and 
    indeed not all tools even use such a list. Some tools specifically avoid 
    removing these stop words to support phrase search.
    '''
    print("\nOriginal string:")
    print(text)
    clean_word_list = [word for word in text.split() if word not in stoplist]
    print("\nAfter removing stop words from the said text:")
    print(clean_word_list)


def read_font():
    ttf = glob.glob('./font/*.ttf')
    ttc = glob.glob('./font/*.ttc')

    ttfs = [file.replace('./font/', '') for file in ttf]
    ttcs = [file.replace('./font/', '') for file in ttc]

    all_fonts = ttfs + ttcs
    all_fonts = [font.split('.')[0] for font in all_fonts]

    return sorted(all_fonts)


def get_fonts_name():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'MC1=GUID=37855b93d0b3408a8f6f6b6ee220c994&HASH=3785&LV=202011&V=4&LU=1606264460400; _ga=GA1.2.1651103298.1608286832; MSFPC=GUID=37855b93d0b3408a8f6f6b6ee220c994&HASH=3785&LV=202011&V=4&LU=1606264460400; MUID=05FA9111911169A60AC79E9D902968D5; MSCC=NR',
        'if-none-match': '0cHKleAMASG1itx5FYEft/HROflTB/DQjUwGZS68WDo=',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }


    res = requests.get('https://docs.microsoft.com/en-us/typography/fonts/windows_10_font_list', headers=headers)

    soup = BeautifulSoup(res.text, 'html5lib')
    table = soup.find('table')
    trs = table.find_all('tr')
    trs = trs[2:]

    dict_name = {}
    for tr in trs:
        tds = tr.find_all('td')
        font_name = tds[1].text
        file_name = tds[2].text
        dict_name[file_name.lower()] = font_name

    with open('fonts_name.json', 'w') as outfile:
        json.dump(dict_name, outfile)


def change_fonts_name():
    with open('fonts_name.json') as json_file:
        dict_font = json.load(json_file)

    # rename to lower()
    files = glob.glob('./font/*')
    for file in files:
        # print('renaming to lower: {}'.format(file))
        os.rename(file, file.lower())

    # rename filename to font name
    for file in files:
        # print('renaming filename to fonts name')
        original_name = file.replace('./font/', '')

        try:
            result_name = dict_font[original_name]
        except KeyError:
            continue

        os.rename('./font/{}'.format(original_name), './font/{}.{}'.format(result_name, original_name.split('.')[1]))

    # font_unlisted = [font for font in fonts if font not in dict_font.keys()]


fonts = read_font()
print(fonts)