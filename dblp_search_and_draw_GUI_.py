# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 20:24:50 2016

@author: user
"""


import Tkinter as tk

import tkMessageBox

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import dblp_search_and_draw as dblp

TITLE_FONT = ("Helvetica", 8, "bold")

#source url: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("dblp conference plotter")
        #self.geometry(newGeometry='420x110+500+200')

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo,PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
    def search_dblp_GUI(self,author_name,author_surname,ch_b_var):
        temp_list = dblp.search_dblp(author_name,author_surname)
        if temp_list:
            if ch_b_var:
                dblp.main_function(temp_list[0])
            else:
                #PageTwo.temp_list_names=temp_list_names
                #print PageTwo.temp_list_names
                PageTwo.temp_list=temp_list
                PageTwo.change_temp_list(self.frames["PageTwo"])
                self.show_frame("PageTwo")
        else:
            tkMessageBox.showinfo("Author not found","Sorry author not found. Try again.\n You could try using only his last name")
        
    def back_start(self):
        #PageTwo.clear_PageTwo(self.frames["PageTwo"])
        PageTwo.temp_list=[]
        PageTwo.temp_list_names=[]
        StartPage.clear(self.frames["StartPage"])
        self.show_frame("StartPage")
    
    def search_for_conf_GUI(self,conf_name,ch_b_var):
        print "ch_b_var=",ch_b_var
        temp_list = dblp.search_for_conf(conf_name)
        if temp_list:
            if ch_b_var or temp_list.__len__()==1:
                dblp.main_conf_function(*temp_list[0])
            else:
                PageThree.temp_list_names=[temp[1] for temp in temp_list]
                #print PageTwo.temp_list_names
                PageThree.temp_list=[temp[0] for temp in temp_list]
                PageThree.change_temp_list(self.frames["PageThree"])
                self.show_frame("PageThree")
        else:
            tkMessageBox.showinfo("Conference not found","Sorry conference not found. Please try again.")

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        B = tk.Button(self, text="Submit",  command=lambda: controller.search_dblp_GUI(self.E1.get(), self.E2.get(),self.ch_b_var.get()),highlightcolor='red')
        L0=tk.Label(self,text='Welcome! Give the name and surname of the person of interest',font=TITLE_FONT)
        L0.grid(row=0,column=0,columnspan=2)
        
        self.E1 = tk.Entry(self, bd =5)
        self.E1.grid(row=1,column=1)
        L1=tk.Label(self,text='Name')
        L1.grid(row=1,column=0)
        
        self.E2 = tk.Entry(self, bd =5)
        self.E2.grid(row=2,column=1)
        self.E2.bind('<Return>', lambda e: controller.search_dblp_GUI(self.E1.get(), self.E2.get(), self.ch_b_var.get()))
        L2=tk.Label(self,text='Surname')
        L2.grid(row=2,column=0)
        
        self.ch_b_var= tk.BooleanVar(self,False)
        
        self.ch_b=tk.Checkbutton(self,text='Retrieve First Result',variable=self.ch_b_var,onvalue=True,offvalue=False)
        
        self.ch_b.grid(row=3, column=0)
        
        B.grid(row=1,column=2)#,columnspan=2)
        
        clearButton=tk.Button(self,text='Reset',command = self.clear)
        clearButton.grid(row=3,column=2)
        
        self.B_Go2P1=tk.Button(self,text='Search By Conference',command = lambda: controller.show_frame('PageOne'))
        self.B_Go2P1.grid(row=3,column=1)
        
    def clear(self):
        self.E1.delete(0,'end')
        self.E2.delete(0,'end')
        self.ch_b.deselect()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.B = tk.Button(self, text ="Submit", command = lambda:controller.search_for_conf_GUI(self.E1.get(),self.ch_b_var.get()),highlightcolor='red')
        L0=tk.Label(self,text='Welcome! Give the name of the Conference',font=TITLE_FONT)
        L0.grid(row=0,column=0,columnspan=2)
        
        self.E1 = tk.Entry(self, bd =5)
        self.E1.grid(row=1,column=1)
        self.E1.bind('<Return>', lambda e: controller.search_for_conf_GUI(self.E1.get(),self.ch_b_var.get()))
        L1=tk.Label(self,text='Conference Name')
        L1.grid(row=1,column=0)
                
        self.ch_b_var= tk.BooleanVar(self,False)
        
        self.ch_b=tk.Checkbutton(self,text='Retrieve First Result',variable=self.ch_b_var,onvalue=True,offvalue=False)
        
        self.ch_b.grid(row=3, column=0)
        
        self.B.grid(row=1,column=2)#,columnspan=2)
        
        clearButton=tk.Button(self,text='Reset',command = self.clear)
        clearButton.grid(row=3,column=2)
        
        self.B_Go2P1=tk.Button(self,text='Search By Author',command = lambda: controller.show_frame('StartPage'))
        self.B_Go2P1.grid(row=3,column=1)
    
    def clear(self):
        self.E1.delete(0,'end')
        self.ch_b.deselect()


class PageTwo(tk.Frame):
    
    temp_list=["hi","hi_there"]
    temp_list_names=[]
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        L0=tk.Label(self,text='Please specify the person of interest')
        L0.grid(row=0,column=0,columnspan=1,sticky='w')
        variable= tk.StringVar(self)
        if self.temp_list.__len__()!=0:
            variable.set("hi")
        LB1=tk.OptionMenu(self,variable,*self.temp_list)
        LB1.grid(row=1,column=0)
        #self.temp_list_names=[]
        B2=tk.Button(self, text = "Back to Start page", command= lambda: controller.back_start())
        B2.grid(row=2,column=1)
    def change_temp_list(self):
        variable= tk.StringVar(self)
        if self.temp_list.__len__()!=0:
            variable.set(self.temp_list[0])
        LB1=tk.OptionMenu(self,variable,*self.temp_list)
        LB1.grid(row=1,column=0)
        B = tk.Button(self, text ="Submit", command = lambda: dblp.main_function(variable.get()),highlightcolor='red')
        #B = tk.Button(self, text ="Submit", command = lambda: tkMessageBox.showinfo("Author not found",variable.get()),highlightcolor='red')
        #B = tk.Button(self, text ="Submit", command = lambda: tkMessageBox.showinfo("Author not found",self.temp_list_names[0]),highlightcolor='red')
        print 'hi',self.temp_list_names
        B.grid(row=1,column=1)
        
class PageThree(tk.Frame):
    
    temp_list=["hi","hi_there"]
    temp_list_names=["hi","hi_there"]
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        L0=tk.Label(self,text='Please specify the Conference you are searching for')
        L0.grid(row=0,column=0,columnspan=1,sticky='w')
        variable= tk.StringVar(self)
        if self.temp_list.__len__()!=0:
            variable.set("hi")
        LB1=tk.OptionMenu(self,variable,*self.temp_list_names)
        LB1.grid(row=1,column=0)
        #self.temp_list_names=[]
        B2=tk.Button(self, text = "Back to Start page", command= lambda: controller.back_start())
        B2.grid(row=2,column=1)
    def change_temp_list(self):
        variable= tk.StringVar(self)
        if self.temp_list.__len__()!=0:
            variable.set(self.temp_list_names[0])
        LB1=tk.OptionMenu(self,variable,*self.temp_list_names)
        LB1.grid(row=1,column=0)
        B = tk.Button(self, text="Submit", command=lambda: dblp.main_conf_function(self.temp_list[self.temp_list_names.index(variable.get())], variable.get()), highlightcolor='red')
        #B = tk.Button(self, text ="Submit", command = lambda: tkMessageBox.showinfo("Author not found",variable.get()),highlightcolor='red')
        #B = tk.Button(self, text ="Submit", command = lambda: tkMessageBox.showinfo("Author not found",self.temp_list_names[0]),highlightcolor='red')
        print 'hi',self.temp_list_names
        B.grid(row=1,column=1)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
