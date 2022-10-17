import nltk
import sys
nltk.download('punkt')

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

"""
sentence patterns:
subject + verb
subject + verb + object
subject + verb + adverb
subject + verb + noun


Holmes sat down and lit his pipe.
N V Adv

I had a country walk on Thursday and came home in a dreadful mess.
N V Det Adj N P N Conj V N P Det Adj N


I had a little moist red paint in the palm of my hand.
N V Det Adj Adj Adj N P Det N P Det N

"""


NONTERMINALS = """
S -> S | S P S
SC -> NP V | NP V Adv
AP -> Adj | Adj Adj | Adj Adj Adj
VT -> V | AP V
VP -> VT NP
NP -> N | Det N | Det AP N
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
