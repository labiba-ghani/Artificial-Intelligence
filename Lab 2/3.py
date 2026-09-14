
# Prints all letters except 'e' and 's' 
for letter in 'geekforgeeks':
    if letter =='e' or letter =='s':
        continue
    print(letter)

for letter in 'geeksforgeeks': 
# break the loop as soon it sees 'e' 
# or 's' 
    print()
    if letter == 'e' or letter == 's': 
        break 
    print (letter)