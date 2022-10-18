import nltk
import sys
import os
import string

nltk.download('stopwords')
print(nltk.corpus.stopwords.words("english"))
print(string.punctuation)

punctuation = list(string.punctuation)
stopwords = nltk.corpus.stopwords.words("english")

unwanted_words = set(punctuation + stopwords)

print(unwanted_words)