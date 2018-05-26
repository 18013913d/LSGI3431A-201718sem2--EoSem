def return_set_size(*args):

    """
    The function takes indefinite length of variables and return a set with all the elements in non-repeating manner.
    :param args: a indefinite length sized arguments
    :return: the number of the non-repeating elements
    """

    s = set()
    for arg in args:
        s.add(arg)

    #Print the elements in the set
    for element in s:
        print 'Element in the set: ' + str(element)
    return len(s)

if __name__ == '__main__':
    # NOT SUPPORTED: a list of arguments but not multiple arguments.
    # s1 = return_set_size([1,2,3])
    print 'Set 2:'
    s2 = return_set_size(1,1,2,5,'hello')

    # SUPPORTED TYPE: Tuple; KEY DIFFERENCE: They are immutable and hence have a consistent Hash ID
    print 'Set 3:'
    s3 = return_set_size(1,(2,5), 2.1)
    print 'The size of the three sets are: ', s2, s3
