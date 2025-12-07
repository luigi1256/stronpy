import asyncio
from datetime import timedelta
from nostr_sdk import *
import json
import requests
import time
from asyncio import get_event_loop
import requests
import shutil
import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
from cryptography.fernet import Fernet

root = tk.Tk()
root.geometry("1300x800") 

def d_tag_show():
    title=d_title.get()
    global d_identifier
    if title!="":
       if  codifica_spam()=="spam":
            d_identifier=title[8:]
            print(d_identifier)
            d_title.delete(0, END)
            
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

def show_descr():
    if len(list_title)<1:
     list_title.append(descr_summary.get())
     descr_summary.delete(0, END)
    else:
            descr_summary.delete(0, END)

def Clear_Button():
   descr_summary.delete(0, END)  
   descr_summary.delete(0, END)
   combo_lab.set("Tag")         

Check_raw =IntVar()
stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)         
clear_button = tk.Button(root, text="Clear", font=("Arial",12,"bold"), command=Clear_Button)
descr_tag = tk.Label(root, text="Title-Tag",font=("Arial",12,"bold"))
descr_summary=ttk.Entry(root,justify='left',font=("Arial",12))
str_test=StringVar()
List_note_write=[]
relay_list=[]
d_tag = tk.Label(root, text="d-Tag",font=("Arial",12,"bold"))
d_title=ttk.Entry(root,justify='left',font=("Arial",12))
d_identifier=""
list_title=[]
add_tag_str=StringVar()
entry_tag=ttk.Entry(root,justify='left',font=("Arial",12,"bold"),width=12,textvariable=add_tag_str)

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.03,rely=0.2,relheight=0.35,relwidth=0.23) 
        descr_tag.place(relx=0.04,rely=0.32)
        descr_summary.place(relx=0.04,rely=0.36,relwidth=0.15 )
        d_tag.place(relx=0.04,rely=0.23 )
        d_title.place(relx=0.04,rely=0.27)
        combo_lab.place(relx=0.04,rely=0.41,relwidth=0.1)
        button_send.place(relx=0.04,rely=0.46,relwidth=0.1)
        clear_button.place(relx=0.15,rely=0.46,relwidth=0.07)
        entry_tag.place(relx=0.15,rely=0.41,relwidth=0.07)
        lab_button_close.place(relx=0.2,rely=0.22) 
        
   else:
      Check_raw.set(0)
      stuff_frame.place_forget() 
      descr_tag.place_forget()
      descr_summary.place_forget()
      combo_lab.place_forget()
      clear_button.place_forget()
      d_tag.place_forget()
      d_title.place_forget()
      button_send.place_forget()
      entry_tag.place_forget()
      lab_button_close.place_forget() 
      

lab_button = tk.Button(root, text="Raw Link", font=("Arial",12,"bold"), command=raw_label)
lab_button.place(relx=0.05,rely=0.15)      

lab_button_close = tk.Button(root, text="Close", font=("Arial",12,"bold"), command=raw_label)
     

def add_tag(event):
   hashtag=list_hashtag_fun()
   if hashtag!=[]:
      for hash_one in hashtag:
         if hash_one not in Lab_list:
            Lab_list.append(hash_one)
      combo_lab['values']=Lab_list    
        
Lab_list=["energy","nostr","bitcoin","money","ai"]
combo_lab = ttk.Combobox(root, values=Lab_list,font=('Arial',14,'bold'))
combo_lab.set("Tag")
combo_lab.bind("<<ComboboxSelected>>", add_tag)

def link_share():
   d_tag_show()
   show_descr()
   lists_id=[] 
   
   global d_identifier
   if d_identifier!="":
      
      lists_id.append(Tag.identifier(d_identifier))
      if list_title!=[]:   
         lists_id.append(Tag.title(list_title[0]))
         
         if entry_tag.get()!="":  
            stringa = entry_tag.get()
            list_string_1 = stringa.split(",")
            
            for hash_tag in list_string_1:    
             lists_id.append(Tag.hashtag(hash_tag))
         else:
            pass   

         if __name__ == '__main__':
          lists_id.append(Tag.custom(TagKind.PUBLISHED_AT() , [str( int(time.time()) )]))
          list_content=[""]
          
          test_result,builder =asyncio.run(link_it(lists_id,list_content[0]))
          messagebox.showinfo("Result",str(test_result))
          if messagebox.askokcancel("Authenticate ","Yes/No") == True:
           output =asyncio.run(send_link_it(builder))
           messagebox.showinfo("Result",str(output))
          list_content.clear()
          list_title.clear()
          combo_lab.set("Tag")
          add_tag_str.set("")
          d_identifier=""
          d_title.delete(0, END)
         
button_send=tk.Button(root,text="Speed Link",command=link_share, background="darkgrey",font=("Arial",12,"bold"))      
db_note_list=[]

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
          button_open=Button(root, command=show_noted(tag), text="Open Tag",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
                
        ra=0
        se=1
        #for word in test1:
           #if word in block_hashtag_word:
              #test1.remove(word)
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
   frame3.place(relx=0.01,rely=0.6,relwidth=0.25)      
    
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

def list_hashtag_fun():
    hashtag_list=[]
    if db_note_list!=[]:
        for note_x in db_note_list:
            if tags_string(note_x,"t")!=[]:
                for hash_y in tags_string(note_x,"t"):
                    if hash_y not in hashtag_list:
                        hashtag_list.append(hash_y)
        return hashtag_list       
    else:
       return hashtag_list       

def tags_string(x,obj):
    f=x["tags"]
    z=[]
    
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z     

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f

def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

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
  

entry_channel=StringVar()
hash_list_notes=[]

def search_for_channel(note_hash):
     Notes=db_note_list
     if Notes:
        hash_list_notes.clear()
        for note_x in Notes:
            if note_hash in tags_string(note_x,"t"): 
               hash_list_notes.append(note_x)
        return hash_list_notes      

def second_one_filter():
     second_filter=test_relay()
     if second_filter:
         timeline_created(second_filter)
         print(len(db_note_list))
         button_open.place(relx=0.4,rely=0.02,anchor='n' ) 
         if messagebox.askokcancel("Metadata user!","Yes/No") == True:
            list_pubkey_id()
            show_read()
         else:    
          show_read()
                
def show_read():
   show_noted(db_note_list)

def show_noted(some_list):
  """Widget function \n
   Open feed Horizontal, 3 Row
   """
  frame2=tk.Frame(root)  
  if len(db_note_list)<=3:
     canvas_1 = tk.Canvas(frame2,width=200)
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

  if db_note_list!=[]:
  
   s=1
   s1=0
   se=1         
   db_note_max=[]
   db_note_max=some_list
   
   def show_tag(entry):
      hashtag_list=search_for_channel(entry)
      if hashtag_list:
       show_noted(hashtag_list)
   
   def p_tag_note(entry):
      lenght,note_p=pubkey_id(entry)
      if lenght>1:
         show_noted(note_p)
      
   i=0 
   if len(db_note_list)!=len(db_note_max):
    
    test_1=[]
    for note_x in db_note_max:
     for tags in tags_string(note_x,"t"):
      if tags not in test_1:
       test_1.append(tags)   
         
    if len(test_1)>0:     
     test_1.sort()
        
     button_grid_1=Button(scrollable_frame_1,text=f"{test_1[0]} ", command=lambda val=test_1[0]: show_tag(val),background="grey",font=("Arial",12,"normal"))
     button_grid_1.grid(row=0,column=0,padx=5,pady=5)
     if len(test_1)>1:
      button_grid_2=Button(scrollable_frame_1,text=f"{test_1[1]}", command= lambda val=test_1[1]: show_tag(val),background="grey",font=("Arial",12,"normal"))
      button_grid_2.grid(row=0,column=1,padx=5,pady=5)
     if len(test_1)>2:
      button_grid_3=Button(scrollable_frame_1,text=f"{test_1[2]}", command= lambda val=test_1[2]: show_tag(val),background="grey",font=("Arial",12,"normal"))
      button_grid_3.grid(row=0,column=2,padx=5,pady=5)   
     if len(test_1)>3:
      button_grid_4=Button(scrollable_frame_1,text=f"{test_1[3]}", command= lambda val=test_1[3]: show_tag(val),background="grey",font=("Arial",12,"normal"))
      button_grid_4.grid(row=0,column=3,padx=5,pady=5)    
     if len(test_1)>4:
      button_grid_4=Button(scrollable_frame_1,text=f"{test_1[4]}", command= lambda val=test_1[4]: show_tag(val),background="grey",font=("Arial",12,"normal"))
      button_grid_4.grid(row=0,column=4,padx=5,pady=5)     
              
   for note in db_note_max:   
    
      if i% 3==0:
        s1=0
        se=int(i//3)+i+1
      
      i=i+1    
  
      try:
       if note['pubkey'] in list(Pubkey_Metadata.keys()):
     
             context0="Nickname " +Pubkey_Metadata[note["pubkey"]]
       else: 
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
       button_keep=Button(scrollable_frame_1,text=f"R", command=lambda val=note["pubkey"]: p_tag_note(val))
       button_keep.grid(column=s1+3,row=se,padx=5,pady=5)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=se+1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5,  width=20, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=se+1) 
       
                                          
                                                                                    
                                                                      
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
button_RE=Button(root,command=second_one_filter, text="Relay Note", font=('Arial',12,'normal'))
button_RE.place(relx=0.2,rely=0.1,anchor='n' )  
button_open=Button(root,command=lambda: show_read(), text="Read Note", font=('Arial',12,'normal'))

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

relay_button = tk.Button(root, text="Add Relay!", font=("Arial",12,"normal"),background="grey", command=relay_class)
counter_relay=Label(root,text="",background="darkgrey",font=('Arial',12,'normal'))
add_relay_str=StringVar()
entry_relay=ttk.Entry(root,justify='left',font=("Arial",12,"bold"),width=12,textvariable=add_relay_str)
add_relay_str.set("wss:// ")
entry_relay.place(relx=0.05,rely=0.05)
relay_button.place(relx=0.165,rely=0.05)   

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

async def Get_notes():
    # Init logger
    init_logger(LogLevel.INFO)
    
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
   
    test_kind = await get_kind(client)
    await client.disconnect()
    return test_kind 

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
   if note['pubkey'] in list(Pubkey_Metadata.keys()):
      var_id_3.set("Nickname " +Pubkey_Metadata[note["pubkey"]])
   else:
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
           show_noted(hashtag_list)

        #for word in test1:
        #if word in block_hashtag_word:
        #test1.remove(word)
        test1.sort()
        
        while ra<len(test1):
   
         button_grid1=Button(scrollable_frame_2,text=f"{test1[ra]} ", command=lambda val=test1[ra]: show_tag(val))
         button_grid1.grid(row=s,column=0,padx=5,pady=5)
    
         if len(test1)>se:
            button_grid2=Button(scrollable_frame_2,text=f"{test1[ra+1]}", command= lambda val=test1[ra+1]: show_tag(val))
            button_grid2.grid(row=s,column=1,padx=5,pady=5)
         if len(test1)>ti:
          button_grid3=Button(scrollable_frame_2,text=f"{test1[ra+2]}", command= lambda val=test1[ra+2]: show_tag(val))
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

async def link_it(tag,description):
   
   init_logger(LogLevel.INFO)
   key_string=Keys.generate()
   if key_string!=None: 
    keys =key_string
    builder= EventBuilder(Kind(39701),description).tags(tag)
    test_result_post=builder.build(keys.public_key())
       
    return test_result_post,builder    

async def send_link_it(builder):
   
   key_string=log_these_key()
   if key_string!=None: 
    keys =key_string
    keys = Keys.parse(key_string) 
    signer=NostrSigner.keys(keys)
    client = Client(signer)
    if relay_list!=[]:
     for j_relay in relay_list:
      await client.add_relay(RelayUrl.parse(j_relay))
     await client.connect() 
     test_result_post= await client.send_event_builder(builder)
      
     return test_result_post    

timeline_people=[]
db_list_note_follow=[]
Pubkey_Metadata={}
photo_profile={}

def pubkey_timeline():
   for note in db_note_list:
      if note["pubkey"] not in timeline_people:
         timeline_people.append(note["pubkey"])

def list_pubkey_id():
  pubkey_timeline()
  if timeline_people !=[]:
      
   metadata_note=search_kind(0)
   if metadata_note!=[]:
       for single in metadata_note:
        if single not in db_list_note_follow:
           db_list_note_follow.append(single)
        single_1=json.loads(single["content"])
        try:
         if "name" in list(single_1.keys()):
          if single_1["name"]!="":
                      
           if single["pubkey"] not in list(Pubkey_Metadata.keys()):
              Pubkey_Metadata[single["pubkey"]]=single_1["name"]
              
         else:   
            if "display_name" in list(single_1.keys()):
             if single_1["display_name"]!="":
                                
                if single["pubkey"]not in list(Pubkey_Metadata.keys()):
                  Pubkey_Metadata[single["pubkey"]]=single_1["display_name"]    
         
         if "picture" in list(single_1.keys()):
          if single_1["picture"]!="":
                      
           if single["pubkey"] not in list(photo_profile.keys()):
              if single_1["picture"]!="":
               photo_profile[single["pubkey"]]=single_1["picture"]
                       
                        
        except KeyError as e:
          print("KeyError ",e) 
       print("Profile ",len(Pubkey_Metadata)," Profile with image ",len(photo_profile)) 

button_user=Button(root,text=f"Metadata Users", command=list_pubkey_id,font=("Arial",12,"normal"))
button_user.place(relx=0.05,rely=0.1)

def search_kind(x):
   Zeta=[]
   if __name__ == "__main__":
    # Example usage with a single key
    
    single_results = asyncio.run(feed_cluster([Kind(x)]))
    if single_results:
      
      note=get_note(single_results)
      for r in note:
         if (r)['kind']==x:
            Zeta.append(r)
   return Zeta       

add_relay_list=[]

async def get_note_cluster(client, type_of_event):
    if timeline_people!=[]:
     f = Filter().kinds(type_of_event).authors(user_convert(timeline_people)).limit(1000)
    else:
       f = Filter().kinds(type_of_event).limit(1000)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def feed_cluster(type_of_event):
    # Init logger
   init_logger(LogLevel.INFO)
   
   client = Client(None)
    #uniffi_set_event_loop(asyncio.get_running_loop())
   add_relay_list.clear()
   list_add_relay=["wss://nos.lol/","wss://nostr.mom/","wss://nostr-pub.wellorder.net/"]
   await Search_status(client=Client(None),list_relay_connect=list_add_relay)
   if list_add_relay!=[]:
      for x_relay in list_add_relay:
         if x_relay not in relay_list:
            relay_list.append(x_relay)

   if relay_list!=[]:
      for relay_j in relay_list:
         if RelayUrl.parse(relay_j) not in add_relay_list:
            add_relay_list.append(RelayUrl.parse(relay_j))
            await client.add_relay(RelayUrl.parse(relay_j))         
    
      await client.connect()
      await asyncio.sleep(2.0)

      combined_results = await get_note_cluster(client, type_of_event)
      return combined_results

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
                    
                    if i==1:
                        if stats.bytes_received()>0:  #Auth ort other stuff
                           if str(url) in list_relay_connect:
                            list_relay_connect.remove(str(url))
                            break
                        if stats.success()==0 and relay.is_connected()==False:
                            if str(url) in list_relay_connect:
                                list_relay_connect.remove(str(url))
                        
                    i=i+1 
    except IOError as e:
        print(e) 
    except ValueError as b:
        print(b)                   

def pubkey_id(test):
   note_pubkey=[]
   for note_x in db_note_list:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   return len(note_pubkey),note_pubkey  

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

root.mainloop()     