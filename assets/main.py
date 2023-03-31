import openai
import customtkinter
import urllib.request
from PIL import Image
import os


geometry = "1024x700"
title = "CreatY"
img_file = "download.png"
folder_name = "assets"
day_img = "day.png"
night_img = "night.png"
about_w = "about_w.png"
about_b = "about_b.png"
reset_ = "reset.png"
logo_w = "logo_w.png"
logo_b = "logo_b.png" 
green = "#34eb83"


class App:
    def __init__(self) -> None:
        self.window = customtkinter.CTk()
        self.window.geometry(geometry)
        self.window.title(title)
        self.window.resizable(False, False)
        self.curtheme = "light"

        customtkinter.set_appearance_mode(self.curtheme)
        customtkinter.set_default_color_theme("green")
        
        openai.api_key = open("API_KEY.txt", "r").read()


        img_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), folder_name)
        self.theme_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(img_path, day_img)), light_image=Image.open(os.path.join(img_path, night_img)), size=(25, 25))
        self.about_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(img_path, about_w)), light_image=Image.open(os.path.join(img_path, about_b)), size=(25, 25))
        self.reset_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(img_path, reset_)), light_image=Image.open(os.path.join(img_path, reset_)), size=(25, 25))
        self.logo_img = customtkinter.CTkImage(dark_image=Image.open(os.path.join(img_path, logo_w)), light_image=Image.open(os.path.join(img_path, logo_b)), size=(120, 35))


        self.home_page()

    def dwonload_img(self, image_url : str) -> None:
        
        filename = "download.png"

        req = urllib.request.build_opener()
        req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64)')]
        urllib.request.install_opener(req)

        urllib.request.urlretrieve(image_url, filename)

    def generate_img(self, text : str) -> str :
        #return "https://cdn.vox-cdn.com/thumbor/LLdAbmQsq9cBjz3dLG5IdMnVtpE=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/24323106/sd_123022.jpg"
        
        response = openai.Image.create(
            prompt=text,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        return image_url
    
    def set_img(self, event) :
        self.txt_input.configure(state = 'disabled')

        text = self.txt_input.get()
        
        generated_img_url = self.generate_img(text)

        self.dwonload_img(generated_img_url)
         
        image_path = os.path.dirname(os.path.realpath(__file__))
        
        self.gen_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, img_file)), size=(512, 512))

        self.frame_header = customtkinter.CTkFrame(master = self.frame_home, height = 45, corner_radius = 5, border_width = 2)
        self.frame_header.place(relx = 0.5, rely = 0.2, relwidth = 0.5, anchor = 'center')

        self.image_header = customtkinter.CTkLabel(master = self.frame_header, text = text, height = 45, corner_radius = 2)

        self.image_header.place(relx = 0.5, rely = 0.5, relwidth = 0.9, relheight = 0.9,anchor = 'center')


        self.image_label = customtkinter.CTkLabel(master = self.frame_image, text = "", image = self.gen_img)

        self.image_label.place(relx = 0.5, rely = 0.5, anchor = 'center')

        self.txt_input.configure(state = 'normal')

        self.reset_btn.configure(state = 'normal')



    def change_theme(self, event) :
        if self.curtheme == 'light' :
            self.curtheme= 'dark'
            customtkinter.set_appearance_mode(self.curtheme)
        elif self.curtheme == 'dark' :
            self.curtheme = 'light'
            customtkinter.set_appearance_mode(self.curtheme)


    def home_page(self):
        self.frame_home = customtkinter.CTkFrame(master = self.window)
        self.frame_home.place(relx = 0.5, rely = 0.5, relheight = 1, relwidth = 1, anchor = "center")
        
        self.logo_label = customtkinter.CTkLabel(master = self.frame_home, text = "", image = self.logo_img)
        self.logo_label.place(relx = 0.05, rely = 0.01)
        
        
        self.txt_input = customtkinter.CTkEntry(master = self.frame_home, placeholder_text = "Enter Your text here...", height = 45)
        self.txt_input.place(relx = 0.05, rely = 0.1, relwidth = 0.79, anchor = 'w')

        self.generate_btn = customtkinter.CTkButton(master = self.frame_home, height = 45, width = 150, text = "Generate", command = lambda : self.set_img(None))
        self.generate_btn.place(relx = 0.85, rely = 0.1, relwidth = 0.1, anchor = 'w')

        self.theme_btn = customtkinter.CTkButton(master = self.frame_home,text = "", height = 25, width = 25, bg_color = 'transparent' ,fg_color = 'transparent', 
                                                 image = self.theme_img, command = lambda : self.change_theme(None))

        self.theme_btn.place(relx = 0.98, rely = 0.03, anchor = 'center')


        self.about_btn = customtkinter.CTkButton(master = self.frame_home,text = "", height = 25, width = 25, bg_color = 'transparent' ,fg_color = 'transparent', 
                                                 image = self.about_img, command = lambda : self.about_page())

        self.about_btn.place(relx = 0.94, rely = 0.03, anchor = 'center')

        self.reset_btn = customtkinter.CTkButton(master = self.frame_home,text = "", height = 45, width = 45, bg_color = 'transparent' ,fg_color = 'transparent', 
                                                 border_color = green, border_width = 1,image = self.reset_img, command = lambda : self.home_page(), state = "disabled")
        
        self.reset_btn.place(relx = 0.975, rely = 0.1, anchor = 'center')

        self.frame_image = customtkinter.CTkFrame(master= self.frame_home, width=512, height=512)
        self.frame_image.place(relx = 0.5, rely = 0.6, anchor = 'center')

        self.tmp_label = customtkinter.CTkLabel(master= self.frame_image, text="Generated Image Will Appear Here...",font=customtkinter.CTkFont(size=15) )
        self.tmp_label.place(relx = 0.5, rely = 0.5, anchor = 'center')



    def about_page(self):
        
        self.frame_about = customtkinter.CTkFrame(master= self.window)



    

if __name__ == '__main__':
    app = App()
    app.window.mainloop()



