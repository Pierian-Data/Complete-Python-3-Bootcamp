from random import random
from multiprocessing import Pool
import timeit

def find_pi(n):
    """
    Function to estimate the value of Pi
    """
    inside=0

    for i in range(0,n):
        x=random()
        y=random()
        if (x*x+y*y)**(0.5)<=1:  # if i falls inside the circle
            inside+=1

    pi=4*inside/n
    return pi

if __name__ == '__main__':
    N = 10**7  # total iterations
    
    P = 1      # number of processes
    p = Pool(P)
    print(timeit.timeit(lambda: print(f'{sum(p.map(find_pi, [N//P]*P))/P:0.7f}'), number=10))
    p.close()
    p.join()
    print(f'{N} total iterations with {P} processes')
    
    P = 5      # number of processes
    p = Pool(P)
    print(timeit.timeit(lambda: print(f'{sum(p.map(find_pi, [N//P]*P))/P:0.7f}'), number=10))
    p.close()
    p.join()
    print(f'{N} total iterations with {P} processes\n')