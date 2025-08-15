"""
Task 3.3 — N-Queens

Goal: Place N queens on an N×N chessboard so no two queens attack each other (no two share the same row, column, or diagonal).

What you'll need to learn

Represent each row as a variable that gives the column position of the queen in that row.

NewIntVar to create variables with domain 0..N-1.

AddAllDifferent to ensure no two queens share a column.

Pairwise constraints for diagonals: for rows i != j, ensure col[i] + i != col[j] + j and col[i] - i != col[j] - j.

Writing a small solution printer to show board layouts or enumerate solutions.
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
            out_values = []
            for c in range(self._cols):
                index = r * self._cols + c
                row_values.append(self.Value(self._variables[index]))

            for val in row_values:
                if val == 1:
                    out_values.append("-")
                else:
                    out_values.append("Q")
            # print(row_values)
            print(out_values)
        print()  # blank line between solutions

    def SolutionCount(self):
        return self._solution_count


# Create the model
model = cp_model.CpModel()

n = 4
nsq = n * n
np1 = (n + 1)
nm1 = n - 1

# Create nsq variables for the nxn grid, domain 1..3
cells = []
for i in range(nsq):
    var = model.NewIntVar(1, 2, f'cell_{i}')
    cells.append(var)


def cell(row, col):
    return cells[row * n + col]


# Row constraints: each row must have all different values (1, 2 ... 9)
for r in range(n):
    row_vars = []
    for c in range(n):
        i_v = cell(r, c)
        row_vars.append(i_v)
    model.Add(sum(row_vars) < n + 2)

# column constraints: each column mut have all different values (1, 2 ... 9)
for c in range(n):
    column_values = []
    for r in range(n):
        column_value = cell(r, c)
        column_values.append(column_value)
    model.Add(sum(column_values) < n + 2)

# main diagonal constraints
main_diags = []
for start_col in range(n):  # start from top row
    diag = []
    r, c = 0, start_col
    while r < n and c < n:
        diag.append(cells[r * n + c])
        r += 1
        c += 1
    model.Add(sum(diag) < len(diag) + 2)
    main_diags.append(diag)

for start_row in range(1, n):  # start from first column
    diag = []
    r, c = start_row, 0
    while r < n and c < n:
        diag.append(cells[r * n + c])
        r += 1
        c += 1
    model.Add(sum(diag) < len(diag) + 2)
    main_diags.append(diag)

# enforce anti diagonal constraints
anti_diags = []
for start_col in range(n):  # start from top row
    diag = []
    r, c = 0, start_col
    while r < n and c >= 0:
        diag.append(cells[r * n + c])
        r += 1
        c -= 1
    model.Add(sum(diag) < len(diag) + 2)
    anti_diags.append(diag)

for start_row in range(1, n):  # start from last column
    diag = []
    r, c = start_row, n - 1
    while r < n and c >= 0:
        diag.append(cells[r * n + c])
        r += 1
        c -= 1
    model.Add(sum(diag) < len(diag) + 2)
    anti_diags.append(diag)

# enforce n number of queens
model.Add(sum(cells) == n * np1)

# Solve and print one solution
solver = cp_model.CpSolver()
solution_printer = AllSolutionsPrinter(cells, n, n)
status = solver.SearchForAllSolutions(model, solution_printer)


"""QUESTION SOLUTION"""
# from ortools.sat.python import cp_model
#
# def solve_n_queens(N=8, find_all=False, max_solutions=1000):
#     model = cp_model.CpModel()
#
#     # col[i] is column of queen in row i (0..N-1)
#     cols = [model.NewIntVar(0, N-1, f'col_{i}') for i in range(N)]
#
#     # No two queens in same column
#     model.AddAllDifferent(cols)
#
#     # No two queens on same diagonal
#     for i in range(N):
#         for j in range(i + 1, N):
#             model.Add(cols[i] + i != cols[j] + j)  # same main diagonal
#             model.Add(cols[i] - i != cols[j] - j)  # same anti-diagonal
#
#     solver = cp_model.CpSolver()
#     solver.parameters.max_time_in_seconds = 10.0  # optional: avoid very long runs for large N
#     solver.parameters.num_search_workers = 8     # use multiple threads if available
#
#     if not find_all:
#         status = solver.Solve(model)
#         if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
#             solution = [solver.Value(c) for c in cols]
#             print(f"One solution for N={N}: {solution}\n")
#             # Print board representation
#             for r in range(N):
#                 row = ['Q' if solution[r] == c else '.' for c in range(N)]
#                 print(' '.join(row))
#         else:
#             print("No solution found.")
#     else:
#         # Callback to collect all solutions (careful: number can grow quickly)
#         class AllSolPrinter(cp_model.CpSolverSolutionCallback):
#             def __init__(self, variables, limit):
#                 super().__init__()
#                 self.vars = variables
#                 self.count = 0
#                 self.limit = limit
#
#             def OnSolutionCallback(self):
#                 self.count += 1
#                 sol = [self.Value(v) for v in self.vars]
#                 print(f"Solution {self.count}: {sol}")
#                 # print board (optional)
#                 # for r in range(len(sol)):
#                 #     print(' '.join('Q' if sol[r]==c else '.' for c in range(len(sol))))
#                 # print()
#                 if self.count >= self.limit:
#                     print(f"Reached max_solutions={self.limit}, stopping search.")
#                     self.StopSearch()
#
#         printer = AllSolPrinter(cols, max_solutions)
#         solver.SearchForAllSolutions(model, printer)
#         print(f"Total solutions found (up to limit): {printer.count}")
#
# if __name__ == '__main__':
#     # Example: find one solution for N=8
#     solve_n_queens(N=8, find_all=False)
#
#     # Example: enumerate all solutions for N=4 (2 solutions)
#     # solve_n_queens(N=4, find_all=True, max_solutions=100)
