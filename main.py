from tkinter  import *;
from tkinter import messagebox;
from generate_password import generate;
import pyperclip;
import json;
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #

email_saved = None;
website_saved = None;
password_saved = None;

def save_vars():
    global email_saved, website_saved, password_saved;
    email_saved = email_input.get();
    website_saved = website_input.get();
    password_saved = password_input.get();

def generate_random_password():
    new_pass = generate();
    password_input.insert(0,new_pass)
    pyperclip.copy(new_pass)

def save_to_file():
    global email_saved, website_saved, password_saved;
    new_data = {
        website_saved.lower(): {
            "email":email_saved,
            "password":password_saved
        }
    }
    try:
         saved_data = None;
         with open("saved_data/data.json", "r") as file:
            saved_data = json.load(file);
            saved_data.update(new_data);
         with open("saved_data/data.json", "w") as file:
            json.dump(saved_data,file,indent=4);
    except:
        with open("saved_data/data.json", "w") as file:
            json.dump(new_data,file,indent=4);
    finally:
        messagebox.showinfo(title="Updated",message="Updated Info!")

# ---------------------------- UI SETUP ------------------------------- #

def search_info():
    website = website_input.get();
    try:
        with open("./saved_data/data.json") as file:
            loaded_data = json.load(file);
            if website in loaded_data:
                email = loaded_data[website]["email"];
                password = loaded_data[website]["password"];
                messagebox.showinfo(title=website,message = f"Email: {email} \n Password: {password}");
                pyperclip.copy(password);
            else:
                messagebox.showinfo(title=website,message="No Info Found!");
    except FileExistsError:
        messagebox.showinfo(message="You have no saved info yet!",title=website);

def submit_info():
    save_vars();
    
    if len(website_saved) > 0 and len(email_saved) > 0 and len(password_saved) > 0: 
        is_ok = messagebox.askyesnocancel(title=f"{email_saved}",message= f"Save following? \n Email:{email_saved} \n Password {password_saved} \n" );
        if is_ok:
            save_to_file();
    else:
        messagebox.showinfo(title="Validation Error", message="You are missing some key info");


window = Tk();
window.config(padx=50,pady=50,bg="white");
canvas = Canvas(width=200,height=200,bg="white",highlightthickness=0);
logo = PhotoImage(file = "./imgs/logo.png");
logo_element = canvas.create_image(100,100,image = logo);

website_label = Label(text = "Website:",bg="white")
email_label = Label(text = "Email/Username:",bg="white")
password_label = Label(text = "Passsword:",bg="white")
website_input = Entry(width=50);
email_input = Entry(width=50);
generate_button = Button(text="Generate Password",bg="white",borderwidth=1,command = generate_random_password);
submit_button = Button(text="Submit",highlightthickness=1,bg="white",width=35,borderwidth=1,command = submit_info);
password_input = Entry(width=35);
website_label.grid(row=1,column=0);
email_label.grid(row=2,column=0);
search_button = Button(text = "Search",command=search_info);
search_button.grid(row=1,column=3);
password_label.grid(row=3,column=0,columnspan=1);
website_input.grid(row=1,column=2,columnspan=1,pady=5);
email_input.grid(row=2,column=2,columnspan=2,pady=5);
password_input.grid(row=3,column=2,pady=5);
canvas.grid(row=0,column=2);

submit_button.grid(row=4,column=2,columnspan=2,pady=15);
generate_button.grid(row=3,column=3,columnspan=3);
window.mainloop();
