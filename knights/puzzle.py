from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
'''
Logic: 
AKnight and AKnave cannot both be true (exclusive or)
If A is a Knight, then AKnave and AKnight are both true
'''

knowledge0 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight,AKnave))),
    Biconditional(AKnight, And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

'''
Logic: If A is a Knight - it implies they are both Knaves
A has to be either a Knight or a Knave
B has to be either a Knight or a Knave
'''

knowledge1 = And(
    Biconditional(AKnight, And(AKnave, BKnave)),
    And(Or(AKnight, AKnave), Not(And(AKnight,AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight,BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnight, Or(And(AKnight,BKnight), And(AKnave,BKnave))),
    Biconditional(BKnight, Or(And(AKnight,BKnave), And(BKnight,AKnave))),
    And(Or(AKnight, AKnave), Not(And(AKnight,AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight,BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

'''
A saying 'I am a knave' is an obvious logical paradox, and can be represented as biconditional(AKnave, AKnight),
an obviously false statement when we know that A cannot be both a Knave and a Knight.
'''


knowledge3 = And(
    Or(Biconditional(AKnight, AKnight), Biconditional(AKnave, AKnight)),
    Biconditional(BKnight,  Biconditional(AKnave, AKnight)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight),
    And(Or(AKnight, AKnave), Not(And(AKnight,AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight,BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight,CKnave))),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
