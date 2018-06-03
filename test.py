import argparse
print "hello world"
def func (x):
    print " this is " + x
func("3") ## define function
def func2 (x) :
    if x == 3 :
        print "hahahahah"
    else :
        print "wuwuwuwu"
func2(3)
func2(4)
array =[1,2,3]
def func3 (x) :
    for item in x :
        print item +1
func3(array) ## two type of for loops
def func4 (x):
    for i in range(0,len(x)):
        print x[i]
func4(array) ## while loops
y = 0
z = 0
while y < 5:
    print y
    y += 1
a = [1,2,3]
a.append(4)
print a
print a.pop()
print a
print a.pop(0)
print a
