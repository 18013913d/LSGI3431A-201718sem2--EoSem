# LSGI3431A System Customization and Development
# Laboratory Exercise 2 - Task 1 Program
# Library file for computing circle area
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 5/2/2018

def Calculate_Circle_Area(argv):
    """
    This function provides area calculation of a list of circle
    :param argv: A list of circle radius which is numeric
    :return: A list of circle area in the same order as the input parameter. Non-numeric value would be skipped.
    """
    if not (type(argv) is list):
        return None
    PI = 3.1415926
    area_list = []

    for arg in argv:
        if not (type(arg) is int or type(arg) is float):
            continue
        area_list.append(PI*(arg**2))
    return area_list
