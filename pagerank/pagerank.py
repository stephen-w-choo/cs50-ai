import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # the dictionary that will be returned
    res = {}

    # the corpus is given as an adjacency list
    # make a baseline weighting - evenly split due to the randomisation provided by the damping factor
    for node in corpus:
        res[node] = (1 - damping_factor) / len(corpus)

    page_links = corpus[page]

    # then divide up the remaining weight between any links on that particular page
    for link in page_links:
        res[link] += damping_factor / len(page_links)

    return res


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    transitions = {}
    pages = corpus.keys()
    for page in pages:
        transitions[page] = transition_model(corpus, page, damping_factor)

    def random_choice(probability_dictionary):
        # Takes a dictionary of probabilities that sum to 1 and returns a random page
        # Under the hood, it's converting the dictionary to cumulative weights and selecting it that way
        return random.choices(list(probability_dictionary.keys()), weights=list(probability_dictionary.values()), k = 1)[0]

    count = {}  
    current = random.choice(list(corpus.keys()))
    for i in range(n):
        nextpage = random_choice(transitions[current])
        if nextpage not in count:
            count[nextpage] = 0
        count[nextpage] += 1 / n
        current = nextpage
    
    return count

    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_num = len(corpus)
    page_ranks = {}
    for page in corpus:
        page_ranks[page] = 1 / page_num
    
    def new_page_rank(page_rank_dict):
        # Takes a dictionary of pages with associated pageranks and returns a new set of pageranks for the next iteration
        # formula: PageRank(page) = ((1 - damping_factor) / page_num) + damping_factor * (sum of all (PageRank of pages that link to page)/(number of links of PageRank(i)) )
        new_page_ranks = {}
        
        for page in corpus:
            new_page_ranks[page] = (1 - damping_factor) / page_num
        
        for page in corpus:
            list_of_links = corpus[page] # list of pages that this page links to
            for page_link in list_of_links:
                new_page_ranks[page_link] += 0.85 * (page_rank_dict[page] / len(list_of_links))

        return new_page_ranks
    
    for i in range(SAMPLES):
        page_ranks = new_page_rank(page_ranks)
    print(page_ranks)
    return page_ranks
        
    
    


    raise NotImplementedError


if __name__ == "__main__":
    main()
