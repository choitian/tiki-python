sentence = "the quick brown fox jumps over the lazy dog"
words = sentence.split()
word_lengths = []
for word in words:
      if word != "the":
          word_lengths.append(len(word))
print(words)
print(word_lengths)


sentence = "the quick brown fox jumps over the lazy dog"
words = sentence.split()
word_lengths = [len(word) for word in words if word != "the"]
print(words)
print(word_lengths)


def foo(first, second, third, *therest):
    print("First: %s" % first)
    print("Second: %s" % second)
    print("Third: %s" % third)
    
    print(type(therest))
    
    print("And all the rest... %s" % list(therest))
    print("last: %s" % therest[len(therest)-1])
    

foo(1,2,3,4,5,6,7,8,9)

def bar(first, second, third, **options):
    if options.get("action") == "sum":
        print("The sum is: %d" %(first + second + third))

    print(type(options))
    
    if options.get("number") == "first":
        return first
    return third

result = bar(1, 2, 3, action = "sum", number = "not first")
print("Result: %d" %(result))