rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

matrix = []

for i in range(rows):
    row = []

    for j in range(cols):
        row.append(i * j)

    matrix.append(row)

print(matrix)