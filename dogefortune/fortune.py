import random
from textblob import TextBlob as TB

fortunes = open("fortunes").read().lower().replace("'", "").split("\n")

qualifiers = {
    "NNS": ["very", "so", "much", "such"],
    "NN": ["very", "so", "many"],
    "VBG": ["very", "so", "many"],
    "VBN": ["very", "so", "many"],
    "VB": ["so", "plz"]
}

ends = [". wow", ". amaze", ". omg", ""]

no = ["be", "am"]


def get_fortune():
    fortune = random.choice(fortunes)
    tags = TB(fortune).tags
    sentence = []
    for tag in tags:
        if tag[0] in no:
            continue
        if tag[1] in qualifiers:
            adj = random.choice(qualifiers[tag[1]])
            sentence.append(adj + " " + tag[0].lower())
    if not sentence:
        return get_fortune()
    return ', '.join(sentence) + random.choice(ends)

if __name__ == "__main__":
    for i in range(20):
        print(get_fortune())
