n = 4
for i in range(0, n):
    print(i)






print("List Iteration")
l = ["ankush", "aditi", 1]
for i in l:
    print(i)






print("\nDictionary Iteration")  
d = dict()
d['xyz'] = 123
d['abc'] = 345
for i in d :
    print("%s  %d" %(i, d[i]))






print("\nSet Iteration")
set1 = {1,2,3,4,5,6}
for i in set1:
    print(i)

list = ["ankush", "aditi", "rathi"]
for index in range(len(list)):
    print(list[index])

for i in range(1, 5):
    for j in range(i):
         print(i, end=' ')
    print()