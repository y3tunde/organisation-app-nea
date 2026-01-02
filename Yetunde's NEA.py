import datetime
from datetime import date
import customtkinter
import sqlite3
import random
from tkinter import *
from tkcalendar import * 
from tkinter import messagebox

#CLEAR DATABASE


app2 = customtkinter.CTk()
app2.title('Login')
app2.geometry('340x560')
app2.config(bg='#EFC9D0')

font0 = ('Times New Roman',50,'bold')
font1 = ('Courier',30,'bold')
font2 = ('Helvetica',17,'bold') 
font3 = ('Helvetica',13,'bold')
font4 = ('Helvetica',13,'bold','underline')
font5 = ('Helvetica',30,'bold')
font6 = ('Helvetica',40,'bold')
font7 = ('Times New Roman',17,'bold','underline')
font8 = ('Helvetica',10,'bold')
font9 = ('Times New Roman',30,'bold','underline')
#create database
conn = sqlite3.connect('app2.db')
#create cursor
cursor = conn.cursor() 
#commit changes
conn.commit()


#CREATING USER TABLE

cursor.execute("""CREATE TABLE IF NOT EXISTS TblUser(
Email Text PRIMARY KEY,
UserFname TEXT NOT NULL,
UserSname TEXT NOT NULL,
Password TEXT NOT NULL,
Phone TEXT,
Age INTEGER,
Verified INTEGER);""")

#END OF USER TABLE
conn.commit()


#CREATING Activity TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblActivity(
ActivityID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
UserID INTEGER,
FOREIGN KEY (UserID) REFERENCES TblUser(UserID) )""")

#END OF Activity TABLE 

#CREATING SCHEDULE TABLE

cursor.execute("""CREATE TABLE IF NOT EXISTS tblSchedule(
ScheduleID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Dimensions TEXT NOT NULL,
UserID INTEGER,
FOREIGN KEY (UserID) REFERENCES TblUser(UserID) ) """)

#END OF SCHEDULE TABLE

#CREATING LESSON TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblBox(
BoxID INTEGER PRIMARY KEY,
Description TEXT NOT NULL,
ScheduleID INTEGER,
FOREIGN KEY (ScheduleID) REFERENCES tblSchedule(ScheduleID)) """)

#END OF LESSON TABLE 

#CREATING CALENDAR TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblCalendar(
CalendarID INTEGER PRIMARY KEY) """)

#END OF CALENDAR TABLE 

#CREATING TO DO LIST TABLE

cursor.execute("""CREATE TABLE IF NOT EXISTS tblToDoList(
ToDoListID INTEGER PRIMARY KEY,
Date DATE NOT NULL,
UserID INTEGER,
CalendarID INTEGER,
FOREIGN KEY (UserID) REFERENCES TblUser(UserID),
FOREIGN KEY (CalendarID) REFERENCES tblCalendar(CalendarID)) """)

#END OF TO DO LIST TABLE

#CREATING DIFFICULTY TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblDifficulty(
DifficultyID TEXT PRIMARY KEY,
Description TEXT NOT NULL) """)

#END OF DIFFICULTY TABLE 
conn.commit()
#CREATING Task TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblTask(
TaskID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Priority TEXT NOT NULL,
RepeatWhen TEXT NOT NULL,
Time TEXT NOT NULL,
Completed INT NOT NULL,
Description TEXT NOT NULL,
ActivityID INTEGER,
ToDoListID INTEGER,
DifficultyID INTEGER,
UserID INTEGER,
FOREIGN KEY (ActivityID) REFERENCES tblActivity(ActivityID),
FOREIGN KEY (ToDoListID) REFERENCES tblToDoList(ToDoListID),
FOREIGN KEY (DifficultyID) REFERENCES tblDifficulty(DifficultyID),
FOREIGN KEY (UserID) REFERENCES TblUser(UserID)) """)

#END OF Task TABLE 
conn.commit()
#CREATING SubTask TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblSubTask(
SubTaskID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Completed INT NOT NULL,
TaskID INTEGER,
FOREIGN KEY (TaskID) REFERENCES tblTask(TaskID)) """)

#END OF SubTask TABLE

#CREATING CompletedTask TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblCompletedTask(
CompletedTaskID INTEGER PRIMARY KEY,
TaskID INTEGER,
FOREIGN KEY (TaskID) REFERENCES tblTask(TaskID)) """)

#END OF CompletedTask TABLE

#CREATING Emotion TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblEmotion(
EmotionID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Message TEXT NOT NULL)""")

#END OF Emotion TABLE

#CREATING Event TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblEvent(
EventID INTEGER PRIMARY KEY,
Date DATE NOT NULL,
EventTime INT NOT NULL,
Repeat INT NOT NULL,
EmotionID INTEGER,
CalendarID INTEGER,
FOREIGN KEY (EmotionID) REFERENCES tblEmotion(EmotionID)
FOREIGN KEY (CalendarID) REFERENCES tblCalendar(CalendarID)) """)

#END OF Event TABLE

#CREATING Reminder TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblEvent(
EventID INTEGER PRIMARY KEY,
Comment TEXT NOT NULL,
EmotionID INTEGER,
FOREIGN KEY (EmotionID) REFERENCES tblEmotion(EmotionID)) """)

#END OF Event TABLE
conn.commit()

cursor.execute("DROP TABLE IF EXISTS tblCompletedTask;")
conn.commit()

#CREATING CompletedTask TABLE 

cursor.execute("""CREATE TABLE IF NOT EXISTS tblCompletedTask(
CompletedTaskID INTEGER PRIMARY KEY,
TaskID INTEGER,
FOREIGN KEY (TaskID) REFERENCES tblTask(TaskID)) """)

#END OF CompletedTask TABLE

conn.commit()


#DELETENG EVERYTHINGG
'''cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    cursor.execute(f"DELETE FROM {table[0]};")
    print(f"Cleared data from table: {table[0]}")
conn.commit()'''





#PROGRAM

#TO DO LIST PAGES############################################################################################################################

def MoveTask(email,name):
    
    completed_tasks = []
    query = '''
    SELECT TaskID,Priority,Description
    FROM tblTask
    WHERE Name=?
    '''
    cursor.execute(query,(name,))
    global task_details
    task_details = cursor.fetchone()
    name = name
    if task_details:
        CompletedID, Priority, Description = task_details
        completed_tasks.append({
            "TaskID":CompletedID,
            "Name": name,
            "Priority": Priority,
            "Description":Description
        })

    query2 = '''
    INSERT INTO tblCompletedTask(TaskID)
    VALUES(?)
    '''
    cursor.execute(query2,(str(CompletedID),))

    query4='''
    DELETE FROM tblTask
    WHERE TaskID=?
    '''
    cursor.execute(query4,(str(CompletedID),))
    
    conn.commit()
    ToDo(email)

def StoreTask(email,Priority_entry,Description_entry,Repeat_entry,Time_entry,Difficulty_entry,Name_entry):
    name = Name_entry.get()
    priority = Priority_entry.get()
    description = Description_entry.get()
    repeat = Repeat_entry.get()
    difficulty = Difficulty_entry.get()
    time = Time_entry.get()
    
    query1="""
    SELECT UserID FROM TblUSER
    WHERE Email = ?
    """
    cursor.execute(query1,(email,))
    conn.commit()
    user_id = cursor.fetchone()

    user_id = user_id[0] 
    query ='''
    INSERT INTO tblTask(Name,Priority,RepeatWhen,Time,DifficultyID,Description,ActivityID,UserID,Completed)
    VALUES(?,?,?,?,?,?,?,?,?)
    '''
    cursor.execute(query,(name,priority,repeat,time,difficulty,description,user_id,user_id,0))
    conn.commit()
    ToDo(email)

def SetDifficulty():

    #HARD 
    query ='''
    INSERT INTO tblDifficulty(DifficultyID,Description,ScheduleID)
    VALUES(?,?,?,?)
    '''
    cursor.execute(query,("Hard","These tasks are quite difficult",))
    
def TaskInfo(email,name):

    frame4 = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame4.place(x=0,y=0)
        
    PriorityLbl = customtkinter.CTkLabel(frame4,font=font8,text='Priority Key Colours: ',text_color='#FF8BBD',bg_color='#FFE1EE')       
    PriorityLbl.place(x=12,y=12)
    
    HighBtn = customtkinter.CTkButton(frame4,command=HighPopUp,font=font8,text='High',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FF539D',hover_color='#FF8FBF',height=3,width=10)
    HighBtn.place(x=17,y=35)

    MediumBtn = customtkinter.CTkButton(frame4,command=MediumPopUp,font=font8,text='Medium',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FF8FBF',hover_color='#FFC5DF',height=3,width=10)
    MediumBtn.place(x=17,y=50)
    
    LowBtn = customtkinter.CTkButton(frame4,command=LowPopUp,font=font8,text='Low',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FFC5DF',hover_color='#FF539D',height=3,width=10)
    LowBtn.place(x=17,y=65)

    Today = customtkinter.CTkLabel(frame4,font=font5,text='Today',text_color='#FF73AF',bg_color='#FFE1EE',fg_color='#FFE1EE')
    Today.place(x=130,y=15)
    
    AddTaskBtn = customtkinter.CTkButton(frame4,command=AddTask,font=font2,text='+ New Task',text_color='#FF539D',bg_color='#FFE1EE',fg_color='#FFE1EE',hover_color='#FFFFFF')
    AddTaskBtn.place(x=170,y=93)

    IncompleteLabel = customtkinter.CTkLabel(frame4,font=font7,text='Incomplete Tasks',text_color='#000000',bg_color='#FFE1EE')       
    IncompleteLabel.place(x=12,y=100)

    CompleteLabel = customtkinter.CTkLabel(frame4,font=font7,text='Complete Tasks',text_color='#000000',bg_color='#FFE1EE')       
    CompleteLabel.place(x=12,y=300)

    query = """
    SELECT * FROM tblTask
    WHERE UserID=? AND Name=?
    """
    cursor.execute(query,(str(user_id[0]),name))
    taskInfo = cursor.fetchone()

    print(taskInfo)
    
    framePop = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFFFFF',border_color='#FFA7CD',border_width=10,width=280,height=500)
    framePop.place(x=30,y=25)

    X_buttton = customtkinter.CTkButton(framePop,command=lambda: ToDo(email),font=font2,text_color='#FF0000',text='X',fg_color='#FF8BBD',hover_color='#FFE1EE',bg_color='#FFFFFF',cursor='hand2',width=20,height=30)
    X_buttton.place(x=230,y=20)
    
    Name_display = customtkinter.CTkLabel(framePop,font=font9,text=name,text_color='#101111',bg_color='#FFE1EE',fg_color='#FFFFFF')
    Name_display.place(x=10,y=30)
    
    Priority_display = customtkinter.CTkLabel(framePop,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',text='Priority Level:',width=120,height=40)
    Priority_display.place(x=10,y=100)

    Priority_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#000000',placeholder_text=taskInfo[2],fg_color='#FFFFFF',bg_color='#FFFFFF',border_color='#FFFFFF',border_width=3,placeholder_text_color='#000000',width=100,height=20)
    Priority_entry.place(x=135,y=105)

    Description_display = customtkinter.CTkLabel(framePop,font=font2,text='Description:',text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',width=100,height=40)
    Description_display.place(x=10,y=150)

    Description_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#000000',placeholder_text=taskInfo[6],fg_color='#FFFFFF',bg_color='#FFFFFF',border_color='#FFFFFF',border_width=3,placeholder_text_color='#000000',width=200,height=20)
    Description_entry.place(x=20,y=190)

    Difficulty_display = customtkinter.CTkLabel(framePop,font=font2,text='Difficulty Level:',text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',width=100,height=40)
    Difficulty_display.place(x=15,y=270)

    Difficulty_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#000000',placeholder_text=taskInfo[9],fg_color='#FFFFFF',bg_color='#FFFFFF',border_color='#FFFFFF',border_width=3,placeholder_text_color='#000000',width=60,height=20)
    Difficulty_entry.place(x=150,y=275)

    Repeat_display = customtkinter.CTkLabel(framePop,font=font2,text='Repeat:',text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',width=80,height=40)
    Repeat_display.place(x=10,y=230)

    Repeat_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#000000',placeholder_text=taskInfo[3],fg_color='#FFFFFF',bg_color='#FFFFFF',border_color='#FFFFFF',border_width=3,placeholder_text_color='#000000',width=60,height=20)
    Repeat_entry.place(x=85,y=235)

    Time_display = customtkinter.CTkLabel(framePop,font=font2,text='Time:',text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',width=60,height=40)
    Time_display.place(x=10,y=310)

    Time_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#000000',placeholder_text=taskInfo[4],fg_color='#FFFFFF',bg_color='#FFFFFF',border_color='#FFFFFF',border_width=3,placeholder_text_color='#000000',width=60,height=20)
    Time_entry.place(x=65,y=315)
    
    CompleteTask_buttton = customtkinter.CTkButton(framePop,command=lambda: MoveTask(email,name),font=font2,text_color='#FFFFFF',text='Complete Task',fg_color='#FF8BBD',hover_color='#AA0067',bg_color='#FFFFFF',border_color='#000000',border_width=3,cursor='hand2',corner_radius=5,width=200,height=30)
    CompleteTask_buttton.place(x=40,y=370)
    
def SelectedToDo(email,selected_date):

    frame4 = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame4.place(x=0,y=0)

    now = str(selected_date)
    
    PriorityLbl = customtkinter.CTkLabel(frame4,font=font8,text='Priority Key Colours: ',text_color='#000000',bg_color='#FFE1EE')       
    PriorityLbl.place(x=12,y=12)
    
    HighBtn = customtkinter.CTkButton(frame4,command=HighPopUp,font=font8,text='High',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FF539D',hover_color='#FF8FBF',height=3,width=10)
    HighBtn.place(x=17,y=35)

    MediumBtn = customtkinter.CTkButton(frame4,command=MediumPopUp,font=font8,text='Medium',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FF8FBF',hover_color='#FFC5DF',height=3,width=10)
    MediumBtn.place(x=17,y=50)
    
    LowBtn = customtkinter.CTkButton(frame4,command=LowPopUp,font=font8,text='Low',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FFC5DF',hover_color='#FF539D',height=3,width=10)
    LowBtn.place(x=17,y=65)

    Today = customtkinter.CTkLabel(frame4,font=font5,text='Date',text_color='#FF73AF',bg_color='#FFE1EE',fg_color='#FFE1EE')
    Today.place(x=130,y=15)

    _date = customtkinter.CTkButton(frame4,command=lambda: CalendarPage(email),font=font5,  text=now,text_color='#FF73AF',hover_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FFE1EE')
    _date.place(x=120,y=50)

    AddTaskBtn = customtkinter.CTkButton(frame4,command=AddTask(email,now),font=font2,text='+ New Task',text_color='#FF539D',bg_color='#FFE1EE',fg_color='#FFE1EE',hover_color='#FFFFFF')
    AddTaskBtn.place(x=170,y=93)

    IncompleteLabel = customtkinter.CTkLabel(frame4,font=font7,text='Incomplete Tasks',text_color='#000000',bg_color='#FFE1EE')       
    IncompleteLabel.place(x=12,y=100)

    CompleteLabel = customtkinter.CTkLabel(frame4,font=font7,text='Complete Tasks',text_color='#000000',bg_color='#FFE1EE')       
    CompleteLabel.place(x=12,y=300)

    query1="""
    SELECT UserID FROM TblUSER
    WHERE Email = ?
    """
    cursor.execute(query1,(email,))
    user_id = cursor.fetchone()
    user_id = user_id[0]
    query ='''
    INSERT INTO tblToDoList(Date,UserID)
    VALUES(?,?)
    '''
    cursor.execute(query,(now,str(user_id)))
    conn.commit()
    cursor.execute(query,(now,str(user_id)))
    query2 = """
    SELECT Name,Priority FROM tblTask
    WHERE UserID = ?
    """
    cursor.execute(query2,(str(user_id)))
    UserList = cursor.fetchall()
    print(UserList)
    count = 0
    StartPoint = 130 
    for Task in UserList:
        count = count + 1
        Colour = Task[1]
        if Colour == 'High':
            hexCode = '#FF539D'
        elif Colour == 'Medium':
            hexCode = '#FF8FBF'
        elif Colour == 'Low':
            hexCode = '#FFC5DF'
        Task = Task[0]
        UserTaskBtn = customtkinter.CTkButton(frame4,command=lambda: TaskInfo(email,Task),font=font2,text=str(Task),text_color='#FFFFFF',bg_color='#FFE1EE',fg_color=hexCode,hover_color='#FFFFFF')
        UserTaskBtn.place(x=17,y=StartPoint)
        StartPoint = StartPoint+40

def getDate(email,selected_date,cal):
    selected_date = cal.get_date()
    print(selected_date) 
    SelectedToDo(email,selected_date)
    
def CalendarPage(email,selected_date):
    root = Tk()
    root.geometry("340x540")
    root.title("Calendar")
    
    cal = Calendar(
        root, 
        selectmode="day", 
        date_pattern="dd/mm/y")
    cal.pack(pady=0)
    submit_btn = Button(root, text="Submit", command=lambda: getDate(email,selected_date,cal))
    submit_btn.pack()
    root.mainloop()
    
def HighPopUp():
    messagebox.showinfo('High','These Tasks are most important')
def MediumPopUp():
    messagebox.showinfo('Medium','These Tasks are mildly important')
def LowPopUp():
    messagebox.showinfo('Low','These Tasks are least important')

    
def ToDo(email):
    global CTaskDetails
    CTaskDetails = []
    frame4 = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame4.place(x=0,y=0)
    selected_date = date.today()
    now = selected_date#initialises the date to be displayed  
    
    PriorityLbl = customtkinter.CTkLabel(frame4,font=font8,text='Priority Key Colours: ',text_color='#000000',bg_color='#FFE1EE')       
    PriorityLbl.place(x=12,y=12)#labels the priority levels
    
    HighBtn = customtkinter.CTkButton(frame4,command=HighPopUp,font=font8,text='High',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FF539D',hover_color='#FF8FBF',height=3,width=10)
    HighBtn.place(x=17,y=35)

    MediumBtn = customtkinter.CTkButton(frame4,command=MediumPopUp,font=font8,text='Medium',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FF8FBF',hover_color='#FFC5DF',height=3,width=10)
    MediumBtn.place(x=17,y=50)
    
    LowBtn = customtkinter.CTkButton(frame4,command=LowPopUp,font=font8,text='Low',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FFC5DF',hover_color='#FF539D',height=3,width=10)
    LowBtn.place(x=17,y=65)

    Today = customtkinter.CTkLabel(frame4,font=font5,text='Today',text_color='#FF73AF',bg_color='#FFE1EE',fg_color='#FFE1EE')
    Today.place(x=120,y=20)
    
    _date = customtkinter.CTkButton(frame4,command=lambda: CalendarPage(email,selected_date),font=font5,text=now,text_color='#FF73AF',hover_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FFE1EE')
    _date.place(x=120,y=50)#displays the date of the to do list

    AddTaskBtn = customtkinter.CTkButton(frame4,command=lambda: AddTask(email,now),font=font2,text='+ New Task',text_color='#FF539D',bg_color='#FFE1EE',fg_color='#FFE1EE',hover_color='#FFFFFF')
    AddTaskBtn.place(x=170,y=93)#Takes the user to the page where they can add a task to the to do list

    IncompleteLabel = customtkinter.CTkLabel(frame4,font=font7,text='Incomplete Tasks',text_color='#000000',bg_color='#FFE1EE')       
    IncompleteLabel.place(x=12,y=100)

    CompleteLabel = customtkinter.CTkLabel(frame4,font=font7,text='Complete Tasks',text_color='#000000',bg_color='#FFE1EE')       
    CompleteLabel.place(x=12,y=300)

    
    query1="""
    SELECT UserID FROM TblUSER
    WHERE Email = ?
    """
    cursor.execute(query1,(email,))
    user_id = cursor.fetchone()
    user_id = user_id[0]
    query ='''
    INSERT INTO tblToDoList(Date,UserID)
    VALUES(?,?)
    '''  
    cursor.execute(query,(now,str(user_id)))
    #Fetches the name and priority level of all the tasks stored in the database
    query2 = """
    SELECT Name,Priority FROM tblTask
    WHERE UserID = ?
    """
    cursor.execute(query2,(str(user_id)))
    UserList = cursor.fetchall()#Stores all the e details from query2 in UserList
    print(UserList)
    count = 0
    StartPoint = 130
    for Task in UserList:
        count = count + 1
        Colour = Task[1]
        if Colour == 'High':
            hexCode = '#FF539D'
        elif Colour == 'Medium':
            hexCode = '#FF8FBF'
        elif Colour == 'Low':
            hexCode = '#FFC5DF'
        Task = Task[0]
        name = Task
        #displays every task in the stored tasks on the to do list page
        UserTaskBtn = customtkinter.CTkButton(frame4,command=lambda: TaskInfo(email,name),font=font2,text=name,text_color='#FFFFFF',fg_color=hexCode,bg_color='#FFE1EE',hover_color='#FFFFFF')
        UserTaskBtn.place(x=17,y=StartPoint)
        StartPoint = StartPoint+40
        cursor.execute(query,(now,str(user_id)))
        
    query3 = '''
    SELECT TaskID FROM tblCompletedTask
    '''
    cursor.execute(query3)
    CompletedTaskIDs = cursor.fetchall()

    count = 0
    StartPoint = 330

    if len(CompletedTaskIDs)>0: 
        for ID in CompletedTaskIDs:
                if ID == task_details[0]:
                    count = count + 1
                    Colour = task_details[1]
                    print(Colour)
                    if Colour == 'High':
                        hexCode = '#FF539D'
                    elif Colour == 'Medium':
                        hexCode = '#FF8FBF'
                    elif Colour == 'Low':
                        hexCode = '#FFC5DF'
                    Task = task_details[2]
                    name2 = Task
                    print(name2)
                    UserCTaskBtn = customtkinter.CTkButton(frame4,command=lambda: TaskInfo(email,name),font=font2,text=name2,text_color='#FFFFFF',bg_color='#FFE1EE',fg_color=hexCode,hover_color='#FFFFFF')
                    UserCTaskBtn.place(x=17,y=StartPoint)
                    StartPoint = StartPoint+40

    else:
        print("no completed tasks to display")
    conn.commit()

def AddTask(email,now):
    
    frame4 = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame4.place(x=0,y=0)
        
    PriorityLbl = customtkinter.CTkLabel(frame4,font=font8,text='Priority Key Colours: ',text_color='#FF8BBD',bg_color='#FFE1EE')       
    PriorityLbl.place(x=12,y=12)
    
    HighBtn = customtkinter.CTkButton(frame4,command=HighPopUp,font=font8,text='High',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FF539D',hover_color='#FF8FBF',height=3,width=10)
    HighBtn.place(x=17,y=35)

    MediumBtn = customtkinter.CTkButton(frame4,command=MediumPopUp,font=font8,text='Medium',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FF8FBF',hover_color='#FFC5DF',height=3,width=10)
    MediumBtn.place(x=17,y=50)
    
    LowBtn = customtkinter.CTkButton(frame4,command=LowPopUp,font=font8,text='Low',text_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FFC5DF',hover_color='#FF539D',height=3,width=10)
    LowBtn.place(x=17,y=65)


    Today = customtkinter.CTkLabel(frame4,font=font5,text='Today',text_color='#FF73AF',bg_color='#FFE1EE',fg_color='#FFE1EE')
    Today.place(x=130,y=15)
    
    _date = customtkinter.CTkButton(frame4,command=CalendarPage,font=font5,text=now,text_color='#FF73AF',hover_color='#FFFFFF',bg_color='#FFE1EE',fg_color='#FFE1EE')
    _date.place(x=120,y=50)
    
    AddTaskBtn = customtkinter.CTkButton(frame4,command=AddTask,font=font2,text='+ New Task',text_color='#FF539D',bg_color='#FFE1EE',fg_color='#FFE1EE',hover_color='#FFFFFF')
    AddTaskBtn.place(x=170,y=93)

    IncompleteLabel = customtkinter.CTkLabel(frame4,font=font7,text='Incomplete Tasks',text_color='#000000',bg_color='#FFE1EE')       
    IncompleteLabel.place(x=12,y=100)
    
    framePop = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=280,height=500)
    framePop.place(x=20,y=25)

    X_buttton = customtkinter.CTkButton(framePop,command=lambda: ToDo(email),font=font2,text_color='#FF0000',text='X',fg_color='#FF8BBD',hover_color='#FFE1EE',bg_color='#FFE1EE',cursor='hand2',width=20,height=30)
    X_buttton.place(x=230,y=20)

    Name_entry = customtkinter.CTkEntry(framePop,font=font5,placeholder_text='Name',text_color='#000000',bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFE1EE',placeholder_text_color='#000000',border_width=10)
    Name_entry.place(x=60,y=60)
    
    Priority_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='Priority Level',placeholder_text_color='#FF8BBD',width=200,height=40)
    Priority_entry.place(x=40,y=140)

    Description_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='Description',placeholder_text_color='#FF8BBD',width=200,height=40)
    Description_entry.place(x=40,y=180)

    Repeat_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='Repeat',placeholder_text_color='#FF8BBD',width=200,height=40)
    Repeat_entry.place(x=40,y=220)

    Difficulty_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='Difficulty Level',placeholder_text_color='#FF8BBD',width=200,height=40)
    Difficulty_entry.place(x=40,y=260)

    Time_entry = customtkinter.CTkEntry(framePop,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='Time(HH:MM AM/PM)',placeholder_text_color='#FF8BBD',width=200,height=40)
    Time_entry.place(x=40,y=300)
           
    CreateTask_buttton = customtkinter.CTkButton(framePop,command=lambda: StoreTask(email,Priority_entry,Description_entry,Repeat_entry,Time_entry,Difficulty_entry,Name_entry),font=font2,text_color='#FFE1EE',text='Create Task',fg_color='#FF8BBD',hover_color='#AA0067',bg_color='#FF8BBD',cursor='hand2',corner_radius=5,width=200,height=30)
    CreateTask_buttton.place(x=40,y=370)


######END OF TO DO PAGES############################################################################################################################













#####QUESTIONNAIRE PAGES############################################################################################################################

def storeActivity(userID,question2_entry):
  
    activity = question2_entry.get()

    '''query="""
    SELECT Email FROM TblUSER
    WHERE Email = ?
    
    """
    cursor.execute(query,(str(email),))     THIS PART BECOMES COMPLETELY UNNECESSARY
    user_id = cursor.fetchone()
            
    user_id = user_id[0]'''


    
    insert_query = '''
    INSERT INTO tblActivity(Name,Email)
    VALUES(?,?)
    '''
    cursor.execute(insert_query,(activity,userID))
    conn.commit()
    question2_entry.delete(0,len(activity))

def storeAge(email,question1_entry):
    labelWidth=200
    age =  question1_entry.get()

    #INSERTING VALUES INTO DB
    query = '''
    UPDATE TblUser
    SET Age = ?
    WHERE Email = ?
    '''
    cursor.execute(query,(age,str(email)))
    conn.commit()
    questionnaire2(email)

def questionnaire2(email):
    Temp = 0
    labelWidth=200

    frame3 = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame3.place(x=0,y=0)

    appName_label2 = customtkinter.CTkLabel(frame3,font=font0,text='appName',text_color='#000000',bg_color='#FFE1EE')       
    appName_label2.place(x=70,y=50)

    question2 = customtkinter.CTkLabel(frame3,font=font5,text='What is an activity \nyou enjoy (Enter 3)',text_color='#FF539D',bg_color='#FFE1EE')       
    question2.place(x=50,y=150)

    question2_entry = customtkinter.CTkEntry(frame3,font=font2,text_color='#FFA7CD',fg_color='#FFFFFF',bg_color='#FFFFFF',border_color='#FFA7CD',border_width=3,width=200,height=50)
    question2_entry.place(x=70,y=250)
    
    #Stores activity in database
    AddActivity_button = customtkinter.CTkButton(frame3,command= lambda: storeActivity(email,question2_entry),font=font2,text_color='#FFE1EE',text='Add Activity',fg_color='#FFA7CD',hover_color='#AA0067',bg_color='#FFA7CD',cursor='hand2',corner_radius=5,width=200,height=30)
    AddActivity_button.place(x=70,y=350)

    #Continues to the login page
    Next_button = customtkinter.CTkButton(frame3,command=login,font=font2,text_color='#FFE1EE',text='Next',fg_color='#FFA7CD',hover_color='#AA0067',bg_color='#FFA7CD',cursor='hand2',corner_radius=5,width=200,height=30)
    Next_button.place(x=70,y=400)

def questionnaire1(email):
    labelWidth=200

    frame3 =  customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame3.place(x=0,y=0)

    appName_label2 = customtkinter.CTkLabel(frame3,font=font0,text='appName',text_color='#000000',bg_color='#FFE1EE')       
    appName_label2.place(x=70,y=50)
    
    question1 = customtkinter.CTkLabel(frame3,font=font5,text='How old are you?',text_color='#FF539D',bg_color='#FFE1EE')       
    question1.place(x=50,y=150)

    question1_entry = customtkinter.CTkEntry(frame3,font=font2,text_color='#FFA7CD',fg_color='#FFFFFF',bg_color='#FFFFFF',border_color='#FFA7CD',border_width=3,width=200,height=50)
    question1_entry.place(x=70,y=250)

    Enter_button = customtkinter.CTkButton(frame3,command=lambda: storeAge(email,question1_entry),font=font2,text_color='#FFE1EE',text='Enter',fg_color='#FFA7CD',hover_color='#AA0067',bg_color='#FFA7CD',cursor='hand2',corner_radius=5,width=200,height=30)
    Enter_button.place(x=70,y=400)


    
######END OF QUESTIONNAIRE PAGES#################################################################################################################




######SIGN UP LOG IN PAGES#######################################################################################################################

def StoreInfo(hPass,email,FName,LName,Phone,password):

    #INSERTING VALUES INTO DB
    cursor.execute("""
        INSERT INTO TblUser (UserFname,UserSname,Email,Phone,Password)
        VALUES(?,?,?,?,?)
    """, (FName,LName,str(email),Phone,hPass))
    conn.commit()
          
    messagebox.showinfo('Success','Account has been created.')

    questionnaire1(email)
    
def signup_account(Email_entry,FirstName_entry,LastName_entry,Phone_entry,password_entry):
    
    userID = Email_entry.get()#here i defined initialised the user ID variable as the users email
    print(email)
    FName = FirstName_entry.get()
    LName = LastName_entry.get()
    Phone = Phone_entry.get()
    password = password_entry.get()
    
    if email != '' and password != '' and FName != '' and LName != '':
        
        for char in FName:
            if not char.isalpha():
                messagebox.showerror('Error','Enter a real name')
                signup()
                return
            
        if len(Phone) != 11:
            messagebox.showerror('Error','Your phone number should be 11 integers')
            signup()
            return
        for num in Phone:
            if not num.isdigit():
                messagebox.showerror('Error','Enter a valid Phone number')
                signup()
                return

        cursor.execute("SELECT Email FROM TblUser")
        Email = cursor.fetchall()
        for item in Email:
            
            if item[0] == email:
                messagebox.showerror('Error','Email already exists.')
                signup()
                return
        if len(password)>10:
            messagebox.showerror('Error','Password must be 10 characters or less.')

        #HASHING ALGORITHM

        else:
            hashWords = ["bunny","leprechaun","pink","sky","cake","echo"]
            values = []
            passLength = 0
            for i in password:
                val=ord(i)
                values.append(val)
                passLength += 1
            num1 = values[passLength//2]
            if passLength > 5:
                passLength = passLength//2
            
            num2 = hashWords[passLength]
            num2 = len(num2)

            hashed_password= (num1//passLength) + num2
            print(hashed_password)

        #COLISION RESOLUTION
            query = """
            SELECT Password FROM TblUser
            """
            cursor.execute(query)
            storedPasswords=cursor.fetchall()

            print(storedPasswords)
            
            if storedPasswords != '':
                for item in storedPasswords:
                    password = int(item[0])
                    print(password)
                    
                    if hashed_password == password:
                        hashed_password +=1
                        print(hashed_password)
                    else:
                        hashed_password = hashed_password
            else:
                StoreInfo(hashed_password,email,FName,LName,Phone,password)
                
            StoreInfo(hashed_password,email,FName,LName,Phone,password)
            
    else:
        messagebox.showerror('Error','Enter all data')
        signup() 

def signup():
    frame1 = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame1.place(x=0,y=0)
    
    #label of the app name
    appName_label2 = customtkinter.CTkLabel(frame1,font=font0,text='appName',text_color='#000000',bg_color='#FFE1EE')       
    appName_label2.place(x=70,y=50)

    #label of the page the user is currently on, sign up page
    signup_label = customtkinter.CTkLabel(frame1,font=font1,text='Sign Up',text_color='#FF8BBD',bg_color='#FFE1EE')
    signup_label.place(x=110,y=130)

    #stores the users email when they sign up
    Email_entry = customtkinter.CTkEntry(frame1,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='Email',placeholder_text_color='#FF8BBD',width=200,height=40)
    Email_entry.place(x=70,y=180)
    
    #stores the users first name when they sign up
    FirstName_entry = customtkinter.CTkEntry(frame1,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='First Name',placeholder_text_color='#FF8BBD',width=200,height=40)
    FirstName_entry.place(x=70,y=220)

    #stores the users last name when they sign up
    LastName_entry = customtkinter.CTkEntry(frame1,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='Last Name',placeholder_text_color='#FF8BBD',width=200,height=40)
    LastName_entry.place(x=70,y=260)

    #stores the users phone number when they sign up
    Phone_entry = customtkinter.CTkEntry(frame1,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='Phone',placeholder_text_color='#FF8BBD',width=200,height=40)
    Phone_entry.place(x=70,y=300)
    
    #stores the users password when they sign up
    password_entry = customtkinter.CTkEntry(frame1,font=font2,text_color='#FF8BBD',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FF8BBD',border_width=3,placeholder_text='password',placeholder_text_color='#FF8BBD',width=200,height=40)
    password_entry.place(x=70,y=340)

    #takes all the user information to be stored in the signup_account subprogram
    signup_buttton = customtkinter.CTkButton(frame1,command=lambda: signup_account(Email_entry,FirstName_entry,LastName_entry,Phone_entry,password_entry),font=font2,text_color='#FFE1EE',text='Create Account',fg_color='#FF8BBD',hover_color='#AA0067',bg_color='#FF8BBD',cursor='hand2',corner_radius=5,width=200,height=30)
    signup_buttton.place(x=70,y=400)

    #igives the user the option to login if they have an account
    login_label = customtkinter.CTkLabel(frame1,font=font3,text='already have an account?',text_color='#E2619F',bg_color='#FFE1EE')
    login_label.place(x=70,y=450)

    #takes user to the log in page
    login_button = customtkinter.CTkButton(frame1,command=login,font=font4,text_color='#FFE1EE',text='login',fg_color='#E2619F',hover_color='#AA0067',bg_color='#FFE1EE',cursor='hand2',width=40)
    login_button.place(x=235,y=450)


'''def apply_styles():

    style = ttk.Style() 
    # Configure the style for the calendar 
    style.configure("TCalendar", 
                    background="#FFE1EE", # Background color 
                    foreground="#E2619F", # Text color 
                    bordercolor="#FF8BBD", # Border color 
                    borderwidth=2, # Border width 
                    relief="solid") # Border style 
    
    # Customize header style (months) 
    style.configure("CalendarHeader.TLabel", 
                    background="#FFE1EE", 
                    foreground="#FFE1EE", 
                    font=font2) 
    # Customize day cells 
    style.configure("CalendarDay.TLabel", 
                    background="lightyellow", 
                    foreground="black", 
                    font=("Helvetica", 10)) 
    # Customize the selected day 
    style.configure("CalendarSelectedDay.TLabel", 
                    background="lightgreen", 
                    foreground="black", 
                    font=("Helvetica", 10))'''

def login_account(email_entry2,password_entry2):
    
    email = email_entry2.get()
    password = password_entry2.get()
    #checks if the inputs are empty
    if email != '' and password != '':
        query2 = '''
        SELECT Email FROM TblUser
        WHERE Email=?
        '''
        cursor.execute(query2,(email,))
        StoredEmail = cursor.fetchone()
        
        if StoredEmail != None:
            pass
            #selecting the password stored with the email the user inputs
            query = """
            SELECT Password FROM TblUser
            WHERE Email=?
            """
            cursor.execute(query,(email,))
            result = cursor.fetchone()
            print(result)

            if result!="" or result!=None:
                #hashing algorithm is applied to users input
                hashWords = ["bunny","leprechaun","pink","sky","cake","echo"]
                values = []
                passLength = 0
                for i in password:
                    val=ord(i)
                    values.append(val)
                    passLength += 1
                num1 = values[passLength//2]
                if passLength > 5:
                    passLength = passLength//2
                
                num2 = hashWords[passLength]
                num2 = len(num2)

                hashed_password= (num1//passLength) + num2
                
                #hashed password is compared with stored passwored
                if str(result[0]) == str(hashed_password):
                    messagebox.showinfo('Success','Logged in successfully.')
                    #selects the users user id once they have logged in
                    query ='''
                    SELECT UserID FROM tblUser
                    WHERE Email = ?
                    '''
                    cursor.execute(query,(str(email),))
                    #globalises the user id
                    global user_id
                    user_id = cursor.fetchone()
                    ToDo(email)#takes user to their account to do list
                    
                elif result[0] != hashed_password:#if the password doesnt match an error occurs
                    messagebox.showerror('Error','Invalid Password')
        else:
            #if the email is not stored this message appears
            messagebox.showerror('Error','Account does not exist')
    else:
         messagebox.showerror('Error','Enter All Details')
        
            
def login():
    frame1 = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame1.place(x=0,y=0)
    frame1.destroy()#removes the sign up frame
    
    frame2 = customtkinter.CTkFrame(app2,bg_color='#FFE1EE',fg_color='#FFE1EE',border_color='#FFA7CD',border_width=10,width=340,height=560)
    frame2.place(x=0,y=0)

    appName_label2 = customtkinter.CTkLabel(frame2,font=font0,text='appName',text_color='#000000',bg_color='#FFE1EE')       
    appName_label2.place(x=70,y=50)

    login_label2 = customtkinter.CTkLabel(frame2,font=font1,text='Log In',text_color='#FF8BBD',bg_color='#FFE1EE')       
    login_label2.place(x=120,y=150)

    #stores the users email entry. If valid this is used throughout the whole program
    email_entry2 = customtkinter.CTkEntry(frame2,font=font2,text_color='#1B1C1C',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FFA7CD',border_width=3,placeholder_text='Email',placeholder_text_color='#000000',width=200,height=50)
    email_entry2.place(x=70,y=200)

    #users password entry 
    password_entry2 = customtkinter.CTkEntry(frame2,font=font2,text_color='#000000',fg_color='#FFFFFF',bg_color='#FFE1EE',border_color='#FFA7CD',border_width=3,placeholder_text='password',placeholder_text_color='#000000',width=200,height=50)
    password_entry2.place(x=70,y=270)
    
    #takes user back to the sign up page
    return_button = customtkinter.CTkButton(frame2,command=signup,font=font2,text_color='#FFE1EE',text='Create Account',fg_color='#FF8BBD',hover_color='#AA0067',bg_color='#FFA7CD',cursor='hand2',corner_radius=5,width=200,height=30)
    return_button.place(x=70,y=400)

    #takes all the user inputs to be checked in the login_account subprogram
    login_buttton2 = customtkinter.CTkButton(frame2,command=lambda: login_account(email_entry2,password_entry2),font=font2,text_color='#FFE1EE',text='Log In',fg_color='#FF8BBD',hover_color='#AA0067',bg_color='#FFA7CD',cursor='hand2',corner_radius=5,width=200,height=30)
    login_buttton2.place(x=70,y=350)


#######END OF SIGN UP PAGES#########################################################################################################################
signup()

app2.mainloop()


###PRINTING DATABASE
cursor.execute("SELECT * FROM TblUser")
users = cursor.fetchall()
print("Users:")
for user in users:
    print(user)


cursor.execute("SELECT * FROM tblActivity")
activities = cursor.fetchall()
print("Activity:")
for activity in activities:
    print(activity)


cursor.execute("SELECT * FROM tblToDoList")
Lists = cursor.fetchall()
print("To Do Lists:")
for List in Lists:
    print(List)
    
cursor.execute("SELECT * FROM tblTask")
Tasks = cursor.fetchall()
print("Tasks:")
for Task in Tasks:
    print(Task)

cursor.execute("SELECT TaskID FROM tblCompletedTask")
CTasks = cursor.fetchall()
print("Completed Tasks:")
for Task in CTasks:
    print(Task)
conn.close()

