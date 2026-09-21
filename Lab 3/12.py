print("Enter lines of text (press Enter on an empty line to finish):")
lines = []

while True:
    line = input()
    if line == "":
        break
    lines.append(line.lower())

print("\nResult:")
for line in lines:
    print(line)