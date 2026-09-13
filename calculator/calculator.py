def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

def power(a, b):
    return a**b

def modulus(a, b):
    return a%b

def display_result(result):
    if result.is_integer():
        print(f"Result ={int(result)}")
    else:
        print(f"Result = {result}")

def format_number(num):
    if num.is_integer():
        return int(num)
    else:
        return num
    
history = []

try:
    with open("history.txt", "r") as f:
        for line in f:
            history.append(line.strip())

except FileNotFoundError:
    pass

while True:

 print("-"*25)
 print("     CALCULATOR")
 print("-"*25)
      
 print("1. Addition")
 print("2. Subtraction")
 print("3. Multiplication")
 print("4. Division")
 print("5. Power")
 print("6. Modulus")
 print("7. View History")
 print("8. Exit")
 print("")

 choice=input("Choose the option: ")

 if choice in ["1","2","3","4","5","6"]:
  try:
    a=float(input("Enter Value 1:"))
    b=float(input("Enter Value 2:"))
  except ValueError:
    print("Please! Enter the Valid Number")
    continue
  
  if choice=="1":
        result = add(a,b)
        history.append(f"{format_number(a)} + {format_number(b)} = {format_number(result)}")
        display_result(result)

  elif choice=="2":
        result = subtract(a,b)
        history.append(f"{format_number(a)} - {format_number(b)} = {format_number(result)}")
        display_result(result)

  elif choice=="3":
        result = multiply(a,b)
        history.append(f"{format_number(a)} * {format_number(b)} = {format_number(result)}")
        display_result(result)

  elif choice=="4":
        if(b==0):
            print("Error: Cannot divide by zero.")
        else:
            result = divide(a,b)
            history.append(f"{format_number(a)} / {format_number(b)} = {result:.4f}")
            display_result(result)

  elif choice=="5":
        result = power(a,b)
        history.append(f"{format_number(a)} ^ {format_number(b)} = {format_number(result)}")
        display_result(result)

  elif choice=="6":
        if(b==0):
            print("Error: Cannot divide by zero.")
        else:
            result = modulus(a,b)
            history.append(f"{format_number(a)} % {format_number(b)} = {format_number(result)}")
            display_result(result)

 elif choice=="7":
     print("-"*25)
     print("    HISTORY")
     print("-"*25)

    #  if len(history) == 0:
     if not history:
        print("No calculations yet!")
     else:
        for item in history:
            print(item)
            print("")

 elif choice=="8":
     print("Thank you for using the calculator!")
     with open("history.txt", "w") as f:
         for item in history:
             f.write(item + "\n")
     break
 else:
        print("Invalid choice! Please select a number between 1 and 8.")


        