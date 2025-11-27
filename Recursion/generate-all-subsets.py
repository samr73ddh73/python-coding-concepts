def generate(n, str, res):
    if n == 0:
        res.append(str)
        return res
    generate(n-1, str+'0', res)
    generate(n-1, str+'1', res)
    return res

def main():
    print(generate(3, '', []))
    res = generate(3, '', [])
    arr = [ 1, 2, 3]
    output = []
    for bits in res:
        curr = []
        for i in range(len(bits)):
            if bits[i] == '1':
                curr.append(arr[i])
        output.append(curr)
    print(output)

main()