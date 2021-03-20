s# Print fomatting with Strings Practice

#There's three ways to do string formatting
#1 - With the modulo character "%" - it acts as a placeholder and can work with one or multiple strings:
print("Currently Playing: %s" %"So Gone - Monica")
print("Currently %s: %s" %("Playing","So Gone - Monica"))

#Also can use variables instead
x,y = "Currently Playing:", "On Fire - Lloyd Banks"
print("%s %s"%(x,y))

# %s and %r can be used in this sense. %r is based of the repr() function.
# %r delivers the "string representation" of the object which includes any quotation marks and escape characters
print("My name is %r" %"Meghan")
print("My name is %s" %"Meghan")

# Can also use escape characters to see this difference.
# \n will produce a new line
print("My name is: %r" %"\nMeghan")
print("My name is: %s" %"\nMeghan")

# The s% operator will convert numbers into strings.
# The %d operator will convert numbers into integers first.
print("I am %s years old" %30.8)
print("I am %d years old" %30.8)

# Floating point (decimal) numbers are indicated by #.#f 
# First number the the minimum numbers of characters in the string should contain.
# The Sceond number in the exact amount of numbers that should be shown after the decimal point.
print("5 characters and 2 decimals: %5.2f" %12.345) # last numbers is cut off so only shows 4 numbers.
print("1 character and 0 decimals: %1.0f" %12.345)
print("1 character and 5 decimals: %1.5f" %12.345)
print("10 characters and 2 decimals: %10.2f" %12.345)
print("25 characters and 2 decimals: %25.2f" %12.345)

# You can also do multiple formatting
print("First Name: %s\n Last Name: %r\n Age: %2.0f" %("Meghan", "Harris", 30))

#2 - With the .format method:
# Inserted objects can be called by index position
print("Last Name {1}, First Name {0}".format("Meghan","Harris"))

# Inserted objects can also be assigned keywords
print("First Name: {a}\nLast Name: {b}\nTitle: {c}".format(a = "Meghan", b = "Harris", c = "Data Integration Specialist" ))

# Assignments allow for words to be used multiple times, avoiding duplication.
print("As a {a} specialist, I work with {a} everyday. I love working with {a}!".format(a = "data"))

# You can alter alignment, padding, and precision with the.format function also.
print('{0:6} | {1:7}'.format('Game', 'Type')) #First number in the brackets represents the element in the .format call. Second number is the field length that's printed.
print('{0:6} | {1:7}'.format('Portal 2', 'Puzzle'))
print('{0:6} | {1:7}'.format('Stardew Valley', 'Farming Simulator'))
print('{0:6} | {1:7}'.format('Minecraft', 'RPG Sandbox'))

# The .fromat function aligns text to the left and numbers to the right by default.
# You can pass optional calls to force the alignments(< left, ^ center, > right)
print('{0:<8} | {1:^8} | {2:>8}'.format('Left','Center','Right'))
print('{0:<8} | {1:^8} | {2:>8}'.format(11,22,33))

# You can also set alignments with a padding character placed after the colon.
print('{0:=<8} | {1:-^8} | {2:.>8}'.format('Left','Center','Right'))
print('{0:=<8} | {1:-^8} | {2:.>8}'.format(11,22,33))

# Field widths and floa precision are handled similarly to placeholders.
print("I am %1.0f years old today." %30)
print("I am {0:1.0f} years old today.".format(30))

# You can also formatted String Literals, which is the best option.
name = "Patches"
print(f"My dog's name is {name}.")

# You can pass the !r call to get the string representation.
print(f"My dog's name is {name!r}.")

# You can also do float formatting with literals. Precsision refers to the total number of digits.
num = 23.45678
print("My 10 character, four decimal number is:{0:10.4f}".format(num))
print(f"My 10 character, four decimal number is:{num:{10}.{6}}") #f-strings do not pad to the right of the decimal, even if precision allows it.




