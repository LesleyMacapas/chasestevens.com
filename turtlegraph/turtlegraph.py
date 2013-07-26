from __future__ import division # floating point division is well important, innit?
from math import sqrt, cos, sin, tan, acos, asin, atan, radians, degrees #Just in case you'd like to use these ever
from Tkinter import * #gui!
from tkMessageBox import *

def find_vertex(coordinates): #expects dictionary of x,y coordinates
    x_list = coordinates.keys()
    op1 = [float(x_list[0]),float(coordinates[x_list[0]])]
    op2 = [float(x_list[1]),float(coordinates[x_list[1]])]
    op3 = [float(x_list[-1]),float(coordinates[x_list[-1]])]
    denom = (op1[0] - op2[0])*(op1[0] - op3[0])*(op2[0] - op3[0]) #begin matrix magic
    a = (op3[0] * (op2[1] - op1[1]) + op2[0] * (op1[1] - op3[1]) + op1[0] * (op3[1] - op2[1])) / denom #stolen from a post on stackoverflow
    b = (op3[0]**2 * (op1[1] - op2[1]) + op2[0]**2 * (op3[1] - op1[1]) + op1[0]**2 * (op2[1] - op3[1])) / denom #which in turn was generated using wolfram mathematica
    c = (op2[0] * op3[0] * (op2[0] - op3[0]) * op1[1] + op3[0] * op1[0] * (op3[0] - op1[0]) * op2[1] + op1[0] * op2[0] * (op1[0] - op2[0]) * op3[1]) / denom #end matrix magic
    x = -(b / (2*a))
    y = c - (b ** 2) / (4 * a) 
    return x,y

def replace_implied_multiplication(string): #turn '75x' into '75 * x'
    import re
    for substring in re.findall('[1234567890]+x',string):
        replacement = substring[:substring.find('x')] + ' * x'
        string = string.replace(substring,replacement)
    return string

def turtlevector(magnitude, angle, origin=[0,0], time=100, gravity=(-9.8)):  #vector conversion
    global output
    xvelocity = magnitude * (cos(radians(angle)))
    yvelocity = magnitude * (sin(radians(angle)))
    output += "For vector with magnitude " + str(magnitude) + " at a " + str(angle) + " degree angle:" + "\n"
    turtlephysics(xvelocity, yvelocity, origin, time, gravity) #passes to main physics function
    return

def general_gui(physics=False):
    import turtle
    global root
    global output
    def unimplemented():
        showwarning("Whoops","Totally unimplemented, dude.")

    def save_output():
        global output
        from tkFileDialog import asksaveasfilename as save
        filename = save(defaultextension='.txt')
        file_io = open(filename,"w")
        file_io.write(output)
        file_io.close()
        output = ''
        showinfo("File Saved",("File successfully saved as %s" %filename))

    def save_graph():
        import ImageGrab #windows only, for now
        from tkFileDialog import asksaveasfilename as save
        canvas = turtle.getscreen().getcanvas()
        turtle.update()
        turtle.listen()
        canvas.update()
        x0 = canvas.winfo_rootx()
        y0 = canvas.winfo_rooty()
        x1 = x0 + canvas.winfo_width()
        y1 = y0 + canvas.winfo_height()
        turtle.listen()
        image = ImageGrab.grab((x0,y0, x1,y1))
        filename = save(defaultextension='.png')
        image.save(filename, "PNG")
        showinfo("File Saved",("File successfully saved as %s" %filename))

    def help_popup():
        try:
            filetext = open('helpfile.txt','r')
            Help = Tk()
            Help.title("TurtleGraph Help")
            scroll = Scrollbar(Help)
            scroll.pack(side=RIGHT, fill=Y)
            text = Text(Help, wrap=WORD, yscrollcommand=scroll.set)
            text.pack()
            scroll.config(command=text.yview)
            for line in filetext.readlines():
                text.insert(END, line)
            text.config(state=DISABLED)
        except IOError:
            showerror("Error","Help file error: Help file missing or corrupt.")

    def switch_physics():
        root.destroy()
        turtle.clear()
        general_gui(True)

    def switch_classic():
        root.destroy()
        turtle.clear()
        general_gui(False)

    def init_outwin(): #open output folder
        global outwin
        try:
            outwin.destroy()
        except:
            None
        outwin = Tk()
        outwin.title("TurtleGraph Output")
        scroll = Scrollbar(outwin)
        scroll.pack(side=RIGHT, fill=Y)
        global outtext
        outtext = Text(outwin, wrap=WORD, yscrollcommand=scroll.set)
        outtext.pack()
        scroll.config(command=outtext.yview)

    global put_outwin
    def put_outwin(*strings): #to go along with any instance of print
        global disp_outwin
        if disp_outwin.get():
            global outtext
            outtext.config(state=NORMAL)
            out = ''
            for string in strings:
               out += str(string) + ' '
            out += '\n'
            outtext.insert(END, out)
            outtext.yview('scroll',1,"units")
            outtext.config(state=DISABLED)

    try:
        root.destroy()
    except:
        None
    root = Tk()
    root.title("TurtleGraph")
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Save Output", command=save_output)
    filemenu.add_command(label="Save Graph", command=save_graph)
    modemenu = Menu(menubar, tearoff=0)
    global disp_outwin
    disp_outwin = IntVar()
    outwin_check = Checkbutton(root, text="Show Output", variable=disp_outwin, onvalue=1, offvalue=0)
    if physics == True:
        modemenu.add_command(label="Classic", command=switch_classic)
        modemenu.add_command(label="Physics", command=unimplemented, state=DISABLED)
    else:
        modemenu.add_command(label="Classic", command=unimplemented, state=DISABLED)
        modemenu.add_command(label="Physics", command=switch_physics)
    menubar.add_cascade(label="Save", menu=filemenu)
    menubar.add_cascade(label="Mode", menu=modemenu)
    menubar.add_command(label="Help", command=help_popup)
    menubar.add_command(label="Quit", command=quit)
    root.config(menu=menubar)
    if physics == True:
        instruct1 = Label(root, text="Magnitude:")
        instruct2 = Label(root, text="Angle:")
        instruct3 = Label(root, text="Origin:")
        instruct4 = Label(root, text="Time:")
        instruct5 = Label(root, text="Gravity:")
        cred = Label(root, text="Created by chase@chasestevens.com\nfor The New School, Kennebunk")
        mag_entry = Entry(root)
        angle_entry = Entry(root)
        origin_entry = Entry(root)
        time_entry = Entry(root)
        grav_entry = Entry(root)
        def plot():
            global outwin
            if disp_outwin.get(): 
                try:
                    outwin.update() #check to see if outwin is already open
                except:
                    init_outwin()
            else:
                try:
                    outwin.destroy()
                except:
                    None
            x = origin_entry.get().replace("^","**")
            if (eval(angle_entry.get()) > 90 or
                eval(angle_entry.get()) < 0):
                showerror("Error","Angle error: Please select an angle between 0 and 90 degrees.")
                return
            turtlevector(float(mag_entry.get()),
                         float(angle_entry.get()),
                         [float(x[0:x.find(',')]), float(x[x.find(',')+1:])],
                         float(time_entry.get()),
                         float(grav_entry.get()))
            return
        def cleargraph():
            global outwin
            try:
                outwin.destroy()
            except:
                None
            turtle.clear()
            gridlines(True)
            return
        go = Button(root, text="         Graph         ", command=plot)
        clear = Button(root, text="          Reset          ", command=cleargraph)
        instruct1.grid(column=0,row=0,columnspan=4)
        mag_entry.grid(column=4,row=0,columnspan=6)
        instruct2.grid(column=0,row=1,columnspan=4)
        angle_entry.grid(column=4,row=1,columnspan=6)
        instruct3.grid(column=0,row=2,columnspan=4)
        origin_entry.grid(column=4,row=2,columnspan=6)
        instruct4.grid(column=0,row=3,columnspan=4)
        time_entry.grid(column=4,row=3,columnspan=6)
        instruct5.grid(column=0,row=4,columnspan=4)
        grav_entry.grid(column=4,row=4,columnspan=6)
        go.grid(column=2,row=5,columnspan=6)
        clear.grid(column=2,row=6,columnspan=6)
        outwin_check.grid(columnspan=10,rowspan=1)
        cred.grid(columnspan=10,rowspan=2)
        origin_entry.insert(0, "0,0")
        time_entry.insert(0, "100")
        grav_entry.insert(0, "-9.8")
        gridlines(True)
    else:
        instruct1 = Label(root, text="Function:")
        instruct2 = Label(root, text="X Minimum:")
        instruct3 = Label(root, text="X Maximum:")
        cred = Label(root, text="Created by chase@chasestevens.com\nfor The New School, Kennebunk")
        func_entry = Entry(root)
        xmin_entry = Entry(root)
        xmax_entry = Entry(root)
        def plot():
            global outwin
            if disp_outwin.get():
                try:
                    outwin.update() #check to see if outwin is already open
                except:
                    init_outwin()
            else:
                try:
                    outwin.destroy()
                except:
                    None
            try:
                turtlegraph(func_entry.get().replace("^","**"),
                            int(xmin_entry.get()),
                            int(xmax_entry.get()))
                return
            except ZeroDivisionError:
                showerror("Error", "Zero Division Error: Can not divide by zero. Try altering function or x-value range.")
            except ValueError:
                showerror("Error", "Integer Error: Please choose integers for the x range values.")
            except SyntaxError:
                showerror("Error", "Syntax Error: Please check the syntax of the function for illegal characters or syntax.")
            except TypeError:
                showerror("Error", "Implied Multiplication Error: Please check the function for any instances of implied multiplication (e.g. \"3x\" as opposed to \"3*x\").")
        def cleargraph():
            global outwin
            try:
                outwin.destroy()
            except:
                None
            if int(xmin_entry.get()) > 0:
                showerror("Error", "X Range Error: Please choose a value for x minimum less than or equal to 0.")
                return
            elif int(xmax_entry.get()) < 0:
                showerror("Error", "X Range Error: Please choose a value for x maximum greater than or equal to 0.")
            else:
                turtle.clear()
                gridlines(False,int(xmin_entry.get()),int(xmax_entry.get()))
                return
        go = Button(root, text="         Graph         ", command=plot)
        clear = Button(root, text="          Reset          ", command=cleargraph)
        instruct1.grid(column=0,row=0,columnspan=4)
        func_entry.grid(column=4,row=0,columnspan=6)
        instruct2.grid(column=0,row=1,columnspan=4)
        xmin_entry.grid(column=4,row=1,columnspan=6)
        instruct3.grid(column=0,row=2,columnspan=4)
        xmax_entry.grid(column=4,row=2,columnspan=6)
        go.grid(column=2,row=3,columnspan=6)
        clear.grid(column=2,row=4,columnspan=6)
        outwin_check.grid(columnspan=10,rowspan=1)
        cred.grid(columnspan=10,rowspan=2)
        xmin_entry.insert(0, "-100")
        xmax_entry.insert(0, "100")
        gridlines(False,int(xmin_entry.get()),int(xmax_entry.get()))
    root.mainloop()
    return

def physics_gui():
    general_gui(True)
    return

def gridlines(physics=False,xmin=-100,xmax=100): # Makes graph for window
    import turtle
    ymin = -(abs(xmin-xmax)/2.)
    ymax = abs(xmin-xmax/2.)
    turtle.setworldcoordinates(xmin,ymin,xmax,ymax)
    turtle.home()
    turtle.hideturtle()
    xadjust = 0
    yadjust = 0
    if physics: #physics window is fixed-size
        xadjust = -50
        yadjust = -50
    turtle.up()
    turtle.setx(xmin + xadjust) #starting x-axis
    turtle.sety(yadjust)
    turtle.down()
    turtle.setheading(0)
    xvals = xmin
    graph_range = 10 + 1
    if physics:
        graph_range = 20 + 1
    for x in range(graph_range):
        turtle.write(str(turtle.xcor()-xadjust)) #writing values for x axis
        turtle.forward(abs(xmin-xmax)/10.) #advancing along x axis
        xvals += abs(xmin-xmax)/10.
        turtle.update()
    turtle.setx(0 + xadjust)
    turtle.sety(0 + yadjust)
    turtle.sety(ymin + yadjust) #starting y-axis
    turtle.setheading(90)
    yvals = ymin
    for y in range(graph_range):
        turtle.write(str(turtle.ycor()-yadjust)) #writing values for y axis
        turtle.forward(abs(ymin-ymax)/10.) #advancing along y axis
        yvals += abs(ymin-ymax)/10.
        turtle.update()
    turtle.setx(0 + xadjust)
    turtle.setx(0 + yadjust)
    turtle.penup()
    return xadjust, yadjust
    return

def turtlegraph(function, xmin=-100, xmax=100):
    import turtle
    global output
    xmin = int(xmin)
    xmax = int(xmax)
    if xmin > 0:
        raise 
    coordinates = {} # creating coordinate dictionary
    function = replace_implied_multiplication(function)
    for xval in range(xmin, xmax+1):
        coordinates[xval] = eval(function.replace("x","(float(" + str(xval) + "))")) # solve equation for y, add to coordinates dictionary
    turtle.home()
    turtle.hideturtle()
    turtle.speed(0) # meh
    turtle.penup()
    print "x , y for function y =", function
    put_outwin("x , y for function y =", function)
    output += "x , y for function y=" + str(function) + "\n"
    for xval in sorted(coordinates.iterkeys()): # graph, baby, graph!
        turtle.setposition(xval, coordinates[xval]) 
        turtle.pendown()
        print turtle.xcor(), ",", turtle.ycor()
        put_outwin(turtle.xcor(), ",", turtle.ycor())
        output += str(turtle.xcor()) + " , " + str(turtle.ycor()) + "\n"
        turtle.update()
    try:
        vertex = find_vertex(coordinates)
        showinfo("Vertex Found",("Parabola vertex was found to be %s" %str(vertex)))
        print "Vertex found: %s" %str(vertex)
        put_outwin("Vertex found:", vertex)
        output += "Vertex found: %s" %str(vertex)
    except:
        None
    print "---------------"
    put_outwin("---------------")
    output += "---------------"  + "\n"
    turtle.penup()
    return

def turtlephysics(xvelocity, yvelocity, origin=[0,0], time=100, gravity=(-9.8)):
    global output
    import turtle
    orig_time = time
    coordinates = {}
    for t in range(time+2):
        coordinates[(origin[0] + xvelocity * t)] = (origin[1] + yvelocity * t + .5 * gravity * t ** 2) #physics!
    xadjust = -50 #shifted axes for physics graphing
    yadjust = -50
    turtle.penup()
    turtle.setposition(origin[0] + xadjust,origin[1] + yadjust)
    turtle.pendown()
    turtle.hideturtle()
    time = 0
    for xval in sorted(coordinates.iterkeys()):
        if (coordinates[xval] <= 0 and
            xval != origin[0]):
            t = (-(sqrt(float(yvelocity) ** 2. + 2. * float(gravity) * float((-origin[1]))) + float(yvelocity))) / gravity
            xval = (origin[0] + xvelocity * t)
            turtle.setposition(xval + xadjust, 0 + yadjust)
            put_outwin(turtle.xcor() - xadjust, ",", turtle.ycor() - yadjust, "@", t, "sec")
            print turtle.xcor() - xadjust, ",", turtle.ycor() - yadjust, "@", t, "sec"
            output += str(turtle.xcor() - xadjust) + " , " + str(turtle.ycor() - yadjust) + " @ " + str(t) + " sec" + "\n"
            break
        turtle.setposition(xval + xadjust, coordinates[xval] + yadjust)
        turtle.pendown()
        print turtle.xcor() - xadjust, ",", turtle.ycor() -yadjust, "@", time, "sec"
        put_outwin(turtle.xcor() - xadjust, ",", turtle.ycor() -yadjust, "@", time, "sec")
        output += str(turtle.xcor() - xadjust) + " , " + str(turtle.ycor() -yadjust) + " @ " + str(time) + " sec" + "\n"
        time += 1
        if time == orig_time+1:
            turtle.penup()
            print "-------------------"
            put_outwin("-------------------")
            output += "-------------------" + "\n"
            return
        turtle.update()
    turtle.penup()
    print "-------------------"
    put_outwin("-------------------")
    output += "-------------------" + "\n"
    return

#Fun Fact: The y=mx+b equation for a circle is y = (+ or -) (sqrt(r^2 - x^2 + 2hx - h^2) + k)
#           In this case, h and k are the x and y coordinates of the circle's centre (r being its radius)
root = Tk()
output = ''
general_gui()
