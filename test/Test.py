import util.commons as commons


def main():
    phonebook = {"John" : 938477566,"Jack" : 938377264,"Jill" : 947662781}

    john = phonebook.pop("John")
    for name, number in phonebook.items():
        print("Phone number of %s is %d" % (name, number))
    
    commons.showSomething("hello is:" + john.__str__())


if __name__ == '__main__':
    main()


