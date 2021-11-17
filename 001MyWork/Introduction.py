# Introduction
print('Hi...')
# intro end


# Python 3 Basic Begin


# 1. Variable and data Structure Begin
def variable_dataStructure():
    """In other programming languages like C, C++, and Java, you will need to declare the type of variables
    but in Python you don’t need to do that. Just type in the variable and when values will be given to it,
    then it will automatically know whether the value given would be an int, float, or char or even a String."""
    myNumber = 3
    print(myNumber)

    myNumber = 4.5
    print(myNumber)

    myNumber = 'Hello World'
    print(myNumber)

    """Python have 4 types of built in Data Structures namely List, Dictionary, Tuple and Set.
    List is the most basic Data Structure in python. 
    List is a mutable data structure i.e items can be added to list later after the list creation. 
    It’s like you are going to shop at the local market and made a list of some items and later on you can add more and more items to the list.
    append() function is used to add data to the list."""

    nums = []
    nums.append(21)
    nums.append(40.5)
    nums.append('Hello World')
    print(nums)
# 1. Variable and data Structure End


# 2. Input and Output Begin
def input_output():
    """"In this section, we will learn how to take input from the user and hence manipulate it or simply display it. 
    input() function is used to take input from the user."""

    name = input('Enter Your name.. ')
    print('hello', name)


    num1 = int(input('Num1 : '))
    num2 = int(input('Num2 : '))
    num3 = num1*num2
    print('Product is : ', num3)
# 2. Input and Output End


# 3. Selection Begin
def selection():
    """Selection in Python is made using the two keywords ‘if’ and ‘elif’ and else (elseif)"""
    num1=20
    if(num1<30):
        print('less than 30')
    elif(num1<50):
        print('less than 50')
    else:
        print('above 50')
# 3. Selection End


# 4. Function Begin
def function():
    """You can think of functions like a bunch of code that is intended to do a particular task in the whole Python script.
    Python used the keyword ‘def’ to define a function.
    Syntax:
    def function-name(arguments):
                #function body"""
    print('hello')
    print("hello again")

"""Now as we know any program starts from a ‘main’ function…
lets create a main function like in many other programming languages."""

def getInt():
    result=int(input('Enter num: '))
    return result

def Main():
    print('Main Started')
    output =getInt()
    print(output)

if __name__=='__main__':
    Main()

# 4. Function Endn 


# 5. Iteration (Looping) Begin
def iteration():
    """As the name suggests it calls repeating things again and again. We will use the most popular ‘for’ loop here."""
    for step in range(5):
        print(step)
# 5. Iteration (Looping) End


# 6. Modules Begin
import math
def modules():
    """Python has a very rich module library that has several functions to do many tasks. You can read more about Python’s standard library by Clicking here
    ‘import’ keyword is used to import a particular module into your python code. For instance consider the following program."""
    num=-85
    num=math.fabs(num)
    print(num)
# 6. Modules End


# Python 3 Basic End
