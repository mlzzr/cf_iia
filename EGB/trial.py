import numpy as np
for k in range(100):
    print(np.random.choice(2, p=[.9, .1]) + 1)
