import csv, json

csvFilePath = './output/spidermanfinal.csv'
jsonFilePath = './output/spiderman.json'

# Find and replace bad chars in csv file
import os

texttofind = ','
texttoreplace = '.'
secondtexttofind = '|'
thirdtexttofind = '\''
thirdtexttoreplace=''
fourthtexttofind = '\"'
fifthtexttofind = '/'
sixthtexttofind = '\\'
sourcepath = os.listdir('./output/')
for file in sourcepath:
    inputfile = 'output/'+ file
    print('Conversion is in process for: ' +inputfile)
    with open(inputfile,'r') as inputfile:
        filedata = inputfile.read()
        freq = 0
        freq = filedata.count(texttofind)
    destinationpath = ('./output/' + file)
    filedata = filedata.replace(texttofind, texttoreplace)
    filedata = filedata.replace(secondtexttofind, texttofind)
    filedata = filedata.replace(thirdtexttofind, thirdtexttoreplace)
    filedata = filedata.replace(fourthtexttofind, thirdtexttoreplace)
    filedata = filedata.replace(fifthtexttofind, thirdtexttoreplace)
    filedata = filedata.replace(sixthtexttofind, thirdtexttoreplace)
    with open(destinationpath,'w') as file:
        file.write(filedata)

    print ('Total %d Records Replaced' %freq)


# Read the CSV and add the data to a dictionary.
# https://www.youtube.com/watch?v=La6ZO8vu-1w
data = []

with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for csvRow in csvReader:
        A = dict(csvRow)
        print(A)

# Write data to a JSON file.
with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(data))
