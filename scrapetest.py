f = open('test-candidates.txt')
lines = f.readlines()
writer = open('senators.txt','w')
for line in lines:
  parts = line.split('\t')
  print parts
  writer.write('%s\tsenator\t%s\t%s\n'%(parts[1],parts[2],parts[2]))
writer.flush()
writer.close()
f.close()