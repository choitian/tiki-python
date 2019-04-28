def do_stuff_with_number(n):
        print(n)

the_list = (1, 2, 3, 4, 5)

for i in range(20):
    try:
        do_stuff_with_number(the_list[i])
        raise NameError('HiThere')
    except NameError as err: # Raised when accessing a non-existing index of a list
        print(err)
    except: # Raised when accessing a non-existing index of a list
        do_stuff_with_number(0)