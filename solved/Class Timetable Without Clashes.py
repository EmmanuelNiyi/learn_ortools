"""
ask: Class Timetable Without Clashes
You’re scheduling 3 classes: Math (M), Science (S), and History (H).

There are 5 time slots available: 1, 2, 3, 4, 5.

Math and Science cannot be in consecutive time slots (too much brain work).

History must be after Math.

All classes must be in different slots.

Goal: Find all possible valid schedules.
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
m = model.NewIntVar(1, 5, 'm')
s = model.NewIntVar(1, 5, 's')
h = model.NewIntVar(1, 5, 'h')
ms_diff = model.NewIntVar(0, 5, "ms_diff")
model.AddAbsEquality(ms_diff, m - s)

model.AddAllDifferent([m, s, h])
model.Add(ms_diff > 1)
model.Add(h > m)

# total_number = model.NewIntVar(1, 10, 'total_number')
# model.Add(total_number == (noa + nob + noo))
# model.Add(total_number >= 8)
#
# total_spent = model.NewIntVar(1, 50, 'total_spent')
# model.Add(total_spent == ((noa * 3) + ((nob * 2) + (noo * 4))))
# model.Add(total_spent <= 20)
# model.Maximize(nob)

# Solve
solver = cp_model.CpSolver()
solution_printer = AllSolutionsPrinter([m, s, h])
status = solver.SearchForAllSolutions(model, solution_printer)
# status = solver.Solve(model)

# Report
print(f"\nTotal solutions found: {solution_printer.SolutionCount()}")

# Display the result
if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print(f"m = {solver.Value(m)}, s = {solver.Value(s)}, h = {solver.Value(h)}, ")
    #       f"total_number = {solver.Value(total_number)}, total_spent = {solver.Value(total_spent)}")
    # print(f"Objective value = {solver.ObjectiveValue()}")

# """GPT SOLUTION""" Was wrong
from ortools.sat.python import cp_model

# Model
model = cp_model.CpModel()

# Variables: time slot for each class
M = model.NewIntVar(1, 5, 'Math')
S = model.NewIntVar(1, 5, 'Science')
H = model.NewIntVar(1, 5, 'History')

# All classes in different slots
model.AddAllDifferent([M, S, H])

# Math and Science not in consecutive slots
model.AddAbsEquality(model.NewIntVar(1, 4, 'diff_MS'), M - S)  # store abs(M - S)
model.Add(model.NewIntVar(1, 4, 'diff_MS') > 1)  # difference must be > 1

# History after Math
model.Add(H > M)

# Solve: find all solutions
# class AllSolutions(cp_model.CpSolverSolutionCallback):
#     def __init__(self, variables):
#         super().__init__()
#         self.variables = variables
#         self.count = 0
#     def OnSolutionCallback(self):
#         self.count += 1
#         print(f"Solution {self.count}: ", end="")
#         for v in self.variables:
#             print(f"{v.Name()}={self.Value(v)} ", end="")
#         print()
#
# solution_printer = AllSolutions([M, S, H])
# solver = cp_model.CpSolver()
# solver.SearchForAllSolutions(model, solution_printer)
#
# print(f"\nTotal solutions: {solution_printer.count}")

