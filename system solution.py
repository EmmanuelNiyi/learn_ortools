from ortools.sat.python import cp_model


class AllSolutionsPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, hours, bonuses):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._hours = hours
        self._bonuses = bonuses
        self._solution_count = 0

    def OnSolutionCallback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}:")
        for person in self._hours:
            name = person.Name()
            hrs = self.Value(person)
            bonus = self.Value(self._bonuses[person])
            print(f"  {name} = {hrs} hours, Bonus: {'Yes' if bonus else 'No'}")
        print()

    def SolutionCount(self):
        return self._solution_count


# Create model
model = cp_model.CpModel()

# Define variables for each person’s hours
alice = model.NewIntVar(1, 10, 'alice')
bob = model.NewIntVar(1, 10, 'bob')
charlie = model.NewIntVar(1, 10, 'charlie')

# Total hours must be exactly 15
model.Add(alice + bob + charlie == 15)

# Define bonus indicator variables (Boolean)
bonus_alice = model.NewBoolVar('bonus_alice')
bonus_bob = model.NewBoolVar('bonus_bob')
bonus_charlie = model.NewBoolVar('bonus_charlie')

# Link bonuses to hours worked
model.Add(alice > 5).OnlyEnforceIf(bonus_alice)
model.Add(alice <= 5).OnlyEnforceIf(bonus_alice.Not())

model.Add(bob > 5).OnlyEnforceIf(bonus_bob)
model.Add(bob <= 5).OnlyEnforceIf(bonus_bob.Not())

model.Add(charlie > 5).OnlyEnforceIf(bonus_charlie)
model.Add(charlie <= 5).OnlyEnforceIf(bonus_charlie.Not())

# At most 2 people can get the bonus
model.Add(bonus_alice + bonus_bob + bonus_charlie <= 2)

# Solve
solver = cp_model.CpSolver()
printer = AllSolutionsPrinter(
    [alice, bob, charlie],
    {alice: bonus_alice, bob: bonus_bob, charlie: bonus_charlie}
)
status = solver.SearchForAllSolutions(model, printer)

print(f"\nTotal solutions found: {printer.SolutionCount()}")



# alice_gt_5 = model.NewBoolVar('alice_gt_5')
model.Add(alice > 5).OnlyEnforceIf(bonus_alice)
model.Add(alice <= 5).OnlyEnforceIf(bonus_alice.Not())
# model.Add(bonus_alice == 1).OnlyEnforceIf(alice_gt_5)

# bob_gt_5 = model.NewBoolVar('bob_gt_5')
model.Add(bob > 5).OnlyEnforceIf(bonus_bob)
model.Add(bob <= 5).OnlyEnforceIf(bonus_bob.Not())
# model.Add(bonus_bob == 1).OnlyEnforceIf(bob_gt_5)

# charlie_gt_5 = model.NewBoolVar('charlie_gt_5')
model.Add(charlie > 5).OnlyEnforceIf(bonus_charlie)
model.Add(charlie <= 5).OnlyEnforceIf(bonus_charlie.Not())
# model.Add(bonus_charlie == 1).OnlyEnforceIf(charlie_gt_5)