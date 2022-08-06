
from cs50 import get_int

# wile proving true of height input being between 1 and 8 it will break out of this While loop
while True:
    n = get_int("height: ")
    if n > 0 and n < 9:
        break

# better and easier way to call loops compared to C
for i in range(0, n, 1):
    # n+1+3 is the formula to place hashtags and spaces were they should be bases off the input typed in(1-8)
    for j in range(0, n+i+3, 1):
        if(j == n or j == n+1 or i+j < n-1):
            # end="" specifies that nothing will be printed at the end of out string
            print(" ", end="")
        else:
            print("#", end="")
    print()