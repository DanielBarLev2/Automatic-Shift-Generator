import tkinter as tk
from tkinter import ttk

root = tk.Tk()

options = ["Option 1", "Option 2", "Option 3", "Option 4"]
default_option = "Option 1"

combobox = ttk.Combobox(root, values=options, state="readonly")
combobox.current(options.index(default_option))
combobox.pack()

root.mainloop()


# import tkinter as tk
#
# # Create a new instance of Tkinter
# window = tk.Tk()
#
# # Set the window size
# window.geometry("500x400")
#
# # Set the window title
# window.title("NETTA")
#
# # Set the window icon
# window.iconbitmap("Netta_Icon.ico")
#
#
# # Get the screen width and height
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()
#
# # Calculate the x and y coordinates of the window's top-left corner
# x = (screen_width - 500) // 2
# y = (screen_height - 400) // 2
#
# # Set the window's position
# window.geometry("+{}+{}".format(x, y))
#
# headline = tk.Label(window, text="Yael's Auto-Shifts-Generator", font=("Times 20 italic bold", 24))
# headline.pack(pady=20)
#
#
# # Create the two labels for the text boxes
# label1 = tk.Label(window, text="Enter text 1:")
# label2 = tk.Label(window, text="Enter text 2:")
#
# # Create the two input boxes
# input_box1 = tk.Entry(window, width=80)
# input_box2 = tk.Entry(window, width=80)
#
# # Create a list of options
# options = ['Option 1', 'Option 2', 'Option 3']
#
# # Create a StringVar to store the selected option
# selected_option = tk.StringVar()
#
# # Set the default value of the StringVar
# selected_option.set(options[0])
#
# # Create the OptionMenu widget
# option_menu = tk.OptionMenu(window, selected_option, *options)
#
# # Create the confirm button
# confirm_button = tk.Button(window, text="Confirm", command=lambda: root.destroy())
#
# # Pack the input boxes into the window
# label1.pack(side="top")
# label2.pack()
# input_box1.pack()
# input_box2.pack()
# option_menu.pack()
# confirm_button.pack()
#
# # Start the main loop of the window
#
# window.mainloop()
