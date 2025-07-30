from tkinter import *
import sqlite3
import json
import tkinter as tk
import time
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox 
import asyncio
from nostr_sdk import *
import json
from datetime import timedelta
import random

root = Tk() 
root.geometry("1250x800")
root.title("Event test") 
fg_color=""

def delete_events(id_event):
      try:
       name="historyc"
       conn = sqlite3.connect(str(name)+'.db')
       try:
         if isinstance(id_event,str):
          id=id_event
         else:
            print(f"Error this is a {type(id_event)}")
                  
         c = conn.cursor()
         c.execute('DELETE FROM event WHERE id = ?', (id,))
         conn.commit()
       
       except ValueError as e:  
          print(f"Error value while deleting events: {e}")
      except sqlite3.Error  as e:
        print(f"Error while deleting events: {e}")
      finally:
        if conn:
            conn.close()

def Notebook_():
 notebook = ttk.Notebook(root)
 notebook.place(relx=0.6,rely=0.01,relheight=0.375)

 frame1 = ttk.Frame(notebook, width=370, height=280)
 frame2 = ttk.Frame(notebook, width=370, height=280)
 frame_3 = ttk.Frame(notebook, width=370, height=280)
 frame_4 = ttk.Frame(notebook, width=370, height=280)
 frame_5= ttk.Frame(notebook, width=370, height=280)
 frame_6= ttk.Frame(notebook, width=370, height=280)
 
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
 Frame_block.pack(pady=5)
 frame1.pack(fill='both', expand=True)
 note=kind1_data_name_g()
 list_note_zer0=[]
 for note_x in note:
    if note_x["tags"]["kind"]==0:
      list_note_zer0.append(note_x["tags"]) 
 i=0
 treeview = ttk.Treeview(frame2, columns=("Value"),height=8)
 
 treeview.heading("#0", text="key")
 treeview.heading("Value", text="Value")
 while i<len(list_note_zer0):
  if "name" in list(json.loads(list_note_zer0[i]["content"]).keys()):
   name_account=json.loads(list_note_zer0[i]["content"])["name"]
   level1 = treeview.insert("", tk.END, text=f"{name_account}")
   content=json.loads(list_note_zer0[i]["content"])
   for key,value in content.items():
    if value!="":
     treeview.insert(level1, tk.END,text=str(key),values=f"{value}")
   treeview.insert(level1, tk.END,text=" \n",values="\n") 
  i=i+1
 v_scrollbar = Scrollbar(frame2, orient=VERTICAL, command=treeview.yview)
 treeview.configure(yscrollcommand=v_scrollbar.set)
 v_scrollbar.grid(column=2,row=0,rowspan=3,ipady=60)  
 treeview.grid(column=0,columnspan=2,row=0,rowspan=3,pady=10,padx=15)
 frame2.pack(fill='both', expand=True)
 
 notebook.add(frame1, text='General Information')
 notebook.add(frame2, text='Profile',padding=20)
 
 #-------------------3---------------------------
 
 number_pubkey={}
 list_publickey_=[]
 list_relay_t=[]
 list_relay_tag=[]
 
 def select_relay(event):
   
   if combo_relay.get()[0:6]=="wss://" and combo_relay.get()[-1]=="/" and combo_relay.get() not in relay_list:
    relay_list.append(combo_relay.get())
    if len(relay_list)<=8:
     text_lab["text"]=str("new relay add ---"+combo_relay.get()+" ---\n lenght list relay list"+ str(len(relay_list))+"\n")
     test_relay=""
     for relay_z in relay_list:
      test_relay = test_relay +relay_z +"\n"
     text_relay["text"]=str(test_relay)
    else:
       text_lab["text"]=str("There are 8 Relays in this list")     
 for note_x in note:
    if note_x["tags"]["pubkey"] not in list_publickey_:
      list_publickey_.append(note_x["tags"]["pubkey"]) 
    if note_x["tags"]["kind"] in [10002,10050,10012,30002]:
       if note_x["tags"] not in list_relay_t:
          list_relay_t.append(note_x["tags"])
 for relay_note in list_relay_t:         
     if tags_string(relay_note,"r")!=[]:
        for relay_x in tags_string(relay_note,"r"):
           if relay_x not in list_relay_tag:
            list_relay_tag.append(relay_x)
     if tags_string(relay_note,"relay")!=[]:   
        for relay_y in tags_string(relay_note,"relay"):   
          if relay_y not in list_relay_tag:
            list_relay_tag.append(relay_y)
 
 text_lab=Label(frame_3,text="",font=entry_font)
 text_lab.grid(column=0,row=2,columnspan=3)
 text_relay=Label(frame_3,text="",font=entry_font)
 text_relay.grid(column=0,row=3,columnspan=3)
 text_number=Label(frame_3,text="Add Relay to List",font=entry_font)
 text_number.grid(column=3,row=1,columnspan=3,padx=10)   
 combo_relay = ttk.Combobox(frame_3, values=list_relay_tag,font=entry_font,width=25)
 combo_relay.grid(column=0,row=1,pady=1,padx=10)
 combo_relay.set("Relay list")
 combo_relay.bind("<<ComboboxSelected>>", select_relay)
 
 for pub_key_x in list_publickey_ :
     t=int(0) 
     for note_y in note:
        if note_y["tags"]["pubkey"]== pub_key_x :
           t=t+1
     number_pubkey[pub_key_x]=int(t)
 notebook.add(frame_3, text='Relays list',padding=20)
 
#----------------4-----------------------------

 treeview_4 = ttk.Treeview(frame_4, columns=("Value"))
 treeview_4.heading("#0", text="key")
 treeview_4.heading("Value", text="Value")
 level3 = treeview_4.insert("", tk.END, text="Profiles")
 note_pubikey_0={}
 for list_x in list_publickey_:
    for test_x in list_note_zer0:
       if list_x== test_x["pubkey"]:
          if list_x not in  list(note_pubikey_0.keys()): 
           note_pubikey_0[list_x]=json.loads(test_x["content"])
 for key,value in note_pubikey_0.items():
    if "name" in list(value.keys()): 
     value_name=value["name"]
     key_value=key[0:18]
     value_pubkey=str(number_pubkey[key])
     treeview_4.insert(level3, tk.END,text=str(key_value),values=f"{value_name},{value_pubkey}")
    
 v_scrollbar3 = ttk.Scrollbar(frame_4, orient=VERTICAL, command=treeview_4.yview)
 treeview_4.configure(yscrollcommand=v_scrollbar3.set,height=8)
 v_scrollbar3.grid(column=3,row=0,pady=10,ipady=40) 
 treeview_4.grid(column=0,columnspan=3,row=0,pady=10,padx=10)
 frame_4.pack(fill='both', expand=True)    
 notebook.add(frame_4, text="Other Profile", padding=20)

 #-----------------5----------------------------------

 def select(event):
    select_name=combo_name.get()
    list_note_select=[]
    for note_name in kind_0:
     if "name" in list(note_name.keys()):
      if note_name["name"]==select_name:
       try: 
        for test_0 in list_note_zer0:
           if json.loads(test_0["content"])==note_name:
            select_pubkey=str(test_0["pubkey"])
       except KeyError as e:
          print(note_name, "\n ", e) 
    for note_y in note:
        if note_y["tags"]["pubkey"]== select_pubkey :    
          list_note_select.append(note_y)
    print(select_pubkey, "name ", select_name )      
    event1,event2=event_number(list_note_select) 
    test_nota=""
    selection_note_dict.clear()
    for event_x, event_y in zip(event1,event2):
       selection_note_dict[event_x]=event_y
       
       test_event="kind "+str(event_x)+ " number of event "+str(len(event_y))+str("\n")
       test_nota=test_nota+test_event+"\n"    
    combo_note["values"]=list(selection_note_dict.keys())   
    note_lab.delete("1.0","end")
    note_lab.insert(END,test_nota)

 kind_0=list(note_pubikey_0.values())
 list_name=[]
 for note_name in kind_0:
   if "name" in list(note_name.keys()):
    if note_name["name"] not in list_name:
       list_name.append(note_name["name"])

 def selection_note(event):
   try: 
    note_lab_2.delete("1.0","end")
    s0=1
    list_note=list(selection_note_dict[int(combo_note.get())])
    for test_x in list_note:
     note_lab_2.insert(END,"note n " +str(s0)+"\n"+  "pubkey: "+str(test_x['pubkey'])+"\n"+"id: "+str(test_x['id'])+"\n"+"Time: "+str(test_x['created_at'])+"\n"+"Content: "+ test_x['content']+"\n"+"\n")       
     s0=s0+1 
   except KeyError as e:
    print(selection_note_dict,"\n", e)     

 combo_name = ttk.Combobox(frame_5, values=list_name,font=entry_font,width=20)
 combo_name.grid(row=0,column=1,columnspan=2)
 combo_name.set("Cluster")
 combo_name.bind("<<ComboboxSelected>>", select)
 note_lab=Text(frame_5,width=30,heigh=13)
 note_lab.grid(column=0,row=1,columnspan=3,pady=2,padx=4)
 selection_note_dict={}
 combo_note = ttk.Combobox(frame_5, font=entry_font,width=20)
 combo_note.grid(row=0,column=3,columnspan=2)
 combo_note.set("Kind Events")
 combo_note.bind("<<ComboboxSelected>>", selection_note)
 note_lab_2=Text(frame_5,width=30,heigh=13)
 note_lab_2.grid(column=3,row=1,columnspan=3,pady=2,padx=4,)
 frame_5.pack(fill='both', expand=True)
 notebook.add(frame_5, text="Name List" )
 
 #---------------6------------------------

 def deletetion_note(event):
    select_name=combo_n.get()
    list_note_select=[]
    for note_name in kind_0:
     if note_name["name"]==select_name:
       try: 
        for test_0 in list_note_zer0:
           if json.loads(test_0["content"])==note_name:
            select_pubkey=str(test_0["pubkey"])
       except KeyError as e:
          print(note_name, "\n ", e) 
    for note_y in note:
        if note_y["tags"]["pubkey"]== select_pubkey :    
          list_note_select.append(note_y)
    if messagebox.askyesno("whant to cancel \n this events","Yes, No")==True:      
      print(select_pubkey, "name ", select_name )      
      for list_note in list_note_select:
          delete_events(list_note["tags"]["id"])

 combo_n = ttk.Combobox(frame_6, values=list_name,font=entry_font,width=20)
 combo_n.grid(row=0,column=1,columnspan=2,pady=5,padx=5)
 combo_n.bind("<<ComboboxSelected>>", deletetion_note)
 frame_6.pack(fill='both', expand=True)
 notebook.add(frame_6, text="Delete note" )

 def close_n():
    notebook.place_forget()
    button_close.place_forget()
 
 button_close=Button(root,text="x Close",command=close_n, border=1,highlightbackground="white",background="#e6e9ea")
 button_close.place(relx=0.94,rely=0.011,relheight=0.029)

block_npub=[]
color_list=["#F1E7E7","#302BBD","#F8FAFC","darkgrey","#5450B3","white","#6C6B8C","#D4F6FF","#3732C2"]     
button_fg_color=StringVar()
fg_color=str(color_list[2])
button_font=tkFont.Font(family="Roboto Mono", size=12, weight="bold")   
font_font = tkFont.Font(family="Roboto Mono", size=12, weight="normal")
entry_font=tkFont.Font(family="sans-serif", size=10, weight="normal")
label_font=tkFont.Font(family="sans-serif", size=10, weight="normal")

def increase_font_size():
     font_font.config(size=min(14,font_font.actual()['size'] + 1))
     button_font.config(size=min(14,font_font.actual()['size'] + 1))
     label_font.config(size=min(14,font_font.actual()['size'] + 1))
     entry_font.config(size=min(10,font_font.actual()['size'] + 1))
     #print(font_font.cget("size"))
    
def decrease_font_size():
     font_font.config(size=max(8, font_font.actual()['size'] - 1))
     button_font.config(size=max(8, font_font.actual()['size'] - 1))  
     label_font.config(size=max(8, font_font.actual()['size'] - 1))
     entry_font.config(size=max(8, font_font.actual()['size'] - 1))
     #print(font_font.cget("size"))

def OpenColumn():
    text_var = StringVar()
    frame3=Frame(root,width=70,height=70, border=5,background="lightgrey")  
    Checkbutton5 = IntVar() 
    frame3.config(background="lightgrey")
    Button5 = Checkbutton(frame3, text = "🔒", variable = Checkbutton5,  onvalue = 1, offvalue = 0, height = 2, width = 10)

    def five_event():
     if Checkbutton5.get() == 1:
          initialize_data_name()
     else:
        pass

    input_PC = Button(frame3, text = "historyc", command =five_event, height = 2, width = 10)
    input_PC.grid(column=0, row=0)
    Button5.grid(column=1, row=0)
    entry_t= Entry(frame3, textvariable=text_var,width=60)
    entry_t.grid(column=0,row=1, columnspan=2)
    scroll_bar_mini = tk.Scrollbar(frame3)
    
    Text_t=Text(frame3, width=45,height=30,wrap="word",undo=True,yscrollcommand = scroll_bar_mini.set)
    scroll_bar_mini.config( command = Text_t.yview )
    scroll_bar_mini.grid( sticky = NS,column=2,row=2,rowspan=3,pady=5)
    Text_t.grid(column=0, row=2, columnspan=2,rowspan=3)
    
    def initialize_data_name():
     try:
        name=input_PC.cget('text')
        conn = sqlite3.connect(str(name)+'.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS event (
            id TEXT PRIMARY KEY,
            tags TEXT)
        ''') 
        conn.commit()
     except sqlite3.Error as e:
        print(f"Error during the initialization of the database: {e}")
     finally:
        if conn:
            conn.close()

    def add_PC_event(event_):
     try:
        name=input_PC.cget('text')
        conn = sqlite3.connect(str(name)+'.db')
        c = conn.cursor()
        
        event={
    "id": str(event_.id().to_hex()),
    "tags": str(event_.as_json())}
        c.execute('''
        INSERT INTO event (id, tags)
        VALUES (?, ?)
        ''', (
            event["id"],
            event["tags"])
            
        )
        conn.commit()
     except sqlite3.Error as e:
        print(f"Error during the addition of the event: {e}")
     finally:
        if conn:
            conn.close()

    def no_id(event):
        Nostr_note_id=[]
        Nostr_note=kind1_data_name()
        for Nostr_x in Nostr_note:
           Nostr_note_id.append(Nostr_x["id"])
        if event.id().to_hex() not in Nostr_note_id:    
           return event

    def test_input():
      list_event=test_relay()
      
      if list_event!=None:
       
        for event in list_event[::-1]:
            if no_id(event)!=None:
             add_PC_event(event)
           
    Send_pc_message=Button(frame3, command=test_input, text="Send message")
    Send_pc_message.grid(column=0, row=5)

    def test_input_local():
      list_event=test_local_relay()
      if list_event!=None:
        for event in list_event[::-1]:
           if no_id(event)!=None:
            add_PC_event(event)

    Send_pc_message=Button(frame3, command=test_input_local, text="Local message")
    Send_pc_message.grid(column=0, row=6)

    def fetch_content():
     try:
        name=input_PC.cget('text')
        conn = sqlite3.connect(str(name)+'.db')
        c = conn.cursor()
        c.execute('SELECT * FROM event')
        events = c.fetchall()
        return events
     except sqlite3.Error as e:
        print(f"Error while reading events: {e}")
        return []
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
          if numb_x["tags"]["kind"]==n:
            list_event.append(numb_x["tags"])
       if n==1:     
        numb_lab.config(text=str(len(list_event)))
       else:
         if n==30023:
            numb_lab_2.config(text=str(len(list_event)))
    
    def return_note():
        if Checkbutton5.get() == 1:
         Nostr_note=kind1_data_name()[::-1]
         if len(Nostr_note)>0:
          Text_t.delete("1.0","end")
          if entry_t.get()=="":
           for x in Nostr_note:
            Text_t.insert(END,"pubkey: "+str(x["tags"]['pubkey'])+"\n"+"Time: "+str(x["tags"]['created_at'])+"\n"+"Content: "+ x["tags"]['content']+"\n")  
          else:
            for v in Nostr_note:
             if v["tags"]['tags']!=[]:
              if tags_string(v["tags"],"t")!=[]:
               if entry_t.get() in tags_string(v["tags"],"t"):
                    Text_t.insert(END,"pubkey: "+str(v["tags"]['pubkey'])+"\n"+"Time: "+str(v["tags"]['created_at'])+"\n"+"Content: " +v["tags"]['content']+"\n"
                             +"Tags:" +"\n"+ str(tags_string(v["tags"],"t"))+"\n")       
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
             if x["tags"]['tags']!=[]:
              if tags_string(x["tags"], "t")!=[]:
               for h_tags in tags_string(x["tags"], "t"):
                if h_tags not in tags_one:
                 tags_one.append(h_tags)
           for z in tags_one:
                 Text_t.insert(END,"Tags: "+ str(z) +"\n")  
          else:
            for v in Nostr_note:
             if v["tags"]['tags']!=[]:
              if tags_string(v["tags"],"t")!=[]:
               if entry_t.get() in tags_string(v["tags"],"t"):
                Text_t.insert(END,"pubkey: "+str(v["tags"]['pubkey'])+"\n"+"Time: "+str(v["tags"]['created_at'])+"\n"+"kind: "+str(v["tags"]['kind'])+"\n"+"\n"+"Content: " +v["tags"]['content']+"\n"
                             +"Tags:" +"\n"+ str(tags_string(v["tags"],"t"))+"\n"+"---------------------"+"\n")             
             else:
                 None

    receive_pc_message=Button(frame3, command=return_note, text="return note")
    receive_pc_message.grid(column=1, row=5,pady=2)   
    receive_pc_message=Button(frame3, command=return_Tags, text="return Tags")
    receive_pc_message.grid(column=1, row=6,pady=2)              
    numb_message=Button(frame3, command=lambda:count_note(1), text="numb note")
    numb_message.grid(column=0, row=7,pady=2) 
    numb_post=Button(frame3, command=lambda:count_note(30023), text="numb post")
    numb_post.grid(column=1, row=7,pady=2) 
    numb_lab=Label(frame3,text="")
    numb_lab.grid(column=0,row=8)
    numb_lab_2=Label(frame3,text="")
    numb_lab_2.grid(column=1,row=8)
    frame3.grid()
    
    def delete_column(): 
     if Checkbutton5.get() == 0:
      frame3.destroy()
     else:
        print("Error "+" ") 

    button_delete=Button(frame3,command=delete_column,text="❌")  
    button_delete.grid(column=2,row=0)
    
def report_fake(event):
     id = event[0]
     tags=json.loads(event[1])
     return id,tags

def fake_rerender(event):
    a,d=report_fake(event)
    l={"id":a,"tags":d,}
    return l

def fetch_content_g():
     try:
        name="historyc"
        conn = sqlite3.connect(str(name)+'.db')
        c = conn.cursor()
        c.execute('SELECT * FROM event')
        events = c.fetchall()
        return events
     except sqlite3.Error as e:
        print(f"Error while reading events: {e}")
        return []
     finally:
        if conn:
            conn.close()

def kind1_data_name_g():
        note=fetch_content_g()  
        events=[]
        for j in note:
            events.append(fake_rerender(j))
        return events

def add_user(name,key):
   
    if name!="": 
     if len(key)==64 or len(key)==63:
      value_key=PublicKey.parse(key)
      if name not in my_name:
        my_dict[name]=value_key.to_hex()
        combo_box["value"]=list(my_dict.keys())
        frame_user.place_forget()
   
frame_user=Frame(root,height=100,width=200)
label_user = tk.Label(frame_user, text="Name",font=label_font)
label_user.grid(column=0,row=0,pady=2,padx=10)
label_pubkey = tk.Label(frame_user, text="Pubkey",font=label_font)
label_pubkey.grid(column=1,row=0,pady=2,padx=10)
user_name=StringVar()
label_number = Entry(frame_user, textvariable=user_name, font=entry_font,width=15)
label_number.grid(column=0,row=1,pady=2,padx=10)
key_string=StringVar()
label_key = Entry(frame_user, textvariable=key_string, font=entry_font,width=15)
label_key.grid(column=1,row=1,pady=2,padx=10)
button_add=Button(frame_user, command=lambda:add_user(user_name.get(),key_string.get()), text="add user",font=entry_font)
button_add.grid(column=0,row=2,pady=4,padx=2)

Check_open_2 = IntVar() 
Check_open_2.set(1)

def open_new_user():
 if my_dict=={}:
  if Check_open_2.get()==1:
   Check_open_2.set(0)
  frame_user.place(relx=0.34,rely=0.05,relheight=0.43,relwidth=0.28)

def close_new_user():
   if Check_open_2.get()==0:  
    Check_open_2.set(1)
    frame_user.place_forget()

numb_close=Button(frame_user, command=close_new_user, text="Close x",font=entry_font)
numb_close.grid(column=1,row=2,pady=10,padx=5,rowspan=2)

def open_frame1():
 if Check_open.get()==1:
  Check_open.set(0)
  frame_root.place(relx=0.34,rely=0.005,relheight=0.43,relwidth=0.25)

def close_frame1():
   if Check_open.get()==0:  
    Check_open.set(1)
    frame_root.place_forget()

Check_open = IntVar() 
Check_open.set(1)
frame_menu=Frame(root,width=20,height=1)
menu = Menu(frame_menu)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New User", command=open_new_user)
filemenu.add_command(label="Profile", command=open_frame1)
filemenu.add_command(label="Database", command=OpenColumn)
filemenu.add_command(label="Settings", command=Notebook_)
frame_menu.grid()
relay_list=[]

def get_note(z):
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f

def test_relay():
  if combo_box.get()!="Cluster":
   if __name__ == "__main__":
     combined_results = asyncio.run(Get_random_kind())
     if combined_results:
       return combined_results 
     else:
      print("not found")

def test_local_relay():
   if __name__ == "__main__":
    combined_results = asyncio.run(local_relè())
    if combined_results:
      return combined_results 
    else:
      print("not found")

my_dict = {}
#"name",pubkey
my_list = list(my_dict.values())
my_name = list(my_dict.keys())

def on_select(event):
    selected_item = combo_box.get()
    relay_list.clear()
    search_relay()

def search_relay():
   if __name__ == "__main__":
    asyncio.run(outboxes())

async def get_outbox(client):
  
  if my_dict[combo_box.get()]!="": 
    
    f = Filter().authors(user_convert([my_dict[combo_box.get()]])).kind(Kind(10002))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def outboxes():
    init_logger(LogLevel.INFO)
    client = Client(None)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
         relay_url = RelayUrl.parse(jrelay)
         await client.add_relay(relay_url)
    else:
       relay_url_3 = RelayUrl.parse("wss://nostr.mom/")
       relay_url_4 = RelayUrl.parse("wss://purplerelay.com/")
       await client.add_relay(relay_url_3)
       await client.add_relay(relay_url_4)

       
    await client.connect()
    result_note=await get_outbox(client)
    if result_note!=None:
     relay_add=get_note(result_note)
     if relay_add !=None and relay_add!=[]:
           i=0
           print( tags_string(relay_add[i],'r'))
           while i<len(relay_add):
            for xrelay in tags_string(relay_add[i],'r'):
              if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay[6:9]!="127":
               
               if xrelay not in relay_list:
                 relay_list.append(xrelay) 
            i=i+1             
    await asyncio.sleep(2.0)

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def convert_user(x):
    try:
     other_user_pk = PublicKey.parse(x)
     return other_user_pk
    except NostrSdkError as e:
       print(e,"this is the hex_npub ",x)

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

def number_kind(tm):
    z=[]
    for v in tm:
        if (v)["tags"]['kind'] in z:
              None  
        else:
              z.append((v)["tags"]['kind'])
    return z

def event_number(tm):
    t=number_kind(tm)
    i=0
    number=[]
    while i<len(t):
        tip_i=[]
        for v in tm:
         if (v)["tags"]['kind']==t[i]:
           tip_i.append(v["tags"])
        number.append(tip_i)
        i=i+1
    j=0
    while j<len(number):
     print("kind number", t[j] ,"number event", len(number[j]))
     j=j+1
    return t, number

def stamp_note():
       number_event=kind1_data_name_g()
       event_number(number_event)
       list_kind=[]
       for numb_x in number_event:
          if numb_x["tags"]["kind"] not in list_kind:
             list_kind.append(numb_x["tags"]["kind"])  
       combo_list.set("Kind Event")      
       order_list=list_kind.sort()
       combo_list['values']=list_kind
       
def read_note(n:int):
       list_event=[]
       list_kind=[]
       number_event=kind1_data_name_g()
       for numb_x in number_event:
          if numb_x["tags"]["kind"]==n:
            list_event.append(numb_x["tags"])
          if numb_x["tags"]["kind"] not in list_kind:
             list_kind.append(numb_x["tags"]["kind"])  
       if list_event!=[]:  
        print("kind number ", n,"number of events ",len(list_event))
        order_list=list_kind.sort()
        combo_list.set("Kind Event")
        combo_list['values']=list_kind

def delete_note(n:int):
       list_event=[]
       number_event=kind1_data_name_g()
       for numb_x in number_event:
          if numb_x["tags"]["kind"]==n:
            list_event.append(numb_x["tags"])
       for event_x in list_event:
          delete_events(event_x["id"])
          
def read_kind_note(n:int):
       list_kind_event.clear()
       list_kind=[]
       number_event=kind1_data_name_g()
       for numb_x in number_event:
          if numb_x["tags"]["kind"]==n:
            list_kind_event.append(numb_x["tags"])
          if numb_x["tags"]["kind"] not in list_kind:
             list_kind.append(numb_x["tags"]["kind"])  
       if list_kind_event!=[]:  
        print("kind number ", n, " number of events ",len(list_kind_event))

list_kind_event=[]
frame_root=Frame(root,height=100,width=200)
Profile_frame = ttk.LabelFrame(frame_root, text="Profile", labelanchor="n", padding=10)
Profile_frame.place(relx=0.01,rely=0.001,relwidth=0.95,relheight=0.95)
label = tk.Label(frame_root, text="Name",font=label_font)
label.grid(column=0,row=0,pady=10)
combo_box = ttk.Combobox(frame_root, values=my_name,font=entry_font,width=15)
combo_box.grid(column=0,row=1,pady=1,padx=10)
combo_box.set("Cluster")
combo_box.bind("<<ComboboxSelected>>", on_select)
kind_note=IntVar()
label_number = Entry(frame_root, textvariable=kind_note, font=entry_font,width=15)
label_number.grid(column=0,row=2,pady=10)
numb_=Button(frame_root, command=lambda:read_note(kind_note.get()), text="one event",font=button_font)
numb_.grid(column=0,row=3,pady=10,padx=5)
numb_close=Button(frame_root, command=close_frame1, text="Close x",font=entry_font)
numb_close.grid(column=1,row=0,pady=10,padx=5,rowspan=2)
numb_d=Button(frame_root, command=lambda:delete_note(kind_note.get()), text="delete event",font=button_font)
numb_d.grid(column=1,row=3,pady=10,padx=2) 
numb_1=Button(frame_root, command=stamp_note, text="stamp event",font=button_font)
numb_1.grid(column=0,row=4,pady=10,padx=10)

def on_selection(event):
    selected_item = combo_list.get()
    kind_note.set(int(selected_item))
    read_kind_note(kind_note.get())

combo_list = ttk.Combobox(frame_root, values=[],font=entry_font,width=12)
combo_list.grid(column=0,row=5,padx=10,pady=10)
combo_list.set("")
combo_list.bind("<<ComboboxSelected>>", on_selection)

async def get_author_event(client):
    f= Filter().author(user_convert([my_dict[combo_box.get()]])[0]).kinds([Kind(0),Kind(10002),Kind(3),Kind(30023),Kind(10050),Kind(10012),Kind(1)]).limit(300)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
    z=[]  
    for event in events.to_vec():
     if event.verify()==True:
        z.append(event)
    if z!=[]: 
     return z   
   
async def Get_random_kind():
        
    client = Client(None)
    if relay_list!=[]:
       
       for jrelay in relay_list:
         relay_url = RelayUrl.parse(jrelay)
         await client.add_relay(relay_url)
    else:
     relay_url_1 = RelayUrl.parse("wss://nos.lol/")
     await client.add_relay(relay_url_1)
     relay_url_x = RelayUrl.parse("wss://nostr.mom/")
     await client.add_relay(relay_url_x)

       
    await client.connect()
    await asyncio.sleep(2.0)
   
    test_kind = await get_author_event(client)
    return test_kind   

async def note_kind(client):
    f = Filter().kinds([Kind(0),Kind(10002),Kind(3),Kind(42),Kind(5002)])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=15))
    z=[]
    for event in events.to_vec():
    
     if event.verify()==True:
        z.append(event)
    if z!=[]: 
      return z   
    else:
       return None

async def local_relè():
   init_logger(LogLevel.INFO)
   try:  
    client = Client(None)
    local_h=RelayUrl.parse("ws://localhost:4869")
    await client.add_relay(local_h)
    #await client.add_relay("ws://192.168.1.8:4869/")
   
    await client.connect()
      
    test_kind = await note_kind(client)
    if test_kind:
         await asyncio.sleep(1.0)
         return test_kind
    else:
       print("fail")  
   except NostrSdkError as e:
      print(e)
       
def show_Teed():
 frame2=tk.Frame(root)  
 canvas_1 = tk.Canvas(frame2)
 scrollbar_1 = ttk.Scrollbar(frame2, orient="vertical", command=canvas_1.yview)
 scrollable_frame_1 = ttk.Frame(canvas_1)

 scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all")))

 canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
 canvas_1.configure(yscrollcommand=scrollbar_1.set)

 def create_page(db_list_):
  if db_list_!=[] and db_list_!=None:
   if len(db_list_)>200:
    db_list_=db_list_[0:200] 
   s=1
   for note in db_list_:
     try:
      context0="Pubkey "+note['pubkey']+"\n"
      if note['tags']!=[]:
        context1="Content lenght "+str(len(note["content"]))+"\n"
        context2="\n"
        if tags_string(note,"title")!=[]: 
         xnote= "Title: "+str(tags_string(note,"title")[0])
         context2=context2+str(xnote) +"\n"
        else: 
         if note["kind"]==30023:
          context1="there is no Title"
         context2=""
        if tags_string(note,"summary")!=[] and str(tags_string(note,"summary")[0])!="": 
          xnote= "\n"+"Summary: "+str(tags_string(note,"summary")[0])
          context2=context2+str(xnote) +"\n"
      else:
          context1="no tags"
          context2=""   
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0+context1+context2)

      label_id.grid(pady=2,column=0, columnspan=3)
      def print_id(entry):
           number=list(db_list_).index(entry)
           print(number)
           show_print_test(entry)       
                          
      def print_var(entry):
                print(entry["content"])
           
      button=Button(scrollable_frame_1,text=f"Print me!", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"click to read!", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s,column=1,padx=5,pady=5)      
      s=s+2  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="right", fill="y",pady=20)
   canvas_1.pack( fill="y", expand=True)
   frame2.place(relx=0.34,rely=0.45,relwidth=0.30,relheight=0.4)
    
   def close_number() -> None :
        frame2.destroy()    
        button_f_close.place_forget()
        
   button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"))
   button_f_close.place(relx=0.6,rely=0.4)      
     
 create_page(list_kind_event[::-1])
 root.update_idletasks()
 
button_id=tk.Button(frame_root,command=show_Teed,text="Go id",font=button_font)
button_id.grid(column=1,row=5,padx=10,pady=10)

def show_print_test(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = ttk.Frame(canvas_2)

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")))
   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
   context0="Pubkey: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
   try:
    if note['tags']!=[]:
        context1=note['content']+"\n"
        tag_note=""
        for note_x in note["tags"]:
           tag_note=tag_note+ str(note_x)+"\n"
        context2="[[ Tags ]]"+"\n" +tag_note

    else: 
        context1=note['content']+"\n"
        context2=""
   except TypeError as e:
      print(e)        
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   var_id.set(context0)
   label_id.grid(pady=2,column=0, columnspan=3)
   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
   second_label10 = tk.Text(scrollable_frame_2, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   second_label10.insert(END,context1+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label10.yview )
   second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
      
   def print_note(entry):
           print(entry)

   def print_var(entry):
        if entry["tags"]!=[]:
          if tags_string(entry,"image")!=[]: 
           print("see this photo: ", tags_string(entry,"image")[0])
         
   button=Button(scrollable_frame_2,text=f"Photo!", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Stamp", command=lambda val=note: print_note(val))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
   button_grid3=Button(scrollable_frame_2,text="Delete", command=lambda val=note["id"]: delete_events(val))
   button_grid3.grid(row=s+2,column=2,padx=5,pady=5)
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()    

   button_frame=Button(scrollable_frame_2,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.grid(row=s+3,column=1,padx=5,pady=5)
   frame3.place(relx=0.67,rely=0.45,relwidth=0.3,relheight=0.5 ) 

root.mainloop()