from random import*;

'''
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
'''
#create dictionary 
thisdict = {}

#get the number of lines in each file

numlines = len(open("answers.txt", encoding = "utf8").readlines())


#create arrays that will go into dictionary
arrayanswers = []
arrayquestions = []

#fill arrays 
with open ("answers.txt", encoding = "utf8") as afile:
  for line in afile:
    each_line = line.strip()
    arrayanswers.append(each_line)
afile.close()


with open ("questions.txt", encoding = "utf8") as afile:
  for line in afile:
    each_line = line.strip()
    arrayquestions.append(each_line)
afile.close()

#fills dictionary
for x in range(numlines):
  thisdict.update({arrayquestions[x]:arrayanswers[x]})

print (thisdict)