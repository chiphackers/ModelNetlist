import math

def Initial_Gap(h):
    if h==1:
        return 0
    else:
        return math.pow(2,h-2) + Initial_Gap(h-1)

def Tree(A):
    h = int(math.floor(math.log(len(A),2))+1)
    for i in range(h,0,-1):
        print ('\n')
        print ('  '*int(Initial_Gap(i)), end=" ")
        for j in A[int(math.pow(2,h-i)-1):int(math.pow(2,h-i+1)-1)]:
            print (str(j) + ' '*(2-len(str(j))) + '  '*int(Initial_Gap(i+1)-1)+' ', end=" " ) 

def HEAPIFY(A,i):
    L = 2*i+1
    R = 2*i+2
    if (L <= len(A)-1) and (A[L]>A[i]):
        Largest = L
    else:
        Largest = i
    if (R <= len(A)-1) and (A[R] > A[Largest]):
        Largest = R
    if (Largest != i):
        Temp = A[Largest]
        A[Largest] = A[i]
        A[i] = Temp
        HEAPIFY(A,Largest)
    return A
    
def BUILD_HEAP(A):
    k = int(math.floor((len(A)/2)-1))
    for i in range(k,-1,-1):
        HEAPIFY(A,i)
    
def HEAP_SORT(A):
    BUILD_HEAP(A)
    for i in range(len(A)-1,0,-1):
        Temp = A[i]
        A[i] = A[0]
        A[0] = Temp
        A = HEAPIFY(A[:-(len(A)-i)],0)+A[i:]
    return A

def MaxMinClk():
    lines = [line.rstrip('\n') for line in open('file1')]
    Array=[]
    for i in lines:
        Array.append(int(i.split()[1]))	
	
    Tree(Array)
    print('\n')
    global x
    x = HEAP_SORT(Array)
    for j in lines:
        if (int(j.split()[1]))	== x[0]:
            print ('Minimum FF driven clk =',(j.split()[0]))
        elif (int(j.split()[1])) == x[-1]:
            print ('Maximum FF driven clk =',(j.split()[0]))

MaxMinClk()

Tree(x)
print('\n')        
