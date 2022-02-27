def gcd_J(a,b):
    if b>0:
        return gcd_J(b,a%b)
    else:
        return a

print(gcd_J(-12,-8))