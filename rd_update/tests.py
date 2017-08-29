
import itertools

treatments = itertools.cycle(range(2))
dict= {}
for p in ['a', 'b', 'c']:
    dict[p] = next(treatments)
print(dict)