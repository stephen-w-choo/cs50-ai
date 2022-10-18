import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


NONTERMINALS = """
S -> Chunk | Chunk Runon | Chunk Runon Runon | Chunk Runon Runon Runon
Runon -> AVP | Conj AVP | Chunk | Conj Chunk
Chunk -> NP AVP
VP -> V | V NP | P NP
AVP -> VP | Adv VP | VP Adv
NP -> N | Det N | Det AP N
AP -> Adj | Adj Adj | Adj Adj Adj
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = nltk.word_tokenize(sentence)

    res = []

    for word in sentence:
        newword = []
        for char in word:
            if char.isalpha():
                newword.append(char.lower())
        if newword:
            res.append("".join(newword))

    return res


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.

    Return value: list of nltk.tree objects, where each element has the label NP.
    """
    res = []
    # run a recursive DFS through the tree
    # iterate down to the leaf nodes - on the return, return either True (if NP phrase has already been found)
    # or False if NP phrase has not been found

    def recursion(node):
        found = False
        
        if len(node) > 0:
            for subtree in node:
                if recursion(subtree):
                    found = True

        # if NP phrase has not yet been found in a subtree, add the node if it's NP and set found to True
        if not found and node.label() == "NP":
            res.append(node)
            found = True
        
        return found

    return res


if __name__ == "__main__":
    main()
