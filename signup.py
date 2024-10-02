from tkinter import *
from tkinter import font,ttk
from tkcalendar import Calendar
import random

def create_user():
    rand_num=random.randint(100000,999999)
    user_id.config(text=f"Your user id is: {rand_num}")


root=Tk()
root.geometry("600x600")

title=Label(root,text='Signup Page')
title.pack()
#Personal info
name=Label(root,text='Name:')
name.place(x=5,y=60)
name_entry=Entry(root)
name_entry.place(x=120,y=60)
mob=Label(root,text='Mobile number:')
mob.place(x=5,y=90)
mob_entry=Entry(root)
mob_entry.place(x=120,y=90)
email=Label(root,text='Email:')
email.place(x=5,y=120)
email_entry=Entry(root)
email_entry.place(x=120,y=120)
dob=Label(root,text='Date of birth:')
dob.place(x=5,y=150)
dob_entry=Entry(root)
dob_entry.place(x=120,y=150)
pwd=Label(root,text='Password:')
pwd.place(x=5,y=180)
pwd_entry=Entry(root)
pwd_entry.place(x=120,y=180)
conf_pwd=Label(root,text='Confirm Password:')
conf_pwd.place(x=5,y=210)
conf_pwd_entry=Entry(root)
conf_pwd_entry.place(x=120,y=210)

#Account details
acc_no=Label(root,text='Account number:')
acc_no.place(x=330,y=60)
acc_no_entry=Entry(root)
acc_no_entry.place(x=450,y=60)
ifsc=Label(root,text='IFSC Code:')
ifsc.place(x=330,y=90)
ifsc_entry=Entry(root)
ifsc_entry.place(x=450,y=90)
status=Label(root,text='Account status:')
status.place(x=330,y=120)
statuss=['Active','Inactive']
status_entry=ttk.Combobox(root,values=statuss,width=17,font=('Arial',8))
status_entry.place(x=450,y=120)
type=Label(root,text='Account type:')
type.place(x=330,y=150)
types=["Savings","Current"]
type_entry=ttk.Combobox(root,values=types,width=17,font=('Arial',8))
type_entry.place(x=450,y=150)
created_on=Label(root,text='Account created on:')
created_on.place(x=330,y=180)
created_on_entry=Entry(root)
created_on_entry.place(x=450,y=180)
format=Label(root,text='(in dd-mmm-yyyy)')
format.place(x=330,y=200)

submit=Button(root,text='Signup',command=create_user)
submit.place(x=270,y=300)
user_id=Label(root,text='')
user_id.place(x=240,y=330)
return_back=Button(root,text='Return to login page',borderwidth=0,font=('Arial',10,'underline'))
return_back.place(x=230,y=350)
root.mainloop()