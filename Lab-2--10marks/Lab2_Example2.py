# LSGI3431A System Customization and Development
# Laboratory Exercise 2 - Task 1 Program
# Reproducing Example 2
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 5/2/2018

def items_to_string(argv=[2,3,4,5,6]):

    """
    The function takes only one argument a list, convert items in it to string.
    :param argv: a list of input arguments, the items in it will be converted to string.
    :return: a list contains string items.
    """

    # Initialize an empty list.
    str_list = []
    # Print the input arguments.
    print argv

    # Iterate through all the input arguments, convert them to string and append it into str_list.
    for arg in argv:
        str_list.append(str(arg))

    # Insert a string value at the end of str_list
    # Use NULL (ASCII 0) to terminate the list in this example
    str_list.append(chr(0))
    return str_list

if __name__ == '__main__':
    #Demonstrate the default argument
    c1 = items_to_string()
    print c1, ' ', len(c1)
    #demonstrate the specified argument
    c2 = items_to_string([2.1, 3.1, 4.1, 5.1, 6.1])
    print c2
