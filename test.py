import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Anshu2004"
)

print(mydb)