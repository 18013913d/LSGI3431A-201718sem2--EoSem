# LSGI3431A System Customization and Development
# Laboratory Exercise 2 - Task 1 Program
# Demonstration of changing value at different call-stack
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 5/2/2018

value = 3

def change_a_local():
    # In definition, call a function will lead to higher call stack and become local scope
    # Now it defined as a local variable
    value = 5
    print 'In the function (function called has higher position in call stack), value are ' + str(value)
    print 'Is it a global? ' + str('value' in globals())
    print 'local id = ' + str(id(value))


def change_a_global():
    # force to refer a global variable
    global value

    value = 7
    print 'In the forced global function, value are ' + str(value)
    print 'global id = ' + str(id(value))


if __name__ == '__main__':
    # Demonstrate call stack by function call
    print 'Before the function (function called has higher position in call stack), value are ' + str(value)
    print 'global id = ' + str(id(value))
    change_a_local()
    print 'After the function (function called has higher position in call stack), value are ' + str(value)
    print 'global id = ' + str(id(value))
    print
    change_a_global()
    print 'After global keywords function call, new value are ' + str(value)
    print 'global id = ' + str(id(value))
    print

    print 'anotherNewValue are in global variable ' + str('anotherNewValue' in globals())
    # Demonstrate for loop leakage (COMPARE WITH JAVA)
    for i in range(1, 3):
        anotherNewValue = i
        print 'anotherNewValue are in global variable ' + str('anotherNewValue' in globals())

    print 'anotherNewValue = ' + str(anotherNewValue)
