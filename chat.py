from tkinter import *
import customtkinter
import openai
import os
import pickle
#Instantiate app
root = customtkinter.CTk()
root.title('ChatGPT Bot')
root.geometry('600x365')
root.iconbitmap('ai_lt.ico') #https://tkinter.com/ai_lt.ico
#Set color Scheme
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

#Submit to ChatGPT
def speak():
    if chat_entry.get():
        filename = 'api_key'
        try:
            if os.path.isfile(filename):
                #Open the file
                input_file = open_file(filename,'rb')

                #Load data from tnhe file into a variable
                data = pickle.load(input_file)

                #Query ChatGPT
                #Define API key to ChatGPT
                openai.api_key = data
                #Create an instance
                openai.Model.list()
                #Define query/response
                response = openai.Completion.create(
                    model='text-davinci-003',
                    prompt=chat_entry.get(),
                    temperature=0,
                    max_tokens=60,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                my_text.insert(END,(response['choices'][0]['text']).strip())
                my_text.insert(END,'\n\n')
            else:
                #Create file
                input_file = open_file(filename,'wb')
                #Close the file
                input_file.close()
                #Error message for missing API key
                my_text.insert(END,'\n\nAPI key is needed to interact with ChatGPT. Please visit to get one: https://beta.openai.com/account/api-keys')

        except Exception as e:
            my_text.insert(END, f'\n\n An error has occurred\n\n{e}')
    else:
        my_text.insert(END,'\n\nNo message received! Please type something.')

#Clear the screens
def clear():
    #Clear the main textbox
    my_text.delete(1.0,END)
    #Clear the query entry widget
    chat_entry.delete(0,END)

def open_file(filename, action):
       return open(filename,action)

#Process API key
def key():
    #Define filename
    filename = 'api_key'

    try:
        if os.path.isfile(filename):
            #Open the file
            input_file = open_file(filename,'rb')

            #Load data from tnhe file into a variable
            data = pickle.load(input_file)

            #Output data to entry box
            api_entry.insert(END, data)
        else:
            #Create file
            input_file = open_file(filename,'wb')
            #Close the file
            input_file.close()
    except Exception as e:
        my_text.insert(END, f'\n\n An error has occurred\n\n{e}')

    root.geometry('600x500')
    api_frame.pack(pady=30)

#Save the API key
def save_key():
    #Define filename
    filename = 'api_key'
    try:
        #Open file
        output_file = open_file(filename,'wb')

        #Add data to the file
        pickle.dump(api_entry.get(), output_file)

        #Delete entry box
        api_entry.delete(0,END)

        api_frame.pack_forget()
        root.geometry('600x365')
    except Exception as e:
        my_text.insert(END, f'\n\n An error has occurred\n\n{e}')

#Create text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

#Add Text widget for chatgpt responses
my_text = Text(text_frame, 
bg='#343638', 
width=85, 
bd=1,
fg='#d6d6d6',
relief='flat',
wrap=WORD,
selectbackground='#1f538d')
my_text.grid(row=0, column=0)

#Create scrollbar for widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
command=my_text.yview)
text_scroll.grid(row=0,column=1,sticky='ns')

#Add the scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

# Entry widget to type to ChatGPT
chat_entry = customtkinter.CTkEntry(root,
placeholder_text='What\'s on your mind?',
width=535,
height=50,
border_width=1)
chat_entry.pack(pady=10)

#Create button frame
button_frame = customtkinter.CTkFrame(root,
fg_color='#242424')
button_frame.pack(pady=10)

#Create submit button
submit_button = customtkinter.CTkButton(button_frame,
text='Speak To ChatGPT',
command=speak)
submit_button.grid(row=0,column=0,padx=25)

#Create clear button
clear_button = customtkinter.CTkButton(button_frame,
text='Clear Response',
command=clear)
clear_button.grid(row=0,column=1,padx=35)

#Create api button
api_button = customtkinter.CTkButton(button_frame,
text='Update API Key',
command=key)
api_button.grid(row=0,column=2,padx=25)

#Add API key frame
api_frame = customtkinter.CTkFrame(root,
border_width=1)
api_frame.pack(pady=10)

#Add API entry widget
api_entry = customtkinter.CTkEntry(api_frame,
placeholder_text='Enter your API key',
width=350,
height=50,
border_width=1)
api_entry.grid(row=0,
column=0,
padx=20,
pady=20)

#Add API button
api_save_button = customtkinter.CTkButton(api_frame,
text='Save key',
command=save_key)
api_save_button.grid(row=0,
column=1,
padx=10)


root.mainloop()