#Reporter
import asyncio
from nostr_sdk import *
from datetime import timedelta
import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import shutil
import time
import random
import tkinter.font as tkFont

def note_list(list_follow):
    L=[]
    if __name__ == "__main__":
     test_people = list_follow
     combined_results = asyncio.run(main(test_people))
    L=get_note(combined_results)
    return L

def note_user(user):
    if __name__ == "__main__":
     single_author = user  
     L = asyncio.run(main(single_author))
    note=get_note(L)
    return note

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z

def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def search_kind(user,x):
    if __name__ == "__main__":
     # Example usage with a single key
     single_author = user 
     single_results = asyncio.run(main(single_author))
    Z=[]
    note=get_note(single_results)
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

list_event=[1984]

async def get_relays(client, authors):
    f = Filter().authors(authors).kind(Kind(list_event[0])).limit(700)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_relay(client, user):
    f = Filter().author(user).kind(Kind(3))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

senza=int(0)

async def main(authors):
    # Init logger
    global senza
    if senza==0:
      init_logger(LogLevel.INFO)
      senza=int(1) 
    client = Client(None)
    
    # Add relays and connect
    relay_url_1 = RelayUrl.parse("wss://nos.lol/")
    await client.add_relay(relay_url_1)
    relay_url_x = RelayUrl.parse("wss://nostr.mom/")
    await client.add_relay(relay_url_x)
    if relay_list!=[]:
       s=0
       for relay_x in relay_list:
          if s<3:
            relay_url = RelayUrl.parse(relay_x)
            await client.add_relay(relay_url)

          s=s+1 
    await client.connect()
    await asyncio.sleep(1.0)

    if isinstance(authors, list):
        combined_results = await get_relays(client, authors)
    else:
        combined_results = await get_relay(client, authors)
    
    return combined_results

root = tk.Tk()
root.title("test link")
root.geometry("1250x800")
frame_top_box=tk.Frame(root,height=30,width=200,background="darkgrey")
frame2=tk.Frame(root,height=60,width=110)
timeline_people=[]

def list_people_fun():
    people_list=[]
    if db_list!=[]:
        for note_x in db_list:
            if note_x["pubkey"] not in people_list:
                        people_list.append(note_x["pubkey"])
            if note_x["pubkey"] not in timeline_people:
                        timeline_people.append(note_x["pubkey"])    
        return people_list       
    else:
       return people_list

def print_people(): 
   if db_list!=[]:  
    show_people()
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=270)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    s=1     
    
    test1=list_people_fun()
    ra=0
    sz=0
    labeL_button=Label(scrollable_frame,text="Number of pubkey "+str(len(test1)))
    labeL_button.grid(row=0,column=0,padx=5,pady=5,columnspan=3)           
    while ra<len(test1):
                lenght,note_p=pubkey_id(test1[ra])
                if lenght>1:
                 sz=sz+1   
                 if test1[ra] in list(Pubkey_Metadata.keys()):
                    button_grid1=Label(scrollable_frame,text=f"{Pubkey_Metadata[test1[ra]]} note {lenght}",width=20)
                 else:
                    button_grid1=Label(scrollable_frame,text=f"{test1[ra][0:9]} note {lenght}",width=20)
                 button_grid1.grid(row=s,column=0,padx=2,pady=5)
                 button_grid2=Button(scrollable_frame,text=f"Reports", command= lambda val=note_p: show_lst_ntd(val))
                 button_grid2.grid(row=s,column=2,padx=2,pady=5) 
            
                 root.update()  
              
                s=s+1
            
                ra=ra+1   
    labeL_button.config(text="Number of pubkey "+str(len(test1))+"  "+"\n"+"Number of poster more than one note "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
    button_people_2.place(relx=0.15,rely=0.65) 
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.1,rely=0.3,relwidth=0.3, relheight=0.3)      

    def Close_print():
       frame3.destroy()  
       button_people_2.place_forget()
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

Pubkey_Metadata={}
photo_profile={}
db_list_note_follow=[]
timeline_people=[]

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
       if note['pubkey'] in list(Pubkey_Metadata.keys()):
         
         context0="Nickname " +Pubkey_Metadata[note["pubkey"]]
       else: 
         context0="Author: "+note['pubkey']
       context0=context0+"\n"+"Time: "+str(round(float(int(time.time())-note["created_at"])/(86400),3))+str(" Days")  
       context1=note['content']+"\n"
       context2=" "
       if note['tags']!=[]: 
        context2=""   
        if tags_string(note,"alt")!=[]:
              for F_note in tags_str(note,"alt"):
                   
                  context2=context2+str( F_note )+"\n"
              
        for xnote in tags_str(note,"p"):
         context2=context2+"\n"+str(xnote) +"\n"
       
        if tags_string(note,"e")!=None and tags_string(note,"e")!=[] :
           s=0
           for xnote in tags_str(note,"e"):
            if s<5:
             context2=context2+str(xnote) +"\n"
            s=s+1
        
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=1) 
      
       def print_id(entry):
            if entry["tags"]!=[]:
              print(db_list.index(entry)+1)
              print(entry["tags"])   
                  
       def print_var(entry):
                print(entry)
                print(str(round(float((time.time()-float(entry["created_at"]))/86400),3)), " days")

           
       button=Button(scrollable_frame_1,text=f"Print note", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
       button_grid2.grid(row=2,column=s1+1,padx=5,pady=5)    
       
       s=s+2  
       s1=s1+4
      except TypeError as e:
         print(e)
      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

  scrollbar_1.pack(side="bottom", fill="x",padx=20)
  scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
  canvas_1.pack( fill="y", expand=True)
  frame2.place(relx=0.63,rely=0.5,relwidth=0.32,relheight=0.31)

  def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
  button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
  button_frame.place(relx=0.74,rely=0.83,relwidth=0.1)   
   
test_note=[]
list_note_read=[]

def pubkey_id(test):
   note_pubkey=[]
   for note_x in db_list:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   return len(note_pubkey),note_pubkey   

def pubkey_rep(test):
   note_pubkey=[]
   for note_x in db_list:
       if tags_string(note_x,"p")!=[]:
        if tags_string(note_x,"p")[0] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   return len(note_pubkey),note_pubkey  

button_people_=tk.Button(root,text="List of People",command=print_people, font=('Arial',12,'bold'))
button_people_.place(relx=0.25,rely=0.25) 

my_dict = {"Pablo": "fa984bd7dbb282f07e16e7ae87b26a2a7b9b90b7246a44771f0cf5ae58018f52", 
           "jb55": "32e1827635450ebb3c5a7d12c1f8e7b2b514439ac10a67eef3d9fd9c5c68e245",
             "Vitor": "460c25e682fda7832b52d1f22d3d22b3176d972f60dcdc3212ed8c92ef85065c", 
             "Hodlbod": "97c70a44366a6535c145b333f973ea86dfdc2d7a99da618c40c64705ad98e322", 
             "il_lost_": "592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"}

my_list = list(my_dict.values())
my_name = list(my_dict.keys())
def on_select(event):
    selected_item = combo_box.get()
    label.config(text="Selected Item: " + my_dict[selected_item][0:9])

label = tk.Label(frame_top_box, text="Selected Item: ",font=("Arial",10,"bold"),width=20)
label.grid(row=1, column=5, columnspan=2,pady=5,padx=5 )
combo_box = ttk.Combobox(frame_top_box, values=["Pablo","jb55","Vitor","Hodlbod","il_lost_"],font=("Arial",10,"bold"))
combo_box.grid(row=0, column=5,columnspan=2, pady=5 )
combo_box.set("Option 1")
combo_box.bind("<<ComboboxSelected>>", on_select)
stringa=tk.IntVar()
select_kind=Label(frame_top_box,text="Reports", font=("Arial",20,"bold"),background="lightgrey")
select_kind.grid(column=2, row=0,padx=10,columnspan=2,rowspan=2,pady=10)

def search_event(): 
 if combo_box.get()!="Option 1":
  user=convert_user(my_dict[combo_box.get()])
  z=search_kind(user,3)
  if z!=[]:
   people=tags_string(z[0],'p')
   User=user_convert(people)
   tm=note_list(User)
   return tm

def search_():
   result=search_event()
   if result !=None:
    timeline_created(db_list,result)
     
    print_text()

frame1=tk.Frame(root,height=100,width=200)
button_tm=tk.Button(frame_top_box,command= search_,text="View note", font=("Arial",10,"bold"))
button_tm.grid(column=8, row=1,padx=5,pady=5)
db_link=[]
db_list=[]

def show_people():
     people_list=list_people_fun()
    
     for item in people_list:
      if item not in db_link:
       db_link.append(item)

frame3=tk.Frame(root,height=120,width= 100)
frame1=tk.Frame(root,height=100,width=200)
frame_top_box.grid(column=0,row=0,padx=5,rowspan=2,columnspan=4)
frame1.grid()
frame3.grid()

def add_db_list():
        button_block.grid_forget()
        Frame_block=Frame(root, height=30,width=200, background="darkgrey")
                
        def Close_block(event):
            Frame_block.place_forget()
            button_block.grid(column=9, columnspan=2, row=0, pady=5,padx=10) 
         
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',10,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=17, row=0, padx=5, columnspan=1) 
        
        def search_block_list():
            label_string_block1.set(len(db_list))    

        def delete_block_list():
            db_list.clear()
            label_string_block1.set(len(db_list))   

        def link_count():
            label_link_var.set(len(db_link))

        def clear_db_link():
            db_link.clear()
            label_link_var.set(len(db_link))   
                   
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey")
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ")
        random_block1.grid(column=1,row=0,padx=5,pady=5)
        clear_link=Button(Frame_block, command=clear_db_link, text= "Clear List: ",background="darkgrey")
        clear_link.grid(column=0,row=1,padx=5,pady=5)    
        random_count=Button(Frame_block, command=link_count, text= "Reporter: ")
        random_count.grid(column=1,row=1,padx=5,pady=5)
        label_string_block1=StringVar()
        label_link_var=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1)
        label_block_list1.grid(column=2,row=0,padx=5,pady=5)
        label_var_list1=Label(Frame_block, textvariable=label_link_var)
        label_var_list1.grid(column=2,row=1,padx=5,pady=5)
        
        Frame_block.place(relx=0.32,rely=0,relwidth=0.2,relheight=0.095)
        
button_block=tk.Button(root, highlightcolor='WHITE',
                  text='DB count',
                  font=("Arial",10,"bold"),
                  command=add_db_list)
button_block.grid(column=9, columnspan=2, row=0, pady=5,padx=10) 
frame2.place(relx=0.65,rely=0.15,relwidth=0.2,relheight=0.3)

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
 if db_list!=[]:
   
   s=1
   if List_note_out==[]:
      value=0
   else:   
    value=len(List_note_out)
   if value+50<len(db_list):
    for note in db_list[value:value+50]:
     if note not in List_note_out:
        List_note_out.append(note)
     try:
      if note['pubkey'] in list(Pubkey_Metadata.keys()):
         context0="Nickname "+Pubkey_Metadata[note['pubkey']]+"\n"+"id: "+note["id"]
      else:
         context0="Pubkey "+note['pubkey']+"\n"+"id: "+note["id"]
      if note['tags']!=[]:
        context1=note['content']+ "Time: "+str(int(float(int(time.time())-note["created_at"])/(86400)))+str(" Days") 
        context2="\n"+" [  [ Tags ] ] "+"\n"
        for xnote in note["tags"]:
         context2=context2+str(xnote) +"\n"
      else: 
        context1=note['content']
        context2=""
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0)
      label_id.grid(pady=2,column=0, columnspan=3,row=s)
      scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
      scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
      second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
      second_label10.insert(END,context1+str(context2))
      scroll_bar_mini.config( command = second_label10.yview )
      second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
      
      def print_id(entry):
           number=list(db_list).index(entry)
           print(number)
                  
      def print_var(entry):
                print(entry)
           
      button=Button(scrollable_frame_1,text=f"Note", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s+2,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"Number note", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s+2,column=1,padx=5,pady=5)      
      s=s+3  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.44,rely=0.35,relwidth=0.30,relheight=0.4)

    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()

    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.5,rely=0.78,relwidth=0.1)      
   
button_read=Button(root,text="Stamp Note", command=show_Teed,font=("Arial",12,"normal"))
button_read.place(relx=0.15, rely=0.25)
label_combo_link=StringVar()      
entry_label_theme=tk.Entry(root, textvariable=label_combo_link)    
label_entry_theme=Label(root,text="label")
report_manual={}

def show_note_link(note):
 frame2=tk.Frame(root)  
 canvas_1 = tk.Canvas(frame2)
 scrollbar_1 = ttk.Scrollbar(frame2, orient="vertical", command=canvas_1.yview)
 scrollable_frame_1 = ttk.Frame(canvas_1)
 label_entry_theme.place(relx=0.78,rely=0.65)
 entry_label_theme.place(relx=0.76,rely=0.7)  
 scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all")))

 canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
 canvas_1.configure(yscrollcommand=scrollbar_1.set)
 if db_list!=[]:
    s=1
    try:
      if note['pubkey'] in list(Pubkey_Metadata.keys()):
          context0="Nickname "+Pubkey_Metadata[note['pubkey']]+"\n"+"id: "+note["id"]+"\n"
      else:
       context0="Pubkey "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
      if note['tags']!=[]:
        context1=note['content']+"Time: "+str(int(float(int(time.time())-note["created_at"])/(86400)))+str(" Days") 
        context2="\n"+" [ [ Tags ]  ] "+"\n"
        for xnote in note["tags"]:
         context2=context2+str(xnote) +"\n"
      else: 
        context1=note['content']
        context2=""
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0)
      label_id.grid(pady=2,column=0, columnspan=3,row=s)
      scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
      scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
      second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
      second_label10.insert(END,context1+"\n"+str(context2))
      scroll_bar_mini.config( command = second_label10.yview )
      second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 

      def print_id(entry):
           number=list(db_list).index(entry)
           print(number)

      def write_the_file(entry):
         if entry_label_theme.get()!="": 
          name_label=entry_label_theme.get()
          report_manual[entry["id"]]=name_label 
          print(len(report_manual))
                  
      def print_var(entry):
                print(entry)
                              
      button=Button(scrollable_frame_1,text=f"Note", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s+2,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"number note", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s+2,column=1,padx=5,pady=5)      
      button_grid3=Button(scrollable_frame_1,text=f"label it", command=lambda val=note: write_the_file(val))
      button_grid3.grid(row=s+2,column=2,padx=5,pady=5)  
      
      s=s+3  

    except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.41,rely=0.35,relwidth=0.30,relheight=0.4)
    
    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
        label_entry_theme.place_forget()
        entry_label_theme.place_forget() 

    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.5,rely=0.78,relwidth=0.1)      

def show_one_note(note):
    if note in db_list:
        show_note_link(note)
                             
List_note_out=[]

def print_text():  
    
    frame3=tk.Frame(root,height=120,width= 400)
    canvas = tk.Canvas(frame3,width=390)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    s=1    
    if db_list!=[]: 
     print(len(db_list))
     for note in db_list[0:100]:
         try:   
            var_time =StringVar()
            Message_time= Message(scrollable_frame, textvariable=var_time, width=350,font=('Arial',12,'normal'))
            var_time.set("Time: "+str(round(float(int(time.time())-note["created_at"])/(86400),3))+str(" Days") )
            Message_time.grid(row=s, column=0, columnspan=2, padx=50, pady=5,sticky="w")
            var_id=StringVar()
            label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=370)
            label_id.grid(pady=10,column=0,columnspan=2,row=s+1)
            var_id.set(str("Alt "+str(tags_str(note,"alt"))))
            var_id_tag=StringVar()
            label_tag = Message(scrollable_frame,textvariable=var_id_tag, relief=RAISED,width=370)
            label_tag.grid(pady=10,column=0,columnspan=3,row=s+2)
            if tags_str(note,"p")!=[] and tags_str(note,"p")!=None:
             test_p=""
             for p_x  in tags_str(note,"p"):
              if len(p_x)>2:
                if p_x[1] in list(Pubkey_report.keys()):
                 test_p =str(test_p) +str(p_x[0])+str(" "+Pubkey_report[p_x[1]])+str(" "+p_x[2]) +"\n"
                else:
                   test_p =str(test_p) +str(p_x[0])+str(" "+p_x[1])+str(" "+p_x[2]) +"\n"
              else:
                if p_x[1] in list(Pubkey_report.keys()):
                  test_p =str(test_p) +str(p_x[0])+str(" "+Pubkey_report[p_x[1]])+"\n"   
                else:
                   test_p =str(test_p) +str(p_x[0])+str(" "+p_x[1])+"\n"   
             var_id_tag.set(str(test_p)) 

            def print_id(test):
                if tags_string(test,"p")!=[]:
                   search_pubey=str(tags_string(test,"p")[0])
                   string_person.set(search_pubey)
                            
            def print_var(test):
                print(test)
            
            button=Button(scrollable_frame,text=f"print", command=lambda val=note: print_var(val))
            button.grid(column=0,row=s+3,padx=5,pady=10)
            button_grid2=Button(scrollable_frame,text=f"Search pubkey Reported", command=lambda val=note: print_id(val))
            button_grid2.grid(row=s+3,column=1,padx=5,pady=10)
            button_grid3=Button(scrollable_frame,text="Open Note", command=lambda val=note: show_one_note(val))
            button_grid3.grid(row=s+3,column=2,padx=5,pady=10)
                                                                                                             
            root.update()  
            s=s+4
         except TypeError as e:
            print(e)
     canvas.pack(side="left", fill="y", expand=True)
     scrollbar.pack(side="right", fill="y")  
     frame3.place(relx=0.01,rely=0.35,relwidth=0.4)      
    
     def Close_print():
       frame3.destroy()  

     button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
     button_close_.pack(pady=5,padx=5) 

button4=tk.Button(root,text="View Note Report",command=print_text, font=("Arial",12,"normal"))
button4.place(relx=0.02, rely=0.25) 
frame1.grid()
relay_list=[]

def open_relay():
    frame_account=tk.Frame(root, background="darkgrey")
    structure_relay = tk.Label(frame_account, text="relay",font=("Arial",12,"bold"))
    entry_relay=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"),width=10)
    structure_relay.grid(column=11, row=1, padx=5,pady=5) 
    button_beau.place_forget()
    
    def relay_class():
     if entry_relay.get()!="":
        if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/":
           
            if entry_relay.get() not in relay_list:
                relay_list.append(entry_relay.get())
                
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=0)
            entry_relay.delete(0, END)
            combo_bo_r['value']=relay_list
            
            return relay_list  
     else:
       if relay_list!=[]:  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=0)
          combo_bo_r['value']=relay_list
           
       else:
          upload_relay_list("relay")  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=0)
          combo_bo_r['value']=relay_list

    def remove_one_relay():
     if combo_bo_r.get()!="":
        if combo_bo_r.get() in relay_list:
            number=relay_list.index(combo_bo_r.get())
            relay_list.pop(number)
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=0)
            combo_bo_r['value']=relay_list
            return relay_list  
     else:
       if relay_list!=[]:  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=0)
          combo_bo_r['value']=relay_list
           
       else:
          upload_relay_list("relay")  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=0)
          combo_bo_r['value']=relay_list        

    relay_button = tk.Button(frame_account, text="Check ", font=("Arial",12,"normal"),background="grey", command=relay_class)
    counter_relay=Label(frame_account,text="count",font=("Arial",12,"normal"))
    entry_relay.grid(column=12, row=1, padx=10,pady=5)
    relay_button.grid(column=13, row=1, padx=5,pady=5)
    relay_d_button = tk.Button(frame_account, text="Remove [R]", font=("Arial",12,"normal"),background="grey", command=remove_one_relay)
    relay_d_button.grid(column=13, row=2, padx=10,pady=5)

    def Close_profile(event):
       frame_account.destroy()
       
       button_beau.place(relx=0.55,rely=0.02) 
        
    button_close=tk.Button(frame_account, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=0, padx=5,pady=5) 

    def on_server(event):
       label_relay["text"] = combo_bo_r.get()[6:16]
       
    label_relay = tk.Label(frame_account, text="Name relay",font=('Arial',12,'bold'))
    label_relay.grid(column=11,row=2,pady=5,padx=5)
    combo_bo_r = ttk.Combobox(frame_account, font=('Arial',12,'normal'),width=10)
    combo_bo_r.grid(column=12,row=2,pady=5)
    combo_bo_r.set("Relays set")
    combo_bo_r.bind("<<ComboboxSelected>>", on_server)
    frame_account.place(relx=0.53,rely=0.001,relheight=0.18,relwidth=0.28)

button_beau=tk.Button(root, highlightcolor='WHITE',text='Relay',font=('Arial',12,'bold'),command=open_relay )
button_beau.place(relx=0.55,rely=0.02) 

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


def list_pubkey_id():
   
  if timeline_people !=[]:
   test_people=user_convert(timeline_people)    #not cover people are alre
   print("ready")
   list_event.clear()
   list_event.append(0)
   metadata_note=search_kind(test_people,0)
   if metadata_note!=[]:
     try:  
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
     except json.decoder.JSONDecodeError as e:
        print(e,single)  

button_people_2=Button(root,text=f"Metadata Reporter ", command=list_pubkey_id,font=('Arial',12,'bold'))

async def get_relays_z(client, authors):
    f = Filter().authors(authors).kind(Kind(0))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_relay_z(client, user):
    f = Filter().author(user).kind(Kind(0))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def feed(authors):
      
    client = Client(None)
    
    # Add relays and connect
    relay_url_1 = RelayUrl.parse("wss://nos.lol/")
    relay_url_2 = RelayUrl.parse("wss://relay.damus.io/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    
    if relay_list!=[]:
       
       for jrelay in relay_list:
        relay_url = RelayUrl.parse(jrelay)
        await client.add_relay(relay_url)
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_relays_z(client, authors)
    else:
        combined_results = await get_relay_z(client, authors)
    await client.disconnect()
    return combined_results    

def show_print_test_tag():
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
              
   def print_var():
    pass
   
   def print_content_2(filter_string):
    s=1
    z=7
    
    for key,value in report_ID2_stem.items():
       report=""
       if value=="Report for "+ filter_string:
         for note in db_list:
          if note["id"]==key:
            
            zeta,number=count_rect2(value)
            
            if s<=number and s<150:
             report=report + "Note " +str(s)+"\n"+ str(zeta) +"\n"
             if tags_string(note,"p")!=[]:
               if tags_string(note,"p")[0] in list(Pubkey_report.keys()):
                report= report +"Person " +Pubkey_report[tags_string(note,"p")[0]] +"\n" 
               else:
                  report= report +"Person " +str(tags_string(note,"p")[0]) +"\n" 

              
             if tags_string(note,"e")!=[]: 
              report=report+"Event "+str(tags_string(note,"e"))+"\n"
             s=s+1  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             var_id_r.set("Report for "+filter_string)                                
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             second_label10_r.insert(END,report+"\n")
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
             button_grid_4=Button(scrollable_frame_2,text=f"Open Report ", command=lambda val=note: show_one_note(val))
             button_grid_4.grid(row=z+2,column=0,padx=5,pady=5)    
             z=z+3
       root.update_idletasks()
 
   def print_content(filter_string):
       s=1
       z=7
       
       for key,value in report_ID_stem.items():
          report=""
          if value=="Report for "+ filter_string:
            for note in db_list:
             if note["id"]==key:
               zeta,number=count_rect(value)
               
               if s<number and s<150:
                report=report + "Note " +str(s)+"\n"+ str(tags_string(note,"alt")[0]) +"\n" "Person " +str(tags_string(note,"p")[0]) +"\n" "Event "+str(tags_string(note,"e"))+"\n"
                s=s+1  
                var_id_r=StringVar()
                label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
                label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
                var_id_r.set("Report for "+filter_string)                                
                scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
                scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
                second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
                second_label10_r.insert(END,report+"\n")
                scroll_bar_mini_r.config( command = second_label10_r.yview )
                second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
                button_grid_4=Button(scrollable_frame_2,text=f"Open Report ", command=lambda val=note: show_one_note(val))
                button_grid_4.grid(row=z+2,column=0,padx=5,pady=5)    
                z=z+3
          root.update_idletasks()

      
   button_grid3=Button(scrollable_frame_2,text=f"Read Report ", command=lambda: print_content(entry_rep.get()))
   button_grid3.grid(row=s+2,column=0,padx=5,pady=5)    
   button_grid4=Button(scrollable_frame_2,text=f"Read Report Time", command=lambda: print_content_2(entry_rep.get()))
   button_grid4.grid(row=s+2,column=1,padx=5,pady=5)    

   scrollbar_2.pack(side="right", fill="y",padx=2,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     button_frame.place_forget()
     frame3.destroy()    
         
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.63,rely=0.25) 
   button_frame_s=Button(scrollable_frame_2,command=search_type,text="Create Report",font=("Arial",12,"normal"))
   button_frame_s.grid(row=s+3,column=0,padx=5,pady=5)
   entry_rep_2 = Entry(scrollable_frame_2, textvariable=string_value)
   button_frame_s2=Button(scrollable_frame_2,command=search_report_time ,text="Report Time",font=("Arial",12,"normal"))
   button_frame_s2.grid(row=s+5,column=0,padx=5,pady=5)              
   entry_rep = Entry(scrollable_frame_2, textvariable=string_report)
  
   button_frame_s=Button(scrollable_frame_2,command=lambda:count_report(entry_rep.get()),text="Report for Type",font=("Arial",12,"normal"))
   button_frame_s.grid(row=s+4,column=0,padx=5,pady=5)                
   entry_rep.grid(row=s+4,column=1,padx=5,pady=5)
   entry_rep_2.grid(row=s+5,column=1,padx=5,pady=5)
   frame3.place(relx=0.72,rely=0.25,relheight=0.38,relwidth=0.28) 

button_frame=Button(root,command=show_print_test_tag,text="Report List",font=("Arial",12,"normal"))
button_frame.place(relx=0.75,rely=0.25) 

def timeline_created(db_list,list_new):
  new_note=[] 
  if db_list!=[]:
   for new_x in list_new:
     if new_x not in db_list:
        new_note.append(new_x) 
   i=0
    
   while i<len(new_note):
     j=0
     while j< len(db_list): 
      if db_list[j]["created_at"]>(new_note[i]["created_at"]):
         j=j+1
      else:
         db_list.insert(j,new_note[i])
         break
     i=i+1
   return db_list   
  else:
        for list_x in list_new:
            db_list.append(list_x)
        return db_list     

result_p_stem={}
result_e_stem={}
report_ID_stem={}

def search_type():
   if db_list!=[]:
      s=0
      for note in db_list:
         
         if note["tags"]!=[]:
          if tags_string(note,"alt")!=[]: 
           if tags_string(note,"p")!=[] or tags_string(note,"e")!=[]:
                           result_p_stem[s]=tags_string(note,"alt")[0]
                           report_ID_stem[note["id"]]=tags_string(note,"alt")[0]
                           if tags_string(note,"p")!=[]:
                            result_e_stem[tags_string(note,"p")[0]]=tags_string(note,"alt")[0]
         s=s+1
               
def search_report_time():
   if db_list!=[]:
      value=string_value.get()
      s=0
      print("1")
      for note in db_list:
        select=str("")
        select1=str("")
        if (time.time()-float(note["created_at"]))<float(value*86400):
          
          if tags_string(note,"p")!=[] or tags_string(note,"e")!=[]:
                if tags_string(note,"alt")!=[]:  
                          
                           if tags_string(note,"alt")[0]!="":
                            result_p2_stem[s]=tags_string(note,"alt")[0]
                            report_ID2_stem[note["id"]]=tags_string(note,"alt")[0]
                            if tags_string(note,"p")!=[]:
                             result_e2_stem[tags_string(note,"p")[0]]=tags_string(note,"alt")[0]
                           else:
                              if len(four_tags(note,"p"))>2:
                                select1=four_tags(note,"p")[2]
                              else:
                                if len(four_tags(note,"e"))>2:
                                  select1=four_tags(note,"e")[2]    
                              if select1!="":    
                                result_p2_stem[s]="Report for "+str(select1)  
                                report_ID2_stem[note["id"]]="Report for "+str(select1)  
                                if tags_string(note,"p")!=[]:
                                 result_e2_stem[tags_string(note,"p")[0]]="Report for "+str(select1)  
                else:
                    
                    if len(four_tags(note,"p"))>2:
                      
                      select=four_tags(note,"p")[2]
                    else:
                      if len(four_tags(note,"e"))>2:
                          select=four_tags(note,"e")[2]  
                    if select!="": 
                        result_p2_stem[s]="Report for "+str(select)  
                        report_ID2_stem[note["id"]]="Report for "+str(select)  
                        if tags_string(note,"p")!=[]:
                         result_e2_stem[tags_string(note,"p")[0]]="Report for "+str(select)  
                      
        s=s+1  
      print(result_e2_stem)               

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        
        if len(jtags)>2:
          for xtags in jtags:
            tags_list.append(xtags)
          
   return tags_list 

list_report=[]
result_p2_stem={}
report_ID2_stem={}
result_e2_stem={}


def count_report(type_ofreport):
  if result_p_stem !={}:
   if type_ofreport!="":
    values_list=list(result_p_stem.values())
    global list_report
    list_report.clear()
    for key,value in result_e_stem.items():
       if value==type_ofreport:
          if key not in list_report:
           list_report.append(key)
     
    number=values_list.count(type_ofreport)      
    print(type_ofreport,number)
    string_report.set("")

def count_rect(type_ofreport):
  if result_p_stem !={}:
   if type_ofreport!="":
    values_list=list(result_p_stem.values())
    global list_report
    list_report.clear()
    for key,value in result_e_stem.items():
       if value==type_ofreport:
          if key not in list_report:
           list_report.append(key)
     
    number=values_list.count(type_ofreport)      
    return(type_ofreport,number)

def count_rect2(type_ofreport):
  if result_p2_stem !={}:
   if type_ofreport!="":
    values_list=list(result_p2_stem.values())
    global list_report
    list_report.clear()
    for key,value in result_e2_stem.items():
       if value==type_ofreport:
          if key not in list_report:
           list_report.append(key)
     
    number=values_list.count(type_ofreport)      
    return(type_ofreport,number)

string_report=StringVar()
string_value=IntVar(root,7)

def Notebook_():
 notebook = ttk.Notebook(root)
 notebook.place(relx=0.33,rely=0.1,relheight=0.375)

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
 note=result_e_stem

 if note!= None:

  treeview = ttk.Treeview(frame2, columns=("Value"),height=8)
  level_0 = treeview.insert("", tk.END, text="TEST")
 
  for key,value in note.items():
     treeview.insert(level_0, tk.END,text=str(key))
     
     treeview.insert(level_0 , tk.END,text=value+" \n",values="\n") 
    
  v_scrollbar = Scrollbar(frame2, orient=VERTICAL, command=treeview.yview)
  treeview.configure(yscrollcommand=v_scrollbar.set)
  v_scrollbar.grid(column=2,row=0,rowspan=3,ipady=60)  
  treeview.grid(column=0,columnspan=2,row=0,rowspan=3,pady=10,padx=15)
  frame2.pack(fill='both', expand=True)
 
 notebook.add(frame1, text='General Information')
 notebook.add(frame2, text='Profile',padding=20)
 
 #-------------------3---------------------------
 
 def select_filter(event):
   selcted_item=combo_filter.get()
   report="Report for "+selcted_item
   test1, test2=count_rect(report)
   text_lab.config(text=report)
   text_filter.config(text=test1+" "+str(test2))

 text_lab=Label(frame_3,text="",font=entry_font)
 text_lab.grid(column=0,row=2,columnspan=3)
 text_filter=Label(frame_3,text="",font=entry_font)
 text_filter.grid(column=0,row=3,columnspan=3)
 list_filter=["SPAM","NUDITY","IMPERSONATION","PROFANITY","MALWARE","ILLEGAL"]
 combo_filter = ttk.Combobox(frame_3, values=list_filter,font=entry_font,width=25)
 combo_filter.grid(column=0,row=1,pady=1,padx=10)
 combo_filter.set("Report for")
 combo_filter.bind("<<ComboboxSelected>>", select_filter)


 notebook.add(frame_3, text='Report list',padding=20)
 
#----------------4-----------------------------

 
 def Update():
    report=""
    s=1
    for key,value in report_ID_stem.items():
            
     if value=="Report for "+ combo_filter.get():
      for note in db_list:
         if note["id"]==key:
          report=report + "Note " +str(s)+"\n"+ str(tags_string(note,"alt")[0]) +"\n" "Person " +str(tags_string(note,"p")[0]) +"\n" "Event "+str(tags_string(note,"e"))+"\n"
          s=s+1  
      note_lab_3.insert(END,str(report))
      
 button_up=Button(frame_4,text="Up",command=Update, border=1,highlightbackground="white",background="#e6e9ea")
 button_up.grid(column=4,row=2)  
 note_lab_3=Text(frame_4,width=30,heigh=13)
 v_scrollbar3 = ttk.Scrollbar(frame_4, orient=VERTICAL, command=note_lab_3.yview)
 v_scrollbar3.grid(column=3,row=0,pady=10,ipady=40) 
 note_lab_3.grid(column=0,row=0,columnspan=3,pady=2,padx=4)
 note_lab_3.configure(yscrollcommand=v_scrollbar3.set,height=8)
 frame_4.pack(fill='both', expand=True)    
 notebook.add(frame_4, text="Other Profile", padding=20)

 def close_n():
    notebook.place_forget()
    button_close.place_forget()
 
 button_close=Button(root,text="x Close",command=close_n, border=1,highlightbackground="white",background="#e6e9ea")
 button_close.place(relx=0.64,rely=0.1,relheight=0.029)

 #--------------5-------------------------
     
 string_p=StringVar()
 note_entry_2=Entry(frame_5,width=50,textvariable=string_p)
 note_entry_2.grid(column=0,row=1,pady=2,padx=4)
 list_pubkey=[]

 def search_pubkey_report(pubkey):
    
    if len(pubkey)==64 or len(pubkey)==63:
       
       list_pubkey.append(convert_user(pubkey))
       string_p.set("")
       test_result=asyncio.run(main_report(list_pubkey))
       if test_result:
        result_note=get_note(test_result)
        timeline_created(db_list,result_note)
        result_note=search_pubkey_list(pubkey)
        if result_note!=[]:
          note_Label_2.config(text="number note "+str(len(result_note)))
       else:
        print(len(pubkey))   

 note_Label_2=Label(frame_5,text="")
 note_Label_2.grid(column=0,row=2,pady=2,padx=4)   
 button_up1=Button(frame_5,text="search 2",command=lambda: search_pubkey_report(note_entry_2.get()), border=1,highlightbackground="white",background="#e6e9ea")
 button_up1.grid(column=4,row=2)  
 #search_pubkey_report
 frame_5.pack(fill='both', expand=True)
 notebook.add(frame_5, text="Search Pubkey",padding=20 )
 
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

frame_menu=Frame(root,width=20,height=1)
menu = Menu(frame_menu)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Settings", command=Notebook_)
frame_menu.grid(columnspan=5,rowspan=1)

def search_pubkey_list(pubkey):
   
      list_note_p=[]
      for db_note in db_list:
         if pubkey in tags_string(db_note,"p"):
            list_note_p.append(db_note)
      return list_note_p      

def search_p_db_list():
      list_note_tag_p=[]
      for db_note in db_list:
         if tags_string(db_note,"p")!=[]:
            if tags_string(db_note,"p")[0] not in list_note_tag_p:
              list_note_tag_p.append(tags_string(db_note,"p")[0])
      return list_note_tag_p      

async def search_relays_report(client, authors):
   f = Filter().pubkeys(authors).kind(Kind(1984)).limit(700)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   return z

async def main_report(authors):
   # Init logger
   init_logger(LogLevel.INFO)
   
   client = Client(None)
   
   # Add relays and connect
   relay_url_1 = RelayUrl.parse("wss://nos.lol/")
   await client.add_relay(relay_url_1)
   relay_url_x = RelayUrl.parse("wss://nostr.mom/")
   await client.add_relay(relay_url_x)
   if relay_list!=[]:
      s=0
      for relay_x in relay_list:
         if s<3:
           relay_url = RelayUrl.parse(relay_x)
           await client.add_relay(relay_url)
         s=s+1 
   await client.connect()
   await asyncio.sleep(1.0)
   if isinstance(authors, list):
       combined_results = await  search_relays_report(client, authors)
       return combined_results

string_person=StringVar()
frame_search=Frame(root)
note_entry_2d=Entry(frame_search,width=30,textvariable=string_person)
note_entry_2d.grid(column=0,row=3,pady=2,padx=4)
list_pubkey_rep=[]

def search_pubkey_reported(pubkey):
  if note_entry_2d.get()!="":
   if len(pubkey)==64 or len(pubkey):
      list_pubkey_rep.append(convert_user(pubkey))
      string_person.set("")
      test_result=asyncio.run(main_report(list_pubkey_rep))
      if test_result:
       result_note=get_note(test_result)
       timeline_created(db_list,result_note)
       result_note=search_pubkey_list(pubkey)
       if result_note!=[]:
         note_Label_2d.grid(column=5,row=3,pady=2,padx=4)  
         note_Label_2d.config(text="number note "+str(len(result_note)))
         print_tag(pubkey)
      else:
       print(len(pubkey))   
  else:
       people=search_p_db_list()
       if people!=[]:
          list_pubkey_p(people)
          print(len(Pubkey_report))
         
note_Label_2d=Label(frame_search,text="")
#note_Label_2d.grid(column=5,row=3,pady=2,padx=4)   
button_up1=Button(frame_search,text="Search Pubkey",command=lambda: search_pubkey_reported(note_entry_2d.get()), border=1,highlightbackground="white",background="#e6e9ea")
button_up1.grid(column=4,row=3,padx=2) 
frame_search.place(relx=0.02,rely=0.12,relwidth=0.3,relheight=0.12)
db_list_note_report=[]
Pubkey_report={}

def list_pubkey_p(list_people):
   
  if list_people !=[]:
   test_people=user_convert(list_people)    #not cover people are alre
   list_event.clear()
   list_event.append(0)
   metadata_note=search_kind(test_people,0)
   if metadata_note!=[]:
    
       for single in metadata_note:
        if single not in db_list_note_report:
           db_list_note_report.append(single)
        single_1=json.loads(single["content"])
      
        if "name" in list(single_1.keys()):
          if single_1["name"]!="":
                      
           if single["pubkey"] not in list(Pubkey_report.keys()):
              Pubkey_report[single["pubkey"]]=single_1["name"]
              
        else:   
            if "display_name" in list(single_1.keys()):
             if single_1["display_name"]!="":
                                
                if single["pubkey"]not in list(Pubkey_report.keys()):
                  Pubkey_report[single["pubkey"]]=single_1["display_name"]    

topology=[]
topology_note=[]

def search_for_report(note_hash,note_pubkey):
     Notes=note_pubkey
     if Notes:
        topology.clear()
        topology_note.clear()
        for note_x in Notes:
            if tags_string(note_x,"alt"):
               if str(tags_string(note_x,"alt")[0][11:]).lower() not in topology:
                topology.append(str(tags_string(note_x,"alt")[0][11:]).lower())
                
               if  str(tags_string(note_x,"alt")[0][11:]).lower()==note_hash or str(tags_string(note_x,"alt")[0][11:]).capitalize()==str(note_hash).capitalize:
                  if note_x not in topology_note:
                    topology_note.append(note_x)
            
            
        return topology,topology_note   

def search_for_topology(topology,note_pubkey):
     Notes=note_pubkey
     note_top=[]
     if Notes:
       for note_x in Notes:
        if tags_string(note_x,"alt")!=[]:
         if str(tags_string(note_x,"alt")[0][11:]).lower()==topology or str(tags_string(note_x,"alt")[0][11:]).capitalize()==str(topology).capitalize:
            if note_x not in note_top:
                    note_top.append(note_x)
            
            
       return len(note_top),note_top
     else:
          return None,None

report_value={}

def print_tag(entry):
    lenght,note_list=pubkey_rep(entry)
    if report_value=={}:
     report_value[entry]="pubkey"
    else:
       if entry in list(report_value.keys()):
          pass
       else:
          report_value.clear()
          report_value[entry]="pubkey"

    frame_tab=Frame(root)

    def Close_print():
      frame_tab.place_forget()          
      button_close_TAB.place_forget()
      note_Label_2d.config(text="")

    button_close_TAB=tk.Button(root,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    test1,note_top=search_for_report("",note_list)
    if test1!=None:
     for test_1 in test1:
        number,report_l=search_for_topology(test_1,note_list)
        if isinstance(report_l,list):
         report_value[test_1]=len(report_l)
      
     print(report_value)
     s=5
     ra=0
     se=1
     ti=2

     def show_tag(entry,pubkey):
      lenght1,note_list=pubkey_rep(pubkey)
      topology,report_list=search_for_report(entry,note_list)
      
      
      if report_list:
        show_lst_ntd(report_list)
     #for word in test1:
     #if word in block_hashtag_word:
     #test1.remove(word)
     test1.sort()
     
     while ra<len(test1):
      if entry in list(report_value.keys()) and test1[ra] in list(report_value.keys()):
         button_grid1=Button(frame_tab,text=f"{test1[ra]} number {report_value[test1[ra]]}", command=lambda val=test1[ra]: show_tag(val,entry))
         button_grid1.grid(row=s,column=0,padx=5,pady=5)                 
      else:
         button_grid1=Button(frame_tab,text=f"{test1[ra]} ", command=lambda val=test1[ra]: show_tag(val,entry))
         button_grid1.grid(row=s,column=0,padx=5,pady=5)
 
      if len(test1)>se:
        if entry in list(report_value.keys()) and test1[ra+1] in list(report_value.keys()):
            button_grid2=Button(frame_tab,text=f"{test1[ra+1]} number {report_value[test1[ra+1]]}", command= lambda val=test1[ra+1]: show_tag(val,entry))
            button_grid2.grid(row=s,column=1,padx=5,pady=5)
        else:
         button_grid2=Button(frame_tab,text=f"{test1[ra+1]}", command= lambda val=test1[ra+1]: show_tag(val,entry))
         button_grid2.grid(row=s,column=1,padx=5,pady=5)

      if len(test1)>ti:
       if entry in list(report_value.keys()) and test1[ra+1] in list(report_value.keys()): 
            button_grid3=Button(frame_tab,text=f"{test1[ra+2]} number {report_value[test1[ra+2]]}", command= lambda val=test1[ra+2]: show_tag(val,entry))
            button_grid3.grid(row=s,column=2,padx=5,pady=5)
       else:
          button_grid3=Button(frame_tab,text=f"{test1[ra+2]}", command= lambda val=test1[ra+2]: show_tag(val,entry))
          button_grid3.grid(row=s,column=2,padx=5,pady=5)   
     
      root.update()  
      s=s+1
      se=se+3
      ra=ra+3
      ti=ti+3   
     else:
        Close_print()
     frame_tab.place(relx=0.05,rely=0.35)
     
     button_close_TAB.place(relx=0.38,rely=0.35)                  

root.mainloop()