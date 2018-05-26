# LSGI3431A System Customization and Development
# Laboratory Exercise 2 - Task 1 Program
# Reproducing Example 1
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 5/2/2018

def fib(N):
  """
    The function produces a Fibonacci series.
    :param N: an integer number, the maximum range of Fibonacci sereis.
    :return: the list of Fibonacci series
    """
  fibonacci = []
  a, b = 0, 1
  while a < N:
    fibonacci.append(a)
    a, b = b, a + b
  return fibonacci


if __name__ == '__main__':
  # Now call the function we just defined:
  fib_list = fib(2000)
  #Print the Fibonacci series
  print fib_list
