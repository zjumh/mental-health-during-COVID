import os
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from ast import literal_eval
from pprint import pprint
import gensim
from gensim.corpora import Dictionary
from wordcloud import WordCloud
from pickle import load, dump
import gensim
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.ticker as ticker
import numpy as np
from numpy.polynomial.polynomial import polyfit
import scipy.stats
import gensim
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.phrases import Phrases, Phraser
from gensim.corpora import Dictionary
from gensim.models import LdaModel, LdaMulticore, LsiModel


# Topic modeling
df = pd.read_csv("/data_8t/lmh_total/model3/mental_token.csv", keep_default_na=False)

# convert strings of lists to lists
df.tokens = df.tokens.apply(literal_eval)

corpus = df.tokens.values.tolist()
dictionary = Dictionary(corpus)
# changing these numbers can increase/decrease the run time if needed, but too exclusive will lead to worse results
no_below = 5
dictionary.filter_extremes(no_below=no_below, no_above=0.5)
corpus = [dictionary.doc2bow(tokens) for tokens in corpus]
print('vocab size: {}'.format(len(dictionary)))
print('documents in corpus: {}'.format(len(corpus)))

os.makedirs(f"/data_8t/lmh_total/model3/Models/{no_below}/", exist_ok=True)
savefile = f'/data_8t/lmh_total/model3/Models/{no_below}/all.PICKLE'
print('saving dataset to {}...'.format(savefile))
dump({'corpus': corpus, 'dictionary': dictionary}, open(savefile, 'wb+'))
loaddict = {'corpus': corpus, 'dictionary': dictionary}

#topic model
def topic_modeling(num_topics=5):
    np.random.seed(0)
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token
    iterations = 50
    passes = 5

    print('topics: {}'.format(num_topics))
    print('interations: {}'.format(iterations))
    print('passes: {}'.format(passes))
    print('vocab size: {}'.format(len(dictionary)))
    print('documents in corpus: {}'.format(len(corpus)))

    model_directory = f"/data_8t/lmh_total/model3/Models/{no_below}/"
    os.makedirs(model_directory, exist_ok=True)
    model_name = f"{model_directory}/all_p{passes}_i{iterations}_t{num_topics}"
    print("Model: ", model_name)

    ##Create new model with desired parameters
    # https://radimrehurek.com/gensim/models/ldamulticore.html
    model = LdaModel(
        corpus=corpus,  # leave commented out for batch training, uncomment to train on full corpus at once
        id2word=id2word,
        iterations=iterations,
        passes=passes,
        num_topics=num_topics,
        random_state=0
    )

    top_topics = model.top_topics(corpus)

    # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    print('\nAverage topic coherence: %.4f.' % avg_topic_coherence)
    # pprint(top_topics)  # prints list of ((list of top probability,term tuples), topic coherence) tuples

    print(datetime.now())
    try:
        print('saving model...')
        model.save(model_name)
        print('model saved as {}.'.format(model_name))
    except Exception as e:
        print('saving error: {}'.format(e))
    print("----------------", "\n")

n_topics = [6, 7 , 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
for num_topics in n_topics:
    topic_modeling(num_topics=num_topics)
