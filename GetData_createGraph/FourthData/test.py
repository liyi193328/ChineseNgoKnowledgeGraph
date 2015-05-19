import pickle
fp = open("orginfoFourthData.pkl","rb")
ngo = pickle.load(fp)
print(len(ngo))
for i in ngo:
	print(i.name)