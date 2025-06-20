import asyncio
from nostr_sdk import Client, Filter, Keys, NostrSigner, init_logger, LogLevel, PublicKey,Kind, uniffi_set_event_loop
from datetime import timedelta
from asyncio import get_event_loop
from nostr_sdk import *
import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import shutil

async def get_event(client, event_):
    tag_event=[]
    tag_identifiers=[]
    tag_pubkey=[]
    for tag_id in event_:
     if len(tag_id)==64:
      tag_event.append(EventId.parse(tag_id))
     else:
       try:
        if len(tag_id)>71 and tag_id[5]==":" and tag_id[70]==":":
         coord = Coordinate(Kind(int(tag_id[0:5])),PublicKey.parse(tag_id[6:70]),str(tag_id[71:]))
         if coord not in tag_identifiers:
           tag_identifiers.append(coord.identifier())
           tag_pubkey.append(coord.public_key())
       except NostrSdkError as e:
          print(e)     
    if tag_event!=[]: 
     tag_identifiers.clear()
     tag_pubkey=[]
     f = Filter().ids(tag_event)
    if tag_identifiers!=[]: 
     f = Filter().identifiers(tag_identifiers).authors(tag_pubkey)
     
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Selected_event(event_):
        
    client = Client(None)
    uniffi_set_event_loop(asyncio.get_running_loop())
    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    
    await client.connect()
    
    if isinstance(event_, list):
        test_kind = await get_event(client, event_)
    else:
        print("errore")
    await asyncio.sleep(2.0)
    
    return test_kind

async def get_note_cluster(client, authors, type_of_event):
    f = Filter().authors(authors).kinds(type_of_event).limit(1000)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_relay(client, user):
    f = Filter().author(user).kind(Kind(3))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_metadata(user):
    uniffi_set_event_loop(asyncio.get_running_loop())  
    client = Client(None)
    
    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://nostr-pub.wellorder.net/")
   
    await client.connect()
    if isinstance(user,list):
     f = Filter().authors(user).kind(Kind(0))
    else:
       f = Filter().author(user).kind(Kind(0)) 
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    await asyncio.sleep(2.0)
    await client.disconnect()
    return z
  
async def feed_cluster(authors,type_of_event):
    # Init logger
    init_logger(LogLevel.INFO)
   
    client = Client(None)
    #uniffi_set_event_loop(asyncio.get_running_loop())

    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://nostr-pub.wellorder.net/")
   
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_note_cluster(client, authors, type_of_event)
    else:
        combined_results = await get_relay(client, authors)
    
    return combined_results

timeline_list_kind=[]
timeline_people=[]
block_id=[]

def tags_string(x,obj):
    f=x["tags"]
    z=[]
    if f!=[]:
     for j in f:
      if j[0]==obj:
          z.append(j[1])
     return z
    
def get_note(z):
    f=[]
    
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

def found_follow():
   if combo_box.get()!="Name": 
     type_event=""
     follow_kind=get_note(asyncio.run(feed_cluster(convert_user(my_dict[str(combo_box.get())]),type_event))) 
     if follow_kind!=[]:
        people=tags_string(follow_kind[0],"p")
        if people!=None:
         for people_x in people:
           if people_x not in timeline_people:
              timeline_people.append(people_x)

def timelines(): 
 if combo_box.get()!="Name": 
  type_event=[Kind(30023),Kind(1),Kind(7)]
  if timeline_people!=[]:
   tm=get_note(asyncio.run(feed_cluster(user_convert(timeline_people),type_event)))
   for tm_x in tm:
      if tm_x not in timeline_list_kind:
         timeline_list_kind.append(tm_x)
  else:
     found_follow()
      
my_dict = {"Pablo": "fa984bd7dbb282f07e16e7ae87b26a2a7b9b90b7246a44771f0cf5ae58018f52", 
           "jb55": "32e1827635450ebb3c5a7d12c1f8e7b2b514439ac10a67eef3d9fd9c5c68e245",
             "Vitor": "460c25e682fda7832b52d1f22d3d22b3176d972f60dcdc3212ed8c92ef85065c", 
             " Hodlbod": "97c70a44366a6535c145b333f973ea86dfdc2d7a99da618c40c64705ad98e322", 
             "me": "592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"}


root = tk.Tk()
root.geometry("1250x800")
root.title("Combobox Example")

frame1=tk.Frame(root,height=100,width=200,background="grey")
label = tk.Label(frame1, text="Selected Item: ",font=('Arial',12,'bold'))
label.grid(pady=10, column=0, columnspan=2, row=1)

my_list = list(my_dict.values())
my_name = list(my_dict.keys())
def on_select(event):
    selected_item = combo_box.get()
    label.config(text="Selected Item: " + my_dict[selected_item][0:9])

combo_box = ttk.Combobox(frame1, values=["Pablo","jb55","Vitor"," Hodlbod","me"],font=('Arial',12,'bold'))
combo_box.grid(pady=5,column=1, row=0,ipadx=1)
combo_box.set("Name")
combo_box.bind("<<ComboboxSelected>>", on_select)
label_name=tk.Label(frame1, text="Profile",font=('Arial',12))
label_name.grid(column=0, row=0,ipadx=1, padx=5)

label1=tk.Label(frame1, text= "Trending Note", font=('Arial',12,'bold'),background="grey")
label1.grid(column=4, row=0,padx=5,pady=5,ipadx=1,ipady=1,rowspan=2)
frame4=tk.Frame(root,height=25,width= 100)
Channel_frame = ttk.LabelFrame(root, text="Relay", labelanchor="n", padding=10)
Channel_frame.place(relx=0.1,rely=0.21,relheight=0.15,relwidth=0.22)   
button3=tk.Button(root,text="Some Kinds",command=timelines,font=('Arial',14))  #read_Timeline
button3.place(relx=0.12,rely=0.26)   
button_2=tk.Button(root,text="kind 3",command=found_follow,font=('Arial',14))  #timeline
button_2.place(relx=0.24,rely=0.26)  
label_count=tk.Label(frame4, text="Timeline People: "+str(len(timeline_people)), font=('Arial',12,'bold'),foreground="darkgrey")

def count_follow_list():
       label_count.config(text="Timeline People: "+str(len(timeline_people)))
       label_count_2.config(text=str(len(timeline_people)))
       label_count.grid(column=4, row=2,ipadx=1,ipady=1)
       label_count_2.place(relx=0.45,rely=0.25)
       button_3_c.place(relx=0.33,rely=0.24)

def clear_follow_list():
     timeline_people.clear()
     label_count.config(text="Timeline People: "+str(len(timeline_people)))
     button_3_c.place_forget()
     label_count_2.place_forget()

Channel_frame_three = ttk.LabelFrame(root, text="Count", labelanchor="n", padding=10)
Channel_frame_three.place(relx=0.32,rely=0.21,relheight=0.15,relwidth=0.17) 
label_count_2=tk.Label(root, text=str(len(timeline_people)), font=('Arial',12,'bold'),foreground="darkgrey")
button_3=tk.Button(root,text="kind 3 len",command=count_follow_list,font=('Arial',14))  
button_3.place(relx=0.36,rely=0.24)  
label2=tk.Label(frame4, text="", font=('Arial',12,'bold'),foreground="darkgrey")
label_tm_1=tk.Label(root, text=str(len(timeline_list_kind)), font=('Arial',12,'bold'),foreground="darkgrey")

def count_note_list():
    label1=tk.Label(frame4, text="Number events: " +str(len(timeline_list_kind)), font=('Arial',12,'bold'),foreground="darkgrey")
    label1.grid(column=4, row=3,padx=5,pady=5,ipadx=1,ipady=1)
    label_tm_1=tk.Label(root, text=str(len(timeline_list_kind)), font=('Arial',12,'bold'),foreground="darkgrey")
    label_tm_1.place(relx=0.45,rely=0.32)
    event_number()

def call_layoput_note():
   if note_lile!=[]:
        note=asyncio.run(Selected_event(note_lile))
        lile_note=get_note(note)
        timeline_created(lile_note)
        
        print(len(kind_db_list))         

def timeline_created(list_new):
  new_note=[] 
  global kind_db_list
  if kind_db_list!=[]:
   for new_x in list_new:
    if len(kind_db_list)<100: 
     if new_x not in kind_db_list:
        new_note.append(new_x) 
   i=0
    
   while i<len(new_note):
     j=0
     while j< len(kind_db_list): 
      if kind_db_list[j]["created_at"]>(new_note[i]["created_at"]):
         j=j+1
      else:
         kind_db_list.insert(j,new_note[i])
         break
     i=i+1
   return kind_db_list   
  else:
        for list_x in list_new:
            kind_db_list.append(list_x)
        return kind_db_list  

button_4=tk.Button(root,text="kind TM len",command=count_note_list,font=('Arial',12))  
button_4.place(relx=0.36,rely=0.31)     
kind_db_list=[]
note_lile=[]

def choice_kind(x):
    Z=[]
    if timeline_list_kind!=[]:
     if check_seven.get()==0:
      for r in timeline_list_kind:
       if (r)['kind']==x:
          Z.append(r)
      if Z!=[]:
      
        for zeta_p in Z:
           if zeta_p not in kind_db_list and zeta_p["id"] not in block_id:
              if len(kind_db_list)<100:
               kind_db_list.append(zeta_p)
        print(len(kind_db_list))
     else:
       if x==1:
          kind_1=like_note_7()
         
          if kind_1:
             print("1")
             for zeta_j in kind_1:
               if zeta_j not in kind_db_list:
                 if len(kind_db_list)<100:
                  kind_db_list.append(zeta_j)
             #print(len(kind_db_list))  
          else:
                test= like_note_seven()  
                if test:
                 for tex in test:
                    note_lile.append(tex)
                 #print("note lile ",len(note_lile))   

       if x==30023:
           kind_30023=like_long_thread()
           if kind_30023:
             for zeta_a in kind_30023:
               if zeta_a not in kind_db_list:
                 if len(kind_db_list)<100:
                  kind_db_list.append(zeta_a)
             print(len(kind_db_list))     
            
Channel_frame = ttk.LabelFrame(root, text="Type of Note", labelanchor="n", padding=10)
Channel_frame.place(relx=0.1,rely=0.4,relheight=0.15,relwidth=0.22)         
button_4=tk.Button(root,text="note",command=lambda val=1: choice_kind(val),font=('Arial',14))  
button_4.place(relx=0.12,rely=0.44) 
button_4=tk.Button(root,text="Long FORM",command=lambda val=30023: choice_kind(val),font=('Arial',14))  
button_4.place(relx=0.2,rely=0.44) 
button_3_c=tk.Button(root,text="C",command=clear_follow_list,font=('Arial',14, "bold"))  

def clear_kind_scroll():
   for kind_x in kind_db_list:
      block_id.append(kind_x["id"])  
   kind_db_list.clear() 
   label_count_id=Label(root,text="Block Id "+ str(len(block_id)),font=('Arial',14),fg="grey") 
   label_count_id.place(relx=0.6,rely=0.02) 

button_3_z=tk.Button(root,text="Scrolless",command=clear_kind_scroll,font=('Arial',14), background="grey") 
button_3_z.place(relx=0.75,rely=0.11, anchor="n") 
wall=tk.Label(frame1, text="",background="lightgrey",height=4)
wall.grid(column=3, row=0,padx=10,pady=5, rowspan=2)
frame1.place(relx=0.1,rely=0.06)
frame4.place(relx=0.05,rely=0.7)

def number_kind(tm):
    z=[]
    for v in tm:
        if (v)['kind'] in z:
              None  
        else:
              z.append((v)['kind'])
    return z

def event_number():
   if timeline_list_kind!=[]: 
    tm=timeline_list_kind
    t=number_kind(tm)
    i=0
    number=[]
    while i<len(t):
        tip_i=[]
        for v in tm:
         if (v)['kind']==t[i]:
           tip_i.append(v)
        number.append(tip_i)
        i=i+1
    j=0
    label_event=""
    while j<len(number):
     label_event=label_event+str("kind number ")+ str(t[j]) +str(" number event ")+ str(len(number[j]))+"\n"
     
     j=j+1 
    label2["text"]=label_event 
    label2.grid(column=4, row=4,padx=5,pady=5,ipadx=1,ipady=1, rowspan=j) 
    button_5.grid(column=4, row=1,padx=5,pady=5,ipadx=1)    
    return t, number

def close_label():
   label2.grid_forget()
   button_5.grid_forget()
   label_tm_1.place_forget()

button_5=tk.Button(frame4,text="close x",command=close_label,font=('Arial',14))  
Channel_frame_seven = ttk.LabelFrame(root, text="Like", labelanchor="n", padding=10)
Channel_frame_seven.place(relx=0.32,rely=0.4,relheight=0.15,relwidth=0.17) 
check_seven=IntVar()
like_moed = Checkbutton(root, text = "Seven Like", variable = check_seven, onvalue = 1, 
                    offvalue = 0, height = 2, command="",font=('Arial',12,'bold'))
like_moed.place(relx=0.35,rely=0.42)     
button_4_c=tk.Button(root,text="Call layout",command=call_layoput_note,font=('Arial',12))  
button_4_c.place(relx=0.35,rely=0.48) 

def search_3(note,x):
    Z=[]
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list 

def layout():
   if kind_db_list!=[]: 
    frame1=Frame(root, width=360, height=100)
    canvas = Canvas(frame1)
    canvas.pack(side="left", fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame1, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

    # Frame scrollabile
    scrollable_frame = Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    list_note_lib=[]
    def create_note(note_text, s):
        # Message 
       
        if note_text["content"] not in list_note_lib:
         list_note_lib.append(note_text["content"])
         var_npub =StringVar()
         Message_npub= Message(scrollable_frame, textvariable=var_npub, width=350,font=('Arial',12,'bold'),foreground="grey") 
         if note_text["pubkey"] in list(Pubkey_Metadata.keys()):
            var_npub.set("Nickname " +Pubkey_Metadata[note_text["pubkey"]])
         else:
            var_npub.set("Pubkey "+note_text["pubkey"])
         Message_npub.grid(row=s+1, column=0, columnspan=3, padx=10, pady=2, sticky="w") 
                     
         var_time =StringVar()
         Message_time= Message(scrollable_frame, textvariable=var_time, width=350, font=('Arial',12,'bold'), foreground="grey")
         var_time.set("Time: "+(str((note_text)["created_at"])))
         Message_time.grid(row=s, column=0, columnspan=3, padx=50, pady=5, sticky="w")

         scroll_bar_mini = tk.Scrollbar(scrollable_frame)
         scroll_bar_mini.grid( sticky = NS,column=4,row=s+2,pady=5)
         second_label10 = tk.Text(scrollable_frame, padx=8, height=5, width=35, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
         context2=""   
         if note["tags"]!=[]:
          if tags_string(note_text,"t")!=[] :
            for note_tags in tags_string(note_text,"t"):
               context2=context2+str("#")+note_tags+" "
          if tags_string(note,"e")!=[]:
           
           if four_tags(note,"e") and note["kind"]!=30023:
            for F_note in four_tags(note,"e"):
             if len(F_note)>3:
              context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
         else:
          pass            
         second_label10.insert(END,note_text["content"]+"\n"+str(context2))
         scroll_bar_mini.config( command = second_label10.yview )
         
         second_label10.grid(padx=10, column=0, columnspan=3, row=s+2)  
         
         # Button down
         Button(scrollable_frame, text="Open", command=lambda: show_print_test_tag(note_text)).grid(row=s+3, column=0, padx=5, pady=5)
         blo_label = Button(scrollable_frame, text="Share",font=('Arial',12,'normal'),command=lambda: share_note(note_text) )
         blo_label.grid(row=s + 3, column=1, padx=2, pady=5)
         Button(scrollable_frame, text="Print Note", command=lambda: print(note_text)).grid(row=s +3, column=2, padx=5, pady=2)
         
    s = 1
    for note in kind_db_list: #reverse
     create_note(note, s)
     s += 4   
    
    frame1.place(relx=0.55,rely=0.21, relheight=0.4,relwidth=0.4)  
    
    def share_note(note_text):
      test=EventId.parse(note_text["id"])
      test1=Nip19Event(test,PublicKey.parse(note_text["pubkey"]),Kind(note_text["kind"]),[])
      print(test1.to_nostr_uri())
      
      print(str(test.to_nostr_uri()))

    def close_canvas():
        scrollable_frame.forget()
        canvas.destroy()
        frame1.destroy()
        
    if list_note_lib==[]:
     close_canvas()    
    def print_tags(entry):
        
                list_one,list_two=tags_first(entry)
                var_id_2=StringVar()
                label_id_2= Message(scrollable_frame,textvariable=var_id_2, relief=RAISED,width=300,font=("Arial",12,"normal"))
                s=3
                
                def val_tag(val):
                    s=3
                    list_z,par=tags_parameters(list_one,list_two,val)
                    var_id_2.set(str(list_z))
                    value=list_one.index(par)
                    label_id_2.grid(pady=2,column=1,row=s+value, columnspan=3)  
        
                if list_one:
         
                 z=0
         
                 while z<len(list_one):
          
                    button_grid2=Button(scrollable_frame,text=str(list_one[z]), command=lambda val=list_one[z]: val_tag(val))
                    button_grid2.grid(row=s,column=0,padx=5,pady=5)    
                    z=z+1
                    s=s+1 
                 button=Button(scrollable_frame,text="stamp", command=lambda val=var_id_2: stamp_var(val))
                 button.grid(column=0,row=s+1,padx=5,pady=5)
          
                if 'mention' in tags_str_long(entry,"e"):
                    print("e "+tags_str_long(entry,"e"))
                if 'mention' in tags_str_long(entry,"a"):   
                     print("a "+tags_str_long(entry,"a"))
    def stamp_var(entry):
                if entry.get()!="":
                 
                 print(entry.get())         
    
    button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close.grid(column=1,row=0, padx=5,pady=5)  
    label_channel_id = tk.Label(root, text="Id ",font=("Arial",10,"bold"))
    
    
button_open=Button(root, command=layout, 
                   text="scroll",
                    highlightcolor='WHITE',
                    background="grey",
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))

button_open.place(relx=0.65,rely=0.11, anchor="n")

def show_print_test_tag(note):
   
   frame3=tk.Frame(root)  
   canvas_2 = tk.Canvas(frame3,width=490)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = ttk.Frame(canvas_2)

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")
    )
)

   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
   if note["pubkey"] in list(Pubkey_Metadata.keys()):
            context0="Nickname " +Pubkey_Metadata[note["pubkey"]]
   else:
            context0="Pubkey "+note["pubkey"]
   context0=context0+"\n"+"id: "+note["id"]+"\n"
   if note['tags']!=[]:
        context1="Content "+"\n"+note['content']+"\n"
        context2="\n"+"[ - [ - [ Tags ] - ] - ]"+"\n"+"\n"
        context2=context2+"tags number: "+str(len(note["tags"])) +"\n"
   else: 
        context1="content: "+"\n"+note['content']+"\n"
        context2=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   
   var_id.set(context0)
   s=0
   label_id.grid(pady=2,column=0, row=s,columnspan=3,rowspan=2)
   scroll_bar_mini_2 = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini_2.grid( sticky = NS,column=3,row=s+2,rowspan=2,pady=5)
   second_label_2 = tk.Text(scrollable_frame_2, padx=8, height=5, width=30, yscrollcommand = scroll_bar_mini_2.set, font=('Arial',14,'bold'),background="#D9D6D3")
   if note["tags"]!=[]:
         if tags_string(note,"t")!=[] :
            for note_tags in tags_string(note,"t"):
               context2=context2+str("#")+note_tags+" "
         if tags_string(note,"e")!=[]:
           
           if four_tags(note,"e") and note["kind"]!=30023:
            for F_note in four_tags(note,"e"):
             if len(F_note)>3:
              context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
         else:
          pass            
   second_label_2.insert(END,note["content"]+"\n"+str(context2))
   scroll_bar_mini_2.config( command = second_label_2.yview )
   second_label_2.grid(padx=10, column=0, columnspan=3, row=s+2,rowspan=2)

   def print_var(entry):
        amount_zap(entry)
            

   button_grid_1=Button(scrollable_frame_2,text="Zap", command=lambda val=note: print_var(val), width=10, height=3)
   button_grid_1.grid(row=s,column=5,padx=5,pady=5)    
                   
   def print_like(entry):
      reply_re_action(entry)  

   def print_media(entry):
      if len(more_spam(entry))<2: 
              photo_print(entry)
      else:
               
               if tags_string(entry,"imeta")!=[]:
                photo_list_2(entry)
               else:
                  if len(more_spam(entry))==2:
                    photo_list(more_spam(entry))

   button_grid_2=Button(scrollable_frame_2,text="Read", command=lambda val=note: print_content(val),width=10, height=3)
   button_grid_2.grid(row=s+1,column=5,padx=5,pady=5)    
   button_grid_3=Button(scrollable_frame_2,text="Open Media", command=lambda val=note: print_media(val),width=10, height=3)
   button_grid_3.grid(row=s+2,column=5,padx=5,pady=5)
   button_grid_4=Button(scrollable_frame_2,text="Like", command=lambda val=note: print_like(val),width=10, height=3)
   button_grid_4.grid(row=s+3,column=5,padx=5,pady=5)        
   def print_tags(entry):
        
                list_one,list_two=tags_first(entry)
                var_id_2=StringVar()
                label_id_2= Message(scrollable_frame_2,textvariable=var_id_2, relief=RAISED,width=220,font=("Arial",12,"normal"))
                s=5
                
                def val_tag(val):
                    s=5
                    list_z,par=tags_parameters(list_one,list_two,val)
                    var_id_2.set(str(list_z))
                    value=list_one.index(par)
                    label_id_2.grid(pady=2,column=1,row=s+value, columnspan=2)  
                button_list=[]
                if list_one:
         
                 z=0
         
                 while z<len(list_one):
          
                    button_grid2=Button(scrollable_frame_2,text=str(list_one[z]), command=lambda val=list_one[z]: val_tag(val))
                    button_grid2.grid(row=s,column=0,padx=5,pady=5) 
                    button_list.append(button_grid2)   
                    z=z+1
                    s=s+1 
                 button_stamp=Button(scrollable_frame_2,text="stamp", command=lambda val=var_id_2: stamp_var(val))
                 button_stamp.grid(column=0,row=s+1,padx=5,pady=5)
                 def close_Tags():
                    button_stamp.grid_forget()
                     
                    for button2 in  button_list:
                     button2.grid_forget()
                    
                    #button_grid2.destroy()
                    button_c_tags.grid_forget()
                    label_id_2.grid_forget()
                    
                 button_c_tags=Button(scrollable_frame_2,command=close_Tags,text="Tag ❌",font=("Arial",12,"normal"))
                 button_c_tags.grid()   
          
                if 'mention' in tags_str_long(entry,"e"):
                    print("e "+tags_str_long(entry,"e"))
                if 'mention' in tags_str_long(entry,"a"):   
                     print("a "+tags_str_long(entry,"a"))
   def stamp_var(entry):
                if entry.get()!="":
                 print(entry.get())                                  
   s=4        
   button=Button(scrollable_frame_2,text=f"Tags!", command=lambda val=note: print_tags(val))
   button.grid(column=0,row=s,padx=5,pady=5)

   def print_content(entry):
       result=show_note_from_id(entry)
       if result!=None: 
        z=3
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             if jresult["pubkey"] in list(Pubkey_Metadata.keys()):
                var_id_r.set("Nickname " +Pubkey_Metadata[jresult["pubkey"]])
             else:
                var_id_r.set(" Author: "+jresult["pubkey"])
         
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             context22="---> tags: <--- "+"\n"   
             if tags_string(jresult,"e")!=[]:
              if four_tags(jresult,"e"):
                for F_note in four_tags(note,"e"):
                     context22=context22+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              else:
                 if tags_string(jresult,"e"):
                    context22=context22+str(len(tags_string(jresult,"e")))+ "\n"
                 else:
                    context22="---> Root  <--- "     
             else:
               context22="---> Root  <--- "  
             second_label10_r.insert(END,jresult["content"]+"\n"+str(context22))
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
           z=z+2
                           
      
   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply!", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s,column=2,padx=5,pady=5)    
   else:
    if is_video(note)!=None:
     button_grid3=Button(scrollable_frame_2,text=f"See video!")  #pass
     button_grid3.grid(row=s,column=2,padx=5,pady=5)   

   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()    
   button_frame=Button(frame3,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.pack(pady=5)   
   frame3.place(relx=0.55,rely=0.20,relheight=0.53,relwidth=0.45) 

def show_note_from_id(note):
        result=note["id"]
       
        replay=nota_reply_id(note)
        replay.append(result)
        if replay!=[]:
           items=get_note(asyncio.run(Selected_event(replay)))
        else:
           items=get_note(asyncio.run(Selected_event(result)))
        return items   

def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id  

def is_video(nota):
   if nota["tags"]!=[]: 
    if tags_str(nota,"imeta")!=[]:
      url_=[]
      for dim_photo in tags_str(nota,"imeta"):
       if more_link(dim_photo[1][4:])=="video":
          url_.append(dim_photo[1][4:])
      if url_!=[]:
         print(url_)
         return url_  

def tags_str_long(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
       if len(j)>2:
         z.append(j[1:]) 
       else:    
          z.append(j[1])
    return z   

def tags_first(x):
   tags_list=[]
   tags_value=[]
   if x["tags"]!=[]:
      for jtags in x["tags"]:
         if jtags[0] not in tags_list:
            tags_list.append(jtags[0])
   if tags_list!=[]:
       for xtags in tags_list:
         for ztags in tags_str(x,xtags):
            tags_value.append(ztags)
   return tags_list,tags_value 

def tags_parameters(key,value,s):
    list_q=[]
    if s in key:
        for xvalue in value:
          if xvalue[0]==s:
              list_q.append(xvalue[1:])
    return list_q,s  

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z 

def choice_kind_to_list(x):
    Z=[]
    if timeline_list_kind!=[]:
    
     for r in timeline_list_kind:
       if (r)['kind']==x:
          Z.append(r)
     if Z!=[]:
        list_lind=[] 
        for zeta_p in Z:
           if zeta_p not in list_lind:
              list_lind.append(zeta_p)
     if list_lind!=[]:
        return list_lind   

def like_note_seven():
   kind_7=choice_kind_to_list(7) 
   if kind_7!=None:
    vore_id=[]
    core_id=[]
    zore_id=[]
    uore_id=[]
    for x in kind_7:
     if tags_string(x,'e')!=[]:
      if (tags_string(x,'e')[0]) not in vore_id: 
        vore_id.append(tags_string(x,'e')[0]) 
      else:
           if tags_string(x,'e')[0] not in core_id:
            core_id.append(tags_string(x,'e')[0])
           else:
              if tags_string(x,'e')[0] not in zore_id:
               zore_id.append(tags_string(x,'e')[0])
              else:
                 if tags_string(x,'e')[0] not in uore_id:
                  uore_id.append(tags_string(x,'e')[0])
              
    print(len(vore_id), len(core_id),len(zore_id),len(uore_id))
    if uore_id!=[]:
       return uore_id
    if zore_id!=[]:
       return zore_id   

def like_note_7():
  kind_1=choice_kind_to_list(1)
  kind_7=choice_kind_to_list(7) 
  
  if kind_7!=None and kind_1!=None:
   vore_id=[]
   for x in kind_7:
    if tags_string(x,'e')!=[]:
     if tags_string(x,'e')[0] in kind_1:  
      if (tags_string(x,'e')[0]) not in vore_id: 
       vore_id.append(tags_string(x,'e')[0]) 
   print(len(vore_id))   
   note_kind_one=[]
   for note in kind_1:
      if note["id"] in vore_id:
         if note not in note_kind_one:
            note_kind_one.append(note) 
   if note_kind_one!=[]:
      print("print ", len(note_kind_one))
      return note_kind_one    

def like_long_thread():
   vore_id=[]
   kind_long=choice_kind_to_list(30023) 
   kind_7=choice_kind_to_list(7) 
   if kind_7!=None and kind_long !=None:
    for x in kind_7:
     if tags_string(x,'a')!=[]:
      name= tags_string(x,'a')[0]
      if name[0:6]=="30023:":
          print("note like",x["kind"],"\n", name)
          if tags_string(x,'a')[0] not in vore_id:   
            vore_id.append(tags_string(x,'a')[0])
   if vore_id!=[]:
      for vore_x in vore_id:
         if vore_x not in note_lile:
            note_lile.append(vore_x)
      long_article=[]
      for j in kind_long:
       if tags_string(j,"d")!=None:
            if tags_string(j,"d")!=[]:
                if str("30023:")+str(j["pubkey"])+str(":")+str(tags_string(j,"d")[0]) in vore_id:
                  long_article.append(j)   
      if long_article!=[]:
         return long_article                 

def more_spam(x):
 z=x['content']
 notes_link=[]
 for j in z.split():
    if j[0:5]=="https":
        notes_link.append(str(j))
 return notes_link   

def photo_list_2(note):
 frame_pic=tk.Frame(root,height=80,width= 80) 
 
 balance,list_note1=balance_photo_print(note)
 int_var=IntVar()
 lbel_var=Entry(frame_pic, textvariable=int_var)    
 if list_note1!=[] and balance!=[]: 
  if list_note1!=None and balance!=None:
   
   def next_number():
      #lbel_var.grid(column=1,row=3,pady=2) 
      if int((int(lbel_var.get())+1))< len(list_note1):
       int_var.set(int(lbel_var.get())+1)
       print_photo()
      else:
          int_var.set(int(0)) 
          print_photo()
     
   
    #while int(lbel_var.get())<len(list_note1):  
   stringa_pic=StringVar()
   def print_photo():
     s=0  
     stringa_pic.set(list_note1[int(lbel_var.get())])
     label_pic = Entry(frame_pic, textvariable=stringa_pic)
    
     image_label = tk.Label(frame_pic)
     image_label.grid(column=1,row=s, columnspan=2)
     if label_pic.get()!="":
       response = requests.get(label_pic.get(), stream=True)
       if response.ok==True:
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        number=balance[int(lbel_var.get())]
        test1=int(float(number)*250)
        if test1>400:
           test1=int(400)
        if test1<150:
           test1=int(160)   
        image.thumbnail((test1, 250))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image_names= photo
  
        def close_pic():
            image_label.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)
            frame_pic.destroy()

        def close_one_pic():
            image_label.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)    
            next_number()
        s=s+3
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        button_close.grid(column=2,columnspan=1,row=s+1)
        button_close_photo=Button(frame_pic,command=close_one_pic,text="Next",font=("Arial",12,"bold"))
        button_close_photo.grid(column=1,row=s+1)
        s=s+2
   print_photo()     
   frame_pic.place(relx=0.4,rely=0.6,relwidth=0.3) 
  else:
     print("error", "none")        
 else:
     pass
     #print("error", "[]","maybe a video")

def balance_photo_print(nota):
 if nota["tags"]!=[]: 
  if tags_str(nota,"imeta")!=[]:
   balance=[]
   url_=[]
   for dim_photo in tags_str(nota,"imeta"):
     if more_link(dim_photo[1][4:])=="pic": 
      url_.append(dim_photo[1][4:])
      
      for jdim in dim_photo:
       if jdim[0:3]=="dim":
        list_number=dim_photo.index(jdim)   
        for xdim in dim_photo[list_number][4:]:
         if xdim=="x":
          number=dim_photo[list_number].index(xdim)
       
          numberx=number
          numbery=number+1
          balx=dim_photo[list_number][4:numberx]
          baly=dim_photo[list_number][numbery:]  
          
          balance.append(float(int(balx)/int(baly)))
   
   return balance,url_       
  else:
     return None,None
 else:
     return None,None 

def more_link(f):
   
   list=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
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

def codifica_link(x):
   f=url_spam(x)
   list=['mov','mp4']
   img=['png','jpg','JPG','gif']
   img1=['jpeg','webp'] 
   tme=["https://t.me/"]
   xtwitter=["https://x.com/"]
   if f==None:
                 return "no spam"
   if f[-3:] in list:
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

def url_spam(x):
 z=x['content']
 for j in z.split():
    if j[0:5]=="https":
        return str(j)
    
def photo_list(list_note):
 frame_pic=tk.Frame(root,height=80,width= 80) 
 s=0
 list_note1=[]
 for xnote in list_note:
  if more_link(xnote)=="pic":
     list_note1.append(xnote)
 if list_note1!=[]:  
  for note in list_note1:  
   if list_note.index(note)<4:
  
    stringa_pic=StringVar()
    stringa_pic.set(note)
    label_pic = Entry(frame_pic, textvariable=stringa_pic)
    #label_pic.grid(column=1,row=2,pady=2)
    image_label = tk.Label(frame_pic)
    image_label.grid(column=1,row=s, columnspan=2)
    if label_pic.get()!="":
         
        response = requests.get(label_pic.get(), stream=True)
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        image.thumbnail((250, 250))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image_names= photo
  
        def close_pic():
            image_label.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)
            frame_pic.destroy()
  
        s=s+3
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        button_close.grid(column=2,row=s+1,sticky="n")
        s=s+2
  frame_pic.place(relx=0.45,rely=0.6,relwidth=0.18)    

def photo_print(note):
  #print(codifica_link(note),url_spam(note))
  if codifica_link(note)=="pic":
   #morespam

   frame_pic=tk.Frame(root,height=20,width= 80)
   stringa_pic=StringVar()
   stringa_pic.set(url_spam(note))
   label_pic = Entry(frame_pic, textvariable=stringa_pic)
   #label_pic.grid(column=1,row=2,pady=2)
   image_label = tk.Label(frame_pic)
   image_label.grid(column=0,row=0, padx=10,pady=10)
   if label_pic.get()!="":
       try:
        response = requests.get(label_pic.get(), stream=True)
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        image.thumbnail((250, 250))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image_names= photo
       
        def close_pic():
            image_label.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)
            frame_pic.destroy()
  
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        frame_pic.columnconfigure(0,weight=1)
        frame_pic.rowconfigure(0,weight=3)
        
        button_close.grid(column=0,row=1,padx=10)
        frame_pic.place(relx=0.45,rely=0.6,relwidth=0.3,relheight=0.3,anchor="n")
       except TypeError as e: 
        print(e)  

def search_kind(user,x):
    
    # Example usage with a single key
    single_author = user 
    single_results = asyncio.run(get_metadata(single_author))
    Z=[]
    note=get_note(single_results)
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z     

Zap_frame = ttk.LabelFrame(root, text="Zap Button", labelanchor="n", padding=10)

def val_number(number:int):
   number_string.set(number)
   
def amount_zap(note):
    number_string.set(0)
    stringa_nota_id.set(note["id"])
    Zap_frame.place(relx=0.77,rely=0.2,relheight=0.25,relwidth=0.22) 
    button_zap_1=tk.Button(root,text="5", background="darkgrey", command=lambda val=5: val_number(val))
    button_zap_1.place(relx=0.8,rely=0.25)   
    button_zap_2=tk.Button(root,text="10", background="darkgrey", command=lambda val=10: val_number(val))
    button_zap_2.place(relx=0.85,rely=0.25)   
    button_zap_3=tk.Button(root,text="20", background="darkgrey", command=lambda val=20: val_number(val))
    button_zap_3.place(relx=0.9,rely=0.25)   
    button_zap_4=tk.Button(root,text="50", background="darkgrey", command=lambda val=50: val_number(val))
    button_zap_4.place(relx=0.8,rely=0.3)   
    button_zap_5=tk.Button(root,text="100", background="darkgrey", command=lambda val=100: val_number(val))
    button_zap_5.place(relx=0.85,rely=0.3)   
    button_zap_6=tk.Button(root,text="200", background="darkgrey", command=lambda val=200: val_number(val))
    button_zap_6.place(relx=0.9,rely=0.3)  
    select_number.place(relx=0.82,rely=0.4)
    pre_nota_tag.place(relx=0.78,rely=0.5,relwidth=0.2,relheight=0.05 )
    pre_nota_lab.place(relx=0.8,rely=0.45,relwidth=0.1,relheight=0.05 )

    def close_stuff():
       button_zap_1.place_forget()
       button_zap_2.place_forget()
       button_zap_3.place_forget()
       button_zap_4.place_forget()
       button_zap_5.place_forget()
       button_zap_6.place_forget()
       button_zap_c.place_forget()
       select_number.place_forget()
       button_zap_o1.place_forget()
       Zap_frame.place_forget()
       pre_nota_tag.place_forget()
       pre_nota_lab.place_forget()

    button_zap_c=tk.Button(root,text="close", background="darkgrey", command=close_stuff)
    button_zap_c.place(relx=0.95,rely=0.22)       
    button_zap_o1=tk.Button(root,text=f"Zap", background="darkgrey", command=zap_id_note2)  
    button_zap_o1.place(relx=0.9,rely=0.4)    

number_string=IntVar()
select_number=Entry(root, textvariable=number_string,font=('Arial',12,'bold'),width=10)

stringa_nota_id=tk.StringVar()
pre_nota_lab = tk.Label(root, text="Note Id")
pre_nota_tag = tk.Entry(root, textvariable=stringa_nota_id)

def evnt_id(id):
    try: 
     test2=EventId.parse(id)
     return test2
    except NostrSdkError as e:
       print(e)

def reply_id_zap():
   event=pre_nota_tag.get()
   search_id=evnt_id(event)
   if search_id!=None:
    found_nota=asyncio.run(Get_id(search_id))
    nota=get_note(found_nota)
    if nota!=None:
     return nota[0]
    else:
      print ("error")

def zap_id_note():
  note=reply_id_zap()
  if note:
   if __name__ == '__main__':
    callback=fetch_lud_16(note)
    if callback!=None:
     request,amount_=asyncio.run(zap_request(note, callback))
    else:
       return None,None,None 
    
    if __name__ == '__main__':
     invoice,preimage=asyncio.run(main_2(callback,amount_))
    if invoice!=None and preimage!=None: 
     return invoice,request,preimage  
  else:
     return None,None,None
  
def zap_id_note2():
  if pre_nota_tag.get()!="" and number_string.get()!=0:
   invoice,request,preimage=zap_id_note()
   
   if __name__ == '__main__':
       if preimage!=None:
          asyncio.run(zap_ing(invoice,preimage,request))
   else:
          print("Error")
          entry_preimage.insert(0, "Error ")

def fetch_lud_16(note):
 public_key_=PublicKey.parse(note['pubkey'])
 kind_0=search_kind(public_key_,0)
 if kind_0!=[]:
  content=json.loads((kind_0[0]['content']))    
  if 'lud16' in list(content.keys()):
   try:
    url_16=content['lud16']
    i=0
    while i <len(url_16):
     if url_16[i]=="@":
       name=url_16[0:i]
       suff=url_16[i+1:]
     i=i+1
    print(name,suff) 
    request=str(str("https://")+suff+str("/.well-known/"))+str("lnurlp/")+str(name)
    print(request) 
    return request
   except KeyError as e:
     print(e )
     return None 
  else:
    return None 
 else:
    return None
 

def qrcode_f(invoice):
    for j in invoice.split():
        if j[0:4]=="lnbc":
         import qrcode
         img = qrcode.make(invoice)
         img.show()           

pre_image_tag = tk.Label(root, text="call lnurlp")
entry_preimage=ttk.Entry(root,justify='left')

async def zap_ing(invoice,preimage,public_zap_):
    # Compose client
    keys = Keys.generate()
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    await client.add_relay("wss://nos.lol/")
    await client.connect()
            
    eventis_= EventBuilder.zap_receipt(invoice,preimage,public_zap_ )
    await client.send_event_builder(eventis_)
       
    print(f"Public zap event: {eventis_}\n")
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     print(event.as_json())

async def get_relays(client, authors):
    f = Filter().authors(authors)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_relay_str(client, user):
    f = Filter().author(user)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def feed(authors):
    # Init logger
    init_logger(LogLevel.INFO)
   
    client = Client(None)
    
    # Add relays and connect
    await client.add_relay("wss://relay.damus.io/")
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://relay.nostr.band/")
    await client.add_relay("wss://purplepag.es/")

    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_relays(client, authors)
    else:
        combined_results = await get_relay_str(client, authors)
    
    return combined_results    

async def get_one_Event(client, event_):
    f = Filter().id(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://relay.primal.net")
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        print("errore")
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

async def zap_request(test, callback):
    init_logger(LogLevel.INFO)
    #uniffi_set_event_loop(asyncio.get_running_loop())
    keys = Keys.generate()
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://relay.damus.io/")
    await client.connect()
        
    public_key_ = PublicKey.parse(test['pubkey'])
    relays = ["wss://nostr.mom"]
    msg = "Zap!"
    amount_=int(number_string.get())*1000
    url=callback
    
    data = ZapRequestData(public_key_, relays).message(msg).event_id(EventId.parse(test['id'])).amount(amount_).lnurl(url)
    public_zap_ = EventBuilder.public_zap_request(data).sign_with_keys(keys)               #to_event(keys)
    return public_zap_,amount_

async def main_2(url,amount_):
    # create the background task
    task = asyncio.create_task(background())
    # allow the background task to start executing
    await asyncio.sleep(0)
    pre_image_tag = tk.Label(root, text="call lnurlp")
    pre_image_tag.place(relx=0.55,rely=0.9,relwidth=0.1,relheight=0.05 )
    entry_preimage=ttk.Entry(root,justify='left')
    entry_preimage.place(relx=0.55,rely=0.95,relwidth=0.2 ) 
    entry_preimage.insert(0,url)
  
    if url[8:19]!="getalby.com" or url[8:14]!="zbd.gg":
     r2=requests.get(url) 
     data_test2=json.loads(r2.text)
     data_test35= data_test2['callback']
     r3=requests.get(data_test35+str(f"?&amount={amount_}"))
     data_test3=json.loads(r3.text)
     print(data_test3)
     data_test4= data_test3["pr"]

    else:  
     try: 
         print(url[8:19]) 
         r4=requests.get(url+"/callback"+str(f"?&amount={amount_}"))
         print(r4.status_code)
         if r4.status_code ==1:
          data_test3=json.loads(r4.text)
          print(data_test3)
          data_test4= data_test3["pr"]
         else:
             return None,None 
     except KeyError as e:
        print(e)
        return None,None
         
    qrcode_f(data_test4)
    task2 = await background2(data_test3)
    if task2:
     return data_test4,task2
    else:
       #qrcode_f(data_test4)
       return None,None

async def background():
    while True:
        print('Running in the background...')
        await asyncio.sleep(0.01)

async def background2(data_test1):
    while True:
        print('Running in the background...')
        #print(data_test1)
        if 'verify'not in data_test1:
         print("enable to verify")
         await asyncio.sleep(0.01)  
         return None
        else:
         url_2=data_test1['verify']
         print(url_2)
         r4=requests.get(url_2)
         data_test_2= json.loads(r4.text)
         data_test_3=data_test_2['preimage']
         if data_test_3!= None:
          print( data_test_3)  
          await asyncio.sleep(0.01)  
          return data_test_3
         else:
            print(data_test_2)

def reply_re_action(note):
  
   test = EventId.parse(note["id"])
   public_key=convert_user(note["pubkey"])
   if __name__ == '__main__':
    note_rea="+"
    type_event=Kind(int(note["kind"]))
    asyncio.run(reply_reaction(test,public_key,note_rea,type_event))    

async def reply_reaction(event_id,public_key,str_reaction,type_event):
   
    keys = Keys.generate()
    
    signer = NostrSigner.keys(keys)
    
    client = Client(signer)
    # Add relays and connect
    await client.add_relay("wss://nostr.mom")
    await client.add_relay("wss://nos.lol")
    await client.connect()

    # Send an event using the Nostr Signer
    builder = EventBuilder.reaction_extended(event_id,public_key,str_reaction,type_event)
    test_note=await client.send_event_builder(builder)
    print("this relay is going good", test_note.success, "\n", "this relay is bad",test_note.failed)

def list_people_fun():
    people_list=[]
    if kind_db_list!=[]:
        for note_x in kind_db_list:
            if note_x["pubkey"] not in people_list:
                        people_list.append(note_x["pubkey"])
        return people_list       
    else:
       return people_list

Pubkey_Metadata={}

def pubkey_id(test):
   
   metadata_note=search_kind(PublicKey.parse(test),0)
   if metadata_note!=[]:
       single=metadata_note[0]
       single_1=json.loads(single["content"])
       try:
        if single_1["name"]!="":
           
           if test not in list(Pubkey_Metadata.keys()):
              Pubkey_Metadata[test]=single_1["name"]
              print("Pubkey", test,"\n","Npub ",PublicKey.parse(test).to_bech32())
              print(single_1["name"])
        else:   
            if single_1["display_name"]!="":
                  
                if test not in list(Pubkey_Metadata.keys()):
                  Pubkey_Metadata[test]=single_1["display_name"]  
                  print("Pubkey", test,"\n","Npub ",PublicKey.parse(test).to_bech32())
                  print(single_1["display_name"])      
       except KeyError as e:
          print("KeyError ",e)     

def list_pubkey_id():
  people_list=list_people_fun()
  if people_list !=[]:
   test_people=user_convert(people_list)    #not cover people are already on metadata
   metadata_note=search_kind(test_people,0)
   if metadata_note!=[]:
       for single in metadata_note:
        single_1=json.loads(single["content"])
        try:
         if single_1["name"]!="":
           #print("Pubkey", single["pubkey"],"\n","Npub ",PublicKey.parse(single["pubkey"]).to_bech32())
           
           if single["pubkey"] not in list(Pubkey_Metadata.keys()):
              Pubkey_Metadata[single["pubkey"]]=single_1["name"]
              #print(single_1["name"])
         else:   
            if single_1["display_name"]!="":
                #print("Pubkey", single["pubkey"],"\n","Npub ",PublicKey.parse(single["pubkey"]).to_bech32())
                
                if single["pubkey"]not in list(Pubkey_Metadata.keys()):
                  Pubkey_Metadata[single["pubkey"]]=single_1["display_name"]    
                  #print(single_1["display_name"])      
        except KeyError as e:
          print("KeyError ",e)             
   
def print_people(): 
   if kind_db_list!=[]:  
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=280)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas,border=2)

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
    se=2
            
    while ra<len(test1):
            
                button_grid1=Button(scrollable_frame,text=f"{test1[ra][0:9]} ", command=lambda val=test1[ra]: pubkey_id(val))
                button_grid1.grid(row=s,column=1,padx=5,pady=5)
                
                if len(test1)>se:
                 button_grid2=Button(scrollable_frame,text=f"{test1[ra+1][0:10]}", command= lambda val=test1[ra+1]: pubkey_id(val))
                 button_grid2.grid(row=s,column=2,padx=5,pady=5)
                if len(test1)>se:
                 button_grid2=Button(scrollable_frame,text=f"{test1[ra+2][0:10]}", command= lambda val=test1[ra+2]: pubkey_id(val))
                 button_grid2.grid(row=s,column=3,padx=5,pady=5) 
            
                root.update()  
              
                s=s+1
                se=se+3
                ra=ra+3   

    canvas.pack(side="left", fill="y", expand=True)
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.3,rely=0.65,relwidth=0.28, relheight=0.3)      
    def Close_print():
       frame3.destroy()  
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

button_people_=tk.Button(root,text="Print People",command=print_people, font=('Arial',12,'bold'))
button_people_.place(relx=0.12,rely=0.58) 

button_people_2=Button(root,text=f"Find People ", command=list_pubkey_id,font=('Arial',12,'bold'))
button_people_2.place(relx=0.22,rely=0.58) 

root.mainloop()