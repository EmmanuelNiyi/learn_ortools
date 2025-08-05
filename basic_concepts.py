from ortools.sat.python import cp_model

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
alice = model.NewIntVar(1, 10, 'alice')
bob = model.NewIntVar(1, 10, 'bob')
charlie = model.NewIntVar(1, 10, 'charlie')


bonus_alice = model.NewBoolVar('bonus_alice')
bonus_bob = model.NewBoolVar('bonus_bob')
bonus_charlie = model.NewBoolVar('bonus_charlie')

# abs_value_1 = model.NewIntVar(0, 20, 'abs_value_1')
# abs_value_2 = model.NewIntVar(0, 20, 'abs_value_2')
# abs_value_3 = model.NewIntVar(0, 20, 'abs_value_3')

# Add constraints
model.Add(alice + bob + charlie == 15)

alice_gt_5 = model.NewBoolVar('alice_gt_5')
model.Add(alice > 5).OnlyEnforceIf(alice_gt_5)
model.Add(alice <= 5).OnlyEnforceIf(alice_gt_5.Not())
model.Add(bonus_alice == 1).OnlyEnforceIf(alice_gt_5 == 1)

bob_gt_5 = model.NewBoolVar('bob_gt_5')
model.Add(bob > 5).OnlyEnforceIf(bob_gt_5)
model.Add(bob <= 5).OnlyEnforceIf(bob_gt_5.Not())
model.Add(bonus_bob == 1).OnlyEnforceIf(bob_gt_5 == 1)

charlie_gt_5 = model.NewBoolVar('charlie_gt_5')
model.Add(charlie > 5).OnlyEnforceIf(charlie_gt_5)
model.Add(charlie <= 5).OnlyEnforceIf(charlie_gt_5.Not())
model.Add(bonus_charlie == 1).OnlyEnforceIf(charlie_gt_5)

model.Add(bonus_alice + bonus_bob + bonus_charlie <= 2)

# Solve
solver = cp_model.CpSolver()
solution_printer = AllSolutionsPrinter([alice, bob, charlie, bonus_alice, bonus_bob, bonus_charlie])
status = solver.SearchForAllSolutions(model, solution_printer)

# Report
print(f"\nTotal solutions found: {solution_printer.SolutionCount()}")

# Display the result
if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print(f"alice = {solver.Value(alice)}, bob = {solver.Value(bob)}, charlie = {solver.Value(charlie)}, bonus_alice = "
          f"{solver.Value(bonus_alice)}, bonus_bob = {solver.Value(bonus_bob)}, "
          f"bonus_charlie = {solver.Value(bonus_charlie)}")
