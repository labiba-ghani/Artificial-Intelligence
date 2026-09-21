a, b = 0, 1
fib_series = []

while b < 50:
    fib_series.append(str(b))
    a, b = b, a + b #a=b and b=a+b 
    #multiple assignmet(or tuple unpacking)
    # old_a =a old_b=b 
    #a=old_b
    #b=old_a+old_b
print(" ".join(fib_series))

# append is the list method (add one item at the last)
# join is the string method (take multiple strings and combine them into one string)
# " " tells python what to put between the items