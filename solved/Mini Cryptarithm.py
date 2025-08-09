"""
**Challenge:**

Solve a simpler version of a cryptarithm:

```
AB + BC = CD
```
Where each letter is a digit from 1–9, and A ≠ 0, C ≠ 0.
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
a = model.NewIntVar(1, 9, 'a')
b = model.NewIntVar(1, 9, 'b')
c = model.NewIntVar(1, 9, 'c')
d = model.NewIntVar(1, 9, 'd')

model.AddAllDifferent([a, b, c, d])

ab = model.NewIntVar(1, 100, 'ab')
bc = model.NewIntVar(1, 100, 'bc')
cd = model.NewIntVar(1, 100, 'cd')

model.Add(ab == a*10 + b)
model.Add(bc == b*10 + c)
model.Add(cd == c*10 + d)

model.Add(ab + bc == cd)

# Solve
solver = cp_model.CpSolver()
solution_printer = AllSolutionsPrinter([a, b, c, d, ab, bc, cd, ])
status = solver.SearchForAllSolutions(model, solution_printer)
# status = solver.Solve(model)

# Report
print(f"\nTotal solutions found: {solution_printer.SolutionCount()}")


model.Maximize(cd)
status = solver.Solve(model)

# Display the result
if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print(f"a = {solver.Value(a)}, b = {solver.Value(b)}, c = {solver.Value(c)}, "
          f"ab = {solver.Value(ab)}, bc = {solver.Value(bc)}, cd = {solver.Value(cd)}")
    print(f"Objective value = {solver.ObjectiveValue()}")



#
# """GPT SOLUTION"""
#
#
# from ortools.sat.python import cp_model
#
# # Create the model
# model = cp_model.CpModel()
#
# # Variables: how many of each fruit to buy
# A = model.NewIntVar(1, 20, 'Apples')   # must buy at least 1
# B = model.NewIntVar(1, 20, 'Bananas')  # must buy at least 1
# O = model.NewIntVar(1, 20, 'Oranges')  # must buy at least 1
#
# # Total cost = 3*A + 2*B + 4*O must be exactly 20
# model.Add(3*A + 2*B + 4*O == 20)
#
# # Must have more than 8 fruits in total
# model.Add(A + B + O > 8)
#
# # Objective: Maximize the number of oranges
# model.Maximize(O)
#
# # Solve
# solver = cp_model.CpSolver()
# status = solver.Solve(model)
#
# # Result
# if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
#     print(f"Apples = {solver.Value(A)}")
#     print(f"Bananas = {solver.Value(B)}")
#     print(f"Oranges = {solver.Value(O)}")
#     print(f"Total fruits = {solver.Value(A) + solver.Value(B) + solver.Value(O)}")
#     print(f"Total cost = {3*solver.Value(A) + 2*solver.Value(B) + 4*solver.Value(O)}")
# else:
#     print("No solution found")
#
