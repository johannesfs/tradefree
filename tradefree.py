import urllib2
import zipfile
import logging
logging.basicConfig(filename='./log/tradefree.log',format='%(asctime)s %(levelname)s:%(message)s',level=logging.INFO)

from collections import defaultdict
import mysql.connector
from datetime import date, datetime, timedelta

print("Welcome to the liberation of trading: TradeFree")

dataDirectory = "/Users/johannes/Projects/tradefree/data"
historicalDataUrl = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist\
.zip?76f8c1fe67f7febddf32443dbafa6424"
currentDataUrl = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip?d4acbc94de4b8c8a6550ef5d9be07261"

outfile = open(dataDirectory + "/ref_currency.zip", "w")

try:
    response = urllib2.urlopen(historicalDataUrl)
except:
    print("Fail")
#html = response.read()

outfile.write(response.read())
outfile.close()

zip_ref = zipfile.ZipFile("./data/ref_currency.zip", 'r')
zip_ref.extractall("./data")
zip_ref.close()


try:
    fxFile = open("./data/eurofxref-hist.csv", "r")
except IOError:
    print "The file does not exist"

input = fxFile.readlines()
fxFile.close()

rowNumber = 0
currencyPair = {}
fxRates = defaultdict(dict)

for line in input:
    i = 0
    date = ""
    records = line.split(",")
    
    for pair in records:
        
        if i == 0:
            date = pair

        if rowNumber == 0:
            currencyPair[i] = "EUR/" + str(pair)
        elif i > 0:
            fxRates[currencyPair[i]][date] = pair
                            
        i = i + 1
    rowNumber = rowNumber + 1
logging.info("Parsed " + str(rowNumber)  + " of rows")

logging.debug(str(fxRates["EUR/USD"]))

try:
    logging.debug("Connecting to mysql")
    cnx = mysql.connector.connect(user='johannes', passwd='tluhmmal75', host='localhost', database='tradefree')
except mysql.connector.Error as err:
    print(err.errno)
#    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#        print("Something is wrong with your user name or password")
#    elif err.errno == errorcode.ER_BAD_DB_ERROR:
#        print("Database does not exist")
#    else:
#        print(err)
else:
    logging.error("Shutting down mysql connection")
    cnx.close()

cursor = cnx.cursor()

## Example code
tomorrow = datetime.now().date() + timedelta(days=1)

add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

# Insert new employee
cursor.execute(add_employee, data_employee)
emp_no = cursor.lastrowid

# Insert salary information
data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}
cursor.execute(add_salary, data_salary)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()
