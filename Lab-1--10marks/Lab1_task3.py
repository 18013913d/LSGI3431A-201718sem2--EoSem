# LSGI3431A System Customization and Development
# Laboratory Exercise 1 - Task 3 Program
# Demonstration of using if Statement and For loop in Python
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 26/1/2018

PI = 3.1415926
Radius_List = [5.1, 1.3, 0.85, 2.2, 7.583, 25.6]
print 'Index if area >= 15 |       Area        '
print '----------------------------------------'
for index, radius in enumerate(Radius_List):
    Area = PI*(radius**2)
    if Area >= 15:
        print '         '+str(index)+'          |    ' + str(Area)
    else:
        print '                    |    ' + str(Area)
print
