import nltk
import sys
import os
import string
import math


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens


    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    res = {}
    # f.read() will return a string in text mode
    filenames = os.listdir(os.path.join(directory))
    for filename in filenames:
        if filename[-4:] == ".txt":
            file = open(os.path.join(directory, filename), "r")
            txt = file.read()
            res[filename] = txt
    
    return res


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    word_list = nltk.tokenize.word_tokenize(document)

    res = []

    punctuation = list(string.punctuation)
    stopwords = nltk.corpus.stopwords.words("english")

    unwanted_words = set(punctuation + stopwords)

    for word in word_list:
        word = word.lower()
        if word not in unwanted_words:
            res.append(word)

    return res


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # convert the document list of words into a hash for this function 
    # needed for faster lookups

    documents_hashes = {}
    
    for document in documents:
        documents_hashes[document] = set(documents[document])

    idf_dict = {}

    n_documents = len(documents)

    # initialise a dictionary for all the words in all the documents
    for document in documents_hashes:
        document_words = documents_hashes[document]
        for word in document_words:
            if word not in idf_dict:
                idf_dict[word] = 0
    
    # get the frequency of the number of times each word appears
    for word in idf_dict:
        for document in documents_hashes:
            if word in documents_hashes[document]:
                idf_dict[word] += 1
    
    # calculate idf based on frequency
    for word in idf_dict:
        idf_dict[word] = math.log(n_documents/idf_dict[word])
    
    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # initialise a dictionary of files and their total tf-idf score
    
    file_scores = {}
    for file in files:
        file_scores[file] = 0
    
    # go through the list of words and compute the tf-idf scores
    for file in files:
        for word in files[file]: # for each word in the document
            if word in query: # if the word is in the query
                file_scores[file] += idfs[word] # increase the score of that file by the word idf value
    
    # initialise a list of files
    file_rankings = list(file_scores.keys())

    # sort the list by 
    file_rankings.sort(key=lambda f: file_scores[f], reverse=True)

    return file_rankings[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # store the values as a list of [score, density]
    sentence_scores_and_density = {}


    for sentence in sentences:
        sentence_scores_and_density[sentence] = [0, 0]

    for sentence in sentences:
        inverse_sentence_length = 1/len(sentences[sentence])
        sentence_hash = set(sentences[sentence])
        for word in query:
            if word in sentence_hash:
                sentence_scores_and_density[sentence][0] += idfs[word]
                sentence_scores_and_density[sentence][1] += inverse_sentence_length

    sentence_rankings = list(sentence_scores_and_density.keys())

    sentence_rankings.sort(key=lambda s:(sentence_scores_and_density[s][0], sentence_scores_and_density[s][1]), reverse=True)

    return sentence_rankings[:n]


if __name__ == "__main__":
    main()
