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
class AllSolutions(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        super().__init__()
        self.variables = variables
        self.count = 0
    def OnSolutionCallback(self):
        self.count += 1
        print(f"Solution {self.count}: ", end="")
        for v in self.variables:
            print(f"{v.Name()}={self.Value(v)} ", end="")
        print()

solution_printer = AllSolutions([M, S, H])
solver = cp_model.CpSolver()
solver.SearchForAllSolutions(model, solution_printer)

print(f"\nTotal solutions: {solution_printer.count}")
