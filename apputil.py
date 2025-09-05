

# EXERCISE 1
# import all punctuation characters 
import string
# Function to check if a string is palindrome
def palindrome(str)

# String conversion to lowercase
    str = str.lower()

 # Removes spaces/punctuation
    for char in string.punctuation + " ":       #string.punctuation contains all common punctuation characters
        str = str.replace(char, "")
    
    # Check if the word is the same reversed
    return str == str[::-1]                     #string[start:stop:step]

#Test cases
print(palindrome("racecar"))             
print(palindrome("Nurses Run"))          
print(palindrome("Sit on a potato pan, Otis."))  
print(palindrome("Madam")


 #EXERCISE 2
 #Method 1

  def parentheses(sequence):
    # To keep track of open parentheses
    count = 0

    for char in sequence:
        if char == "(":
            count += 1  # increment for open parenthesis
        elif char == ")":
            count -= 1  # decrement for close parenthesis

        if count < 0:
            return False


    return count == 0   # parentheses are balanced


# Test cases
print(parentheses("((blah)()()())"))
print(parentheses("(((())blee))"))
print(parentheses("(()hello((())()))"))
print(parentheses("((((((())"))
print(parentheses("()))"))

  #Method 2
def parentheses(sequence):
    # declare empty list
    list = []
    for char in sequence:
        if char == "(":
            list.append("(")
        elif char == ")":
            if not list:  # no matching with"("
                return False
            list.pop()
    return len(list) == 0
#Test cases
print(parentheses("((blah)()()())"))
print(parentheses("(((())blee))"))
print(parentheses("(()hello((())()))"))
print(parentheses("((((((())"))
print(parentheses("()))"))
   
     
