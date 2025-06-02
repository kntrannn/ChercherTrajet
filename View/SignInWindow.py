import tkinter as tk
import customtkinter as ctk
from Controller.LoginController import login_success
from View.MapWindow import MapWindow
from View.SignUpWindow import SignUpWindow

class LoginWindow(tk.Tk):
    """
    A window for logging in.

    Attributes:
        canva: Canvas widget for the background image.
        title1: Customized label for the title.
        label1: Customized label for "Username".
        username: Entry widget for entering the username.
        label2: Customized label for "Password".
        password: Entry widget for entering the password.
        button1: Customized button for logging in.
        button2: Customized button for creating a new account.
        label3: Customized label for displaying error messages.
    """
    def __init__(self):
        ctk.set_appearance_mode("light")

        super().__init__()
        self.title("Your personal travel map")
        self.geometry("500x500")
        self.resizable(False, False)

        # Apply custom color theme
        self.canva = ctk.CTkCanvas(width=500, height=500)
        self.canva.pack()

        # Load the image file.
        img1 = tk.PhotoImage(file="View/pictures/bg_map.png")
        self.canva.create_image(0, 0, image=img1, anchor="nw")


        self.title1 = ctk.CTkLabel(self,text = "Your personal travel map", font = ("Impact", 25), text_color='#354f52', fg_color= "#f5f6f9")
        self.title1.place(x = 130, y = 50)

        self.label1 = ctk.CTkLabel(self,text = "Username", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.label1.place(x = 175, y = 100)
        
        self.username = ctk.CTkEntry(self, font = ("Arial", 11, 'bold'), width= 150, height = 20, text_color = '#354f52')
        self.username.place(x = 175, y = 125)
        
        self.label2 = ctk.CTkLabel(self,text = "Password", font = ("Arial", 11, 'bold'), text_color = '#354f52', fg_color= "#f5f6f9")
        self.label2.place(x = 175, y = 200) 
        
        self.password = ctk.CTkEntry(self, font = ("Arial", 11, 'bold'), width= 150, height = 20, text_color = '#354f52', show = "*")
        self.password.place(x = 175, y = 225)

        self.button1 = ctk.CTkButton(self, text = "Connect", font = ("Arial", 11, 'bold'), width = 200, height = 30, fg_color= '#354f52', corner_radius = 10)
        self.button1.place(x = 150, y = 300)
        self.button1.bind('<Button-1>', self.login)
        self.bind('<Return>', self.login)
        
        self.button2 = ctk.CTkButton(self, text = "Create a new Account", font = ("Arial", 11, 'bold'), width = 200, height = 30, fg_color= '#354f52', text_color='#f9f7f3', corner_radius = 10)
        self.button2.place(x = 150, y = 350)
        self.button2.bind('<Button-1>', self.SignUp)

        self.mainloop()

    def login(self, event):
        """Sign in the user."""
        username_val = self.username.get().strip()
        password_val = self.password.get().strip()

        is_valid, user, error_message = login_success(username_val, password_val)

        if is_valid:
            self.user = user

            # Unbind events before destruction
            self.button1.unbind('<Button-1>')
            self.button2.unbind('<Button-1>')
            self.unbind('<Return>')

            # Delay destruction to ensure event handler completes
            self.after(100, self.open_map_window)
        else:
            # If error message already exists, destroy it
            if hasattr(self, "label3"):
                self.label3.destroy()

            # Label for error message
            self.label3 = ctk.CTkLabel(self, text = error_message, font = ("Courier", 15), width = 400, height = 30, bg_color= "red")
            self.label3.place(x = 50, y = 400)

            # Clear the entry
            self.username.delete(0, 'end')
            self.password.delete(0, 'end')

            # Focus on username entry
            self.username.focus()

    def SignUp(self, event):
        """Sign up the user."""
        # Unbind events before destruction
        self.button1.unbind('<Button-1>')
        self.button2.unbind('<Button-1>')
        self.unbind('<Return>')

        # Delay destruction to ensure event handler completes
        self.after(100, self.open_sign_up_window)

    def open_map_window(self):
        """Open the map window."""
        self.destroy()
        MapWindow(self.user)

    def open_sign_up_window(self):
        """Open the sign up window."""
        self.destroy()
        SignUpWindow()
    
    def quit(self):
        """Close the window."""
        self.destroy()
        
