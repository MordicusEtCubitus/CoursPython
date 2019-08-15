
from memory_profiler import profile

def my_range(start, stop, step=1):
    """
    Reproduce a simple version of Python 2 *range* function
    
    Examples:
    
    >>> my_range(10, 20, 2)
    [10, 12, 14, 16, 18]
    
    >>> my_range(20, 10, -2)
    [20, 18, 16, 14, 12]
    
    >>> my_range(10, 20, -1)
    []
    """
    result = []
    
    while start * step < stop * step:
        result.append(start)
        start += step
        
    return result

@profile
def memtest():
    a = my_range(0, 10**6)
    b = my_range(0, 10**6)

if __name__ == "__main__":
   memtest()
