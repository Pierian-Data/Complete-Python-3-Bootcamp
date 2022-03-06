from typing import Dict

from matplotlib.pyplot import hist


def Matrix (top_left_corner, bottom_right_corner):
  x_l,y_t = top_left_corner
  x_r,y_b = bottom_right_corner
  Matrix_coordinate = {}
 
  for y in range(y_t,y_b-1,-1):
     for x in range(x_l,x_r+1,1):
       Matrix_coordinate[(x,y)] = '⬜'
  return Matrix_coordinate
 
def printMatrix(Matrix,top_left_corner, bottom_right_corner):
  x_l,y_t = top_left_corner
  x_r,y_b = bottom_right_corner
  width = x_r - x_l + 1
  str=''
  count = width
  for key in Matrix:
    if count>0:
      str+=Matrix[key]
      count-=1
    elif count ==0:
      print(str)
      count=width-1
      str=Matrix[key]
  #print last line
  print(str)
      
    

  

def addingToothpick(Matrix, point, direction):
  x,y = point
  if direction=='VERTICAL':
    for h in range(y-2, y+3, 1):
      Matrix[(x,h)] = '⬛'
  if direction=='HORIZONTAL':
    for w in range(x-2, x+3, 1):
      Matrix[(w,y)] = '⬛'


# m1 = Matrix((-4,4), (4,-4))
# printMatrix(m1, (-4,4), (4,-4))

# print('------------')
# addingToothpick (m1,(0,0), 'VERTICAL')
# printMatrix(m1, (-4,4), (4,-4))

# print('------------')
# addingToothpick (m1,(0,2), 'HORIZONTAL')
# addingToothpick (m1,(0,-2), 'HORIZONTAL')
# printMatrix(m1, (-4,4), (4,-4))


Tracking ={(0,2):'HORIZONTAL', (0,-2): 'HORIZONTAL'}
Tracking2 = {(-2, 2): 'VERTICAL', (2, 2): 'VERTICAL', (-2, -2): 'VERTICAL', (2, -2): 'VERTICAL'}
Tracking3 = {(-2, 4): 'HORIZONTAL', (2, 4): 'HORIZONTAL', (-2, -4): 'HORIZONTAL', (2, -4): 'HORIZONTAL'}
Tracking4 = {(-4, 4): 'VERTICAL', (4, 4): 'VERTICAL', (-4, -4): 'VERTICAL', (4, -4): 'VERTICAL'}
Tracking5 = {(-4, 2): 'HORIZONTAL', (-4, 6): 'HORIZONTAL', (4, 2): 'HORIZONTAL', (4, 6): 'HORIZONTAL', (-4, -6): 'HORIZONTAL', (-4, -2): 'HORIZONTAL', (4, -6): 'HORIZONTAL', (4, -2): 'HORIZONTAL'}


historical_removed={}

def expend():
  for tip in dict(Tracking):
    x,y = tip
    if Tracking[tip]=='HORIZONTAL':
      historical_removed[tip]=Tracking[tip]
      Tracking.pop(tip)
      
      new_tip1= (x-2,y)
      new_tip2= (x+2,y)
      if new_tip1 in Tracking:
        historical_removed[new_tip1]=Tracking[new_tip1]
        Tracking.pop(new_tip1)

      else:
        if new_tip1 not in historical_removed:
          Tracking[new_tip1] = 'VERTICAL'
      
      if new_tip2 in Tracking:
        historical_removed[new_tip2]=Tracking[new_tip2]
        Tracking.pop(new_tip2)
      else:
        if new_tip2 not in historical_removed:
          Tracking[new_tip2] = 'VERTICAL'
      
    else:
      historical_removed[tip]=Tracking[tip]
      Tracking.pop(tip)
      new_tip1= (x,y-2)
      new_tip2= (x,y+2)

      if new_tip1 in Tracking:
        historical_removed[new_tip1]=Tracking[new_tip1]
        Tracking.pop(new_tip1)
      else:
        if new_tip1 not in historical_removed:
          Tracking[new_tip1] = 'HORIZONTAL'
      
      if new_tip2 in Tracking:
        historical_removed[new_tip2]=Tracking[new_tip2]
        Tracking.pop(new_tip2)
      else:
        if new_tip2 not in historical_removed:
          Tracking[new_tip2] = 'HORIZONTAL'
    

  print(Tracking)
  #print('removed: '+ str(historical_removed))
  print()



print(Tracking)
print('removed: '+ str(historical_removed))
print()

expend()
expend()
expend()
expend()
expend()
expend()
expend()



# t1 = (-4,5)
# t2 = (4, -5)

# m1 = Matrix(t1,t2);

# # round0
# addingToothpick(m1, (0,0),'VERTICAL')
# printMatrix(m1, t1,t2)
# print()

# # round1
# addingToothpick(m1, (0,2),'HORIZONTAL')
# addingToothpick(m1, (0,-2),'HORIZONTAL')
# printMatrix(m1, t1,t2)
# print()

# # round2
# addingToothpick(m1, (-2,2),'VERTICAL')
# addingToothpick(m1, (2,2),'VERTICAL')
# addingToothpick(m1, (-2,-2),'VERTICAL')
# addingToothpick(m1, (2,-2),'VERTICAL')
# printMatrix(m1, t1,t2)

