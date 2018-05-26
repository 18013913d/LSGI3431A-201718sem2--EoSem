def generate_list(**kwargs):
    """
    This program convert the keyworded arguments into a 'list of list'
    :param kwargs: Keyworded arguments
    :return: The 'list of list' with each keyword and its value
    """

    new_list =[]

    for key, item in kwargs.iteritems():
        new_list.append([key,item])
    return new_list

if __name__=="__main__":

    #We define the key are the name of the person and the item are the salary
    list1 = generate_list(Bob=3000, Jerry=4000)
    print 'The first list are: ' + str(list1)
    for record in list1:
        print 'The salary for ' + record[0] + ' are $' + str(record[1])

    print

    list2 = generate_list(Jacob=6000, Ray=8500, Tom=5000)
    print 'The second list are: ' + str(list2)
    for record in list2:
        print 'The salary for ' + record[0] + ' are $' + str(record[1])
