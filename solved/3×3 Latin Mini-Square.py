"""
Fill the 3×3 grid
a b c
d e f
g h i
with digits 1–3 so that every row and every column contains each digit exactly once.
"""

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


# Create the model
model = cp_model.CpModel()

# Create 9 variables for the 3x3 grid, domain 1..3
cells = []
for i in range(9):
    var = model.NewIntVar(1, 3, f'cell_{i}')
    cells.append(var)


def get_index_value(row, col):
    return cells[row * 3 + col]


# Row constraints: each row must have all different values (1, 2, 3)
for r in range(3):
    row_vars = []
    for c in range(3):
        row_vars.append(get_index_value(r, c))
    model.AddAllDifferent(row_vars)

# column constraints: each column mut have all different values (1,2,3)
for c in range(3):
    column_values = []
    for r in range(3):
        column_value = get_index_value(r, c)
        column_values.append(column_value)
    model.AddAllDifferent(column_values)

# Solve and print one solution
solver = cp_model.CpSolver()
solution_printer = AllSolutionsPrinter(cells, 3, 3)
status = solver.SearchForAllSolutions(model, solution_printer)
status = solver.Solve(model)

print(f"\nTotal solutions found: {solution_printer.SolutionCount()}")

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for r in range(3):
        row_values = []
        for c in range(3):
            row_values.append(solver.Value(get_index_value(r, c)))
        print(row_values)
else:
    print("No solution found.")





"""SOLUTION"""
# from ortools.sat.python import cp_model
#
# model = cp_model.CpModel()
#
# # Create 9 variables for the 3x3 grid, domain 1..3
# cells = [model.NewIntVar(1, 3, f'cell_{i}') for i in range(9)]
#
# def cell(r, c):
#     return cells[r * 3 + c]
#
# # Row constraints: each row must have all different values (1,2,3)
# for r in range(3):
#     model.AddAllDifferent([cell(r, c) for c in range(3)])
#
# # Column constraints: each column must have all different values (1,2,3)
# for c in range(3):
#     model.AddAllDifferent([cell(r, c) for r in range(3)])
#
# # Solve and print one solution
# solver = cp_model.CpSolver()
# status = solver.Solve(model)
#
# if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
#     for r in range(3):
#         print([solver.Value(cell(r, c)) for c in range(3)])
# else:
#     print("No solution found.")
