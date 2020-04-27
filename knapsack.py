 # Aaron Shehan
# Het Patel


import sys

# The source for our 0-1 algorithm https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/
# The source foe our fractional algorithm https://www.geeksforgeeks.org/fractional-knapsack-problem/
# class containing Item attributes


'''We use 2 main algorthims to compute the knapsack, the 0-1 for whole cases, and the fractional approach for
the knapsack, we combine these two algotithms to make our own which gives us the best value for the knapsack which finds the max value between the two algorithms'''




class Item:
    def __init__(self, weight, value, t, index):
        self.wt = weight # weight attribute
        self.val = value #  value attribute
        self.type = t #  type attribute
        self.index = index # index attribute

# Time Complexity: O(nW) if W > n, else O(n^2)
def knapSack(W, items, n): 
    K = [[0 for x in range(W + 1)] for x in range(n + 1)] # initialize table to all zeros 

    # perform 0-1 knapsack, Time Complexity: O(nW)                                                                                   
    for i in range(n + 1): # iterate over the amount of item plus 1                                                                   
        for w in range(W + 1): # iterate over weight plus 1                                                                
            if i == 0 or w == 0: #check if i or w is equal to 0                                                               
                K[i][w] = 0  # if they are zero then set K[i][w] in the matrix equal to zero                                                                  
            elif items[i-1].wt <= w: # check if weight items[i-1] less then equal to w                                                          
                K[i][w] = max(items[i-1].val + K[i-1][w-items[i-1].wt],  K[i-1][w]) # then set K[i][w] of the matrix to the maximum of value of items[i-1] plus K[i-1][w-items[i-1].wt, and K[i-1][w]           
            else:                                                                              
                K[i][w] = K[i-1][w] # if those conditions are not met then set K[i][w]= K[i-1][w]                                                            


    w = W   # set w = weight                                                                                   
    res = K[n][W]     # set result = K[n][W]                                                                         
    itemsUsed = set()        # make a set for items Used                                                                  
    capacityUsed = 0       # set capacity used to 0                                                                    

    # trace table to find items that were used, cost/wt,  Time Complexity: O(n^2)
    for i in range(n, 0, -1): # iterate over the number of items
        if res <= 0: #  if result is less than or equal to zero
            break # then break out the loop
        if res == K[i - 1][w]: # if result is equal to K[i-1][W]
            continue # then continue the loop
        else: #  if the result is not equal to K[i-1][W]
            itemsUsed.add(items[i - 1].index)  # add item that was already used previously to set, Average Time Complexity: O(1), Worst Time Complexity O(n)
            capacityUsed += items[i - 1].wt # increment capacityUsed to items[i-1].wt
            res = res - items[i - 1].val # set result to result-items[i-1].val
            w = w - items[i - 1].wt  # set w to w - items[i-1].weight
   
   
    # if 0-1 knapsack algorithm doesn't cover all of W, then perform fractional knapsack with remaing 'f' items
    if (capacityUsed < W): # check if used capacity is less than W
        fractionalItems = [] # make a list to store the fractional items
        newMaxW = W - capacityUsed # set a new max W for fractional kanpsack which is W - the 0-1 capacity used
        for i in items: #  iterate over the items
            if i.index in itemsUsed: # see if item is already been used, Average Time Complexity: O(1), Worst Time Complexity O(n)
               continue # continue the loop
            if i.type == 'f': #  if the type for the item is fractional
                fractionalItems.append((i.wt, i.val)) # then append items weight and value attributes to the list for fractional items


        fractionalItems.sort(key=lambda x: x[1]//x[0], reverse=True)    # sort by cost per pound,  cost/wt,  Time Complexity: O(nlogn)
        totalValue = 0 # set total value to 0

        for i in fractionalItems: # compute fractional knapsack with remaing 'f' items, cost/wt,  Time Complexity: O(nlogn)
            if newMaxW - i[0] >= 0:  # cehck if the new max weight - i[0] is greater than 0
                newMaxW -= i[0] # decrement new max wight by i[0]
                totalValue += i[1] # incerement totalValue by i[1]
            else: #  if the new max weight is less than 0
                fraction = newMaxW / i[0] #  we set fraction ratio sequal to new max weight divided by i[0]
                totalValue += i[1] * fraction  # then incerement total value by i[1] mutliplied by fraction
                break # then we break out the for loop

        return K[n][W] + totalValue # return the new value
    else:
        return K[n][W] # return the value


# Time Complexity: O(nlogn)
def knapSack2(W, items):
    items.sort(key=lambda x: x.val//x.wt, reverse=True)   # sort by cost per pound,  cost/wt,  Time Complexity: O(nlogn)
    items.sort(key=lambda x: x.type)   # sort by type ('f' or 'w'),  Time Complexity: O(nlogn)
    totalValue = 0 # set total value to 0

    # regular fractional knapsack algorithm, but do not include 'w' items
    for i in items: # iterate over items
        if W - i.wt >= 0: # if weight - i.wt is greater than equal to 0
            W -= i.wt # decrement W and set it to -i.wt
            totalValue += i.val # increment total value and set it to i.val
        else: 
            if i.type == 'w': # skip if item is 'w'
                continue # continue the for loop
            fraction = W / i.wt # set the fractional ratio as weight/ i.wt
            totalValue += i.val * fraction  # incement totalvalue by i.val multiplied by fraction
            W = int(W - (i.wt * fraction)) # set weight equal to w-(i.wt * fraction)
            break # break the for loop
    return totalValue #return the total value

#this function combines the two algorithms and finds the max value between them
def combinedKnapsack(W, items):
    return max(knapSack(W, items.copy(), len(items)), knapSack2(W, items.copy())) # combine the two algorithms by finding the max value between the them




items = [] # list of items

f = open('input.txt', 'r') # open input file
lines = f.readlines() # read input file into list of lines

for i, j in enumerate(lines): #loop over the lines
    tokens = j.split(' ') # split line by whitespace
    items.append(Item(int(tokens[1]), int(tokens[2]), tokens[3].rstrip('\n'), i)) #append items to list and strip new line char
	


print('result: ', combinedKnapsack(int(sys.argv[1]), items))
