'''def get_numbers():
    limit = int(input("Enter limit: "))
    for number in range(limit):
        if 3 < number <= limit:
            print(number)


# get_numbers()

def fizz_buzz(input):
    if (input % 3 == 0) and (input % 5 == 0):
        return"fizz buzz"
    if input % 5 == 0:
        return"fizz"
    if input % 3 == 0:
        return"buzz"
    return input  # dont need to put else at the end as python already understands it


print(fizz_buzz(16))
'''
'''name = "John Smith"
print(name[1])
print(name.find("Smith"))
print(name.replace("j", "k"))
if "John" in name:
    print("yes")'''

# Write a function for checking the speed of drivers. This function should have one parameter: speed.
# If speed is less than 70, it should print “Ok”.
# Otherwise, for every 5km above the speed limit (70), it should give the driver one demerit point and print the total number of demerit points. For example, if the speed is 80, it should print: “Points: 2”.
# If the driver gets more than 12 points, the function should print: “License suspended”
'''def check_speed(speed):
    if speed < 70:
        print("ok")
    else:
        above_limit = (speed-70) / 5
        if above_limit > 12:
            print("License Suspended")
        else:
            print(f"Points: {int(above_limit)}")


x = int(input("speed: "))
check_speed(x)'''

# Write a function called showNumbers that takes a parameter called limit.
# It should print all the numbers between 0 and limit with a label to identify the even and odd numbers.
# For example, if the limit is 3, it should print:
# 0 EVEN
# 1 ODD
# 2 EVEN
# 3 ODD


'''def showNumbers(limit):
    for number in range(0, limit+1):  # repeats 3 times - 0,1,2
        if number % 2 == 0:
            value = "EVEN"
            print(number, value)
        else:
            value = "ODD"
            print(number, value)


showNumbers(3)
'''
# Write a function that returns the sum of multiples of 3 and 5 between 0 and limit (parameter).
# For example, if limit is 20, it should return the sum of 3, 5, 6, 9, 10, 12, 15, 18, 20.


'''def sum_multiples(limit):
    total = 1
    if limit <= 2:
        print("please enter a number higher than 3")
        exit()
    for number in range(limit+1):
        if (number % 3 == 0) or (number % 5 == 0):
            total += number

    print(total)


x = int(input("Enter number:"))
sum_multiples(x)'''

# Write a function called show_stars(rows). If rows is 5, it should print the following:
# *
# **
# ***
# ****
# *****

'''def show_stars(rows):
    for stars in range(rows+1):
        print("*"*stars)


x = int(input("Enter no. of rows: "))
show_stars(x)
'''

# Write a function that prints all the prime numbers between 0 and limit where limit is a parameter.


'''def prime_numbers(limit):
    for num in range(0, limit+1):
       # prime numbers are greater than 1
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                print(num)


x = int(input("Enter no. of rows: "))
prime_numbers(x)'''

# Find the most common character in the below sentence
# sentence = "This is a common interview question"


# # print(sentence)
# sentence.sort()
# count = 0
# repeat = 1
# values = [' ', 0]
# index = 0
# for char in sentence:
#     if char == sentence[count+1]:
#         repeat += 1
#         if char != values[index]:
#             repeat = 1
#             values.append(char)
#             values.append(repeat)
#             index +=2
#             increase = 1
#             continue
#         if continue = 0:
#             values = [char, repeat]
#         else:
#             output = tuple(values)
#             values.append()

#     count += 1

# use dictionary to store the sentence
from pprint import pprint  # from module import function
sentence = "This is a common interview question"

char_Frequence = {}

for char in sentence:
    if char in char_Frequence:
        char_Frequence[char] += 1
    else:
        char_Frequence[char] = 1

pprint(char_Frequence, width=7)

# sorted takes iterables as parameters and .items gets key-value pairs as tuples
# print(sorted(char_Frequence.items(), key=lambda kv: kv[1], reverse=True))

repeat = [0, 0]
for letter in char_Frequence:
    value = char_Frequence[letter]
    if value == 1:
        continue
    elif value > repeat[1]:
        repeat = [letter, value]
    elif value == repeat[1]:
        repeat.append(letter)
        repeat.append(value)

pprint(repeat)
