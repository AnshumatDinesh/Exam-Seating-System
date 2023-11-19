'''SubjectList: List of all the exams today;
    self.student_dict:Dictionary of coursecode and exams
                "Coursecode":[List of students enrolled];
    RoomList:List of rooms available with 2x8x5 capacity;
'''
from GUI import GUI
from DataBase import DataBase
import xlwt 
from xlwt import Workbook 
class Seater:
    def __init__(self) -> None:
        self.g=None
        self.g=None
        self.student_dict={}
        self.SeatingMatrix={}
    def dict2list(self,slot_dict:dict)->list:
        res=[]
        for i in slot_dict.keys():
            for j in slot_dict[i]:
                res.append(j);  
        return res
    def Seating(self,CourseSel:list,DateSel:list)->dict:
        for i in CourseSel:
            self.student_dict[i]=self.d.studentsEnrolledInCourse(i)
            print(self.d.studentsEnrolledInCourse(i))
        return self.student_dict
    def write2xl(self)->None:
        wb=Workbook()
        for i in self.SeatingMatrix.keys():
            roomtemp=wb.add_sheet(i)
            for j in range(0,len(self.SeatingMatrix[i])):
                for k in range(0,len(self.SeatingMatrix[i][j])):
                    roomtemp.write(k,j,self.SeatingMatrix[i][j][k])
        wb.save("test.xls")
    def crt_Seating(self,SubjectList,Roomdict):
        for i in self.d.roomMap.keys():
            row_iterator=1
            sub_iterator=0
            self.SeatingMatrix[i]=[]
            while(len(self.student_dict[SubjectList[sub_iterator]])!=0 and len(self.student_dict[SubjectList[sub_iterator+1]])!=0 and row_iterator<(Roomdict[i][1])):
                self.SeatingMatrix[i].append(self.student_dict[SubjectList[sub_iterator]][:Roomdict[i][0]])
                self.SeatingMatrix[i].append(self.student_dict[SubjectList[sub_iterator+1]][:Roomdict[i][0]])
                del self.student_dict[SubjectList[sub_iterator]][:Roomdict[i][0]]
                del self.student_dict[SubjectList[sub_iterator+1]][:Roomdict[i][0]]
                row_iterator+=2
            if(Roomdict[i][0]%2==1):
                self.SeatingMatrix[i].append(self.student_dict[SubjectList[sub_iterator]][:Roomdict[i][0]])
                del self.student_dict[SubjectList[sub_iterator]][:Roomdict[i][0]]
            if(Roomdict[i][2]!=0):
                if(Roomdict[i][0]%2==1):
                    self.SeatingMatrix[i].append(self.student_dict[SubjectList[sub_iterator]][:Roomdict[i][2]])
                    del self.student_dict[SubjectList[sub_iterator]][:Roomdict[i][2]]
                else:
                    self.SeatingMatrix[i].append(self.student_dict[SubjectList[sub_iterator+1]][:Roomdict[i][2]])
                    del self.student_dict[SubjectList[sub_iterator+1]][:Roomdict[i][2]]
            if(len(self.student_dict[SubjectList[sub_iterator]])==0 and len(self.student_dict[SubjectList[sub_iterator+1]])==0 ):
                sub_iterator+=2
        for i in self.SeatingMatrix.keys():
            print(i)
            for j in self.SeatingMatrix[i]:
                print(j,end='\n')
        self.write2xl()
    def main(self):
        self.g=GUI()
        self.d=DataBase()
        # # d=DataBase()
        #Loop for Login
        login_runner=True
        Home_runner=False
        while(login_runner):
            (login_runner,username,password)=self.g.AuthPage()
            self.d.databaseConnection(userName=username,passwordInput=password)
            if(not self.d.connectionSuccessful):
                print("Login Failed")
            else:
                login_runner=False
                Home_runner=True
                print("Login Successfull!")
        # Rendering Homepage

        self.d.dataInit_1()
        self.d.dataInit_2()
        print(self.d.slots)
        self.g.CourseList=self.dict2list(self.d.slots)
        Coursesel=None
        Datesel=None
        pathToExcel = r"C:\Users\anshu\Exam-Seating-System\tempStudentData.xlsx"
        stuData = self.d.studentData
        while(Home_runner):
            hpsel=self.g.HomePage()
            if(hpsel==1):
                (crt_sel,Coursesel,Datesel)=self.g.CreateSeatingPage()
                if(crt_sel):
                    print(Coursesel,Datesel)
                    self.stu_dict=self.Seating(Coursesel,Datesel)
                    self.crt_Seating(Coursesel,self.d.roomMap)
                else:
                    break
            elif(hpsel==0):
                (mng_sel,filepath)=self.g.ManageDBPage()
                if(mng_sel==0):
                    self.d.call_dropTable()
                    self.d.call_initializeTable(filepath)
                elif(mng_sel==1):
                    self.d.call_dropTable()
                elif(mng_sel==2):
                    continue
                else:
                    break
            else:
                break
# SubjectList=[
#     "ECL-101",
#     "ECL-201",
#     "ECL-301",
# ]
# self.student_dict={
#     "ECL-101":["BT22ECE001","BT22ECE002","BT22ECE003","BT22ECE004","BT22ECE005","BT22ECE006","BT22ECE007","BT22ECE008","BT22ECE009","BT22ECE010","BT22ECE011","BT22ECE012"],
#     "ECL-102":["BT22ECE001","BT22ECE002","BT22ECE003","BT22ECE004","BT22ECE005","BT22ECE006","BT22ECE007","BT22ECE008","BT22ECE009","BT22ECE010","BT22ECE011","BT22ECE012"],
#     "ECL-103":["BT22ECE001","BT22ECE002","BT22ECE003","BT22ECE004","BT22ECE005","BT22ECE006","BT22ECE007","BT22ECE008","BT22ECE009","BT22ECE010","BT22ECE011","BT22ECE012"],
#     "ECL-104":["BT22ECE001","BT22ECE002","BT22ECE003","BT22ECE004","BT22ECE005","BT22ECE006","BT22ECE007","BT22ECE008","BT22ECE009","BT22ECE010","BT22ECE011","BT22ECE012"],
#     "ECL-201":["BT21ECE001","BT21ECE002","BT21ECE003","BT21ECE004","BT21ECE005","BT21ECE006","BT21ECE007","BT21ECE008","BT21ECE009","BT21ECE010","BT21ECE011","BT21ECE012"],
#     "ECL-202":["BT21ECE001","BT21ECE002","BT21ECE003","BT21ECE004","BT21ECE005","BT21ECE006","BT21ECE007","BT21ECE008","BT21ECE009","BT21ECE010","BT21ECE011","BT21ECE012"],
#     "ECL-203":["BT21ECE001","BT21ECE002","BT21ECE003","BT21ECE004","BT21ECE005","BT21ECE006","BT21ECE007","BT21ECE008","BT21ECE009","BT21ECE010","BT21ECE011","BT21ECE012"],
#     "ECL-301":["BT20ECE001","BT20ECE002","BT20ECE003","BT20ECE004","BT20ECE005","BT20ECE006","BT20ECE007","BT20ECE008","BT20ECE009","BT20ECE010","BT20ECE011","BT20ECE012"],
#     "ECL-302":["BT20ECE001","BT20ECE002","BT20ECE003","BT20ECE004","BT20ECE005","BT20ECE006","BT20ECE007","BT20ECE008","BT20ECE009","BT20ECE010","BT20ECE011","BT20ECE012"],
#     "ECL-303":["BT20ECE001","BT20ECE002","BT20ECE003","BT20ECE004","BT20ECE005","BT20ECE006","BT20ECE007","BT20ECE008","BT20ECE009","BT20ECE010","BT20ECE011","BT20ECE012"],
# }
# RoomList=[
#     "101",
#     "102",
#     "103",
#     "104"
# ]

        
# # seater(SubjectList,self.student_dict,RoomList)
# d=DataBase(userName="root",passwordInput="Anshu2004")
# print(d.mydb)
# d.initializeRooms()
# d.initializeCourses()
# d=DataBase()
s=Seater()
s.main()