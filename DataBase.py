import numpy as np
import pandas as pd
import mysql.connector
import re

class DataBase:
    connectionSuccessful = True
    mycursor = None
    mydb  = None
    
    slots = dict()
    roomMap = dict()
    studentData = dict()
    loadingFormula = "INSERT INTO temp VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    roomLoadingFormula = "INSERT INTO roomtemp VALUES (%s,%s,%s,%s)"
        
    def dataInit_1(self):
        # to initialize room and course data from DB
        self.__initializeRooms()
        self.__createTableCourses()
        self.__loadCoursesFromDB()
        
    
    def dataInit_2(self):
        # for checking if student table exists, and creates one otherwise
        if (self.__checkIfTableExists()):
            self.__loadFromDB()
        else:
            self.__createTableStudent()
            
    def databaseConnection(self,hostName="localhost", userName="root", passwordInput="12345", databaseName="tempstudent"):
        self.connectionSuccessful = True
        try:
            self.mydb = mysql.connector.connect(host=hostName, user=userName, passwd=passwordInput, database=databaseName)
        except mysql.connector.errors.DatabaseError as e:
            print("failed :(")
            self.mydb = None
            self.connectionSuccessful = False

        if self.connectionSuccessful:
            self.mycursor = self.mydb.cursor()
        
        return self.connectionSuccessful

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------INITIALIZATION FUNCTIONS----------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __initializeRooms(self):
        self.roomMap["302"] = (10,4,0)
        self.roomMap["303"] = (5,7,0)
        self.roomMap["304"] = (5,7,0)
        self.roomMap["307"] = (10,4,0)
        
    def __createTableCourses(self):
        self.mycursor.execute("CREATE TABLE if not exists courses (coursecode varchar(10),slot varchar(2),PRIMARY KEY(coursecode));")
        #table courses created if it didnt already exist
        self.mycursor.execute("select * from courses")
        res = self.mycursor.fetchall()
        if (res == []):
            # if courses is blank, initialize it with default data
            self.call_initializeCourses()
        else:
            return
        #         self.mycursor.execute("show tables")
        #         res = self.mycursor.fetchall()
        #         res2 = [res[i][0] for i in range(len(res))]
        #         if "courses" in res2:
        #             pass:
        #         else:
        #             self.mycursor.execute("CREATE TABLE courses (coursecode varchar(10),slot varchar(2),PRIMARY KEY(coursecode));")

        
    def call_initializeCourses(self):
        self.__initializeCourses()
        self.__loadCoursesFromDB()
    
    def call_loadCoursesfromDB(self):
        self.__loadCoursesFromDB()
        
    def call_addCourse(self,courseCode,courseSlot):
        self.__addCourse(courseCode,courseSlot)
        self.__loadCoursesFromDB()
        
    def call_deleteCourse(self,courseCode):
        self.__deleteCourse(courseCode)
        self.__loadCoursesFromDB()
        
    def __initializeCourses(self):
        self.mycursor.execute("show tables")
        res = self.mycursor.fetchall()
        for i in range(len(res)):
            if (res[i][0] == "courses"):
                self.mycursor.execute("drop table courses")
                break
        self.mycursor.execute("CREATE TABLE courses (coursecode varchar(10),slot varchar(2),PRIMARY KEY(coursecode));")
        self.slots={}
        # whenever the "courses" table is destroyed, it will be replaced by the below dictionary
        initialCourses = dict()
        initialCourses["A"] = ["HUL-301", "ECL-205"]
        initialCourses["B"] = ["HUL-304", "CSL-210"]
        initialCourses["C"] = ["ECL-320"]
        initialCourses["D"] = ["ECL-303"]
        initialCourses["E"] = ["ECL-307"]
        initialCourses["F"] = ["ECL-308"]
        initialCourses["G"] = ["CSL-202"]
        initialCourses["H"] = [""]
        
        tempTuple = 0
        for key in initialCourses.keys():
            for el in initialCourses[key]:
                if (el == ""):
                    continue
                else:
                    tempTuple = (el,key)
                    self.mycursor.execute("INSERT INTO courses VALUES (%s,%s)",tempTuple)
        self.mydb.commit()
        print("courses loaded into DB")
        
 
    def __loadCoursesFromDB(self):
        self.mycursor.execute("select * from courses")
        res = self.mycursor.fetchall()
        for entry in range(len(res)):
            if res[entry][1] in self.slots:
                self.slots[res[entry][1]].append(res[entry][0])
            else:
                self.slots[res[entry][1]] = [res[entry][0]]
        self.slots = dict(sorted(self.slots.items()))
    
        
    def __addCourse(self, courseCode, courseSlot):
        # attempts to add course to table, but since primary key declared, duplicate courses cant be added
        # in that case, exception is handled and error message is thrown
        try:
            self.mycursor.execute("insert into courses values (%s,%s)",(courseCode.upper(),courseSlot.upper()))
            self.mydb.commit()
        except mysql.connector.IntegrityError as e:
            if e.args[0] == 1062:
                print("duplicate primary key error")
            else:
                print("some other integrity error occurred")
        else:
            print("course added successfully")
                
            
        
        
    def __deleteCourse(self,courseCode):
        # for some reason, deleting a non-existing row in MYSQL does not raise errors, so here the try-except is kinda useless
        try:
            self.mycursor.execute("delete from courses where coursecode=%s",(courseCode.upper(),))
            self.mydb.commit()
        except mysql.connector.errors.OperationalError as e:
            if e.errno == 1062:
                print("specified row not present")
            else:
                print("an error occurred ",e)
                                
        
                                  
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------DATA EXTRACTION FROM SPREADSHEET-------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------

    def call_initializeTable(self,path):
        self.__initializeTable(path)
        self.__loadTable()
        self.__loadFromDB()
        
        
    def __initializeTable(self,path):
        masterDict = dict()
        studentSet = set()
        studentData = dict()
        xls = pd.ExcelFile(path)
        numSheets = len(xls.sheet_names)
        
        tempSlot = ""
        for sheet in range(numSheets):    
            sheetNP = np.array(pd.read_excel(xls,sheet).applymap(str)) #loads individual sheets as dataframes, which are converted to a numpy array
            regexRoll = r'^(BT\d{2}[A-Z]{3}[0-9]{3})$'
            rollStartCoords = (None,None)
            endingRow = None

            # for-else is employed to find the topmost-first occurrence of any roll number using the regular expression
            # expression searches for BT<2-digit-number><3-alphabets><3-digit-number>
            # the sheet array is traversed in a nested fashion, and the coordinates of the very first encounter are returned as a 2-tuple
            # if no match found, (None,None) is returned
            for i in range(len(sheetNP)):
                for j in range(len(sheetNP[0])):
                    if (re.match(regexRoll , sheetNP[i][j]) != None):
                        rollStartCoords = (i,j)
                        break
                    else:
                        continue
                else:
                    continue
                break

            # if roll number not found in the sheet, then skip the sheet
            if (rollStartCoords[0] == None or rollStartCoords[1] == None):
                print("sheet ",sheet+1," skipped")
                continue

                # now we have the starting coords of rollnos, we will find the ending coords
                # column number would be same of the ending coordinates
                # IT IS ASSUMED THAT ALL ROLL NOS ARE CONTINOUSLY ENTERED IN THE SPREADSHEET
                # WHILE TRAVERSING FOR ROLL NOS, ANY DIFFERENT VALUE IS ASSUMED TO MARK THE END OF ROLL NOS
            for i in range(rollStartCoords[0],len(sheetNP)):
                # if, by chance, and I mean I have already explained not to do this, but still, if the last roll number is in the very last row of the dataframe, then this if-block makes sure that we dont have an array-out-of-bounds situation
                if (i == len(sheetNP)-1):
                    endingRow = i
                    break
                if (re.match(regexRoll , sheetNP[i+1][rollStartCoords[1]]) == None):
                    endingRow = i
                    break

            # 2 places above the first roll number occurrence, we have the course code
            courseCode = sheetNP[rollStartCoords[0] - 2][rollStartCoords[1]]

            # masterDict is LOCALLY declared
            masterDict [courseCode.upper()] = sheetNP[rollStartCoords[0] : endingRow , rollStartCoords[1] ].tolist()
        
        for key in masterDict:
            studentSet.update(masterDict[key]) #creates a list of all unique roll numbers in the spreadsheet

        # converting masterDict to a student-wise dictionary
        for student in studentSet:
            temp = ["None","None","None","None","None","None","None","None"]
            for key in masterDict.keys(): # traverses through all course codes
                for slot in self.slots.keys(): # traverses through slots A to H
                    if key in self.slots[slot]:
                        tempSlot = ord(slot) - 65 #ord() gives the unicode of character; this line returns 0 for A, 1 for B and so on
                        break
                #now we have the slot for the particular course code
                if student in masterDict[key]:
                    temp[tempSlot] = key
            studentData[student] = temp
            
        # studentData is a variable in the local scope, while self.studentData is a class attribute
        #sorting the dictionary key-wise
        studentData = dict(sorted(studentData.items()))
        self.studentData = studentData
                    
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------DATA HANDLING FUNCTIONS - MYSQL----------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------    
        
    def call_dropTable(self):
        self.__dropTable()
        self.__createTableStudent()
        self.__loadFromDB()
        
             
    def __checkIfTableExists(self):
        self.mycursor.execute("show tables")
        res = self.mycursor.fetchall()
        for i in range(len(res)):
            if (res[i][0] == "temp"):
                return True
        return False

    def checkIfTableEmpty(self):
        if (not self.mydb.query("""SELECT * from temp limit 1""")):
            return True
        else:
            return False
        
    
    def __createTableStudent(self):
        if (not self.__checkIfTableExists()):
            self.mycursor.execute("CREATE TABLE temp (roll varchar(12),a varchar(7),b varchar(7),c varchar(7),d varchar(7),e varchar(7),f varchar(7),g varchar(7),h varchar(7),PRIMARY KEY(roll));")
            self.mydb.commit()
            print("table created")
        else:
            print("table already exists")
        
        
    def __loadTable(self):
        # THIS IS ALSO, SURPRISINGLY, A DESTRUCTIVE FUNCTION
        # PRIMARY KEY NOT USED IN DATABASE, AND THEREFORE NO TRY-EXCEPT FOR THE SAME
        # CALLING THIS FUNCTION REPEATEDLY REPLICATES DATA IN THE SAME TABLE, THEREBY POLLUTING EVERYTHING
        self.__createTableStudent() #creates table if it doesnt exist, else lets it be
        for key in self.studentData.keys():
            tempTuple = (key,)  # comma ensures that () are treated as tuple markers and not to change order of execution

            for course in self.studentData[key]:
                tempTuple = tempTuple + (course,)

            self.mycursor.execute(self.loadingFormula, tempTuple)
        self.mydb.commit()
        print("data loaded into database")
        
        
    def __dropTable(self):
        # THIS IS A DESTRUCTIVE FUNCTION, USE WITH DISCRETION
        self.mycursor.execute("drop table temp");
        
        
    #below function extracts data from already existing table in DB and manipulates the studentData dict attribute
    def __loadFromDB(self):
        # assuming table exists and is populated
        self.mycursor.execute("select * from temp")
        self.studentData={}
        res = self.mycursor.fetchall()
        for entry in range(len(res)):
            roll = res[entry][0]
            subA = res[entry][1]
            subB = res[entry][2]
            subC = res[entry][3]
            subD = res[entry][4]
            subE = res[entry][5]
            subF = res[entry][6]
            subG = res[entry][7]
            subH = res[entry][8]
            self.studentData[roll] = [subA,subB,subC,subD,subE,subF,subG,subH]
        
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~ONLY FOR TESTING PURPOSE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # deletes already existing table by the name "temp" and creates a new one in its place
    # followed by functions initializeTable and loadTable
    def createTableStudent(self):
        #for testing purposes, if "temp" table already exists, it is dropped and a fresh is created
        #a fresh one is created if "temp" doesn't exist
        self.mycursor.execute("show tables")
        flag = 0;
        res = self.mycursor.fetchall();
        for i in range(len(res)):
            if (res[i][0] == "temp"):
                flag = 1
                break
        if (flag == 1):
            self.mycursor.execute("drop table temp")

        self.mycursor.execute(
            "CREATE TABLE temp (roll varchar(12),a varchar(7),b varchar(7),c varchar(7),d varchar(7),e varchar(7),f varchar(7),g varchar(7),h varchar(7),PRIMARY KEY(roll));")
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------ROOM DATA MANIPULATION-------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------ 
# room data is stored locally
#     def call_initializeRooms(self):
#         tempRoomMap = self.__initializeRooms()
#         return tempRoomMap
    
#     def call_updateRoom(self,roomData):
#         pass
    
#     def __initializeRooms(self):
#         roomMap = dict()
#         # ------roomMap-------
#         return roomMap

#     def __updateRoom(roomMap, roomData):
#         # roomData is expected to be a 3-tuple specifying the new things
#         pass

#     def __addRoom(roomMap, roomData):
#         pass

#     def __getRoomSize(roomMap,roomNo):
#         # roomNo is expected to be a STRING
#         return roomMap[roomNo]

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------FUNCTIONS TO RETURN DATA TO FRONT-END-----------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------  
    def findRoomSize(self,roomNo):
        return self.roomMap[roomNo.upper()]
        
    
    def findCourseSlot(self,course):
        # returns "" if  course not in table
        #returns course slot for the entered course code
        courseCode = ""
        for key in self.slots.keys():
            if course in self.slots[key]:
                courseCode = key
        return courseCode
            
            
    def studentsEnrolledInCourse(self,course):
        # returns a list of all students enrolled in a given course
        studentList = []
        for key in self.studentData.keys():
            if course in self.studentData[key]:
                studentList.append(key)
        return studentList
               
    def getStudentsOfBatch(self,batchString):
        # batch string of the form BT21AIC only
        tempDict={}
        check = batchString.upper()
        if (self.studentData):
            for roll in self.studentData.keys():
                if (roll[0:7] == check):
                    tempDict[roll] = self.studentData[roll]
        return tempDict
                    