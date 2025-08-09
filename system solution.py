from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.solution_count = 0

    def OnSolutionCallback(self):
        self.solution_count += 1
        values = {var.Name(): self.Value(var) for var in self.variables}
        print(f"Solution {self.solution_count}: A={values['A']}, B={values['B']}, C={values['C']}, D={values['D']} "
              f"→ {10*values['A']+values['B']} + {10*values['B']+values['C']} = {10*values['C']+values['D']}")

model = cp_model.CpModel()

# Variables: digits from 1–9
A = model.NewIntVar(1, 9, 'A')
B = model.NewIntVar(1, 9, 'B')
C = model.NewIntVar(1, 9, 'C')
D = model.NewIntVar(1, 9, 'D')

# All letters must be different
model.AddAllDifferent([A, B, C, D])

# Cryptarithm constraint: AB + BC = CD
model.Add((10*A + B) + (10*B + C) == (10*C + D))

# Solve
solver = cp_model.CpSolver()
solution_printer = SolutionPrinter([A, B, C, D])
solver.SearchForAllSolutions(model, solution_printer)

print(f"Total solutions found: {solution_printer.solution_count}")
