numbers = input("Enter binary numbers: ").split(",")

result = []

for num in numbers:
    decimal = int(num, 2)

    if decimal % 5 == 0:
        result.append(num)

print(",".join(result))