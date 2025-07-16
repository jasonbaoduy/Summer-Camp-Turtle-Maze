# Imported the turtle library and set it to turt
import turtle as turt

#Basic example no loop
turt.fd(100) # Move forward 100 pixels
turt.left(90) # Turn left 90 degrees
turt.fd(100) # repeat 
turt.left(90)
turt.fd(100)
turt.left(90)
turt.fd(100)

# #Same process in loop
for i in range(4): # Set how many times the loop will run 
    turt.fd(100) # Move forward 100 pixels
    turt.left(90) # Turn left 90 degrees

# In a function
def square(): # Define the function 'square'
    for i in range(4): # Same as the above loop
        turt.fd(100)
        turt.left(90)
        
square() # Call the function to run it


# Will keep the window open until mouse is clicked
turt.Screen().exitonclick()


