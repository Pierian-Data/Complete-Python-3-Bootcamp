# Written by *** for COMP9021
#
# Generates a random integer dim strictly greater than 2
# and a list of random digits of length dim.
#
# Outputs some text and two "pictures".
# The text clarifies what "pictures" are expected.
#
# There are a few blank lines in the output,
# including one at the very end.


from random import seed, randrange
import sys

try: 
    for_seed, dim = (int(x) for x in input('Enter two integers, the second '
                                           'one being 3 or more: '
                                          ).split()
                    )
    if dim <= 2:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
digits = [randrange(10) for _ in range(dim)]
print()
print(f'The chosen dimension is {dim}.')
print(f'Also, I have this sequence of {dim} digits for you:')
print(' ', digits)

# INSERT YOUR CODE HERE
contentWidth = 2*dim-1
instructionOne_1= 'Here is a first picture.'
instructionOne_2= 'There are spaces on each side of the star.'
instructionTwo_1= 'Here is a second picture.'
instructionTwo_2 = 'Top and bottom borders are complementary, because:'
instructionTwo_3 = '  0 is 9\'s "complement".'
instructionTwo_4 = '  1 is 8\'s "complement".'
instructionTwo_5 = '  2 is 7\'s "complement".'
instructionTwo_6 = '  ...'



def printInstructionOne():
  print()
  print(instructionOne_1)
  print(instructionOne_2.)
  print()

def printInstructionTwo():
  print()
  print(instructionTwo_1)
  print(instructionTwo_2)
  print(instructionTwo_3)
  print(instructionTwo_4)
  print(instructionTwo_5)
  print(instructionTwo_6)
  print()

def addingBars(innerContent):
  return '  |'+ innerContent + '|'

def drawOuterLine(filling):
  content = contentWidth*filling
  print(addingBars(content))

def drawInnerLineWith(fMid, fMidSides):
  content = ' '*(dim-2)+fMidSides+fMid+fMidSides+' '*(dim-2)
  print(addingBars(content))

def drawCenterLine():
  content = int(contentWidth/2)*' '+'*'+ int(contentWidth/2)*' '
  print(addingBars(content))

def complementary(intList):
 return [9-x for x in intList]

def drawFirstDigitsLine():
  content = '-'.join([str(i) for i in digits])
  print(addingBars(content))

def drawLastDigitsLine():
  content = '-'.join([str(i) for i in complementary(digits)])
  print(addingBars(content))
  print()

def drawFirstPicture():
  printInstructionOne()
  drawOuterLine('-')
  drawOuterLine(' ')
  drawCenterLine()
  drawOuterLine(' ')
  drawOuterLine('-')

def draw2ndPicture():
  printInstructionTwo()
  drawFirstDigitsLine()
  drawOuterLine(' ')
  drawInnerLineWith('-','-')
  drawInnerLineWith('*','|')
  drawInnerLineWith('-','-')
  drawOuterLine(' ')
  drawLastDigitsLine()

drawFirstPicture()
draw2ndPicture()
