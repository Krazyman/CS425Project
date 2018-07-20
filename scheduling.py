from tkinter import *
import tkinter.filedialog
from funcs import *
import os
from PIL import ImageTk, Image

class Redir(object):
    # This is what we're using for the redirect, it needs a text box
    def __init__(self, textbox):
        self.textbox = textbox
        self.textbox.config(state=NORMAL)
        # self.fileno = sys.stdout.fileno


    def write(self, message):
        # When you set this up as redirect it needs a write method as the
        # stdin/out will be looking to write to somewhere!
        self.textbox.insert(END, str(message))

class Holder:

    def __init__(self, name, lst):
        self.name = name
        self.lst = lst

    def __eq__(self, other):
        return type(other) == Holder and \
               self.name == other.name and \
               self.lst == other.lst

    def get(self):
        return self.lst

# prints the schedule details into a text file of your desire
def file_save():
    f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    print(f)
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    # text2save = str(text.get(1.0, END)) # starts from `1.0`, not `0.0`
    for schedule in schedules:
        f.write(str(schedule))
    f.write("\n\nUnscheduled locations:")
    for i in unscheduled_company:
        f.write(str(i))
    f.write("\n\nUnscheduled employees:")    
    for j in unscheduled_employee:
        f.write(str(j))
    f.write("\n\nPending schedules due to minimum number of staff not met:")
    for k in pending_employee:
        f.write(str(k))
    f.close() # `()` was missing.

# function to ask for user files
def askopenfilename():
    """ Prints the selected files name """
    # get filename, this is the bit that opens up the dialog box this will
    # return a string of the file name you have clicked on.
    filename = tkinter.filedialog.askopenfilename()
    if filename:
        # Will print the file name to the text box
        print(filename)

# pops up to ask for company requested schedules
def my_PR_file():
    filename = tkinter.filedialog.askopenfilename( initialdir="C:/desktop/CS425", title="select file", filetypes=(("comma-seperated values", "csv"), ("text files", "*.txt"), ("all files", "*.*")))
    # os.system(r"notepad.exe " + filename)
    global y
    company = read_company_from_files(filename)
    y = Holder("company", company)
    print("Promotion Request File Read!!!")

# pops up to ask for company requested schedules
def my_staff_file():
    filename = tkinter.filedialog.askopenfilename( initialdir="C:/desktop/CS425", title="select file", filetypes=(("comma-seperated values", "csv"), ("text files", "*.txt"), ("all files", "*.*")))
    # os.system(r"notepad.exe " + filename)
    global x
    employee = read_staff_from_files(filename)
    x = Holder("employee", employee)
    print("Staff Schedule Read!!!")

# Starts the scheduling 
def main():

    company = y.get()
    employee = x.get() 
    global schedules
    global unscheduled_employee
    global unscheduled_company
    global pending_employee
    schedules = []
    unscheduled_company = []
    unscheduled_employee = []
    pending_employee = []
    time_fix(company, employee)
    schedule_loop(company, employee, schedules)
    for place in company:
        unscheduled_c(unscheduled_company, place)
    for staff in employee:
        unscheduled_e(unscheduled_employee, staff)
    sort_by_date(schedules)
    pending_schedules(schedules, unscheduled_company, pending_employee)
    print("Unscheduled locations:")
    print(unscheduled_company)
    print("Unscheduled employees:")
    print(unscheduled_employee)
    print("Pending schedules due to minimum number of staff not met:")
    print(pending_employee)
    
# function for action event
def buttonpress(function, *args):
    value = function(*args)
    textbox.see(END)

# Creates the window for the graphic user interface
def gui():
    root = Tk()
    root.geometry("700x600")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.title("MBI Scheduling Program")
    root.iconbitmap("Logos-mbi.ico")

    img1 = PhotoImage(file='i4.png')
    panel1 = Label(root, image=img1)
    panel1.grid(row=4, column=4+1, sticky=N+S+E+W)


    img2 = PhotoImage(file='i2.png')   
    panel2 = Label(root, image=img2)
    panel2.grid(row=4, column=5+1, sticky=N+S+E+W)

    img3 = PhotoImage(file='i3.png')
    panel3 = Label(root, image=img3)
    panel3.grid(row=4, column=6+1, sticky=N+S+E+W)

    img4 = PhotoImage(file='i1.png')   
    panel4 = Label(root, image=img4)
    panel4.grid(row=4, column=7+1, sticky=N+S+E+W)

    # Make a button to get the file name
    # The method the button executes is the askopenfilename from above
    # You don't use askopenfilename() because you only want to bind the button
    # to the function, then the button calls the function.
    button0 = Button(root, text='save as', command=file_save, fg='blue')
    button0.grid(row=1, column=6)

    button1 = Button(root, text='Promotion Request Form', command=my_PR_file, fg='blue')
    # button = Button(root, text="open text file", command = my_file).pack(, fg='blue')
    # this puts the button at the top in the middle
    button1.grid(row=1, column=1, sticky=W+E)

    button2 = Button(root, text='Staff Schedule', command=my_staff_file, fg='blue')
    button2.grid(row=1, column=2, sticky=W+E)

    button3 = Button(root, text='Start', command=main, fg='blue')
    button3.grid(row=1, column=3, sticky=W+E)

    e1 = Entry(root)
    e1.grid(row=1, column=4, sticky=W+E)
    button4 = Button(root, text='Filter', command=lambda: buttonpress(filter_by_word, schedules, e1.get()), fg='blue')
    button4.grid(row=1, column=5, sticky=W+E)

    label1 = Label(root, text='Sort:', fg='blue')
    label1.grid(row=3, column=0, sticky=W+E)

    button5 = Button(root, text='Date', command=lambda: buttonpress(sort_by_date, schedules), fg='blue')
    button5.grid(row=3, column=1, sticky=W+E)

    button6 = Button(root, text='Employee', command=lambda: buttonpress(sort_by_employee, schedules), fg='blue')
    button6.grid(row=3, column=2, sticky=W+E)

    button7 = Button(root, text='Company', command=lambda: buttonpress(sort_by_company, schedules), fg='blue')
    button7.grid(row=3, column=3, sticky=W+E)

    button8 = Button(root, text='Location', command=lambda: buttonpress(sort_by_location, schedules), fg='blue')
    button8.grid(row=3, column=4, sticky=W+E)

    button9 = Button(root, text='Unscheduled Companies', command=lambda: buttonpress(printing, unscheduled_company), fg='blue')
    button9.grid(row=4, column=1, sticky=W+E)

    button10 = Button(root, text='Unscheduled Employees', command=lambda: buttonpress(printing, unscheduled_employee), fg='blue')
    button10.grid(row=4, column=2, sticky=W+E)

    button11 = Button(root, text='Pendng Schedules', command=lambda: buttonpress(printing, pending_employee), fg='blue')
    button11.grid(row=4, column=3, sticky=W+E)

    # Make a scroll bar so we can follow the text if it goes off a single box
    scrollbar = Scrollbar(root, orient=VERTICAL)
    # This puts the scrollbar on the right handside
    scrollbar.grid(row=2, column=8, sticky=N+S+E)

    # Make a text box to hold the text
    global textbox
    textbox = Text(root,font=("Helvetica",8),state=DISABLED, yscrollcommand=scrollbar.set, wrap=WORD)
    # This puts the text box on the left hand side
    textbox.config(width=100, height=35)
    textbox.grid(row=2, rowspan=1, column=0, columnspan=8, sticky=N+S+W+E)

    # Configure the scroll bar to stroll with the text box!
    scrollbar.config(command=textbox.yview)

    #Set up the redirect 
    stdre = Redir(textbox)
    # Redirect stdout, stdout is where the standard messages are output
    sys.stdout = stdre
    # Redirect stderr, stderr is where the errors are printed too!
    sys.stderr = stdre
    # Print hello so we can see the redirect is working!
    print ("Please input Promotion Request and Staff Schedule.\nPress Start when files are inputted.\n\
Use the buttons to sort and filter the schedules that have been generated.\n")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1) # not needed, this is the default behavior
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    # Start the application mainloop
    root.mainloop()

if __name__.endswith('__main__'):
    gui()