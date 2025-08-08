"""
✅ Task: Assign 4 Students to Unique Grades
You have 4 students: A, B, C, and D.

Each gets a grade from 1 to 4, and:

No two students can have the same grade.

A must have a better grade than B.

C must not get the worst grade (i.e. C ≠ 4).

D must get an even-numbered grade.


"""

from ortools.sat.python import cp_model


class AllSolutionsPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables
        self._solution_count = 0

    def OnSolutionCallback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}: ", end="")
        for var in self._variables:
            print(f"{var.Name()} = {self.Value(var)}", end="  ")
        print()

    def SolutionCount(self):
        return self._solution_count


# Create the model
model = cp_model.CpModel()

# Define variables
a = model.NewIntVar(1, 4, 'a')
b = model.NewIntVar(1, 4, 'b')
c = model.NewIntVar(1, 4, 'c')
d = model.NewIntVar(1, 4, 'd')

model.AddAllDifferent([a, b, c, d])
model.Add(a < b)
model.Add(c < 4)
model.AddModuloEquality(0, d, 2)

# Solve
solver = cp_model.CpSolver()
solution_printer = AllSolutionsPrinter([a, b, c, d])
status = solver.SearchForAllSolutions(model, solution_printer)

# Report
print(f"\nTotal solutions found: {solution_printer.SolutionCount()}")

# Display the result
if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print(f"a = {solver.Value(a)}, b = {solver.Value(b)}, c = {solver.Value(c)}, d = {solver.Value(d)}")





"""Solution"""


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables
        self._solution_count = 0

    def OnSolutionCallback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}: ", end="")
        for var in self._variables:
            print(f"{var.Name()} = {self.Value(var)}", end="  ")
        print()

    def SolutionCount(self):
        return self._solution_count


# Create the model
model = cp_model.CpModel()

# Variables: grades from 1 (best) to 4 (worst)
A = model.NewIntVar(1, 4, 'A')
B = model.NewIntVar(1, 4, 'B')
C = model.NewIntVar(1, 4, 'C')
D = model.NewIntVar(1, 4, 'D')

# All different grades
model.AddAllDifferent([A, B, C, D])

# Constraints
model.Add(A < B)          # A must have better grade than B
model.Add(C != 4)         # C must not have the worst grade
model.AddModuloEquality(0, D, 2)  # D must be even (2 or 4)

# Solve
solver = cp_model.CpSolver()
solution_printer = SolutionPrinter([A, B, C, D])
status = solver.SearchForAllSolutions(model, solution_printer)

# Summary
print(f"\nTotal solutions: {solution_printer.SolutionCount()}")
