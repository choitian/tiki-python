# Create 2 new lists height and weight
height = [1.0,  1.87, 10.0, 1.91, 1.90, 1.85]
weight = [81.65, 97.52, 95.25, 92.98, 86.18, 88.45]

# Import the numpy package as np
import numpy as np

# Create 2 numpy arrays from height and weight
np_height = np.array(height)
np_weight = np.array(weight)
print(type(np_height))

# Calculate bmi
bmi = np_weight / np_height
bmiAdd = np_weight + np_height
# Print the result




print(bmi)
print(bmiAdd)

print(bmi[bmi > 23])