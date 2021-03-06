import sys

#Find S-Numbers

#We define an -number to be a natural number, , 
#that is a perfect square and its square root can be 
#obtained by splitting the decimal representation of  
#into 2 or more numbers then adding the numbers.
#https://projecteuler.net/problem=719
#Examples - 9801, 6724, 8281

def evaluateCompositions(n, i, maxN):
    if (n == 0): 
        compArr = []
        for k in range(i):
            compArr.append(arr[k])
        compositions.append(compArr)
    elif(n > 0): 
        for k in range(1, maxN): 
            arr[i] = k
            evaluateCompositions(n-k, i+1, maxN)

if( len(sys.argv) < 2 ) :
    print("Need a number is parameter.")
    sys.exit()

argNum = sys.argv[1]
if( not argNum.isnumeric() ) :
    print("Input parameter must be a whole number. No decimals, no negatives.")
    sys.exit()

maxN = int(argNum)
sNumberTotal = 0
for num in range(1, maxN+1) :
    strNum = str(num)
    sqrt = num ** 0.5
    #print("Checking if", num, "with square root", sqrt, "is an S-Number")
    isSNumber = False

    if( int(sqrt) == sqrt ) :
        N = len(strNum)
        arr = [0] * 100
        compositions = []
        evaluateCompositions(N, 0, N)

        nums = []
        for composition in compositions :
            idx = 0
            total = 0
            nums = []
            for numDigit in composition :
                aNum = int( strNum[idx:idx+numDigit] )
                nums.append(aNum)
                total = total + aNum
                idx = idx + numDigit
            if( total == sqrt ) :
                isSNumber = True
                break

    if( isSNumber ) :
        sNumberTotal += num

print("Total is", sNumberTotal)