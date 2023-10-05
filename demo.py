from tkinter import ttk, Tk


def button_clicked():
    print(my_name.get())


root = Tk()

my_label = ttk.Label(root, text = "This is a text label")
my_label.pack()

my_name = ttk.Entry(root)
my_name.pack()

ttk.Button(root, text="Click Me", command=button_clicked).pack()




root.mainloop()
