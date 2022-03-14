import pandas as pd
from nltk.tokenize import TweetTokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
tknzr = TweetTokenizer()
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.phrases import Phrases, Phraser
from ast import literal_eval
# the number of "stop words"
print("Stop words: ", len(STOPWORDS))
file_path = '/data_8t/lmh_total/model_merge/mental.csv'
df = pd.read_csv(file_path, keep_default_na=False, lineterminator='\n')
# remove @ handlers and lower texts
print(len(df))
df["full_text"] = df.full_text.str.replace(r"@\S+", '').str.lower()
print(len(df))
# use NLTK's TweetTokenizer to tokenize the full_text
df["tokens"] = df.full_text.apply(lambda x: tknzr.tokenize(x))
print(len(df))
# remove super short tokens such as "do", "re", etc (those with length <= 2)
# remove numerical values
# remove stop words
df["tokens"] = df.tokens.apply(lambda x: [t for t in x if len(t) > 2 and t.isalpha() and t not in STOPWORDS])
print(len(df))
# lemmatize tokens
df["tokens"] = df.tokens.apply(lambda x: [lemmatizer.lemmatize(t) for t in x])
print(len(df))
# add bigrams
#     # convert strings of lists to lists
#df.tokens = df.tokens.apply(literal_eval)

#     # add tokens from each tweet to the corpus
corpus = df.tokens.values.tolist()

#     # https://radimrehurek.com/gensim/models/phrases.html#gensim.models.phrases.Phraser
#     # default min_count=5
phrases = Phraser(Phrases(corpus))

#     # iterates through the corpus and adds bigram tokens to notes when appropriate, unigram components aren't removed
for i in range(len(corpus)):
    bigrams = [token for token in phrases[corpus[i]] if "_" in token]
    corpus[i].extend(bigrams)

#     # remove stop words
df["tokens"] = df.tokens.apply(lambda x: [t for t in x if t not in STOPWORDS])
print(len(df))
corpus = df.tokens.values.tolist()
long_string = ",".join([",".join([
        t for t in c
        if t not in ["covid", "pandemic"]
    ]) for c in corpus])
# # Create a WordCloud object
wordcloud = WordCloud(scale=4, random_state=0, background_color="white", max_words=5000, contour_width=3, contour_color='steelblue', collocations=False)

# # Generate a word cloud
wordcloud.generate(long_string)
plt.switch_backend('agg')
plt.switch_backend('Agg')
# # Visualize the word cloud
image = wordcloud.to_image()
image.show()
wordcloud.to_file('/data_8t/lmh_total/model3/mental.png')
#    # save tokens to files
file_name = '/data_8t/lmh_total/model3/mental_token.csv'
df[["user_id", "tokens"]].to_csv(file_name, index=False)


