#B-spline GUI
from tkinter import *
import numpy as np
from  matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

point_list=[]
note_list=[]
xlist=[]
ylist=[]
curve_exists=False
mesh_exists=False
mesh=None
def basis(i,p,u,t):
    if p==0:
        if u>=t[i] and u<t[i+1]:
            return 1
        else:
            return 0
        
    else:
            a=u-t[i]
            b=t[i+p]-t[i]
            if b==0:
                c=0
            else:
                 c=a/b

    
            d=t[i+p+1]-u
            e=t[i+p+1]-t[i+1]
            if e==0:
                f=0
            else:
                f=d/e


            return c*basis(i,p-1,u,t)+f*basis(i+1,p-1,u,t)

def create_curve():
    global curve_exists,point_list,xlist,ylist,curve,N,e2_val,note_list
    degree=int(e2_val.get())

    n=len(point_list)
    k=degree+1
    t=[]
    for i in range(0,n+k):
        if i<=k-1:
            t.append(0)
        elif i>=k and i<=n-1:
            t.append(i-k+1)
        else:
            t.append(n-k+1)
    xu=[]
    yu=[]
    N = [ [] for _ in range(n) ]

    for u in np.linspace(0,n-k+1,10*(n-1),endpoint=False):
        x_new=0
        y_new=0
        for i in range(0,n):
            B=basis(i,k-1,u,t)
            x_new+=B*xlist[i]
            y_new+=B*ylist[i]
            N[i].append(B)

        xu.append(x_new)
        yu.append(y_new)
    xu.append(xlist[-1])
    yu.append(ylist[-1])
    
    if curve_exists==True:
        curve.remove()

    curve, =plot1.plot(xu,yu,color='blue',linestyle="-",linewidth=1,label="B-spline")
    plot1.legend(handles=[mesh, curve],bbox_to_anchor=(1.1, 1))
    fig.canvas.draw()
    curve_exists=True
    plot2.cla()
    U=np.linspace(0,n-k+1,10*(n-1)+1,endpoint=True)
    for i in range(0,n):
        if i<n-1:
            N[i].append(0)
        else:
            N[i].append(1)

        point_color=point_list[i].get_color()
        plot2.plot(U,N[i],color=point_color,linestyle="-",linewidth=1,label="N") 
        value=N[i].index(max(N[i]))
        x_pos=U[value]
        y_pos=N[i][value]
        plot2.text(x_pos,y_pos+0.05,s="N{},{}".format(i+1,k-1))
    fig.canvas.draw()


def on_canvas_click(event):
    global drag, index,mesh_exists,mesh,new_point,note_list
    new_point=True
    try:
        x,y=event.xdata,event.ydata
        if len(point_list)>0:
            for j in range(0,len(point_list)):
                if abs(x-xlist[j])<0.05 and abs(y-ylist[j])<0.05:
                    drag=True
                    index=j
                    new_point=False
                    break
                else:
                    new_point=True


    except:
        new_point=False

    if new_point==True:
        point, =plot1.plot(x,y,marker="o",markersize=10)
        point_list.append(point)
        note=plot1.text(x,y+0.1,s="P{}".format(len(point_list)))
        note_list.append(note)

        fig.canvas.draw()
        if mesh_exists==True:
            mesh.remove()
        xlist.append(x)
        ylist.append(y)
        mesh,=plot1.plot(xlist,ylist,color="black",linewidth=1,linestyle="-",label="Mesh")
        mesh_exists=True
        fig.canvas.draw()
        degree=int(e2_val.get())
        if len(point_list)>degree:
            create_curve()
    




def clear_graph():
    global curve_exists,point_list,xlist,ylist,curve,mesh_exists,note_list
    point_list=[]
    note_list=[]
    xlist=[]
    ylist=[]
    curve_exists=False
    mesh_exists=False
    
    plot1.cla()
    plot1.set_xlim(0,2)
    plot1.set_ylim(0,2)
    plot1.set_title("Plot 1")
    plot1.set_xlabel("X-axis")
    plot1.set_ylabel("Y-axis")
    plot2.cla()
    plot2.set_title("Plot 2")
    plot2.set_xlim(0,1)
    plot2.set_ylim(0,1)
    fig.canvas.draw()

def increase_degree():
    global point_list
    degree=int(e2_val.get())
    degree+=1
    e2_val.set(degree)
    if len(point_list)>degree:
        create_curve()


def decrease_degree():
    global point_list
    degree=int(e2_val.get())
    degree-=1
    e2_val.set(degree)
    if len(point_list)>degree:
        create_curve()

def change_degree(event):
    global point_list
    degree=int(e2_val.get())
    if len(point_list)>degree:
        create_curve()

def on_drag(event):
    global drag, index, mesh, N,curve
    if drag==True and index is not None:
        xlist[index] = event.xdata
        ylist[index] = event.ydata
        point_list[index].set_data(xlist[index], ylist[index])
        note_list[index].set_position([xlist[index],ylist[index]+0.1])
        mesh.set_data(xlist,ylist)
        xu=np.dot(xlist,N)
        yu=np.dot(ylist,N)
        curve.set_data(xu,yu)
        canvas.draw()


def on_release(event):
    global drag, index
    drag=False
    index=None

#### MAIN CODE       
##Create the display window
window=Tk()
window.geometry("1600x2000")
window.title("Create B-spline Curve")
window.configure(bg="blue")
frame=Frame(window)
frame.configure(bg="black")
frame.pack()
## Take degree of the curve as input
l2=Label(frame,text="Enter the degree of curve",bg="yellow",font="Arial")
l2.grid(row=0,column=0,)
e2_val=StringVar()
e2=Entry(frame,textvariable=e2_val,width=4,font="Arial")
e2.grid(row=0,column=1,padx=5,pady=0)
e2.bind('<Return>',change_degree)


## Plus and Minus button to add or decrease degree
b2=Button(frame,text="+",command=increase_degree)
b2.grid(row=0,column=2)
b3=Button(frame,text="-",command=decrease_degree)
b3.grid(row=0,column=3)

## Figure to create plot
fig=Figure(figsize=(40,8),dpi=100)
plot1=fig.add_subplot(10,1,(1,6))
plot1.set_title("Plot 1")
plot1.set_xlabel("X-axis")
plot1.set_ylabel("Y-axis")
plot1.set_xlim(0,2)
plot1.set_ylim(0,2)

plot2=fig.add_subplot(10,1,(8,10))
plot2.set_title("Plot 2")
plot2.set_xlim(0,1)
plot2.set_ylim(0,1)
canvas=FigureCanvasTkAgg(figure=fig,master=window)
canvas_widget=canvas.get_tk_widget()
canvas_widget.pack(padx=0,pady=0)
fig.canvas.mpl_connect("button_press_event", on_canvas_click)## 
## Button to clear plot and start new
b1=Button(frame,text="Clear Graph",command=clear_graph,bg="yellow",font="Arial")
b1.grid(row=0,column=4,padx=50,pady=0)

## Drag points to new position
drag=False
index=None
fig.canvas.mpl_connect("motion_notify_event",on_drag)
fig.canvas.mpl_connect("button_release_event",on_release)


window.mainloop()