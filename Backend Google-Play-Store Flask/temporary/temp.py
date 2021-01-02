from collections import OrderedDict
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('res.html'), 'html.parser')

h3 = soup.find_all('h3')

user_review = None
for head in h3:
    if 'User reviews' in str(head):
        user_review = head

user_review_parent = user_review.find_parent()

review_area = user_review_parent.find('div', recursive=False)
reviews = review_area.find_all('div', recursive=False)

f = open('res3.html', 'w+')
f.write(str(review_area))
f.close()
# print(user_review_parent)

all_comments = []
for review in reviews:
    text = review.find_all('div')[-1]
    if text.text == 'Full Review':
        text = review.find_all('div')[-2]

    comment = text.text.strip()
    comment = ' '.join(comment.split())
    all_comments.append(comment)

merged_comment = ' '.join(all_comments)
print(merged_comment)


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

results = word_count(merged_comment)
d_sorted_by_value = OrderedDict(sorted(results.items(), key=lambda x: x[1], reverse=True))

final_words = []
for k, v in d_sorted_by_value.items():
    final_words.append(k)
    print(str(k) + ':' + str(v))

print(final_words)
