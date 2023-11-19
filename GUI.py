import tkinter
from tkinter import filedialog
from tkcalendar import Calendar, DateEntry

class GUI:
    def __init__(self) :
        self.CourseList=[]
        pass
    def AuthPage(self):
        '''
        Creates the Login page and returns the username and pasword as a 
        tuple of strings, when login button is pressed
        '''
        self.__Authclose=False
        self.__rt=tkinter.Tk()
        self.__rt.geometry("200x100")
        self.__rt.title("Exam Seating Planner")
        
        username_label=tkinter.Label(
            self.__rt,
            text="Username: ")
        
        password_label=tkinter.Label(self.__rt,
                                     text="Password: ")
        
        username=tkinter.StringVar()
        password=tkinter.StringVar()
        
        username_inp=tkinter.Entry(self.__rt,
                                   textvariable=username)
        
        password_inp=tkinter.Entry(self.__rt,
                                   textvariable=password,
                                   show="*")
        
        login_btn=tkinter.Button(self.__rt,
                                 text="Login",
                                 command=lambda:self.__Login_btn_routine())
            
        
        username_label.grid(row=0,column=0)
        username_inp.grid(row=0,column=1)
        password_label.grid(row=1,column=0)
        password_inp.grid(row=1,column=1)
        login_btn.grid(row=2,column=0,columnspan=2)
        self.__rt.mainloop()
        return(self.__Authclose,username.get(),password.get())
    def __Login_btn_routine(self):
        '''Routine on login button press'''
        self.__rt.destroy()
        self.__Authclose==True
        return
    
    def HomePage(self):
        '''
        This methods renders the Homepage and returns the selected option
        0 for manage database
        1 for Create Seating plan
        '''
        self.__Homesel=-1
        self.__rt=tkinter.Tk()
        self.__rt.title("Exam Seating Planner")
        self.__rt.geometry("240x100")
        Mng_DBMS_bttn=tkinter.Button(
            self.__rt,
            text="Manage Data",
            command=lambda:self.__Mng_DB_btn_routine()
        )
        crt_Stn_bttn=tkinter.Button(
            self.__rt,
            text="Create Seating Plan",
            command=lambda: self.__Crt_stn_btn_routine()
        )
        Mng_DBMS_bttn.grid(row=0,column=0)
        crt_Stn_bttn.grid(row=1,column=0)
        self.__rt.mainloop()
        return self.__Homesel
    def __Mng_DB_btn_routine(self):
        '''Routine on Manage Database button press'''
        print("Manage Database button\n")
        self.__Homesel=0
        self.__rt.destroy()
    
    def __Crt_stn_btn_routine(self):
        '''Routine on Create Seating button press'''
        print("Create Seating Plan button\n")
        self.__Homesel=1
        self.__rt.destroy()
        
    def ManageDBPage(self):
        '''
        This methods renders the Manage DB page and returns the selected option
        0 for Update 
        1 for Clear 
        2 for Back
        '''
        self.__mngdbSel=-1
        self.__fileSel=""
        self.__rt=tkinter.Tk()
        self.__rt.title("Exam Seating Planner")
        self.__rt.geometry("240x100")
        Update_DB_bttn=tkinter.Button(
            self.__rt,
            text="Update Data",
            command=lambda:self.__updt_btn_routine()
        )
        Clr_DB_bttn=tkinter.Button(
            self.__rt,
            text="Clear Data",
            command=lambda: self.__clrdb_btn_routine()
        )
        Back_bttn=tkinter.Button(
            self.__rt,
            text="Back",
            command=lambda: self.__bck_btn_routine()
        )
        Update_DB_bttn.grid(row=0,column=0)
        Clr_DB_bttn.grid(row=1,column=0)
        Back_bttn.grid(row=2,column=0)
        self.__rt.mainloop()
        return (self.__mngdbSel,self.__fileSel)
    def __updt_btn_routine(self):
        filetypes = (
            ('Excel files', '*.xlsx'),
            ('All files', '*.*')
        )
        fileSelect=filedialog.askopenfile(
            title="Open a file",
            initialdir='/',
            filetypes=filetypes
        )
        print(fileSelect.name)
        self.__mngdbSel=0
        self.__fileSel=fileSelect.name
        self.__rt.destroy()
        
    def __clrdb_btn_routine(self):
        self.__mngdbSel=1
        self.__fileSel=""
        self.__rt.destroy()
    def __bck_btn_routine(self):
        self.__mngdbSel=2
        self.__fileSel=""
        print("Returning to Home\n")
        self.__rt.destroy()
    def CreateSeatingPage(self):
        self.__crt=0
        self.__rt=tkinter.Tk()
        self.__rt.title("Exam Seating Planner")
        self.__rt.geometry("200x300")
        self.__csel=[]
        self.__dsel=""
        Course=tkinter.StringVar()
        yscrollbar = tkinter.Scrollbar(self.__rt) 
        yscrollbar.pack(side = "right",
                        fill = "y") 
        
        self.__CourseSel=tkinter.Listbox(self.__rt,
                                  listvariable=Course,
                                  selectmode="multiple",
                                  yscrollcommand=yscrollbar.set)
        
        for i in self.CourseList:
            self.__CourseSel.insert("end",i)
        yscrollbar.config(command=self.__CourseSel.yview)
        Date_lbl=tkinter.Label(self.__rt,text="Choose Date")
        self.__DateSel=DateEntry(self.__rt)
        Course_lbl=tkinter.Label(self.__rt,text="Select Course")
        Crt_btn=tkinter.Button(self.__rt,
                               text="Create Plan",
                               command=lambda: self.CreatePlan())
        
        Date_lbl.pack()
        self.__DateSel.pack()
        Course_lbl.pack()
        self.__CourseSel.pack()
        Crt_btn.pack()
        self.__rt.mainloop()
        return(self.__crt,self.__csel,self.__dsel)
    
    def CreatePlan(self):
        print("Creating Plan from Seating\n")
        self.__dsel=self.__DateSel.get_date()
        for i in self.__CourseSel.curselection():
            self.__csel.append(self.__CourseSel.get(i))
        self.__rt.destroy()
        self.__crt=1
        
# gui=GUI()
# gui.AuthPage()