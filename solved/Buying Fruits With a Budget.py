"""
Task: Buying Fruits With a Budget
You are buying apples (A), bananas (B), and oranges (O).

Apples cost 3 units each.

Bananas cost 2 units each.

Oranges cost 4 units each.

You have exactly 20 units to spend.
You must buy at least 1 of each fruit.
The total number of fruits must be more than 8.

Goal:
Find a combination that maximizes the number of bananas you buy.
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
noa = model.NewIntVar(1, 7, 'noa')
nob = model.NewIntVar(1, 10, 'nob')
noo = model.NewIntVar(1, 5, 'noo')

total_number = model.NewIntVar(1, 10, 'total_number')
model.Add(total_number == (noa + nob + noo))
model.Add(total_number >= 8)

total_spent = model.NewIntVar(1, 50, 'total_spent')
model.Add(total_spent == ((noa*3)+((nob*2)+(noo*4))))
model.Add(total_spent <= 20)
model.Maximize(nob)

# Solve
solver = cp_model.CpSolver()
solution_printer = AllSolutionsPrinter([noa, nob, noo, total_spent, total_number])
# status = solver.SearchForAllSolutions(model, solution_printer)
status = solver.Solve(model)

# Report
print(f"\nTotal solutions found: {solution_printer.SolutionCount()}")

# Display the result
if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print(f"noa = {solver.Value(noa)}, nob = {solver.Value(nob)}, noo = {solver.Value(noo)}, "
          f"total_number = {solver.Value(total_number)}, total_spent = {solver.Value(total_spent)}")
    print(f"Objective value = {solver.ObjectiveValue()}")




"""GPT SOLUTION"""


from ortools.sat.python import cp_model

# Create the model
model = cp_model.CpModel()

# Variables: how many of each fruit to buy
A = model.NewIntVar(1, 20, 'Apples')   # must buy at least 1
B = model.NewIntVar(1, 20, 'Bananas')  # must buy at least 1
O = model.NewIntVar(1, 20, 'Oranges')  # must buy at least 1

# Total cost = 3*A + 2*B + 4*O must be exactly 20
model.Add(3*A + 2*B + 4*O == 20)

# Must have more than 8 fruits in total
model.Add(A + B + O > 8)

# Objective: Maximize the number of oranges
model.Maximize(O)

# Solve
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Result
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Apples = {solver.Value(A)}")
    print(f"Bananas = {solver.Value(B)}")
    print(f"Oranges = {solver.Value(O)}")
    print(f"Total fruits = {solver.Value(A) + solver.Value(B) + solver.Value(O)}")
    print(f"Total cost = {3*solver.Value(A) + 2*solver.Value(B) + 4*solver.Value(O)}")
else:
    print("No solution found")
