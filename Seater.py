import xlsxwriter
class Seater:
    def __init__(self) -> None:
        self.roomDict={}
        self.courseList=[]
        self.studentDict={}
        self.seatingMatrix={}
        self.Institute=""
        self.Department=""
        self.date=""
        return
    def setInstitute(self,institute):
        self.Institute=institute
        return
    def setDepartment(self,dep):
        self.Department=dep
        return
    def setroomDict(self,roomDict)->None:
        self.roomDict=roomDict
        return
    def setcourseList(self,selectedCourses)->None:
        self.courseList=selectedCourses
        return
    def setStudentDict(self,studentDict)->None:
        for i in self.courseList:
            self.studentDict[i]=studentDict[i]
        return
    def setDate(self,date):
        self.date=date
        return
    def arrange(self)->dict:
        it_course_odd=0
        it_course_even=1
        skip_odd=False
        skip_even=False
        temp_stu=self.studentDict
        for i in self.roomDict.keys():
            self.seatingMatrix[i]={
                "Courses":[],
                "Seating":[]
            }
            j=0
            for  j in range(0,len(self.roomDict[i]),2):
                rowOdd=[]
                if(not skip_odd):
                    if(it_course_odd not in self.seatingMatrix[i]["Courses"]):
                        self.seatingMatrix[i]["Courses"].append(it_course_odd)
                    if(len(temp_stu[self.courseList[it_course_odd]])>=self.roomDict[i][j]):
                        rowOdd.append(temp_stu[self.courseList[it_course_odd]][:self.roomDict[i][j]])
                        del temp_stu[self.courseList[it_course_odd]][:self.roomDict[i][j]]
                    else:
                        rowOdd.append(temp_stu[self.courseList[it_course_odd]][:])
                        del temp_stu[self.courseList[it_course_odd]][:]
                    self.seatingMatrix[i]["Seating"].append(rowOdd)
                    if(len(temp_stu[self.courseList[it_course_odd]])==0):
                        it_course_odd+=2
                    if(it_course_odd>len(self.courseList)-1):
                        skip_odd=True
                else:
                    for k in range(0,self.roomDict[i][j]):
                        rowOdd.append(" ")
                    self.seatingMatrix[i]["Seating"].append(rowOdd)    
                rowEven=[]
                if(not skip_even):
                    if(it_course_even not in self.seatingMatrix[i]["Courses"]):
                        self.seatingMatrix[i]["Courses"].append(it_course_even)
                    if(len(temp_stu[self.courseList[it_course_even]])>=self.roomDict[i][j+1]):
                        rowEven.append(temp_stu[self.courseList[it_course_even]][:self.roomDict[i][j+1]])
                        del temp_stu[self.courseList[it_course_even]][:self.roomDict[i][j+1]]
                    else:
                        rowEven.append(temp_stu[self.courseList[it_course_even]][:])
                        del temp_stu[self.courseList[it_course_even]][:]
                    self.seatingMatrix[i]["Seating"].append(rowEven)              
                    if(len(temp_stu[self.courseList[it_course_even]])==0):
                        it_course_even+=2
                    if(it_course_even>len(self.courseList)-1):
                        skip_even=True
                else:
                    for k in range(0,self.roomDict[i][j+1]):
                        rowEven.append(" ")
                    self.seatingMatrix[i]["Seating"].append(rowEven)
                    
            if(len(self.roomDict[i])%2!=0 and not skip_odd):
                rowOdd=[]
                if(temp_stu[self.courseList[it_course_odd]]>=self.roomDict[i][j]):
                    rowOdd.append(temp_stu[self.courseList[it_course_odd]][:self.roomDict[i][j]])
                    del temp_stu[self.courseList[it_course_odd]][:self.roomDict[i][j]]
                else:
                    rowOdd.append(temp_stu[self.courseList[it_course_odd]])
                    del temp_stu[self.courseList[it_course_odd]][:]
                self.seatingMatrix[i]["Seating"].append(rowOdd)
        return self.seatingMatrix
    def getSpreadsheet(self):
        wb=xlsxwriter.Workbook(self.Institute+"_"+self.Department+self.date.replace("/","_")+"test.xlsx")
        for i in self.seatingMatrix.keys():
            roomsheet=wb.add_worksheet(i)
            head1format=wb.add_format({"bold":True,"align": "center","valign": "vcenter","top":True,"right":True,"left":True})
            head2format=wb.add_format({"bold":True,"align": "center","valign": "vcenter","right":True,"left":True})
            head3format=wb.add_format({"bold":True,"align": "center","valign": "vcenter","bottom":True,"right":True,"left":True})
            roomsheet.merge_range(1,1,1,len(self.seatingMatrix[i]["Seating"]),self.Institute,head1format)
            roomsheet.merge_range(2,1,2,len(self.seatingMatrix[i]["Seating"]),self.Department,head2format)
            roomsheet.merge_range(3,1,3,len(self.seatingMatrix[i]["Seating"]),"Enter Name of Exam",head2format)
            roomsheet.merge_range(4,1,4,len(self.seatingMatrix[i]["Seating"]),self.date,head3format)
            k=0
            j=0
            for j in range(0,len(self.seatingMatrix[i]["Seating"])):
                for k in range(0,len(self.seatingMatrix[i]["Seating"][j])):
                    roomsheet.write(k+6,j+1,self.seatingMatrix[i]["Seating"][j][k])
            k+=2
            roomsheet.write(k+6,len(self.seatingMatrix[i]["Seating"]),"Courses",head1format)
            
            for j in self.seatingMatrix[i]["Courses"]:
                k+=1
                
                roomsheet.write(k+6,len(self.seatingMatrix[i]["Seating"]),self.courseList[j],head2format)
            roomsheet.autofit()
        wb.close()
    def new_arrange(self):
        it_c_o=0
        it_c_e=1
        temp_stu=self.studentDict
        room1=[6,6,6,6,6,6]
        self.seatingMatrix={}
        for j in self.roomDict.keys():
            self.seatingMatrix[j]={
                "Courses":[],
                "Seating":[]
            }
            for i in range(0,len(self.roomDict[j])):
                if(i%2==0):
                    if(it_c_o>=len(self.courseList)):
                        self.seatingMatrix[j]["Seating"].append([])
                    else:
                        if(it_c_o not in self.seatingMatrix[j]["Courses"]):
                            self.seatingMatrix[j]["Courses"].append(it_c_o)
                        if(len(temp_stu[self.courseList[it_c_o]])>self.roomDict[j][i]):
                            self.seatingMatrix[j]["Seating"].append(temp_stu[self.courseList[it_c_o]][0:self.roomDict[j][i]])
                            del temp_stu[self.courseList[it_c_o]][0:self.roomDict[j][i]]
                            if(len(temp_stu[self.courseList[it_c_o]])==0):
                                it_c_o+=2
                        else:
                            self.seatingMatrix[j]["Seating"].append(temp_stu[self.courseList[it_c_o]][:])
                            del temp_stu[self.courseList[it_c_o]][:]
                            it_c_o+=2
                else:
                    if(it_c_e>=len(self.courseList)):
                        self.seatingMatrix[j]["Seating"].append([])
                    else:
                        if(it_c_e not in self.seatingMatrix[j]["Courses"]):
                            self.seatingMatrix[j]["Courses"].append(it_c_e)
                        if(len(temp_stu[self.courseList[it_c_e]])>self.roomDict[j][i]):
                            self.seatingMatrix[j]["Seating"].append(temp_stu[self.courseList[it_c_e]][0:self.roomDict[j][i]])
                            del temp_stu[self.courseList[it_c_e]][0:self.roomDict[j][i]]
                            if(len(temp_stu[self.courseList[it_c_e]])==0):
                                it_c_e+=2
                        else:
                            self.seatingMatrix[j]["Seating"].append(temp_stu[self.courseList[it_c_e]][:])
                            del temp_stu[self.courseList[it_c_e]][:]
                            it_c_e+=2
        return self.seatingMatrix
            
# s=Seater()
# s.setcourseList(["ECL-301","ECL-302"])
# s.setroomDict({
#     "101":[2,3,2,4],
#     "102":[2,3,4,2],
#     "104":[5,4,3,5],
#     "105":[6,7,5,8]
# })
# s.setStudentDict({
#     "ECL-301":["BT21ECE001","BT21ECE002","BT21ECE003","BT21ECE004","BT21ECE005","BT21ECE006","BT21ECE007","BT21ECE008","BT21ECE009"],
#     "ECL-302":["BT21CSE001","BT21CSE002","BT21CSE003","BT21CSE004","BT21CSE005","BT21CSE006","BT21CSE007","BT21CSE008","BT21CSE009"],
#     "ECL-303":["BT21ECE001","BT21ECE002","BT211ECE003","BT21ECE004","BT21ECE005","BT21ECE006","BT211ECE007","BT21ECE008","BT21ECE009"],
#     "ECL-304":["BT21ECE001","BT21ECE002","BT211ECE003","BT21ECE004","BT21ECE005","BT21ECE006","BT211ECE007","BT21ECE008","BT21ECE009"]
# })
# print(s.new_arrange())
# s.setDate("12/12/23")
# print(s.arrange())
# s.getSpreadsheet()