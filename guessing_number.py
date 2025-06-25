while True:
    try :
        var= range(1,11)
        user = int(input("enter intergers..."))
        if user in var:
            print(f"Entered number is wihtin the range -> {user}")
            break
        else:
            print("Enter number b/w the range 1-10 ")
    except:
        print("Enter only digits")