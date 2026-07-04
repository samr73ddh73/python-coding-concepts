#initializing a set from list:

set1=set([1,2,3,2,2,4,5,5])
set2=set([6,7,8,1,2])
print(set1)

#set operations
#1.Union
unionset=set1.union(set2)
print(unionset)
#2.Intersection
interset=set1.intersection(set2)
print(interset)
#3.Difference
diff=set1.difference(set2)
print(diff)
#4.SymmetricDifference
symmdiff=set1.symmetric_difference(set2)
print(symmdiff)

#5. check subset:
print(set1.issubset(set2))
print(set2.issuperset(set1))