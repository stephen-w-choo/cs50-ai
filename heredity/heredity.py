import csv
import itertools
from ntpath import join
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.

        # for each person, calculate probability that
        # they have
    }
    """

    """
    for each person, calculate probability that
    1. They have the specific number of genes that they have
        if they have no known parents, get the PROBS["gene"] probability
        else work it out from the number of genes that their parents have

        1a. Working it out from the parents
            if they have no copies of the gene
                probability of parent passing no copies multiplied together
            if they have 1 copy of the gene
                probability of each parent passing 1 copy added together
            if they have 2 copies
                probability of both parents pasing 1 copy multiplied together
    
    2. They have the trait given a certain number of genes
    """

    # Calculates probability of having a trait given a number of genes
    def trait_probability(person_gene_number):
        if person in have_trait:
            return PROBS["trait"][person_gene_number][True]
        else:
            return PROBS["trait"][person_gene_number][False]

    # Takes a person and returns the no_of genes they are assumed to have 
    def gene_no(person):
        if person in one_gene:
            return 1
        elif person in two_genes:
            return 2
        else:
            return 0

    # Takes a person and return the probability that they have a certain number of genes
    def gene_number_probability(person):
        # dictionary of probabilities of passing the gene on given a number of genes
        inheritance_probability = {
            0: PROBS["mutation"],
            1: 0.5,
            2: (1 - PROBS["mutation"])
        }

        person_gene_number = gene_no(person)
        father_inheritance_probability = inheritance_probability[gene_no(people[person]["father"])]
        mother_inheritance_probability = inheritance_probability[gene_no(people[person]["mother"])]

        # returns the baseline probability if no parents
        if not people[person]["mother"] or not people[person]["father"]:
            return PROBS["gene"][person_gene_number]
        
        # otherwise
        # if they have no copies of the gene, probability of parents passing no copies multiplied
        if person_gene_number == 0:
            # only one case - both parents have to NOT pass on the gene
            return (1 - father_inheritance_probability) * (1 - mother_inheritance_probability)
        if person_gene_number == 1:
            # case 1  - inherits from father
            father_case = father_inheritance_probability * (1 - mother_inheritance_probability)
            # case 2 - inherits from mother
            mother_case = (1 - father_inheritance_probability) * mother_inheritance_probability
            return father_case + mother_case
        if person_gene_number == 2:
            # only one case - both parents MUST pass on the gene
            return father_inheritance_probability * mother_inheritance_probability

    joint_prob_val = 1
    for person in people:
        person_prob_val = trait_probability(gene_no(person)) * gene_number_probability(person)
        joint_prob_val = person_prob_val * joint_prob_val
    
    return joint_prob_val
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Takes a person and returns the no_of genes they are assumed to have 
    def gene_no(person):
        if person in one_gene:
            return 1
        elif person in two_genes:
            return 2
        else:
            return 0

    for person in probabilities:
        person_gene_number = gene_no(person)
        if person in have_trait:
            trait = True
        else:
            trait = False
        probabilities[person]["gene"][person_gene_number] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        person_dict = probabilities[person]
        person_gene_dict = person_dict["gene"]
        gene_probability_total = sum(person_gene_dict.values())
        for gene_no in person_gene_dict:
            person_gene_dict[gene_no] = person_gene_dict[gene_no] / gene_probability_total
        
        person_trait_dict = person_dict["trait"]
        trait_probability_total = sum(person_trait_dict.values())
        for trait_presence in person_trait_dict:
            person_trait_dict[trait_presence] = person_trait_dict[trait_presence] / trait_probability_total


if __name__ == "__main__":
    main()
    