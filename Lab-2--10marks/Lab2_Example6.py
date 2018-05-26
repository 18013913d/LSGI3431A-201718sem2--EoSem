def test_args_kwargs(arg1, arg2, arg3):
    print 'arg1: ' + str(arg1)
    print 'arg2: ' + str(arg2)
    print 'arg3: ' + str(arg3)

print 'Tuple:'
args = ("two", 5, 3)
print 'Arguments=' + str(args)
test_args_kwargs(*args)

print
print 'A dictionary: '
kwargs = {'arg3': 3, 'arg1': 'two', 'arg2': 5}
print 'Dereference once'
test_args_kwargs(*kwargs)

print 'Dereference twice'
test_args_kwargs(**kwargs)

