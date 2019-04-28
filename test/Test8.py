a = set(["Jake", "John", "Eric"])
b = set(["John", "Jill"])

print(a.intersection(b))

print(a.symmetric_difference(b))
print(b.symmetric_difference(a))

print(a.difference(b))
print(b.difference(a))

print(a.union(b))


import json
json_string = json.dumps([1, 2, 3, "a", "b", "c"])
print(json_string)

import pickle
pickled_string = pickle.dumps([1, 2, 3, "a", "b", "c"])
print(pickle.loads(pickled_string))





# fix this function, so it adds the given name
# and salary pair to salaries_json, and return it
def add_employee(salaries_json, name, salary):
    # Add your code here
    salaries = json.loads(salaries_json)
    salaries[name] = salary
    print(type(salaries))
    print(json.dumps(salaries))
    print(type(json.dumps(salaries)))
    return json.dumps(salaries)

# test code
salaries = '{"Alfred" : 300, "Jane" : 400 }'
new_salaries = add_employee(salaries, "Me", 800)
decoded_salaries = json.loads(new_salaries)
print(type(decoded_salaries))
print(decoded_salaries["Alfred"])
print(decoded_salaries["Jane"])
print(decoded_salaries["Me"])




from functools import partial

def multiply(x,y,z):
        return x * y + z

# create a new function that multiplies by 2
mulByTen = partial(multiply,10)
print(mulByTen(2,4))