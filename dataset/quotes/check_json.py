import json

data = {}
with open('quotes.json') as f:
	data = json.load(f)
f.close()

total = 0
sety = set()
for k,v in data.iteritems():
	print k, len(v)
	total+=len(v)
	for i in range(len(v)):
		sety.add(v[i])

print total
print len(sety)