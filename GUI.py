import tkinter
from tkinter import filedialog,messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
class GUI:
    def __init__(self):
        pass
    def LoginPage(self):
        '''
            New log in page
        '''
        self.__rt = tkinter.Tk()
        self.__rt.geometry("400x300")
        self.__rt.config(background="#ADD8E6")
        self.__rt.title("Exam Seating System")
        self.__LoginPageReturn={
            "Close":True,
            "Username":tkinter.StringVar(),
            "Password":tkinter.StringVar()
        }
        #Heading 
        heading_style = {
            "text": "Exam Seating System",
            "font": ("Arial", 24, "bold"),
            "bg": "#ADD8E6",
            "fg": "#333333"
            }

        heading_label = tkinter.Label(self.__rt, **heading_style)
        heading_label.grid(row=0, column=0, columnspan=2, padx=20, pady=50, sticky="nsew")
        label_style = {
            "font": ("Arial", 12),
            "bg": "#ADD8E6",
            "fg": "#333333"
        }

        entry_style = {
            "font": ("Arial", 12),
            "bg": "white",
            "fg": "black",
            "relief": "flat"
        }

        # Username Label and Entry
        username_label = tkinter.Label(self.__rt, text="Username", **label_style)
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        username_inp = tkinter.Entry(self.__rt, textvariable=self.__LoginPageReturn["Username"], **entry_style)
        username_inp.grid(row=1, column=1, padx=10, pady=5)

        # Password Label and Entry
        password_label = tkinter.Label(self.__rt, text="Password", **label_style)
        password_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        password_inp = tkinter.Entry(self.__rt, textvariable=self.__LoginPageReturn["Password"], show="*", **entry_style)
        password_inp.grid(row=2, column=1, padx=10, pady=5)

        # Login Button
        login_btn_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#88a8b3",
            "fg": "white",
            "relief": "flat",
            "activebackground": "#6c8793",
            "activeforeground": "white"
        }

        login_btn = tkinter.Button(self.__rt, text="Login",command=lambda:self.__LoginButton(), **login_btn_style)
        login_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.__rt.mainloop()
        return self.__LoginPageReturn
    def __LoginButton(self):
        self.__rt.destroy()
        self.__LoginPageReturn["Close"]=False
        self.__LoginPageReturn["Username"]=self.__LoginPageReturn["Username"].get()
        self.__LoginPageReturn["Password"]=self.__LoginPageReturn["Password"].get()
        return
    def DataManagementPage(self):
        '''
            New Data managment page
        '''
        self.__dataret={
            "Close":True,
            "Option":0,
            "filename":""
        }
        button_style = {
            "bg": "#5ca6bf",
            "fg": "white",
            "font": ("Helvetica", 12),
            "relief": "flat",
            "bd": 0,
            "highlightbackground": "#88a8b3",
            "highlightcolor": "#88a8b3",
            "activebackground": "#6c8793",
            "activeforeground": "white",
        }
        self.__rt = tkinter.Tk()
        self.__rt.geometry("400x300")
        self.__rt.config(background="#ADD8E6")
        self.__rt.title("Exam Seating System")
        labels = [
            tkinter.Label(self.__rt, text="Students", font=(
                "Arial", 16), background="#ADD8E6"),
            tkinter.Label(self.__rt, text="Rooms", font=(
                "Arial", 16), background="#ADD8E6")
        ]
        stu_btn = [tkinter.Button(self.__rt, text="View", **button_style,command=lambda:self.__DataManagementPageRetValue(0))]
        stu_btn.append(tkinter.Button(self.__rt, text="Edit", **button_style,command=lambda:self.__DataManagementPageRetValue(1)))
        stu_btn.append(tkinter.Button(self.__rt, text="Delete", **button_style,command=lambda:self.__DataManagementPageRetValue(2)))
        
        rms_btn = [tkinter.Button(self.__rt, text="View", **button_style,command=lambda:self.__DataManagementPageRetValue(3))]
        rms_btn.append(tkinter.Button(self.__rt, text="Edit", **button_style,command=lambda:self.__DataManagementPageRetValue(4)))
        rms_btn.append(tkinter.Button(self.__rt, text="Delete", **button_style,command=lambda:self.__DataManagementPageRetValue(5)))

        for i, label in enumerate(labels):
            label.grid(row=i*2, column=0, columnspan=5, sticky="nsew")

        for i, btn in enumerate(stu_btn):
            btn.grid(row=1, column=i+2, sticky="nsew", padx=5, pady=5)


        for i, btn in enumerate(rms_btn):
            btn.grid(row=3, column=i+2, sticky="nsew", padx=5, pady=5)

        self.__rt.grid_rowconfigure(4, weight=1)
        self.__rt.grid_columnconfigure((0, 1, 4), weight=1)

        for i in range(5):
            self.__rt.grid_rowconfigure(i, weight=1)

        for i in range(5):
            self.__rt.grid_columnconfigure(i, weight=1)

        self.__rt.mainloop()
        return self.__dataret
    def __DataManagementPageRetValue(self,selected:int):
        self.__dataret["Close"]=False
        self.__dataret["Option"]=selected
        if(selected==1 or selected==4):
            self.__dataret["filename"]=self.getfile()
        self.__rt.destroy()
        return
    def getfile(self):
        filetypes = (
            ('Excel files', '*.xlsx'),
            ('All files', '*.*')
        )
        fileSelect = filedialog.askopenfile(
            title="Open a file",
            initialdir='/',
            filetypes=filetypes
        )
        return fileSelect.name
    def HomePage(self):
        self.__rt = tkinter.Tk()
        self.__rt.geometry("500x300")
        self.__rt.config(background="#ADD8E6")
        self.__rt.title("Exam Seating System")
        self.__HomePageReturn = {
            "Close": True,
            "OptionSelect": -1,
        }

        # Heading Label Style
        heading_style = {
            "text": "Exam Seating System",
            "font": ("Arial", 24, "bold"),
            "bg": "#ADD8E6",
            "fg": "#333333"
        }

        heading_label = tkinter.Label(self.__rt, **heading_style)
        heading_label.grid(row=0, column=0, columnspan=2, pady=50)  # Center the heading label

        # Button Style
        button_style = {
            "font": ("Arial", 14),
            "bg": "#88a8b3",
            "fg": "white",
            "relief": "flat",
            "activebackground": "#6c8793",
            "activeforeground": "white",
            "width": 20,
            "height": 2
        }

        # Button: Manage Database
        manage_db_btn = tkinter.Button(self.__rt, text="Manage Database",command=lambda:self.__MngDbButton(), **button_style)
        manage_db_btn.grid(row=1, column=0, padx=10, pady=20)

        # Button: Create Seating Plan
        create_plan_btn = tkinter.Button(self.__rt, text="Create Seating Plan",command=lambda:self.__CrtSpButton(), **button_style)
        create_plan_btn.grid(row=1, column=1, padx=10, pady=20)

        self.__rt.mainloop() 
        return self.__HomePageReturn
    def __MngDbButton(self):
        self.__rt.destroy()
        self.__HomePageReturn["Close"]=False
        self.__HomePageReturn["OptionSelect"]=0
        return
    def __CrtSpButton(self):
        self.__rt.destroy()
        self.__HomePageReturn["Close"]=False
        self.__HomePageReturn["OptionSelect"]=1
        return
    
    def SeatingPlanPage(self,Courselist):
        self.__rt = tkinter.Tk()
        self.__rt.geometry("600x600")
        self.__rt.config(background="#ADD8E6")
        self.__rt.title("Seating Plan")
        
        self.__SeatingPageReturn={
            "Close":True,
            "Institute":"",
            "Department":"",
            "Courses":[],
            "Date":""
        }
        self.__institute_name = tkinter.StringVar()
        self.__department_name = tkinter.StringVar()
        self.__selected_courses = tkinter.StringVar()
        self.__selected_date = tkinter.StringVar()

        # Label and Entry Style
        label_entry_style = {
            "font": ("Arial", 12),
            "bg": "#ADD8E6",
            "fg": "#333333"
        }

        # Dropdown Style
        dropdown_style = {
            "font": ("Arial", 12),
            "width": 25
        }

        # Label and Entry: Institute Name
        institute_label = tkinter.Label(self.__rt, text="Institute Name:", **label_entry_style)
        institute_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        institute_entry = tkinter.Entry(self.__rt, textvariable=self.__institute_name, **label_entry_style)
        institute_entry.grid(row=0, column=1, padx=10, pady=10)

        # Label and Entry: Department Name
        department_label = tkinter.Label(self.__rt, text="Department Name:", **label_entry_style)
        department_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        department_entry = tkinter.Entry(self.__rt, textvariable=self.__department_name, **label_entry_style)
        department_entry.grid(row=1, column=1, padx=10, pady=10)

        # Label and Dropdown: Courses
        courses_label = tkinter.Label(self.__rt, text="Select Courses:", **label_entry_style)
        courses_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

         
        self.__courses_listbox = tkinter.Listbox(self.__rt, selectmode=tkinter.MULTIPLE, **label_entry_style)
        for course in Courselist:
            self.__courses_listbox.insert(tkinter.END, course)
        self.__courses_listbox.grid(row=2, column=1, padx=10, pady=10)
        # self.__courses_listbox.pack()
        # Label and Calendar: Date
        date_label = tkinter.Label(self.__rt, text="Select Date:", **label_entry_style)
        date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.__cal = Calendar(self.__rt, selectmode="day", year=2023, month=1, day=1,
                              date_pattern="yyyy-mm-dd")
        self.__cal.grid(row=3, column=1, padx=10, pady=10)

        # Create Plan Button
        create_plan_btn_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#88a8b3",
            "fg": "white",
            "relief": "flat",
            "activebackground": "#6c8793",
            "activeforeground": "white",
            "width": 20,
            "height": 2,
            "command": self.create_plan
        }

        create_plan_btn = tkinter.Button(self.__rt, text="Create Plan", **create_plan_btn_style)
        create_plan_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        self.__rt.mainloop()
        return self.__SeatingPageReturn
    def create_plan(self):
        
        # Retrieve input values and perform plan creation logic
        institute_name = self.__institute_name.get()
        department_name = self.__department_name.get()
        selected_courses=[]
        for i in self.__courses_listbox.curselection():
            selected_courses.append(self.__courses_listbox.get(i))
        selected_date = self.__cal.get_date()
        
        self.__SeatingPageReturn["Close"]=False
        self.__SeatingPageReturn["Institute"]=institute_name
        self.__SeatingPageReturn["Department"]=department_name
        self.__SeatingPageReturn["Courses"]=selected_courses
        self.__SeatingPageReturn["Date"]=selected_date
        self.__rt.destroy()
        # Placeholder logic (Replace this with actual plan creation)
        messagebox.showinfo("Creting Plan for",
                            f"Plan created for:\nInstitute: {institute_name}\nDepartment: {department_name}\n"
                            f"Courses: {selected_courses}\nDate: {selected_date}")

    def infobox(self,mssg):
        messagebox.showinfo(mssg)
        return
    def alert(self,error):
        messagebox.showerror(title="ERROR",message=error)
        return

# gui = GUI()
# gui.DataManagementPage()
# gui.getfile()
# gui.LoginPage()
# gui.HomePage()
# gui.SeatingPlanPage()
# gui.AuthPage()
