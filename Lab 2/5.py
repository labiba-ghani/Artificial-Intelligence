# Default Parameter Value

def my_function(country = "Norway"): 
    print("I am from " + country) 
my_function("Sweden")  
my_function("India")  
my_function()  
my_function("Brazil")
print() 

# Passing a List as a Parameter 

def my_function(food): 
    for x in food: 
        print(x) 
food = ["apple", "banana", "cherry"] 
my_function(food)
print()

# Return Values 

def my_function(x): 
    return 5 * x 
print(my_function(3)) 
print(my_function(5)) 
print(my_function(9))
print()

# Keyword Arguments 
def my_function(child3,child2,child1):
    print(f"the yougest child is {child3}")

my_function(child1 = "Emil", child2 = "Tobias", child3 = "Linus")