def Change(var):
    var[0] = 'Changed'

variable = ['Original']
Change(variable)      
print(variable[0])