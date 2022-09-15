import sys

from crossword import *

from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            var_length = var.length
            for word in set(self.domains[var]):
                if len(word) != var_length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        modified = False

        overlaps = self.crossword.overlaps[(x, y)]
        # overlap will be a tuple representing the character at which (x, y) overlap
        # they need to overlap at this specific character in order for the arc to be consistent
        
        
        for word1 in set(self.domains[x]): # iterate through a copy of the set
            consistent = False
            for word2 in self.domains[y]:
                if word1[overlaps[0]] == word2[overlaps[1]]:
                    consistent = True
            if not consistent:
                self.domains[x].remove(word1)
                modified = True
        
        return modified

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        queue = all arcs in csp
            while queue non-empty:
            (X, Y) = Dequeue(queue)
            if Revise(csp, X, Y):
                if size of X.domain == 0:
                    return false
            for each Z in X.neighbors - {Y}:
                Enqueue(queue, (Z,X))
        return true
        """
        if not arcs:
            arc_queue = deque()
            for overlap in self.crossword.overlaps:
                if self.crossword.overlaps[overlap]:
                    arc_queue.append(overlap)
        else:
            arc_queue = deque(arcs)
        while arc_queue:
            current_arc = arc_queue.popleft()
            x, y = current_arc
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
            for z in self.crossword.neighbors(x):
                if z == y:
                    continue
                arc_queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # assume that unassigned variables will have a value of None
        for var in self.domains:
            if var not in assignment or not assignment[var]:
                return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.

        conditions:
        An assignment is consistent if 
        1 all values are distinct 
        2 every value is the correct length
        3 there are no conflicts between neighboring variables
        """
        # set to keep track of existing words to ensure distinct values
        seen = set()
        # checks each variable
        for var in assignment:
            word = assignment[var]
            if word in seen:
                return False
            if len(word) != var.length:
                return False

        # checks overlaps for conflicts between variables
        for x, y in self.crossword.overlaps:
            if x not in assignment or y not in assignment:
                continue
            word1 = assignment[x]
            word2 = assignment[y]
            intersection = self.crossword.overlaps[(x, y)]
            if intersection:
                if word1[intersection[0]] != word2[intersection[1]]:
                    return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        neighbors = self.crossword.neighbors(var)

        def count_consistent_vals(word):
            # Takes a word/value and checks neighbors
            ruled_out_count = 0
            for neighbor_variable in neighbors: # check the neighbouring variables for overlaps
                i, j = self.crossword.overlaps[(var, neighbor_variable)] # get the overlapping points
                for word2 in self.domains[neighbor_variable]:
                    if word[i] != word2[j]:
                        ruled_out_count += 1

            return ruled_out_count
        
        res = list(self.domains[var])

        res.sort(key=count_consistent_vals)

        return res

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        min_vals_remaining = float('inf')
        minvar = None

        for variable in self.domains:
            if variable not in assignment or not assignment[variable]:
                vals_remaining = len(self.domains[variable])
                
                if vals_remaining == min_vals_remaining: # checks for a tie
                    if len(self.crossword.neighbors(variable)) > len(self.crossword.neighbors(minvar)):
                        minvar = variable
                
                if vals_remaining < min_vals_remaining: # checks for a lower num of remaining values
                    min_vals_remaining = vals_remaining
                    minvar = variable
        
        return minvar

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.

        if assignment complete:
            return assignment
        var = Select-Unassigned-Var(assignment, csp)
        for value in Domain-Values(var, assignment, csp):
            if value consistent with assignment:
                add {var = value} to assignment
                result = Backtrack(assignment, csp)
                if result ≠ failure:
                    return result
                remove {var = value} from assignment
        return failure
        """
        if self.assignment_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(variable, assignment): #val will represent each word
            assignment[variable] = val
            if self.consistent(assignment):
                res = self.backtrack(assignment)
                if res:
                    return res # returns early if the assignment is complete
            del assignment[variable] # otherwise backtracks and removes assigned var
        
        return False # returns false if none of the paths lead anywhere


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
