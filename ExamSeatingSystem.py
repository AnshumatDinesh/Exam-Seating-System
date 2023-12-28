import GUI
import DataBase
import Seater
from tkinter import filedialog
global temproom
temproom={
        "101" : [6,6,6,6,6,6,6,6,6,6],
        "102" : [6,6,6,6,6,6,6,6,6,6],
        "201" : [8,8,8,8,8,8,8,8],
        "202" : [10,10,10,10,10,10,10,10],
        "204" : [8,8,8,8,8,8,8,8,8,8],
        "301" : [7,7,7,7,7,7,7,7,7,7,7],
        "302" : [10,10,10,10,10,10,12,12],
        "303" : [6,5,5,5,5,5,5,6],
        "304" : [6,6,5,5,5,5,5,5,5,5,5,5,6,6],
        "305" : [6,6,6,6,5,5,5,5,5,5,5,5,6,6],
        "306" : [8,8,8,8,8,8,8,8,8,8],
        "307" : [10,10,10,10,10,10,12,12],
        "seminar" : [9,9,9,9,9,9,9,9,9,9,9],
        "VLSI" : [6,6,6,6,6,6,6]
        }
class ExamSeatingSystem:
    def __init__(self) -> None:
        self.frontend=GUI.GUI()
        self.backend=DataBase.DataBase()
        self.seater=Seater.Seater()
        self.courseList=[]
        self.studentDict={}
    def __dict2list(self,slot_dict:dict)->list:
        res=[]
        for i in slot_dict.keys():
            for j in slot_dict[i]:
                res.append(j);  
        return res
    def Login(self):
        loginret=self.frontend.LoginPage()
        if(loginret["Close"]):
            return -1
        if(self.backend.databaseConnection(userName=loginret["Username"],passwordInput=loginret["Password"])):
            self.backend.dataInit_1()
            self.backend.dataInit_2()
            self.courseList=self.__dict2list(self.backend.slots)
            return 1
        self.frontend.alert("Incorrect Username or Password")
        return 0
    def HomePage(self):
        homeret=self.frontend.HomePage()
        if(homeret["Close"]):
            return -1
        return homeret["OptionSelect"]
    def DBmanage(self):
        dbret=self.frontend.DataManagementPage()
        if(dbret["Close"]):
            return -1
        if(dbret["Option"]==1):
            self.backend.call_dropTable()
            self.backend.call_initializeTable(dbret["filename"])
            print(self.backend.studentData)
    def plan(self):
        spret=self.frontend.SeatingPlanPage(self.courseList)
        if(spret["Close"]):
            return -1
        if(len(spret["Courses"])==0):
            self.frontend.alert("No Courses were Selected")
            return -1
        studata={}
        for i in spret["Courses"]:
            studata[i]=self.backend.studentsEnrolledInCourse(i)
        self.seater.setroomDict(temproom)
        self.seater.setcourseList(spret["Courses"])
        self.seater.setDate(spret["Date"])
        self.seater.setInstitute(spret["Institute"])
        self.seater.setDepartment(spret["Department"])
        self.seater.setStudentDict(studata)
        self.seater.new_arrange()
        self.seater.getSpreadsheet()
        # try:
        #     self.seater.arrange()
        #     self.seater.getSpreadsheet()
        # except:
        #     self.frontend.alert("An error occured while creating seating plan")
E=ExamSeatingSystem()
if(E.Login()==1):
    h=E.HomePage()
    if(h==0):
        db=E.DBmanage()
    elif(h==1):
        E.plan()
        