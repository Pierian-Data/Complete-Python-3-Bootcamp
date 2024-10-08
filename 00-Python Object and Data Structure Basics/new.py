x=int(input("enter the no 1"))
y=int(input("enter the no 2"))
z=int(input("enter the no 3"))
if(x!=7 and y!=7 and z!=7):
    print (x*y*z)
elif(x==7):
    print(y*z)
elif(y==7):
    print(x*z)
elif(z==7):
    print(y*x)
elif(x==7 and y==7 and z==7):
    print