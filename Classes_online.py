# import python_tips prints first modules name variable:__main__ but doesnt when the equality is called
# prints this only when __name__ == '__main__' is called in python_tips

'''import python_tips
python_tips.main()'''
# if you want to run the module
# outputs:
# This will always be run - outside the main fn
# Running from Import
# first modules name variable:python_tips # main fn is called because it is running the main method anyways
# Second modules name variable:__main__
'''print(f'Second modules name variable:{__name__}')'''


'''def diff(f, x, h=1E-5):
    return (f(x+h) - f(x))/h'''

# The aim of the doc string is to explain the purpose of the function and, for instance, what the arguments and return values are.
# A class can also have a doc string, it is just the first string that appears right after the class headline.
#  The convention is to enclose the doc string in triple double quotes """


# class Y:
"""
    Mathematical function for the vertical motion of a ball.

    Methods:
       constructor(v0): set initial velocity v0.
       value(t): compute the height as function of t.
       formula(): print out the formula for the height.

    Data attributes:
       v0: the initial velocity of the ball (time 0).
       g: acceleration of gravity (fixed).

    Usage:
    y = Y(3)
    position1 = y.value(0.1)
    position2 = y.value(0.3)
    print y.formula()
    v0*t - 0.5*g*t**2; v0=3
    """
# we define two new data attributes in this instance. The self parameter is invisibly returned to the calling code.
# We can imagine that Python translates the syntax y = Y(3) to a call written as Y.__init__(y, 3)

# Now, self becomes the new instance y we want to create, so when we do self.v0 = v0 in the constructor, we actually assign v0 to y.v0.
# prefix with y. (the instance name) the self argument is dropped in the syntax, and Python will automatically assign
# the y instance to the self argument.

'''def __init__(self, v0):
        self.v0 = v0
        self.g = 9.81

    def value(self, t):
        return self.v0*t - 0.5*self.g*t**2

    def formula(self):
        return 'v0*t - 0.5*g*t**2; v0=%g' % self.v0


y = Y(3)

print(y.v0)  # outputs 3
print(y.g)  # outputs 9.81
t = 0.1
# print(Y.value(t))
y1 = Y(1)
y2 = Y(1.5)
y3 = Y(-3)
print(y1.value(0.1))'''  # outputs 0.050949999999999995

# However, if we first create y = Y(2) and then call Y.__init__(y, 3), the syntax works,
# and y.v0 is 3 after the call.

# self argument in the value method becomes the y instance
'''value = y.value(0.1)
value1 = Y.value(y, 0.1)
print(value, value1)'''  # outputs the same value 0.25095 0.25095

# The diff(f,x) function, f that behaves as a function of one variables actually carries two variables v0 = 1 and g = 9.81
# while passing on t = 0.1
'''dy1dt = diff(y1.value, 0.1)
dy2dt = diff(y2.value, 0.1)
dy3dt = diff(y3.value, 0.2)

print(dy1dt)
'''
# In addition, every Python object obj has a unique identifier obtained by id(obj) that we can also print to track what self is.


'''class SelfExplorer(object):
    def __init__(self, a):
        self.a = a
        print(f'init: a={self.a}, id(self)={id(self)}')

    def value(self, x):
        print(f'value: a={self.a}, id(self)={id(self)}')
        return self.a*x


# We clearly see that self inside the constructor is the same object as s1, which we want to create by calling the constructor.
s1 = SelfExplorer(1)  # outputs init: a=1, id(self)=12927472
print(id(s1))  # outputs 12927472
s2 = SelfExplorer(2)  # init: a=2, id(self)=12927504
print(id(s2))'''

'''SelfExplorer.value(s1, 4)  # value: a=1, id(self)=40878128
s1.value(4) '''  # value: a=1, id(self)=40878128


# Initializing many variables
'''class V(object):
    def __init__(self, beta, mu0, n, R):
        # Can initialize many variables on the same line
        self.beta, self.mu0, self.n, self.R = beta, mu0, n, R

    def value(self, r):
        # LHS upnaking the tuple on the RHS so you dont need to use self.beta everytime you use it in the method
        beta, mu0, n, R = self.beta, self.mu0, self.n, self.R
        n = float(n)  # ensure float divisions
        v = (beta/(2.0*mu0))**(1/n)*(n/(n+1)) *\
            (R**(1+1/n) - r**(1+1/n))
        return v


v1 = V(2, 3, 4, 5)
# outputs 2.1448774658699974 , 2.1448774658699974
print(v1.value(3), V.value(v1, 3), sep=',')
'''

# It is a good habit always to have a constructor in a class and to initialize the data attributes in the class here,
# but this is not a requirement.

# Let us drop the constructor and make v0 an optional argument to the value method.

# If the user does not provide v0 in the call to value, we use a v0 value that must have been provided in an earlier call
# and stored as a data attribute self.v0. We can recognize if the user provides v0 as argument or not
# by using None as default value for the keyword argument and then test if v0 is None.

'''
class Y2(object):
    def value(self, t, v0=None):
        if v0 is not None:
            self.v0 = v0
        g = 9.81
        return self.v0*t - 0.5*g*t**2'''


# But if there is no constructor, how is an instance created? Python fortunately creates an empty constructor.
# This allows us to write:
# y = Y2()
# nothing happens so y has no data atttributes at this stage as y.v0 will provide an Attribute Error
'''x = y.value(0.1, 5)
print(y.v0)  # outputs 5
z = y.value(0.3)
print(z)'''  # outputs 1.0585499999999999 because the previous v0 is used inside method value as 5 unless a v0 is specified in the call

# print(isinstance(Y2, object))  # outputs True

# using more informative messages if no attribute is provided
# To check if we have an attribute v0, we can use the Python function hasattr. Calling hasattr(self, 'v0')
# returns True only if the instance self has an attribute with name 'v0'. An improved value method now reads


'''class Y1(object):
    def value(self, t, v0=None):
        if v0 is not None:
            self.v0 = v0
        if not hasattr(self, 'v0'):
            print('You cannot call value(t) without first
calling value(t, v0) to set v0')
            return None
        g = 9.81
        return self.v0*t - 0.5*g*t**2

# Alternatively, we can try to access self.v0 in a try-except block, and perhaps raise an exception TypeError
# (which is what Python raises if there are not enough arguments to a function or method):


class Y3(object):
    def value(self, t, v0=None):
        if v0 is not None:
            self.v0 = v0
        g = 9.81
        try:
            value = self.v0*t - 0.5*g*t**2
        except AttributeError:
            msg = 'You cannot call value(t) without first
            calling value(t,v0) to set v0'
            raise TypeError(msg)
        return value


y1 = Y1()
y2 = Y3()
y2.value(0.1, 1)
y1.value(0.2)'''


'''class Y:
    def __init__(self, v0):
        self.v0 = v0
        self.g = 9.81

    def value(self, t):
        return self.v0*t - 0.5*self.g*t**2

    def formula(self):
        return 'v0*t - 0.5*g*t**2; v0=%g' % self.v0'''

print('Hello')
for x in range(10):
    assert isinstance(x, object)
    print(x)
