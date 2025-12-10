import asyncio
from datetime import timedelta
from nostr_sdk import *
import json
import requests
import time
import requests
import shutil
import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
from cryptography.fernet import Fernet

root = tk.Tk()
root.geometry("1300x800") 
db_note_list=[]

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f

def timeline_created(list_new):
  new_note=[] 
  global db_note_list
  if db_note_list!=[]:
   for new_x in list_new:
    
     if new_x not in db_note_list:
        new_note.append(new_x) 
   i=0
    
   while i<len(new_note):
     j=0
     while j< len(db_note_list): 
      if db_note_list[j]["created_at"]>(new_note[i]["created_at"]):
         j=j+1
      else:
         db_note_list.insert(j,new_note[i])
         break
     i=i+1
   return db_note_list   
  else:
        for list_x in list_new:
            
             db_note_list.append(list_x)
        return db_note_list  
  
def tags_string(x,obj):
    f=x["tags"]
    z=[]
    
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z     

def codifica_link(x):
   f=url_spam(x)
   list_v=['mov','mp4']
   img=['png','jpg','JPG','gif']
   img1=['jpeg','webp'] 
   tme=["https://t.me/"]
   xtwitter=["https://x.com/"]
   if f==None:
                 return "no spam"
   if f[-3:] in list_v:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   if f[0:13] in tme:
            return "tme"
   if f[0:14] in xtwitter:
            return "tme"
   else:
       return "spam"  

list_note_out=[]
list_note_save=[]

def show_noted():
  """Widget function \n
   Open feed Horizontal, 3 Row
   """
  frame2=tk.Frame(root)  
  if len(db_note_list)<=3:
     canvas_1 = tk.Canvas(frame2)
  else:   
    canvas_1 = tk.Canvas(frame2,width=620)
  scrollbar_1 = ttk.Scrollbar(frame2, orient=HORIZONTAL,command=canvas_1.xview)
  scrollable_frame_1 = tk.Frame(canvas_1,background="#E3E0DD")
  scrollbar_2 = ttk.Scrollbar(frame2, orient=VERTICAL,command=canvas_1.yview)
  scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all") ))

  canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
  canvas_1.configure(xscrollcommand=scrollbar_1.set,yscrollcommand=scrollbar_2.set)
  if db_note_list!=[] and len(list_note_out)!=len(db_note_list):
  
   s=1
   s1=0
   se=0         
   db_note_max=[]
 
   if len(db_note_list)>12:
      for note in db_note_list:
         if note not in list_note_out: #or note in list_note_save:
            list_note_out.append(note)
            if len(db_note_max)<12:
             db_note_max.append(note)
            else:
               break
                
   else: 
           
      db_note_max=db_note_list   
   if len(list_note_save)==12:
    
    db_note_max=list_note_save    
   i=0   
   for note in db_note_max:   
    
      if i% 3==0:
        s1=0
        se=int(i//3)+i
      
      i=i+1    
  
      try:
       
       context0="Author: "+note['pubkey']
       context1=note['content']+"\n"
       context2=" "
       if note['tags']!=[]: 
         
        if tags_string(note,"d")!=[]:
              
             context2=context2+"https://"+str(tags_string(note,"d")[0])+ "\n"
        
        
        for xnote in tags_string(note,"title"):
         context2=context2+"\n"+str(xnote) +"\n"
       
        if len(tags_string(note,"t"))==1:
         for xnote in tags_string(note,"t"):
          context2=context2+"Category "+str(xnote) +" "  
        else:
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context2=context2+"#"+str(xnote) +"\n"
            s=s+1
        
       else: 
        context1=note['content']+"\n"
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=210,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=se,column=s1, columnspan=3)
       if note in list_note_save:
        button_keep=Button(scrollable_frame_1,text=f"X", command=lambda val=note: un_save(val),fg="blue")
        button_keep.grid(column=s1+3,row=se,padx=5,pady=5)
       else:
        button_keep=Button(scrollable_frame_1,text=f"S", command=lambda val=note: keep_safe(val))
        button_keep.grid(column=s1+3,row=se,padx=5,pady=5)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=se+1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=20, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=se+1) 
       
       def keep(entry):
         try:
          number=list_note_out.index(entry)
          list_note_out.pop(number)
         except ValueError as e:
            print(e)

       def keep_safe(entry):
         try:
          if entry not in list_note_save:
             if len(list_note_save)<12:
              number=list_note_out.index(entry)
              list_note_save.append(entry)
              if (len(list_note_save))==12: 
               button_open.config(text="Save link")
              text_var_1.set(len(list_note_save))
              labeL_n.place(relx=0.45,rely=0.03 ) 
            
                
           
         except ValueError as e:
            print(e)     

       def un_save(entry):
         try:
          if entry in list_note_save:
              number_1=list_note_save.index(entry)
              list_note_save.pop(number_1)
              if (len(list_note_save))!=12: 
               button_open.config(text="Next Note")
              text_var_1.set(len(list_note_save))
              labeL_n.place(relx=0.45,rely=0.03 ) 
           
         except ValueError as e:
            print(e)          

       def print_id(entry):
            if entry["tags"]!=[]:
              print(db_note_list.index(entry)+1)
              if tags_string(entry,"d")!=[]:
                 show_print_test_tag(entry)
              else:
                 print(entry["tags"])   
                  
       def print_var(entry):
                print(entry)
                print(entry["id"],"\n",entry["content"])

       button=Button(scrollable_frame_1,text=f"Print Note", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=se+2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
       button_grid2.grid(row=se+2,column=s1+1,padx=5,pady=5)    
                                 
       s=s+2  
       s1=s1+4
       root.update() 
      except NostrSdkError and IndexError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="bottom", fill="x",padx=20)
   scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
   canvas_1.pack( fill="both", expand=True)
   frame2.place(relx=0.28,rely=0.1,relwidth=0.72,relheight=0.62)

   def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
        entry_text.place_forget()
        scroll_bar_text.place_forget()
        
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.55,rely=0.02,relwidth=0.1)      

scroll_bar_text = tk.Scrollbar(root, background="darkgrey")
entry_text=tk.Text(root, background="grey", yscrollcommand = scroll_bar_text.set, font=('Arial',14,'bold'))
scroll_bar_text.config( command = entry_text.yview )

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list 

def url_spam(x):
 z=x['content']
 for j in z.split():
    if j[0:5]=="https":
        return str(j)

def more_spam(x):
 z=x['content']
 notes_link=[]
 for j in z.split():
    if j[0:5]=="https":
        notes_link.append(str(j))
 return notes_link    

def more_link(f):
   
   list_v=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_v:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam"   

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z       

def test_relay():
   if __name__ == "__main__":
     
    combined_results = asyncio.run(Get_notes())
    List_note=get_note(combined_results)
   if List_note:
    
    return List_note    
   else:
      print("not found")
   
async def get_kind(client):
    f= Filter().kind(Kind(39701)).limit(300)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z   

relay_list=[] 

def relay_class():
          if entry_relay.get()!="":
            if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/" and len(entry_relay.get())>7:
                
                if entry_relay.get() not in relay_list:
                    relay_list.append(entry_relay.get())
                add_relay_str.set("wss:// ")    
                counter_relay['text']=str(len(relay_list)) 
                counter_relay.place(relx=0.25,rely=0.05, relheight=0.04)
            else:
               print(entry_relay.get())   
            entry_relay.delete(0, END)
            add_relay_str.set("wss:// ") 

relay_button = tk.Button(root, text="Add Relay ", font=("Arial",12,"normal"),background="grey", command=relay_class)
counter_relay=Label(root,text="",background="darkgrey",font=('Arial',12,'normal'))
add_relay_str=StringVar()
entry_relay=ttk.Entry(root,justify='left',font=("Arial",12,"bold"),width=12,textvariable=add_relay_str)
add_relay_str.set("wss:// ")
entry_relay.place(relx=0.05,rely=0.05)
relay_button.place(relx=0.165,rely=0.05)   

async def Get_notes():
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    list_relay_set={"wss://nos.lol/","wss://nostr.mom/"}
    for relay_x in list_relay_set:
      if relay_x not in relay_list:
         relay_list.append(relay_x)
    await Search_status(client=Client(None),list_relay_connect=relay_list)      
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(RelayUrl.parse(jrelay))
                      
    await client.connect()
    await asyncio.sleep(2.0)
   
    test_kind = await get_kind(client)
    await client.disconnect()
    return test_kind   

def second_one_filter():
     second_filter=test_relay()
     if second_filter:
         timeline_created(second_filter)
         print(len(db_note_list))
         button_open.place(relx=0.4,rely=0.02,anchor='n' ) 
         button_close_save.place(relx=0.5,rely=0.02,anchor='n' )  
         show_read()
                
def show_read():
   show_noted()

def clear_list_save():
   list_note_save.clear()   
   button_open.config(text="Next Note")
   text_var_1.set(len(list_note_save))

button_RE=Button(root,command=second_one_filter, text="Relay Note", font=('Arial',12,'normal'))
button_RE.place(relx=0.2,rely=0.1,anchor='n' )  
button_open=Button(root,command=show_read, text="Next Note", font=('Arial',12,'normal'))
button_close_save=Button(root,command=clear_list_save, text="x", font=('Arial',12,'normal'))

def show_print_test_tag(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = tk.Frame(canvas_2, background="#E3E0DD")

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")))

   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
              
   var_id_3=StringVar()
   label_id_3 = Message(scrollable_frame_2,textvariable=var_id_3, relief=RAISED,width=290,font=("Arial",12,"normal"))
   label_id_3.grid(pady=1,padx=8,row=s,column=0, columnspan=3)
   var_id_3.set("Author: "+note['pubkey'])

   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid( sticky = NS,column=4,row=s+1)
   second_label_10 = tk.Text(scrollable_frame_2, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   context2=""   
   if tags_string(note,"t")!=[]:
        for note_tags in tags_string(note,"t"):
            context2=context2+str("#")+note_tags+" "
   else:
           context2=""  
   if tags_string(note,"d")!=[]:
    context2=context2+"https://"+str(tags_string(note,"d")[0])+ "\n"
   second_label_10.insert(END,note["content"]+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label_10.yview )
   second_label_10.grid(padx=10, column=0, columnspan=3, row=s+1) 

   def print_content(entry):
       test1=tags_string(entry,"t")
       if test1!=[]:
        s=5
        ra=0
        se=1
        ti=2

        def show_tag(entry):
         hashtag_list=search_for_channel(entry)
         if hashtag_list:
           show_lst_ntd(hashtag_list)

        
        
        
        test1.sort()
        
        while ra<len(test1):
   
         button_grid1=Button(scrollable_frame_2,text=f"{test1[ra]} ", command=lambda val=test1[ra]: show_tag(val))
         button_grid1.grid(row=s,column=0,padx=5,pady=5)
    
         if len(test1)>se:
            button_grid2=Button(scrollable_frame_2,text=f"{test1[ra+1]}", command= lambda val=test1[ra+1]: show_tag(val))
            button_grid2.grid(row=s,column=1,padx=5,pady=5)
         if len(test1)>ti:
          button_grid3=Button(scrollable_frame_2,text=f"{test1[ra+2]}", command= lambda val=test1[ra+1]: show_tag(val))
          button_grid3.grid(row=s,column=2,padx=5,pady=5)   
        
         root.update()  
         s=s+1
         se=se+3
         ra=ra+3
         ti=ti+3   
         
                   
   if tags_string(note,"d")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read Tag ", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    

   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     button_frame.place_forget()
     frame3.destroy()    
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.75,rely=0.04) 
   frame3.place(relx=0.66,rely=0.1,relheight=0.35,relwidth=0.33) 


def list_people_fun():
    people_list=[]
    if db_note_list!=[]:
        for note_x in db_note_list:
            if note_x["pubkey"] not in people_list:
                        people_list.append(note_x["pubkey"])
                 
        return people_list       
    else:
       return people_list

text_var_1=IntVar()
labeL_n=Label(root,textvariable=text_var_1,font=('Arial',12,'normal'))

def pubkey_id(test):
   note_pubkey=[]
   for note_x in db_note_list:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   return len(note_pubkey),note_pubkey          

def show_lst_ntd(list_note_p):
 frame2=tk.Frame(root)  
 canvas_1 = tk.Canvas(frame2)
 scrollbar_1 = ttk.Scrollbar(frame2, orient=HORIZONTAL,command=canvas_1.xview)
 scrollable_frame_1 = tk.Frame(canvas_1,background="#E3E0DD")
 scrollbar_2 = ttk.Scrollbar(frame2, orient=VERTICAL,command=canvas_1.yview)
 scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all")))
 canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
 canvas_1.configure(xscrollcommand=scrollbar_1.set,yscrollcommand=scrollbar_2.set)
 if list_note_p!=[]:
  
  s=1
  s1=0
  
  for note in list_note_p:
         
      try:
        
       context0="Author: "+note['pubkey']
       context1=note['content']+"\n"
       context2=" "
       if note['tags']!=[]: 
         
        if tags_string(note,"d")!=[]:
            context2=context2+str("https://"+tags_string(note,"d")[0])+ "\n"
              
        else:
               pass
        for xnote in tags_string(note,"title"):
         context2=context2+"\n"+str(xnote) +"\n"
       
        if tags_string(note,"t")!=None and tags_string(note,"t")!=[] :
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context2=context2+"#"+str(xnote) +" "
            s=s+1
        
       else: 
        context1=note['content']+"\n"
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=29, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=1) 
      
       def print_id(entry):
            if entry["tags"]!=[]:
              print(db_note_list.index(entry)+1)
              if tags_string(entry,"d")!=[]:
                 show_print_test_tag(entry)
              else:
                 print(entry["tags"])   
                  
       def print_var(entry):
                print(entry["content"])

                                                                                 
                                      
       button=Button(scrollable_frame_1,text=f"Print note", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
       button_grid2.grid(row=2,column=s1+1,padx=5,pady=5)    
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

  scrollbar_1.pack(side="bottom", fill="x",padx=2)
  scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
  canvas_1.pack( fill="y", expand=True)
  frame2.place(relx=0.66,rely=0.45,relwidth=0.34,relheight=0.31)

  def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
  button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
  button_frame.place(relx=0.74,rely=0.75,relwidth=0.1)      

test_note=[]
list_note_read=[]

def list_hashtag_fun():
    hashtag_list=[]
    if db_note_list!=[]:
        for note_x in db_note_list:
            if tags_string(note_x,"t")!=[]:
               for hash_y in tags_string(note_x,"t"):
                  if str(hash_y).islower(): 
                        if hash_y not in hashtag_list:
                           hashtag_list.append(hash_y)
                  
                              
        return hashtag_list       
    else:
       return hashtag_list       

entry_channel=StringVar()

hash_list_notes=[]

def search_for_channel(note_hash):
     Notes=db_note_list
     if Notes:
        hash_list_notes.clear()
        for note_x in Notes:
            if str(note_hash).lower() in tags_string(note_x,"t"): 
               hash_list_notes.append(note_x)
        return hash_list_notes      


def call_hashtag():
  if relay_list!=[]:
  
   if __name__ == "__main__":
    response=asyncio.run(Get_notes)
    if response!= None and response!=[]:
       response_list= get_note(response)
       timeline_created(db_note_list,response_list) 
       
def print_list_tag(): 
  """Widget function \n
   List of hashtag  \n
   and search

  """
  open_frame() 
  if db_note_list!=[]:  
   frame3=tk.Frame(root)
   canvas = tk.Canvas(frame3,width=230)
   scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
   scrollable_frame = ttk.Frame(canvas,border=2)
   scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
     
   canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
   canvas.configure(yscrollcommand=scrollbar.set)
   s=1     
   
   test1=list_hashtag_fun()
   if test1!=[]:
       
        def print_id(test):
         
         
         entry_channel.set(test)
         tag=search_for_channel(test)
         if tag:
          button_open=Button(root, command=show_lst_ntd(tag), text="Open Tag",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
                
        ra=0
        se=1
        test1.sort()
        
        while ra<len(test1):
           
            button_grid1=Button(scrollable_frame,text=f"{test1[ra]} ", command=lambda val=test1[ra]: print_id(val))
            button_grid1.grid(row=s,column=1,padx=5,pady=5)
            
            if len(test1)>se:
             button_grid2=Button(scrollable_frame,text=f"{test1[ra+1]}", command= lambda val=test1[ra+1]: print_id(val))
             button_grid2.grid(row=s,column=2,padx=5,pady=5)
        
            root.update()  
            s=s+1
            se=se+2
            ra=ra+2   
   else:
     print("error") #It didn't find a channel
     
   canvas.pack(side="left", fill="y", expand=True)
   if len(test1)>5:
      scrollbar.pack(side="right", fill="y")  
   frame3.place(relx=0.01,rely=0.36,relwidth=0.25)      
    
   def Close_print():
      frame3.destroy()  
   if test1!=[]:   
      button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
      button_close_.pack(pady=5,padx=5)    
   else:
      Close_print() 
 
button_tag=tk.Button(root,text="Tag List",command=print_list_tag, font=('Arial',12,'bold'))
button_tag.place(relx=0.17,rely=0.15)

def open_frame():
 if Check_open.get()==1:
  Check_open.set(0)
  button_frame_c=Button(frame1,command=close_frame1,text="Close ❌",font=("Arial",12,"normal"))
  button_frame_c.grid(column=2, row=4, padx=2, pady=5)
  frame1.place(relx=0.01,rely=0.75,relwidth=0.32,relheight=0.23)

def close_frame1():
   if Check_open.get()==0:  
    Check_open.set(1)
    frame1.place_forget()

Check_open = IntVar() 
Check_open.set(1)
frame1=tk.Frame(root,height=100,width=200)
frame_time=tk.Frame(root,height=100,width=200)
entry_channel=StringVar()
wall_2=tk.Label(frame_time, text="",background="lightgrey",height=4)
label_since=Label(frame_time,text="day since",font=("Arial",12,"normal"))

def five_event():
     if Checkbutton5.get() == 0:
        Button5.config(text= " 60 day")
        frame_time.place_forget()
        
     else:
       
        Button5.config(text= "Time")
        frame_time.place(relx=0.35,rely=0.8)

Checkbutton5 = IntVar()         
Button5 = Checkbutton(frame1, text = "60 day", variable = Checkbutton5, onvalue = 1, offvalue = 0, height = 2, width = 10,font=('Arial',16,'normal'),command=five_event)
Button5.grid(column=0, row=0,rowspan=3,padx=10)     
since_variable=IntVar(value=1)
since_entry=Entry(frame_time,textvariable=since_variable,font=("Arial",12,"normal"),width=5)
until_variable=IntVar()
until_entry=Entry(frame_time,textvariable=until_variable,font=("Arial",12,"normal"),width=5)

def next_since():
   since_variable.set(int(since_entry.get()) + 1)

def back_since():
   if int(since_entry.get())- 1<1:
      since_variable.set(int(1))
   else:
    if int(since_entry.get())- 1==int(until_entry.get()):
       since_variable.set(since_entry.get())
    else:   
     since_variable.set(int(since_entry.get())- 1)   

def next_until():
   if int(until_entry.get()) + 1>=int(since_entry.get()):
       until_variable.set(until_entry.get())
   else:    
    until_variable.set(int(until_entry.get()) + 1)

def back_until():
   if int(until_entry.get())- 1<0:
      until_variable.set(0)
   else:
    until_variable.set(int(until_entry.get())- 1) 

button_mov=tk.Button(frame_time,text="➕",command=next_since)   
button_back=tk.Button(frame_time,text="➖",command=back_since)  
label_until=Label(frame_time,text="day until",font=("Arial",12,"normal"))
label_until.grid(column=6,row=5,pady=10)
button_mov_dep=tk.Button(frame_time,text="➕",command= next_until)       
button_mov_dep.grid(column=7, row=5,padx=5,pady=5)
button_back_dep=tk.Button(frame_time,text="➖",command=back_until)       
button_back_dep.grid(column=7, row=6,padx=5,pady=5)
since_entry.grid(column=1,row=6,pady=10,padx=10)
until_entry.grid(column=6,row=6,pady=10)
wall_2.grid(column=0, row=5,pady=5, rowspan=2)
label_since.grid(column=1,row=5,pady=10)    
button_mov.grid(column=2, row=5,padx=5,pady=5)     
button_back.grid(column=2, row=6,padx=5,pady=5)     
entry_variable=StringVar()
entry_var=Entry(frame1, textvariable=entry_variable,font=("Arial",12,"bold"),width=17)
entry_var.grid(column=0,row=4)
scroll_bar_mini = tk.Scrollbar(frame1)
scroll_bar_mini.grid( sticky = NS,column=3,row=0,rowspan=3)
second_label_t = tk.Text(frame1, padx=10, height=5, width=16, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'))
scroll_bar_mini.config( command = second_label_t.yview )
second_label_t.grid(padx=10, column=1, columnspan=2, row=0, rowspan=3,pady=5) 
db_list_note=[]

def call_text():
  if entry_var.get()!="":
   if __name__ == "__main__":
    response=asyncio.run(Search_text())
    if response:
     second_label_t.delete("1.0", "end")
     note_=get_note(response)
     timeline_created(note_)
     for jnote in note_:
              
       if len(jnote["content"])<300:
          second_label_t.insert(END, str("https://")+str(tags_string(jnote,"d")[0]+"\n"+jnote["content"]))
                    
       second_label_t.insert(END,"\n"+"____________________"+"\n")
       second_label_t.insert(END,"\n"+"\n")
     show_print_test_tag(jnote)
       
    else:
       print("empty")
  else:     
       if relay_search_list==[]:
          if __name__ == "__main__":
            response=asyncio.run(Search_text())
          if len(relay_search_list)>0:
             button_close_search["text"]="Search 🔍 url" 

button_close_search=tk.Button(frame1, text='Search Relay',font=('Arial',12,'bold'), command=call_text)    
button_close_search.grid(column=1,row=4)

def since_day(number):
    import datetime
    import calendar
    date = datetime.date.today() - datetime.timedelta(days=number)
    t = datetime.datetime.combine(date, datetime.time(1, 2, 1))
    z=calendar.timegm(t.timetuple())
    return z

def url_speed(string):
 z=string
 for j in z.split():
    if j[0:8]=="https://":
        return str(j)[8:]   
    if j[0:7]=="http://":
      return str(j)[7:]  
    return str(string)  

relay_search_list=[]

async def get_result_(client):
   if entry_var.get()!="":  
    if Checkbutton5.get() == 1:
          f = Filter().search(entry_var.get()).kind(Kind(39701)).since(timestamp=Timestamp.from_secs(since_day(int(since_entry.get())))).until(timestamp=Timestamp.from_secs(since_day(int(until_entry.get())))).limit(10)
    else:
          url=url_speed(entry_var.get())
          f = Filter().identifier(url).kind(Kind(39701)).since(timestamp=Timestamp.from_secs(since_day(int(60)))).until(timestamp=Timestamp.from_secs(since_day(int(0)))).limit(10)
          print(url)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Search_text():
    init_logger(LogLevel.INFO)
    client = Client(None)
    
    if relay_search_list!=[]:
      
      
      for jrelay in relay_search_list:
         await client.add_relay(RelayUrl.parse(jrelay))
      await client.connect()
      combined_results = await get_result_(client)
      if combined_results:
        return combined_results
     
    await search_box_relay()
    

public_list=[]

async def get_search_relay(client):
   if public_list!=[]:
    f=Filter().authors(public_list).kind(Kind(10007))
   else: 
    f=Filter().kind(Kind(10007)).limit(10)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   return z

async def search_box_relay():
        
    client = Client(None)
    
    list_relay_set={"wss://nostr.mom/"}
    for relay_x in list_relay_set:
      if relay_x not in relay_list:
         relay_list.append(relay_x)
    if relay_list!=[]:
      
      for jrelay in relay_list:
         await client.add_relay(RelayUrl.parse(jrelay))
      
      await client.connect()
      relay_add=get_note(await get_search_relay(client))
      if relay_add !=None and relay_add!=[]:
           i=0
           while i<len(relay_add):
            for xrelay in tags_string(relay_add[i],'relay'):
              if xrelay[0:6]=="wss://":
               if xrelay not in relay_search_list:
                relay_search_list.append(xrelay) 
              
            i=i+1             
           await Search_status(client=Client(None),list_relay_connect=relay_search_list)

Check_raw =IntVar()

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.65,rely=0.12,relheight=0.75,relwidth=0.3) 
        lab_button_x.place(relx=0.92,rely=0.15)     
        button_up_relay.place(relx=0.88,rely=0.78 )
        r_tag.place(relx=0.7,rely=0.43,relwidth=0.1 )
        r_summary.place(relx=0.7,rely=0.47,relwidth=0.2 )
        r_button.place(relx=0.7,rely=0.52,relwidth=0.1)
        r_view.place(relx=0.85,rely=0.52)
        error_label.place(relx=0.7,rely=0.9)
        print_label.place(relx=0.7,rely=0.95)
        descr_tag.place(relx=0.7,rely=0.17,relwidth=0.1,relheight=0.1 )
        descr_summary.place(relx=0.7,rely=0.27,relwidth=0.2 )
        descr_button.place(relx=0.82,rely=0.2)
        descr_view.place(relx=0.7,rely=0.32,relwidth=0.23,relheight=0.1)
        d_button.place(relx=0.83,rely=0.59,relwidth=0.07)  
        d_tag.place(relx=0.75,rely=0.6 )
        d_title.place(relx=0.75,rely=0.65)
        d_view.place(relx=0.7,rely=0.7) 
        combo_lab.place(relx=0.7,rely=0.03,relwidth=0.15)
        button_send.place(relx=0.75,rely=0.78,relwidth=0.1,relheight=0.05,anchor='n' )
        button_entry1.place(relx=0.82,rely=0.78,relwidth=0.05, relheight=0.05,anchor="n" )
   else:
      Check_raw.set(0)
      lab_button_x.place_forget()
      stuff_frame.place_forget() 
      r_tag.place_forget()
      r_summary.place_forget()
      r_button.place_forget()
      r_view.place_forget()
      error_label.place_forget()
      print_label.place_forget()
      descr_tag.place_forget()
      descr_summary.place_forget()
      descr_button.place_forget()
      descr_view.place_forget()
      combo_lab.place_forget()
      d_button.place_forget()
      d_tag.place_forget()
      d_title.place_forget()
      button_send.place_forget()
      button_entry1.place_forget()
      d_view.place_forget()
      button_up_relay.place_forget()

def d_tag_show():
    title=d_title.get()
    global d_identifier
    if title!="":
       if  codifica_spam()=="spam":
            d_identifier=title[8:]
            print(d_identifier)
            d_view.config(text=d_identifier[0:30]+"\n"+d_identifier[30:60]+"\n"+d_identifier[60:90]) 

def url_speed_one():
 z=d_title.get()
 for j in z.split():
    if j[0:8]=="https://":
        return str(j)   
    
def codifica_spam():
   f=url_speed_one()
   list=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jepg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam"     

def r_show():
     r_tag_entry=r_summary.get()
     if r_tag_entry!="":
        if r_tag_entry not in list_content:
            list_content.append(r_tag_entry)
            r_view.config(text=str(len(list_content)))
            r_summary.delete(0, END)
        else:
             r_view.config(text="Enter a Content: " )         
             r_summary.delete(0, END)
     else:
            r_view.config(text="Uncorrect: ")             
            r_summary.delete(0, END)
       
def show_descr():
    if len(list_title)<1:
     descr_entry=descr_summary.get()
     if descr_entry!="":
           if len(descr_entry)<105:
                
                descr_view.config(text=str(descr_entry[0:35]+"\n ")+ str(descr_entry[35:70]+"\n")+ str(descr_entry[70:105]))
           else:
            descr_view.config(text="Sorry, this is longer than a tweet: " + str(len(descr_entry))+"\n"+descr_entry[0:60])
                       
           def add_description():
             if len(list_title)<1:
              list_title.append(descr_summary.get())
              descr_view.config(text=str(len(list_title)))
              descr_summary.delete(0, END)
              add_button.place_forget()
             else:
               descr_summary.delete(0, END)
               add_button.place_forget()  

           add_button = tk.Button(root, text="Add", font=("Arial",12,"bold"), command=add_description)
           add_button.place(relx=0.91,rely=0.26) 
        
     else:
           
            if len(list_title)==1: 
                descr_view.config(text=str(len(list_title)))
            else:
                 descr_view.config(text="Uncorrect: ")                
            descr_summary.delete(0, END)
    else:
        descr_view.config(text=str(len(list_title)))
        descr_summary.delete(0, END)                     

stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)   
lab_button_x = tk.Button(root, foreground="red",text="X", font=("Arial",12,"bold"), command=raw_label)
r_tag = tk.Label(root, text="Content-Tag",font=("Arial",12,"bold"))
r_summary=ttk.Entry(root,justify='left',font=("Arial",12))
r_button = tk.Button(root, text="Content tag", font=("Arial",12,"bold"), command=r_show)
r_view = tk.Label(root, text="Content: ", font=("helvetica",13,"bold"),justify="center")
d_button = tk.Button(root, text="View d Tag", font=("Arial",12,"bold"), command=d_tag_show)
e_tag = tk.Label(root, text="e-Tag",font=("Arial",12,"bold"))
e_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12))
list_content=[]                  
descr_tag = tk.Label(root, text="Title-Tag",font=("Arial",12,"bold"))
descr_summary=ttk.Entry(root,justify='left',font=("Arial",12))
descr_button = tk.Button(root, text="Preview ", font=("Arial",12,"bold"), command=show_descr)
descr_view = ttk.Label(root, text="Title: ", font=("helvetica",12,"bold"),justify='left')
entry_Home_title=ttk.Label(frame1,text="Speed Link", justify='left',font=("Arial",12,"bold"), background="darkgrey",border=2)
entry_Home_title.place(relx=0.1,rely=0.1)
str_test=StringVar()
List_note_write=[]
relay_list=[]
lab_button = tk.Button(root, text="Share Link", font=("Arial",12,"bold"), command=raw_label)
lab_button.place(relx=0.88,rely=0.03)
d_tag = tk.Label(root, text="d-Tag",font=("Arial",12,"bold"))
d_title=ttk.Entry(root,justify='left',font=("Arial",12))
d_view = tk.Label(root, text="d-view ", font=("helvetica",13,"bold"),justify="center")
d_identifier=""
list_title=[]
error_label = tk.Label(root, text="Problem:",font=("Arial",12))
print_label = ttk.Label(root, text="Wait for Tag",font=("Arial",12))



def link_share():
   check_square()
   lists_id=[] 
   if button_entry1.cget('foreground')=="green":
    global d_identifier
    if d_identifier!="":
      
      lists_id.append(Tag.identifier(d_identifier))
      if list_title!=[]:   
         lists_id.append(Tag.title(list_title[0]))
         
         if combo_lab.get()!="Type of Hashtag":        
            lists_id.append(Tag.hashtag(str(combo_lab.get()).lower()))
         else:
            pass   

         if __name__ == '__main__':
          lists_id.append(Tag.custom(TagKind.PUBLISHED_AT() , [str( int(time.time()) )]))
          if list_content==[]:
             list_content.append("")
          test_result =asyncio.run(link_it(lists_id,list_content[0]))
          messagebox.showinfo("Result",str(test_result))
          button_entry1.config(text="■",foreground="grey")
          list_content.clear()
          list_title.clear()
          combo_lab.set("Type of Hashtag")
          d_identifier=""
          d_view.config(text="")  
          d_title.delete(0, END)
          descr_view.config(text="")
          r_view.config(text="")
          error_label.config(text="Problem:")
          print_label.config(text="Wait for Tag", font=("Arial",12,"bold"),foreground="black")

def check_square():
    if d_identifier!="" and list_title!=[]:
       
       if combo_lab.get()!="Type of Hashtag":
        print_label.config(text="Hashtag "+combo_lab.get(), font=("Arial",12,"bold"),foreground="blue")
        button_entry1.config(text="■",foreground="green")
        error_label.config(text="ok")
       
       else:
        print_label.config(text="Hashtag "+combo_lab.get(), font=("Arial",12,"bold"),foreground="blue")
        button_entry1.config(text="■",foreground="green")
        error_label.config(text="ok, No Tag ")
  
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for Tag", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")

button_send=tk.Button(root,text="Speed Link",command=link_share, background="darkgrey",font=("Arial",12,"bold"))
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)

def add_tag(event):
   if len(Lab_list)==5:
      hashtag=list_hashtag_fun()
      if hashtag!=[]:
         combo_lab.set("Type of Hashtag")
         for hash_one in hashtag:
            if hash_one not in Lab_list:
               Lab_list.append(hash_one)
         Lab_list.sort()       
         combo_lab['values']=Lab_list    
        
Lab_list=["energy","nostr","bitcoin","money","ai"]
combo_lab = ttk.Combobox(root, values=Lab_list,font=('Arial',14,'bold'))
combo_lab.set("Type of Hashtag")
combo_lab.bind("<<ComboboxSelected>>", add_tag)

async def link_it(tag,description):
   
   init_logger(LogLevel.INFO)
   key_string=log_these_key()
   if key_string!=None: 
    keys = Keys.parse(key_string)
       
    signer=NostrSigner.keys(keys)
    client = Client(signer)

    if relay_list!=[]:
       
     for jrelay in relay_list:
        relay_url = RelayUrl.parse(jrelay)
        await client.add_relay(relay_url)
     await client.connect()
    
     builder = EventBuilder(Kind(39701),description).tags(tag)
     test_result_post= await client.send_event_builder(builder)
    
     f = Filter().authors([keys.public_key()]).kind(Kind(39701)).limit(3)
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     for event in events.to_vec():
       if event.verify():
           print(event.as_json())
     return test_result_post    

def Open_txt_note(name):
      if name:
          try:
            with open(name+str(".txt"), mode="r", encoding="utf-8") as f:
                content = f.read()
                return content
          except FileNotFoundError as e:
             print(e)      

def log_these_key():
   try: 
    test_key= Open_txt_note("fernet_key_test")
    fernet=Fernet(test_key[1:])
    note=Open_txt_note("message_test")
    
    decMessage = fernet.decrypt(note[1:]).decode()
    return decMessage
   except FileNotFoundError as e:
       print(e)

def upload_relay_list(name):
    with open(name+".txt", 'r',encoding="utf-8") as file:
        global relay_list 
        new_relay=file.read()
        new_relay = json.loads(new_relay.replace("'", '"'))
        
        for jrelay in new_relay:
         if jrelay!="":
          if jrelay[0:6]=="wss://" and jrelay[-1]=="/":
           
            if jrelay not in relay_list:
                relay_list.append(jrelay)

def upload_relay():
 upload_relay_list("relay")  
 for relay_s in relay_list:
    print(str(relay_s))

button_up_relay=tk.Button(root,text="Relay",command=upload_relay, background="darkgrey",font=("Arial",14,"bold"))

async def Search_status(client:Client,list_relay_connect:list):
    try: 
        if list_relay_connect!=[]:
            for relay_y in list_relay_connect:
                await client.add_relay(RelayUrl.parse(relay_y))
            await client.connect()
            relays = await client.relays()
            await asyncio.sleep(1.0)   
            for url, relay in relays.items():
                i=0
                while i<2:   
            
                    print(f"Relay: {url}")
                    print(f"Connected: {relay.is_connected()}")
                    print(f"Status: {relay.status()}")
                    stats = relay.stats()
                    print("Stats:")
                    print(f"    Attempts: {stats.attempts()}")
                    print(f"    Success: {stats.success()}")
                    
                    
                    if stats.bytes_received()>0:  #Auth ort other stuff
                           if str(url) in list_relay_connect:
                            list_relay_connect.remove(str(url))
                    if i==1:

                     if stats.success()==0 and relay.is_connected()==False:
                            if str(url) in list_relay_connect:
                                list_relay_connect.remove(str(url))
                        
                    i=i+1 
    except IOError as e:
        print(e) 
    except ValueError as b:
        print(b)                   

async def Search_one_status(client:Client,relay_str:str):
    try: 
         if relay_str.startswith("wss://"):
            await client.add_relay(RelayUrl.parse(relay_str))
            await client.connect()
            relays = await client.relays()
            await asyncio.sleep(1.0)   
            for url, relay in relays.items():
                i=0
                while i<2:   
            
                    print(f"Relay: {url}")
                    print(f"Connected: {relay.is_connected()}")
                    print(f"Status: {relay.status()}")
                    stats = relay.stats()
                    print("Stats:")
                    print(f"    Attempts: {stats.attempts()}")
                    print(f"    Success: {stats.success()}")
                    
                    
                    if stats.bytes_received()>0:  #Auth ort other stuff
                           return stats.bytes_received()
                    if i==1:

                     if stats.success()==0 and relay.is_connected()==False:
                           return stats.success() 
                            
                        
                    i=i+1 
         else:
            return 0           
    except IOError as e:
        print(e) 
    except ValueError as b:
        print(b)                   

root.mainloop()