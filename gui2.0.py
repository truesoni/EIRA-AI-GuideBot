'''
Eira - AN AI GuideBot (GUI)
'''
import tkinter
import customtkinter
import os
import sqlite3
from PIL import Image
from bot_utils import *
import time



quit_txt =["thank you", "no thank you", "thanks", "no thanks", "bye", "thank you for you service", "have a nice day", "see ya", "see you", "shut up"]

'''Graphical Variables'''


'''System Variables'''
geometry = "1400x720"
title = "EIRA - An AI GuideBot"
CENTER = tkinter.CENTER
bot = "EIRA"



'''Files'''
json_file = "D:\GLOBOT\database.json"
red_blip = "red_blip.png"
green_blip = "green_blip.png"
settings_icon_black = "settings_b.png"
settings_icon_white = "settings_w.png"
back_btn_ico_w = "back_w.png"
back_btn_ico_b = "back_b.png"

eira_logo = "eira_logo2.png"
college_logo = "college_logo.png"
lock_icon_black = "lock_b.png"
lock_icon_white = "lock_w.png"
add_white = "add_w.png"
add_black = "add_b.png"
delete_white = "delete_w.png"
delete_black = "delete_b.png"
home_white = "home_w.png"
home_black = "home_b.png"
robot_white = "robot_w.png"
robot_black = "robot_b.png"
sys_white = "system_w.png"
sys_black = "system_b.png"
key_white = "key_w.png"
key_black = "key_b.png"
transparent = "transparent.png"
train_black = "train_b.png"
train_white = "train_w.png"
start_white = "start_w.png"
start_black = "start_b.png"
quit_black = "quit_b.png"
quit_white = "quit_w.png"
day_img = "day.png"
night_img = "night.png"

shubham = "shubham.png"
shiv = "shiv.png"
shobhit = "shobhit.png"
tapasvi = "tapasvi.png"
shranjal = "shranjal.png"
sangeet = "sangeet.png"


eye_open_w = 'eye_open_w.png'
eye_open_b = 'eye_open_b.png'
eye_closed_b = 'eye_closed_b.png'
eye_closed_w = 'eye_closed_w.png'

texture = "black_texture.png"
texture2 = "black_texture_2.png"

folder_name = "assets"

'''Colors'''
RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"
WHITE = "#FFFFFF"
BLACK = "#000000"
LIGHT_GREY = "#5B6068"
DARK_GREY = "#222222"
AQUA = "#00FFFF"
LIGHT_BLUE = "#1da2dc"
LIGHT_GREEN = "#32e379"
Color_theme = LIGHT_BLUE




class Mydb:
    '''
    Database class
    '''

    def __init__(self) -> None:
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def load_data(self, tag: str) -> str:
        self.cursor.execute(f"""
        SELECT * from data_table 
        WHERE tag = '{tag}';
        """)

        res = self.cursor.fetchall()
        try:
            return res[0][2]
        except IndexError:
            return "No such tag"

    def load_data_system(self, tag: str) -> str:
        self.cursor.execute(f"""
        SELECT * from system_table 
        WHERE tag = '{tag}';
        """)

        res = self.cursor.fetchall()
        try:
            return res[0][1]
        except IndexError:
            return "No such tag"

    def insert_data(self, tag: str, pattern: str, response: str) -> None:
        self.cursor.execute(f"""
        INSERT INTO data_table VALUES 
        ('{tag}', '{pattern}', '{response}');
        """)

        self.connection.commit()

    def delete_data(self, tag: str) -> None:
        self.cursor.execute(f"""
        DELETE from data_table 
        WHERE tag = '{tag}';
        """)
        self.connection.commit()
    
    def update_data2(self, tag : str, pattern : str, response : str) ->None :
        self.cursor.execute(f"""
        UPDATE data_table 
        SET patterns = '{pattern}'
        WHERE tag = '{tag}';
        """)
        self.cursor.execute(f"""
        UPDATE data_table 
        SET responses = '{response}'
        WHERE tag = '{tag}';
        """)

        self.connection.commit()

    def set_attr(self, tag: str, value: str) -> None:
        self.cursor.execute(f"""
        INSERT INTO system_table VALUES 
        ('{tag}', '{value}');
        """)

        self.connection.commit()

    def get_attr(self, attr: str) -> str:
        self.cursor.execute(f"""
        SELECT value from system_table
        WHERE tag = '{attr}'
        """)
        l = self.cursor.fetchall()
        try:
            s = list(l[0])[0]

        except IndexError:
            return ''
        return s

    def update_data(self, tag: str, value: str) -> None:
        self.cursor.execute(f"""
        UPDATE system_table 
        SET value = '{value}'
        WHERE tag = '{tag}'
        """)
        self.connection.commit()

    def get_tags(self) -> list:
        self.cursor.execute("""
        SELECT tag from data_table;
        """)

        l = self.cursor.fetchall()
        res = []
        try:
            for li in l:
                li = list(li)
                res.append(li[0])
        except IndexError:
            pass
        return res

    def get_responses(self, tag: str) -> list:
        self.cursor.execute(f"""
        SELECT responses from data_table
        WHERE tag = '{tag}'
        """)
        l = self.cursor.fetchall()
        try:
            s = list(l[0])[0]
            res = s.split('&')
            res.reverse()
            res.pop()
        except IndexError:
            return []
        return res

    def get_patterns(self, tag: str) -> list:
        self.cursor.execute(f"""
        SELECT patterns from data_table
        WHERE tag = '{tag}'
        """)
        l = self.cursor.fetchall()
        try:
            s = list(l[0])[0]
            res = s.split('&')
            res.reverse()
            res.pop()
        except IndexError:
            return []
        return res

class App:
    '''
    Main GUI class

    '''

    def __init__(self) -> None:
        '''
        Init Constructor

        '''
        self.window = customtkinter.CTk()
        self.window.geometry(geometry)
        self.window.title(title)

        self.Color_theme  = "blue"
        self.curtheme = 'dark' 

        self.about_string = f"""Welcome to BGIOEM! EIRA is designed to help students, faculty, and staff get the information they need quickly and easily. Whether you're looking for information on courses, events, or campus services, EIRA is here to help.

                        EIRA is powered by advanced AI technology that allows it to understand natural language queries and provide accurate, relevant answers in real-time. It's like having a personal assistant at your fingertips, ready to help you with whatever you need.

                        EIRA is constantly learning and improving, thanks to the power of machine learning algorithms. This means that the more you use it, the better it gets at understanding your queries and providing the information you need.

                        At BGIOEM, we're committed to using the latest technology to enhance the student experience, and EIRA is just one example of this. We're proud to offer this innovative tool to our community and we hope you find it helpful. If you have any feedback or suggestions for how we can improve our chatbot, please don't hesitate to let us know.

                        Thank you!"""


        customtkinter.set_appearance_mode(self.curtheme)
        customtkinter.set_default_color_theme(self.Color_theme)


        '''IMAGE LOADINGS'''
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), folder_name)
        self.red_blip_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, red_blip)), size=(20, 20))
        self.green_blip_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, green_blip)), size=(20, 20))
        self.settings_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(
            image_path, settings_icon_black)), dark_image=Image.open(os.path.join(image_path, settings_icon_white)), size=(25, 25))
        self.back_btn_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, back_btn_ico_w)), light_image=Image.open(os.path.join(image_path, back_btn_ico_b)), size=(25, 25))
        self.eira_logo_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, eira_logo)), size=(400, 140))
        self.lock_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, lock_icon_white)), light_image=Image.open(os.path.join(image_path, lock_icon_black)), size=(100, 100))
        self.college_logo_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, college_logo)), size=(200, 100))
        self.texture_black = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, texture)), size=(1600, 900))
        self.key_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, key_white)), light_image=Image.open(os.path.join(image_path, key_black)), size=(25, 25))
        self.sys_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, sys_white)), light_image=Image.open(os.path.join(image_path, sys_black)), size=(25, 25))
        self.robot_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, robot_white)), light_image=Image.open(os.path.join(image_path, robot_black)), size=(25, 25))
        self.home_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, home_white)), light_image=Image.open(os.path.join(image_path, home_black)), size=(25, 25))
        self.delete_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, delete_white)), light_image=Image.open(os.path.join(image_path, delete_black)), size=(25, 25))
        self.add_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, add_white)), light_image=Image.open(os.path.join(image_path, add_black)), size=(25, 25))
        self.transparent = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, transparent)), size=(1600, 900))
        self.texture_black_2 = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, texture2)), size=(1600, 900))
        self.train_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, train_white)), light_image=Image.open(os.path.join(image_path, train_black)), size=(25, 25))
        self.quit_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, quit_white)), light_image=Image.open(os.path.join(image_path, quit_black)), size=(25, 25))
        
        self.start_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(
            image_path, start_white)), light_image=Image.open(os.path.join(image_path, start_black)), size=(150, 150))

        self.theme_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, day_img)), 
                                                light_image=Image.open(os.path.join(image_path, night_img)), size=(25, 25))


        self.shubham_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, shubham)), size=(110, 140))
        self.shiv_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, shiv)), size=(110, 140))
        self.shobhit_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, shobhit)), size=(110, 140))
        self.sangeet_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, sangeet)), size=(110, 140))
        self.shranjal_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, shranjal)), size=(110, 140))
        self.tapasvi_img = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, tapasvi)), size=(110, 140))
        
        
        '''Database Object'''
        self.db = Mydb()

        '''Attribute loading'''
        self.PASSWORD = self.db.get_attr('password')
        self.MASTER_PASSWORD = self.db.get_attr('m_password')

        print(self.PASSWORD)

        #self.home()
        self.settings_page()

    def home(self) -> None:
        
        def get_response(query : str) :
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

          

            File = 'data.pth'
            data = torch.load(File)

            input_size = data["input_size"]
            output_size = data["output_size"]
            hidden_size = data["hidden_size"]
            all_words = data["all_words"]
            tags = data["tags"]
            model_state = data["model_state"]

            model = NeuralCode(input_size, hidden_size, output_size).to(device)
            model.load_state_dict(model_state)
            model.eval()
            
            sentence = tokenize(query)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X)
            output = model(X)
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]

            if prob.item() > 0.75:
                response_list = self.db.get_responses(tag)
                k = random.randint(0, (len(response_list)-1))
                return response_list[k]
            else : return "Sorry! I did not understand. "

        def add_text(text : str, sender : str) ->None :
            text = f"{sender} : {text}\n\n"
            self.text_box.configure(state = 'normal')
            self.text_box.insert('end',text)
            self.text_box.configure(state = 'disabled')
            self.text_box.see('end')
            self.window.update()

        def start():
            self.start_btn.destroy()
            self.college_logo_home.destroy()
            self.theme_btn.configure(state = 'disabled')
            self.login_btn.configure(state = 'disabled')
            self.blip.configure(image = self.green_blip_img)
            self.text_box.place(relx = 0.5, rely = 0.5, relwidth = 1, relheight = 1, anchor = 'center')


            self.window.update()
            add_text("Hello, How can I help you?", bot)
            talk("Hello, How can I help you?")
            
            idk_count = 0
            run = True

            while(run):
                
                text, key , sender = recognizer()

                if key == 'm' :
                    add_text(text,bot)
                    self.window.update()
                    talk("Sorry I cannot hear you")
                    self.window.update()
                    time.sleep(2)
                    run = False
                    self.home()
                elif key == 'e' :
                    add_text("Network is down, please try later.\n Have a nice day!",bot)
                    self.window.update()
                    talk("Network is down, please try later. Have a nice day")
                    run = False
                elif key == 'a' :
                    add_text(text,bot)
                    self.window.update()
                    if idk_count == 3 : run = False
                    talk(text)
                    self.window.update()
                    idk_count+=1
                elif key == 'n' :
                    add_text(text, 'You')


                    if text.lower() in quit_txt:
                        add_text("Have a nice day!",bot)
                        self.window.update()
                        talk("have a nice day")
                        run = False
                    else:
                        response = get_response(text)
                        add_text(response,bot)
                        self.window.update()
                        talk(response)
                        add_text("Can I help you with anything else? (Say 'Thank You' to end )",bot)
                        talk("Can I help you with anything else?") 
                        self.window.update()

            self.home()

        '''PLACINGS'''
        self.frame_home = customtkinter.CTkFrame(master=self.window)
        self.frame_home.place(relwidth=1, relheight=1,
                              relx=0.5, rely=0.5, anchor=CENTER)

        self.blip = customtkinter.CTkLabel(
            master=self.frame_home, text="", width=50, image=self.red_blip_img)
        self.blip.place(relheight=0.05, relwidth=0.05, rely=0.01, relx=0.001)
        
        self.quit_btn = customtkinter.CTkButton(
            master=self.frame_home, image=self.quit_img, text="", fg_color='transparent', command= lambda : quit())
        self.quit_btn.place(
            relheight=0.05, relwidth=0.03, rely=0.01, relx=0.88)

        self.theme_btn = customtkinter.CTkButton(
            master=self.frame_home, image=self.theme_img, text="", fg_color='transparent', command = lambda : self.change_theme_home(None))
        self.theme_btn.place(
            relheight=0.05, relwidth=0.035, rely=0.01, relx=0.91)

        self.login_btn = customtkinter.CTkButton(
            master=self.frame_home, text="Login", command=lambda: self.login_page(None))
        self.login_btn.place(
            relheight=0.05, relwidth=0.035, rely=0.01, relx=0.95)
        
        self.frame_text = customtkinter.CTkFrame(master= self.frame_home)
        self.frame_text.place(relx = 0.5, rely = 0.5, relwidth = 0.8, relheight = 0.8, anchor = CENTER)

        self.college_logo_home = customtkinter.CTkLabel(
            master=self.frame_text, text='', image=self.college_logo_img, fg_color='transparent')
        self.college_logo_home.place(relx = 0.5, rely = 0.2,anchor=CENTER)

        self.start_btn = customtkinter.CTkButton(master= self.frame_text, text = "", fg_color='transparent',border_color="#FFFFFF", border_width=2, corner_radius=50 ,image = self.start_img, command= lambda : start())
        self.start_btn.place(relx = 0.5, rely = 0.5, anchor = 'center')
        
        self.text_box = customtkinter.CTkTextbox(master = self.frame_text, font = customtkinter.CTkFont(size=20) ,state = 'disabled')

    def login_page(self, event) -> None:

        self.switch('login')

        def login_chk(event, state: str):
            '''
            Checks validity of password

            '''
            password = self.pass_entry.get()
            if state == 'n':
                if password == self.PASSWORD:
                    self.settings_page()
                else:
                    self.invalid_label = customtkinter.CTkLabel(
                        master=self.frame_login, text="Incorrect Password", text_color=RED, fg_color='transparent')
                    self.invalid_label.place(x=105, y=163, anchor=CENTER)
            if state == 'f':
                if password == self.MASTER_PASSWORD:
                    self.settings_page()
                else:
                    self.invalid_label = customtkinter.CTkLabel(
                        master=self.frame_login, text="Incorrect Password", text_color=RED, fg_color='transparent')
                    self.invalid_label.place(x=200, y=325, anchor=CENTER)

        def forget_pass_page():
            self.college_logo_label.destroy()
            try:
                self.invalid_label.destroy()
            except:
                pass
            self.pass_entry.configure(placeholder_text="Enter Master Password")
            self.pass_entry.place(x=200, y=375, anchor=CENTER)

            self.login_chk_btn.configure(command=lambda: login_chk(None, 'f'))
            self.login_chk_btn.place(x=200, y=425, anchor=CENTER)

            self.forgot_pass_btn.configure(
                text="Back to Log in", command=lambda: self.back('login'))
            self.forgot_pass_btn.place(x=200, y=475)

            self.lock_label = customtkinter.CTkLabel(
                master=self.frame_login, text='', image=self.lock_img, fg_color='transparent')
            self.lock_label.place(x=200, y=200, anchor=CENTER)

            self.sub_label = customtkinter.CTkLabel(master=self.frame_login, text='Trouble with logging in? \n Enter Master Password to continue.', text_color=(
                DARK_GREY, LIGHT_GREY), fg_color='transparent')
            self.sub_label.place(x=200, y=275, anchor=CENTER)

        self.frame_login_master = customtkinter.CTkFrame(master=self.window)
        self.frame_login_master.place(relheight = 1, relwidth = 1, relx = 0.5, rely = 0.5, anchor = 'center')

        self.frame_login = customtkinter.CTkFrame(
            master=self.frame_login_master, width=400, height=500, corner_radius=15)
        self.frame_login.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.login_label = customtkinter.CTkLabel(
            master=self.frame_login, text="", image=self.eira_logo_img, fg_color='transparent', corner_radius=15)
        self.login_label.place(x=200, y=70, anchor=CENTER)

        self.back_button = customtkinter.CTkButton(
            master=self.window, image=self.back_btn_img, text="", command=lambda: self.back('home'), fg_color='transparent')
        self.back_button.place(
            relheight=0.05, relwidth=0.05, rely=0.01, relx=0.001)

        self.pass_entry = customtkinter.CTkEntry(master=self.frame_login, width=300, height=45, corner_radius=5, placeholder_text="Enter Admin Password", show='*',
                                                 placeholder_text_color=(LIGHT_GREY, AQUA))
        self.pass_entry.place(x=200, y=200, anchor=CENTER)

        self.login_chk_btn = customtkinter.CTkButton(
            master=self.frame_login, text="Log in", width=300, height=40, command=lambda: login_chk(None, 'n'))
        self.login_chk_btn.place(x=200, y=250, anchor=CENTER)

        self.forgot_pass_btn = customtkinter.CTkButton(
            master=self.frame_login, text="Forgotten your password?", fg_color='transparent', text_color=LIGHT_GREY, command=lambda: forget_pass_page())
        self.forgot_pass_btn.place(x=200, y=450, anchor=CENTER)

        self.college_logo_label = customtkinter.CTkLabel(
            master=self.frame_login, text='', image=self.college_logo_img, fg_color='transparent')
        self.college_logo_label.place(x=200, y=350, anchor=CENTER)

    def change_scaling(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def change_theme_home(self, event) :
        if self.curtheme == 'light' :
            self.curtheme= 'dark'
            customtkinter.set_appearance_mode(self.curtheme)
        elif self.curtheme == 'dark' :
            self.curtheme = 'light'
            customtkinter.set_appearance_mode(self.curtheme)

    def change_theme(self, new_theme : str) :
        customtkinter.set_appearance_mode(new_theme)
        
    def change_color(self, new_color : str) :
        customtkinter.set_default_color_theme(new_color)
        self.window.update()
        self.settings_page()

    def change_volume(self, new_volume) :
        pass

    def change_voice(self, new_voice) :
        pass

    def change_speed(self, new_speed) :
        pass

    def settings_page(self) -> None:
        self.switch('settings')

        def add_data():
            self.switch('add_data')
            self.TAG_N = ""
            self.PATTERN_N = ""
            self.RESPONSE_N = ""

            def check_tag():
                tags = self.db.get_tags()

                tag = self.tag_txt_entry.get()

                if tag not in tags and len(tag) != 0:
                    self.tag_validity_label.configure(
                        text='Valid Tag', text_color=GREEN)
                    self.tag_validity_label.place(
                        relx=0.04, rely=0.17, anchor='w')
                    self.tag_validity_label.update()
                    self.pattern_add_btn.configure(state='normal')
                    self.response_add_btn.configure(state='normal')
                    self.save_data_btn.configure(state='normal')
                    self.tag_txt_entry.configure(state='readonly')
                    self.tag_chk_btn.configure(text_color=GREEN, command=None)

                    self.TAG_N = tag

                    self.add_data_textbox.configure(state='normal')
                    self.add_data_textbox.insert(
                        customtkinter.END, f'\"TAG\" :    {self.TAG_N} \n\n')
                    self.add_data_textbox.configure(state='disabled')

                else:
                    if tag in tags:
                        self.tag_validity_label.configure(
                            text='Tag already in database', text_color=RED)
                    if len(tag) == 0:
                        self.tag_validity_label.configure(
                            text='Invalid Tag', text_color=RED)

                    self.tag_validity_label.place(
                        relx=0.04, rely=0.17, anchor='w')
                    self.tag_validity_label.update()
                    self.tag_chk_btn.configure(text_color=RED)

            def insert_tags():
                tag_disp_textbox.configure(state='normal')
                tags = self.db.get_tags()
                tag_disp_textbox.insert(customtkinter.END, '\"TAGS\" - \n\n')

                for i, tag in enumerate(tags, 1):
                    tag_disp_textbox.insert(
                        customtkinter.END, f'({i}) : {tag} \n')

                tag_disp_textbox.configure(state='disabled')

            def add_pattern():
                pattern = self.pattern_txt_entry.get()

                if len(pattern):
                    self.PATTERN_N = self.PATTERN_N + '&' + pattern
                    self.pattern_txt_entry.delete(0, customtkinter.END)
                    self.pattern_validity_label.configure(
                        text="Valid Pattern", text_color=GREEN)
                    self.pattern_validity_label.place(
                        relx=0.04, rely=0.35, anchor='w')

                    self.add_data_textbox.configure(state='normal')
                    self.add_data_textbox.insert(
                        customtkinter.END, f'\"Pattern\" :    {pattern} \n\n')
                    self.add_data_textbox.configure(state='disabled')

                else:
                    self.pattern_validity_label.configure(
                        text="Please enter valid Pattern", text_color=RED)
                    self.pattern_validity_label.place(
                        relx=0.04, rely=0.35, anchor='w')

            def add_response():
                response = self.response_txt_entry.get()

                if len(response):
                    self.RESPONSE_N = self.RESPONSE_N + '&' + response
                    self.response_txt_entry.delete(0, customtkinter.END)
                    self.response_validity_label.configure(
                        text="Valid Response", text_color=GREEN)
                    self.response_validity_label.place(
                        relx=0.04, rely=0.53, anchor='w')

                    self.add_data_textbox.configure(state='normal')
                    self.add_data_textbox.insert(
                        customtkinter.END, f'\"Response\" :    {response} \n\n')
                    self.add_data_textbox.configure(state='disabled')
                else:
                    self.response_validity_label.configure(
                        text="Please enter valid Response", text_color=RED)
                    self.response_validity_label.place(
                        relx=0.04, rely=0.53, anchor='w')

            def save_data():
                if len(self.PATTERN_N) == 0:
                    self.save_validity_label.configure(
                        text='Please Enter Pattern', text_color=RED)
                    self.save_validity_label.place(
                        relx=0.19, rely=0.63, anchor='w')
                    self.pattern_txt_entry.focus()
                    return
                if len(self.RESPONSE_N) == 0:
                    self.save_validity_label.configure(
                        text='Please Enter Response', text_color=RED)
                    self.save_validity_label.place(
                        relx=0.19, rely=0.63, anchor='w')
                    self.response_txt_entry.focus()
                    return
                choice = open_dialog(
                    "Do you want to save changes to the database?")

                if choice.lower() == "yes":
                    self.db.insert_data(
                        tag=self.TAG_N, pattern=self.PATTERN_N, response=self.RESPONSE_N)

                    self.save_validity_label.configure(
                        text='DATA SAVED', text_color=GREEN)
                    self.save_validity_label.place(
                        relx=0.19, rely=0.63, anchor='w')
                    self.window.update()
                    time.sleep(1)
                    reset()
                else:
                    self.save_validity_label.configure(
                        text='DATA NOT SAVED', text_color=RED)
                    self.save_validity_label.place(
                        relx=0.19, rely=0.63, anchor='w')

            def reset():
                self.TAG_N = ""
                self.PATTERN_N = ""
                self.RESPONSE_N = ""
                add_data()

            def open_dialog(text: str) -> str:
                dialog = customtkinter.CTkInputDialog(
                    text=f"{text}", title="Save? (YES/NO)")
                return dialog.get_input()

            self.add_data_btn.configure(fg_color=Color_theme)

            self.frame_add_data = customtkinter.CTkFrame(
                master=self.frame_settings)
            self.frame_add_data.place(
                relheight=1, relwidth=0.84, relx=0.578, rely=0.5, anchor=CENTER)

            self.tag_label = customtkinter.CTkLabel(master=self.frame_add_data, text="Enter Tag", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                    font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.tag_label.place(relwidth=0.2, relx=0.136,
                                 rely=0.05, anchor=CENTER)
            self.tag_txt_entry = customtkinter.CTkEntry(
                master=self.frame_add_data, height=45, placeholder_text='Enter Unique tag')
            self.tag_txt_entry.place(
                relwidth=0.2, relx=0.136, rely=0.12, anchor=CENTER)
            self.tag_chk_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Check", width=100, height=45, border_color=WHITE, border_width=2,
                                                       text_color=(BLACK, WHITE), fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: check_tag())
            self.tag_chk_btn.place(relx=0.28, rely=0.12, anchor=CENTER)

            self.pattern_label = customtkinter.CTkLabel(master=self.frame_add_data, text="Enter Pattern", width=150, height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                        font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.pattern_label.place(
                relwidth=0.2, relx=0.136, rely=0.23, anchor=CENTER)
            self.pattern_txt_entry = customtkinter.CTkEntry(
                master=self.frame_add_data, height=45, placeholder_text='Enter Pattern')
            self.pattern_txt_entry.place(
                relwidth=0.2, relx=0.136, rely=0.30, anchor=CENTER)
            self.pattern_add_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Add", width=100, height=45, border_color=WHITE, border_width=2,
                                                           text_color=(BLACK, WHITE), fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: add_pattern(), state='disabled')
            self.pattern_add_btn.place(relx=0.28, rely=0.30, anchor=CENTER)

            self.response_label = customtkinter.CTkLabel(master=self.frame_add_data, text="Enter Response", width=150, height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                         font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.response_label.place(
                relwidth=0.2, relx=0.136, rely=0.41, anchor=CENTER)
            self.response_txt_entry = customtkinter.CTkEntry(
                master=self.frame_add_data, height=45, placeholder_text='Enter Response')
            self.response_txt_entry.place(
                relwidth=0.2, relx=0.136, rely=0.48, anchor=CENTER)
            self.response_add_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Add", width=100, height=45, border_color=WHITE, border_width=2,
                                                            text_color=(BLACK, WHITE), fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: add_response(), state='disabled')
            self.response_add_btn.place(relx=0.28, rely=0.48, anchor=CENTER)

            self.save_data_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Save", width=150, height=45, border_width=2,
                                                         text_color=GREEN, fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: save_data(), state='disabled')
            self.save_data_btn.place(relx=0.24, rely=0.58, anchor=CENTER)

            self.reset_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Reset", width=150, height=45, border_width=2,
                                                     text_color=RED, fg_color=('transparent'), font=customtkinter.CTkFont(size=14), command=lambda: reset())
            self.reset_btn.place(relx=0.1, rely=0.58, anchor=CENTER)

            self.tag_validity_label = customtkinter.CTkLabel(
                master=self.frame_add_data)
            self.pattern_validity_label = customtkinter.CTkLabel(
                master=self.frame_add_data)
            self.response_validity_label = customtkinter.CTkLabel(
                master=self.frame_add_data)
            self.save_validity_label = customtkinter.CTkLabel(
                master=self.frame_add_data)

            self.add_data_textbox = customtkinter.CTkTextbox(
                master=self.frame_add_data,  state='disabled', font=customtkinter.CTkFont(size=14))
            self.add_data_textbox.place(
                relwidth=0.4, relheight=0.9, relx=0.35, rely=0.54, anchor='w')

            self.add_data_table_label = customtkinter.CTkLabel(master=self.frame_add_data, text="Your data Appears here", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                               font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.add_data_table_label.place(
                relwidth=0.2, relx=0.45, rely=0.05, anchor='w')

            tag_disp_textbox = customtkinter.CTkTextbox(
                master=self.frame_add_data, state='disabled', font=customtkinter.CTkFont(size=14))
            tag_disp_textbox.place(
                relwidth=0.2, relheight=0.9, relx=0.77, rely=0.54, anchor='w')

            self.tag_table_label = customtkinter.CTkLabel(master=self.frame_add_data, text="Tags in Database", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                          font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.tag_table_label.place(
                relwidth=0.2, relx=0.77, rely=0.05, anchor='w')
            insert_tags()

        def del_data():
            self.switch('del_data')

            def check_tag():
                tags = self.db.get_tags()

                tag = self.tag_txt_entry.get()

                if tag in tags and len(tag) != 0:
                    self.tag_validity_label.configure(
                        text='Valid Tag', text_color=GREEN)
                    self.tag_validity_label.place(
                        relx=0.04, rely=0.17, anchor='w')
                    self.tag_validity_label.update()

                    self.tag_txt_entry.configure(state='readonly')
                    self.tag_chk_btn.configure(text_color=GREEN, command=None)
                    self.del_data_textbox.configure(state='normal')
                    self.del_data_textbox.insert(
                        customtkinter.END, f"Tag  :   {tag}\n")
                    self.del_data_textbox.configure(state='disabled')
                    self.delete_btn.configure(state='normal')

                    insert_data(tag)

                else:
                    if tag not in tags:
                        self.tag_validity_label.configure(
                            text='Tag not in database', text_color=RED)
                    if len(tag) == 0:
                        self.tag_validity_label.configure(
                            text='Invalid Tag', text_color=RED)

                    self.tag_validity_label.place(
                        relx=0.04, rely=0.17, anchor='w')
                    self.tag_validity_label.update()
                    self.tag_chk_btn.configure(text_color=RED)

            def del_data_fun():

                tag = self.tag_txt_entry.get()
                choice = open_dialog(tag)

                if choice.lower() == "yes":

                    self.db.delete_data(tag)

                    self.del_validity_label.configure(
                        text='DATA DELETED', text_color=GREEN)
                    self.del_validity_label.place(
                        relx=0.2, rely=0.28, anchor='w')
                    self.window.update()
                    time.sleep(1)
                    reset()
                else:
                    self.save_validity_label.configure(
                        text='DATA NOT DELETED', text_color=RED)
                    self.save_validity_label.place(
                        relx=0.2, rely=0.28, anchor='w')

            def insert_tags():
                tag_disp_textbox.configure(state='normal')
                tags = self.db.get_tags()
                tag_disp_textbox.insert(customtkinter.END, '\"TAGS\" - \n\n')

                for i, tag in enumerate(tags, 1):
                    tag_disp_textbox.insert(
                        customtkinter.END, f'({i}) : {tag} \n')

                tag_disp_textbox.configure(state='disabled')

            def insert_data(tag: str):
                self.del_data_textbox.configure(state='normal')

                patterns = self.db.get_patterns(tag)
                responses = self.db.get_responses(tag)

                self.del_data_textbox.configure(state='normal')

                for i, pattern in enumerate(patterns, 1):
                    self.del_data_textbox.insert(
                        customtkinter.END, f"\nPattern  #{i} :   {pattern}\n")

                for i, response in enumerate(responses, 1):
                    self.del_data_textbox.insert(
                        customtkinter.END, f"\nResponse #{i} :   {response}\n")

                self.del_data_textbox.configure(state='disabled')

            def insert_all_data():

                self.all_data_textbox.configure(state='normal', wrap = 'word')

                tags = self.db.get_tags()

                for i, tag in enumerate(tags, 1):
                    self.all_data_textbox.insert(
                        customtkinter.END, f"\nTag  #{i} :   {tag}\n")

                    patterns = self.db.get_patterns(tag)
                    responses = self.db.get_responses(tag)
                    for j, pattern in enumerate(patterns, 1):
                        self.all_data_textbox.insert(
                            customtkinter.END, f"\nPattern  #{j} :   {pattern}\n")

                    for k, response in enumerate(responses, 1):
                        self.all_data_textbox.insert(
                            customtkinter.END, f"\nResponse #{k} :   {response}\n")

                    self.all_data_textbox.insert(
                        customtkinter.END, '__'*25 + '\n')

                self.all_data_textbox.configure(state='disabled')

            def open_dialog(text: str) -> str:
                dialog = customtkinter.CTkInputDialog(
                    text=f"This action cannot be UNDONE.\nAre you sure you want to delete this record.\n TAG : {text}", title="DELETE? (YES/NO)")
                return dialog.get_input()

            def reset():
                del_data()

            self.frame_del_data = customtkinter.CTkFrame(
                master=self.frame_settings)
            self.frame_del_data.place(
                relheight=1, relwidth=0.84, relx=0.578, rely=0.5, anchor=CENTER)

            self.tag_label = customtkinter.CTkLabel(master=self.frame_del_data, text="Enter Tag", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                    font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.tag_label.place(relwidth=0.2, relx=0.136,
                                 rely=0.05, anchor=CENTER)
            self.tag_txt_entry = customtkinter.CTkEntry(
                master=self.frame_del_data, height=45, placeholder_text='Enter tag from database')
            self.tag_txt_entry.place(
                relwidth=0.2, relx=0.136, rely=0.12, anchor=CENTER)
            self.tag_chk_btn = customtkinter.CTkButton(master=self.frame_del_data, text="Check", width=100, height=45, border_color=WHITE, border_width=2,
                                                       text_color=(BLACK, WHITE), fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: check_tag())
            self.tag_chk_btn.place(relx=0.28, rely=0.12, anchor=CENTER)

            self.del_data_label = customtkinter.CTkLabel(master=self.frame_del_data, text="Data to be deleted", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                         font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.del_data_label.place(
                relwidth=0.3, relx=0.03, rely=0.35, anchor='w')

            self.del_data_textbox = customtkinter.CTkTextbox(
                master=self.frame_del_data,  state='disabled', font=customtkinter.CTkFont(size=14))
            self.del_data_textbox.place(
                relwidth=0.3, relheight=0.6, relx=0.03, rely=0.69, anchor='w')

            self.all_data_textbox = customtkinter.CTkTextbox(
                master=self.frame_del_data,  state='disabled', font=customtkinter.CTkFont(size=14))
            self.all_data_textbox.place(
                relwidth=0.4, relheight=0.9, relx=0.35, rely=0.54, anchor='w')
            insert_all_data()
            self.del_data_table_label = customtkinter.CTkLabel(master=self.frame_del_data, text="Your data Appears here", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                               font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.del_data_table_label.place(
                relwidth=0.2, relx=0.45, rely=0.05, anchor='w')

            tag_disp_textbox = customtkinter.CTkTextbox(
                master=self.frame_del_data, state='disabled', font=customtkinter.CTkFont(size=14))
            tag_disp_textbox.place(
                relwidth=0.2, relheight=0.9, relx=0.77, rely=0.54, anchor='w')
            insert_tags()

            self.tag_validity_label = customtkinter.CTkLabel(
                master=self.frame_del_data)

            self.delete_btn = customtkinter.CTkButton(master=self.frame_del_data, text="DELETE", width=150, height=45, border_width=2,
                                                      text_color=RED, fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: del_data_fun(), state='disabled')
            self.delete_btn.place(relx=0.24, rely=0.23, anchor=CENTER)

            self.reset_btn = customtkinter.CTkButton(master=self.frame_del_data, text="Reset", width=150, height=45, border_width=2,
                                                     text_color=RED, fg_color=('transparent'), font=customtkinter.CTkFont(size=14), command=lambda: reset())
            self.reset_btn.place(relx=0.1, rely=0.23, anchor=CENTER)

            self.tag_table_label = customtkinter.CTkLabel(master=self.frame_del_data, text="Tags in Database", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                          font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.tag_table_label.place(
                relwidth=0.2, relx=0.77, rely=0.05, anchor='w')
            self.del_validity_label = customtkinter.CTkLabel(
                master=self.frame_del_data)

        def update_data() :
            self.switch('up_data')
            self.TAG_N = ""
            self.PATTERN_N = ""
            self.RESPONSE_N = ""

            def add_pattern():
                pattern = self.pattern_txt_entry.get()

                if len(pattern):
                    self.PATTERN_N = self.PATTERN_N + '&' + pattern
                    self.pattern_txt_entry.delete(0, customtkinter.END)
                    self.pattern_validity_label.configure(
                        text="Valid Pattern", text_color=GREEN)
                    self.pattern_validity_label.place(
                        relx=0.04, rely=0.35, anchor='w')

                    self.update_data_textbox.configure(state='normal')
                    self.update_data_textbox.insert(
                        customtkinter.END, f'\"Pattern\" :    {pattern} \n\n')
                    self.update_data_textbox.configure(state='disabled')

                else:
                    self.pattern_validity_label.configure(
                        text="Please enter valid Pattern", text_color=RED)
                    self.pattern_validity_label.place(
                        relx=0.04, rely=0.35, anchor='w')

            def add_response():
                response = self.response_txt_entry.get()

                if len(response):
                    self.RESPONSE_N = self.RESPONSE_N + '&' + response
                    self.response_txt_entry.delete(0, customtkinter.END)
                    self.response_validity_label.configure(
                        text="Valid Response", text_color=GREEN)
                    self.response_validity_label.place(
                        relx=0.04, rely=0.53, anchor='w')

                    self.update_data_textbox.configure(state='normal')
                    self.update_data_textbox.insert(
                        customtkinter.END, f'\"Response\" :    {response} \n\n')
                    self.update_data_textbox.configure(state='disabled')
                else:
                    self.response_validity_label.configure(
                        text="Please enter valid Response", text_color=RED)
                    self.response_validity_label.place(
                        relx=0.04, rely=0.53, anchor='w')

            def save_data():
                if len(self.PATTERN_N) == 0:
                    self.save_validity_label.configure(
                        text='Please Enter Pattern', text_color=RED)
                    self.save_validity_label.place(
                        relx=0.19, rely=0.63, anchor='w')
                    self.pattern_txt_entry.focus()
                    return
                if len(self.RESPONSE_N) == 0:
                    self.save_validity_label.configure(
                        text='Please Enter Response', text_color=RED)
                    self.save_validity_label.place(
                        relx=0.19, rely=0.63, anchor='w')
                    self.response_txt_entry.focus()
                    return
               

                
                self.db.update_data2(
                    tag=self.TAG_N, pattern=self.PATTERN_N, response=self.RESPONSE_N)
                self.save_validity_label.configure(
                    text='DATA SAVED', text_color=GREEN)
                self.save_validity_label.place(
                    relx=0.19, rely=0.63, anchor='w')
                self.window.update()
                time.sleep(1)
                reset()
                
            def reset():
                self.TAG_N = ""
                self.PATTERN_N = ""
                self.RESPONSE_N = ""
                update_data()

            def check_tag():
                tags = self.db.get_tags()

                tag = self.tag_txt_entry.get()

                if tag  in tags and len(tag) != 0:
                    self.tag_validity_label.configure(
                        text='Valid Tag', text_color=GREEN)
                    self.tag_validity_label.place(
                        relx=0.04, rely=0.17, anchor='w')
                    self.tag_validity_label.update()
                    self.pattern_add_btn.configure(state='normal')
                    self.response_add_btn.configure(state='normal')
                    self.save_data_btn.configure(state='normal')
                    self.tag_txt_entry.configure(state='readonly')
                    self.tag_chk_btn.configure(text_color=GREEN, command=None)

                    self.TAG_N = tag

                    self.response_add_btn.configure(state = 'normal')
                    self.pattern_add_btn.configure(state = 'normal')
                    self.window.update()

                    self.update_data_textbox.configure(state='normal')
                    self.update_data_textbox.insert(
                        customtkinter.END, f'\"TAG\" :    {self.TAG_N} \n\n')
                    self.update_data_textbox.configure(state='disabled')

                else:
                    if tag not in tags:
                        self.tag_validity_label.configure(
                            text='Tag not in database', text_color=RED)
                    if len(tag) == 0:
                        self.tag_validity_label.configure(
                            text='Invalid Tag', text_color=RED)

                    self.tag_validity_label.place(
                        relx=0.04, rely=0.17, anchor='w')
                    self.tag_validity_label.update()
                    self.tag_chk_btn.configure(text_color=RED)
    
            def insert_tags():
                tag_disp_textbox.configure(state='normal')
                tags = self.db.get_tags()
                tag_disp_textbox.insert(customtkinter.END, '\"TAGS\" - \n\n')

                for i, tag in enumerate(tags, 1):
                    tag_disp_textbox.insert(
                        customtkinter.END, f'({i}) : {tag} \n')

                tag_disp_textbox.configure(state='disabled')

            def insert_all_data():

                self.all_data_textbox.configure(state='normal', wrap = 'word')

                tags = self.db.get_tags()

                for i, tag in enumerate(tags, 1):
                    self.all_data_textbox.insert(
                        customtkinter.END, f"\nTag  #{i} :   {tag}\n")

                    patterns = self.db.get_patterns(tag)
                    responses = self.db.get_responses(tag)
                    for j, pattern in enumerate(patterns, 1):
                        self.all_data_textbox.insert(
                            customtkinter.END, f"\nPattern  #{j} :   {pattern}\n")

                    for k, response in enumerate(responses, 1):
                        self.all_data_textbox.insert(
                            customtkinter.END, f"\nResponse #{k} :   {response}\n")

                    self.all_data_textbox.insert(
                        customtkinter.END, '__'*25 + '\n')

                self.all_data_textbox.configure(state='disabled')


            self.frame_update_data = customtkinter.CTkFrame(
                master=self.frame_settings)
            self.frame_update_data.place(
                relheight=1, relwidth=0.84, relx=0.578, rely=0.5, anchor=CENTER)

            self.tag_label = customtkinter.CTkLabel(master=self.frame_update_data, text="Enter Tag", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                    font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.tag_label.place(relwidth=0.2, relx=0.136,
                                 rely=0.05, anchor=CENTER)
            self.tag_txt_entry = customtkinter.CTkEntry(
                master=self.frame_update_data, height=45, placeholder_text='Enter tag from database')
            self.tag_txt_entry.place(
                relwidth=0.2, relx=0.136, rely=0.12, anchor=CENTER)
            self.tag_chk_btn = customtkinter.CTkButton(master=self.frame_update_data, text="Check", width=100, height=45, border_color=WHITE, border_width=2,
                                                       text_color=(BLACK, WHITE), fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: check_tag())
            self.tag_chk_btn.place(relx=0.28, rely=0.12, anchor=CENTER)

            self.update_data_textbox = customtkinter.CTkTextbox(
                master=self.frame_update_data,  state='disabled', font=customtkinter.CTkFont(size=14))
            self.update_data_textbox.place(
                relwidth=0.3, relheight=0.35, relx=0.03, rely=0.79, anchor='w')

            self.all_data_textbox = customtkinter.CTkTextbox(
                master=self.frame_update_data,  state='disabled', font=customtkinter.CTkFont(size=14))
            self.all_data_textbox.place(
                relwidth=0.4, relheight=0.9, relx=0.35, rely=0.54, anchor='w')
            insert_all_data()
            self.del_data_table_label = customtkinter.CTkLabel(master=self.frame_update_data, text="Your data Appears here", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                               font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.del_data_table_label.place(
                relwidth=0.2, relx=0.45, rely=0.05, anchor='w')

            tag_disp_textbox = customtkinter.CTkTextbox(
                master=self.frame_update_data, state='disabled', font=customtkinter.CTkFont(size=14))
            tag_disp_textbox.place(
                relwidth=0.2, relheight=0.9, relx=0.77, rely=0.54, anchor='w')
            insert_tags()

            self.tag_validity_label = customtkinter.CTkLabel(
                master=self.frame_update_data)
            self.pattern_validity_label = customtkinter.CTkLabel(
                master=self.frame_update_data)
            self.response_validity_label = customtkinter.CTkLabel(
                master=self.frame_update_data)
            self.save_validity_label = customtkinter.CTkLabel(
                master=self.frame_update_data)

            self.pattern_label = customtkinter.CTkLabel(master=self.frame_update_data, text="Enter Pattern", width=150, height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                        font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.pattern_label.place(
                relwidth=0.2, relx=0.136, rely=0.23, anchor=CENTER)
            self.pattern_txt_entry = customtkinter.CTkEntry(
                master=self.frame_update_data, height=45, placeholder_text='Enter Pattern')
            self.pattern_txt_entry.place(
                relwidth=0.2, relx=0.136, rely=0.30, anchor=CENTER)
            self.pattern_add_btn = customtkinter.CTkButton(master=self.frame_update_data, text="Add", width=100, height=45, border_color=WHITE, border_width=2,
                                                           text_color=(BLACK, WHITE), fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: add_pattern(), state='disabled')
            self.pattern_add_btn.place(relx=0.28, rely=0.30, anchor=CENTER)

            self.response_label = customtkinter.CTkLabel(master=self.frame_update_data, text="Enter Response", width=150, height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                         font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.response_label.place(
                relwidth=0.2, relx=0.136, rely=0.41, anchor=CENTER)
            self.response_txt_entry = customtkinter.CTkEntry(
                master=self.frame_update_data, height=45, placeholder_text='Enter Response')
            self.response_txt_entry.place(
                relwidth=0.2, relx=0.136, rely=0.48, anchor=CENTER)
            self.response_add_btn = customtkinter.CTkButton(master=self.frame_update_data, text="Add", width=100, height=45, border_color=WHITE, border_width=2,
                                                            text_color=(BLACK, WHITE), fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: add_response(), state='disabled')
            self.response_add_btn.place(relx=0.28, rely=0.48, anchor=CENTER)

            self.save_data_btn = customtkinter.CTkButton(master=self.frame_update_data, text="Update", width=150, height=45, border_width=2,
                                                         text_color=GREEN, fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: save_data(), state='disabled')
            self.save_data_btn.place(relx=0.24, rely=0.58, anchor=CENTER)

            self.reset_btn = customtkinter.CTkButton(master=self.frame_update_data, text="Reset", width=150, height=45, border_width=2,
                                                     text_color=RED, fg_color=('transparent'), font=customtkinter.CTkFont(size=14), command=lambda: reset())
            self.reset_btn.place(relx=0.1, rely=0.58, anchor=CENTER)

            self.tag_table_label = customtkinter.CTkLabel(master=self.frame_update_data, text="Tags in Database", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                          font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            self.tag_table_label.place(
                relwidth=0.2, relx=0.77, rely=0.05, anchor='w')
            self.del_validity_label = customtkinter.CTkLabel(
                master=self.frame_update_data)
            
            insert_all_data()

        def change_pass():

            def check_pass() -> None:
                password = self.en_pass_entry.get()

                password_d = self.db.get_attr('password')

                if password == password_d:
                    self.chk_pass_btn.configure(text_color=GREEN)
                    self.en_pass_entry.configure(state='readonly')
                    self.update_pass_btn.configure(state='normal')
                    self.pass_validity_label.configure(
                        text='Correct Password', text_color=GREEN)
                    self.pass_validity_label.place(
                        relx=0.06, rely=0.295, anchor='w')

                else:
                    self.chk_pass_btn.configure(text_color=RED)
                    self.pass_validity_label.configure(
                        text='Incorrect Password', text_color=RED)
                    self.pass_validity_label.place(
                        relx=0.06, rely=0.295, anchor='w')

            def update_pass() -> None:
                p1 = self.en_new_pass_entry.get()
                p2 = self.conf_pass_entry.get()

                if p1 == p2 and len(p1) >= 8:
                    ch = open_dialog()
                    if ch.lower() == 'yes':
                        self.same_validity_label.configure(
                            text='Password Updated Successfully', text_color=GREEN)
                        self.same_validity_label.place(
                            relx=0.06, rely=0.795, anchor='w')
                        self.same_validity_label.update()
                        self.db.update_data('password', p1)
                        time.sleep(1)
                        change_pass()
                    else:
                        self.same_validity_label.configure(
                            text='Password Not Updated', text_color=RED)
                        self.same_validity_label.place(
                            relx=0.06, rely=0.85, anchor='w')

                elif p1 != p2:
                    self.same_validity_label.configure(
                        text='Password do not match', text_color=RED)
                    self.same_validity_label.place(
                        relx=0.06, rely=0.85, anchor='w')

                elif len(p1) == 0 or len(p2) == 0:
                    self.same_validity_label.configure(
                        text='Invalid Password', text_color=RED)
                    self.same_validity_label.place(
                        relx=0.06, rely=0.85, anchor='w')

                elif len(p1) < 8 or len(p2) < 8:
                    self.same_validity_label.configure(
                        text='Password too short', text_color=RED)
                    self.same_validity_label.place(
                        relx=0.06, rely=0.85, anchor='w')

            def open_dialog() -> str:
                dialog = customtkinter.CTkInputDialog(
                    text=f"Are you sure you want to update the password?", title="Save? (YES/NO)")
                return dialog.get_input()

            self.switch('change_pass')

            self.frame_change_pass = customtkinter.CTkFrame(
                master=self.frame_settings)
            self.frame_change_pass.place(
                relheight=1, relwidth=0.84, relx=0.578, rely=0.5, anchor=CENTER)

            self.frame_cp = customtkinter.CTkFrame(
                master=self.frame_change_pass)
            self.frame_cp.place(relheight=0.6, relwidth=0.4,
                                relx=0.5, rely=0.45, anchor=CENTER)

            self.en_pass_label = customtkinter.CTkLabel(master=self.frame_cp, text="Current Password", height=40, font=customtkinter.CTkFont(
                size=14), text_color=Color_theme, fg_color=DARK_GREY, corner_radius=10)
            self.en_pass_label.place(
                relwidth=0.5, relx=0.04, rely=0.1, anchor='w')

            self.en_pass_entry = customtkinter.CTkEntry(
                master=self.frame_cp, placeholder_text="Enter current Password", height=45, show='*')
            self.en_pass_entry.place(
                relwidth=0.6, relx=0.04, rely=0.21, anchor='w')

            self.chk_pass_btn = customtkinter.CTkButton(master=self.frame_cp, text='Check', fg_color='transparent',
                                                        text_color=(BLACK, WHITE), width=100, height=45, border_width=2, font=customtkinter.CTkFont(size=14), command=lambda: check_pass())
            self.chk_pass_btn.place(relx=0.65, rely=0.21, anchor='w')

            self.en_new_pass_label = customtkinter.CTkLabel(master=self.frame_cp, text="New Password", height=40, font=customtkinter.CTkFont(
                size=14), text_color=Color_theme, fg_color=DARK_GREY, corner_radius=10)
            self.en_new_pass_label.place(
                relwidth=0.5, relx=0.04, rely=0.375, anchor='w')

            self.en_new_pass_entry = customtkinter.CTkEntry(
                master=self.frame_cp, placeholder_text="Enter New Password (atleast 8 char)", height=45, show='*')
            self.en_new_pass_entry.place(
                relwidth=0.6, relx=0.04, rely=0.485, anchor='w')

            self.cnf_pass_label = customtkinter.CTkLabel(master=self.frame_cp, text="Confirm Password", height=40, font=customtkinter.CTkFont(
                size=14), text_color=Color_theme, fg_color=DARK_GREY, corner_radius=10)
            self.cnf_pass_label.place(
                relwidth=0.5, relx=0.04, rely=0.65, anchor='w')

            self.conf_pass_entry = customtkinter.CTkEntry(
                master=self.frame_cp, placeholder_text="Confirm Password", height=45, show='*')
            self.conf_pass_entry.place(
                relwidth=0.6, relx=0.04, rely=0.76, anchor='w')

            self.update_pass_btn = customtkinter.CTkButton(master=self.frame_cp, text='Update', fg_color='transparent', width=100,
                                                           text_color=(BLACK, WHITE), height=45, border_width=2, font=customtkinter.CTkFont(size=14), command=lambda: update_pass(), state='disabled')
            self.update_pass_btn.place(relx=0.65, rely=0.76, anchor='w')

            self.pass_validity_label = customtkinter.CTkLabel(
                master=self.frame_cp)
            self.same_validity_label = customtkinter.CTkLabel(
                master=self.frame_cp)

        def system_setting(self):

            self.switch('system_settings')
            
            self.frame_system_settings = customtkinter.CTkFrame(
                master=self.frame_settings)
            self.frame_system_settings.place(
                relheight=1, relwidth=0.84, relx=0.578, rely=0.5, anchor=CENTER)
            
            """VISUAL SETTINGS"""
            
            self.add_visual_settings_label = customtkinter.CTkLabel(master=self.frame_system_settings, text="Visual Settings", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                               font=customtkinter.CTkFont(size=15), text_color=Color_theme, corner_radius=5)
            
            self.add_visual_settings_label.place(relwidth=0.45, relx=0.25, rely=0.09, anchor=CENTER)

            self.frame_visual_settings = customtkinter.CTkFrame(
                master=self.frame_system_settings)
            self.frame_visual_settings.place(
                relheight=0.85, relwidth=0.45, relx=0.25, rely=0.55, anchor=CENTER)
            
            self.appearance_mode_label = customtkinter.CTkLabel(self.frame_visual_settings, text="Change Appearance Theme", font=customtkinter.CTkFont(size=15), bg_color=LIGHT_GREY, anchor = 'w', corner_radius=15)

            self.appearance_mode_label.place(relwidth = 0.6, relx = 0.05, rely = 0.05, anchor  = 'w')

            self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_visual_settings, values=["Dark", "Light", "System"],
                                                                       command= self.change_theme)
        
            self.appearance_mode_optionemenu.place(relx = 0.8, rely = 0.05, anchor  = CENTER)



            self.color_mode_label = customtkinter.CTkLabel(self.frame_visual_settings, text="Change Background Color", font=customtkinter.CTkFont(size=15), bg_color=LIGHT_GREY, anchor = 'w', corner_radius=15)

            self.color_mode_label.place(relwidth = 0.6, relx = 0.05, rely = 0.2, anchor  = 'w')

            self.color_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_visual_settings, values=['blue', 'green'],
                                                                       command= self.change_color)
        
            self.color_mode_optionemenu.place(relx = 0.8, rely = 0.2, anchor  = CENTER)


            self.scaling_label = customtkinter.CTkLabel(self.frame_visual_settings, text="Change UI Scaling", font=customtkinter.CTkFont(size=15), bg_color=LIGHT_GREY, anchor = 'w', corner_radius=15)

            self.scaling_label.place(relwidth = 0.6, relx = 0.05, rely = 0.35, anchor  = 'w')

            self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.frame_visual_settings, values=["100%", "110%", "120%", "80%", "90%" ],
                                                               command=self.change_scaling)
            
            self.scaling_optionemenu.place( relx = 0.8, rely = 0.35, anchor  = CENTER)

            """AUDIO SETTINGS"""

            
            self.add_audio_settings_label = customtkinter.CTkLabel(master=self.frame_system_settings, text="Audio Settings", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                               font=customtkinter.CTkFont(size=14), text_color=Color_theme, corner_radius=5)
            
            self.add_audio_settings_label.place(relwidth=0.45, relx=0.75, rely=0.09, anchor=CENTER)

            self.frame_audio_settings = customtkinter.CTkFrame(
                master=self.frame_system_settings)
            self.frame_audio_settings.place(
                relheight=0.85, relwidth=0.45, relx=0.75, rely=0.55, anchor=CENTER)

        def training_page(self) :
    
            def start_training() :
                self.start_training_btn.configure(state = 'disabled')
                self.data_table.configure(state = 'normal')
                self.data_table.delete('1.0', tkinter.END)
                tags = self.db.get_tags()
                all_words = []
                xy = []

                for tag in tags :
                    patterns = self.db.get_patterns(tag)
                    for pattern in patterns:
                        w = tokenize(pattern)
                        all_words.extend(w)
                        xy.append((w, tag))
                
                ignore_words = ['?', '!', ',', '.']
                all_words = [stem(word) for word in all_words if word not in ignore_words]
                all_words = sorted(set(all_words))
                tags = sorted(set(tags))

                X_train = []
                Y_train = []
                for (pattern_sentence, tag) in xy:
                    bag = bag_of_words(pattern_sentence, all_words)
                    X_train.append(bag)

                    label = tags.index(tag)
                    Y_train.append(label)  # cross entropy loss

                X_train = np.array(X_train)
                Y_train = np.array(Y_train)


                class ChatDataSet(Dataset):
                    def __init__(self):
                        self.n_samples = len(X_train)
                        self.x_data = X_train
                        self.y_data = Y_train

                    def __getitem__(self, index):
                        return self.x_data[index], self.y_data[index]

                    def __len__(self):
                        return self.n_samples

                # hyper parameter


                batch_size = 8
                hidden_size = 8
                output_size = len(tags)
                input_size = len(X_train[0])
                learning_rate = .001
                num_epochs = 2000


                dataset = ChatDataSet()
                train_loader = DataLoader(dataset=dataset,
                                        batch_size=batch_size,
                                        shuffle=True,
                                        num_workers=0)
                device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                model = NeuralCode(input_size, hidden_size, output_size).to(device)

                #loss and optimizer

                criterion = nn.CrossEntropyLoss()
                optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

                for epoch in range(num_epochs):
                    for (words, labels) in train_loader:
                        words = words.to(device)
                        labels = labels.to(dtype=torch.long).to(device)

                        # forward
                        outputs = model(words)
                        loss = criterion(outputs, labels)

                        # backward and optimizer steps

                        optimizer.zero_grad()
                        loss.backward()
                        optimizer.step()
                    if (epoch + 1) % 200 == 0:
                        self.data_table.insert("end", f'Epoch [{epoch+1}/{num_epochs}], Loss : {loss.item():.4f}\n')
                        self.data_table.update()

                self.data_table.insert("end", f'Final loss : {loss.item():.4f}\n')

                data = {
                    "model_state": model.state_dict(),
                    "input_size": input_size,
                    "output_size": output_size,
                    "hidden_size": hidden_size,
                    "all_words": all_words,
                    "tags": tags
                }
                File = "data.pth"

                torch.save(data, File)

                for i in range(10):
                    self.data_table.insert("end",'.\n')
                    time.sleep(0.2)
                    self.window.update()

                self.data_table.insert("end", f'Training Completed.Please Restart the app to see changes.')
                self.data_table.update()

                self.start_training_btn.configure(state = 'normal')
                self.data_table.configure(state = 'disabled')


            self.switch('training_page')

            self.frame_training = customtkinter.CTkFrame(
                master=self.frame_settings)
            self.frame_training.place(
                relheight=1, relwidth=0.84, relx=0.578, rely=0.5, anchor=CENTER)
            
            self.training_label = customtkinter.CTkLabel(master=self.frame_training, text="\"TRAIN EIRA\"", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                               font=customtkinter.CTkFont(size=17), text_color=Color_theme, corner_radius=5)
            
            self.training_label.place(relx = 0.5, rely = 0.09, anchor = CENTER, relwidth = 0.5)

            self.data_table = customtkinter.CTkTextbox(master=self.frame_training, fg_color=(LIGHT_GREY, DARK_GREY) ,text_color=GREEN, state = 'disabled', font=customtkinter.CTkFont(size=15))
            self.data_table.place(relx = 0.5, rely = 0.5, anchor = CENTER, relwidth = 0.5, relheight = 0.75)

            self.start_training_btn = customtkinter.CTkButton(master=self.frame_training, text="START", width=150, height=45, border_width=2, border_color=GREEN,
                                                         text_color=GREEN, fg_color='transparent', font=customtkinter.CTkFont(size=14), command=lambda: start_training())

            self.start_training_btn.place(relx = 0.5, rely = 0.92, anchor = CENTER)

        def about():
            self.switch('about')

            self.frame_about = customtkinter.CTkFrame(
                master=self.frame_settings)
            self.frame_about.place(relheight=1, relwidth=0.84, relx=0.578, rely=0.5, anchor=CENTER)


            self.about_label = customtkinter.CTkLabel(master=self.frame_about, text="\"ABOUT\"", height=45, fg_color=(DARK_GREY), bg_color='transparent',
                                                               font=customtkinter.CTkFont(size=17), text_color=Color_theme, corner_radius=5)
            
         
            self.about_label.place(relx = 0.5, rely = 0.09, anchor = CENTER, relwidth = 0.5)
            
            self.frame_content = customtkinter.CTkFrame(master=self.frame_about)
            self.frame_content.place(relx = 0.5, rely = 0.5, relheight = 0.7, relwidth = 0.8, anchor = CENTER)

            self.about_textbox = customtkinter.CTkTextbox(master = self.frame_content, wrap = 'word')
            self.about_textbox.place(relx = 0.5, rely = 0.3, relheight = 0.5, relwidth = 0.9, anchor = CENTER)
            self.about_textbox.insert('end', self.about_string)
            self.about_textbox.insert('end', f'\n\n ~ Team EIRA')
            self.about_textbox.configure(state = 'disabled')

            self.frame_photo = customtkinter.CTkFrame(master=self.frame_content)
            self.frame_photo.place(relx = 0.5, rely = 0.75, relheight = 0.4, relwidth = 0.9, anchor = CENTER)
            
            self.img_shubh = customtkinter.CTkLabel(master=self.frame_photo, image = self.shubham_img, text ="", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_shubh = customtkinter.CTkLabel(master=self.frame_photo, text ="Shubham Namdev\nECE", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_shubh.place(relx = 0.1, rely = 0.85, anchor  = CENTER)
            self.img_shubh.place(relx = 0.1, rely = 0.4, anchor  = CENTER)

            self.img_shiv = customtkinter.CTkLabel(master=self.frame_photo, image = self.shiv_img, text ="", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_shiv = customtkinter.CTkLabel(master=self.frame_photo, text ="Shiv Nandan Soni\nECE", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_shiv.place(relx = 0.26, rely = 0.85, anchor  = CENTER)
            self.img_shiv.place(relx = 0.26, rely = 0.4, anchor  = CENTER)

            self.img_sangeet = customtkinter.CTkLabel(master=self.frame_photo, image = self.sangeet_img, text ="", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_sangeet = customtkinter.CTkLabel(master=self.frame_photo, text ="Sangeet Kumar\nECE", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_sangeet.place(relx = 0.42, rely = 0.85, anchor  = CENTER)
            self.img_sangeet.place(relx = 0.42, rely = 0.4, anchor  = CENTER)

            self.img_shobhit = customtkinter.CTkLabel(master=self.frame_photo, image = self.shobhit_img, text ="", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_shobhit = customtkinter.CTkLabel(master=self.frame_photo, text ="Shobhit Soni\nECE", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_shobhit.place(relx = 0.58, rely = 0.85, anchor  = CENTER)
            self.img_shobhit.place(relx = 0.58, rely = 0.4, anchor  = CENTER)

            self.img_shranjal = customtkinter.CTkLabel(master=self.frame_photo, image = self.shranjal_img, text ="", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_shranjal = customtkinter.CTkLabel(master=self.frame_photo, text ="Shranjal Agrawal\nECE", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_shranjal.place(relx = 0.74, rely = 0.85, anchor  = CENTER)
            self.img_shranjal.place(relx = 0.74, rely = 0.4, anchor  = CENTER)

            self.img_tapasvi = customtkinter.CTkLabel(master=self.frame_photo, image = self.tapasvi_img, text ="", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_tapasvi = customtkinter.CTkLabel(master=self.frame_photo, text ="Tapasvi Roy\nECE", bg_color='transparent',corner_radius=5, anchor = CENTER)
            self.label_tapasvi.place(relx = 0.9, rely = 0.85, anchor  = CENTER)
            self.img_tapasvi.place(relx = 0.9, rely = 0.4, anchor  = CENTER)


     

        self.frame_settings = customtkinter.CTkFrame(master=self.window)
        self.frame_settings.place(
            relheight=1, relwidth=1, anchor=CENTER, relx=0.5, rely=0.5)

        self.side_panel_settings = customtkinter.CTkFrame(
            master=self.frame_settings)
        self.side_panel_settings.place(
            relheight=1, relwidth=0.15, relx=0.08, rely=0.5, anchor=CENTER)

        self.add_data_btn = customtkinter.CTkButton(master=self.side_panel_settings, text='Add Data', image=self.add_img, font=customtkinter.CTkFont(
            size=16), text_color=(BLACK, WHITE), fg_color='transparent', border_width=2, command=lambda: add_data(), anchor="w")
        self.add_data_btn.place(
            relwidth=0.95, relheight=0.05, relx=0.5, rely=0.05, anchor=CENTER)

        self.del_data_btn = customtkinter.CTkButton(master=self.side_panel_settings, text='Delete Data', image=self.delete_img, font=customtkinter.CTkFont(
            size=16),text_color=(BLACK, WHITE),  fg_color='transparent', border_width=2, command=lambda: del_data(), anchor="w")
        self.del_data_btn.place(
            relwidth=0.95, relheight=0.05, relx=0.5, rely=0.15, anchor=CENTER)

        self.update_data_btn = customtkinter.CTkButton(master=self.side_panel_settings, text='Update Data', image=self.delete_img, font=customtkinter.CTkFont(
            size=16),text_color=(BLACK, WHITE),  fg_color='transparent', border_width=2, command=lambda: update_data(), anchor="w")
        self.update_data_btn.place(
            relwidth=0.95, relheight=0.05, relx=0.5, rely=0.25, anchor=CENTER)

        self.change_pass_btn = customtkinter.CTkButton(master=self.side_panel_settings, text='Change Password', image=self.key_img, font=customtkinter.CTkFont(
            size=16), text_color=(BLACK, WHITE), fg_color='transparent', border_width=2, command=lambda: change_pass(), anchor="w")
        self.change_pass_btn.place(
            relwidth=0.95, relheight=0.05, relx=0.5, rely=0.35, anchor=CENTER)

        self.system_setting_btn = customtkinter.CTkButton(master=self.side_panel_settings, image=self.sys_img, text='System', font=customtkinter.CTkFont(
            size=16), text_color=(BLACK, WHITE), fg_color='transparent', border_width=2, command=lambda: system_setting(self), anchor="w")
        self.system_setting_btn.place(
            relwidth=0.95, relheight=0.05, relx=0.5, rely=0.45, anchor=CENTER)

        self.training_btn = customtkinter.CTkButton(master=self.side_panel_settings, text='Train Bot', image=self.train_img, font=customtkinter.CTkFont(
            size=16), text_color=(BLACK, WHITE), fg_color='transparent', border_width=2, command=lambda: training_page(self), anchor="w")
        self.training_btn.place(
            relwidth=0.95, relheight=0.05, relx=0.5, rely=0.55, anchor=CENTER)
        
        self.about_btn = customtkinter.CTkButton(master=self.side_panel_settings, text='About EIRA', image=self.robot_img, font=customtkinter.CTkFont(
            size=16), text_color=(BLACK, WHITE), fg_color='transparent', border_width=2, command=lambda: about(), anchor="w")
        self.about_btn.place(
            relwidth=0.95, relheight=0.05, relx=0.5, rely=0.65, anchor=CENTER)
        
        self.home_btn = customtkinter.CTkButton(master=self.side_panel_settings, text='Home', image=self.home_img, font=customtkinter.CTkFont(
            size=16),text_color=(BLACK, WHITE),  fg_color='transparent', border_width=2, command=lambda: self.home(), anchor="w")
        self.home_btn.place(
            relwidth=0.95, relheight=0.05, relx=0.5, rely=0.95, anchor=CENTER)

    def back(self, dest: str) -> None:
        if dest == 'login':
            try:
                self.frame_login.destroy()
            except:
                pass
            self.login_page(None)

        if dest == 'home':
            try:
                self.frame_login.destroy()
            except:
                pass
            try:
                self.frame_settings.destroy()
            except:
                pass
            self.home()
 
    def switch(self, page: str) -> None:
        if page == 'login':
            try:
                self.frame_home.destroy()
            except:
                pass
        if page == 'settings':
            try:
                self.frame_login.destroy()
            except:
                pass
        if page == 'add_data':
            try:
                self.del_data_btn.configure(fg_color='transparent')
                self.change_pass_btn.configure(fg_color='transparent')
                self.system_setting_btn.configure(fg_color='transparent')
                self.training_btn.configure(fg_color='transparent')
                self.about_btn.configure(fg_color='transparent')
                self.add_data_btn.configure(fg_color=Color_theme)
                self.update_data_btn.configure(fg_color='transparent')
            except:
                pass
        if page == 'del_data':
            try:
                self.update_data_btn.configure(fg_color='transparent')
                self.add_data_btn.configure(fg_color='transparent')
                self.change_pass_btn.configure(fg_color='transparent')
                self.system_setting_btn.configure(fg_color='transparent')
                self.training_btn.configure(fg_color='transparent')
                self.about_btn.configure(fg_color='transparent')
                self.del_data_btn.configure(fg_color=Color_theme)
            except:
                pass
        if page == 'up_data' :
            try:
                self.add_data_btn.configure(fg_color='transparent')
                self.change_pass_btn.configure(fg_color='transparent')
                self.system_setting_btn.configure(fg_color='transparent')
                self.training_btn.configure(fg_color='transparent')
                self.about_btn.configure(fg_color='transparent')
                self.del_data_btn.configure(fg_color='transparent')
                self.update_data_btn.configure(fg_color=Color_theme)
            except:
                pass
        if page == 'change_pass':
            try:
                self.update_data_btn.configure(fg_color='transparent')
                self.del_data_btn.configure(fg_color='transparent')
                self.add_data_btn.configure(fg_color='transparent')
                self.system_setting_btn.configure(fg_color='transparent')
                self.training_btn.configure(fg_color='transparent')
                self.about_btn.configure(fg_color='transparent')
                self.change_pass_btn.configure(fg_color=Color_theme)
            except:
                pass
        if page == 'system_settings' :
            try :
                self.update_data_btn.configure(fg_color='transparent')
                self.del_data_btn.configure(fg_color='transparent')
                self.add_data_btn.configure(fg_color='transparent')
                self.change_pass_btn.configure(fg_color='transparent')
                self.about_btn.configure(fg_color='transparent')
                self.training_btn.configure(fg_color='transparent')
                self.system_setting_btn.configure(fg_color=Color_theme)
            except:
                pass
        if page == 'about' :
            try :
                self.update_data_btn.configure(fg_color='transparent')
                self.del_data_btn.configure(fg_color='transparent')
                self.add_data_btn.configure(fg_color='transparent')
                self.change_pass_btn.configure(fg_color='transparent')
                self.system_setting_btn.configure(fg_color='transparent')
                self.training_btn.configure(fg_color='transparent')
                self.about_btn.configure(fg_color=Color_theme)
            except:
                pass
        if page == 'training_page' :
            try :
                self.update_data_btn.configure(fg_color='transparent')
                self.del_data_btn.configure(fg_color='transparent')
                self.add_data_btn.configure(fg_color='transparent')
                self.change_pass_btn.configure(fg_color='transparent')
                self.system_setting_btn.configure(fg_color='transparent')
                self.about_btn.configure(fg_color='transparent')
                self.training_btn.configure(fg_color=Color_theme)
            except:
                pass 

    
if __name__ == "__main__":
    app = App()
    app.window.mainloop()
