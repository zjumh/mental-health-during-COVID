import gensim
import codecs
import pandas as pd
import numpy as np
from ast import literal_eval
from gensim.models import LdaModel, LdaMulticore, LsiModel
from gensim.corpora import Dictionary
model_name = '/data_8t/lmh_total/model3/Models/5/all_p5_i50_t17'
print("Loading model:", model_name)
df = pd.read_csv("/data_8t/lmh_total/model3/mental_token.csv",keep_default_na=False)
print(len(df))
data = pd.read_csv("/data_8t/lmh_total/model3/mental.csv",low_memory=False, keep_default_na=False, lineterminator='\n')
print(len(data))
data['topic'] = "nan"
data['p'] = "nan"
# convert strings of lists to lists
df.tokens = df.tokens.apply(literal_eval)
corpus = df.tokens.values.tolist()
dictionary = Dictionary(corpus)
# changing these numbers can increase/decrease the run time if needed, but too exclusive will lead to worse results
no_below = 5
dictionary.filter_extremes(no_below=no_below, no_above=0.5)
corpus = [dictionary.doc2bow(tokens) for tokens in corpus]
#the p of the text in which topic
lda_model = gensim.models.ldamodel.LdaModel.load(model_name)
doc_topic = [a for a in lda_model[corpus]]
print(len(doc_topic))
topic = []
p = []
for i in range(0,len(doc_topic)):
    c = []
    t = doc_topic[i]
    c.append([a[1] for a in t])
    m = max(c[0])
    n = min(c[0])
    if len(c[0])==1:
        topic.append(t[0][0])
        p.append(t[0][1])
        #data.loc[i, 'topic'] = t[0][0]
        #data.loc[i, 'p'] = t[0][1]
    elif m == n:
        topic.append(100)
        p.append(0)              
        #data.loc[i, 'topic'] = 100
        #data.loc[i, 'p'] = 0
    else:
        for j in range(0, len(t)):
            if m in t[j]:
                topic.append(t[j][0])
                p.append(t[j][1])
                #data.loc[i, 'topic'] = t[j][0]
                #data.loc[i, 'p'] = t[j][1]
                break
data['topic'] = topic
data['p'] = p
data.to_csv("/data_8t/lmh_total/model3/topic17_5.csv")                