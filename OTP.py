import random
from email.message import EmailMessage
import smtplib, ssl
from tkinter import*
import re

OTP = random.randint(100000,999999)


def is_email_valid(input):
    return bool (re.match( r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',input))



def send_email():
    OTP_frame = Frame()
    OTP_frame.pack(pady=20)
    email_text = Text(OTP_frame, width=40, height=1, font=("Arial", 16))
    email_text.pack(side=TOP, padx=5, pady=5)
    email_text.insert(END, "Enter your E-mail")
   
    
    def clear_email_text(event):
        email_text.delete('1.0', END)

    email_text.bind("<FocusIn>", clear_email_text)
    my_label = Label(OTP_frame, text='', font=("Arial", 16))
    my_label.pack(padx=20)
    send_email_button = Button(OTP_frame, text="Send Verification Number", font=("Arial", 16), command=lambda: send(email_text,my_label,OTP_frame))
    send_email_button.pack()
    


def send(email_text,my_label,OTP_frame):
    msg = EmailMessage()
    msg.set_content("verification Code: {}".format(OTP))
    msg["Subject"] = "verification Number"
    msg["From"] = "E-mail@gmail.com"
    msg["To"] =email_text.get(1.0,END).strip()
    global reciver_email
    reciver_email=msg["To"]
    my_label.config(text="")
    if not (msg["To"]):
        my_label.config(text="Please enter the email first", font=("Arial", 12))
        return
    elif is_email_valid(msg["To"])==False:
        my_label.config(text="ENTER VALID E-MAIL")
        return
    context=ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(msg["From"], "Password")
        smtp.send_message(msg)
    email_text.destroy()
    my_label.destroy()
    OTP_frame.destroy()
    check_OTP_Number()

def resend():
    OTP = random.randint(100000,999999)
    global reciver_email
    msg = EmailMessage()
    msg.set_content("verification Number: {}".format(OTP))
    msg["Subject"] = "verification Number"
    msg["From"] = "E-mail@gmail.com"
    msg["To"] =reciver_email
    context=ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(msg["From"], "password")
        smtp.send_message(msg)

def check_OTP_Number():
    otpframe2 = Frame()
    otpframe2.pack(pady=20)
    OTP_text = Text(otpframe2, width=40, height=1, font=("Arial", 16))
    OTP_text.pack(side=TOP, padx=5, pady=5)
    OTP_text.insert(END, "Enter Verification number")
    my_label = Label(otpframe2, text='', font=("Arial", 16))
    my_label.pack(padx=20)

    def clear_OTP_text(event):
        OTP_text.delete('1.0', END)

    OTP_text.bind("<FocusIn>", clear_OTP_text)


    def Verification():
        userInput = OTP_text.get(1.0, END).strip()[:6]
        if not userInput:
            my_label.config(text="Please enter the verification Code first", font=("Arial", 12))
        elif userInput == str(OTP):
            my_label.config(text="verified successfully")
        else:
            my_label.config(text="Incorrect Code")
            
    button_frame1 = Frame(otpframe2)
    button_frame1.pack(side=TOP, pady=10)
    button_frame3 = Frame(otpframe2)
    button_frame3.pack(side=TOP, pady=10)


    Verification_button = Button(button_frame1, text="Verify", font=("Arial", 16), command=Verification)
    Verification_button.pack(side=LEFT, padx=5)

    resend_button = Button(button_frame1, text="Resend verification Number", font=("Arial", 16), command=resend)
    resend_button.pack(side=LEFT, padx=15)
    
    Back_button = Button(button_frame3, text="Back", font=("Arial", 16), command=lambda: (otpframe2.destroy(), send_email()))
    Back_button.pack(side=TOP, padx=5)
    



root = Tk()
root.title("OTP Verification")
root.geometry("400x300")
send_email()

root.mainloop()
