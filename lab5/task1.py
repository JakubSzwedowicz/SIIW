import os
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from functools import lru_cache

# <HTML>
# <HEAD>
# <TITLE>Joke 3</TITLE>
# </HEAD>
#
# <BODY TEXT="black" BGCOLOR="#fddf84">
#
# <TABLE WIDTH="620" CELLSPACING="0" CELLPADDING="0">
#
# <TD Width="130"> </TD>
# <TD WIDTH="470">
# <BR><CENTER><FONT color="red" size="+2">
#
#
# </Font></center>
# <UL> <Font Size="+1"> <BR>
#
# <!--begin of joke -->
# Q. What's 200 feet long and has 4 teeth? <P>
#
# A. The front row at a Willie Nelson Concert.
# <!--end of joke -->
# </UL>
# </TD></TR></TABLE>
# </BODY>
# </HTML>

JOKES_DIRECTORY = "jokes/dataset/"
RATINGS_FILE = "jokes/jester-data-1.xls"
EMBEDDINGS_FILE = "jokes/embeddings.npy"

@lru_cache(maxsize=None)
def load_jokes():
    jokes = []

    files = os.listdir(JOKES_DIRECTORY)
    files.sort(key=lambda x: int(x[4:-5]))

    for filename in files:
        if filename.endswith(".html"):
            with open(JOKES_DIRECTORY + filename, 'r') as file:
                html = file.read()
                joke = re.search(r'<!--begin of joke -->(.*)<!--end of joke -->', html, re.DOTALL)
                jokes.append(joke.group(1).strip())

    # remove tags
    jokes = [re.sub(r'<.*?>', '', joke) for joke in jokes]
    return jokes


def does_embedding_file_exist():
    return os.path.isfile(EMBEDDINGS_FILE)

def extract_features(jokes):
    if does_embedding_file_exist():
        return np.load(EMBEDDINGS_FILE)

    # extract features from jokes using BERT
    model = SentenceTransformer('bert-base-cased')
    embeddings = model.encode(jokes)
    # serialize embeddings
    np.save(EMBEDDINGS_FILE, embeddings)
    return embeddings


def load_ratings():
    ratings = pd.read_excel(RATINGS_FILE, header=None)
    ratings = ratings.drop(columns=[0]) # drop column with number of rated jokes
    ratings = ratings.replace(99, np.nan) # clear date from placeholder values
    ratings = ratings.to_numpy()
    return ratings


def process_ratings(ratings):
    # rotate ratings matrix so that jokes are rows and users are columns
    # calculate mean rating for each joke so we have one rating per joke
    ratings = np.rot90(ratings)
    ratings = np.nanmean(ratings, axis=1)
    return ratings


def get_data():
    jokes = extract_features(None if does_embedding_file_exist() else load_jokes())
    ratings = process_ratings(load_ratings())
    # join jokes and ratings into one matrix
    data = np.concatenate((jokes, ratings[:, None]), axis=1)
    return data


def split_data(data, test_size=0.2):
    X = data[:, :-1]
    y = data[:, -1]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_val, y_train, y_val


def save_merged_jokes():
    jokes = extract_features(load_jokes())

    print(jokes.shape)
    with open("jokes.txt", "w") as file:
        for id, joke in enumerate(load_jokes()):
            joke = joke.replace('\n', ' ')
            file.write(f"{id+1} {joke}\n")


if __name__ == '__main__':
    data = get_data()



