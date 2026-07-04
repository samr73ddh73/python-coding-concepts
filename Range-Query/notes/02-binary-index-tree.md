# Used for fixe size array or string, and multiple queries of following types:
1. prefix operations (sum, xor, or)
2. update a value

- it is actually an array but concept is tree based
- it takes O(nlogn) processing time to create the binary indexed tree and O(n) auxillary space
- it is similar to segment tree
but why is it used?
- asymptodic time complexity between these two are same but upper bound for this is logn where as segment tree has 4logn
- similary it takes n+1 space and segent tree takes 4n space

- it can also be used for some range queries:
    range(i, j) = prefix(j)- prefix(i-1)

- cannt be used for all the scenarios where segment tree is used like min of a range or max of a range

