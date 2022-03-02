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
    intToDigits = lambda a : list(map(int, str(a)))
    stack1 = intToDigits(number_1)
    stack2 = intToDigits(number_2)
    factor = 0

    while len(stack1) > 0 or len(stack2) > 0:
        result += 10**factor * max(stack1.pop() if len(stack1) >
                              0 else 0, stack2.pop() if len(stack2) > 0 else 0)
        factor += 1

    return result


def lunar_addition(*numbers):
    result = 0
    # INSERT YOUR CODE HERE
    for n in numbers:
        result = binary_lunar_addition(result, n)

    return result


def binary_lunar_multiplication(multiplicand, multiplier):
    result = 0
    # INSERT YOUR CODE HERE
    intToDigits = lambda a : list(map(int, str(a)))
    m1 = intToDigits (multiplicand)
    m2 = intToDigits (multiplier)
    factor = 0

    while m2:
        partialResult = []
        m2Digit = m2.pop()
        for m1Digit in m1:
            partialResult.append(min(m1Digit, m2Digit))

        currentResult = int(
            ''.join(list(map(str, partialResult)))) * 10**factor
        factor += 1
        result = binary_lunar_addition(result, currentResult)

    return result
    