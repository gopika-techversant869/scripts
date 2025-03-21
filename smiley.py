import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Smiley Face")

# Create a Canvas
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()

# Draw face (circle)
canvas.create_oval(50, 50, 250, 250, fill="yellow", outline="black", width=2)

# Draw eyes (small circles)
canvas.create_oval(100, 100, 130, 130, fill="black")  # Left eye
canvas.create_oval(170, 100, 200, 130, fill="black")  # Right eye

# Draw smile (arc)
canvas.create_arc(100, 120, 200, 220, start=0, extent=-180, style=tk.ARC, width=3)

# Run the main loop
root.mainloop()
