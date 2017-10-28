import urllib2
import zipfile
#import mysql.connector

print("Welcome to the liberation of trading: TradeFree")

#urllib2.quote

outfile = open("./data/ref_currency.zip", "w")

try:
    response = urllib2.urlopen("https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip?d4acbc94de4b8c8a6550ef5d9be07261")
except:
    print("Fail")
#html = response.read()

outfile.write(response.read())
outfile.close()

zip_ref = zipfile.ZipFile("./data/ref_currency.zip", 'r')
zip_ref.extractall("./data")
zip_ref.close()


try:
    fxFile = open("./data/eurofxref.csv", "r")
except IOError:
    print "The file does not exist"

input = fxFile.readlines()
fxFile.close()

for line in input:
    records = line.split(",")
    for pair in records:
        print(pair)

#for i=0;i<4;i++:
#    print

#try:
#  cnx = mysql.connector.connect(user='scott',
#                                database='testt')
#except mysql.connector.Error as err:
#  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#    print("Something is wrong with your user name or password")
#  elif err.errno == errorcode.ER_BAD_DB_ERROR:
#    print("Database does not exist")
#  else:
#    print(err)
#else:
#  cnx.close()
