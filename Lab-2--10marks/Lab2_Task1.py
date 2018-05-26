def area(radius):
    """
    This program calculate the area of a circle given the radius
    :param radius: The radius of the circle.
    :return: The area of the circle.
    """
    PI = 3.1415926
    return PI * (radius**2)

if __name__ == "__main__":
    #define the radius of the test circle
    circle1_radius = 5.5
    circle1_area = area(circle1_radius);
    print 'The area of a circle with ' + str(circle1_radius) + ' unit radius are ' +str(circle1_area)
