from tkinter import *
import sqlite3
import json
import tkinter as tk
import uuid
import time
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox 

root = Tk() 
root.state('zoomed')
root.title("Markdown test") 

 
#Menù Layout
frame3=Frame(root,width=70,height=60, border=5)  
frame6=Frame(root,width=120,height=60, border=5,background="lightgrey")    
frame4=Frame(frame3,width=70,height=20)

def test_hash(test_uuid):
 return hash(test_uuid)
 
Text_bar=Text(frame3, width=60,height=2,wrap="word",undo=True,foreground="grey",font=("sans-serif",12,"bold"))
Text_bar.pack(ipadx=2,ipady=2)

def OpenColumn():
    text_var = StringVar()
    frame3=Frame(root,width=70,height=70, border=5,background="lightgrey")  
    frame4=Frame(frame3,width=70,height=20,background="darkblue")
    Checkbutton5 = IntVar() 
    frame3.config(background="lightgrey")

    Button5 = Checkbutton(frame3, text = "Lock", 
                    variable = Checkbutton5, 
                    onvalue = 1, 
                    offvalue = 0, 
                    
                    )

    def five_event():
     if Checkbutton5.get() == 1:
        
         initialize_data_name()
     else:
        pass

    input_PC = Button(frame3, text = "Pcenter", 
                    command =five_event, 
                    
                    )
    input_PC.grid(column=0, row=0)
    Button5.grid(column=1, row=0)
    entry_t= Entry(frame3, textvariable=text_var, width=45)
    entry_t.grid(column=0, row=1, columnspan=2)
    scroll_bar_mini = tk.Scrollbar(frame3)
    
    Text_t=Text(frame3, width=45,height=8,wrap="word",undo=True,yscrollcommand = scroll_bar_mini.set)
    scroll_bar_mini.config( command = Text_t.yview )
    scroll_bar_mini.grid( sticky = NS,column=2,row=2,rowspan=3,pady=5)
    Text_t.grid(column=0, row=2, columnspan=2,rowspan=3)
   
    def initialize_data_name():
     try:
        name=input_PC.cget('text')
        conn = sqlite3.connect(str(name)+'.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS name (
            id TEXT PRIMARY KEY,
            pubkey INTEGER NOT NULL,
            created_at INTEGER NOT NULL,
            kind INTEGER NOT NULL,
            tags TEXT,
            content TEXT NOT NULL,
            sig TEXT NOT NULL
        )
        ''') 
        conn.commit()
     except sqlite3.Error as e:
        print(f"Errore durante l'inizializzazione del database: {e}")
     finally:
        if conn:
            conn.close()

    def add_PC_event():
     try:
        name=input_PC.cget('text')
        conn = sqlite3.connect(str(name)+'.db')
        c = conn.cursor()
        value=uuid.uuid4()
        event={
    "id": str(value),
    "pubkey": test_hash(value.int),
    "created_at": int(time.time()),  # timestamp corrente
    "kind": 1,
    "tags": [],
    "content": Text_t.get(1.0, "end-1c"),
    "sig":str(value)+str(test_hash(value.int))}
        if event["content"]!="":
         if Checkbutton5.get() == 1: 
          c.execute('''
        INSERT INTO name (id, pubkey, created_at, kind, tags, content, sig)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            event["id"],
            event["pubkey"],
            event["created_at"],
            event["kind"],
            json.dumps(event["tags"]),
            event["content"],
            event["sig"]
        ))
          conn.commit()
     except sqlite3.Error as e:
        print(f"Errore durante l'aggiunta dell'evento: {e}")
     finally:
        if conn:
            conn.close()

    #send tag note

    Send_pc_message=Button(frame3, command=add_PC_event, text="Send message")
    Send_pc_message.grid(column=0, row=5)

    def fetch_content():
     try:
        name=input_PC.cget('text')
        conn = sqlite3.connect(str(name)+'.db')
        c = conn.cursor()
        c.execute('SELECT * FROM name')
        events = c.fetchall()
        return events
     except sqlite3.Error as e:
        print(f"Errore durante la lettura degli eventi: {e}")
        return []
     finally:
        if conn:
            conn.close()

    def delete_events():
      try:
       name=input_PC.cget('text')
       conn = sqlite3.connect(str(name)+'.db')
       try:
        if type(int(entry_t.get()))==int:
         time=int(entry_t.get())  
         c = conn.cursor()
         c.execute('DELETE FROM name WHERE created_at < ?', (time,))
         conn.commit()
        else:
           print(type(entry_t.get()))
           entry_t.delete(0, END) 
       except ValueError as e:  
          print(f"Error value while deleting events: {e}")
      except sqlite3.Error  as e:
        print(f"Error while deleting events: {e}")
      finally:
        if conn:
            conn.close()

    def kind1_data_name():
        note=fetch_content()  
        events=[]
        for j in note:
            events.append(fake_rerender(j))
        return events
    
    def count_note(n:int):
       list_event=[]
       number_event=kind1_data_name()
       for numb_x in number_event:
         if numb_x["kind"]==n:
            list_event.append(numb_x)
       if n==1:     
        numb_lab.config(text=str(len(list_event)))
       else:
         if n==30023:
            numb_lab_2.config(text=str(len(list_event)))
    
    def return_note():
        if Checkbutton5.get() == 1:
         Nostr_note=kind1_data_name()
         if len(Nostr_note)>0:
          Text_t.delete("1.0","end")
          if entry_t.get()=="":
           for x in Nostr_note:
            Text_t.insert(END,"npub: "+str(x['pubkey'])+"\n"+"Time: "+str(x['created_at'])+"\n"+"Content: "+ x['content']+"\n")  
          else:
            for v in Nostr_note:
             if v['tags']!=[]:
              if v['tags'][1]==entry_t.get():
               Text_t.insert(END,"npub: "+str(v['pubkey'])+"\n"+"Time: "+str(v['created_at'])+"\n"+"Content: " +v['content']+"\n"
                             +"Tags:" +"\n"+ v['tags'][1]+"\n")       
             else:
                 None

    def return_Tags():
       if Checkbutton5.get() == 1:
         Nostr_note=kind1_data_name()
         if len(Nostr_note)>0:
          Text_t.delete("1.0","end")
          tags_one=[]
          if entry_t.get()=="":
           for x in Nostr_note:
             if x['tags']!=[]:
               if x['tags'][1] not in tags_one:
                tags_one.append(x['tags'][1])
           for z in tags_one:
                 Text_t.insert(END,"Tags: "+ z +"\n")  
          else:
            for v in Nostr_note:
             if v['tags']!=[]:
              if v['tags'][1]==entry_t.get():
               Text_t.insert(END,"npub: "+str(v['pubkey'])+"\n"+"Time: "+str(v['created_at'])+"\n"+"Content: " +v['content']+"\n"
                             +"Tags:" +"\n"+ v['tags'][1]+"\n")       
             else:
                 None

    receive_pc_message=Button(frame3, command=return_note, text="Return Note")
    receive_pc_message.grid(column=1, row=5,pady=2)   
    receive_pc_message=Button(frame3, command=return_Tags, text="Return Tags")
    receive_pc_message.grid(column=1, row=6,pady=2)              
    delete_pc_message=Button(frame3, command=delete_events, text="Delete Note")
    delete_pc_message.grid(column=0, row=6,pady=2)
    numb_message=Button(frame3, command=lambda:count_note(1), text="Number Note")
    numb_message.grid(column=0, row=7,pady=2) 
    numb_post=Button(frame3, command=lambda:count_note(30023), text="Number Post")
    numb_post.grid(column=1, row=7,pady=2) 
    numb_lab=Label(frame3,text="")
    numb_lab.grid(column=0,row=8)
    numb_lab_2=Label(frame3,text="")
    numb_lab_2.grid(column=1,row=8)
    numb_test=Label(frame4,text="",width=50,background="darkgrey")
    numb_test.grid(column=0, row=9,pady=2,columnspan=3,rowspan=2) 
    frame4.grid(column=0,row=9,columnspan=3,rowspan=2,sticky="n",pady=5)
    frame3.place(relx=0.01,rely=0.01)
    
    def delete_column(): 
     if Checkbutton5.get() == 0:
      frame3.destroy()
     else:
        print("Error "+" ") 

    button_delete=Button(frame3,command=delete_column,text="❌")  
    button_delete.grid(column=2,row=0)
    
    #new things 

    def create_button_1():
     frame_open_2=Frame(frame3,width=40,height=20, border=5)
     frame_box=Frame(frame_open_2,width=40,height=5, border=5) 
     
     Checkbutton_6 = IntVar() 
     Button_6 = Checkbutton(frame_box, text = "lock", 
                    variable = Checkbutton_6, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10)
     def six_event_1():
      if Checkbutton_6.get() == 1:
       if Checkbutton_time.get()==1:
        Nostr_note2=kind1_time_name() 
        if len(Nostr_note2)>0:
          Text_t2.delete("1.0","end")
          tags_one=[]
          if combo_to_do_list.get()=="Option Tag":
           for x in Nostr_note2:
             if x['tags']!=[]:
               if x['tags'][1] not in tags_one:
                tags_one.append(x['tags'][1])
           for z in tags_one:
                 Text_t2.insert(END,"Tags: "+ z +"\n")  
          else:
            for v in Nostr_note2:
             if v['tags']!=[]:
              if v['tags'][1]==combo_to_do_list.get():
               Text_t2.insert(END,"Tags: "+ v['tags'][1]+" Time: "+str(v['created_at'])+"\n"+"C: " +v['content']+"\n")       
             else:
                 None

       else:
         Nostr_note=kind1_data_name()
         if len(Nostr_note)>0:
          Text_t2.delete("1.0","end")
          tags_one=[]
          if combo_to_do_list.get()=="Option Tag":
           for x in Nostr_note:
             if x['tags']!=[]:
               if x['tags'][1] not in tags_one:
                tags_one.append(x['tags'][1])
           for z in tags_one:
                 Text_t2.insert(END,"Tags: "+ z +"\n")  
          else:
            for v in Nostr_note:
             if v['tags']!=[]:
              if v['tags'][1]==combo_to_do_list.get():
               Text_t2.insert(END,"Tags: "+ v['tags'][1]+" Time: "+str(v['created_at'])+"\n"+"C: " +v['content']+"\n")       
             else:
                 None
      else:
        Text_bar.delete("1.0","end") 
     def select_content():
      try:
       name=input_PC.cget('text')
       conn = sqlite3.connect(str(name)+'.db')
       c = conn.cursor()
       if Checkbutton_time.get()==1:
        time=since_day(int(since_entry.get()))  
        #print(time)
        c.execute('SELECT * FROM Name Where created_at > ?', (time,))
        events = c.fetchall()
        return events
      except sqlite3.Error as e:
        print(f"Errore durante la lettura degli eventi: {e}")
        
      finally:
        if conn:
            conn.close()  
     def kind1_time_name():
        note=select_content() 
        if note!=None: 
         events=[]
         for j in note:
            events.append(fake_rerender(j))
         return events   
     
     def select_tag(event):
          Text_t2.delete("1.0", "end")
        
     input_6 = Button(frame_box, text = "Read Note", 
                    command =six_event_1, 
                    height = 2, 
                    width = 10)
     input_6.grid(column=0, row=0)
     Button_6.grid(column=1, row=0)
     combo_to_do_list = ttk.Combobox(frame_open_2, values=["To do","Wish list", "Done", "To complete" ],font=button_font,width=10 )
     combo_to_do_list.grid(column=0, row=1)
     combo_to_do_list.set("Option Tag")
     combo_to_do_list.bind("<<ComboboxSelected>>",select_tag)
     since_variable=IntVar(value=1)
     since_entry=Entry(frame_box,textvariable=since_variable,font=("Arial",12,"normal"),width=4)
     since_entry.grid(column=4,row=0,ipadx=1)
     Checkbutton_time = IntVar() 
     Button_time = Checkbutton(frame_box, text = "Since", 
                    variable = Checkbutton_time, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10)
     Button_time.grid(column=3,row=0)
     Text_t2=Text(frame_open_2, width=40,height=10,wrap="word",undo=True)
     Text_t2.grid(column=0, row=2, columnspan=2)
     frame_box.grid(pady=2)
     frame_open_2.grid(column=0,row=0,rowspan=2,padx= 5,pady=5)
     def Clicked(event):
        if Checkbutton_6.get() == 0:
         frame_open_2.grid(column=4,row=4,rowspan=2,padx= 5,pady=5)
     frame_open_2.bind("<Button-1>" ,Clicked)
    
     def Clicked2(event):
        if Checkbutton_6.get() == 0:
         frame_open_2.grid(column=5,row=1,rowspan=2,padx= 5,pady=5)
     frame_open_2.bind("<Button-3>" ,Clicked2)
     def Clicked3(event):
        if Checkbutton_6.get() == 0:
         frame_open_2.grid(column=5,row=4,rowspan=2,padx= 5,pady=5)
     frame_open_2.bind("<Double-Button-3>" ,Clicked3)  

     def delete_column_1(): 
      if Checkbutton_6.get() == 0:
       frame_open_2.destroy()
      else:
         messagebox.showerror("showerror", "Error") 

     button_delete1=Button(frame_box,command=delete_column_1,text="❌")  
     button_delete1.grid(column=2,row=0)
     
    button_open2=Button(frame4,command=create_button_1,text="New Tab button")
    button_open2.grid(column=0, row=0,pady=5,padx=2) 

    button_open3=Button(frame4, command=create_button_test, text= "New Send tab")
    button_open3.grid(column=1, row=0,pady=5,padx=2,columnspan=2) 

y=1
x=4

def create_button_test():
    frame_open=Frame(root,width=70,height=60, border=5)
    def select(event):
        stringa.set(combo_tag_note.get())
        label_note.config(text=combo_tag_note.get())
            
    frame_box=Frame(frame_open,width=40,height=10,background="darkgrey") 
    
    stringa=StringVar()
    tag_note=Entry(frame_box,textvariable=stringa)
    tag_note.grid(column=1,row=0,columnspan=1)
    combo_tag_note= ttk.Combobox(frame_box, values=["To do","Wish list", "Done", "To complete" ],font=button_font, width=15)
    combo_tag_note.grid(column=1,row=0,columnspan=1)
    combo_tag_note.bind("<<ComboboxSelected>>",select)
    tag_note_text=Label(frame_box,text="Tag :")
    tag_note_text.grid(column=0,row=0)
    label_id = Label(frame_box,text="Send a note with tag", width=20, relief=RAISED,font=("Arial",12,"normal"))
    label_id.grid(pady=5,padx=2,row=1,column=0, columnspan=3)
    scroll_bar_mini = tk.Scrollbar(frame_box)
    text_note2=Text(frame_box,height=10,width=30, yscrollcommand = scroll_bar_mini.set,font=("Arial",12,"normal"))
    text_note2.grid(row=2, rowspan=2,columnspan=2)
    scroll_bar_mini.config( command = text_note2.yview )
    scroll_bar_mini.grid( row=2,column=2,rowspan=2,padx=2,sticky="n",pady=5,ipady=65)    
    label_note=Label(frame_box,text= "test", font=("Arial",12,"normal"))
    label_note.grid(row=4,column=1,pady=2)
    
    def add_tag_event_1():
     try:
        conn = sqlite3.connect('Pcenter.db')
        c = conn.cursor()
        value=uuid.uuid4()
        event={
    "id": str(value),
    "pubkey": test_hash(value.int),
    "created_at": int(time.time()),  # timestamp corrente
    "kind": 1,
    "tags": ["hashtag",str(tag_note.get())],
    "content": text_note2.get(1.0, "end-1c"),
    "sig":str(value)+str(test_hash(value.int))}
        
        if event["content"]!="":
          
          if event["tags"][1]!="":
           c.execute('''
        INSERT INTO name (id, pubkey, created_at, kind, tags, content, sig)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            event["id"],
            event["pubkey"],
            event["created_at"],
            event["kind"],
            json.dumps(event["tags"]),
            event["content"],
            event["sig"]
        ))
           conn.commit()
           messagebox.showinfo("showinfo", "Send event") 
           text_note2.delete("1.0", "end")
     except sqlite3.Error as e:
        print(f"Errore durante l'aggiunta dell'evento: {e}")
     finally:
        if conn:
            conn.close()
    button_note=Button(frame_box,text= "send tag note", command=add_tag_event_1)
    button_note.grid(row=4,column=0,pady=2, padx=3)        
    frame_box.grid(column=4,row=0,columnspan=3,rowspan=5)
    frame_open.place(relx=0.01,rely=0.01)

    def delete_create_note(): 
       frame_open.destroy()
    
    button_delete1=Button(frame_box,command=delete_create_note,text="❌", fg="red")  
    button_delete1.grid(column=2,row=0)   
 
def since_day(number):
    import datetime
    import calendar
    date = datetime.date.today() - datetime.timedelta(days=number)
    t = datetime.datetime.combine(date, datetime.time(1, 2, 1))
    z=calendar.timegm(t.timetuple())
    #print(z)
    return z   

def OpenColumn3():
    frame6=Frame(root,width=30,height=15, background="lightgrey")    
    frame7=Frame(frame6,width=25,height=4, background="darkgrey")   
    frame8=Frame(frame6,width=25,height=2,background="lightgrey")  
    Checkbutton8 = IntVar() 
    Button8 = Checkbutton(frame7, text = "lock",  variable = Checkbutton8, onvalue = 1, offvalue = 0, font=button_font)
    
    def eight_event():
     if Checkbutton8.get() == 1:
          print( "Check bar:PC ") 
     else:
        pass
        
    input_8 = Button(frame7, text =str("Size"), command =eight_event,font=button_font)
    input_8.grid(column=1, row=0,ipadx=2,ipady=2)
    Button8.grid(column=0, row=0,ipadx=2,ipady=2)
    
    def get_i_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
       Text_t3.insert(sel_end,"*")
       Text_t3.insert(sel_start,"*")

       
       #Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e)  
    
    def get_u_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
       Text_t3.insert(sel_end,"</u>")
       Text_t3.insert(sel_start," <u>")

       
       #Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e)  
    
    button_type=Button(frame7, text = "<i>", command = get_i_text,font=button_font)
    button_type.grid(column=4, row=0,ipadx=2,ipady=2)
    button_down4=Button(frame7, text = "<u>", command =get_u_text,font=button_font)
    button_down4.grid(column=4, row=1,ipadx=2,ipady=2)

    #General Character Bold
    def Update_B():
     if font_font.actual()['weight']=="bold":
      font_font.config(weight="normal")  
     else:
      font_font.config(weight="bold")    
    
    #Selected Character Bold

    def get_bold_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
       Text_t3.insert(sel_end,"**")
       Text_t3.insert(sel_start,"**")
      
       #Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e)  

    def get_quote_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       Text_t3.insert(sel_end," ")
       Text_t3.insert(sel_start,"\n"+str(">"))
       
       #Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e)      

    button_type1=Button(frame7, text = "B", command =get_bold_text)
    button_type1.grid(column=0, row=5,ipadx=2,ipady=2)
    button_down3=Button(frame7, text = "Quote", command =get_quote_text)
    button_down3.grid(column=1, row=5,ipadx=2,ipady=2)
   
    def get_selected_text():
     try:
      sel_start, sel_end = Text_t3.tag_ranges("sel")
      result_label = tk.Label(Text_t3, text="")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       result_label.config(text="Selected Text: " + selected_text)
       result_label.grid()
      else:
       result_label.config(text="No text selected.")
       result_label.grid()
     except ValueError as e:
        None #print(e)  

    def get_selected_text():
     try:
      Text_t3.tag_configure("warning", background="red", foreground="blue")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
       #Text_t3.insert("1.0",selected_text)
       Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e)  

    def get_code_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
       if len(selected_text)<15:
         Text_t3.insert(sel_end,"`")
         Text_t3.insert(sel_start,"`")
       else:
           Text_t3.insert(sel_end,"``")
           Text_t3.insert(sel_start,"``")
      
      else:
         print("no") 
     except ValueError as e:
        print(e)  
    
    button_type2=Button(frame7, text = "Get", command = get_selected_text)
    button_type2.grid(column=4, row=2,ipadx=2,ipady=2)
    button_down2=Button(frame7, text = "Code", command =get_code_text)
    button_down2.grid(column=3, row=2,ipadx=2,ipady=2)

    def get_headings_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
       
       Text_t3.insert(sel_start,"## ")
      
       #Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e) 

    def get_headings_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
            
      if button_type3.cget('text')in combo_box['values']:
         i=0
         string=""
         while i<len(combo_box['values']):
            string=string+"#"
            if button_type3.cget('text')== combo_box['values'][i]:
               Text_t3.insert(sel_start,"\n"+str(string)+ str(" "))
               break
            else:
             i=i+1
       #  Text_t3.insert(sel_start,str(string)+ str(" "))
       #Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e)     

    button_type3=Button(frame7, text = "H",command =get_headings_text)
    button_type3.grid(column=0, row=1,ipadx=2,ipady=2)

    def on_select(event):
     selected_item = combo_box.get()
     button_type3['text']=selected_item

    #label = tk.Label(frame6, text="Item: ")
    #label.grid(column=3, row=2)
    combo_box = ttk.Combobox(frame7, values=["H1","H2","H3","H4","H5"])
    combo_box.grid(column=1, row=1,ipadx=2,ipady=2)
    combo_box.set("H1")
    combo_box.bind("<<ComboboxSelected>>", on_select)
    #text_var3 = StringVar()
    #entry_t3= Entry(frame6, textvariable=text_var3,width=50)
    #entry_t3.grid(column=0, row=1, columnspan=4)
    font_font = tkFont.Font(family="sans-serif", size=12, weight="normal")

    def increase_font_size():
     font_font.config(size=min(20,font_font.actual()['size'] + 2))
     input_8["text"]=str(font_font.actual()['size'])
     root.update()
    
    def decrease_font_size():
     font_font.config(size=max(8, font_font.actual()['size'] - 2)) 
     input_8["text"]=str(font_font.actual()['size'])
     root.update()

    def increase_font():
     Text_t3.configure(font=("sans-serif", 14, "normal"))
    
    
    def decrease_font():
     Text_t3.configure(font=("sans-serif", 10, "normal")) 
     
      # Ensure font 
    button_input=Button(frame7, text = "+",command =increase_font_size,font=button_font)
    button_input.grid(column=2, row=0,ipadx=2,ipady=2)
    button_input1=Button(frame7, text = "-",  
                    command =decrease_font_size,font=button_font)
    button_input1.grid(column=2, row=1,ipadx=2,ipady=2) 
   
    def get_link_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
       Text_t3.insert(sel_end,"(url)")
       Text_t3.insert(sel_start,"[text]")
       
       
       #Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e)  

    def get_image_text():
     try:
      Text_t3.tag_configure("warning")
      sel_start,sel_end=Text_t3.tag_ranges("sel")
      if sel_start and sel_end:
       selected_text = Text_t3.get(sel_start, sel_end)
       #print(sel_start, sel_end)
       Text_t3.insert(sel_end,"(url image)")
       Text_t3.insert(sel_start,"![text image]")
       
       
       #Text_t3.tag_add("warning",sel_start, sel_end)    
       #Text_t3.grid()
      else:
         print("no") 
     except ValueError as e:
        print(e)      
    
    button_input2=Button(frame7, text = "Link", command =get_link_text,font=button_font)
    button_input2.grid(column=3, row=1,ipadx=2,ipady=2)
    button_input3=Button(frame7, text = "Image",command =get_image_text,font=button_font)
    button_input3.grid(column=3, row=0,ipadx=2,ipady=2)

    label_scroll=tk.Scrollbar(frame6, width=10)
    Text_t3=Text(frame6, wrap=WORD,undo=True,font=font_font, background="darkgrey",width=100,yscrollcommand = label_scroll.set)
    Text_t3.place(relx=0.2,rely=0.55,relheight=0.4,relwidth=0.6 )
    
    label_scroll.place(relx=0.85,rely=0.55, relheight=0.4,relwidth=0.05 )
    label_scroll.config( command = Text_t3.yview )
    frame7.pack(side="top",padx=1)
    text_var = StringVar()
    entry_1= Entry(frame7, textvariable=text_var)
    entry_1.grid(column=1, row=2,ipadx=2,ipady=2)
    tag_var = StringVar()
    entry_2= Entry(frame8, textvariable=tag_var, font=font_font)
    entry_2.grid(column=1, row=3,ipadx=2,ipady=2,columnspan=3)

    def delete_option():
       entry_1.delete(0, END)

    delete_send_3=Button(frame7, text = "Del Text",command=delete_option)
    delete_send_3.grid(column=2, row=2,ipadx=2,ipady=2)

    #save in md
    import io
    from tkinter.filedialog import asksaveasfilename
      
    def SaveFile(): 
     try:
       files = [('All Files', '*.*'),  
             ('Markdown', '*.md'), 
             ('Text Document', '*.txt')] 
       file = asksaveasfilename(filetypes = files, defaultextension = files) 
       fob=open(file,'w',encoding='utf-8')
       fob.write(Text_t3.get(1.0, "end-1c"))
       fob.close()
       if entry_1.get()!="":
        entry_1.delete(0, END)  
        if Text_t3.get(1.0, "end-1c")=="":
          entry_1.insert(0,"Saved: "+ "ok"+" No line")
        else:
          if Text_t3.get(1.0, "end-1c")=="":
           entry_1.insert(0,"Saved: "+ "ok"+" No line")
          else:
           entry_1.insert(0,"Saved: "+ "ok") 
       else:
        entry_1.insert(0,"Saved: "+ "ok")   
     except FileNotFoundError as e:
       if entry_1.get()!="":
        entry_1.delete(0, END)  
        entry_1.insert(0,"Error: "+str(e))
       else:
          entry_1.insert(0,"Error: "+str(e))
        
    def Save_in_DB():
      
     try:
        conn = sqlite3.connect('Pcenter.db')
        c = conn.cursor()
        value=uuid.uuid4()
        if entry_2.get()!="":
          hash_tag=entry_2.get()
        else:
          hash_tag="Week Update"  
        event={
    "id": str(value),
    "pubkey": test_hash(value.int),
    "created_at": int(time.time()),  # timestamp corrente
    "kind": 30023,
    "tags": ["hashtag",hash_tag],
    "content": Text_t3.get(1.0, "end-1c"),
    "sig":str(value)+str(test_hash(value.int))}
        if event["content"]!="":
          if event["tags"][1]!="":
           c.execute('''
        INSERT INTO name (id, pubkey, created_at, kind, tags, content, sig)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            event["id"],
            event["pubkey"],
            event["created_at"],
            event["kind"],
            json.dumps(event["tags"]),
            event["content"],
            event["sig"]
        ))
          conn.commit()
        else:
           entry_1.insert(0," No text")  
     except sqlite3.Error as e:
        print(f"Errore durante l'aggiunta dell'evento: {e}")
     finally:
        if conn:
            conn.close()
    
    def fetch_article():
     try:
        conn = sqlite3.connect('Pcenter.db')
        c = conn.cursor()
        c.execute('SELECT * FROM name where kind= ?', (30023,))
        events = c.fetchall()
        return events
     except sqlite3.Error as e:
        print(f"Errore durante la lettura degli eventi: {e}")
        return []
     finally:
        if conn:
            conn.close()
    def kind30023_data_name():
        note=fetch_article()  
        events=[]
        for j in note:
            events.append(fake_rerender(j))
        return events      

    def read_long_form():
        if Checkbutton8.get() == 1:
         articles=kind30023_data_name()
         if len(articles)>0:
           if entry_1.get()!="":
             entry_1.delete(0, END)
             entry_1.insert(0,"Read: "+ "the article")
           else:
                entry_1.insert(0,"Read: "+ "the article")
           if Text_t3.get(1.0, "end-1c")=="":
               Text_t3.insert(END,articles[::-1][0]['content'])
           else:
                Text_t3.delete("1.0","end")
                Text_t3.insert(END,articles[::-1][0]['content'])
           if entry_2.get()!="":
             entry_2.delete(0, END)
             entry_2.insert(0,str(articles[::-1][0]['tags'][1]))  
           else:
             entry_2.insert(0,str(articles[::-1][0]['tags'][1]))     
                    
         else:
              if entry_1.get()!="":
                    entry_1.delete(0, END)
                    entry_1.insert(0,"No article")
              else:
                    entry_1.insert(0,"No article")
        else:
             if entry_1.get()!="":
                    entry_1.delete(0, END)
                    entry_1.insert(0,"lock button: ")
             else:
                    entry_1.insert(0,"lock button: ")

    def del_text():
      Text_t3.delete("1.0", "end")
                
    button_send_3=Button(frame7, text = "Save ✔",command=SaveFile)
    button_send_3.grid(column=1, row=4,ipadx=2,ipady=2)
    button_send_4=Button(frame7, text = "Save DB",command=Save_in_DB)
    button_send_4.grid(column=2, row=4,ipadx=2,ipady=2)
    button_send_5=Button(frame7, text = "Last Post",command=read_long_form)
    button_send_5.grid(column=3, row=4,ipadx=2,ipady=2)
    button_send_6=Button(frame7, text = "Delete",command=del_text)
    button_send_6.grid(column=4, row=4,ipadx=2,ipady=2)
    tag_text=Label(frame7,text="Text :")
    tag_text.grid(column=0,row=2,ipadx=2,ipady=2)
    tag_text_2=Label(frame8,text="Tag :")
    tag_text_2.grid(column=0,row=3,ipadx=2,ipady=2,pady=2)
       
    frame8.pack(side="top",padx=1,pady=5)
    frame6.pack(side="right",padx=2,fill="both", expand=0.5)
    
    def delete_column_3(): 
     if Checkbutton8.get() == 0:
      frame6.pack_forget()
     else:
        print("Error "+" ")

    button_delete3=Button(frame7,command=delete_column_3,text= "Close❌")  
    button_delete3.grid(column=0,row=4,ipadx=2,ipady=2)
   
frame2=Frame(root,width=20,height=1)
menu = Menu(frame2)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Create Note", command=OpenColumn)
filemenu.add_command(label="Create Post", command=OpenColumn3)
filemenu.add_separator()
filemenu.add_command(label="New Send tab",command=create_button_test)
Test=Menu(frame2)
File2Menu=Menu(frame2)
text_variable = StringVar()

def report_fake(event):
     id = event[0]
     sig= event[6]
     kind=event[3]
     npub=event[1]
     created_at=event[2]
     tags=json.loads(event[4])
     content=event[5]
     return id,kind,created_at,npub,tags,content,sig

def fake_rerender(event):
    a,b,c,d,e,f,g=report_fake(event)
    l={"id":a,"kind":b,"created_at":c,"pubkey":d,"tags":e,"content":f,"sig":g}
    return l

fg_color=""

def Notebook_():
 notebook = ttk.Notebook(root)
 notebook.place(relx=0.4,rely=0.1,relheight=0.395)

 # create frames
 frame1 = Frame(notebook, width=370, height=280)
 import random

 def palette():
     if Check_1.get()==1:
         Check_1.set(0)
         number=random.randint(0,8)
         root.config(bg=color_list[number])
     else:
        Check_1.set(1)
        root.config(bg="grey")

 def palette_fg():
       if Check_0.get()==1:
        Check_0.set(0)
        number=random.randint(0,8)
        for widget in root.winfo_children():  
         if isinstance(widget, tk.Button):  
            
            widget["foreground"] = color_list[number]
      
       else:
          Check_0.set(1)
          for widget in root.winfo_children():  
           if isinstance(widget, tk.Button):  
            widget["foreground"] = "black"
          
 Frame_block=Frame(frame1)
 Check_0 = IntVar()
 Check_0.set(1)
 Check_1= IntVar()
 Check_1.set(1)

 def slide_r1():    
                    font_font.config(size=min(14,font_font.actual()['size'] -1+ int(menu_slider1.get()/25)))
                    
 menu_slider1=Scale(Frame_block,orient=HORIZONTAL)
 menu_slider1.grid(column=0, row=0) 
 button_slider1=Button(Frame_block,command=slide_r1, text="zoom", font=button_font)
 button_slider1.grid(column=0,row=3,padx=3)                   
 entry_A= Label(Frame_block, text="A",width=10,font=font_font)
 entry_A.grid(column=0, row=1,rowspan=2)
 button_palette=Button(Frame_block,text="BG palette",command=palette,font=button_font)
 button_palette.grid(column=2,row=2,padx=5,pady=5)
 button_col_palette=tk.Button(Frame_block,text="FG button",command=palette_fg,font=button_font)
 button_col_palette.grid(column=3,row=2,padx=5,pady=5)
 button_input=Button(Frame_block, text = "+",width=6,command =increase_font_size,font=("Roboto Mono", 12,"bold"))
 button_input.grid(column=2, row=4,ipadx=2,ipady=2)
 button_input1=Button(Frame_block, text = "-", width=6, command =decrease_font_size,font=("Roboto Mono", 12,"bold"))
 button_input1.grid(column=3, row=4,ipadx=2,ipady=2) 
  
 def close_n():
    notebook.place_forget()
    button_close.place_forget()
 
 button_close=Button(Frame_block,text="Close",command=close_n, border=1,highlightbackground="white")
 button_close.grid(row=0, column=3) 
 Frame_block.pack(pady=5)
 frame1.place(relx=0.01,rely=0.01)
 notebook.add(frame1, text='General Settings')
   
color_list=["red","blue","grey","darkgrey","black","white","yellow","green"]     
button_fg_color=StringVar()
fg_color=str(color_list[2])
button_font=tkFont.Font(family="Roboto Mono", size=12, weight="bold")   
font_font = tkFont.Font(family="Roboto Mono", size=12, weight="normal")

entry_font=tkFont.Font(family="sans-serif", size=10, weight="normal")
label_font=tkFont.Font(family="sans-serif", size=10, weight="normal")

def increase_font_size():
     font_font.config(size=min(14,font_font.actual()['size'] + 2))
     button_font.config(size=min(14,font_font.actual()['size'] + 2))
     label_font.config(size=min(14,font_font.actual()['size'] + 2))
     entry_font.config(size=min(14,font_font.actual()['size'] + 2))

    
def decrease_font_size():
     font_font.config(size=max(8, font_font.actual()['size'] - 2))
     button_font.config(size=max(8, font_font.actual()['size'] - 2))  
     label_font.config(size=max(8, font_font.actual()['size'] - 2))
     entry_font.config(size=max(8, font_font.actual()['size'] - 2))

frame_2=Frame(root,width=20,height=1)
filemenu.add_command(label="Settings", command=Notebook_)
filemenu.add_command(label="Exit", command=frame3.quit)
frame1 = ttk.Frame(root, width=200, height=280)

#test database
frame2.pack()


root.mainloop()