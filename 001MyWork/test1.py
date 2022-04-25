

from abc import ABC, abstractmethod

class Calculate_grade(ABC):
    def sum(self,marks):
        sum=0
        for i in marks:
            sum=sum+i
        return sum

    def percentage(self,Total_sum,out_of):
        percentage=Total_sum*100/out_of
        return percentage

    @abstractmethod
    def grades(self,Total_percentage):
        pass

class school1(Calculate_grade):
    def grades(self,Total_percentage):
        str = ''
        if Total_percentage >= 80:
            str = 'First class'
        elif Total_percentage < 80:
            str = 'Fail'
        return str

class school2(Calculate_grade):
        def grades(self,Total_percentage):
            str = ''
            if Total_percentage >= 70:
                str = 'First class'
            elif Total_percentage < 70:
                str = 'Fail'
            return str
        

Total_sub = int(input('Enter total subjects:'))
marks = []

out_of = int(input('Enter out of marks:'))

for j in range(0,2):
    for i in range(1,Total_sub+1):
        score=int(input('Enter score of subject:'))
        marks.append(score)

    C=school2()

    Total_sum = C.sum(marks)
    print(Total_sum)

    Total_percentage = C.percentage(Total_sum,out_of*Total_sub)
    print(Total_percentage)

    Grade = C.grades(Total_percentage)
    print(Grade)