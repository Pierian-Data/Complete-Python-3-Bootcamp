print('-----------------------------------------------------------------------')

#region 1. print the elements of an array in reverse order

#1. print the elements of an array in reverse order
#input=[1,2,3,4,5]
#output=[5,4,3,2,1]


input1 = [1, 2, 3, 4, 5]
output1 = []
print("Array in reverse order: ")
for i in range(len(input1)-1, -1, -1):
    output1.append(input1[i])
print(output1)

#endregion

print('-----------------------------------------------------------------------')

#region 2. find second largest number in a list (nth largest no)


#2. find second largest number in a list (nth largest no)
#input2list = [10, 20, 4,30,40,50,12]
#input2item=2
#Output2: 40


input2list = [10, 20, 4, 30, 40, 50, 12]
input2item = 2
input2list.sort()
output2 = input2list[-input2item]
print("Second largest element is:", output2)


#endregion

print('-----------------------------------------------------------------------')

#region 3. Split the array in half and add the first part to the end

#3. Split the array in half and add the first part to the end
# input3[] = {12, 10, 5, 6, 52, 36}
#output3={6,52,36,12,10,5}


def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]


input3 = [12, 10, 5, 6, 52, 36]
splitarr1, splitarr2 = split_list(input3)
output3 = splitarr2+splitarr1
print("split and merge", output3)

#endregion

print('-----------------------------------------------------------------------')

#region 4. print even numbers in a list

#4. print even numbers in a list
#Input4: list1 = [2, 7, 5, 64, 14]
#Output4: [2, 64, 14]

input4 = [2, 7, 5, 64, 14]
output4 = []

for num in input4:
    if num % 2 == 0:
        output4.append(num)

print("even numbers are", output4)

#endregion

print('-----------------------------------------------------------------------')

#region 5. Check if a Substring is Present in a Given String

#5. Check if a Substring is Present in a Given String
#Input5 : s1 = love s2=Ankush is hopelessly in love with aditi
#Output5 : yes


def check(string, sub_str):
    if (string.find(sub_str) == -1):
        print("NO")
    else:
        print("YES")


input5_str = "Ankush is hopelessly in love with aditi"
input5_sub_str = "love"
check(input5_str, input5_sub_str)

#endregion

print('-----------------------------------------------------------------------')

#region 6. Count the Number of matching characters in a pair of string

#6. Count the Number of matching characters in a pair of string
#Input6_str1 = 'AnkushRathi'
#Input6_str2 = 'AditiTiwari'
#Output6 : 4


def count(str1, str2):
    set_string1 = set(str1)
    set_string2 = set(str2)
    matched_characters = set_string1 & set_string2
    print("No. of matching characters are : " + str(len(matched_characters)))


input6_str1 = 'ankushrathi'  # first string
input6_str2 = 'adititiwari'     # second string
count(input6_str1, input6_str2)


#endregion

print('-----------------------------------------------------------------------')

#region 7. sort a list of tuples by second Item

#7. sort a list of tuples by second Item
#Input7 : [('aditi', 10), ('ankush', 5), ('vinod', 20), ('gaurav', 15)]
#Output7 : [('ankush', 5), ('aditi', 10), ('gaurav', 15), ('vinod', 20)]


def Sort_Tuple(tup):
    tup.sort(key=lambda x: x[1])
    return tup


input7 = [('aditi', 10), ('ankush', 5), ('vinod', 20), ('gaurav', 15)]
output7 = Sort_Tuple(input7)
print("sorted tuple: ", output7)

#endregion

print('-----------------------------------------------------------------------')

#region 8. sort the elements of an array in ascending order

#8. sort the elements of an array in ascending order
#Initialize array
input8 = [5, 2, 8, 7, 1]
output8 = []
temp = 0

for i in range(0, len(input8)):
    for j in range(i+1, len(input8)):
        if(input8[i] > input8[j]):
            temp = input8[i]
            input8[i] = input8[j]
            input8[j] = temp

for i in range(0, len(input8)):
    output8.append(input8[i])

print("Elements of array sorted in ascending order: ")
print(output8)

#endregion

print('-----------------------------------------------------------------------')

#region 9. Check Prime Number

#9. Check Prime Number


def PrimeChecker(a):
    if a > 1:
        for j in range(2, int(a/2) + 1):
            if (a % j) == 0:
                print(a, "is not a prime number")
                break
        else:
            print(a, "is a prime number")
    else:
        print(a, "is not a prime number")


a = int(input("Enter an input number:"))
PrimeChecker(a)

#endregion

print('-----------------------------------------------------------------------')

#region 10. Check if a Key is Already Present in a Dictionary

#10. Check if a Key is Already Present in a Dictionary
#input={1: 'a', 2: 'b', 3: 'c'}
#key=5
#output=key is not present

input10 = {1: 'a', 2: 'b', 3: 'c'}
input10_key = 5

if input10_key in input10:
    print("key is present")
else:
    print("key is not present")
#endregion

print('-----------------------------------------------------------------------')

#region 11. Count the Occurrence of an Item in a List

#11. Count the Occurrence of an Item in a List
#input=['a', 1, 'a', 4, 3, 2, 'a']
#item='a'
#output=3

input11 = ['a', 1, 'a', 4, 3, 2, 'a']
input11_item = 'a'
output11 = input11.count(input11_item)
print("No of occurrence: ", output11)

#endregion

print('-----------------------------------------------------------------------')

#region 12. Convert Two Lists Into a Dictionary

#12. Convert Two Lists Into a Dictionary
#input1=[1, 2, 3]
#input2=['python', 'c', 'c++']
#output={1: 'python', 2: 'c', 3: 'c++'}

input12_index = [1, 2, 3]
input12_languages = ['python', 'c', 'c++']

Output12_dictionary = dict(zip(input12_index, input12_languages))
print("Converted Disctonary: ", Output12_dictionary)

#endregion

print('-----------------------------------------------------------------------')

#region 13. Reverse a Number

#13. Reverse a Number

num = 1234
reversed_num = 0

while num != 0:
    digit = num % 10
    reversed_num = reversed_num * 10 + digit
    num //= 10

print("Reversed Number: " + str(reversed_num))

print(str(num)[::-1])

#endregion

print('-----------------------------------------------------------------------')

#region 14

#


#endregion

print('-----------------------------------------------------------------------')

#region 15

#


#endregion

print('-----------------------------------------------------------------------')
