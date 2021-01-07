
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from plyer import audio

class AudioInterface(Screen):
    '''Root Widget.'''

    audio = ObjectProperty()
    time = NumericProperty(0)

    has_record = False

    def start_recording(self):
        state = self.audio.state
        if state == 'ready':
            self.audio.start()

        if state == 'recording':
            self.audio.stop()
            self.has_record = True

        self.update_labels()

    def play_recording(self):
        state = self.audio.state
        if state == 'playing':
            self.audio.stop()
        else:
            self.audio.play()

        self.update_labels()

    def update_labels(self):
        record_button = self.ids['record_button']
        play_button = self.ids['play_button']
        state_label = self.ids['state_label']

        state = self.audio.state
        state_label.text = 'AudioPlayer State: ' + state

        play_button.disabled = not self.has_record

        if state == 'ready':
            record_button.text = 'Start Recording'

        if state == 'recording':
            record_button.text = 'Press to Stop Recording'
            play_button.disabled = True

        if state == 'playing':
            play_button.text = 'Stop'
            record_button.disabled = True
        else:
            play_button.text = 'Press to play'
            record_button.disabled = False


class ProjectWindowManager(ScreenManager):
    pass
#the part where project will run parent class
    
class MyFirstPage(Screen):
    pass
#First page

class LoginStudent(Screen):
    pass
class LoginTeacher(Screen):
    pass
class QueryTeacher(Screen):
    pass
class ViewAttendance(Screen):
    pass
class TakeAttendance(Screen):
    pass
class LoginAdmin(Screen):
    pass
class AdminQuery(Screen):
    pass
class CreateAccountStudent(Screen):
    pass
class CreateAccountTeacher(Screen):
    pass
class CreateAccountTeacher(Screen):
    pass
class AudioInterface(Screen):
    pass
#fully kivy code and screenChanging code from down here
root_widget=Builder.load_string('''   
#:import audio_player plyer.audio                             
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
    AudioInterface:
<AudioInterface>:
    name:'recorder'
    audio: audio_player
    GridLayout:
        padding:50
        spacing:20
        opacity:0.6
        cols:1
        size:root.width,root.height
        Label:
            id: state_label
            size_hint_y: None
            #height: sp(40)
            text: 'AudioPlayer State: ' + str(root.audio.state)
        Label:
            id: location_label
            size_hint_y: None
            #height: sp(40)
            text: 'Recording Location: ' + str(root.audio.file_path)
        Button:
            id: record_button
            text: 'Start Recording'
            on_press: root.start_recording()
        Button:
            id: play_button
            text: 'Play'
            on_release: root.play_recording()
<MyFirstPage>:
    name: "home"
    GridLayout:
        opacity:0.6
        cols:1
        size:root.width,root.height
        padding:20
        spacing:15
        canvas.before:
            Color : 
                rgba: 0,1,1,1
            Rectangle:
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
#id's--> roll, s_class, s_sub
<LoginStudent>:
    name:"loginS"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            Color : 
                rgba: 0,1,1,1
            Rectangle:
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
                text:'5'
                values:('7', '8', '9', '10','11')
                pos_hint: {"x":0.26, "top":0.80}
                size_hint: 0.2,0.10
                id: s_class
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                size_hint: 0.5,0.12
                pos_hint: { "y":0.58,"right":0.4}
                text: "Subjects : "
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'English'
                values:('Algorithm', 'Data Structure', 'Python', 'Operating System','Economics')
                pos_hint: {"x":0.26, "top":0.70}
                size_hint: 0.2,0.10
                id: s_sub
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Button:
                pos_hint:{"x":0.61,"top":0.68}
                #left increase
                size_hint: 0.2, 0.1
                font_size: (root.width**2 + root.height**2) / 14**4
                text: "SUBMIT"
                on_release:root.manager.transition.direction = "left"
            Button:
                pos_hint:{"x":0.9,"top":1}
                #left increase
                size_hint: 0.10, 0.10
                font_size: (root.width**2 + root.height**2) / 14**4
                text: " HOME "
                on_release:
                    root.manager.transition.direction = "right"
                    app.root.current='home'
#Teachers Login id's----> t_uname,t_passw,otp
<LoginTeacher>:
    name:"loginT"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            Color : 
                rgba: 0,0,1,1
            Rectangle:
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
                pos_hint: {"x": 0.48 , "top":0.8}
                size_hint: 0.3,0.12
                id:t_uname
    
            Label:
                text:"Password: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.65}
                size_hint: 0.5, 0.12
    
            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                password: True
                pos_hint: {"x": 0.48, "top":0.65}
                size_hint: 0.3, 0.12
                id:t_passw
            Label:
                text:"Enter OTP: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.48}
                size_hint: 0.5, 0.12
            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                pos_hint: {"x": 0.48, "top":0.48}
                size_hint: 0.2, 0.10
                id:otp
            Button:
                pos_hint:{"x":0.85,"top":0.48}
                size_hint: 0.1,0.1
                font_size: (root.width**2 + root.height**2) / 13**4
                text: " OTP "
                #on_release: app.root.current='dataT'
                #on_press:root.save.otp_gen("priyanshudivergent@gmail.com")
            Button:
                pos_hint:{"x":0.55,"top":0.25}
                #left increase
                size_hint: 0.2, 0.1
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "SUBMIT"
                on_release:
                    root.manager.transition.direction = "left"
                    app.root.current='queryT'
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
            Color : 
                rgba: 0,1,0,1
            Rectangle:
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
#view attendance page id's--->class,sub,percentage
<ViewAttendance>:
    name:"view"
    FloatLayout:
        cols:1
        opacity:0.7
        canvas.before:
            Color : 
                rgba: 1,1,0,0.5
            Rectangle:
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
                text: "Class : "
                font_size: (root.width**2 + root.height**2) / 14**4

            TextInput:
                pos_hint: {"x":0.3, "top":0.8}
                size_hint: 0.4, 0.12
                id: class
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4

            Label:
                size_hint: 0.3,0.10
                pos_hint: {"x":0, "top":0.65}
                text: "Subject: "
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'Subjects'
                values:('Algorithm', 'Data Structure', 'Python', 'Operating System','Economics')
                pos_hint: {"x":0.3, "top":0.65}
                size_hint: 0.2,0.10
                id:sub
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                size_hint: 0.3,0.10
                pos_hint: {"x":0, "top":0.52}
                text: "Student %: "
                font_size: (root.width**2 + root.height**2) / 14**4
            Spinner:
                text:'<40%'
                values:('<40%', '40-60%', '61-75%', '76-90%','>90%')
                pos_hint: {"x":0.3, "top":0.52}
                size_hint: 0.2,0.10
                id:percentage
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Button:
                pos_hint:{"x":0.55,"top":0.65}
                size_hint: 0.2, 0.1
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "Generate"
                on_release:root.manager.transition.direction = "left"
#Teacher will start his attendance process here!!
<TakeAttendance>:
    name:"attendance"
    FloatLayout:
        cols:1
        opacity:0.7
        canvas.before:
            Color : 
                rgba: 0,1,1,0.7
            Rectangle:
                pos: root.pos
                size: root.size
        FloatLayout:
            size:root.width,root.height/2
            Label:
                text: "Attendance Portal!!!"
                size_hint: 0.8, 0.2
                pos_hint: {"x":0.1, "top":1}
                font_size: (root.width**2 + root.height**2) / 14**4
            Button:
                pos_hint:{"x":0.2,"top":0.80}
                size_hint: 0.4,0.12
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "Start Recording"
                #on_press:root.save.MyButton(btn)
                on_release:app.root.current='recorder'
            Button:
                pos_hint:{"x":0.2,"top":0.61}
                size_hint: 0.5, 0.12
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "save audio To drive"
                on_release:root.manager.transition.direction = "left"
            Button:
                pos_hint:{"x":0.2,"top":0.44}
                size_hint: 0.4,0.12
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "Process Attendance"
                on_release:root.manager.transition.direction = "left"
            TextInput:
                pos_hint: {"x":0.2, "top":0.28}
                size_hint: 0.5, 0.14
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
#Admin's login id's-->a_uname, a_passw, otp
<LoginAdmin>:
    name:"loginA"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            Color : 
                rgba: 0,0,0,0.6
            Rectangle:
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
                pos_hint: {"x": 0.48 , "top":0.8}
                size_hint: 0.3,0.12
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
                pos_hint: {"x": 0.48, "top":0.65}
                size_hint: 0.3, 0.12
                id:a_passw
            Label:
                text:"Enter OTP: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.48}
                size_hint: 0.5, 0.12
            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                pos_hint: {"x": 0.48, "top":0.48}
                size_hint: 0.2, 0.10
                id:otp
            Button:
                pos_hint:{"x":0.85,"top":0.48}
                size_hint: 0.1,0.1
                font_size: (root.width**2 + root.height**2) / 13**4
                text: " OTP "
                #on_release: app.root.current='dataT'
                #on_press:root.save.otp_gen("priyanshudivergent@gmail.com")
            Button:
                pos_hint:{"x":0.55,"top":0.25}
                size_hint: 0.2, 0.1
                font_size: (root.width**2 + root.height**2) / 17**4
                text: "SUBMIT"
                on_release:
                    root.manager.transition.direction = "left"
                    app.root.current='queryA'
<AdminQuery>:
    name:"queryA"
    GridLayout:
        opacity:0.6
        cols:1
        size:root.width,root.height
        padding:20
        spacing:15
        canvas.before:
            Color : 
                rgba: 1,0,1,0.7
            Rectangle:
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
#Students Account Creation id's-->s_uame, roll, class
<CreateAccountStudent>:
    name:"createS"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            Color : 
                rgba: 0,0,0,0.6
            Rectangle:
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
                pos_hint: {"x": 0.48 , "top":0.8}
                size_hint: 0.3,0.12
                id:s_uname

            Label:
                text:"Roll No: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.65}
                size_hint: 0.5, 0.12
    
            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                password: True
                pos_hint: {"x": 0.48, "top":0.65}
                size_hint: 0.3, 0.12
                id:roll
            Label:
                text:"Class: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.48}
                size_hint: 0.5, 0.12
            TextInput:
                font_size: (root.width**2 + root.height**2) / 13**4
                multiline: False
                pos_hint: {"x": 0.48, "top":0.48}
                size_hint: 0.2, 0.10
                id:s_class
            Button:
                pos_hint:{"x":0.85,"top":0.48}
                size_hint: 0.1,0.1
                font_size: (root.width**2 + root.height**2) / 13**4
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
#Teachers Account created id's-->t_uname, t_sub ,t_class
<CreateAccountTeacher>: 
    name:"createT"
    FloatLayout:
        opacity:0.6
        cols:1
        canvas.before:
            Color : 
                rgba: 1,0,0,0.6
            Rectangle:
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
                pos_hint: {"x": 0.48 , "top":0.8}
                size_hint: 0.3,0.12
                id:t_uname

            Label:
                text:"Subject: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.65}
                size_hint: 0.5, 0.12
    
            Spinner:
                text:'Subjects'
                values:('Algorithm', 'Data Structure', 'Python', 'Operating System','Economics')
                pos_hint: {"x":0.48, "top":0.65}
                size_hint: 0.3,0.12
                id:t_sub
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Label:
                text:"Class: "
                font_size: (root.width**2 + root.height**2) / 13**4
                pos_hint: {"x":0, "top":0.48}
                size_hint: 0.5, 0.12
            Spinner:
                text:'5'
                values:('7', '8', '9', '10','11')
                pos_hint: {"x":0.48, "top":0.48}
                size_hint: 0.2,0.10
                id: t_class
                multiline: False
                font_size: (root.width**2 + root.height**2) / 14**4
            Button:
                pos_hint:{"x":0.85,"top":0.48}
                size_hint: 0.1,0.1
                font_size: (root.width**2 + root.height**2) / 13**4
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
                                  
                                ''')
class AttedanceApp(App):
     def build(self):
        return root_widget
if __name__ == "__main__":
    AttedanceApp().run()