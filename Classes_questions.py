# Write a Python class to convert an integer to a roman numeral.
'''class Roman:
    name = 5  # class attribute

    def __init__(self, number):
        self.number = number  # roman is a data attribute
        self.x = 6

    def int_to_roman(self, number):
        """ Convert an integer to a Roman numeral. """

        if not isinstance(self.number, type(1)):
            raise TypeError("expected integer, got %s" % type(self.number))
        if not 0 < self.number < 4000:
            raise ValueError("Argument must be between 1 and 3999")
        ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        nums = ('M',  'CM', 'D', 'CD', 'C', 'XC',
                'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
        result = []
        for i in range(len(ints)):
            count = int(self.number / ints[i])
            result.append(nums[i] * count)
            self.number -= ints[i] * count
        return ''.join(result)

'''
'''Italian = Roman(8)
print(Italian.int_to_roman(8))
print(Italian.number, Roman.name, Italian.x)'''
# print(Roman().int_to_roman(9)) #cannot do this because it is an instance method
