import os.path
import random
from textblob import TextBlob as TB

fortunepath = os.path.join(os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))), "fortunes")
fortunes = open(fortunepath).read().lower().replace("'", "").split("\n")

qualifiers = {
    "NNS": set(("very", "so", "much", "such")),
    "NN": set(("very", "so", "many")),
    "VBG": set(("very", "so", "many")),
    "VBN": set(("very", "so", "many")),
    "VB": set(("so", "plz"))
}

ends = [". wow", ". amaze", ". omg", ""]

no = ["be", "am"]


def get_fortune():
    fortune = random.choice(fortunes)
    tags = TB(fortune).tags
    sentence = []
    used_qualifiers = set()
    for tag in tags:
        if tag[0] in no:
            continue
        if tag[1] in qualifiers:
            choices = qualifiers[tag[1]] - used_qualifiers
            if not choices:
                continue
            qual = random.choice(list(choices))
            used_qualifiers.add(qual)
            sentence.append(qual + " " + tag[0].lower())
    if not sentence:
        return get_fortune()
    return ', '.join(sentence) + random.choice(ends)

if __name__ == "__main__":
    for i in range(20):
        print(get_fortune())
