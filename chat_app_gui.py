from tkinter import *
from chat_app import chatbot_response


# Create functionality for send button in the GUI
def send(event=None):
    message = entry_box.get('1.0', 'end-1c').strip()
    entry_box.delete('0.0', END)

    if message != '':
        chat_log.config(state = NORMAL)
        chat_log.insert(END, 'You: ' + message + '\n\n')
        chat_log.config(foreground = '#282828', font = ('Helvetica', 16))

        response = chatbot_response(message)
        chat_log.insert(END, 'Bot: ' + response + '\n\n')

        chat_log.config(state = DISABLED)
        chat_log.yview(END)


base = Tk()
base.title("Hi, I'm Travel Buddy!")
base.geometry('400x500')
base.resizable(width = FALSE, height = FALSE)

# Chat window
chat_log = Text(base, bd = 0, bg = '#F7F7F7', height = '8', width = '50', font = 'Helvetica', wrap='word')

chat_log.config(state = DISABLED)

# Add scrollbar to chat window
scrollbar = Scrollbar(base, command = chat_log.yview, cursor = 'pencil')
chat_log['yscrollcommand'] = scrollbar.set

# Add send button
send_button = Button(base, font = ('Helvetica', 16, 'bold'), text = 'Send', width = '12', height = '5', bd = 0,
                     bg = 'blue', activebackground = 'green', fg = '#F7F7F7', command = send)

# Add message entry box
entry_box = Text(base, bd = 0, bg = "#F7F7F7", width = '29', height = '5', font = 'Helvetica', wrap='word')
entry_box.bind("<Return>", send)

# Combine all components
scrollbar.place(x = 376, y = 6, height = 386)
chat_log.place(x = 6, y = 6, height = 386, width = 370)
entry_box.place(x = 6, y = 401, height = 90, width = 265)
send_button.place(x = 270, y = 401, height = 90)

base.mainloop()