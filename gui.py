import PIL.Image as Image
import tkinter as Tk
import PIL.ImageTk as ImageTk
import cconway
import numpy as np
import tkinter.messagebox

#Only define integer values
WIDTH, HEIGHT = 100, 100
ZOOM = 6


class Gui(Tk.Frame):

    def __init__(self, root):
        self.root = root
        super().__init__(master=root)
        self.grid = cconway.CGrid(WIDTH, HEIGHT)
        canvas_frame = Tk.Frame(master=root)
        canvas_frame.grid(row=0, column=0)
        self.canvas = Tk.Canvas(canvas_frame, width=WIDTH * ZOOM, height = HEIGHT * ZOOM)
        self.canvas.pack()

        ui_frame = Tk.Frame(master=root)
        ui_frame.grid(row=0, column=1)

        Tk.Label(master=ui_frame, text="Spectrum").grid(row=0, sticky=Tk.NW)
        self.entry_spectrum = Tk.Entry(master=ui_frame)
        self.entry_spectrum.grid(row=1, sticky=Tk.NW)
        self.entry_spectrum.insert(0, str(cconway.A))
        self.entry_spectrum.bind("<Return>", lambda e: self.set_spectrum())

        Tk.Label(master=ui_frame, text="Flattness(Exponent)").grid(row=2, sticky=Tk.NW)
        self.entry_flattness = Tk.Entry(master=ui_frame)
        self.entry_flattness.grid(row=3, sticky=Tk.NW)
        self.entry_flattness.insert(0, str(cconway.P))
        self.entry_flattness.bind("<Return>", lambda e: self.set_flattness())

        Tk.Label(master=ui_frame, text="Birth function roots").grid(row=4, sticky=Tk.NW)
        self.entry_birth_function_roots = Tk.Entry(master=ui_frame)
        self.entry_birth_function_roots.grid(row=5, sticky=Tk.NW)
        self.entry_birth_function_roots.insert(0, ",".join(map(str, cconway._B)))
        self.entry_birth_function_roots.bind("<Return>", lambda e: self.set_birth_function_roots())

        Tk.Label(master=ui_frame, text="Durability function roots").grid(row=6, sticky=Tk.NW)
        self.entry_durability_function_roots = Tk.Entry(master=ui_frame)
        self.entry_durability_function_roots.grid(row=5, sticky=Tk.NW)
        self.entry_durability_function_roots.insert(0, ",".join(map(str, cconway._D)))
        self.entry_durability_function_roots.bind("<Return>", lambda e: self.set_durability_function_roots())

        Tk.Button(master=ui_frame, command=self.iter, text="Iterate").grid(row=8, sticky=Tk.NW)
        Tk.Button(master=ui_frame, command=self.random, text="Random").grid(row=9, sticky=Tk.NW)
        Tk.Button(master=ui_frame, command=self.reset, text="Reset").grid(row=10, sticky=Tk.NW)
        self.show()
        self.canvas.bind("<ButtonPress-1>", lambda e: self.set(int(e.x / ZOOM), int(e.y / ZOOM), 1.0))
        self.canvas.bind("<ButtonPress-3>", lambda e: self.set(int(e.x / ZOOM), int(e.y / ZOOM), 0.0))


    def parse_roots(self, s):
        """ Parse an input string as a root list """
        roots = [float(t.strip()) for t in s.split(",")]
        return roots

    
    def set_birth_function_roots(self):
        """ Sets the roots of the birth function """
        try:
            roots = self.parse_roots(self.entry_birth_function_roots.get())
            b = cconway.polynomial_functor(roots)
            self.grid.b = b
            return True
        except Exception as e:
            tkinter.messagebox.showerror("Unable to define birth function (format = 'x1,x2....,xn)", "During definition of the birth function an exception occured: " + str(e))
            return False

    def set_durability_function_roots(self):
        """ Sets the roots of the durability function """
        try:
            roots = self.parse_roots(self.entry_durability_function_roots.get())
            d = cconway.polynomial_functor(roots)
            self.grid.d = d
            return True
        except Exception as e:
            tkinter.messagebox.showerror("Unable to define durability function (format = 'x1,x2....,xn)'", "During definition of the durability function an exception occured: " + str(e))
            return False


    def random(self):
        """ Randomizes the entire grid """
        self.grid.random()
        self.show()

    def reset(self):
        """ Resets the entire grid"""
        self.grid.reset()
        self.show()

    def set(self, x, y, v):
        """ Sets a cell to a given value"""
        self.grid.cells[y][x] = v
        self.show()

    def set_spectrum(self):
        """ Sets the spectrum of the grid """
        try: 
            self.grid.set_A(float(self.entry_spectrum.get()))
            return True
        except: 
            tkinter.messagebox.showerror("Invalid spectrum", "Invalid spectrum: Float expected!")
            return False
        
    def set_flattness(self):
        """ Sets the flattness of the grid """
        try: 
            self.grid.set_P(float(self.entry_flattness.get()))
            return True
        except:
            tkinter.messagebox.showerror("Invalid flattness", "Invalid flattness: Float expected!")
            return False


    def show(self):
        grey = np.array([[int((1-c) * 255) for c in line ] for line in self.grid.cells])
        self.im = Image.fromarray(grey).resize((WIDTH * ZOOM, HEIGHT * ZOOM))
        self.pi = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(1, 1, image=self.pi, anchor=Tk.NW)
    
    def iter(self):
        if self.set_spectrum() and self.set_flattness() and self.set_birth_function_roots() and self.set_durability_function_roots():
            try: 
                self.grid.iter_cells()
                self.show()
            except Exception as e:
                tkinter.messagebox.showerror("Unable to iterate", "Unable to iterate because during calculation this exception occurred: " + str(e))
                raise e
            
        #self.grid.print_field()


root = Tk.Tk()
gui = Gui(root)
root.mainloop()



