import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import math
import csv
conn = sqlite3.connect("main.db")#main database conn.
cursor=conn.cursor()

#####################################################
def calculator():
    def check():
        rec=main.get()
        tt=total.get()
        if rec<0:
            return messagebox.showerror('Error','Invalid')
        elif rec==0:
            return messagebox.showerror('Error','Invalid')
        elif tt<0:
            return messagebox.showerror('Error','Invalid')
        elif tt==0:
            return messagebox.showerror('Error','Invalid')
        else:
            result=(rec/tt)*100
            last=round(result)
            messagebox.showinfo('Result',str(last)+'%')
    calc=Toplevel()
    main=IntVar()
    total=IntVar()
    calc.geometry('400x400')
    calc.title('percentage calculator')

    Label(calc,text='enter mark',font='Helvetica 12 bold').grid(row=1,column=4)
    Label(calc,text='marks').grid(row=2,column=2)
    Entry(calc,width=3,textvariable=main).grid(row=3,column=2)
    Label(calc,text='/').grid(row=2,column=3)
    Label(calc,text='Total').grid(row=2,column=4)
    Entry(calc,width=3,textvariable=total).grid(row=3,column=4)
    Button(calc,text='Calculate',command=check).grid(row=4,column=5)

def subpro():#subject projection
    sub=Toplevel()
    sub.geometry('400x400')
    sub.title('Subject Projection')
    first=IntVar()
    second=IntVar()
    third=IntVar()
    fourth=IntVar()
    fifth=IntVar()
    sixth=IntVar()
    subject=StringVar()
    ch=IntVar()
    def check():
        percentage=['90%-100%','75%-90%','60%-75%','45%-60%','35%-40%','below 35%']
        subname=subject.get()
        aa=first.get()
        bb=second.get()
        cc=third.get()
        dd=fourth.get()
        ee=fifth.get()
        ff=sixth.get()
        choice=ch.get()
        numbers=[aa,bb,cc,dd,ee,ff]
        col=['green','blue','violet','yellow','black','red']
        plt.title(subname)
        if choice==1:#bargraph
            plt.bar(percentage,numbers)
        elif choice==2:#piechart
            plt.pie(numbers,labels=percentage,colors=col,shadow=True,startangle=140)
        else:
            return messagebox.showerror('Error','Enter Type of Graph')
        plt.show()
       
    Label(sub,text='Enter details').grid(row=1,column=2)
    Label(sub,text='Enter Graph Title').grid(row=2,column=1)
    Entry(sub,width=20,textvariable=subject).grid(row=2,column=2)
    Label(sub,text='Percentage').grid(row=3,column=2)
    Label(sub,text='no. of students').grid(row=3,column=3)
    Label(sub,text='90%-100%').grid(row=4,column=2)
    Label(sub,text='75%-90%').grid(row=5,column=2)
    Label(sub,text='60%-75%').grid(row=6,column=2)
    Label(sub,text='below 35%').grid(row=9,column=2)
    Label(sub,text='45%-60%').grid(row=7,column=2)
    Label(sub,text='35%-40%').grid(row=8,column=2)
    Entry(sub,width=2,textvariable=first).grid(row=4,column=3)
    Entry(sub,width=2,textvariable=second).grid(row=5,column=3)
    Entry(sub,width=2,textvariable=third).grid(row=6,column=3)
    Entry(sub,width=2,textvariable=fourth).grid(row=7,column=3)
    Entry(sub,width=2,textvariable=fifth).grid(row=8,column=3)
    Entry(sub,width=2,textvariable=sixth).grid(row=9,column=3)
    Label(sub,text='Type of Graph').grid(row=10,column=2)
    Radiobutton(sub,text='BarGraph',variable=ch,value=1).grid(row=11,column=2)
    Radiobutton(sub,text='PieChart',variable=ch,value=2).grid(row=11,column=3)
    Button(sub,text='Plot',command=check).grid(row=12,column=4)


###################################################################################################################

def classprofile():#classprofile
    global subjects #subjectlist
    global clname
    global fil
    global filters #filterlist
    global flag
    exams=['-select-','PT1','PT2','HFYEARLY','PT3','PT4','M1','M2','FINAL']
    clname=s.get()
    nclass= sqlite3.connect(clname+".db")
    ncursor=nclass.cursor()
    sql22='SELECT subject1,subject2,subject3,subject4,subject5 FROM clsaccounts WHERE classname=?'
    cursor.execute(sql22, (clname,))
    row=cursor.fetchall()
    data=row[0]
    sub=[]
    subjects=['-select-']
    for i in range(len(data)):
        subjects.append(data[i])#subjectslist
        sub.append(data[i])
    ncursor.execute('select studentname from stdetails')
    st=ncursor.fetchall()
    students=['-select-'] 
    for i in range(len(st)):
        stu=st[i]
        students.append(stu[0]) #studentslist
    def remove():
        def pre():
            name=nm.get()
            ex='delete from stdetails where studentname=?'
            ncursor.execute(ex,(name,))
            nclass.commit()
            ex1='delete from subdetails where studentname=?'
            ncursor.execute(ex1,(name,))
            nclass.commit()
            rem.destroy()
            messagebox.showinfo('Result','Student Removed Successfully')
            cprofile.destroy()
            classprofile()
        nms=[]#student names
        nm=StringVar()
        ncursor.execute('select studentname from stdetails')
        d=ncursor.fetchall()
        for i in d:
            i=i[0]
            nms.append(i)
        rem=Toplevel()
        rem.geometry('300x300')
        rem.title('Remove Student')
        Label(rem,text='Select Student').grid(row=1,column=1)
        stuselect1=ttk.Combobox(rem,values=nms,state='readonly',textvariable=nm)
        stuselect1.grid(row=1,column=2)
        stuselect1.current(0)
        Button(rem,text='Proceed',command=pre).grid(row=2,column=2)

    def cperformance():
        ncursor.execute('select * from stdetails')
        row=ncursor.fetchall()#data-stdetails
        rows=len(row) #number of students
        def ok():
            def project():
                ms=[]#marks-list
                names=[]#names-lists
                ex='select studentname from stdetails'
                ex1='select '+exam+' from stdetails'
                ncursor.execute(ex)
                d=ncursor.fetchall()
                for i in d:
                    i=i[0]
                    names.append(i)
                ncursor.execute(ex1)
                d=ncursor.fetchall()
                for i in d:
                    i=i[0]
                    ms.append(i)
                plt.title(exam+' marks')
                plt.xlabel('students')
                plt.ylabel('marks')
                plt.bar(names,ms,width=0.3)
                plt.show()

                
            exam=exm.get()
            if exam=='-select-':
                return messagebox.showerror('Error','Select Exam')
            else:
                marks=[]
                ex='select '+exam+' from stdetails'
                ncursor.execute(ex)
                fe=ncursor.fetchall()
                for i in fe:
                    i=i[0]
                    marks.append(i)
                mar=sum(marks)/len(marks)
                cp.destroy()
                cpf=Toplevel()
                cpf.geometry('400x400')
                cpf.title('Class Performance-CMS')
                Label(cpf,text='Class: '+clname,font='Helvetica 12 bold').grid(row=1,column=1)
                Label(cpf,text='Number of students: '+str(rows)).grid(row=2,column=1)
                Label(cpf,text='Exam Type: '+exam).grid(row=3,column=1)
                Label(cpf,text='Class Average: '+str(round(mar))+'%').grid(row=4,column=1)
                Label(cpf,text='---Individual Marks---').grid(row=5,column=2)
                Button(cpf,text=sub[0]+' marks',command=sub1m).grid(row=6,column=1)
                Button(cpf,text=sub[1]+' marks',command=sub2m).grid(row=7,column=1)
                Button(cpf,text=sub[2]+' marks',command=sub3m).grid(row=8,column=1)
                Button(cpf,text=sub[3]+' marks',command=sub4m).grid(row=9,column=1)
                Button(cpf,text=sub[4]+' marks',command=sub5m).grid(row=10,column=1)
                Button(cpf,text='Project Scores',command=project).grid(row=10,column=3)


        exm=StringVar()
        cp=Toplevel()
        cp.geometry('300x200')
        cp.title('Class Performance-CMS')
        Label(cp,text='Select exam').grid(row=1,column=1)
        stuselect1=ttk.Combobox(cp,values=['-select-','PT1','PT2','HFYEARLY','PT3','PT4','M1','M2','FINAL'],state='readonly',textvariable=exm)
        stuselect1.grid(row=1,column=2)
        stuselect1.current(0)
        Button(cp,text='Proceed',command=ok).grid(row=3,column=2)
        
    def sreport(): #student report
        def report():
            def project():
                plt.title(exm+' projection')
                plt.xlabel('Subjects')
                plt.ylabel('Marks')
                plt.bar(sub,ms)
                plt.show()
            stname=student.get()
            exm=exam.get()
            if stname=='-select-':
                return messagebox.showerror('Error','Select Student')
            elif exm=='-select-':
                return messagebox.showerror('Error','Select Exam')
            else:
                ms=[]#obtained marks
                ask.destroy()
                rep=Toplevel()
                rep.geometry('550x400')
                rep.title('Student Report-CMS')
                Label(rep,text='Class:'+clname,font='Helvetica 12 bold').grid(row=1,column=1)
                Label(rep,text='Student Name:'+stname).grid(row=2,column=1)
                Label(rep,text='Exam Type:'+exm).grid(row=3,column=1)
                Label(rep,text='----Mark Distribution----').grid(row=4,column=2)
                exec1='select '+exm+' from subdetails where studentname=? and subject=?'
                det=(stname,sub[0])
                ncursor.execute(exec1,det)
                row=ncursor.fetchall()
                row1=row[0]
                row2=row1[0]
                ms.append(row2)
                Label(rep,text=sub[0]+'marks: '+str(row2)).grid(row=5,column=2)
                exec1='select '+exm+' from subdetails where studentname=? and subject=?'
                det=(stname,sub[1])
                ncursor.execute(exec1,det)
                row=ncursor.fetchall()
                row1=row[0]
                row2=row1[0]
                ms.append(row2)
                Label(rep,text=sub[1]+'marks: '+str(row2)).grid(row=6,column=2)
                exec1='select '+exm+' from subdetails where studentname=? and subject=?'
                det=(stname,sub[2])
                ncursor.execute(exec1,det)
                row=ncursor.fetchall()
                row1=row[0]
                row2=row1[0]
                ms.append(row2)
                Label(rep,text=sub[2]+'marks: '+str(row2)).grid(row=7,column=2)
                exec1='select '+exm+' from subdetails where studentname=? and subject=?'
                det=(stname,sub[3])
                ncursor.execute(exec1,det)
                row=ncursor.fetchall()
                row1=row[0]
                row2=row1[0]
                ms.append(row2) 
                Label(rep,text=sub[3]+'marks: '+str(row2)).grid(row=8,column=2)
                exec1='select '+exm+' from subdetails where studentname=? and subject=?'
                det=(stname,sub[4])
                ncursor.execute(exec1,det)
                row=ncursor.fetchall()
                row1=row[0]
                row2=row1[0]
                ms.append(row2)
                Label(rep,text=sub[4]+'marks: '+str(row2)).grid(row=9,column=2)
                exec1='select '+exm+' from stdetails where studentname=?'
                ncursor.execute(exec1,(stname,))
                row=ncursor.fetchall()
                row1=row[0]
                row2=row1[0]
                Label(rep,text='Total Percentage: '+str(row2)+'%').grid(row=10,column=1)
                Button(rep,text='Project Scores',command=project).grid(row=10,column=3)

        student=StringVar()
        exam=StringVar()
        ncursor.execute('select studentname from stdetails')
        st=ncursor.fetchall()
        students=['-select-'] 
        for i in range(len(st)):
            stu=st[i]
            students.append(stu[0]) #studentslist
        ask=Toplevel()
        ask.geometry('300x300')
        ask.title('enter details')
        Label(ask,text='Select student name:').grid(row=1,column=1)
        stuselect2=ttk.Combobox(ask,values=students,state='readonly',textvariable=student)
        stuselect2.grid(row=1,column=2)
        stuselect2.current(0)
        Label(ask,text='Select exam').grid(row=2,column=1)
        stuselect1=ttk.Combobox(ask,values=['-select-','PT1','PT2','HFYEARLY','PT3','PT4','M1','M2','FINAL'],state='readonly',textvariable=exam)
        stuselect1.grid(row=2,column=2)
        stuselect1.current(0)
        Button(ask,text='Proceed',command=report).grid(row=3,column=2)

    def mrksheetupload():#upload marksheet 
        def file1():
            outof=0
            mexe=mex.get() #type of exam
            subj=subu.get()
            outof=mrs.get()
            if subj=='-select-':
                return messagebox.showerror('Error','Enter Subject')
            if mexe=='-select-':
                return messagebox.showerror('Error','Enter Name')
            if outof==0:
                return messagebox.showerror('Error','Select Total Marks')
            ft=[("CSV",".csv"),('All Files',"'*")]
            file=fd.askopenfilename(parent=upload,initialdir='/',title='Select File',filetypes=ft,defaultextension=ft)
            mrdata=[] #main data
            datas=[]#cleaned data
            with open(file,'r') as csvfile:
                readCSV = csv.reader(csvfile)
                for row23 in readCSV:
                    mrdata.append(row23)  #appending data             
                for i in range(len(mrdata)):
                    if i%2==0:
                        datas.append(mrdata[i]) #cleaning data
                datas.pop(0)
                print(datas)
                dat=[]
                for i in range(len(datas)):
                    dat=datas[i]
                    sq='UPDATE subdetails SET '+mexe+' = ? WHERE studentname = ?  AND subject = ?' #for subdetails
                    data32=(int(dat[1]),dat[0],subj)
                    ncursor.execute(sq,data32)
                    nclass.commit()
                    pers=[]
                    execu='select '+mexe+' from stdetails where studentname=?'
                    ncursor.execute(execu, (dat[0],))
                    tm=ncursor.fetchall()
                    tm=tm[0]
                    tms=tm[0]
                    pers.append(tms)
                    per=(int(dat[1])/outof)*100 #current percentage
                    pers.append(per)
                    avg1=sum(pers)/len(pers) #total precentage
                    avg=round(avg1)
                    sql37='UPDATE stdetails SET '+mexe+' = ? WHERE studentname = ?' #for stdetails
                    data37=(avg,dat[0])
                    ncursor.execute(sql37,data37)
                    nclass.commit()
                upload.destroy()
                messagebox.showinfo('Result','Marks Uploaded')
                cprofile.destroy()
                classprofile()
        mex=StringVar()
        subu=StringVar()
        upload=Toplevel()
        mrs=IntVar()
        upload.geometry('300x300')
        upload.title('Marksheet Upload')
        Label(upload,text='Enter Details').grid(row=1,column=2)
        Label(upload,text='Select Exam').grid(row=2,column=1)
        sel=ttk.Combobox(upload,values=['-select-','PT1','PT2','HFYEARLY','PT3','PT4','M1','M2','FINAL'],state='readonly',textvariable=mex)
        sel.grid(row=2,column=2)
        sel.current(0)
        Label(upload,text='Select Subject').grid(row=3,column=1)
        sel1=ttk.Combobox(upload,values=['-select-',sub[0],sub[1],sub[2],sub[3],sub[4]],state='readonly',textvariable=subu)
        sel1.grid(row=3,column=2)
        sel1.current(0)
        Label(upload,text='Marks are out of:').grid(row=4,column=1)
        Radiobutton(upload,text='20',variable=mrs,value=20).grid(row=5,column=1)
        Radiobutton(upload,text='30',variable=mrs,value=30).grid(row=5,column=2)
        Radiobutton(upload,text='70',variable=mrs,value=70).grid(row=5,column=3)
        Radiobutton(upload,text='80',variable=mrs,value=80).grid(row=5,column=4)
        Button(upload,text='Select File:',command=file1).grid(row=6,column=1)
      

    def dmarksheet():#saving marksheet
        ft=[('CSV file','*.csv')]
        file=fd.asksaveasfile(filetypes=ft,mode="w",defaultextension=ft)
        fieldnames=['Student Name','Marks']
        writer=csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader() 
        ncursor.execute('select studentname from stdetails;')
        row331=ncursor.fetchall()
        for i in range(len(row331)):
            row33=row331[i]
            nm=row33[0]#name
            writer.writerow({'Student Name':nm,'Marks':0})
        file.close()
        print('complete')
    def sub1m(): #subject1 marks
        execu='select * from subdetails where subject=?'
        ncursor.execute(execu,(subjects[1],))
        marks=ncursor.fetchall()
        sub1=Toplevel()
        sub1.geometry('800x500')
        sub1.title(subjects[1]+' marks')
        scroll1=ttk.Scrollbar(sub1)
        scroll1.grid(row=1,column=2)
        tb1=ttk.Treeview(sub1,columns=(1,2,3,4,5,6,7,8,9,10,11),show='headings',selectmode='browse')
        tb1.grid(row=1,column=1)
        tb1.heading(1,text="Grno")
        tb1.column(1,minwidth=0,width=50,stretch=NO)
        tb1.heading(2,text="Studentname")
        tb1.column(2,minwidth=0,width=120,stretch=NO)
        tb1.heading(3,text="Subject")
        tb1.column(3,minwidth=0,width=50,stretch=NO)
        tb1.heading(4,text="PT1")
        tb1.column(4,minwidth=0,width=50,stretch=NO)
        tb1.heading(5,text="PT2")
        tb1.column(5,minwidth=0,width=50,stretch=NO)
        tb1.heading(6,text="HFYEARLY")
        tb1.column(6,minwidth=0,width=80,stretch=NO)
        tb1.heading(7,text="PT3")
        tb1.column(7,minwidth=0,width=50,stretch=NO)
        tb1.heading(8,text="PT4")
        tb1.column(8,minwidth=0,width=50,stretch=NO)
        tb1.heading(9,text="M1")
        tb1.column(9,minwidth=0,width=50,stretch=NO)
        tb1.heading(10,text="M2")
        tb1.column(10,minwidth=0,width=70,stretch=NO)
        tb1.heading(11,text="FINAL")
        tb1.column(11,minwidth=0,width=70,stretch=NO)
        scroll1.config(command=tb1.yview)
        for i in marks: #appending details(subdetails)
           tb1.insert('','end',values=i)
    def sub2m(): #subject 2 marks
        execu='select * from subdetails where subject=?'
        ncursor.execute(execu,(subjects[2],))
        marks=ncursor.fetchall()
        sub2=Toplevel()
        sub2.geometry('800x500')
        sub2.title(subjects[2]+' marks')
        scroll1=ttk.Scrollbar(sub2)
        scroll1.grid(row=1,column=2)
        tb1=ttk.Treeview(sub2,columns=(1,2,3,4,5,6,7,8,9,10,11),show='headings',selectmode='browse')
        tb1.grid(row=1,column=1)
        tb1.heading(1,text="Grno")
        tb1.column(1,minwidth=0,width=50,stretch=NO)
        tb1.heading(2,text="Studentname")
        tb1.column(2,minwidth=0,width=120,stretch=NO)
        tb1.heading(3,text="Subject")
        tb1.column(3,minwidth=0,width=50,stretch=NO)
        tb1.heading(4,text="PT1")
        tb1.column(4,minwidth=0,width=50,stretch=NO)
        tb1.heading(5,text="PT2")
        tb1.column(5,minwidth=0,width=50,stretch=NO)
        tb1.heading(6,text="HFYEARLY")
        tb1.column(6,minwidth=0,width=80,stretch=NO)
        tb1.heading(7,text="PT3")
        tb1.column(7,minwidth=0,width=50,stretch=NO)
        tb1.heading(8,text="PT4")
        tb1.column(8,minwidth=0,width=50,stretch=NO)
        tb1.heading(9,text="M1")
        tb1.column(9,minwidth=0,width=50,stretch=NO)
        tb1.heading(10,text="M2")
        tb1.column(10,minwidth=0,width=70,stretch=NO)
        tb1.heading(11,text="FINAL")
        tb1.column(11,minwidth=0,width=70,stretch=NO)
        scroll1.config(command=tb1.yview)
        for i in marks: #appending details(subdetails)
           tb1.insert('','end',values=i)
    def sub3m(): #subject3 marks
        execu='select * from subdetails where subject=?'
        ncursor.execute(execu,(subjects[3],))
        marks=ncursor.fetchall()
        sub3=Toplevel()
        sub3.geometry('800x500')
        sub3.title(subjects[3]+' marks')
        scroll1=ttk.Scrollbar(sub3)
        scroll1.grid(row=1,column=2)
        tb1=ttk.Treeview(sub3,columns=(1,2,3,4,5,6,7,8,9,10,11),show='headings',selectmode='browse')
        tb1.grid(row=1,column=1)
        tb1.heading(1,text="Grno")
        tb1.column(1,minwidth=0,width=50,stretch=NO)
        tb1.heading(2,text="Studentname")
        tb1.column(2,minwidth=0,width=120,stretch=NO)
        tb1.heading(3,text="Subject")
        tb1.column(3,minwidth=0,width=50,stretch=NO)
        tb1.heading(4,text="PT1")
        tb1.column(4,minwidth=0,width=50,stretch=NO)
        tb1.heading(5,text="PT2")
        tb1.column(5,minwidth=0,width=50,stretch=NO)
        tb1.heading(6,text="HFYEARLY")
        tb1.column(6,minwidth=0,width=80,stretch=NO)
        tb1.heading(7,text="PT3")
        tb1.column(7,minwidth=0,width=50,stretch=NO)
        tb1.heading(8,text="PT4")
        tb1.column(8,minwidth=0,width=50,stretch=NO)
        tb1.heading(9,text="M1")
        tb1.column(9,minwidth=0,width=50,stretch=NO)
        tb1.heading(10,text="M2")
        tb1.column(10,minwidth=0,width=70,stretch=NO)
        tb1.heading(11,text="FINAL")
        tb1.column(11,minwidth=0,width=70,stretch=NO)
        scroll1.config(command=tb1.yview)
        for i in marks: #appending details(subdetails)
           tb1.insert('','end',values=i)
    def sub4m(): #subject3marks
        execu='select * from subdetails where subject=?'
        ncursor.execute(execu,(subjects[4],))
        marks=ncursor.fetchall()
        sub4=Toplevel()
        sub4.geometry('800x500')
        sub4.title(subjects[4]+' marks')
        scroll1=ttk.Scrollbar(sub4)
        scroll1.grid(row=1,column=2)
        tb1=ttk.Treeview(sub4,columns=(1,2,3,4,5,6,7,8,9,10,11),show='headings',selectmode='browse')
        tb1.grid(row=1,column=1)
        tb1.heading(1,text="Grno")
        tb1.column(1,minwidth=0,width=50,stretch=NO)
        tb1.heading(2,text="Studentname")
        tb1.column(2,minwidth=0,width=120,stretch=NO)
        tb1.heading(3,text="Subject")
        tb1.column(3,minwidth=0,width=50,stretch=NO)
        tb1.heading(4,text="PT1")
        tb1.column(4,minwidth=0,width=50,stretch=NO)
        tb1.heading(5,text="PT2")
        tb1.column(5,minwidth=0,width=50,stretch=NO)
        tb1.heading(6,text="HFYEARLY")
        tb1.column(6,minwidth=0,width=80,stretch=NO)
        tb1.heading(7,text="PT3")
        tb1.column(7,minwidth=0,width=50,stretch=NO)
        tb1.heading(8,text="PT4")
        tb1.column(8,minwidth=0,width=50,stretch=NO)
        tb1.heading(9,text="M1")
        tb1.column(9,minwidth=0,width=50,stretch=NO)
        tb1.heading(10,text="M2")
        tb1.column(10,minwidth=0,width=70,stretch=NO)
        tb1.heading(11,text="FINAL")
        tb1.column(11,minwidth=0,width=70,stretch=NO)
        scroll1.config(command=tb1.yview)
        for i in marks: #appending details(subdetails)
           tb1.insert('','end',values=i)
    def sub4m():
        execu='select * from subdetails where subject=?'
        ncursor.execute(execu,(subjects[4],))
        marks=ncursor.fetchall()
        sub4=Toplevel()
        sub4.geometry('800x500')
        sub4.title(subjects[4]+' marks')
        scroll1=ttk.Scrollbar(sub4)
        scroll1.grid(row=1,column=2)
        tb1=ttk.Treeview(sub4,columns=(1,2,3,4,5,6,7,8,9,10,11),show='headings',selectmode='browse')
        tb1.grid(row=1,column=1)
        tb1.heading(1,text="Grno")
        tb1.column(1,minwidth=0,width=50,stretch=NO)
        tb1.heading(2,text="Studentname")
        tb1.column(2,minwidth=0,width=120,stretch=NO)
        tb1.heading(3,text="Subject")
        tb1.column(3,minwidth=0,width=50,stretch=NO)
        tb1.heading(4,text="PT1")
        tb1.column(4,minwidth=0,width=50,stretch=NO)
        tb1.heading(5,text="PT2")
        tb1.column(5,minwidth=0,width=50,stretch=NO)
        tb1.heading(6,text="HFYEARLY")
        tb1.column(6,minwidth=0,width=80,stretch=NO)
        tb1.heading(7,text="PT3")
        tb1.column(7,minwidth=0,width=50,stretch=NO)
        tb1.heading(8,text="PT4")
        tb1.column(8,minwidth=0,width=50,stretch=NO)
        tb1.heading(9,text="M1")
        tb1.column(9,minwidth=0,width=50,stretch=NO)
        tb1.heading(10,text="M2")
        tb1.column(10,minwidth=0,width=70,stretch=NO)
        tb1.heading(11,text="FINAL")
        tb1.column(11,minwidth=0,width=70,stretch=NO)
        scroll1.config(command=tb1.yview)
        for i in marks: #appending details(subdetails)
           tb1.insert('','end',values=i)
    def sub5m(): #subject5 marks
        execu='select * from subdetails where subject=?'
        ncursor.execute(execu,(subjects[5],))
        marks=ncursor.fetchall()
        sub5=Toplevel()
        sub5.geometry('800x500')
        sub5.title(subjects[5]+' marks')
        scroll1=ttk.Scrollbar(sub5)
        scroll1.grid(row=1,column=2)
        tb1=ttk.Treeview(sub5,columns=(1,2,3,4,5,6,7,8,9,10,11),show='headings',selectmode='browse')
        tb1.grid(row=1,column=1)
        tb1.heading(1,text="Grno")
        tb1.column(1,minwidth=0,width=50,stretch=NO)
        tb1.heading(2,text="Studentname")
        tb1.column(2,minwidth=0,width=120,stretch=NO)
        tb1.heading(3,text="Subject")
        tb1.column(3,minwidth=0,width=50,stretch=NO)
        tb1.heading(4,text="PT1")
        tb1.column(4,minwidth=0,width=50,stretch=NO)
        tb1.heading(5,text="PT2")
        tb1.column(5,minwidth=0,width=50,stretch=NO)
        tb1.heading(6,text="HFYEARLY")
        tb1.column(6,minwidth=0,width=80,stretch=NO)
        tb1.heading(7,text="PT3")
        tb1.column(7,minwidth=0,width=50,stretch=NO)
        tb1.heading(8,text="PT4")
        tb1.column(8,minwidth=0,width=50,stretch=NO)
        tb1.heading(9,text="M1")
        tb1.column(9,minwidth=0,width=50,stretch=NO)
        tb1.heading(10,text="M2")
        tb1.column(10,minwidth=0,width=70,stretch=NO)
        tb1.heading(11,text="FINAL")
        tb1.column(11,minwidth=0,width=70,stretch=NO)
        scroll1.config(command=tb1.yview)
        for i in marks: #appending details(subdetails)
           tb1.insert('','end',values=i)
    def addmarks():#adding marks
        def mrks():
            sel=0
            sel=mr.get() #totalmarks
            marks=mrs.get()
            student=stname.get()
            subject=subname.get()
            exam=exm.get()
            if marks<0:
                return messagebox.showerror ('Error','Invalid Marks')
            elif marks>sel:
                return messagebox.showerror('Error','Invalid Marks')
            elif student=='-select-':
                return messagebox.showerror ('Error','select student')
            elif subject=='-select-':
                return messagebox.showerror ('Error','select subject')
            elif exam=='-select-':
                return messagebox.showerror ('Error','select exam')
            elif sel==0:
                return messagebox.showerror ('Error','Enter Total Marks')
            else:
                pers=[]
                execu='select '+exam+' from stdetails where studentname=?'
                ncursor.execute(execu, (student,))
                tm=ncursor.fetchall()
                tm=tm[0]
                tms=tm[0]
                pers.append(tms)
                per=(marks/sel)*100
                pers.append(per)
                avg1=sum(pers)/len(pers) #total precentage
                avg=round(avg1)
                sql1='select grno from stdetails where studentname=?'
                ncursor.execute(sql1, (student,))
                row2=ncursor.fetchall()
                row2=row2[0]
                row2=row2[0]#grno
                
                sql3='UPDATE subdetails SET '+exam+' = ? WHERE studentname = ?  AND subject = ?' #for subdetails
                data44=(marks,student,subject)
                ncursor.execute(sql3,data44)
                nclass.commit()
                sql37='UPDATE stdetails SET '+exam+' = ? WHERE studentname = ?' #for stdetails
                data37=(avg,student)
                ncursor.execute(sql37,data37)
                nclass.commit()
                messagebox.showinfo('Info','Marks Added Successfully')
                adm.destroy()
                cprofile.destroy()
                classprofile()
        mr=IntVar()#totalmarks
        mrs=IntVar()
        stname=StringVar()
        subname=StringVar()
        exm=StringVar()
        mr.set(20)
        adm=Toplevel()
        adm.geometry('400x300')
        adm.title('add marks')
        Label(adm,text='Enter Details').grid(row=1,column=2)
        Label(adm,text='select Student').grid(row=2,column=1)
        Label(adm,text='select subject').grid(row=3,column=1)
        Label(adm,text='select exam').grid(row=4,column=1)
        stuselect=ttk.Combobox(adm,values=students,state='readonly',textvariable=stname)
        stuselect.grid(row=2,column=2)
        stuselect.current(0)
        subselect=ttk.Combobox(adm,values=subjects,state='readonly',textvariable=subname)
        subselect.grid(row=3,column=2)
        subselect.current(0)
        exselect=ttk.Combobox(adm,values=exams,state='readonly',textvariable=exm)
        exselect.grid(row=4,column=2)
        exselect.current(0)
        Label(adm,text='Enter Marks:').grid(row=5,column=1)
        Entry(adm,width=7,textvariable=mrs).grid(row=5,column=2)#mark entry
        Label(adm,text='marks are out of:').grid(row=6,column=1)
        Radiobutton(adm,text='20',variable=mr,value=20).grid(row=7,column=1)
        Radiobutton(adm,text='30',variable=mr,value=30).grid(row=7,column=2)
        Radiobutton(adm,text='70',variable=mr,value=70).grid(row=7,column=3)
        Radiobutton(adm,text='80',variable=mr,value=80).grid(row=7,column=4)
        Button(adm,text='Proceed',command=mrks).grid(row=8,column=4)
    def update():#for refresh
        cprofile.destroy()
        classprofile()
    def addstudent():
        def proceed():
            grno=0
            grno=gr.get()
            name=nm.get()
            if grno==0:
                return messagebox.showerror('Error','Enter Grno.')
            elif name=='':
                return messagebox.showerror('Error','Enter Student Name')
            else:
                sql6="""INSERT INTO stdetails
                          (grno,studentname,PT1,PT2,HFYEARLY,PT3,PT4,M1,M2,FINAL) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                data = (grno,name,0,0,0,0,0,0,0,0)
                ncursor.execute(sql6,data)
                nclass.commit()
                add.destroy()
                for i in range(len(sub)):
                                sq23="""INSERT INTO subdetails
                                         (grno,studentname,subject,PT1,PT2,HFYEARLY,PT3,PT4,M1,M2,FINAL) 
                                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                                data = (grno,name,sub[i],0,0,0,0,0,0,0,0)
                                ncursor.execute(sq23,data)
                                nclass.commit()
        gr=IntVar()
        nm=StringVar()
        add=Toplevel()
        add.title('New Student')
        add.geometry('400x200')
        Label(add,text='Enter Details',font='Helvetica 12 bold').grid(row=1,column=2)
        Label(add,text='Enter Grno.').grid(row=2,column=1)
        Entry(add,width=6,textvariable=gr).grid(row=2,column=2)
        Label(add,text='Enter Student Name').grid(row=3,column=1)
        Entry(add,width=25,textvariable=nm).grid(row=3,column=2)
        Button(add,text='Proceed',command=proceed).grid(row=4,column=3)
        ####---

    
    ncursor.execute('select * from stdetails')
    row=ncursor.fetchall()#data-stdetails
    rows=len(row)
    ncursor.execute('select * from subdetails')
    staticrow=ncursor.fetchall()
    cprofile=Toplevel() #class-profile-GUI
    cprofile.geometry('1100x700')
    cprofile.title('classprofile-CMS')
    Label(cprofile,text='class:'+clname,font='Helvetica 12 bold').grid(row=1,column=1)
    Label(cprofile,text='No.of students in class:'+str(rows),font='Helvetica 12 bold').grid(row=2,column=1)
    Button(cprofile,text='Add Student',command=addstudent).place(x=650,y=11)
    Button(cprofile,text='Remove Student',command=remove).place(x=650,y=37)
    Button(cprofile,text='Add Marks',command=addmarks).place(x=750,y=11)
    Button(cprofile,text='Attendance Records',fg="red").place(x=830,y=11)
    Button(cprofile,text='Class Performance',command=cperformance).place(x=750,y=37)
    Button(cprofile,text='Student Report',command=sreport).place(x=860,y=37)
    Button(cprofile,text='Refresh',command=update).place(x=960,y=11)
    Label(cprofile,text='Student Details(marks are in %)>>>>>>>').grid(row=3,column=1)
    

    #student details
    scroll=ttk.Scrollbar(cprofile)
    scroll.grid(row=4,column=3)
    tb=ttk.Treeview(cprofile,columns=(1,2,3,4,5,6,7,8,9,10),show='headings',selectmode='browse')
    tb.grid(row=4,column=2)
    
    tb.heading(1,text="Grno")
    tb.column(1,minwidth=0,width=50,stretch=NO)
    tb.heading(2,text="Studentname")
    tb.column(2,minwidth=0,width=120,stretch=NO)
    tb.heading(3,text="PT1(%)")
    tb.column(3,minwidth=0,width=50,stretch=NO)
    tb.heading(4,text="PT2(%)")
    tb.column(4,minwidth=0,width=50,stretch=NO)
    tb.heading(5,text="HFYEARLY(%)")
    tb.column(5,minwidth=0,width=80,stretch=NO)
    tb.heading(6,text="PT3(%)")
    tb.column(6,minwidth=0,width=50,stretch=NO)
    tb.heading(7,text="PT4(%)")
    tb.column(7,minwidth=0,width=50,stretch=NO)
    tb.heading(8,text="M1(%)")
    tb.column(8,minwidth=0,width=50,stretch=NO)
    tb.heading(9,text="M2(%)")
    tb.column(9,minwidth=0,width=50,stretch=NO)
    tb.heading(10,text="FINAL(%)")
    tb.column(10,minwidth=0,width=70,stretch=NO)
    scroll.config(command=tb.yview)
    for i in row: #appending details(stdetails)
        tb.insert('','end',values=i)
    Label(cprofile,text='Student Details with Subjects(Individual Marks)>>>').grid(row=5,column=1)
    #student details with subjects-individual
    scroll1=ttk.Scrollbar(cprofile)
    scroll1.grid(row=6,column=3)
    tb1=ttk.Treeview(cprofile,columns=(1,2,3,4,5,6,7,8,9,10,11),show='headings',selectmode='browse')
    tb1.grid(row=6,column=2)
    
    tb1.heading(1,text="Grno")
    tb1.column(1,minwidth=0,width=50,stretch=NO)
    tb1.heading(2,text="Studentname")
    tb1.column(2,minwidth=0,width=120,stretch=NO)
    tb1.heading(3,text="Subject")
    tb1.column(3,minwidth=0,width=50,stretch=NO)
    tb1.heading(4,text="PT1")
    tb1.column(4,minwidth=0,width=50,stretch=NO)
    tb1.heading(5,text="PT2")
    tb1.column(5,minwidth=0,width=50,stretch=NO)
    tb1.heading(6,text="HFYEARLY")
    tb1.column(6,minwidth=0,width=80,stretch=NO)
    tb1.heading(7,text="PT3")
    tb1.column(7,minwidth=0,width=50,stretch=NO)
    tb1.heading(8,text="PT4")
    tb1.column(8,minwidth=0,width=50,stretch=NO)
    tb1.heading(9,text="M1")
    tb1.column(9,minwidth=0,width=50,stretch=NO)
    tb1.heading(10,text="M2")
    tb1.column(10,minwidth=0,width=70,stretch=NO)
    tb1.heading(11,text="FINAL")
    tb1.column(11,minwidth=0,width=70,stretch=NO)
    scroll1.config(command=tb1.yview)
    for i in staticrow: #appending details(subdetails)
       tb1.insert('','end',values=i)
    Button(cprofile,text=subjects[1]+' marks',command=sub1m).grid(row=7,column=1)
    Button(cprofile,text=subjects[2]+' marks',command=sub2m).grid(row=8,column=1)
    Button(cprofile,text=subjects[3]+' marks',command=sub3m).grid(row=9,column=1)
    Button(cprofile,text=subjects[4]+' marks',command=sub4m).grid(row=10,column=1)
    Button(cprofile,text=subjects[5]+' marks',command=sub5m).grid(row=11,column=1)
    Button(cprofile,text='Download Marksheet',command=dmarksheet).grid(row=8,column=2)
    Button(cprofile,text='Upload Marks',command=mrksheetupload).grid(row=9,column=2)
    Label(cprofile,text='**Attendance Records feature will be available on version 1.3 - Stay Connected for More Updates').grid(row=10,column=2)
    Label(cprofile,text='**Please do not change the format of csv file(marksheet) as it may get corrupted').grid(row=12,column=2)

##############################################################################################################################################################################
def accwindow():#mainprofile
    global s
    def accwindow1():
        dash.destroy()
        accwindow()
    def newclass():#creating new class
        def ok():
            cursor.execute('select classname from clsaccounts;')
            row=cursor.fetchall()
            clname=cname.get()
            flag=0
            for i in range(len(row)):
                tp1=''
                tp=row[i]
                tp1=tp[0]
                if tp1==clname:
                    flag=1
            
            sub1=s1.get()
            sub2=s2.get()
            sub3=s3.get()
            sub4=s4.get()
            sub5=s5.get()
            if clname=='':
                return messagebox.showerror('Error','Enter Class name')
            elif flag==1:
                return messagebox.showerror('Error','Class name used before')    
            elif sub1=='':
                return messagebox.showerror('Error','Enter Subject1')
            elif sub2=='':
                return messagebox.showerror('Error','Enter Subject2')
            elif sub3=='':
                return messagebox.showerror('Error','Enter Subject3')
            elif sub4=='':
                return messagebox.showerror('Error','Enter Subject4')
            elif sub5=='':
                return messagebox.showerror('Error','Enter Subject5')
            else:
             
                sql8="""INSERT INTO clsaccounts
                          (email,classname,subject1,subject2,subject3,subject4,subject5) 
                          VALUES (?, ?, ?, ?, ?, ?, ?);"""
                data = (email,clname,sub1,sub2,sub3,sub4,sub5)
                cur=conn.cursor()
                cur.execute(sql8,data)
                conn.commit()
                conn.close()
                nclass= sqlite3.connect(clname+".db")
                ncursor=nclass.cursor()#cursor for selected class
                ncursor.execute("""CREATE TABLE stdetails (grno INTEGER,studentname TEXT,PT1 INTEGER,PT2 INTEGER,HFYEARLY INTEGER,PT3 INTEGER,PT4 INTEGER,M1 INTEGER,M2 INTEGER,FINAL INTEGER)""")#table for student details
                ncursor.execute("""CREATE TABLE subdetails (grno INTEGER,studentname TEXT,subject TEXT,PT1 INTEGER,PT2 INTEGER,HFYEARLY INTEGER,PT3 INTEGER,PT4 INTGER,M1 INTEGER,M2 INTEGER,FINAL INTEGER)""")#table for subject details
                nclass.close()
                newc.destroy()
                
        
        newc=Toplevel()
        newc.geometry('400x400')
        newc.title('create new class')
        cname=StringVar()
        s1=StringVar()
        s2=StringVar()
        s3=StringVar()
        s4=StringVar()
        s5=StringVar()
        Label(newc,text='Enter Details',font='Helvetica 12 bold').grid(row=1,column=3)
        Label(newc,text='Enter class name:').grid(row=2,column=1)
        Entry(newc,width=11,textvariable=cname).grid(row=2,column=2)
        Label(newc,text='Enter Subject details:').grid(row=3,column=1)
        Label(newc,text='Subject1').grid(row=4,column=1)
        Entry(newc,width=15,textvariable=s1).grid(row=4,column=2)
        Label(newc,text='Subject2').grid(row=5,column=1)
        Entry(newc,width=15,textvariable=s2).grid(row=5,column=2)
        Label(newc,text='Subject3').grid(row=6,column=1)
        Entry(newc,width=15,textvariable=s3).grid(row=6,column=2)
        Label(newc,text='Subject4').grid(row=7,column=1)
        Entry(newc,width=15,textvariable=s4).grid(row=7,column=2)
        Label(newc,text='Subject5').grid(row=8,column=1)
        Entry(newc,width=15,textvariable=s5).grid(row=8,column=2)
        Button(newc,text='OK',command=ok).grid(row=8,column=3)
    def signout():
        dash.destroy()
    classes=[]

    conn = sqlite3.connect("main.db")#main database conn.
    cursor=conn.cursor()
    stat='select * from clsaccounts where email=?'
    cursor.execute(stat, (email,))
    c=cursor.fetchall()
    co=len(c)
    co=str(co)#no. of classes
    #########
    sql='select Name from accdetails where email=?'
    cursor.execute(sql, (email,))
    row=cursor.fetchall()
    row1=row[0]
    finaln=row1[0]
    conn.commit()
    ########
    sql3='select classname from clsaccounts where email=?'
    cursor.execute(sql3, (email,))
    row2=cursor.fetchall()
    count=len(row2)
    for i in range(len(row2)):
        tp=row2[i]
        tp1=tp[0]
        classes.append(tp1)
    dash=Toplevel()
    dash.geometry('500x500')
    dash.title('HomePage-CMS')
    dash['bg'] = '#49A'
    s=StringVar()
    Button(dash,text='SignOut',command=signout).grid(row=1,column=3)
    Label(dash,text='Your DashBoard',font='Helvetica 12 bold',bg='#49A').grid(row=1,column=2)
    Label(dash,text='Your Name: '+finaln,bg='#49A').grid(row=2,column=1)
    Label(dash,text='Email: '+email,bg='#49A').grid(row=3,column=1)
    Label(dash,text='No. of classes:'+co,bg='#49A').grid(row=4,column=1)
    Button(dash,text='Create New Class',command=newclass).grid(row=5,column=1)
    Label(dash,text='Select Class>>>>',bg='#49A').grid(row=6,column=1)
    classselect=ttk.Combobox(dash,values=classes,state='readonly',textvariable=s)
    classselect.grid(row=6,column=2)
    if count!=0:
        classselect.current(0)
    Button(dash,text='Proceed',command=classprofile).grid(row=7,column=3)
    Button(dash,text='refresh',command=accwindow1).grid(row=1,column=4)
def sign():
    def proceed1():
        global email
        email=em.get()
        passwo=pas.get()
        check=[(email,passwo)]
        pre=conn.cursor()
        pre.execute('select email,password from accdetails;')
        row=pre.fetchall()
        flag=0
        for i in range(len(row)):
            if row[i]==check[0]:
                flag=1
        if flag==0:
            return messagebox.showerror('Error','Email/Password is Incorrect')
        else:
            accwindow()
            sign.destroy()
    def account():#newaccount
        sign.destroy()
        def proceed():
            name=n.get()
            email=e.get()
            passw=p.get()
            if name=='':
                return messagebox.showerror('Error','Enter Name')
            elif email=='':
                return messagebox.showerror('Error','Enter email')
            elif passw=='':
                return messagebox.showerror('Error','Enter  Password')
            else:
                nc=conn.cursor()
                sqlite_insert_with_param = """INSERT INTO accdetails
                          (email,password,Name) 
                          VALUES (?, ?, ?);"""
                data_tuple = (email,passw,name)
                nc.execute(sqlite_insert_with_param, data_tuple)
                conn.commit()
                messagebox.showinfo('Result','Registered Successfully')

        n=StringVar()
        e=StringVar()
        p=StringVar()
        new=Toplevel()
        new.title('Create Account')
        new.geometry('400x400')
        Label(new,text='Enter Details',font='Helvetica 12 bold').grid(row=1,column=2)
        Label(new,text='Enter Full Name').grid(row=2,column=1)
        Entry(new,width=25,textvariable=n).grid(row=2,column=2)#name
        Label(new,text='Enter Email').grid(row=3,column=1)
        Entry(new,width=25,textvariable=e).grid(row=3,column=2)#email
        Label(new,text='Enter New Password').grid(row=4,column=1)
        Entry(new,width=25,textvariable=p,show='*').grid(row=4,column=2)#password
        Button(new,text='Proceed',command=proceed).grid(row=5,column=3)

    em=StringVar()
    pas=StringVar()
    sign=Toplevel()
    sign.title('SignIn/CreateAccount-CMS')
    sign.geometry('400x400')
    Label(sign,text='Sign In',font='Helvetica 12 bold').grid(row=1,column=2)
    Button(sign,text='CreateAccount',command=account,bg='yellow').grid(row=1,column=3)
    Label(sign,text='Enter Email Address:').grid(row=2,column=1)
    Entry(sign,width=25,textvariable=em).grid(row=2,column=2)#email
    Label(sign,text='Enter Passsword').grid(row=3,column=1)
    Entry(sign,width=25,textvariable=pas,show='*').grid(row=3,column=2)#password
    Button(sign,text='Proceed',command=proceed1,bg='yellow').grid(row=4,column=3)
    
 

########################################################################################
home=Tk()
home['bg'] = '#49A'
home.geometry('480x300')
home.title('Class-Mangement-System - By Andrew')
Label(home,text='---HOME PAGE---',font='Helvetica 12 bold',bg='#49A').grid(row=1,column=3)
Label(home,text='version 1.2',bg='#49A').grid(row=1,column=4)
Button(home,text='SignIn/Create Account',command=sign,bg='yellow').grid(row=2,column=3)
Button(home,text='Subject Projection',command=subpro,bg='yellow').grid(row=3,column=3)

Button(home,text='percentage calculator',command=calculator,bg='yellow').grid(row=4,column=3)
Label(home,text='**when moving to other windows, do not close this main window!',bg='#49A').grid(row=5,column=3)
Label(home,text='**sign in/create account to Start',bg='#49A').grid(row=6,column=3)
Label(home,text='GitHub: https://github.com/andrew-geeks',bg='#49A').grid(row=7,column=3)
Label(home,text='Twitter: https://twitter.com/andrewissac20',bg='#49A').grid(row=8,column=3)
Label(home,text='Instagram: https://www.instagram.com/_andrewissac',bg='#49A').grid(row=9,column=3)
Label(home,text='Read the tutorialin github on how to get around. Enjoy!!😀',bg='#49A').grid(row=10,column=3)
home.mainloop()


