from py2neo import Node,Relationship,Graph
from py2neo import watch
graph = Graph()

statement = "match (n:Person) return n.name as name limit 20;"
# print( type( graph.cypher.execute(statement)) )
result = graph.cypher.execute(statement)
# print(result)
su = []
i = 1
for record in result:
	# t = (record.name,i)
	su.append((record.name,i))
	i = i + 1
q = dict(su)
print(q['liyi'])
# print(result[0].name)
# print(watch("httpstream"))
# rec = graph.cypher.execute(statement)
# print(rec)