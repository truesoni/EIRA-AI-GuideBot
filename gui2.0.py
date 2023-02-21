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




'''Graphical Variables'''
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue") 

'''System Variables'''
geometry = "1400x720"
title = "EIRA - An AI GuideBot"
CENTER = tkinter.CENTER

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

texture = "black_texture.png"
texture2 = "black_texture_2.png"

folder_name = "assets"

'''Colors'''
RED   = "#FF0000"
GREEN = "#00FF00"
BLUE  = "#0000FF"
WHITE = "#FFFFFF"
BLACK = "#000000"
LIGHT_GREY = "#D3D3D3"
DARK_GREY  = "#222222"
AQUA = "#00FFFF"
LIGHT_BLUE = "#1da2dc"

Color_theme = LIGHT_BLUE


'''FONTS'''


'''System Texts'''

PASSWORD = ""
MASTER_PASSWORD = ""
with open(json_file, "r") as f:
    data = json.load(f)
    PASSWORD = data["essentials"]["password"]
    MASTER_PASSWORD = data["essentials"]["master"]   


class Mydb :
    '''
    Database class
    '''
    def __init__(self) -> None:
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def load_data(self, tag :str) -> str:
        self.cursor.execute (f"""
        SELECT * from data_table 
        WHERE tag = '{tag}';
        """)
    
        res = self.cursor.fetchall()
        try :
            return res[0][2]
        except IndexError :
            return "No such tag"
    
    def load_data_system(self, tag: str) -> str :
        self.cursor.execute (f"""
        SELECT * from system_table 
        WHERE tag = '{tag}';
        """)

        res = self.cursor.fetchall()
        try :
            return res[0][1]
        except IndexError :
            return "No such tag"

    def insert_data(self, tag: str, pattern: str, response: str)  :
        self.cursor.execute(f"""
        INSERT INTO data_table VALUES 
        ('{tag}', '{pattern}', '{response}');
        """)

        self.connection.commit() 
    
    def insert_data_system(self, tag: str, value: str) :
        self.cursor.execute(f"""
        INSERT INTO system_table VALUES 
        ('{tag}', '{value}');
        """)
        
        self.connection.commit() 

    def delete_data(self, tag: str) -> None :
        self.cursor.execute(f"""
        DELETE from data_table 
        WHERE tag = '{tag}';
        """)
        self.connection.commit()
    
    def update_data(self, tag: str, value: str) -> None :
        self.cursor.execute(f"""
        UPDATE system_table 
        SET value = '{value}'
        WHERE tag = '{tag}'
        """)
        self.connection.commit()
    
    def get_tags(self) -> list :
        self.cursor.execute("""
        SELECT tag from data_table;
        """)

        l = self.cursor.fetchall()
        res = []
        try :
            for li in l :
                li = list(li)
                res.append(li[0])
        except IndexError :
            pass
        return res
    
    def get_responses(self, tag: str) -> list :
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
        except IndexError :
            return []
        return res
    
    def get_patterns(self, tag: str) -> list :
        self.cursor.execute(f"""
        SELECT patterns from data_table
        WHERE tag = '{tag}'
        """)
        l = self.cursor.fetchall()
        try :
            s = list(l[0])[0]
            res = s.split('&')
            res.reverse()
            res.pop()
        except IndexError :
            return []
        return res
    
class App :
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
        
        '''IMAGE LOADINGS'''
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), folder_name)
        self.red_blip_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, red_blip)), size=(20, 20))
        self.green_blip_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, green_blip)), size=(20, 20))
        self.settings_img = customtkinter.CTkImage(light_image = Image.open(os.path.join(image_path, settings_icon_black)), dark_image=Image.open(os.path.join(image_path, settings_icon_white)), size=(25,25))
        self.back_btn_img = customtkinter.CTkImage(dark_image = Image.open(os.path.join(image_path, back_btn_ico_w)), light_image = Image.open(os.path.join(image_path, back_btn_ico_b)), size=(25,25))
        self.eira_logo_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, eira_logo)), size = (400,140))
        self.lock_img = customtkinter.CTkImage(dark_image = Image.open(os.path.join(image_path, lock_icon_white)), light_image=Image.open(os.path.join(image_path, lock_icon_black)), size=(100,100))
        self.college_logo_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, college_logo)), size = (200,100))
        self.texture_black = customtkinter.CTkImage(Image.open(os.path.join(image_path, texture)), size= (1600, 900))
        self.key_img = customtkinter.CTkImage(dark_image = Image.open(os.path.join(image_path, key_white)), light_image=Image.open(os.path.join(image_path, key_black)), size=(25,25))
        self.sys_img = customtkinter.CTkImage(dark_image = Image.open(os.path.join(image_path, sys_white)), light_image=Image.open(os.path.join(image_path, sys_black)), size=(25,25))
        self.robot_img = customtkinter.CTkImage(dark_image = Image.open(os.path.join(image_path, robot_white)), light_image=Image.open(os.path.join(image_path, robot_black)), size=(25,25))
        self.home_img = customtkinter.CTkImage(dark_image = Image.open(os.path.join(image_path, home_white)), light_image=Image.open(os.path.join(image_path, home_black)), size=(25,25))
        self.delete_img = customtkinter.CTkImage(dark_image = Image.open(os.path.join(image_path, delete_white)), light_image=Image.open(os.path.join(image_path, delete_black)), size=(25,25))
        self.add_img = customtkinter.CTkImage(dark_image = Image.open(os.path.join(image_path, add_white)), light_image=Image.open(os.path.join(image_path, add_black)), size=(25,25))
        self.transparent = customtkinter.CTkImage(Image.open(os.path.join(image_path, transparent)), size= (1600, 900))
        self.texture_black_2 = customtkinter.CTkImage(Image.open(os.path.join(image_path, texture2)), size= (1600, 900))
        
                
        self.home()
        #self.settings_page()
    
    def home(self) -> None :
        
        
        '''PLACINGS'''
        self.frame_home = customtkinter.CTkFrame(master = self.window)
        self.frame_home.place(relwidth = 1, relheight = 1, relx = 0.5, rely = 0.5, anchor = CENTER)

        self.blip = customtkinter.CTkLabel(master=self.frame_home, text="", width=50, image=self.red_blip_img)
        self.blip.place(relheight= 0.05, relwidth=0.05, rely=0.01, relx=0.001)

        self.settings_btn = customtkinter.CTkButton(master=self.frame_home, image=self.settings_img, text="", fg_color='transparent')
        self.settings_btn.place(relheight= 0.05, relwidth=0.035, rely=0.01, relx=0.91)

        self.login_btn = customtkinter.CTkButton(master=self.frame_home, text="Login", command=lambda:self.login_page(None))
        self.login_btn.place(relheight= 0.05, relwidth=0.035, rely=0.01, relx=0.95)
        
    def login_page(self, event) -> None:
        
        self.switch('login')
        
        def login_chk(event, state:str) :
            '''
            Checks validity of password

            '''
            password = self.pass_entry.get()
            if state == 'n' :
                if password == PASSWORD : 
                    self.settings_page()
                else :
                    self.invalid_label = customtkinter.CTkLabel(master = self.frame_login, text = "Incorrect Password", text_color= RED, fg_color= 'transparent')
                    self.invalid_label.place(x = 105, y = 163, anchor = CENTER)
            if state == 'f' :
                if password == MASTER_PASSWORD : 
                    self.settings_page()
                else :
                    self.invalid_label = customtkinter.CTkLabel(master = self.frame_login, text = "Incorrect Password", text_color= RED, fg_color= 'transparent')
                    self.invalid_label.place(x = 200, y = 325, anchor = CENTER)

        def forget_pass_page() :
            self.college_logo_label.destroy()
            try:
                self.invalid_label.destroy()
            except :
                pass
            self.pass_entry.configure(placeholder_text="Enter Master Password")
            self.pass_entry.place(x = 200, y = 375, anchor = CENTER)

            self.login_chk_btn.configure(command = lambda: login_chk(None, 'f'))
            self.login_chk_btn.place(x = 200, y = 425, anchor = CENTER)

            self.forgot_pass_btn.configure(text = "Back to Log in", command = lambda : self.back('login'))
            self.forgot_pass_btn.place(x = 200, y = 475)

            self.lock_label = customtkinter.CTkLabel(master = self.frame_login, text = '', image=self.lock_img, fg_color='transparent')
            self.lock_label.place(x = 200, y = 200, anchor = CENTER)

            self.sub_label = customtkinter.CTkLabel(master = self.frame_login, text = 'Trouble with logging in? \n Enter Master Password to continue.', text_color=(DARK_GREY, LIGHT_GREY), fg_color='transparent')
            self.sub_label.place(x = 200, y = 275, anchor = CENTER)
        
        
        self.frame_login = customtkinter.CTkFrame(master=self.window, width = 400, height=500, corner_radius=15)
        self.frame_login.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        self.login_label = customtkinter.CTkLabel(master=self.frame_login, text="", image=self.eira_logo_img, fg_color='transparent', corner_radius=15)
        self.login_label.place(x = 200, y = 70, anchor = CENTER)

        self.back_button = customtkinter.CTkButton(master= self.window, image = self.back_btn_img, text = "", command=lambda:self.back('home'), fg_color='transparent')
        self.back_button.place(relheight= 0.05, relwidth=0.05, rely=0.01, relx=0.001)

        self.pass_entry = customtkinter.CTkEntry(master = self.frame_login, width = 300, height=45, corner_radius=5, placeholder_text="Enter Admin Password", show = '*',
                                                  placeholder_text_color=(LIGHT_GREY, AQUA))
        self.pass_entry.place(x = 200, y = 200, anchor = CENTER)
        
        self.login_chk_btn = customtkinter.CTkButton(master = self.frame_login, text="Log in", width=300, height=40,command=lambda:login_chk(None, 'n'))
        self.login_chk_btn.place(x = 200, y = 250, anchor = CENTER)

        self.forgot_pass_btn = customtkinter.CTkButton(master = self.frame_login, text = "Forgotten your password?", fg_color= 'transparent', text_color= LIGHT_GREY, command=lambda: forget_pass_page())
        self.forgot_pass_btn.place(x = 200, y = 450, anchor = CENTER)
        
        self.college_logo_label = customtkinter.CTkLabel(master = self.frame_login, text = '', image = self.college_logo_img, fg_color='transparent')
        self.college_logo_label.place(x = 200, y = 350, anchor = CENTER)
        
    def settings_page(self) -> None:
        self.switch('settings')
        
        def add_data() :
            self.switch('add_data')
            self.TAG_N = ""
            self.PATTERN_N = ""
            self.RESPONSE_N = ""
            def check_tag() :
                tags = self.db.get_tags()  

                tag = self.tag_txt_entry.get()
                
                if tag not in tags and len(tag) != 0 :
                    self.tag_validity_label.configure(text = 'Valid Tag', text_color = GREEN)
                    self.tag_validity_label.place(relx = 0.04, rely = 0.17, anchor = 'w')
                    self.tag_validity_label.update()
                    self.pattern_add_btn.configure(state =   'normal')
                    self.response_add_btn.configure(state =  'normal')
                    self.save_data_btn.configure(state =     'normal')
                    self.tag_txt_entry.configure(state = 'readonly')
                    self.tag_chk_btn.configure(text_color = GREEN, command = None)
                    
                    self.TAG_N = tag
                    
                    self.add_data_textbox.configure(state = 'normal')
                    self.add_data_textbox.insert(customtkinter.END, f'\"TAG\" :    {self.TAG_N} \n\n')
                    self.add_data_textbox.configure(state = 'disabled')
                    

                    

                else :
                    if tag in tags :
                        self.tag_validity_label.configure(text = 'Tag already in database', text_color = RED)
                    if len(tag) == 0 :
                        self.tag_validity_label.configure(text = 'Invalid Tag', text_color = RED)

                    self.tag_validity_label.place(relx = 0.04, rely = 0.17, anchor = 'w')
                    self.tag_validity_label.update()
                    self.tag_chk_btn.configure(text_color = RED)
                
            def insert_tags() :
                tag_disp_textbox.configure(state = 'normal')
                tags = self.db.get_tags()  
                tag_disp_textbox.insert(customtkinter.END, '\"TAGS\" - \n\n')

                for i, tag in enumerate(tags, 1) :
                    tag_disp_textbox.insert(customtkinter.END, f'({i}) : {tag} \n')

                tag_disp_textbox.configure(state = 'disabled')
             
            def add_pattern() :
                pattern = self.pattern_txt_entry.get()

                if len(pattern) :
                    self.PATTERN_N = self.PATTERN_N + '&' + pattern 
                    self.pattern_txt_entry.delete(0, customtkinter.END)
                    self.pattern_validity_label.configure(text = "Valid Pattern", text_color = GREEN)
                    self.pattern_validity_label.place(relx = 0.04, rely = 0.35, anchor = 'w')
                 
                    self.add_data_textbox.configure(state = 'normal')
                    self.add_data_textbox.insert(customtkinter.END, f'\"Pattern\" :    {pattern} \n\n')
                    self.add_data_textbox.configure(state = 'disabled')
    
                else :
                    self.pattern_validity_label.configure(text = "Please enter valid Pattern", text_color = RED)
                    self.pattern_validity_label.place(relx = 0.04, rely = 0.35, anchor = 'w')

            def add_response() :
                response = self.response_txt_entry.get()

                if len(response) :
                    self.RESPONSE_N = self.RESPONSE_N + '&' + response 
                    self.response_txt_entry.delete(0, customtkinter.END)
                    self.response_validity_label.configure(text = "Valid Response", text_color = GREEN)
                    self.response_validity_label.place(relx = 0.04, rely = 0.53, anchor = 'w')
                    
                    self.add_data_textbox.configure(state = 'normal')
                    self.add_data_textbox.insert(customtkinter.END, f'\"Response\" :    {response} \n\n')
                    self.add_data_textbox.configure(state = 'disabled')
                else :
                    self.response_validity_label.configure(text = "Please enter valid Response", text_color = RED)
                    self.response_validity_label.place(relx = 0.04, rely = 0.53, anchor = 'w')

            def save_data() :
                if len(self.PATTERN_N) == 0 :
                    self.save_validity_label.configure(text = 'Please Enter Pattern', text_color = RED)
                    self.save_validity_label.place(relx = 0.19, rely = 0.63, anchor = 'w')
                    self.pattern_txt_entry.focus()
                    return
                if len(self.RESPONSE_N) == 0 :
                    self.save_validity_label.configure(text = 'Please Enter Response', text_color = RED)
                    self.save_validity_label.place(relx = 0.19, rely = 0.63, anchor = 'w')
                    self.response_txt_entry.focus()
                    return
                choice = open_dialog("Do you want to save changes to the database?")

                if choice.lower() == "yes" :
                    self.db.insert_data(tag=self.TAG_N, pattern=self.PATTERN_N, response=self.RESPONSE_N)
                    
                    
                    self.save_validity_label.configure(text = 'DATA SAVED', text_color = GREEN)
                    self.save_validity_label.place(relx = 0.19, rely = 0.63, anchor = 'w')
                    self.window.update()
                    time.sleep(1)
                    reset()
                else :
                    self.save_validity_label.configure(text = 'DATA NOT SAVED', text_color = RED)
                    self.save_validity_label.place(relx = 0.19, rely = 0.63, anchor = 'w')
                
            def reset() :
                self.TAG_N = ""
                self.PATTERN_N = ""
                self.RESPONSE_N = ""
                add_data()

            def open_dialog(text: str) -> str :
                dialog = customtkinter.CTkInputDialog(text=f"{text}", title="Save? (YES/NO)")
                return dialog.get_input()
          
            def pop_up() -> None :
                self.pop_up = customtkinter.CTkLabel(master=self.frame_add_data, text="DATA SAVED", text_color=GREEN, width=320, height=180, bg_color=DARK_GREY, fg_color=DARK_GREY, corner_radius=10,font=customtkinter.CTkFont(size=20))
        
                self.pop_up.place(relx = 0.5, rely = 0.5, anchor = CENTER)
                self.window.update()
                time.sleep(1.5)
                reset()
                

            self.add_data_btn.configure(fg_color = Color_theme)

            self.frame_add_data = customtkinter.CTkFrame(master= self.frame_settings)
            self.frame_add_data.place(relheight = 1, relwidth = 0.84, relx = 0.578, rely = 0.5, anchor = CENTER)          

            self.tag_label = customtkinter.CTkLabel(master= self.frame_add_data, text="Enter Tag", height = 45,fg_color = (DARK_GREY), bg_color='transparent',
                                                     font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.tag_label.place(relwidth = 0.2, relx = 0.136, rely = 0.05, anchor = CENTER)
            self.tag_txt_entry = customtkinter.CTkEntry(master= self.frame_add_data, height = 45, placeholder_text='Enter Unique tag')
            self.tag_txt_entry.place( relwidth = 0.2, relx = 0.136, rely = 0.12, anchor = CENTER)
            self.tag_chk_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Check", width=100, height = 45, border_color=WHITE,border_width=2,
                                                    fg_color='transparent',font=customtkinter.CTkFont(size=14), command=lambda:check_tag())
            self.tag_chk_btn.place(relx = 0.28, rely = 0.12, anchor = CENTER)


            self.pattern_label = customtkinter.CTkLabel(master= self.frame_add_data, text="Enter Pattern", width = 150, height = 45,fg_color = (DARK_GREY), bg_color='transparent',
                                                     font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.pattern_label.place(relwidth = 0.2, relx = 0.136, rely = 0.23, anchor = CENTER)
            self.pattern_txt_entry = customtkinter.CTkEntry(master= self.frame_add_data, height = 45, placeholder_text='Enter Pattern')
            self.pattern_txt_entry.place( relwidth = 0.2, relx = 0.136, rely = 0.30, anchor = CENTER)
            self.pattern_add_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Add", width=100, height = 45, border_color=WHITE,border_width=2,
                                                     fg_color='transparent',font=customtkinter.CTkFont(size=14), command=lambda:add_pattern(),state='disabled')
            self.pattern_add_btn.place(relx = 0.28, rely = 0.30, anchor = CENTER)
            
            
            self.response_label = customtkinter.CTkLabel(master= self.frame_add_data, text="Enter Response", width = 150, height = 45,fg_color = (DARK_GREY), bg_color='transparent',                             
                                                         font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.response_label.place(relwidth = 0.2, relx = 0.136, rely = 0.41, anchor = CENTER)
            self.response_txt_entry = customtkinter.CTkEntry(master= self.frame_add_data, height = 45, placeholder_text='Enter Response')
            self.response_txt_entry.place( relwidth = 0.2, relx = 0.136, rely = 0.48, anchor = CENTER)
            self.response_add_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Add", width=100, height = 45, border_color=WHITE,border_width=2,
                                                     fg_color='transparent',font=customtkinter.CTkFont(size=14), command=lambda:add_response(),state='disabled')
            self.response_add_btn.place(relx = 0.28, rely = 0.48, anchor = CENTER)
          

            self.save_data_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Save", width=150, height = 45 ,border_width=2,
                                                     text_color= GREEN, fg_color='transparent',font=customtkinter.CTkFont(size=14), command=lambda:save_data(),state='disabled')
            self.save_data_btn.place(relx = 0.24, rely = 0.58, anchor = CENTER)
        
            self.reset_btn = customtkinter.CTkButton(master=self.frame_add_data, text="Reset", width=150, height = 45, border_width=2,
                                                     text_color= RED, fg_color=('transparent'),font=customtkinter.CTkFont(size=14), command=lambda:reset())
            self.reset_btn.place(relx = 0.1, rely = 0.58, anchor = CENTER)

            self.tag_validity_label = customtkinter.CTkLabel(master=self.frame_add_data)
            self.pattern_validity_label = customtkinter.CTkLabel(master=self.frame_add_data)
            self.response_validity_label = customtkinter.CTkLabel(master=self.frame_add_data)
            self.save_validity_label = customtkinter.CTkLabel(master=self.frame_add_data)
            
            self.add_data_textbox = customtkinter.CTkTextbox(master=self.frame_add_data,  state= 'disabled', font=customtkinter.CTkFont(size=14))
            self.add_data_textbox.place(relwidth = 0.4, relheight = 0.9, relx = 0.35, rely = 0.54, anchor = 'w')

            self.add_data_table_label = customtkinter.CTkLabel(master= self.frame_add_data, text="Your data Appears here", height = 45,fg_color = (DARK_GREY), bg_color='transparent',
                                                     font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.add_data_table_label.place(relwidth = 0.2, relx = 0.45, rely = 0.05, anchor = 'w')

            tag_disp_textbox = customtkinter.CTkTextbox(master=self.frame_add_data, state = 'disabled', font=customtkinter.CTkFont(size=14) )
            tag_disp_textbox.place(relwidth = 0.2, relheight = 0.9, relx = 0.77, rely = 0.54, anchor = 'w')
            
           
            

            self.tag_table_label = customtkinter.CTkLabel(master= self.frame_add_data, text="Tags in Database", height = 45,fg_color = (DARK_GREY), bg_color='transparent',
                                                     font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.tag_table_label.place(relwidth = 0.2, relx = 0.77, rely = 0.05, anchor = 'w')
            insert_tags()

        def del_data() :
            self.switch('del_data')
            def check_tag() :
                tags = self.db.get_tags()  

                tag = self.tag_txt_entry.get()
                
                if tag in tags and len(tag) != 0 :
                    self.tag_validity_label.configure(text = 'Valid Tag', text_color = GREEN)
                    self.tag_validity_label.place(relx = 0.04, rely = 0.17, anchor = 'w')
                    self.tag_validity_label.update()
                    
                    self.tag_txt_entry.configure(state = 'readonly')
                    self.tag_chk_btn.configure(text_color = GREEN, command = None)
                    self.del_data_textbox.configure(state = 'normal')
                    self.del_data_textbox.insert(customtkinter.END, f"Tag  :   {tag}\n")
                    self.del_data_textbox.configure(state = 'disabled')
                    self.delete_btn.configure(state = 'normal')

                    insert_data(tag) 
                   
                else :
                    if tag not in tags :
                        self.tag_validity_label.configure(text = 'Tag not in database', text_color = RED)
                    if len(tag) == 0 :
                        self.tag_validity_label.configure(text = 'Invalid Tag', text_color = RED)

                    self.tag_validity_label.place(relx = 0.04, rely = 0.17, anchor = 'w')
                    self.tag_validity_label.update()
                    self.tag_chk_btn.configure(text_color = RED)
            
            def del_data_fun() :
                
                tag = self.tag_txt_entry.get()
                choice = open_dialog(tag)

                if choice.lower() == "yes" :

                    self.db.delete_data(tag)
                    
                    self.del_validity_label.configure(text = 'DATA DELETED', text_color = GREEN)
                    self.del_validity_label.place(relx = 0.2, rely = 0.28, anchor = 'w')
                    self.window.update()
                    time.sleep(1)
                    reset()
                else :
                    self.save_validity_label.configure(text = 'DATA NOT DELETED', text_color = RED)
                    self.save_validity_label.place(relx = 0.2, rely = 0.28, anchor = 'w')

            def insert_tags() :
                tag_disp_textbox.configure(state = 'normal')
                tags = self.db.get_tags()  
                tag_disp_textbox.insert(customtkinter.END, '\"TAGS\" - \n\n')

                for i, tag in enumerate(tags, 1) :
                    tag_disp_textbox.insert(customtkinter.END, f'({i}) : {tag} \n')

                tag_disp_textbox.configure(state = 'disabled')
            
            def insert_data(tag: str) :
                self.del_data_textbox.configure(state = 'normal')
                
                patterns = self.db.get_patterns(tag)
                responses = self.db.get_responses(tag)

                self.del_data_textbox.configure(state = 'normal')

                for i, pattern in enumerate(patterns, 1) :
                    self.del_data_textbox.insert(customtkinter.END, f"\nPattern  #{i} :   {pattern}\n")
                
                for i, response in enumerate(responses, 1) :
                    self.del_data_textbox.insert(customtkinter.END, f"\nResponse #{i} :   {response}\n")
                    
                self.del_data_textbox.configure(state = 'disabled')

            def insert_all_data() :
                
                self.all_data_textbox.configure(state = 'normal')

                tags = self.db.get_tags()

                for i, tag in enumerate(tags, 1) :
                    self.all_data_textbox.insert(customtkinter.END, f"\nTag  #{i} :   {tag}\n")
                    
                    patterns = self.db.get_patterns(tag)
                    responses = self.db.get_responses(tag)
                    for j, pattern in enumerate(patterns, 1) :
                        self.all_data_textbox.insert(customtkinter.END, f"\nPattern  #{j} :   {pattern}\n")
                
                    for k, response in enumerate(responses, 1) :
                        self.all_data_textbox.insert(customtkinter.END, f"\nResponse #{k} :   {response}\n")
                    
                    self.all_data_textbox.insert(customtkinter.END, '__'*25 + '\n')
                    
                
                self.all_data_textbox.configure(state = 'disabled')
                    

            def open_dialog(text: str) -> str :
                dialog = customtkinter.CTkInputDialog(text=f"This action cannot be UNDONE.\nAre you sure you want to delete this record.\n TAG : {text}", title="DELETE? (YES/NO)")
                return dialog.get_input()
            
            def reset():
                del_data()
                
            
                
           

            
            self.frame_del_data = customtkinter.CTkFrame(master= self.frame_settings)
            self.frame_del_data.place(relheight = 1, relwidth = 0.84, relx = 0.578, rely = 0.5, anchor = CENTER)    
            
            self.tag_label = customtkinter.CTkLabel(master= self.frame_del_data, text="Enter Tag", height = 45,fg_color = (DARK_GREY), bg_color='transparent',
                                                     font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.tag_label.place(relwidth = 0.2, relx = 0.136, rely = 0.05, anchor = CENTER)
            self.tag_txt_entry = customtkinter.CTkEntry(master= self.frame_del_data, height = 45, placeholder_text='Enter tag from database')
            self.tag_txt_entry.place( relwidth = 0.2, relx = 0.136, rely = 0.12, anchor = CENTER)
            self.tag_chk_btn = customtkinter.CTkButton(master=self.frame_del_data, text="Check", width=100, height = 45, border_color=WHITE,border_width=2,
                                                    fg_color='transparent',font=customtkinter.CTkFont(size=14), command=lambda:check_tag())
            self.tag_chk_btn.place(relx = 0.28, rely = 0.12, anchor = CENTER)       

            self.del_data_label = customtkinter.CTkLabel(master= self.frame_del_data, text="Data to be deleted", height = 45,fg_color = (DARK_GREY), bg_color='transparent',
                                                     font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.del_data_label.place(relwidth = 0.3, relx = 0.03, rely = 0.35, anchor = 'w')

            self.del_data_textbox = customtkinter.CTkTextbox(master=self.frame_del_data,  state= 'disabled', font=customtkinter.CTkFont(size=14))
            self.del_data_textbox.place(relwidth = 0.3, relheight = 0.5, relx = 0.03, rely = 0.7, anchor = 'w')

            self.all_data_textbox = customtkinter.CTkTextbox(master=self.frame_del_data,  state= 'disabled', font=customtkinter.CTkFont(size=14))
            self.all_data_textbox.place(relwidth = 0.4, relheight = 0.9, relx = 0.35, rely = 0.54, anchor = 'w')
            insert_all_data()
            self.del_data_table_label = customtkinter.CTkLabel(master= self.frame_del_data, text="Your data Appears here", height = 45,fg_color = (DARK_GREY), bg_color='transparent',
                                                     font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.del_data_table_label.place(relwidth = 0.2, relx = 0.45, rely = 0.05, anchor = 'w')

            tag_disp_textbox = customtkinter.CTkTextbox(master=self.frame_del_data, state = 'disabled', font=customtkinter.CTkFont(size=14) )
            tag_disp_textbox.place(relwidth = 0.2, relheight = 0.9, relx = 0.77, rely = 0.54, anchor = 'w')
            insert_tags() 
           
            self.tag_validity_label = customtkinter.CTkLabel(master=self.frame_del_data)

            self.delete_btn = customtkinter.CTkButton(master=self.frame_del_data, text="DELETE", width=150, height = 45 ,border_width=2,
                                                     text_color= RED, fg_color='transparent',font=customtkinter.CTkFont(size=14), command=lambda:del_data_fun(),state='disabled')
            self.delete_btn.place(relx = 0.24, rely = 0.23, anchor = CENTER)
        
            self.reset_btn = customtkinter.CTkButton(master=self.frame_del_data, text="Reset", width=150, height = 45, border_width=2,
                                                     text_color= RED, fg_color=('transparent'),font=customtkinter.CTkFont(size=14), command=lambda:reset())
            self.reset_btn.place(relx = 0.1, rely = 0.23, anchor = CENTER)

            self.tag_table_label = customtkinter.CTkLabel(master= self.frame_del_data, text="Tags in Database", height = 45,fg_color = (DARK_GREY), bg_color='transparent',
                                                     font=customtkinter.CTkFont(size=14), text_color = Color_theme, corner_radius=5 )
            self.tag_table_label.place(relwidth = 0.2, relx = 0.77, rely = 0.05, anchor = 'w')      
            self.del_validity_label = customtkinter.CTkLabel(master=self.frame_del_data)

        def change_pass() :
            self.switch('change_pass')

            self.frame_cp = customtkinter.CTkFrame(master= self.frame_settings)
            self.frame_cp.place(relheight = 1, relwidth = 0.84, relx = 0.578, rely = 0.5, anchor = CENTER)    
            
            

        
        def system_setting() :
            def change_scaling_event(self, new_scaling: str):
                new_scaling_float = int(new_scaling.replace("%", "")) / 100
                customtkinter.set_widget_scaling(new_scaling_float)
                
        def about() :
            pass
        
        '''Database Object'''
        self.db = Mydb()
        
        self.frame_settings = customtkinter.CTkFrame(master=self.window)
        self.frame_settings.place(relheight = 1, relwidth = 1, anchor = CENTER, relx = 0.5, rely = 0.5)
        
        self.side_panel_settings = customtkinter.CTkFrame(master = self.frame_settings)
        self.side_panel_settings.place(relheight = 1, relwidth = 0.15, relx = 0.08, rely = 0.5, anchor = CENTER)        

        self.add_data_btn = customtkinter.CTkButton(master = self.side_panel_settings, text= 'Add Data', image=self.add_img, font=customtkinter.CTkFont(size=16),fg_color='transparent', border_width=2, command=lambda: add_data(), anchor="w")
        self.add_data_btn.place(relwidth = 0.95, relheight = 0.05, relx = 0.5, rely = 0.05, anchor = CENTER)

        self.del_data_btn = customtkinter.CTkButton(master = self.side_panel_settings, text= 'Delete Data', image=self.delete_img, font=customtkinter.CTkFont(size=16),fg_color='transparent', border_width=2, command=lambda: del_data(),anchor="w")
        self.del_data_btn.place(relwidth = 0.95, relheight = 0.05, relx = 0.5, rely = 0.15, anchor = CENTER)

        self.change_pass_btn = customtkinter.CTkButton(master = self.side_panel_settings, text= 'Change Password', image=self.key_img, font=customtkinter.CTkFont(size=16),fg_color='transparent', border_width=2, command=lambda: change_pass(), anchor="w")
        self.change_pass_btn.place(relwidth = 0.95, relheight = 0.05, relx = 0.5, rely = 0.25, anchor = CENTER)

        self.system_setting_btn =  customtkinter.CTkButton(master = self.side_panel_settings,image=self.sys_img, text= 'System', font=customtkinter.CTkFont(size=16),fg_color='transparent', border_width=2, command=lambda: system_setting(), anchor="w")
        self.system_setting_btn.place(relwidth = 0.95, relheight = 0.05, relx = 0.5, rely = 0.35, anchor = CENTER)

        self.about_btn = customtkinter.CTkButton(master = self.side_panel_settings, text= 'About EIRA', image=self.robot_img, font=customtkinter.CTkFont(size=16),fg_color='transparent', border_width=2, command=lambda: about(), anchor="w")
        self.about_btn.place(relwidth = 0.95, relheight = 0.05, relx = 0.5, rely = 0.45, anchor = CENTER)
        
    def back(self, dest: str) -> None:
        if dest == 'login' :
            try :
                self.frame_login.destroy()
            except :
                pass
            self.login_page(None)
        
        if dest == 'home' :
            try :
                self.frame_login.destroy()
            except :
                pass
            try :
                self.frame_settings.destroy()
            except :
                pass
            self.home()

    def switch(self, page: str) -> None:
        if page == 'login' :
            try :
                self.frame_home.destroy()
            except :
                pass
        if page == 'settings' :
            try :
                self.frame_login.destroy()
            except :
                pass
        if page == 'add_data' :
            try :
                self.add_data_btn.configure(fg_color = Color_theme)
                self.del_data_btn.configure(fg_color = 'transparent')
                self.change_pass_btn.configure(fg_color = 'transparent')
            except :
                pass
        if page == 'del_data' :
            try :
                self.del_data_btn.configure(fg_color = Color_theme)
                self.add_data_btn.configure(fg_color = 'transparent')
                self.change_pass_btn.configure(fg_color = 'transparent')
            except :
                pass
        if page == 'change_pass' :
            try :
                self.del_data_btn.configure(fg_color = 'transparent')
                self.add_data_btn.configure(fg_color = 'transparent')
                self.change_pass_btn.configure(fg_color = Color_theme)
            except :
                pass

if __name__ == "__main__":
    app = App()
    app.window.mainloop()


