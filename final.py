import smtplib
from random import randint
import gspread
from gspread.utils import rowcol_to_a1
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from oauth2client.service_account import ServiceAccountCredentials
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import imutils
import time
import cv2
import datetime



# variables
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

date = datetime.date.today()
print(date)
creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
client = gspread.authorize(creds)
x = '5'
Attendance_list = []
Attendance_list2 = []


class Record:
    def scanner(self, date):
            # construct the argument parser and parse the arguments
            ap = argparse.ArgumentParser()
            ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                            help="path to output CSV file containing barcodes")
            args = vars(ap.parse_args())

            # initialize the video stream and allow the camera sensor to warm up
            print("[INFO] starting video stream...")
            vs = VideoStream(src=0).start()
            # vs = VideoStream(usePiCamera=True).start()
            time.sleep(2.0)

            # open the output CSV file for writing and initialize the set of
            # barcodes found thus far
            csv = open(args["output"], "w")
            found = set()

            # loop over the frames from the video stream
            while True:
                # grab the frame from the threaded video stream and resize it to
                # have a maximum width of 400 pixels
                frame = vs.read()
                frame = imutils.resize(frame, width=400)

                # find the barcodes in the frame and decode each of the barcodes
                barcodes = pyzbar.decode(frame)
                # loop over the detected barcodes
                for barcode in barcodes:
                    # extract the bounding box location of the barcode and draw
                    # the bounding box surrounding the barcode on the image
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    # the barcode data is a bytes object so if we want to draw it
                    # on our output image we need to convert it to a string first
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    if str(barcode.data) not in Attendance_list:
                        Attendance_list.append(str(barcode.data))
                        print('\a')
                        print(Attendance_list)
                    # draw the barcode data and barcode type on the image
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    # if the barcode text is currently not in our CSV file, write
                    # the timestamp + barcode to disk and update the set
                    if barcodeData not in found:
                        csv.write("{},{}\n".format(datetime.datetime.now(),
                                                   barcodeData))
                        csv.flush()
                        found.add(barcodeData)

                # show the output frame
                cv2.imshow("Barcode Scanner", frame)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key ==ord('q'):
                    break

            # close the output CSV file do a bit of cleanup
            print("[INFO] cleaning up...")
            csv.close()
            cv2.destroyAllWindows()
            vs.stop()

class Recognition:
    def recognize(self, date):
        for i in range(len(Attendance_list)):
            x = Attendance_list[i]
            Attendance_list[i] = x[2:-1]

        print(Attendance_list)
        pass



class Training:
    def otp_gen(self, email1):
        otp = ""
        for i in range(4):
            otp += str(randint(0, 9))
        content = "your otp for smart attendance is " + otp
        email = smtplib.SMTP('smtp.gmail.com', 587)
        email.starttls()
        email.login("smartattendance01@gmail.com", "acmhackathon2020")
        message = "From: smartattendance01@gmail.com \nTo: " + email1 + "\nSubject: Login Otp For smart attendance.\n"
        content = message + content
        email.sendmail("mrishabh781@gmail.com", email1, content)
        print("mail sent")
        email.quit()


class Sheet_operation:
    # returning the proper sheet to hit later.
    def get_sheet_name(self, year, subject):
        # print(year)
        # print(subject)
        sheet_name_list = ["IT 2nd Year", "IT 3rd Year", "IT 4th Year"]
        sheet_number_list = {'Algorithms': '0', 'Data Structure': '1', 'Maths': '2'}
        # print(sheet_number_list[subject])
        return sheet_name_list[int(year[0]) - 2], sheet_number_list[str(subject)]

    # getting data from the rqueired sheet and then formating if required
    def get_data(self, sheet, roll=0):
        data = sheet.get_all_records()
        if roll == 0:
            data = sheet.get_all_records()
            for i in data:
                print(i)

        else:
            data = data[roll - 1]
            for i in data:
                print(i)

        return data

    # finally generating the final attendance details with absent/present list as well as total number of classes and all
    def get_attendance_st(self, roll, year1, sub):
        x = 9
        print(year1)
        print(sub)
        sheet_info = Sheet_operation.get_sheet_name(self, year1, sub)
        print(sheet_info)
        s_name = sheet_info[0]
        s_number = sheet_info[1]
        # print(s_name)
        # print(s_number)
        # print(roll)
        # accessing data base(sheets)
        # client = gspread.authorize(creds)
        sheet = client.open(s_name).get_worksheet(int(s_number))  # seting up the values to fetch the sheet
        data = Sheet_operation.get_data(self, sheet, int(roll))
        present = []
        absent = []
        for i in data:
            print(i)

        Total_class = len(data) - 2
        Class_attended = 0
        print(Total_class)
        student_rec = data
        print(student_rec)
        flag = 0
        # generating final list
        for i in student_rec:
            flag += 1
            if flag > 3:
                if student_rec[i] != 0:
                    present.append(i)
                else:
                    absent.append(i)
                    Class_attended += 1
        print(present, absent, Class_attended)
        # calculating percentage
        try:
            percentage = (Class_attended / Total_class) * 100
            print(str(percentage) + ' %')
        except ZeroDivisionError:
            print('No class taken yet')
        print('done')
        # event = Clock.schedule_interval(AttedanceApp().run(), 1 / 30.)

    def get_attendance_tr(self, year, subject):
        sheet_info = Sheet_operation.get_sheet_name(self, year, subject)
        print(sheet_info)
        s_name = sheet_info[0]
        s_number = sheet_info[1]
        sheet = client.open(s_name).get_worksheet(int(s_number))  # seting up the values to fetch the sheet
        data = Sheet_operation.get_data(self, sheet)
        #print(data)

    def update_attendance(self, date, subject, year):
        sheet_info = Sheet_operation.get_sheet_name(self, year, subject)
        date =str(datetime.date.today())
        s_name = sheet_info[0]
        s_number = sheet_info[1]
        sheet = client.open(s_name).get_worksheet(int(s_number))
        data = sheet.get_all_records()
        length = len(data[0])
        last_roll = data[-1]['Roll No.']
        final_attendance = [date]
        for i in data:
            print(i)

        for i in data:
            if str(i["Device_Id"]) in Attendance_list:
                final_attendance.append('1')
            else:
                final_attendance.append('0')
        # updating attendance in sheet

        h = rowcol_to_a1(1, length + 1) + ':' + rowcol_to_a1(last_roll + 1, length + 1)
        print(h)
        cell_list = sheet.range(h)
        # print(cell_list)
        for cell, atend in zip(cell_list, final_attendance):
            cell.value = atend
            sheet.update_cells(cell_list)
        print("updated")



class ProjectWindowManager(ScreenManager):
    pass


# the part where project will run parent class

class MyFirstPage(Screen):
    pass


# First page

class LoginStudent(Screen):
    info = Sheet_operation()
    h = StringProperty()


class LoginTeacher(Screen):
    save = Training()


class QueryTeacher(Screen):
    pass


class ViewAttendance(Screen):
    info_tr = Sheet_operation()


class TakeAttendance(Screen):
    press = Record()
    push = Recognition()
    update = Sheet_operation()


class LoginAdmin(Screen):
    pass


class AdminQuery(Screen):
    save = Training()


class CreateAccountStudent(Screen):
    pass


class CreateAccountTeacher(Screen):
    pass


# fully kivy code and screenChanging code from down here
root_widget = Builder.load_string(''' 
#:import QRCodeWidget kivy_garden.qrcode                  
ProjectWindowManager:
    MyFirstPage:
    LoginStudent:
    LoginTeacher:
    QueryTeacher:
    ViewAttendance:
    TakeAttendance:
    LoginAdmin:
    AdminQuery:
    CreateAccountStudent:
    CreateAccountTeacher:
<MyFirstPage>:
    name: "home"
    GridLayout:
        opacity:0.6
        cols:1
        size:root.width,root.height
        padding:20
        spacing:15
        canvas.before:
            #Color : 
                #rgba: 0,1,1,1
            Rectangle:
                source: "13th.jpg"
                pos: root.pos
                size: root.size    
        Label:
            text:"ATTENDANCE PORTAL"
            font_size: (root.width**2 + root.height**2) / 13**4 
        Button:
            text:"Student"
            on_release:app.root.current="loginS"
        Button:
            text:"Faculty"
            on_release:app.root.current="loginT"
        Button:
            text:"Admin"
            on_release:app.root.current="loginA"
            #on_press:root.save.otp_gen("smartattendance01@gmail.com")
#Student login page starts here
#id's--> roll, s_class,s_year, s_sub
<LoginStudent>:
    
    atn :attend1
    name:"loginS"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            #Color : 
                #rgba: 0,1,1,1
            Rectangle:
                source:"13th.jpg"
                pos: root.pos
                size: root.size
        FloatLayout:
            size:root.width,root.height
            Label:
                text:"Welcome Student"
                size_hint: 0.8, 0.2
                pos_hint: {"x":0,"top":1.07}
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                size_hint: 0.5,0.12
                pos_hint: { "y":0.81,"right":0.4}
                text: "Roll No : "
                font_size: (root.width**2 + root.height**2) / 14**4

            TextInput:
                pos_hint: {"x":0.26, "top":0.9}
                size_hint: 0.3, 0.06
                id: roll
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                size_hint: 0.5,0.12
                pos_hint: { "y":0.69,"right":0.4}
                text: "Class : "
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'IT'
                values:('IT', 'CSE', 'ECE')
                pos_hint: {"x":0.26, "top":0.80}
                size_hint: 0.2,0.10
                id: s_class
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            #Label:
            #    size_hint: 0.5,0.12
            #    pos_hint: { "y":0.58,"right":0.4}
             #   text: "Year : "
             #   font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'2nd'
                values:('2nd', '3rd', '4th')
                pos_hint: {"x":0.46, "top":0.80}
                size_hint: 0.2,0.10
                id: s_year
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                size_hint: 0.5,0.12
                pos_hint: { "y":0.5,"right":0.4}
                text: "Subjects : "
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'Algorithms'
                values:('Algorithm', 'Data Structure', 'Maths')
                pos_hint: {"x":0.26, "top":0.60}
                size_hint: 0.2,0.10
                id: s_sub
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Button:
                pos_hint:{"x":0.20,"top":0.3}
                #left increase
                size_hint: 0.12, 0.1
                font_size: (root.width**2 + root.height**2) / 14**4
                text: "SUBMIT"
                on_press: 
                    root.info.get_attendance_st(roll.text,s_year.text,s_sub.text)
                on_release:root.manager.transition.direction = "left"
            Button:
                pos_hint:{"x":0.4,"top":0.30}
                #left increase
                size_hint: 0.12,0.10
                font_size: (root.width**2 + root.height**2) / 14**4
                text: " HOME "
                on_release:
                    root.manager.transition.direction = "right"
                    app.root.current='home'
                    
            Label:
                id: attend1
                pos_hint: {"x":0, "top":0.50}
                size_hint: 1, 0.5
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
                text: root.h
                
            
#Teachers Login id's----> t_uname,t_passw,otp
<LoginTeacher>:
    name:"loginT"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            #Color : 
                #rgba: 0,0,1,1
            Rectangle:
                source: "13th.jpg"
                pos: root.pos
                size: root.size
        FloatLayout:
            size:root.width,root.height
            Label:
                text:"Teacher's Portal"
                size_hint: 0.8, 0.7
                pos_hint: {"x":0,"top":1.26}
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                text:"UserName: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.8}
                size_hint: 0.5, 0.12

            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                pos_hint: {"x": 0.48 , "top":0.76}
                size_hint: 0.4,0.06
                id:t_uname

            Label:
                text:"Password: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.61}
                size_hint: 0.5, 0.12

            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                password: True
                pos_hint: {"x": 0.48, "top":0.59}
                size_hint: 0.4, 0.06
                id:t_passw
            Label:
                text:"Enter OTP: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.46}
                size_hint: 0.5, 0.12
            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                pos_hint: {"x": 0.48, "top":0.44}
                size_hint: 0.3,0.08
                id:otp
            Button:
                pos_hint:{"x":0.85,"top":0.48}
                size_hint: 0.15,0.12
                font_size: (root.width**2 + root.height**2) / 13**4
                text: " OTP "
                on_press:root.save.otp_gen("mrishabh781@gmail.com")
            Button:
                pos_hint:{"x":0.55,"top":0.25}
                #left increase
                size_hint: 0.2, 0.1
                font_size: (root.width**2 + root.height**2) / 14**4
                text: "SUBMIT"
                on_release:
                    root.manager.transition.direction = "left"
                    app.root.current='queryT'
            Button:
                pos_hint:{"x":0.76,"top":0.25}
                #left increase
                size_hint: 0.12, 0.10
                font_size: (root.width**2 + root.height**2) / 14**4
                text: " HOME "
                on_release:
                    root.manager.transition.direction = "up"
                    app.root.current='home'
#Teacher's After Login Query page
<QueryTeacher>:
    name:"queryT"
    GridLayout:
        opacity:0.6
        cols:1
        size:root.width,root.height
        padding:20
        spacing:15
        canvas.before:
            #Color : 
                #rgba: 0,1,0,1
            Rectangle:
                source: "13th.jpg"
                pos: root.pos
                size: root.size    
        Label:
            text:"Welcome Teacher"
            font_size: (root.width**2 + root.height**2) / 13**4 
        Button:
            text:"View Attendance"
            on_release:app.root.current="view"
        Button:
            text:"Take Attendance"
            on_release:app.root.current="attendance"
#view attendance page id's--->s_class,s_year,s_sub,show,show_percentage
<ViewAttendance>:
    name:"view"
    FloatLayout:
        cols:1
        opacity:0.7
        canvas.before:
            #Color : 
                #rgba: 1,1,0,0.5
            Rectangle:
                source: "13th.jpg"
                pos: root.pos
                size: root.size
        FloatLayout:
            size:root.width,root.height/2
            Label:
                text: "View Attendance Portal!!!"
                size_hint: 0.8, 0.2
                pos_hint: {"x":0.1, "top":1}
                font_size: (root.width**2 + root.height**2) / 14**4

            Label:
                size_hint: 0.3,0.10
                pos_hint: {"x":0, "top":0.8}
                text: "Branch : "
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'IT'
                values:('IT', 'CSE', 'ECE')
                pos_hint: {"x":0.3, "top":0.8}
                size_hint: 0.2,0.10
                id:s_class
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'2nd'
                values:('2nd', '3rd', '4th')
                pos_hint: {"x":0.53, "top":0.8}
                size_hint: 0.2,0.10
                id: s_year
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4

            Label:
                size_hint: 0.3,0.10
                pos_hint: {"x":0, "top":0.65}
                text: "Subject: "
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'Algorithms'
                values:('Algorithms', 'Data Structure', 'Maths')
                pos_hint: {"x":0.3, "top":0.65}
                size_hint: 0.2,0.10
                id:s_sub
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4

            Label:
                size_hint: 0.3,0.10
                pos_hint: {"x":0, "top":0.52}
                text: "Student : "
                font_size: (root.width**2 + root.height**2) / 14**4
            Button:
                pos_hint:{"x":0.3,"top":0.52}
                size_hint: 0.2, 0.10
                font_size: (root.width**2 + root.height**2) / 14**4
                text: "View All"
                id:show
                on_release:
                    root.manager.transition.direction = "left"
                    root.info_tr.get_attendance_tr(s_year.text,s_sub.text)
            Spinner:
                text:'View %'
                values:('<40%', '40-60%', '61-75%', '76-90%','>90%')
                pos_hint: {"x":0.54, "top":0.52}
                size_hint: 0.2,0.10
                id:show_percentage
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            #Button:
                #pos_hint:{"x":0.1,"top":0.37}
                #size_hint: 0.2, 0.1
                #font_size: (root.width**2 + root.height**2) / 14**4
                #text: "Generate"
                #on_release:root.manager.transition.direction = "left"
            Button:
                pos_hint:{"x":0.31,"top":0.37}
                #left increase
                size_hint: 0.12, 0.10
                font_size: (root.width**2 + root.height**2) / 14**4
                text: " HOME "
                on_release:
                    root.manager.transition.direction = "down"
                    app.root.current='home'
#Teacher will start his attendance process here!!
#id's--->s_class ,s_year(only to check)
<TakeAttendance>:
    name:"attendance"
    FloatLayout:
        cols:1
        opacity:0.7
        canvas.before:
            #Color : 
                #rgba: 0,1,1,0.7
            Rectangle:
                source: "13th.jpg"
                pos: root.pos
                size: root.size
        FloatLayout:
            size:root.width,root.height/2
            Label:
                text: "Attendance Portal!!!"
                size_hint: 0.8, 0.2
                pos_hint: {"x":0.1, "top":1}
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'IT'
                values:('IT', 'CSE', 'ECE')
                pos_hint: {"x":0.04, "top":0.80}
                size_hint: 0.2,0.10
                id: s_class
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'2nd'
                values:('2nd', '3rd', '4th')
                pos_hint: {"x":0.28, "top":0.80}
                size_hint: 0.2,0.10
                id: s_year
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'Algorithms'
                values:('Algorithms', 'Data Structure', 'Maths')
                pos_hint: {"x":0.52, "top":0.80}
                size_hint: 0.2,0.10
                id:t_sub
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            TextInput:
                id: t_date
                hint_text : '16-02-20'
                pos_hint:{"x":0.76,"top":0.80}
                size_hint: 0.2,0.10
                font_size: (root.width**2 + root.height**2) / 14**4
                
            Button:
                pos_hint:{"x":0.04,"top":0.61}
                size_hint: 0.4,0.12
                font_size: (root.width**2 + root.height**2) / 14**4
                text: "Start Scanning"
                on_press:root.press.scanner(t_date.text)
           # Button:
            #    pos_hint:{"x":0.5,"top":0.61}
             #   size_hint: 0.4, 0.12
              #on_press: root.press.var_update()
              #  on_release:root.manager.transition.direction = "left"
                
            Button:
                pos_hint:{"x":0.52,"top":0.61}
                size_hint: 0.4,0.12
                font_size: (root.width**2 + root.height**2) / 14**4
                text: "Process Attendance"
                on_release:root.manager.transition.direction = "left"
                on_press:root.push.recognize(t_date.text)
                
           # Label:
           #     pos_hint:{"x":0.23,"top":0.33}
           #     size_hint: 0.4,0.12
           #     font_size: (root.width**2 + root.height**2) / 14**4
           #     text: "List of absent Students:"

            #TextInput:
            #    pos_hint: {"x":0.2, "top":0.20}
               # text : str(root.push.recognise)
            #    size_hint: 0.5, 0.14
            #    multiline: False
            #    font_size: (root.width**2 + root.height**2) / 14**4
                #text:print(root.push.recognize())
            Button:
                pos_hint:{"x":0.52,"top":.4}
                #left increase
                size_hint: 0.4,0.12
                font_size: (root.width**2 + root.height**2) / 14**4
                text: " HOME "
                on_release:
                    root.manager.transition.direction = "left"
                    app.root.current='home'
            Button:
                pos_hint:{"x":0.04,"top":0.4}
                size_hint: 0.4,0.12
                font_size: (root.width**2 + root.height**2) / 14**4
                text: "Submit"
                on_release:root.manager.transition.direction = "down"
                on_press: root.update.update_attendance(t_date.text,t_sub.text,s_year.text)
#Admin's login id's-->a_uname, a_passw, otp
<LoginAdmin>:
    name:"loginA"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            #Color : 
                #rgba: 1,0,0,0.6
            Rectangle:
                source: "13th.jpg"
                pos: root.pos
                size: root.size
        FloatLayout:
            size:root.width,root.height
            Label:
                text:"Welcome Login"
                size_hint: 0.8, 0.7
                pos_hint: {"x":0,"top":1.26}
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                text:"UserName: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.8}
                size_hint: 0.5, 0.12

            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                pos_hint: {"x": 0.44 , "top":0.77}
                size_hint: 0.3,0.06
                id:a_uname

            Label:
                text:"Password: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.65}
                size_hint: 0.5, 0.12

            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                password: True
                pos_hint: {"x": 0.44, "top":0.62}
                size_hint: 0.3, 0.06
                id:a_passw
            Label:
                text:"Enter OTP: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.48}
                size_hint: 0.5, 0.12
            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                pos_hint: {"x": 0.44, "top":0.46}
                size_hint: 0.2, 0.08
                id:otp
            Button:
                pos_hint:{"x":0.85,"top":0.48}
                size_hint: 0.1,0.1
                font_size: (root.width**2 + root.height**2) / 13**4
                text: " OTP "
                on_press:root.save.otp_gen("priyanshudivergent@gmail.com")
            Button:
                pos_hint:{"x":0.48,"top":0.25}
                size_hint: 0.2, 0.1
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "SUBMIT"
                on_release:
                    root.manager.transition.direction = "left"
                    app.root.current='queryA'
            Button:
                pos_hint:{"x":0.74,"top":0.25}
                #left increase
                size_hint: 0.12, 0.10
                font_size: (root.width**2 + root.height**2) / 14**4
                text: " HOME "
                on_release:
                    root.manager.transition.direction = "left"
                    app.root.current='home'
<AdminQuery>:
    name:"queryA"
    GridLayout:
        opacity:0.6
        cols:1
        size:root.width,root.height
        padding:20
        spacing:15
        canvas.before:
            #Color : 
                #rgba: 1,0,1,0.7
            Rectangle:
                source: "13th.jpg"
                pos: root.pos
                size: root.size    
        Label:
            text:"Admin PORTAL"
            font_size: (root.width**2 + root.height**2) / 13**4 
        Button:
            text:"Create Student Id"
            on_release:app.root.current="createS"
        Button:
            text:"Create Teacher's Id"
            on_release:app.root.current="createT"     
        Button:
            text:"Watch Students Attendance"
            on_release:app.root.current="view"
#Students Account Creation id's--> s_roll,s_class,s_year
<CreateAccountStudent>:
    name:"createS"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            #Color : 
                #rgba: 1,1,0,0.6
            Rectangle:
                source: "21th.jpg"
                pos: root.pos
                size: root.size
        FloatLayout:
            size:root.width,root.height
            Label:
                text:"Create a new Id here!!"
                size_hint: 0.8, 0.7
                pos_hint: {"x":0,"top":1.26}
                font_size: (root.width**2 + root.height**2) / 14**4
            #Label:
               # text:"Name: "
                #font_size: (root.width**2 + root.height**2) / 13**4
                #pos_hint: {"x":0, "top":0.8}
                #size_hint: 0.5, 0.12

            #TextInput:
                #font_size: (root.width**2 + root.height**2) / 13**4
                #multiline: False
                #pos_hint: {"x": 0.44 , "top":0.78}
                #size_hint: 0.3,0.06
                #id:s_name

            Label:
                text:"Roll No: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.65}
                size_hint: 0.5, 0.12

            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                password: True
                pos_hint: {"x": 0.44, "top":0.62}
                size_hint: 0.3, 0.06
                id:s_roll
            Label:
                text:"Class: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.48}
                size_hint: 0.5, 0.12
            Spinner:
                text:'IT'
                values:('IT', 'CSE', 'ECE')
                pos_hint: {"x":0.42, "top":0.48}
                size_hint: 0.2,0.10
                id:s_sub
                pos_hint: {"x": 0.38, "top":0.48}
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'2nd'
                values:('2nd', '3rd', '4th')
                pos_hint: {"x":0.58, "top":0.48}
                size_hint: 0.2,0.10
                id:s_year
                pos_hint: {"x": 0.44, "top":0.48}
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Button:
                pos_hint:{"x":0.82,"top":0.25}
                size_hint: 0.12,0.10
                font_size: (root.width**2 + root.height**2) / 14**4
                text: " Home "
                on_release: app.root.current='home'

            Button:
                pos_hint:{"x":0.55,"top":0.25}
                size_hint: 0.2, 0.1
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "SUBMIT"
                on_release:
                    root.manager.transition.direction = "left"
                    app.root.current='queryA'
#Teachers Account created id's-->t_uname, t_sub ,t_class,t_year
<CreateAccountTeacher>: 
    name:"createT"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            #Color : 
                #rgba: 1,0,0,0.6
            Rectangle:
                source: "22nd.jpg"
                pos: root.pos
                size: root.size
        FloatLayout:
            size:root.width,root.height
            Label:
                text:"Create a new Id here!!"
                size_hint: 0.8, 0.7
                pos_hint: {"x":0,"top":1.26}
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                text:"Name: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.8}
                size_hint: 0.5, 0.12

            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                pos_hint: {"x": 0.44 , "top":0.76}
                size_hint: 0.3,0.06
                id:t_uname

            Label:
                text:"Subject: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.65}
                size_hint: 0.5, 0.12

            Spinner:
                text:'Algorithm'
                values:('Algorithm', 'Data Structure', 'Maths')
                pos_hint: {"x":0.44, "top":0.62}
                size_hint: 0.3,0.12
                id:t_sub
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                text:"Class: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.46}
                size_hint: 0.5, 0.12
            Spinner:
                text:'IT'
                values:('IT', 'CSE', 'ECE')
                pos_hint: {"x":0.36, "top":0.45}
                size_hint: 0.2,0.10
                id: t_class
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'2nd'
                values:('2nd', '3rd', '4th')
                pos_hint: {"x":0.58, "top":0.45}
                size_hint: 0.2,0.10
                id:t_year
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Button:
                pos_hint:{"x":0.85,"top":0.25}
                size_hint: 0.12,0.10
                font_size: (root.width**2 + root.height**2) / 13**4
                text: " Home "
                on_release: 
                    app.root.current='home'
                    root.manager.transition.direction = "down"

            Button:
                pos_hint:{"x":0.55,"top":0.25}
                size_hint: 0.2, 0.1
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "SUBMIT"
                on_release:
                    root.manager.transition.direction = "left"
                    app.root.current='queryA'


                                ''')


class AttedanceApp(App):
    def build(self):
        return root_widget

    def on_pause(self):
        return True


if __name__ == "__main__":
    AttedanceApp().run()
