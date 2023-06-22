print('This is a string that speaks English {}'.format('hello'))

print("The {2} {0} {1}".format("brown", "fox", "quick"))

print("The {q} {b} {f}".format(b="brown", f="fox", q="quick"))

result = 100/777
print(result)

print("The result was {r:1.5f}".format(r=result))


name = "Joseph"
print (f"Hello my name is {name}")
#this is equal to

print ("Hello my name is {}".format(name, name+name))

print ("Hello my name is {name}".format(name=name))

print ("Hello my name is {name}".format(name="Joseph"))

name = "Clarkson"
age = 59
sex = "Male"

print (f"{name} is {age} years old and {'a boy' if sex=='Male' else 'a girl'}")


print (f"{name} is {'old' if age>50 else 'young'} and {'a man' if sex == 'Male' else 'a woman'}")


print (f"{name} is {'old' if age else 'young'} and {'a man' if sex == 'Male' else 'a woman'}")

