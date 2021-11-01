import KNNModel
import tkinter as tk #GUI
import ctypes #Message Boxes

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (Login, App):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        if cont == Login:
            self.title("Login")
            self.minsize(250,75)
            self.maxsize(250,75)
        else:
            self.title("Smartphone Classifier")
            self.minsize(500,200)
            self.maxsize(500,200)

class Login(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self,parent)
        self.configure(background='alice blue')
        self.controller = controller
        
        self.username_label=tk.Label(self, text='Username', bg = 'alice blue')
        self.username_label.grid(row=0, column=0, sticky = 'W', padx = 25)
        self.username_entry=tk.Entry(self)
        self.username_entry.grid(row=0, column=1, sticky = 'W')

        self.password_label=tk.Label(self, text='Password', bg = 'alice blue')
        self.password_label.grid(row=1, column=0, sticky = 'W', padx = 25)
        self.password_entry=tk.Entry(self, show = "*")
        self.password_entry.grid(row=1, column=1, sticky = 'W')

        loginButton=tk.Button(self,text="Login", width = 15, bg = 'SpringGreen2')
        loginButton['command']= lambda: self.validate(self.username_entry.get(), self.password_entry.get())
        loginButton.grid(row=2,column=1, sticky = 'W')

    def validate(self, username, password):

        if username == 'admin' and password == 'admin':
            self.controller.show_frame(App)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Wrong credentials. Please try again.", "ERROR", 0)
            return

        

class App(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        self.widgets()
        self.configure(background='alice blue')

        self.model = KNNModel.Model()
        self.price_dict = {0:'$50 to $249',1:'$250 to $499',2:'$500 to $999',3:'above $1000'}

    def widgets(self):

        self.battery_label=tk.Label(self, text='Battery Power (mAh)', bg = 'alice blue')
        self.battery_label.grid(row=0, column=0, sticky = 'W', padx = 25)
        self.battery_entry=tk.Entry(self)
        self.battery_entry.grid(row=0, column=1, sticky = 'W')

        self.memory_label=tk.Label(self, text='Internal Memory (GB)', bg = 'alice blue')
        self.memory_label.grid(row=1, column=0, sticky = 'W', padx = 25)
        self.memory_entry=tk.Entry(self)
        self.memory_entry.grid(row=1, column=1, sticky = 'W')

        self.heigth_label=tk.Label(self, text='Height (px)', bg = 'alice blue')
        self.heigth_label.grid(row=2, column=0, sticky = 'W', padx = 25)
        self.heigth_entry=tk.Entry(self)
        self.heigth_entry.grid(row=2, column=1, sticky = 'W')

        self.width_label=tk.Label(self, text='Width (px)', bg = 'alice blue')
        self.width_label.grid(row=3, column=0, sticky = 'W', padx = 25)
        self.width_entry=tk.Entry(self)
        self.width_entry.grid(row=3, column=1, sticky = 'W')

        self.ram_label=tk.Label(self, text='RAM (MB)', bg = 'alice blue')
        self.ram_label.grid(row=4, column=0, sticky = 'W', padx = 25)
        self.ram_entry=tk.Entry(self)
        self.ram_entry.grid(row=4, column=1, sticky = 'W')

        classifyButton=tk.Button(self,text="Classify", width = 25, bg = 'SpringGreen2')
        classifyButton['command']= lambda: self.run_model(self.battery_entry.get(), self.memory_entry.get(), self.heigth_entry.get(), self.width_entry.get(),self.ram_entry.get())
        classifyButton.grid(row=5,column=0, sticky = 'W')

        self.result_label=tk.Label(self, text='',width = 25, bg = 'alice blue')
        self.result_label.config(font=("Courier", 10))
        self.result_label.grid(row=7, column=1, sticky = 'W')

        heatmapButton=tk.Button(self,text="Heatmap", width = 16, bg = 'Snow')
        heatmapButton['command']= lambda: self.model.show_heatmap()
        heatmapButton.grid(row=0,column=2, sticky = 'W')

        boxplotButton=tk.Button(self,text="Boxplot", width = 16, bg = 'Snow')
        boxplotButton['command']= lambda: self.model.show_boxplot()
        boxplotButton.grid(row=1,column=2, sticky = 'W')

        pointplotButton=tk.Button(self,text="Pointplot", width = 16, bg = 'Snow')
        pointplotButton['command']= lambda: self.model.show_pointplot()
        pointplotButton.grid(row=2,column=2, sticky = 'W')

        scatterplotButton=tk.Button(self,text="Scatterplot", width = 16, bg = 'Snow')
        scatterplotButton['command']= lambda: self.model.show_scatterplot()
        scatterplotButton.grid(row=3,column=2, sticky = 'W')


    def run_model(self,battery_power,int_memory,px_height,px_width,ram):
        
        if not battery_power.isdigit() or battery_power is None:
            ctypes.windll.user32.MessageBoxW(0, "Enter a number for battery power.", "ERROR", 0)
            return

        if not int_memory.isdigit() or int_memory is None:
            ctypes.windll.user32.MessageBoxW(0, "Enter a number for internal memory.", "ERROR", 0)
            return
        
        if not px_height.isdigit() or px_height is None:
            ctypes.windll.user32.MessageBoxW(0, "Enter a number for pixel height.", "ERROR", 0)
            return
        
        if not px_width.isdigit() or px_width is None:
            ctypes.windll.user32.MessageBoxW(0, "Enter a number for pixel width.", "ERROR", 0)
            return
        
        if not ram.isdigit() or ram is None:
            ctypes.windll.user32.MessageBoxW(0, "Enter a number for RAM.", "ERROR", 0)
            return
        
        range_price = self.model.predict(battery_power,int_memory,px_height,px_width,ram)
        result_text = "The smartphone value is:\n" + self.price_dict[range_price]
        self.result_label.config(text = result_text)
        print(self.price_dict[range_price])


        
if __name__ == '__main__':

    app = Main()
    app.mainloop()
