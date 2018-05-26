# LSGI3431A System Customization and Development
# Laboratory Exercise 3 - Example 4
# Reproduction of Example 4
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 10/2/2018

class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addTwice(self, x):
        self.add(x)
        self.add(x)

if __name__ == "__main__":
    things = Bag()
    things.add("Apple")
    things.addTwice("Orange")

    for thing in things.data:
        print thing
