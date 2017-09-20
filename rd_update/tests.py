import numpy as np

name = ['Bob', 'Mike']
senior, junior = np.random.permutation(name)
print(senior)
print(junior)

treatment = np.random.choice([1,2,3,4],  p=[.2,.3,.2,.3])
print(treatment)