# Python3 code to demonstrate
# to find first position of character
# in a given string

# Initializing string
ini_string1 = 'xyze'

# Character to find
c = "b"
# printing initial string and character
print ("initial_strings : ", ini_string1,
			"\ncharacter_to_find : ", c)

# Using index Method
try:
	res = ini_string1.index(c)
	print ("Character {} in string {} is present at {}".format(
								c, ini_string1, str(res + 1)))
except ValueError as e:
	print ("No such character available in string {}".format(ini_string1))
