n = 5

# Upper half
for i in range(1, n + 1):
    for j in range(i):
        print("*", end=" ") #Print *, but don't go to the next line. Put a space after it.
    print()

# Lower half
for i in range(n - 1, 0, -1): #-1 dec by 1 each time
    for j in range(i):
        print("*", end=" ")
    print()