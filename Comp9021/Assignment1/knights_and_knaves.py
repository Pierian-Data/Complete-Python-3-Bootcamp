# EDIT THE FILE WITH YOUR SOLUTION
import sys
import re


#FILE_NAME = input('Which text file do you want to use for the puzzle?')
FILE_CONTENTS = 'test_3.txt'
DELIMITERS = '\.|\!|\?'

try:
  with open(FILE_CONTENTS,'r') as f:
    FILE_CONTENTS= f.read()
except FileNotFoundError:
  print(f"No such file or directory:{FILE_CONTENTS}")



list1 = re.split(DELIMITERS,FILE_CONTENTS.replace('\n', '').strip())
list1.pop()
print(list1)


# lines = FILE_CONTENTS.split('.')
# print(len(lines))
# print(lines)
#print(FILE_CONTENTS)


# GENERATING all possiblities for each Sir
intToDigits = lambda a : list(map(int, str(a)))
   
Sirs_num = 3
formating_String = str(0)+str(Sirs_num)+'b'
initialP =[]
for p in range(2**Sirs_num):
  temp = [(int(c)) for c in f'{p:{formating_String}}' ]
  initialP.append(temp)

print(initialP)