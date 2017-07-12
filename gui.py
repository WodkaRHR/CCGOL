import PIL.Image as Image
import tkinter as Tk
import PIL.ImageTk as ImageTk
import cconway
import numpy as np
import tkinter.messagebox
import _thread
import time
import tkinter.simpledialog

#Only define integer values
WIDTH, HEIGHT = 50, 50
ZOOM = 12


class Gui(Tk.Frame):

    def __init__(self, root):
        self.root = root
        super().__init__(master=root)
        self.grid = cconway.CGrid(WIDTH, HEIGHT)
        self.auto_iterate_enable = False
        self.auto_iterate_running = False
        canvas_frame = Tk.Frame(master=root)
        canvas_frame.grid(row=0, column=0)
        self.canvas = Tk.Canvas(canvas_frame, width=WIDTH * ZOOM, height = HEIGHT * ZOOM)
        self.canvas.pack()
        self.canvas_image = None

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
        self.entry_durability_function_roots.grid(row=7, sticky=Tk.NW)
        self.entry_durability_function_roots.insert(0, ",".join(map(str, cconway._D)))
        self.entry_durability_function_roots.bind("<Return>", lambda e: self.set_durability_function_roots())

        
        Tk.Label(master=ui_frame, text="Field computation range").grid(row=8, sticky=Tk.NW)
        self.entry_field_computation_range = Tk.Entry(master=ui_frame)
        self.entry_field_computation_range.grid(row=9, sticky=Tk.NW)
        self.entry_field_computation_range.insert(0, ",".join(map(str, [self.grid.xrange, self.grid.yrange])))
        self.entry_field_computation_range.bind("<Return>", lambda e: self.set_field_computation_range())

        self.borders_connected = Tk.IntVar(master=ui_frame, value=int(self.grid.borders_connected))
        self.checkbox_borders_connected = Tk.Checkbutton(master=ui_frame, text="Borders topologically connected", var=self.borders_connected, command=self.set_borders_connected)
        self.checkbox_borders_connected.grid(row=10, sticky=tkinter.NW)

        Tk.Label(master=ui_frame, text="Distance metric").grid(row=11, sticky=tkinter.NW)
        self.distance_metric = Tk.StringVar(master=ui_frame, value="euclid")
        self.option_menu_distance_metric = Tk.OptionMenu(ui_frame, self.distance_metric, "euclid", "max", "average")
        self.option_menu_distance_metric.grid(row=12, sticky=tkinter.NW)

        self.button_iterate = Tk.Button(master=ui_frame, command=self.iter, text="Iterate")
        self.button_iterate.grid(row=13, sticky=Tk.NW)
        self.button_random = Tk.Button(master=ui_frame, command=self.random, text="Random")
        self.button_random.grid(row=14, sticky=Tk.NW)
        self.button_reset = Tk.Button(master=ui_frame, command=self.reset, text="Reset")
        self.button_reset.grid(row=15, sticky=Tk.NW)
        self.canvas.bind("<ButtonPress-1>", lambda e: self.set(int(e.x / ZOOM), int(e.y / ZOOM), 1.0))
        self.canvas.bind("<ButtonPress-3>", lambda e: self.set(int(e.x / ZOOM), int(e.y / ZOOM), 0.0))
        def button_auto_iterate_pressed():
            """ Function to start or end auto iterate """
            if self.auto_iterate_running: self.auto_iterate_enable = False
            else:
                self.auto_iterate_enable = True
                _thread.start_new_thread(self.auto_iterate, () )
                

        self.button_auto_iterate = Tk.Button(master=ui_frame, command=button_auto_iterate_pressed, text="Auto iterate")
        self.button_auto_iterate.grid(row=16, sticky=Tk.NW)
        self.show()

        self.button_export = Tk.Button(master=ui_frame, command=self.export, text="Export")
        self.button_export.grid(row=17, sticky=Tk.NW)
                


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

    def set_borders_connected(self):
        """ Sets if the borders are topologically connected """
        try:
            self.grid.borders_connected = bool(self.borders_connected.get())
            return True
        except Exception as e:
            tkinter.messagebox.showerror("Could not set the connection of the borders", "Following exception occured: " + str(e))
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
        if self.auto_iterate_running: return
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

    def set_distance_metric(self):
        """ Sets the distance metric used """
        try:
            self.grid.set_DISTANCE(self.distance_metric.get())
            return True
        except:
            tkinter.messagebox.showerror("Invalid distance metric", "Invalid distance metric!")
            return False 

    def set_field_computation_range(self):
        """ Sets the computation range of the field function """
        try:
            x, y = map(int, self.entry_field_computation_range.get().split(","))
            self.grid.xrange = x
            self.grid.yrange = y
            return True
        except:
            tkinter.messagebox.showerror("Invalid field computation range", "Invalid field computation range, expected x,y as integers!")
            return False  


    def show(self):
        grey = np.array([[int((1-c) * 255) for c in line ] for line in self.grid.cells])
        self.im = Image.fromarray(grey).resize((WIDTH * ZOOM, HEIGHT * ZOOM))
        self.pi = ImageTk.PhotoImage(self.im)
        if self.canvas_image: self.canvas.delete(self.canvas_image)
        self.canvas_image = self.canvas.create_image(1, 1, image=self.pi, anchor=Tk.NW)
    
    def iter(self):
        if self.set_spectrum() and self.set_flattness() and self.set_birth_function_roots() and self.set_durability_function_roots() and self.set_distance_metric() and self.set_field_computation_range() and self.set_borders_connected():
            try: 
                self.grid.iter_cells()
                self.show()
            except Exception as e:
                tkinter.messagebox.showerror("Unable to iterate", "Unable to iterate because during calculation this exception occurred: " + str(e))
                raise e
            
        #self.grid.print_field()

    def auto_iterate(self):
        """ Function for auto iterating (called inside a paralell thread)"""
        self.button_auto_iterate["text"] = "Stop"
        self.auto_iterate_running = True
        widgets_to_disable = [
            self.entry_birth_function_roots, self.entry_durability_function_roots, self.entry_field_computation_range, self.entry_flattness, self.entry_spectrum,
            self.button_iterate, self.button_random, self.button_reset, self.option_menu_distance_metric, self.checkbox_borders_connected
            ]
        for widget in widgets_to_disable:
            widget.configure(state = "disabled")
        while self.auto_iterate_enable:
            t0 = time.time()
            self.iter()
            t1 = time.time()
            dt = 0.5 - (t1 - t0)
            if dt > 0: time.sleep(dt)
        for widget in widgets_to_disable:
            widget.configure(state = "normal")
        self.button_auto_iterate["text"] = "Auto iterate"
        self.auto_iterate_running = False

    def export(self):
        """ Exports the next iterations """
        num = Tk.simpledialog.askinteger("Number of frames to export", "Enter number of frames to export")
        if not num: return
        path = Tk.simpledialog.askstring("Enter basename", "Enter basename of frames to export (e.g. 'foo/bar' provides foo/bar0.png, foo/bar1.png...)")
        if not path: return
        for i in range(num):
            grey = np.array([[int((1-c) * 255) for c in line ] for line in self.grid.cells])
            image = Image.new("RGB", (WIDTH * ZOOM, HEIGHT * ZOOM))
            image.paste(Image.fromarray(grey).resize((WIDTH * ZOOM, HEIGHT * ZOOM)))
            image.save(path + str(i) + ".png", "PNG")
            self.iter()


root = Tk.Tk()
root.wm_title("Continous Conway's Game Of Life")
gui = Gui(root)
root.mainloop()



