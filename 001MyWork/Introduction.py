# Introduction
print('Hi...')
# intro end


# Python 3 Basic Begin


# 1. Variable and data Structure Begin

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
""""In this section, we will learn how to take input from the user and hence manipulate it or simply display it. 
input() function is used to take input from the user."""

name = input('Enter Your name.. ')
print('hello', name)


num1 = int(input('Num1 : '))
num2 = int(input('Num2 : '))
num3 = num1*num2
print('Product is : ', num3)

# 2. Input and Output End


# Python 3 Basic End
