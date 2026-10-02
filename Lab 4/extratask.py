# reverse the string through stack
stack=[]

text=input("enter a string: ")

# put each charcter in stack
for char in text:
    stack.append(char)

print("Reverse String:",end="")

while len(stack)> 0:
    print(stack.pop(),end="")