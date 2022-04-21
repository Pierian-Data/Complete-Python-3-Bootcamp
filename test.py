import IPython.display as ip

name = input("What is your name? ")

age = input("What is your age? ")

address = input("What is your address? ")


if age.isdigit():
    pass
else:
    age = ip.clear_output()
    print ("age is been cleared")
    print (f"value of age now is {age}")


