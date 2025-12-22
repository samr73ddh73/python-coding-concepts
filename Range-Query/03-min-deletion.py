def build(s, seg, ind, start, end):
    if start == end:
        seg[ind] = (s[start], 0)
    else:
        mid = (start + end)//2
        build(s, seg, 2*ind+1, start, mid)
        build(s, seg, 2*ind+2, mid+1, end)
        leftS, ld = seg[2*ind+1]
        rightS, rd = seg[2*ind+2]
        extra = 1 if leftS[-1] == rightS[0] else 0
        midD = ld + rd + extra
        seg[ind] = (leftS+rightS, midD)


def main():
    s = 'ABAAAAABBAB'
    n = len(s)
    seg = [ None for _ in range(4*n+1)]
    build(s, seg, 0, 0, n-1)
    print(seg)

main()