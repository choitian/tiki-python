dict = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221],
       "population": [200.4, 143.5, 1252, 1357, 52.98] }

import pandas as pd
brics = pd.DataFrame(dict)

brics.index = ["BR", "RU", "IN", "CH", "SA"]
print(brics)

brics.to_csv("countrys.scv")

print(brics['country'])
print(brics['area'])

print(brics[['area','population']])


print(brics[:-2])

print(brics.iloc[2])
print(brics.loc[['CH']])
print(brics.loc['CH'])
print(brics.loc[['CH','SA']])