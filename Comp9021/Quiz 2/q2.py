# Written by *** for COMP9021
#
# Implements three functions:
# - binary_lunar_addition(number_1, number_2)
#   that lunarly (or is it lunatically?) adds number_2 to number_1;
# - lunar_addition(*numbers)
#   that lunarly adds all arguments;
# - binary_lunar_multiplication(multiplicand, multiplier)
#   that lunarly multiplies multiplicand by multiplier.
#
# Both operations are discussed at
# https://www.youtube.com/watch?v=cZkGeR9CWbk
# Watch it!
#
# Essentially, lunar addition and lunar multiplication
# are like standard addition and multiplication, except that:
# - the lunar sum of two digits is the largest of both digits;
# - the lunar product of two digits the smallest of both digits.
#
# You can assume that the function arguments are exactly as expected,
# namely, positive numbers (possibly equal to 0).


def binary_lunar_addition(number_1, number_2):
    result = 0
    # INSERT YOUR CODE HERE
    list_n1 =list(reversed(list(map(int, str(number_1)))))
    list_n2 =list(reversed(list(map(int, str(number_2)))))
    
    if number_1 >= number_2:
      for i in range(len(list_n2)):
        list_n1[i] = max(list_n1[i], list_n2[i])
      result = int(''.join([str(i) for i in reversed(list_n1)]))
    else:
      for i in range(len(list_n1)):
        list_n2[i] = max(list_n2[i], list_n1[i])
      result = int(''.join([str(i) for i in reversed(list_n2)]))

    return result

def lunar_addition(*numbers):
    result = 0
    # INSERT YOUR CODE HERE
    for n in numbers:
      result =  binary_lunar_addition(result, n)
    
    return result


def binary_lunar_multiplication(multiplicand, multiplier):
    result = 0
    # INSERT YOUR CODE HERE
    multiplicandList = list(map(int, str(multiplicand)))
    multiplierList = list(map(int, str(multiplier)))
    tentimes =0

    for multiplierDigit in reversed(multiplierList):
      currentDigitResultList=[]
      for multiplicandDigit in multiplicandList:
        currentDigitResultList.append(min(multiplicandDigit,multiplierDigit))
      currentResult = int(''.join([str(i) for i in currentDigitResultList])) * 10**tentimes
      tentimes +=1
      result = binary_lunar_addition(result, currentResult)
    
    return result

        


