'''

    Main -  Run File


'''

import numpy as np
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import random
import json
import torch
from model import NeuralCode
import pyglet
import time
from tkinter import *
from bot_utils import *



# bot variables
idk = "I do not understand"
bot_name = "EIRA"

json_file = "database.json"

quit_txt =["quit", "OK go to sleep",
            "quit","thank you", "okay go to sleep", "sleep", "OK goto sleep", "okay thank you"]


####################################################################### NEURAL NET SECTION ###################################################

#def fun_mode()

# NORMAL MODE SECTION
def normal_mode(sentence):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open(json_file, 'r') as database:
        intents = json.load(database)

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
    
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    #if(key == 1):
     #   return
    #elif(key == 2):
    #    pass
    #elif(key == 0):
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                a = random.randint(0, (len(intent["responses"])-1))
                #print(f'{bot_name}: {(intent["responses"][a])}')
                return intent["responses"][a]
           
    else:
        return idk
        #print(f'{bot_name}: I do not Understand...')
        #talk("I do not Understand...")


########################################################################## GUI SECTION #######################################################

#variables

PASSWORD = ""
MASTER_PASSWORD = ""
with open(json_file, "r") as f:
    data = json.load(f)
    PASSWORD = data["essentials"]["password"]
    MASTER_PASSWORD = data["essentials"]["master"]   





##################################################################### VISUALS ################################################################

WIDTH = 1200
HEIGHT = 700
BG_COLOR = "#9381ff"#11c3e3" #"#34568b" #"#111111" #"#34568B""#00758fr" 
SETTING_BG = "#aed6dc"  #"#eab676"
TEXT_COLOR = "#111111"
WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#FF0000"
BLUE = "#0000FF"
GREEN = "#00FF00"

PROCESSING_COLOR = "#1e81b0"
RUN_COLOR = GREEN 
ERR_COLOR = RED


# FONTS
FONT = "Arial 14"
FONT_BOLD = "Calibri 19"

#SETTING_ICO = "F:\\EIRA\\assets\\setting.png"

####################################################################### MAIN SECTION #########################################################

class Application: 

    def __init__(self):
        self.window = Tk()
        self._main_window()
    
    def run(self):
        self.window.mainloop()
     
    def _main_window(self):
        self.window.title("EIRA")
        #self.window.iconbitmap("assets/icon.ico")
        #self.window.resizable(width = False, height = False)
        self.window.configure(width = WIDTH , height = HEIGHT, bg = BG_COLOR )

        # head title
        self.head_title = Label(self.window, bg = BG_COLOR, fg = "#FFFFFF",
                        text  ="\" Welcome To Global College \"", font = FONT_BOLD, pady = 10)
        self.head_title.place(relwidth=1)
        
        # divider
        divider = Label(self.window, width = 690, bg = TEXT_COLOR)
        divider.place(relwidth=1, rely= 0.07, relheight=0.006)    
        
        #text widget
        self.text_widget = Text(self.window,width = 20, bg = BG_COLOR,
                                fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5 )
        self.text_widget.place(relheight=0.92, relwidth=1,rely=0.08 )  
        self.text_widget.configure(cursor = "arrow", state = DISABLED)
        
        # scroll bar
        sb = Scrollbar(self.text_widget)
        sb.place(relheight=1, relx = 0.989)
        sb.configure(command=self.text_widget.yview)

        # self._insert_message("Hello Sir, You can ask me whatever you want, Please say QUIT to exit",0, "EIRA")

        # button
        self.start_button = Button(text = "Start", font=FONT_BOLD, width = 20, bg = WHITE,
                              command = lambda: self._on_enter_pressed(NONE))
        self.start_button.place(relx=0.87, rely= 0.008 , relheight=0.06, relwidth= 0.12)

        self.stop_button = Button(self.window, text = "exit", font=FONT_BOLD, command = lambda: self.window.quit())
        self.stop_button.place(relx=0.82, rely= 0.008 , relheight=0.06, relwidth= 0.04)


        # listening status run_indicator:
        self.run_indic = Label(self.window, text="Stopped", width =50, bg = BG_COLOR, 
                     fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5 )
        self.run_indic.place(relheight= 0.05, relwidth=0.1, rely=0.01, relx=0.01)
        
        
        # run_indicator run_blip 
        self.run_blip = Label(self.window, text = "",  width = 8, height = 8, bg = RED, font = FONT, padx = 5, pady = 5)
        self.run_blip.place(relheight=0.02, relwidth=0.014, rely=0.025, relx=0.011)
        
        
        # settings button
        self.settings_button = Button(self.window, text= "#",font=FONT_BOLD, command= lambda: self._password_page(NONE), borderwidth=0)
        self.settings_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.04)
     
    def _password_page(self,event):
      
        def back_to_main_window_from_pass():
            self.pass_enter_button.destroy()
            self.pass_enter_text.destroy()
            self.pass_label.destroy()
            self.window.update()
            self._main_window()
        
        def pass_check():
            try:
                password = self.pass_enter_text.get(1.0, "end-1c")
            except TclError :
                self.pass_label.configure(text="Incorrect Password", fg=RED)
                self.window.update()
                talk("Access Denied")
                self.pass_label.configure(text="Enter Password", fg = BLACK)
                    
                self.window.update()
            
            if password == PASSWORD or password == MASTER_PASSWORD:
                self.pass_label.configure(text="Correct Password", fg=GREEN)
                self.window.update()
                talk("Access Granted")
                  
                self.pass_label.destroy()
                self.pass_enter_button.destroy()
                self.pass_enter_text.destroy()
                
                self._settings_(NONE)
            else:
                self.pass_enter_text.delete(1.0, "end-1c")
                self.pass_label.configure(text="Incorrect Password", fg=RED)
                self.window.update()
                talk("Access Denied")
                self.pass_label.configure(text="Enter Password", fg = BLACK)
                self.pass_enter_text.focus()
                self.window.update()        
              
        
        self.settings_button.destroy()
        self.start_button.destroy()
        self.text_widget.destroy()
        self.run_blip.destroy()
        self.run_indic.destroy()
        self.stop_button.destroy()
        
        
        
        
        self.pass_label = Label(self.window, text="Enter Passsword", font= "Calibri 18 bold")
        self.pass_label.place(relheight=0.06, relwidth=0.2, relx=0.4, rely=0.3)
        
        # password input box
        self.pass_enter_text = Text(self.window,width = 20, bg = WHITE,
                                fg = BLACK, font = "Calibri 20 bold", padx = 5, pady = 5 )
        self.pass_enter_text.place(relheight=0.06, relwidth=0.2, relx=0.4, rely=0.4)
        
        # login button    
        self.pass_enter_button = Button(self.window, text="Login", bg=WHITE, fg = BLACK,
                                        font=FONT,command= lambda:pass_check())
        self.pass_enter_button.place(relheight=0.06, relwidth=0.1, relx=0.45, rely=0.5)
        self.pass_enter_text.focus()
        
        
        self.back_button = Button(self.window, text= "<<",font= "Calibri 20", command= lambda: back_to_main_window_from_pass(), borderwidth=0)
        self.back_button.place(relx=0.001, rely=0.007, relheight=0.055, relwidth=0.04)
      
    # setting page:
    def _settings_(self,event):
        
        def _get_tag_list():
            tags_list = []
            with open(json_file) as f:
                temp = json.load(f)
            for intent in temp["intents"]:
                tag = intent["tag"]
                tags_list.append(tag)
            return tags_list
        
        def reset_password():
            
            def pass_check():
                try:
                    password = self.enter_current_password_text.get(1.0, "end-1c")
                except TclError :
                    self.enter_current_password_button.configure(text="Incorrect ", fg=RED)
                    self.window.update()
                    talk("Incorrect Password")
                    self.enter_current_password_button.configure(text="Check", fg = BLACK)
                        
                    self.window.update()
                    
                if password == PASSWORD or password == MASTER_PASSWORD:
                    self.enter_current_password_button.configure(state="disabled")
                    self.enter_current_password_text.configure(state="disabled")
                    self.enter_new_password_button.configure(state="normal")
                    self.enter_new_password_text.configure(state="normal")
                    self.enter_new_password_text.focus()
                    self.window.update()
                else:
                    self.enter_current_password_button.configure(text="Incorrect ", fg=RED)
                    self.window.update()
                    talk("Incorrect Password")
                    self.enter_current_password_button.configure(text="Check", fg = BLACK)
                    self.window.update()
                                          
            def update_pass():
                password = self.enter_new_password_text.get(1.0, "end-1c")
                if len(password) != 0:
                    self.enter_new_password_text.configure(state="disabled")
                    self.pass_table.place(relheight=0.4, relwidth=0.45, relx=0.25, rely=0.5)
                    self.pass_table.see("end")
                    self.window.update()
                    with open(json_file, "r") as f:
                        data = json.load(f)
                    
                    data["essentials"]["password"] = password
                        
                    with open(json_file, "w") as f:
                         json.dump(data, f, indent = 4)
                        
                    for i in range(11):
                        self.pass_table.insert("end", ".\n")
                        time.sleep(0.3) 
                        self.window.update()
                          
                    self.pass_table.insert("end", f"Password Successfully Updated :\nNEW PASSWORD : {password}\nPlease Restart :)")
                    self.pass_table.configure(state="disabled")
                    
                else:
                    self.enter_new_password_button.configure(text= "Invalid", fg = RED)
                    self.window.update()
                    talk("Invalid")
                    self.enter_new_password_button.configure(text="Save", fg = BLACK)    
                    self.enter_new_password_text.delete(1.0, "end-1c")
                    self.window.update()
                
            #self.view_data_button.destroy()
            self.add_data_button.destroy()
            self.delete_data_button.destroy()
            self.train_button.destroy()
            self.password_change_button.destroy()
            self.data_table.destroy()
            self.back_button.configure(command=lambda:back_to_setting_page())
            
            self.enter_current_password_label.place(relheight=0.06, relwidth=0.2, relx=0.4, rely=0.1)
            self.enter_current_password_text.place(relheight=0.06, relwidth=0.25, relx=0.35, rely=0.2)      
            self.enter_current_password_button.place(relheight=0.06, relwidth=0.1, relx=0.55, rely=0.2)      
            self.enter_current_password_button.configure(command=lambda:pass_check())
            self.enter_current_password_text.focus()
                  
            self.enter_new_password_label.place(relheight=0.06, relwidth=0.2, relx=0.4, rely=0.3)      
            self.enter_new_password_text.place(relheight=0.06, relwidth=0.25, relx=0.35, rely=0.4)      
            self.enter_new_password_button.place(relheight=0.06, relwidth=0.1, relx=0.55, rely=0.4)      
            self.enter_new_password_button.configure(command=lambda:update_pass())
                            
        def reset(key):
            
            if key == "add_data":    
                self.check_tag_button.configure(bg = TEXT_COLOR, text="Check Tag", state="normal")
                self.add_tag_text.configure(state="normal")
                self.add_tag_text.delete(1.0, "end-1c")
                self.add_pattern_button.configure(state="disabled")
                self.add_patterns_text.delete(1.0,"end-1c")
                self.add_patterns_text.configure(state="disabled")
                self.add_response_button.configure(state="disabled")
                self.add_response_text.delete(1.0, "end-1c")
                self.add_response_text.configure(state="disabled")
                self.save_data_button.configure(state="disabled", fg=BLACK)
                self.table_.configure(state="normal")
                self.table_.delete(1.0, "end-1c")
                tmp["responses"] = []
                tmp["patterns"] = []
                self.table_.configure(state="disabled")
                self.window.update()
            elif key == "delete_data":
                self.enter_index_button.configure(state="normal")
                self.enter_index_text.configure(state="normal")
                self.enter_index_text.delete(1.0,"end-1c")
                self.data_table.configure(state="normal") 
                self.data_table.delete(1.0,"end-1c")
                self.data_table.configure(state="disabled")
                self.delete_data_conf_button.configure(state="disabled")
                                            
        def add_response():
            temp_response = self.add_response_text.get(1.0, "end-1c")
            if len(temp_response) != 0 and temp_response not in tmp["responses"]:
                
                tmp["responses"].append(temp_response)
                self.add_response_text.delete(1.0, "end-1c")
                self.table_.configure(state="normal")
                self.table_.insert("end", f"Response : \"{temp_response}\"\n")
                self.table_.configure(state="disabled")
                self.save_data_button.configure(state="normal", fg = GREEN)
                self.reset_button.configure(state="normal")

            else:
                self.add_response_button.configure(text="Invalid", fg = RED)
                self.window.update()
                talk("Invalid Response")
                self.add_response_button.configure(text="Add", fg = BLACK)
 
        def add_pattern():
            temp_pattern = self.add_patterns_text.get(1.0, "end-1c")
            if len(temp_pattern) != 0 and temp_pattern not in tmp["patterns"]:
                
                tmp["patterns"].append(temp_pattern)
                self.add_patterns_text.delete(1.0, "end-1c")
                self.table_.configure(state="normal")
                self.table_.insert("end", f"Pattern : \"{temp_pattern}\"\n")
                self.table_.configure(state="disabled")
                self.reset_button.configure(state="normal")

            else:
                self.add_pattern_button.configure(text="Invalid", fg = RED)
                self.window.update()
                talk("Invalid Pattern")
                self.add_pattern_button.configure(text="Add", fg = BLACK)
      
        def check_tag():
            
            
            tag = self.add_tag_text.get(1.0, "end-1c")
            tags_list = _get_tag_list()
            
            if tag not in tags_list and len(tag) != 0:
                self.add_tag_text.configure(state="disabled")
                self.check_tag_button.configure(state="disabled", text="Valid Tag", bg = GREEN)
                self.add_pattern_button.configure(state="normal")
                self.add_patterns_text.configure(state="normal")
                self.add_response_button.configure(state="normal")
                self.add_response_text.configure(state="normal")
                self.table_.configure(state="normal")
                self.table_.insert("end", f"Tag : \"{tag}\"\n")
                self.table_.configure(state="disabled")
                self.window.update()
                

            else:
                self.check_tag_button.configure(text="Invalid Tag",fg=RED)
                self.window.update()
                talk("invalid tag")
                self.check_tag_button.configure(text ="Check Tag", fg = BLACK)
        
        def training():
            #self.view_data_button.destroy()
            self.add_data_button.destroy()
            self.delete_data_button.destroy()
            self.train_button.destroy()
            self.password_change_button.destroy()
            self.back_button.configure(command= lambda: back_to_setting_page())
            
            self.data_table.place(relheight=0.8, relwidth=0.98, relx= 0.01, rely=0.09)
            self.data_table.configure(state="normal")
            self.data_table.delete(1.0, "end-1c")
            self.data_table.configure(fg = "#FFF", bg = BLACK, state="disabled")
            self.start_training_button.configure(command=lambda: start_training())
            self.start_training_button.place(relx=0.1, rely=0.9, relheight=0.06, relwidth=0.1)
            
            
            
            
            def start_training():
                
                self.data_table.configure(state="normal", font="Calibri 12")
                self.data_table.delete(1.0, "end-1c")
                self.data_table.insert("end", "Training Started:\n")
                self.data_table.update()
                talk("training started")
                self.start_training_button.configure(state="disabled")
                self.back_button.configure(state="disabled")
                
                self.window.update()
                f = open(json_file, 'r')

                with f as database:
                    intents = json.load(database)


                all_words = []
                tags = []
                xy = []

                for intent in intents['intents']:
                    tag = intent['tag']
                    tags.append(tag)
                    for pattern in intent['patterns']:
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
                num_epochs = 1000


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
                    if (epoch + 1) % 100 == 0:
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

                self.data_table.insert("end", f'Training Complete. File saved to {File}\nPlease Restart the app to see changes.')
                self.data_table.update()
                talk("Training Completed, Please Restart the app to see changes")
                self.data_table.configure(state="disabled")
                self.start_training_button.configure(state="normal")
                self.back_button.configure(state="normal")
                self.window.update()    
        
        def view_data():
            ##self.view_data_button.destroy()
            #self.add_data_button.destroy()
            #self.delete_data_button.destroy()
            #self.train_button.destroy()
            #self.view_data_button.configure(state="disabled")
            self.add_data_button.configure(state="disabled")
            self.delete_data_button.configure(state="disabled")
            self.password_change_button.configure(state="disabled")
            self.add_data_button.configure(state="disabled")
            self.train_button.configure(state="disabled")
            
            self.back_button.configure(command= lambda: back_to_setting_page())
            self.head_title.configure(text="Data")  
            self.data_table.place(relheight=0.9, relwidth=0.8, relx= 0.17, rely=0.09)
            
            self.data_table.config(state="normal")
          
            with open(json_file, "r") as f:
                file = json.load(f)
                j = 0
                for intent in file["intents"]:
                    tag = intent["tag"]
                    pattern = intent["patterns"]
                    responses = intent["responses"]
                    
                    self.data_table.insert("end", f"\n({j}) Tag : {tag}\n")
                    
                    self.data_table.insert("end", "\nPatterns : \n")
                    
                    i = 0
                    for p in pattern:
                        self.data_table.insert("end", f"{i} : {p}\n")
                        #print(f"{i} : {p}")
                        i+=1
                    
                    self.data_table.insert("end", "\nResponses : \n")
                    
                    i = 0
                    for r in responses:
                        self.data_table.insert("end", f"{i} : {r}\n")
                        #print(f"{i} : {r}")
                        i+=1    
                    self.data_table.insert("end", "\n\n")
                    j +=1
            
            # always see end
            self.data_table.see(END)
            self.data_table.config(state="disabled")
            self.window.update()       
               
        def view_tags():
            
            tags_list2 = _get_tag_list()
            
            
            self.tags_table.place(relheight=0.9, relwidth=0.25, relx=0.745, rely=0.09)
            self.tags_table.config(state="normal")
            self.tags_table.delete('1.0',END)
            self.window.update()
            i = 0
            for tag in tags_list2:
                self.tags_table.insert("end", f"{i} : {tag}\n")
                i+=1
            self.tags_table.config(state="disabled")
            self.window.update()
        
        def add_data():
            #self.view_data_button.destroy()
            self.add_data_button.destroy()
            self.delete_data_button.destroy()
            self.train_button.destroy()
            
            self.password_change_button.destroy()
            
            self.data_table.destroy()
            self.back_button.configure(command= lambda: back_to_setting_page())
            self.window.update()
            self.window.update_idletasks()
            
            self.add_tag_label.place(relwidth=0.2, relheight=0.06,relx=0.05, rely=0.1)
            self.add_tag_text.place(relwidth=0.2, relheight=0.06, relx=0.05, rely=0.2)
            self.add_tag_text.focus()
            self.view_tags_button.place(relheight=0.06, relwidth=0.1, relx=0.05, rely=0.3)
            self.check_tag_button.place(relwidth=0.1, relheight=0.06,relx=0.15 ,rely=0.3)
            
            self.add_pattern_label.place(relwidth=0.2, relheight=0.06, relx=0.05,rely=0.4)
            self.add_patterns_text.place(relwidth=0.2, relheight=0.06, relx=0.05, rely=0.5)
            self.add_pattern_button.place(relwidth=0.1, relheight=0.06, relx=0.25, rely=0.5)
            
            self.add_response_label.place(relwidth=0.2, relheight=0.06, relx=0.05,rely=0.6)
            self.add_response_text.place(relwidth=0.2, relheight=0.06, relx=0.05, rely=0.7)
            self.add_response_button.place(relwidth=0.1, relheight=0.06, relx=0.25, rely=0.7)
            
            self.save_data_button.place(relwidth=0.1, relheight=0.06, relx=0.15, rely=0.8)
            self.reset_button.place(relwidth=0.1, relheight=0.06, relx=0.05, rely=0.8)
            self.reset_button.configure(command=lambda:reset("add_data"))
            self.reset_button.configure(state="disabled")
            self.table_label.place(relwidth=0.2,relheight=0.06, relx=0.45 , rely=0.1)
            self.table_.place(relheight=0.7, relwidth=0.35, relx=0.38, rely=0.2)
            
            self.window.update()
        
        def save_data():
            
            if len(tmp["patterns"]) == 0:
                talk("Please add pattern")
                self.add_patterns_text.focus()
                return    
            
            
            save = {}
            with open(json_file,"r") as f:
                temp = json.load(f)
                
            
            save["tag"] = self.add_tag_text.get(1.0, "end-1c")
            save["responses"] = tmp["responses"]
            save["patterns"] = tmp["patterns"]
            
            
            
            temp["intents"].append(save)
            with open(json_file, "w") as f:
                json.dump(temp, f, indent = 4)

            tmp["patterns"]  = []
            tmp["responses"] = []        
        
            self.add_tag_text.configure(state="normal")
            self.add_tag_text.delete(1.0, "end-1c")
            self.add_tag_text.focus()
            
            self.add_patterns_text.delete(1.0, "end-1c")
            self.add_patterns_text.configure(state="disabled")
            self.add_pattern_button.configure(state= "disabled")
            
            self.add_response_text.delete(1.0, "end-1c")
            self.add_response_text.configure(state="disabled")
            self.add_response_button.configure(state= "disabled")
            
            self.check_tag_button.configure(state="normal", fg = BLACK, bg = TEXT_COLOR, text="Check Tag")
            self.save_data_button.configure(state="disabled")
            
            self.table_.configure(state="normal")
            self.table_.delete(1.0, "end-1c")
            self.table_.configure(state="disabled")
            
            view_tags()

            
            self.tags_table.update()
            self.window.update()
           
        def delete_tag_at_index():
            with open(json_file,"r") as f:
                temp = json.load(f)
            
            save = []

            self.enter_index_text.configure(state="normal")
            index = self.enter_index_text.get(1.0,"end-1c")
            self.enter_index_text.configure(state="disabled")
            
                        
           
            for i in range(len(temp["intents"])):
                if i == int(index):
                    temp["intents"].pop(i)
                
            
            with open(json_file,"w") as f:
                json.dump(temp, f, indent=4)

            
            self.delete_data_conf_button.configure(fg = GREEN)
            self.window.update()
            talk("Data deleted")
            
            self.enter_index_button.configure(state="normal")
            self.enter_index_text.configure(state="normal")
            self.enter_index_text.delete(1.0,"end-1c")
            self.data_table.configure(state="normal")
            self.data_table.delete(1.0,"end-1c")
            self.data_table.configure(state="disabled")
            self.delete_data_conf_button.configure(fg = RED,state="disabled")
            
            delete_data()
            
        def check_delete_index():

                self.data_table.configure(state="normal")
                
                
                index = self.enter_index_text.get(1.0,"end-1c") 
                
                tags_list2 = _get_tag_list()
                
                try:
                    
                    index = int(index)
                    if index in range(len(tags_list2)):
                        self.enter_index_button.configure(state="disabled")
                        self.enter_index_text.configure(state="disabled")
                        self.delete_data_conf_button.configure(state="normal")
                        
                        tag = tags_list2[index]
                        
                        with open(json_file, 'r') as f:
                            intents = json.load(f)
                        for intent  in intents["intents"]:
                            if tag == intent["tag"]:
                                self.data_table.insert("end", f"Tag : {tag}\n")
                    
                                self.data_table.insert("end", "\nPatterns : \n")
                    
                                i = 0
                                for p in intent["patterns"]:
                                    self.data_table.insert("end", f"{i} : {p}\n")
                                    #print(f"{i} : {p}")
                                    i+=1
                                
                                self.data_table.insert("end", "\nResponses : \n")
                                
                                i = 0
                                for r in intent["responses"]:
                                    self.data_table.insert("end", f"{i} : {r}\n")
                                    #print(f"{i} : {r}")
                                    i+=1    
                                self.data_table.insert("end", "\n\n")
                                    
                        self.data_table.configure(state="disabled")            
                        
                    else:  
                         
                        self.enter_index_button.configure(text="Invalid Index", fg = RED)
                        self.window.update()
                        talk("Invalid index")
                        self.enter_index_text.delete(1.0, "end-1c")
                        self.enter_index_button.configure(text="Confirm",fg = BLACK)
                        self.window.update()
                except:
                   
                    self.enter_index_button.configure(text="Invalid Index", fg = RED)
                    self.window.update()
                    talk("Invalid index")
                    self.enter_index_text.delete(1.0, "end-1c")
                    self.enter_index_button.configure(text="Confirm",fg = BLACK)
                    self.window.update()

                self.data_table.configure(state="disabled")
                                
        def delete_data():
            
            #self.view_data_button.destroy()
            self.add_data_button.destroy()
            self.delete_data_button.destroy()
            self.train_button.destroy()
            self.password_change_button.destroy()
            self.data_table.configure(state="normal")
            self.data_table.delete(1.0,"end-1c")
            self.data_table.configure(state="disabled")
            
            self.back_button.configure(command=lambda:back_to_setting_page())
            self.window.update()
            
            self.enter_index_label.place(relheight=0.06, relwidth=0.2, relx=0.09, rely=0.1)
            self.enter_index_text.place (relheight=0.06, relwidth=0.2, relx=0.09, rely=0.17)
            self.enter_index_text.focus()
            self.enter_index_button.place(relheight=0.06, relwidth=0.2, relx=0.09, rely=0.24)        
            
            
            self.table_label.place(relwidth=0.2,relheight=0.06, relx=0.45 , rely=0.085)
            self.table_label.configure(text="Data in Database")
            self.table_.place(relheight=0.84, relwidth=0.35, relx=0.38, rely=0.15)
            
            self.reset_button.place(relwidth=0.15, relheight=0.06, relx=0.05, rely=0.8)
            self.reset_button.configure(command=lambda:reset("delete_data"))
            
            self.delete_data_conf_button.place(relwidth=0.1,relheight=0.06, relx=0.2, rely=0.8)
            self.delete_data_conf_button.configure(command=lambda: delete_tag_at_index())
            self.window.update()
            
            
            
    
            
            view_tags()
        
            self.table_.config(state="normal")
          
            with open(json_file, "r") as f:
                file = json.load(f)
                j = 0
                for intent in file["intents"]:
                    tag = intent["tag"]
                    pattern = intent["patterns"]
                    responses = intent["responses"]
                    
                    self.table_.insert("end", f"\n({j}) Tag : {tag}\n")
                    
                    self.table_.insert("end", "\nPatterns : \n")
                    
                    i = 0
                    for p in pattern:
                        self.table_.insert("end", f"{i} : {p}\n")
                        #print(f"{i} : {p}")
                        i+=1
                    
                    self.table_.insert("end", "\nResponses : \n")
                    
                    i = 0
                    for r in responses:
                        self.table_.insert("end", f"{i} : {r}\n")
                        #print(f"{i} : {r}")
                        i+=1    
                    self.table_.insert("end", "\n\n")
                    j +=1
            
            # always see end
            self.table_.see(END)
            self.table_.config(state="disabled")
            self.window.update() 
        
            self.data_table.place(relheight=0.5, relwidth=0.35, relx=0.01, rely=0.3)
           
        tmp = {}
       
        tmp["responses"] = []
        tmp["patterns"] = []   
               
        def back_to_main_page():
            self.add_data_button.configure(state="normal")
            self.delete_data_button.configure(state="normal")
            #self.view_data_button.configure(state="normal")
            self.train_button.configure(state="normal")
            self.password_change_button.configure(state="normal")
            
            
        
            self.add_data_button.destroy()
            self.delete_data_button.destroy()
            #self.view_data_button.destroy()
            self.train_button.destroy()
            self.password_change_button.destroy()
            self.pass_enter_text.destroy()
            self.pass_enter_button.destroy()
            self.pass_label.destroy()
            self.back_button.destroy()
            self.data_table.destroy()
            self.tags_table.destroy()
            self.start_training_button.destroy()
            self.table_.destroy()
            
            self.window.update()
            
            self._main_window()
        
        def back_to_setting_page():
            self.add_tag_text.destroy()
            self.add_tag_label.destroy()
            self.add_pattern_label.destroy()
            self.add_pattern_button.destroy()
            self.add_patterns_text.destroy()
            self.add_response_label.destroy()
            self.add_response_button.destroy()
            self.add_response_text.destroy()
            self.check_tag_button.destroy()
            self.reset_button.destroy()
            self.save_data_button.destroy()
            self.view_tags_button.destroy()
            self.data_table.destroy()
            self.tags_table.destroy()
            self.table_.destroy()
            self.table_label.destroy()
            #self.view_data_button.destroy()
            self.delete_data_button.destroy()
            self.add_data_button.destroy
            self.train_button.destroy()
            self.start_training_button.destroy()
            self.enter_index_button.destroy()
            self.enter_index_label.destroy()
            self.enter_index_text.destroy()
            self.delete_data_conf_button.destroy()
            self.enter_current_password_label.destroy()
            self.enter_current_password_text.destroy()      
            self.enter_current_password_button.destroy()      
                  
            self.enter_new_password_label.destroy()      
            self.enter_new_password_text.destroy()      
            self.enter_new_password_button.destroy()  
            self.pass_table.destroy()
            
            
            
            self._settings_(NONE)

         # view data vars
        self.data_table = Text(self.window,width = 20, bg = BG_COLOR,
                                fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5 )
        self.tags_table = Text(self.window,width = 20, bg = BG_COLOR,
                                fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5 )
        
        self.table_label = Label(self.window, text="Live Preview", font= FONT)
        self.table_ = Text(self.window,width = 20, bg = BG_COLOR,
                                fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5, state="disabled")
        
        
        # add data vars
        self.add_tag_label = Label(self.window, text="Enter Tag", font= FONT_BOLD)
        self.add_tag_text = Text(self.window, bg = BG_COLOR, fg=TEXT_COLOR, 
                                font= FONT, padx=5,pady=5, insertbackground= WHITE)
        self.view_tags_button = Button(self.window, text = "View Tags", font=FONT, command= lambda : view_tags())
        self.check_tag_button = Button(self.window, text="Check Tag", font=FONT, command=lambda:check_tag())
        
        
        self.add_pattern_label = Label(self.window, text="Enter Pattern", font= FONT_BOLD)        
        self.add_patterns_text = Text(self.window, bg=BG_COLOR, fg = TEXT_COLOR, font="Calibri 20", 
                                      padx=5, pady=5, state="disabled", insertbackground= WHITE)
        self.add_pattern_button = Button(self.window, text = "Add", font= FONT, command=lambda:add_pattern(), state="disabled")
        
        self.add_response_label = Label(self.window, text="Enter Response", font= FONT_BOLD)        
        self.add_response_button = Button(self.window, text = "Add", font= FONT, command=lambda:add_response(), state="disabled")
        self.add_response_text = Text(self.window, bg=BG_COLOR, fg = TEXT_COLOR, font="Calibri 20", 
                                      padx=5, pady=5, state="disabled", insertbackground= WHITE)
        
        
        # reset button
        self.reset_button = Button(self.window, text= "Reset", font=FONT)
        # save button
        self.save_data_button = Button(self.window, text= "Save", font=FONT, command=lambda: save_data(), state="disabled")
    
        
        # delete data variables
        
        self.enter_index_label = Label(self.window, text="Select Index", font=FONT)
        self.enter_index_text = Text(self.window, bg=BG_COLOR, fg = TEXT_COLOR, font="Calibri 20", padx=5, pady=5 , insertbackground= WHITE)
        self.enter_index_button = Button(self.window, text="Confirm", font= FONT,command=lambda: check_delete_index())
        self.delete_data_conf_button = Button(self.window, text="Delete", font=FONT, fg=RED,state="disabled")
        
        # password reset variables
        self.enter_current_password_label = Label(self.window, text="Enter Current Password", font= FONT)
        self.enter_current_password_text = Text(self.window, bg = BG_COLOR, fg=TEXT_COLOR, font= "Calibri 20", padx=5, pady=5,
                                                insertbackground= WHITE)
        self.enter_current_password_button = Button(self.window, text="Check", font= FONT)
        
        self.enter_new_password_label = Label(self.window, text="Enter New Password", font= FONT)
        self.enter_new_password_text = Text(self.window, bg = BG_COLOR, fg=TEXT_COLOR, font= "Calibri 20", padx=5, pady=5,
                                            state="disabled", insertbackground= WHITE)
        self.enter_new_password_button = Button(self.window, text="Save" , state="disabled", font=FONT)
        self.pass_table = Text(self.window, bg = BG_COLOR, fg = TEXT_COLOR, padx=5, pady=5, font="Calibri, 12")
        
        # setup            
        self.start_button.destroy()
        self.run_blip.destroy()
        self.run_indic.destroy()
        self.text_widget.destroy()
        self.settings_button.destroy()
        self.head_title.configure(text="Settings")
        self.window.configure(bg = SETTING_BG)
        
        # button declration
        self.delete_data_button = Button(self.window, text = "Delete Data", font=FONT_BOLD , command= lambda : delete_data())
        self.add_data_button = Button(self.window, text = "Add Data", font=FONT_BOLD , command= lambda : add_data())
        ##self.view_data_button = Button(self.window, text = "View Data", font=FONT_BOLD , command= lambda : view_data())
        
        self.password_change_button = Button(self.window, text = "Reset Password", font=FONT_BOLD , command= lambda : reset_password())
        
        
        # train button vars
        self.train_button = Button(self.window, text="Train Bot", font=FONT_BOLD, command= lambda: training())
        self.start_training_button = Button(self.window, text="Start", font=FONT)
       
        # setup 
        
        
       # placing
        self.add_data_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.1)
        self.delete_data_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.2)            
        ##self.view_data_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.3)
        self.train_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.3)
        self.password_change_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.4)
         
        # back button
        self.back_button = Button(self.window, text= "<<",font= "Calibri 20", command= lambda: back_to_main_page(), borderwidth=0)
        self.back_button.place(relx=0.001, rely=0.007, relheight=0.055, relwidth=0.04)
        self.window.update()
             
    def running_state(self):
        run = True
        # stop automatically if user daid nothing two times
        err_count = 0
        
        while run and err_count < 2:
            
            self.run_indic.configure(text="  Listening..")
            self.run_blip.configure(bg = GREEN)
            self.window.update()
            
            msg , key, sender = recognizer()
            
            self.run_indic.configure(text="     Processing")
            self.run_blip.configure(bg = "#0000FF")
            self.window.update()
            
            
            if key == 'm':
                self.text_widget.config(fg= ERR_COLOR)
                self._insert_message("MICROPHONE ERROR :(", sender)
                self.text_widget.update()
                self.text_widget.config(fg=TEXT_COLOR)
                
                talk(msg)
                run = False
            elif key == 'e':
                self._insert_message("SERVER ERROR/NO INTERNET CONNECTION :(", sender)
                self.text_widget.update()
                talk(msg)
                run = False
            elif key == 'a':
                self._insert_message("Could not understand :(", sender)
                self.text_widget.update()
                err_count+=1
                talk(msg)
                continue
            else:
                self._insert_message(msg, sender)
                self.text_widget.update()
            
                err_count = 0 # error count reset
                if msg in quit_txt:
                    self._insert_message("See ya later :)",bot_name)
                    self.text_widget.update()
                    talk("see ya later")
                    self.text_widget.config(state="normal")
                    #self.text_widget.delete('1.0',END)
                    self.text_widget.update()
                    self.text_widget.config(state="disabled")
                    run = False
                else:
                    reply = normal_mode(msg)
                    self._insert_message(reply,bot_name)
                    self.text_widget.update()
                    talk(reply)    
         
         
        self.stop_button.configure(state="normal")

        self.settings_button.configure(state="normal")  
        self.run_indic.configure(text="Stopped")
        self.run_blip.configure(bg = RED)
        self.window.update()
        
        return
    
    def _on_enter_pressed(self,event):
        
        self.settings_button.configure(state= "disabled")
        self.stop_button.configure(state="disabled")
        self.start_button.configure(text= "Running", state = "disabled")
        
        self.run_indic.configure(text="Running")
        self.run_blip.configure(bg = GREEN)
        
        self._insert_message("Hello, My name is EIRA, How may I help you ?", bot_name)
        self.window.update()

        talk("Hello, My name is eera, How may I help you")
        self.running_state()
        
        self.start_button.config(text="Start", state = "normal")
        self.window.update()
        
        return
          
    # insert message
    def _insert_message(self, msg,sender):
        if not msg :
            return
        msg = f"{sender}: {msg}\n\n"
        
        # change text widget state to normal for a moment
        # this may have nothing to do as we are not using mouse so will refractor it
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", msg)
        self.text_widget.config(state="disabled")

        # always see end
        self.text_widget.see(END)
         
if __name__ == "__main__":
    app = Application()
    app.window.mainloop()

