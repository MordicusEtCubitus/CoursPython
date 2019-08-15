# Exemple 
import sys
old_profiler = sys.getprofile()

def my_profiler(frame, event, arg):
    print(f"frame={frame}, event={event}, arg={type(arg)}")
    
    
def square(x):
    return x ** 2

a = list(range(10))
b = list(range(5,15))

# Setting the profiler
sys.setprofile(my_profiler)

square(10)

# Restoring the previous profiler
sys.setprofile(old_profiler)
