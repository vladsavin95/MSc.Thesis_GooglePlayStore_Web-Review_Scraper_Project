from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- examples -------
sentences = ["VADER is smart, handsome, and funny.",  # positive sentence example
             "VADER is smart, handsome, and funny!",  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is very smart, handsome, and funny.", # booster words handled correctly (sentiment intensity adjusted)
             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
             "VADER is VERY SMART, handsome, and FUNNY!!!", # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", # booster words & punctuation make this close to ceiling for score
             "VADER is not smart, handsome, nor funny.",  # negation sentence example
             "The book was good.",  # positive sentence
             "At least it isn't a horrible book.",  # negated negative sentence with contraction
             "The book was only kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
             "Today SUX!",  # negative slang with capitalization emphasis
             "Today only kinda sux! But I'll get by, lol", # mixed sentiment example with slang and constrastive conjunction "but"
             "Make sure you :) or :D today!",  # emoticons handled
             "Catch utf-8 emoji such as such as 💘 and 💋 and 😁",  # emojis handled
             "Not bad at all"  # Capitalized negation
             ]


analyzer = SentimentIntensityAnalyzer()
negative_group = []
neutral_group = []
positive_group = []
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence)
    negative_score = vs['neg']
    neutral_score = vs['neu']
    positive_score = vs['pos']

    if negative_score > neutral_score and negative_score > positive_score:
        negative_group.append(negative_score)
    if neutral_score > negative_score and neutral_score > positive_score:
        neutral_group.append(neutral_score)
    if positive_score > negative_score and positive_score > neutral_score:
        positive_group.append(positive_score)

    print("{:-<65} {}".format(sentence, str(vs)))

print(negative_group)
print(neutral_group)
print(positive_group)
