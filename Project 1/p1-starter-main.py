#
# Jiaxin Lu
# jlu73@uic.edu
#
import sqlite3
import matplotlib.pyplot as plt
import datetime

##################################################################  
#
# print_stats
#
# Given a connection to the database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General Statistics:")
    
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras;")
    row = dbCursor.fetchone()
    print("  Number of Red Light Cameras:", f"{row[0]}")
    
##################################################################  

##################################################################  
#
# Command 1
# Find all the intersections that match the user input.
#
def command1(dbConn):
    dbCursor = dbConn.cursor()
    stationName = input("Enter the name of the intersection to find (wildcards _ and % allowed): ")

    sql =   """
            SELECT INTERSECTION_ID, INTERSECTION
            FROM INTERSECTIONS
            WHERE INTERSECTION LIKE ?
            ORDER BY INTERSECTION
            """

    dbCursor.execute(sql, (stationName,))
    result = dbCursor.fetchall()

    if not result:
        print("No intersections matching that name were found.")
    else:
        for row in result:
            print(row[0], ":", row[1])
    
##################################################################  

##################################################################  
#
# Command 2
# Given the name of an intersection, find all the cameras located at that intersection.
#
def command2(dbConn):
    dbCursor = dbConn.cursor()
    intersection = input("Enter the name of the intersection (no wildcards allowed): ")

    sql1 =  """
            SELECT CAMERA_ID, ADDRESS
            FROM INTERSECTIONS 
            JOIN REDCAMERAS
            ON INTERSECTIONS.INTERSECTION_ID = REDCAMERAS.INTERSECTION_ID
            WHERE INTERSECTION = ?
            ORDER BY CAMERA_ID
            """
    dbCursor.execute(sql1, (intersection,))
    result1 = dbCursor.fetchall()
    if not result1:
        print("No red light cameras found at that intersection.")
    else:
        print("Red Light Cameras:")
        for row in result1:
            print(row[0], ":", row[1])

    print()
    sql2 =  """
            SELECT CAMERA_ID, ADDRESS
            FROM INTERSECTIONS 
            JOIN SPEEDCAMERAS
            ON INTERSECTIONS.INTERSECTION_ID = SPEEDCAMERAS.INTERSECTION_ID
            WHERE INTERSECTION = ?
            ORDER BY CAMERA_ID
            """
    dbCursor.execute(sql2, (intersection,))
    result2 = dbCursor.fetchall()
    if not result2:
        print("No speed cameras found at that intersection.")
    else:
        print("Speed Cameras:")
        for row in result2:
            print(row[0], ":", row[1])
    
##################################################################  

##################################################################  
#
# Command 3
# Find the number of red light violations for that date across all cameras 
# and the number of speed violations for that date across all cameras. 
# Also show the percentages of each, taken out of the total number of violations.
#
def command3(dbConn):
    dbCursor = dbConn.cursor()
    date = input("Enter the date that you would like to look at (format should be YYYY-MM-DD): ")

    sql1 =  """
            SELECT SUM(NUM_VIOLATIONS)
            FROM REDVIOLATIONS
            WHERE VIOLATION_DATE = ?
            GROUP BY VIOLATION_DATE
            """
    sql2 =  """
            SELECT SUM(NUM_VIOLATIONS)
            FROM SPEEDVIOLATIONS
            WHERE VIOLATION_DATE = ?
            GROUP BY VIOLATION_DATE
            """

    dbCursor.execute(sql1, (date,))
    result1 = dbCursor.fetchall()
    if not result1:
        print("No violations on record for that date.")
        return
    numRed = result1[0][0]

    dbCursor.execute(sql2, (date,))
    result2 = dbCursor.fetchall()
    if not result2:
        print("No violations on record for that date.")
        return
    numSpeed = result2[0][0]

    sum = numRed + numSpeed
    percentRed = (numRed / sum) * 100
    percentSpeed = (numSpeed / sum) * 100

    print("Number of Red Light Violations:",f"{numRed:,}",f"({percentRed:.3f}%)")
    print("Number of Speed Violations:",f"{numSpeed:,}",f"({percentSpeed:.3f}%)")
    print("Total Number of Violations:",f"{sum:,}")

##################################################################  

##################################################################  
#
# Command 4
# Output the number of red light cameras at each intersection, 
# along with the percentages (taken out of the total number of red light cameras in Chicago).
# Then output the number of speed cameras at each intersection, 
# along with the percentages (taken out of the total number of speed cameras in Chicago).
#
def command4(dbConn):
    dbCursor = dbConn.cursor()

    sql1 =  """
            SELECT INTERSECTION, INTERSECTIONS.INTERSECTION_ID, COUNT(CAMERA_ID)
            FROM INTERSECTIONS
            JOIN REDCAMERAS
            ON INTERSECTIONS.INTERSECTION_ID = REDCAMERAS.INTERSECTION_ID
            GROUP BY INTERSECTION
            ORDER BY COUNT(CAMERA_ID) DESC
            """
    
    sql2 =  """
            SELECT INTERSECTION, INTERSECTIONS.INTERSECTION_ID, COUNT(CAMERA_ID)
            FROM INTERSECTIONS
            JOIN SPEEDCAMERAS
            ON INTERSECTIONS.INTERSECTION_ID = SPEEDCAMERAS.INTERSECTION_ID
            GROUP BY INTERSECTION
            ORDER BY COUNT(CAMERA_ID) DESC
            """
    
    sql3 =  """
            SELECT COUNT(*)
            FROM REDCAMERAS
            """
    
    sql4 =  """
            SELECT COUNT(*)
            FROM SPEEDCAMERAS
            """

    dbCursor.execute(sql1)
    result1 = dbCursor.fetchall()
    dbCursor.execute(sql2)
    result2 = dbCursor.fetchall()
    dbCursor.execute(sql3)
    result3 = dbCursor.fetchall()
    sum1 = result3[0][0]
    dbCursor.execute(sql4)
    result4 = dbCursor.fetchall()
    sum2 = result4[0][0]

    print("Number of Red Light Cameras at Each Intersection")
    for row in result1:
        percent = (row[2] / sum1) * 100
        print(row[0], f"({row[1]})", ":", row[2], f"({percent:.3f}%)")
    print()
    print("Number of Speed Cameras at Each Intersection")
    for row in result2:
        percent = (row[2] / sum2) * 100
        print(row[0], f"({row[1]})", ":", row[2], f"({percent:.3f}%)")
    
##################################################################  

##################################################################  
#
# Command 5
# Find all the intersections that match the user input.
#
def command5(dbConn):
    dbCursor = dbConn.cursor()
    year = input("Enter the year that you would like to analyze: ")

    sql1 =  """
            SELECT INTERSECTION, INTERSECTIONS.INTERSECTION_ID, SUM(NUM_VIOLATIONS)
            FROM INTERSECTIONS
            JOIN REDCAMERAS
            ON INTERSECTIONS.INTERSECTION_ID = REDCAMERAS.INTERSECTION_ID
            JOIN REDVIOLATIONS
            ON REDCAMERAS.CAMERA_ID = REDVIOLATIONS.CAMERA_ID
            WHERE STRFTIME('%Y', VIOLATION_DATE) = ?
            GROUP BY INTERSECTION
            ORDER BY SUM(NUM_VIOLATIONS) DESC
            """
    
    sql2 =  """
            SELECT SUM(NUM_VIOLATIONS)
            FROM REDVIOLATIONS
            WHERE STRFTIME('%Y', VIOLATION_DATE) = ?
            """
    
    sql3 =  """
            SELECT INTERSECTION, INTERSECTIONS.INTERSECTION_ID, SUM(NUM_VIOLATIONS)
            FROM INTERSECTIONS
            JOIN SPEEDCAMERAS
            ON INTERSECTIONS.INTERSECTION_ID = SPEEDCAMERAS.INTERSECTION_ID
            JOIN SPEEDVIOLATIONS
            ON SPEEDCAMERAS.CAMERA_ID = SPEEDVIOLATIONS.CAMERA_ID
            WHERE STRFTIME('%Y', VIOLATION_DATE) = ?
            GROUP BY INTERSECTION
            ORDER BY SUM(NUM_VIOLATIONS) DESC
            """
    
    sql4 =  """
            SELECT SUM(NUM_VIOLATIONS)
            FROM SPEEDVIOLATIONS
            WHERE STRFTIME('%Y', VIOLATION_DATE) = ?
            """

    dbCursor.execute(sql1, (year,))
    result1 = dbCursor.fetchall()
    dbCursor.execute(sql2, (year,))
    result2 = dbCursor.fetchall()
    sum1 = result2[0][0]
    dbCursor.execute(sql3, (year,))
    result3 = dbCursor.fetchall()
    dbCursor.execute(sql4, (year,))
    result4 = dbCursor.fetchall()
    sum2 = result4[0][0]

    print("Number of Red Light Violations at Each Intersection for", f"{year}")
    if not result1:
        print("No red light violations on record for that year.")
    else:
        for row in result1:
            percent = (row[2] / sum1) * 100
            print(row[0], f"({row[1]})", ":", f"{row[2]:,}", f"({percent:.3f}%)")
        print("Total Red Light Violations in", f"{year}", ":", f"{sum1:,}")

    print()
    print("Number of Speed Violations at Each Intersection for", f"{year}")
    if not result3:
        print("No speed violations on record for that year.")
    else:
        for row in result3:
            percent = (row[2] / sum2) * 100
            print(row[0], f"({row[1]})", ":", f"{row[2]:,}", f"({percent:.3f}%)")
        print("Total Speed Violations in", f"{year}", ":", f"{sum2:,}")
    
##################################################################  

##################################################################  
#
# Command 6
# Output the number of violations recorded by that camera for each year, in ascending order by year.
#
def command6(dbConn):
    dbCursor = dbConn.cursor()
    cameraId = input("Enter a camera ID: ")

    sql =   """
            SELECT STRFTIME('%Y', VIOLATION_DATE) AS YEAR, SUM(NUM_VIOLATIONS)
            FROM (
                SELECT CAMERA_ID, VIOLATION_DATE, NUM_VIOLATIONS FROM REDVIOLATIONS
                UNION ALL
                SELECT CAMERA_ID, VIOLATION_DATE, NUM_VIOLATIONS FROM SPEEDVIOLATIONS
            )
            WHERE CAMERA_ID = ?
            GROUP BY YEAR
            ORDER BY YEAR
            """

    dbCursor.execute(sql, (cameraId,))
    result = dbCursor.fetchall()

    if not result:
        print("No cameras matching that ID were found in the database.")
    else:
        print("Yearly Violations for Camera", f"{cameraId}")
        for row in result:
            print(row[0], ":", f"{row[1]:,}")
    
    plot = input("Plot? (y/n) ")
    if(plot != 'y'):
        return
    else: 
        years = []
        numbers = []
        for row in result:
            years.append(row[0])
            numbers.append(row[1])
        
        plt.plot(years, numbers, color='b', linestyle='-')
        plt.xlabel("Year")
        plt.ylabel("Number of Violations")
        plt.title(f"Yearly Violations for Camera %s" %cameraId)
        plt.xticks(years)
        plt.legend()
        plt.grid(False)
        plt.show()

##################################################################  

##################################################################  
#
# Command 7
# Output the number of violations recorded by that camera for each month in the specified year, in ascending order by month.
#
def command7(dbConn):
    dbCursor = dbConn.cursor()
    cameraId = input("Enter a camera ID: ")
    year = input("Enter a year: ")

    sql =   """
            SELECT STRFTIME("%m/%Y", VIOLATION_DATE), SUM(NUM_VIOLATIONS)
            FROM (
                SELECT CAMERA_ID, VIOLATION_DATE, NUM_VIOLATIONS FROM REDVIOLATIONS
                UNION ALL
                SELECT CAMERA_ID, VIOLATION_DATE, NUM_VIOLATIONS FROM SPEEDVIOLATIONS
            )
            WHERE CAMERA_ID = ? AND STRFTIME('%Y', VIOLATION_DATE) = ?
            GROUP BY STRFTIME("%m/%Y", VIOLATION_DATE)
            ORDER BY STRFTIME("%m/%Y", VIOLATION_DATE)
            """

    dbCursor.execute(sql, (cameraId, year))
    result = dbCursor.fetchall()

    if not result:
        print("No cameras matching that ID were found in the database.")
    else:
        print("Monthly Violations for Camera", f"{cameraId}", "in", f"{year}")
        for row in result:
            print(row[0], ":", f"{row[1]:,}")
    
    plot = input("Plot? (y/n) ")
    if(plot != 'y'):
        return
    else: 
        months = []
        numbers = []
        for row in result:
            months.append(row[0][:2])
            numbers.append(row[1])
        
        plt.plot(months, numbers, color='b', linestyle='-')
        plt.xlabel("Month")
        plt.ylabel("Number of Violations")
        plt.title(f"Monthly Violations for Camera %s (%s)" %(cameraId, year))
        plt.xticks(months)
        plt.legend()
        plt.grid(False)
        plt.show()

##################################################################  

##################################################################  
#
# Command 8
# Output the number of red light violations across all red light cameras, 
# and the number of speed violations across all speed cameras, for each day in that year. 
# The data should be displayed in ascending order by the date.
#
def command8(dbConn):
    dbCursor = dbConn.cursor()
    year = input("Enter a year: ")

    sql1 =   """
            SELECT DATE(VIOLATION_DATE), SUM(NUM_VIOLATIONS)
            FROM REDVIOLATIONS
            WHERE STRFTIME('%Y', VIOLATION_DATE) = ?
            GROUP BY DATE(VIOLATION_DATE)
            ORDER BY DATE(VIOLATION_DATE)
            """

    sql2 =   """
            SELECT DATE(VIOLATION_DATE), SUM(NUM_VIOLATIONS)
            FROM SPEEDVIOLATIONS
            WHERE STRFTIME('%Y', VIOLATION_DATE) = ?
            GROUP BY DATE(VIOLATION_DATE)
            ORDER BY DATE(VIOLATION_DATE)
            """

    dbCursor.execute(sql1, (year,))
    result1 = dbCursor.fetchall()
    dbCursor.execute(sql2, (year,))
    result2 = dbCursor.fetchall()

    print("Red Light Violations: ")
    i = 0
    for row in result1:
        i = i + 1
        if i <= 5 or i > len(result1) - 5:
            print(row[0], row[1])

    print("Speed Violations: ")
    i = 0
    for row in result2:
        i = i + 1
        if i <= 5 or i > len(result2) - 5:
            print(row[0], row[1])

    start_date = datetime.date(int(year), 1, 1)
    end_data = datetime.date(int(year), 12, 31)
    dates = []
    current_date = start_date
    while current_date <= end_data:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += datetime.timedelta(days=1)

    day = 1
    redCounter = 0
    speedCounter = 0
    x = []
    y1 = []
    y2 = []
    for date in dates:
        x.append(day)
        day = day + 1
        if(redCounter < len(result1) and result1[redCounter][0] == date):
            y1.append(result1[redCounter][1])
            redCounter += 1
        else:
            y1.append(0)
        if(speedCounter < len(result2) and result2[speedCounter][0] == date):
            y2.append(result2[speedCounter][1])
            speedCounter += 1
        else:
            y2.append(0)
    
    plot = input("Plot? (y/n) ")
    if(plot != 'y'):
        return
    else: 
        pass
        
        plt.plot(x, y1, color='red', linestyle='-')
        plt.plot(x, y2, color='orange', linestyle='-')
        plt.xlabel("Day")
        plt.ylabel("Number of Violations")
        plt.title("Violations Each Day of %s" %year)
        plt.legend(["Red Light", "Speed"])
        plt.grid(False)
        plt.show()

##################################################################  

##################################################################  
#
# Command 9
# Output all red light cameras and all speed cameras that are physically located on that street. 
# Display the ID, address, latitude and longitude of those cameras, in ascending order by the camera ID.
#
def command9(dbConn):
    dbCursor = dbConn.cursor()
    streetName = input("Enter a street name: ")

    sql1 =   """
            SELECT CAMERA_ID, ADDRESS, LATITUDE, LONGITUDE
            FROM REDCAMERAS
            WHERE ADDRESS LIKE ?
            ORDER BY CAMERA_ID
            """

    sql2 =   """
            SELECT CAMERA_ID, ADDRESS, LATITUDE, LONGITUDE
            FROM SPEEDCAMERAS
            WHERE ADDRESS LIKE ?
            ORDER BY CAMERA_ID
            """

    dbCursor.execute(sql1, (f"%{streetName}%",))
    result1 = dbCursor.fetchall()
    dbCursor.execute(sql2, (f"%{streetName}%",))
    result2 = dbCursor.fetchall()

    longitudes1 = []
    latitudes1 = []
    longitudes2 = []
    latitudes2 = []

    if not result1 and not result2:
        print("There are no cameras located on that street.")
        return
    
    if result1:
        print("List of Cameras Located on Street: %s" %(streetName))
        print("Red Light Cameras: ")
        for row in result1:
            print(row[0], ":", row[1], f"{(row[2], row[3])}")
            longitudes1.append(row[3])
            latitudes1.append(row[2])
    if result2:
        print("Speed Cameras: ")
        for row in result2:
            print(row[0], ":", row[1], f"{(row[2], row[3])}")
            longitudes2.append(row[3])
            latitudes2.append(row[2])

    plot = input("Plot? (y/n) ")
    if(plot != 'y'):
        return
    else: 
        pass

    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    plt.imshow(image, extent=xydims)
    plt.title("Cameras on Street: %s" %(streetName))

    plt.plot(longitudes1, latitudes1, color='red', marker='o')
    plt.plot(longitudes2, latitudes2, color='orange', marker='o')

    for row in result1:
        plt.annotate(row[0], (row[3], row[2]))
    for row in result2:
        plt.annotate(row[0], (row[3], row[2]))
    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])
    plt.show()

##################################################################  

#
# main
#
dbConn = sqlite3.connect('chicago-traffic-cameras.db')

print("Project 1: Chicago Traffic Camera Analysis")
print("CS 341, Spring 2025")
print()
print("This application allows you to analyze various")
print("aspects of the Chicago traffic camera database.")
print()
print_stats(dbConn)
print()

print("Select a menu option: ")
print("  1. Find an intersection by name")
print("  2. Find all cameras at an intersection")
print("  3. Percentage of violations for a specific date")
print("  4. Number of cameras at each intersection")
print("  5. Number of violations at each intersection, given a year")
print("  6. Number of violations by year, given a camera ID")
print("  7. Number of violations by month, given a camera ID and year")
print("  8. Compare the number of red light and speed violations, given a year")
print("  9. Find cameras located on a street")
print("or x to exit the program.")

question = input("Your choice -->  ")
while(question != 'x' and question != 'X'):
    if(question == '1'): 
        command1(dbConn)
        question = input("Your choice -->  ")
    elif(question == '2'):
        command2(dbConn)
        question = input("Your choice -->  ")
    elif(question == '3'):
        command3(dbConn)
        question = input("Your choice -->  ")
    elif(question == '4'):
        command4(dbConn)
        question = input("Your choice -->  ")
    elif(question == '5'):
        command5(dbConn)
        question = input("Your choice -->  ")
    elif(question == '6'):
        command6(dbConn)
        question = input("Your choice -->  ")
    elif(question == '7'):
        command7(dbConn)
        question = input("Your choice -->  ")
    elif(question == '8'):
        command8(dbConn)
        question = input("Your choice -->  ")
    elif(question == '9'):
        command9(dbConn)
        question = input("Your choice -->  ")
    else:
        print("Error, unknown command, try again...")
        question = input("Your choice -->  ")

print("Exiting program.")
#
# done
#
