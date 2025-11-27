def longest_consecutive_sequence(nums: list[int]) -> int:
    # WRITE YOUR BRILLIANT CODE HERE
    s = set()
    for n in nums:
        s.add(n)
    l = 0
    for n in nums:
        i = 0
        count = 0
        while(True):
            if (n+i) in s:
                count += 1
                i+=1
            else:
                break
        l = max(l, count)
    return l

if __name__ == "__main__":
    nums = [int(x) for x in input().split()]
    res = longest_consecutive_sequence(nums)
    print(res)
