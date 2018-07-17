from operator import attrgetter

# a Company contains an email, name, location, date, time, scheduled or not, product, number of staff needed
# - Company(email, name, location, date, time, scheduled, product, num_of_staff)
class Company:

    def __init__(self, email, name, location, date, time, scheduled, product, num_of_staff):
        self.email = str(email)
        self.name = str(name)
        self.location = str(location)
        self.date = str(date)
        self.time = str(time)
        self.scheduled = int(scheduled)
        self.product = str(product)
        self.num_of_staff = num_of_staff

    def __eq__(self, other):
        return type(other) == Company and \
               self.name == other.name and \
               self.location == other.location and \
               self.product == other.product and \
               self.time == other.time and \
               self.date == other.date and \
               self.scheduled == other.scheduled and \
               self.email == other.email and \
               self.num_of_staff == other.num_of_staff

    def __repr__(self):
        return "{!r}, {!r}: {!r} {!r}, {!r} ({!r}) - {!r}\n".format(self.name, self.location, self.date, self.time, self.product, self.scheduled, self.num_of_staff)

# an Employee contains a name, date, time, scheduled or not
# Employee(name, date, time, scheduled)
class Employee:

    def __init__(self, name, date, time, scheduled):
        self.name = str(name)
        self.time = str(time)
        self.date = str(date)
        self.scheduled = scheduled

    def __eq__(self, other):
        return type(other) == Employee and \
               self.name == other.name and \
               self.time == other.time and \
               self.date == other.date and \
               self.scheduled == other.scheduled

    def __repr__(self):
        return "{!r}: {!r}, {!r} ({!r})\n".format(self.name, self.date, self.time, self.scheduled)

# a Schedule contains an Company and Employees
# Schedule(company, employees)
class Schedule: 

    def __init__(self, company, employees):
        self.company = company
        self.employees = employees

    def __eq__(self, other):
        return type(other) == Schedule and \
               self.company == other.company and \
               self.employees == other.employees

    def __repr__(self):
        return "{!r}:\n\tCompany: {!r}\n\tName:{!r}\n\tLocation:{!r}\n\tTime:{!r}\n".format(self.employees.date, self.company.name, \
            self.employees.name, self.company.location, self.company.time)

# .csv -> List
# Reads the company .cvs file and then puts it into the class
def read_company_from_files(filename):
    inFile = open(filename, "r")
    comp = []
    z = inFile.readlines()
    inFile.close()
    for i in range(1,len(z)):
        info = []
        info.append(z[i].split(","))
        info2 = ", ".join(map(str, info[0][7:]))
        n = [info[0][1], info[0][2], info[0][3], info[0][4], info[0][5], info[0][6], info2.strip('"\n"'), 0]
        new_info = Company(*n)
        comp.append(new_info)
    return comp

# .csv -> List
# Reads the employees .cvs file and then puts it into the class
def read_staff_from_files(filename):
    inFile = open(filename, "r")
    staff = []
    z = inFile.readlines()
    inFile.close()
    for i in range(1, len(z)):
        info = []
        info.append(z[i].split(","))
        n = [info[0][1], info[0][2], info[0][3].strip("\n"), 0]
        new_info = Employee(*n)
        staff.append(new_info)
    return staff

# List List -> None
# splits any Morning and Afternoons into Morning, Afternoon
def time_fix(objects1, objects2):
    i=0
    for noun in objects1:
        i+=1
        if type(noun) == (Company):
            if noun.time == "Morning and Afternoon" and noun.num_of_staff < 2:
                objects1.remove(noun)
                objects1.insert(i-1, Company(noun.email, noun.name,  noun.location, noun.date, "Morning", noun.scheduled, noun.product, noun.num_of_staff))
                objects1.insert(i, Company(noun.email, noun.name,  noun.location, noun.date, "Afternoon", noun.scheduled, noun.product, noun.num_of_staff))
    j=0
    for noun2 in objects2:
        if type(noun2) == (Employee):
            if noun2.time == "Morning and Afternoon" and noun2.scheduled < 1:
                objects2.remove(noun2)
                objects2.insert(j-1, Employee(noun2.name, noun2.date, "Morning", noun2.scheduled))
                objects2.insert(j, Employee(noun2.name, noun2.date, "Afternoon", noun2.scheduled))

# Company Employee -> Boolean
# schedules the staff in a first come first serve basis
def scheduling(place, staff):
    if place.num_of_staff < place.scheduled and staff.scheduled < 1:
        if (place.date == staff.date) and (place.time == staff.time):
            place.num_of_staff += 1
            staff.scheduled += 1
            return True
    return None

# List Company -> None
# put all unscheduled companies into a List
def unscheduled_c(unscheduled_company, place):
    if place.num_of_staff < place.scheduled:
        unscheduled_company.append(place)

# List Employee -> None
# put all unscheduled employees into a List 
def unscheduled_e(unscheduled_employee, staff):
    if staff.scheduled < 1:
        unscheduled_employee.append(staff)

# Company Employee List -> None
# runs the scheduling function
def schedule_loop(company, employee, schedules):
    for place in company:
        for staff in employee:
            if scheduling(place, staff) is not None:
                schedules.append(Schedule(place, staff))

# List List List -> None
# puts all unscheduled companies and any employee that is not certain to be ready into a List
def pending_schedules(schedules, unscheduled_company, pending_employee):
    index = []
    for i in range(len(schedules)):
        for ucomp in unscheduled_company:
            if schedules[i].company == ucomp:
                index.append(i)
    index.reverse()
    for j in range(len(index)):
        pending_employee.append(schedules[index[j]])
        schedules.remove(schedules[index[j]])

# List -> None
# sorts the schedule list by employee name then prints it
def sort_by_employee(schedules):
    schedules.sort(key = attrgetter("employees.name"))
    printer()
    print(schedules)

# List -> None
# sorts the schedule list by date then prints it
def sort_by_date(schedules):
    schedules.sort(key = attrgetter("company.date"))
    printer()
    print(schedules)

# List -> None
# sorts the schedule list by company name then prints it
def sort_by_company(schedules):
    schedules.sort(key = attrgetter("company.name"))
    printer()
    print(schedules)

# List -> None
# sorts the schedule list by location then prints it
def sort_by_location(schedules):
    schedules.sort(key = attrgetter("company.location"))
    printer()
    print(schedules)

# None -> None
# prints Schedule
def printer():
    print("\n\nSchedule:\n--------------------------------")

# List -> None
# printing function to make the buttons work smoothly
def printing(details):   
    print("\n\n\n------------------------------------")
    print(details)

# List Str -> None
# filters a keyword given and then prints it
def filter_by_word(schedules, word):
    schedules1 = []
    print("\n")
    for schedule in schedules:
        if str.lower(word) in str.lower(schedule.company.name) or \
        str.lower(word) in str.lower(schedule.company.location) or \
        str.lower(word) in str.lower(schedule.company.date) or \
        str.lower(word) in str.lower(schedule.company.time) or \
        str.lower(word) in str.lower(schedule.company.product) or \
        str.lower(word) in str.lower(schedule.employees.name):
            schedules1.append(schedule)
    print(schedules1)