# Use the help function to see what each function does.
# Delete this when you are done.
help(dir)
help(hasattr)
help(id)

# Define the Vehicle class.
class Vehicle:
    name = ""
    kind = "car"
    color = ""
    value = 100.00
    def description(self):
        desc_str = "%s is a %s %s worth $%.2f." % (self.name, self.color, self.kind, self.value)
        return desc_str


class Plane:
    name = ""
    kind = "car"
    color = ""
    value = 100.00
    def description(self):
        desc_str = "%s is a %s %s worth $%.2f." % (self.name, self.color, self.kind, self.value)
        return desc_str
       
car  = Vehicle()

print(id(car))
print(type(car))
print(repr(car))
print(callable(car))
print(issubclass(Vehicle,Plane))
print(isinstance(100,int))


def print_msg(number):
    def printer():
        "Here we are using the nonlocal keyword"
        #nonlocal number
        number=3
        print(number)
    printer()
    print(number)

print_msg(9)


def transmit_to_space(message):
    "This is the enclosing function"
    def data_transmitter():
        "The nested function"
        print(message)
    return data_transmitter

fun = transmit_to_space("12345")

fun()

# your code goes here
def multiplier_of(scale):
    realScale = scale
    "This is the enclosing function"
    def data_transmitter(value):
        print(realScale * value)
    return data_transmitter


multiplywith5 = multiplier_of(5)
multiplywith5(9)


def callTwice(oldFun):
    def newFun(value):
        return oldFun(oldFun(value))
    return newFun

def double_out(old_function):
    def new_function(*args, **kwds):
        return 2 * old_function(*args, **kwds) # modify the return value
    return new_function

def checkArg(old_function):
    def new_function(arg):
        if arg < 0: raise (ValueError, "Negative Argument") # This causes an error, which is better than it doing the wrong thing
        return old_function(arg)
    return new_function

@checkArg
@callTwice
@double_out
def mulBy10(value):
    return value *10


ret = mulBy10(9)
print(ret)

def multiply(multiplier):
    def multiply_generator(old_function):
        def new_function(*args, **kwds):
            return multiplier * old_function(*args, **kwds)
        return new_function
    return multiply_generator # it returns the new generator

val = 5
# Usage
@multiply(val) # multiply is not a generator, but multiply(3) is
def return_num(num):
    return num

# Now return_num is decorated and reassigned into itself
print(return_num(5)) # should return 15





def type_check(correct_type):
    def multiply_generator(old_function):
        def new_function(value):
            if not isinstance(value,correct_type):
                print("expect type '%s'" % correct_type)
                return value
            return old_function(value)
        return new_function
    return multiply_generator # it returns the new generator

@type_check(int)
def times2(num):
    return num*2

print(times2(2))
print(times2('Not A Number'))

@type_check(str)
def first_letter(word):
    return word[0]

print(first_letter('Hello World'))
print(first_letter(['Not', 'A', 'String']))
