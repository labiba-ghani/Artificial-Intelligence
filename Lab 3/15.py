import re 
#python regular expression libraryimport re

password = input("Enter password to validate: ")

is_valid = True

if not (6 <= len(password) <= 16):
    is_valid = False
elif not re.search(r"[a-z]", password):
    is_valid = False
elif not re.search(r"[A-Z]", password):
    is_valid = False
elif not re.search(r"[0-9]", password):
    is_valid = False
elif not re.search(r"[$#@]", password):
    is_valid = False

if is_valid:
    print("Valid Password")
else:
    print("Invalid Password")