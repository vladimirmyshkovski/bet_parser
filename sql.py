import datetime
import mysql.connector

cnx = mysql.connector.connect(user='root', database='narnik')
cursor = cnx.cursor()

#query = ("SELECT eventFK, home_odd, away_odd, under_odd, hdp, ou, active FROM narnik.score108_bettingoffer"
#         "WHERE eventFK %s hode_odd %s away_odd %s under_odd %s hdp %s ou %s active %s")

#cursor.execute(query, (hire_start, hire_end))

query = ("SELECT eventFK, home_odd, away_odd, under_odd, hdp, ou, active FROM narnik.score108_bettingoffer")

cursor.execute(query)

def main():
	for item in cursor:
		print(item)

	cursor.close()
	cnx.close()


#for (first_name, last_name, hire_date) in cursor:
#  print("{}, {} was hired on {:%d %b %Y}".format(
#    last_name, first_name, hire_date))




if __name__ == '__main__':
	main()