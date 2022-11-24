import itertools

test = set(["B", "C"])
testB = set(["C", "D"])

print(set(itertools.product(test, testB, repeat=1)))
