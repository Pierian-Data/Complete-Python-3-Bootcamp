# String Notes in Python====

# Creating strings in Python is similar to R.
string = "Meghan Harris"

#You can print a string by calling the variable or using the "print" function
string
print(string)

# Checking the length of a string.
len(string)

# Python uses zero-based indexing so starts at "0" instead of "1".
# Pulling the first element out of the string. 
string[0]

# The colon is how we can perform slicing. 
# The statements are usually evaluated as "Up to but not including"
string[0:3] #Only pulls elements 0,1 and 2 - "Meg

# Negative indexing can be used to go backwards.
string[-1] # Last letter (one index behind 0 so it loops back around)

# Grabbing everything but the last letter.
string[:-1]

# Slicing can also be used for sequenced grabbing.
# Two colons in a row with tell python this is what we want to do.
# Numbers before the column provide the starting position
# Numbers after the column provide the step size.
string[::2] #Starting from the first element
string[1::2] #Starting from the second element

# This can be use to print a string backwards.
string[::-1]

# Strings have "immutability" meaning that they can't be changed once created
# In order to change strings, you'd need to reassign them completely if desired
string[7] = " Santiago "
string = "Meghan Santiago Harris"
print(string)

# The multiplication symbol can be used for replication.
song = "WAP "
song * 3

# Addition can also be used.
song + song + song

# Python has basic built-in string methods. 
# Methods are called with a "period" and then the methods name:

# Uppercasing a string with built-in methods. Parenthesis are needed!
string.upper()

# Lowercasing a string
string.lower()

# Splitting a string (by a blank space is the default)
string.split()

# Splitting by "H".
string.split("H") # Whatever you're splitting on gets removed

# Print formatting. The .format function can be used to add formatted objects to printed string statments.
# This won't change the strings, but will add to them with the curly square brackets.

"Currently Playing: {}".format("Fantasy - Mariah Carey")
