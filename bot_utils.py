'''
Contains Functions Used during Training and execution

'''
import pyttsx3
import nltk
from nltk.stem.porter import PorterStemmer
import speech_recognition as sr
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import random
import json
from model import NeuralCode
import pyglet


'''System Variables'''

bot_name = "EIRA"
json_file = "D:\GLOBOT\database.json"
idk = "I do not understand"



'''Functions'''
# tokenize sentence
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Stem word to root
def stem(word):
    stemmer = PorterStemmer()
    return stemmer.stem(word.lower())

# Bag of words (vocabulary builder for bot)
def bag_of_words(tokenized_sentence, all_words):
    """
    sentence = "Hello there"
    words = ['hello', 'bye', 'there']
    bag   = [   1   ,   0  ,    1   ]
    """
    tokenized_sentence = [stem(word) for word in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, word in enumerate(all_words):
        if word in tokenized_sentence:
            bag[idx] = 1.0

    return bag
    '''
    sentence = ["hey", "how", "are", "you"]
    words =  ["hey", "hello", "how", "we", "are", "they", "you"]   
    bag = bag_of_words(sentence,words)    
    print(bag)
    '''

# Speech to text
def recognizer():
   
    key = 'n'
    sender = "You"
    
    
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
    except OSError:
        txt = "TECHNICAL ERR. (MICERR) :{"
        key = 'm'
        sender = "EIRA"
        return txt, key, sender      
    
    
    try:
        txt = r.recognize_google(audio)
        
    except sr.UnknownValueError:
        key = 'a'
        sender = "EIRA"
        txt = "Sorry I didn't understand. Can you please repeat?"
        return txt, key, sender
    
    except sr.RequestError :
        txt = "SERVERS ARE DOWN :/ "
        key = 'e'
        sender = "EIRA"
        return txt, key, sender
    
    return txt, key, sender

# Play mp3 files
def play(mp3_file):
    
    music = pyglet.resource.media(mp3_file)
    music.play()
    pyglet.app.run()
    pyglet.app.exit()
    return
 
# Text to speech (offline)
def talk(text):
    # initialisation
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 
    engine.setProperty('rate', 150)
    # running
    engine.say(text)
    engine.runAndWait()

# main answer
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