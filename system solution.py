from ortools.sat.python import cp_model

class AllSolutionsPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, rows, cols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables
        self._rows = rows
        self._cols = cols
        self._solution_count = 0

    def OnSolutionCallback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}:")

        # Print the variables in a grid
        for r in range(self._rows):
            row_values = []
            for c in range(self._cols):
                index = r * self._cols + c
                row_values.append(self.Value(self._variables[index]))
            print(row_values)
        print()  # blank line between solutions

    def SolutionCount(self):
        return self._solution_count

model = cp_model.CpModel()

# Variables: 1–9 for each cell
cells = [model.NewIntVar(1, 9, f'cell_{i}') for i in range(9)]

# All numbers must be different
model.AddAllDifferent(cells)

# Helper to access cells by (row, col)
def cell(r, c):
    return cells[r * 3 + c]

# Magic constant for 3x3
magic_sum = 15

# Row constraints
for r in range(3):
    model.Add(sum(cell(r, c) for c in range(3)) == magic_sum)

# Column constraints
for c in range(3):
    model.Add(sum(cell(r, c) for r in range(3)) == magic_sum)

# Diagonal constraints
model.Add(cell(0, 0) + cell(1, 1) + cell(2, 2) == magic_sum)
model.Add(cell(0, 2) + cell(1, 1) + cell(2, 0) == magic_sum)

# Solve
solver = cp_model.CpSolver()
solution_printer = AllSolutionsPrinter(cells, 3, 3)
status = solver.SearchForAllSolutions(model, solution_printer)
status = solver.Solve(model)

print(f"\nTotal solutions found: {solution_printer.SolutionCount()}")

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for r in range(3):
        print([solver.Value(cell(r, c)) for c in range(3)])
else:
    print("No solution found.")
