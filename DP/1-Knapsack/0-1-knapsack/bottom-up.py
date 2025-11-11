def knapsack(wt, profit, n, capacity):
    mem = [[0]*(capacity+1) for _ in range(n+1) ]
    for numIdx in range(1, n+1):
        for cap in range(1, capacity+1):
            if wt[numIdx-1] <= cap:
                mem[numIdx][cap] = max(
                    profit[numIdx-1] + mem[numIdx-1][cap-wt[numIdx-1]],
                    mem[numIdx-1][cap]
                )
            else:
                mem[numIdx][cap] = mem[numIdx-1][cap]
    return mem[n][capacity]

def main():
    wt = [3, 1, 5, 2]
    profit = [23, 37, 52, 1]
    capacity = 7
    n = len(wt)
    
    result = knapsack(wt, profit, n, capacity)
    print(f"Maximum profit: {result}")

if __name__ == "__main__":
    main() 



#time complexity: O(n* capacity)
# space: O(n* capacity) 