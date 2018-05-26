# LSGI3431A System Customization and Development
# Laboratory Exercise 2 - Task 2 Program
# Entry point of Lab2_Circle.
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 5/2/2018

import sys
sys.path.append(r'.\\lib\\')
# N.B. Potential Glitch in PyCharm. Run smooth in both PyCharm IDE and CLI (Windows 10 Powershell and CentOS)
import Lab2_Circle

if __name__ == '__main__':
    # Define a list of circle radius
    radius_list = [5.1, 1.3, 0.85, 2.2, 25.6]
    print 'The list for radius are: ' + str(radius_list)

    # Calculate and store the list of area
    area_list = Lab2_Circle.Calculate_Circle_Area(radius_list)
    # Print out the result
    print 'The list for area are: ' + str(area_list)
