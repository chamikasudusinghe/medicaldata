import hashlib as h
import getpass

class ABChospital:
    
    def _init_(self):
        self.username=""
        self.privilege=""
        self.userid=""        
        
    def userInput(self):
        print("Welcome to ABC Hospital Management System")
        print("-----------------------------------------")
        print("-----------------------------------------")
        userinit = input("Login or SignUp? (login/signup)")
        userinit = userinit.lower()
        if userinit == "login":
            self.logIn()
        elif userinit == "signup":
            self.signUp()
        else:
            print("Invalid Credentials")
            
    def signUp(self):
        print("SignUp is Stricly Reseicted to ABC Hospital Employees")
        username = input("Please Enter a Username: ")
        password = getpass.getpass("Please Enter a Password: ")
        usertype = "staff"
        empid = input("Please Enter Your Employee Id: ")
        print("Please Follow these Instructions when Answering the Next Question")
        print("If you are a doctor, answer as 1")
        print("If you are a nurse, answer as 2")
        privilege = input("Which Category are You Falling Into?")
        self.writeConfig(username,password,empid,usertype,privilege)
        print("Registration Successful")
        print("Please Login")
        self.logIn()
        
    def logIn(self):
        print("If you are not having an account, enter 'signup' as the username ")
        username = input("Enter Your Username: ")
        if (username == "signup"):
            self.signUp()
        password = getpass.getpass("Enter Password: ")
        seek = 0
        while not self.validate(username, password):
            seek+=1
            if (seek<5):
                username = input("Enter Your Username: ")
                password = getpass.getpass("Enter Your Password: ")
            else:
                print("Session Terminated")
        else:
            print ("You are Authorized")
            print ("Logged In")
            self.tasks()
    
    def writeConfig(self,username, password, userid, usertype, privilege):
        with open("config.txt", "a") as file:
            file.write(username + "," + h.md5(password.encode("utf-8")).hexdigest() + ","+userid+","+ usertype+","+privilege + "\n")
    
    def validate(self,username, password):
        users = self.readConfig()
        for line in users:
            if line[0] == username and line[1] == h.md5(password.encode("utf-8")).hexdigest():
                if (self.readData(username, "first")):
                    print("You are Logging in for the First Time")
                    newusername = input("Enter A New Username: ")
                    newpassword = getpass.getpass("Enter A New Password: ")
                    rfile = open("config.txt", "r")
                    lines = rfile.readlines()
                    for found in range(len(lines)):
                        if (username in lines[found]):
                            content = lines[found].rstrip("\n").split(",")
                            content[0] = newusername
                            content[1] = h.md5(newpassword.encode("utf-8")).hexdigest()
                            content = content[0] + "," + content[1] + ","+content[2]+","+ content[3]+","+ content[4]+ "\n"
                        rfile = open("config.txt", "w")
                        rfile.writelines(lines)
                    for found in range(len(lines)):
                        if (username in lines[found]):
                            lines[found] = content
                    rfile = open("config.txt", "w")
                    rfile.writelines(lines)
                    rfile.close()
                    content = content.rstrip("\n").split(",")
                    self.username = content[0]
                    self.userid = content[2]
                    self.privilege = content[4]
                else:
                    self.username = line[0]
                    self.userid = line[2]
                    self.privilege = line[4]
                return True
            else:
                continue
        else:
            print("Incorrect Username or Password!")
            return False  
    
    def readConfig(self):
        with open("config.txt", "r") as file:
            users = []
            for line in file:
                users.append(line.rstrip("\n").split(","))
        return users      
    
    def readData(self, patient_id, event):
        with open("data.txt", "r") as file:
            records = []
            for line in file:
                records.append(line.rstrip("\n").split(","))
        if self.privilege in ["1","2","3"]:
            for record in records:
                if record[0] == patient_id:
                    print(record)
        if (event == "first"):
            for record in records:
                if record[0] == patient_id:
                    return True
            else:
                return False
    
    def writeData(self,patient_id,name,age,sex,mobile,illness,doctor,prescription,lab_test_prescription):
        with open("data.txt", "a") as file:
            print("Patient's Data: ")
            print("["+patient_id+","+name+","+age+","+sex+","+mobile+","+illness+","+prescription+","+lab_test_prescription+"]")
            file.write(patient_id+","+name+","+age+","+sex+","+mobile+","+illness+","+doctor+","+prescription+","+lab_test_prescription+"\n")
            print("Data Record Added Successully")
    
    def tasks(self):
        event = "read"
        if self.privilege == "0":
            print("Welcome to Admin Panel of ABC Hospital Management System")
            users = self.readConfig()
            for user in users:
                print(user[0],user[2])
        elif self.privilege == "1":
            print("Welcome to Doctor's Panel of ABC Hospital Management System")
            reason = input("Do You Wish to Add a New Patient:(yes/no) ")
            reason = reason.lower()
            if (reason == "yes"):
                patient_id = input("Enter Patient's Id: ")
                name = input("Enter Patient's Name: ")
                age = input("Enter Patient's Age: ")
                sex = input("Enter Patient's Sex: ")
                mobile = input("Enter Patient's Mobile: ")
                illness = input("Enter Patient's Illness: ")
                doctor = self.userid
                prescription = input("Enter Patient's Prescription: ")
                lab_test_prescription = input("Enter Patient's Lab Test Prescription: ")
                usertype = "patient"
                self.writeData(patient_id,name,age,sex,mobile,illness,doctor,prescription,lab_test_prescription)
                self.writeConfig(patient_id, mobile, patient_id,usertype,"3")
            elif (reason =="no"):
                print("Please Enter the Patient Id to View Data")
                patient_id = input("Enter Patient's Id: ")
                self.readData(patient_id,event)
        elif self.privilege == "2":
            print("Welcome to Nurse's Panel of ABC Hospital Management System")
            print("Please Enter the Patient Id to View Data")
            patient_id = input("Enter Patient's Id: ")
            self.readData(patient_id,event)
        elif self.privilege == "3":
            print("Welcome to Patient's Panel of ABC Hospital Management System")
            patient_id = self.userid
            self.readData(patient_id,event)
                
abc_hospital = ABChospital()
abc_hospital._init_()
abc_hospital.userInput()
