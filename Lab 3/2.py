def c_to_f(c):
    return int((c * 9 / 5) + 32)

def f_to_c(f):
    return int((f - 32) * 5 / 9)

# Demonstrating expected outputs
c_val = 60
f_val = 45

print(f"{c_val}°C is {c_to_f(c_val)} in Fahrenheit")
print(f"{f_val}°F is {f_to_c(f_val)} in Celsius")