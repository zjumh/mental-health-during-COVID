import os
# import wget
from datetime import datetime
# from dateutils import timedelta
# import itertools
import pandas as pd
import numpy as np
# import math
from pathlib import Path
# import regex as re
# from functools import reduce
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

df = pd.read_csv("/data_8t/lmh_total/model3/mental_token.csv", keep_default_na=False)

# convert strings of lists to lists
df.tokens = df.tokens.apply(literal_eval)

corpus = df.tokens.values.tolist()
dictionary = Dictionary(corpus)
# changing these numbers can increase/decrease the run time if needed, but too exclusive will lead to worse results
no_below = 5
dictionary.filter_extremes(no_below=no_below, no_above=0.5)
corpus = [dictionary.doc2bow(tokens) for tokens in corpus]

x_labels = [6, 7, 8, 9, 10, 11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
perplexity_list = []
coherence_list = []
for num_topics in x_labels:
    model_name = f'/data_8t/lmh_total/model3/Models/5/all_p5_i50_t{num_topics}'
    print("Loading model:", model_name)
    lda_model = gensim.models.ldamodel.LdaModel.load(model_name)
    topic_list = lda_model.print_topics(num_topics=5, num_words=10)
    print(topic_list)
    perplexity_list.append(lda_model.log_perplexity(corpus))

    # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    top_topics = lda_model.top_topics(corpus)
    avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    coherence_list.append(avg_topic_coherence)

perplexity_list = np.asarray(perplexity_list)
coherence_list = np.asarray(coherence_list)

font_size=16

# ticks
t = np.asarray(range(len(x_labels)))

# main plot
fig, ax1 = plt.subplots(figsize=(10, 6))
plt.xticks(t, x_labels, rotation=90)
ax1.set_xlabel('Topics', fontsize=font_size)

# subplot 1
color = 'tab:red'
ax1.set_ylabel('Perplexity', color=color, fontsize=font_size)
p1 = ax1.plot(t, perplexity_list, marker='o', color=color, label = 'Perplexity')
b, m = polyfit(t, perplexity_list, 1)
# plt.plot(t, b + m * t, '--', color=color)
ax1.tick_params(axis='y', labelcolor=color)
# ax1.set_ylim([0, 0.26])
for tick in ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(font_size-1)

# instantiate a second axes that shares the same x-axis
ax2 = ax1.twinx()

# subplot 2
color = 'tab:blue'
ax2.set_ylabel('Model Coherence', color=color, fontsize=font_size)  # we already handled the x-label with ax1
p2 = ax2.plot(t, coherence_list, marker='o', color=color, label = 'Model Coherence')
b, m = polyfit(t, coherence_list, 1)
# plt.plot(t, b + m * t, '--', color=color)
ax2.tick_params(axis='y', labelcolor=color)
# ax2.set_ylim([0, 0.131])

# ax1.xaxis.set_minor_locator(ticker.IndexLocator(base=1, offset=1))
# plt.xticks(list(range(len(x_labels))), x_labels, rotation=20)
# for tick in ax1.xaxis.get_major_ticks():
#     tick.label.set_fontsize(font_size-1)

# Pad margins so that markers don't get clipped by the axes
plt.margins(0.1)

plt.yticks(fontsize=font_size-1)
# fig.tight_layout()  # otherwise the right y-label is slightly clipped
lns = p1+p2
labs = [l.get_label() for l in lns]

# adjust legends location
ax1.legend(lns, labs, loc=0)

# plt.title("", fontsize=font_size)

plt.show()
fig.savefig("/data_8t/lmh_total/model3/pc5.pdf", bbox_inches='tight')
