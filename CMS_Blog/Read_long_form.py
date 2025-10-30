import tkinter as tk
from tkinter import *
from tkinter import ttk
from nostr_sdk import *
import asyncio
import json
from datetime import timedelta
import asyncio
import json
import requests
import qrcode
import shutil
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("1300x800")
root.title("Test Example")

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

def get_note(z):
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f

def evnt_id(id):
    try: 
     test2=EventId.parse(id)
     return test2
    except NostrSdkError as e:
       print(e,"input ",id)

def evnts_ids(list_id):
     Event=[]
     for j in list_id:
        if evnt_id(j):
         Event.append(evnt_id(j))
     return Event       

def search_kind(user,x):
    if __name__ == "__main__":
     # Example usage with a single key
     single_author = user 
     single_results = asyncio.run(feed(single_author))
    Z=[]
    note=get_note(single_results)
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z        

def search_o_tags(x):
   tags_list=[]
   
   if x["tags"]!=[]:
      for jtags in x["tags"]:
         if len(jtags)>2:
          for xtags in jtags[2:]:
           if xtags not in tags_list:
            tags_list.append(xtags)
   return tags_list            

my_dict = {"Pablo": "fa984bd7dbb282f07e16e7ae87b26a2a7b9b90b7246a44771f0cf5ae58018f52", 
           "jb55": "32e1827635450ebb3c5a7d12c1f8e7b2b514439ac10a67eef3d9fd9c5c68e245",
             "Vitor": "460c25e682fda7832b52d1f22d3d22b3176d972f60dcdc3212ed8c92ef85065c", 
             " hodlbod": "97c70a44366a6535c145b333f973ea86dfdc2d7a99da618c40c64705ad98e322", 
             "il_lost_": "592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"}

my_list = list(my_dict.values())
my_name = list(my_dict.keys())

def on_select(event):
    selected_item = combo_box.get()
    entry_id_note.set(my_dict[selected_item])
    label_entry_id["text"]="Pubkey"
    relay_list.clear()
    search_relay()
  
frame1=tk.Frame(root)    
Profile_frame = ttk.LabelFrame(root, text="Profile", labelanchor="n", padding=10)
Profile_frame.place(relx=0.01,rely=0.03,relwidth=0.2,relheight=0.3)
label = tk.Label(root, text="Name")
label.place(relx=0.08,rely=0.07)
combo_box = ttk.Combobox(root, values=["Pablo","jb55","Vitor"," hodlbod","il_lost_"],font=("Arial",12,"normal"),width=15)
combo_box.place(relx=0.06,rely=0.1)
combo_box.set("Cluster")
combo_box.bind("<<ComboboxSelected>>", on_select)
entry_id_note=StringVar()
entry_note_note=StringVar()
label_entry_id=tk.Label(root, text="Pubkey",font=("Arial",12,"normal"))
label_entry_id.place(relx=0.08,rely=0.18)
label_entry_name=tk.Label(root, text="",font=("Arial",12,"normal"))
time_frame = ttk.LabelFrame(root, text="Time", labelanchor="n", padding=10)
time_frame.place(relx=0.21,rely=0.03,relwidth=0.13,relheight=0.3)
combo_note = ttk.Combobox(root, values=["Timeline","My_post","Inbox","Hashtag","my_hashtag","my_time"],width=10, font=("Arial",12,"normal"))
combo_note.place(relx=0.23,rely=0.15)
combo_note.set("Type of feed")
combo_note.bind("<<ComboboxSelected>>", None)
Timeline=[]
My_post=[]
Inbox=[]
Hashtag=[]
my_hashtag=[]
my_time=[]
Frame_block=Frame(frame1,width=50, height=20)

def timeline_published(list_new):
  new_note=[] 
  
  if db_list!=[]:
   for new_x in list_new:
     if new_x not in db_list:
        new_note.append(new_x) 
   i=0
  
   while i<len(new_note):
    if tags_string(new_note[i],"published_at")!=[]:  
     j=0
     while j< len(db_list): 
      if tags_string(db_list[j],"published_at")!=[]:
       if tags_string(db_list[j],"published_at")[0]>tags_string(new_note[i],"published_at")[0]:
         j=j+1
       else:
         db_list.insert(j,new_note[i])
         break
      else:
         j=j+1 
    i=i+1
   return db_list   
  else:
        for list_x in list_new:
            db_list.append(list_x)
        return db_list    

test_check = IntVar() 

def check_dash():
 if combo_note.get()!="Type of feed":
  if combo_note.get()=="my_time":
   if test_check.get()==1:
    since_entry.place(relx=0.42,rely=0.04)
    button_mov.place(relx=0.46,rely=0.04,relwidth=0.03)
    button_backs.place(relx=0.38,rely=0.04,relwidth=0.03) 
    date_entry.place(relx=0.4,rely=0.1,relheight=0.04, x=0.01 )
   else:
    since_entry.place_forget()
    button_mov.place_forget()
    button_backs.place_forget()
    date_entry.place_forget()
  else:
     print("this an other function ", combo_note.get())  
     if test_check.get()==1:
      test_check.set(0)
      combo_note.set("my_time")
     since_entry.place_forget()
     button_mov.place_forget()
     button_backs.place_forget()
     date_entry.place_forget()

Button_check_2 = Checkbutton(root, text ="" , variable = test_check, onvalue = 1, 
                    offvalue = 0, height = 1, command=check_dash,)
Button_check_2.place(relx=0.3,rely=0.22)
label_time = tk.Label(root, text="Time",font=("Arial",12,"normal"))
label_time.place(relx=0.25,rely=0.22)
since_variable=IntVar(value=0)
since_entry=Entry(root,textvariable=since_variable,font=("Arial",12,"normal"),width=4)

def next_since():
   since_variable.set(int(since_entry.get()) + 1)
   since_day_time()

def back_since():
   if int(since_entry.get())- 1<1:
      since_variable.set(int(1))
      since_day_time()
   else:
    since_variable.set(int(since_entry.get())- 1)  
    since_day_time()

button_mov=tk.Button(root,text="➕",command=next_since)
button_backs=tk.Button(root,text="➖",command=back_since)
text_variable=StringVar()
date_entry=Entry(root,text=text_variable,font=("Arial",12,"normal"),width=11)

def since_day_time():
    import datetime
    import calendar
    date = datetime.date.today() - datetime.timedelta(days=int(since_entry.get()))
    t = datetime.datetime.combine(date, datetime.time(1, 2, 1))
    date=datetime.datetime.combine(date, datetime.time(1, 2, 1)).timestamp()
    text_variable.set(str(int(date)))

def list_timeline(Value):
  if Value!="Type of feed":  
   if Value in combo_note["values"]:
      if Value=="Timeline":
         return db_list
      if Value=="My_post":
         My_post.clear()
         for db_x in db_list:
            if db_x["pubkey"]==entry_id.get():
               My_post.append(db_x)
         return My_post      
           

      if Value=="Inbox":
         Inbox.clear()
         for db_x in db_list:
           if tags_string(db_x,"p")!=[]:
            for pubkey_x in tags_string(db_x,"p"): 
             if pubkey_x==entry_id.get():
               Inbox.append(db_x)     
         return Inbox
      if Value=="Hashtag": 
         Hashtag.clear()
         for db_x in db_list:
           if tags_string(db_x,"t")!=[]:
              if db_x not in Hashtag:
                Hashtag.append(db_x)     
         return Hashtag
      if Value=="my_hashtag":
         my_hashtag.clear()
         for db_x in db_list:
            if db_x["pubkey"]==entry_id.get():
              if tags_string(db_x,"t")!=[]:
               my_hashtag.append(db_x)
         return my_hashtag   
      if Value=="my_time":
         my_time.clear()
         for db_x in db_list:
            if date_entry.get()!="":
             if int(db_x["created_at"])>int(date_entry.get()):
              my_time.append(db_x)
            else:
                since_day_time()
                if int(db_x["created_at"])>int(date_entry.get()):
                  my_time.append(db_x) 
         return my_time   
                    
entry_id=tk.Entry(root, textvariable=entry_id_note, width=20,font=("Arial",12,"normal"))
entry_note=tk.Entry(root, textvariable=entry_note_note, width=50)
entry_id.place(relx=0.06,rely=0.22)

draft_user=[]
relay_list=[]
user_metadata={}
List_three=[]

def npub_list_title(List_30000,hex_npub):
   for list_x in List_30000:
      if hex_npub in tags_string(list_x,"p"):
        if tags_string(list_x,"title")!=[]: 
         return str(tags_string(list_x,"title")[0])
        else:
           return str("Undefined")

async def get_relay(client, user):
    f = Filter().author(user).remove_identifiers(["influenceScoresList"]).kinds([Kind(30000)]).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_long_note(client, user):
  try:
   f = Filter().authors(user).kind(Kind(30023)).remove_hashtags(["nosli"]).limit(80)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   return z
  except RelayMessage as e:
      print(e)

async def main_long_tk(authors):
   try: # Init logger
    client = Client(None)
    # Add relays and connect
    relay_url_1=RelayUrl.parse("wss://nostr.mom/")
    relay_url_2=RelayUrl.parse("wss://nos.lol/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    if relay_list!=[]:
       
       for jrelay in relay_list:
          relay_url_list = RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
    await client.connect()     
    await asyncio.sleep(2.0)
    combined_results = await get_relay(client, authors)
    List_note=get_note(combined_results)
    if List_note:
       for jlist in List_note:
         if jlist not in List_three and len(tags_string(jlist,"p"))<200:
            List_three.append(jlist)
            for xuser in tags_string(jlist,"p"):
              if xuser not in draft_user:
                 draft_user.append(xuser)
    if draft_user:
     Draft_User=user_convert(draft_user)
     combined_note = await get_long_note(client, Draft_User)
     combine_get_note=get_note(combined_note)
    if combine_get_note!=[]:
      timeline_published(combine_get_note)
      return combine_get_note
   except NostrSdkError as e:
      print(e) 
   
def create_tm():
  if entry_id.get()!="":
   user=convert_user(entry_id.get())
   test_note=asyncio.run(main_long_tk(user))
   print(len(test_note),len(draft_user))

async def get_outbox(client):
  if my_list!=[]:
   if my_dict[combo_box.get()] in my_list: 
    f = Filter().authors(user_convert([my_dict[combo_box.get()]])).kind(Kind(10002))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def outboxes():
    init_logger(LogLevel.INFO)
    client = Client(None)
    
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          relay_url_list=RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
             
    else:
            relay_url_1=RelayUrl.parse("wss://nostr.mom/")
            relay_url_2=RelayUrl.parse("wss://purplerelay.com/")
            await client.add_relay(relay_url_1)
            await client.add_relay(relay_url_2)
     
       
    await client.connect()
    relay_add=get_note(await get_outbox(client))
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

def search_relay():
   if __name__ == "__main__":
    asyncio.run(outboxes())

async def get_metanota(client):
  if draft_user!=[]:
    print("draft_user ", len(draft_user))
    f = Filter().authors(user_convert(draft_user)).kind(Kind(0))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def metadata_object():
    client = Client(None)
    
    # Add relays and connect
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          relay_url_list=RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
             
    else:
           relay_url_1=RelayUrl.parse("wss://nostr.mom/")
           relay_url_2=RelayUrl.parse("wss://purplerelay.com/")
           await client.add_relay(relay_url_1)
           await client.add_relay(relay_url_2)
              
    await client.connect()
    metadata_page=get_note(await get_metanota(client))
    if metadata_page !=None and metadata_page!=[]:
           #print(metadata_page[0])
           zeta,pub0=metadata_list(metadata_page,"name")
           for name, key in zip(zeta,pub0):
             if name!=None: 
              if len(name)>20:
                 name=name[0:20]
              if name=="":
                name="undefined" 
              user_metadata[name]=key
                        
    await asyncio.sleep(2.0)

def search_metadata():

   if __name__ == "__main__":
      asyncio.run(metadata_object())  
      

def metadata_0(nota,y):
   import json
   try:
    test=json.loads(nota["content"])
    return str(test[y])
   except KeyError as e:
      print(e)

def metadata_list(List,y):
    """
    This function takes one list of note and a metadata tag and \n returns two list name metatag and pubkey.

    Parameters:
    List (list): The list.
    y (str): the metadata tag.

    Returns:
    list: name metatag {zeta} \n
    list: pubkey  {pub0}
    """
    zeta=[]
    pub0=[]
    for j in List:
        zeta.append(metadata_0(j,y))
        pub0.append(j['pubkey'])
    return zeta,pub0

def print_text(): 
   if db_list!=[]:  
    list_frame = ttk.LabelFrame(root, text="list", labelanchor="n", padding=10)
    frame3=tk.Frame(root,height=120,width= 100)
    canvas = tk.Canvas(frame3,width=330)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    s=1     
    if user_metadata=={}:
     search_metadata()
     list_frame.place(relx=0.01,rely=0.35,relwidth=0.33,relheight=0.4)
    
    for note in list(user_metadata.keys()):
           
            var_id=StringVar()
            label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=250)
            var_id.set(note) 
            test=list(user_metadata.keys()).index(note)
            label_id.grid(pady=2,column=1,row=s)

            def print_id(test):
                entry_id_note.set(user_metadata[test])
                if test not in combo_box.get():
                 
                 label_entry_id["text"]=test
                else:
                   
                   label_entry_id["text"]="Pubkey"
                  
            def print_var(test):
                print(user_metadata[test])
                              
            button=Button(scrollable_frame,text=f"{npub_list_title(List_three,user_metadata[note])[0:10]}", command=lambda val=note: print_var(val))
            button.grid(column=0,row=s,padx=20,pady=5)
            button_grid2=Button(scrollable_frame,text=f"click me for id ", command=lambda val=note: print_id(val))
            button_grid2.grid(row=s,column=2,padx=5,pady=5)
            
            root.update()  
            s=s+1
   
    canvas.pack(side="left", fill="y", expand=True)
    scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.03,rely=0.38,relwidth=0.3)      
    
    def Close_print():
       frame3.destroy()  
       list_frame.place_forget()
    
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)    
   else:
      print("test")    

button4=tk.Button(root,text="People List",command=print_text, font=('Arial',12,'bold'))
button4.place(relx=0.07,rely=0.37) 
button4=tk.Button(root,text="Search Post",command=create_tm,font=('Arial',12,'bold'))
button4.place(relx=0.07,rely=0.27) 
frame_upfront=Frame(root)
frame2=Frame(root)

def add_db_list():
        Frame_2=Frame(root)
        Frame_block=Frame(Frame_2,width=50, height=20)
               
        def Close_block(event):
            Frame_block.destroy()
        
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=17, row=1, padx=5, columnspan=1) 
            
        def search_block_list():
            label_string_block1.set(len(db_list))    

        def delete_block_list():
            db_list.clear()
            label_string_block1.set(len(db_list))    
    
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey")
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ")
        random_block1.grid(column=1,row=0,padx=5,pady=5)
        label_string_block1=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1,font=('Arial',12,'bold'))
        label_block_list1.grid(column=1,row=1,padx=5,pady=5)
        Frame_block.grid(column=0,row=6, columnspan=3, rowspan=2)
        Frame_2.place(relx=0.01,rely=0.75)

button_block=tk.Button(root, highlightcolor='WHITE',text='DB count',font=('Arial',12,'bold'),command=add_db_list)
button_block.place(relx=0.02,rely=0.85) 
frame2.grid(column=0, row=0,columnspan=3, rowspan=4,pady=10)
frame_upfront.grid()
int_var=IntVar()
int_var.set(1)

def note_number():
    if db_list!=[]:
      if int((int(lbel_var.get())+1))< int((len(list_timeline(combo_note.get()))/16)+1):
          int_var.set(int(lbel_var.get())+1)
          show_Teed()
      else:
          if int((len(list_timeline(combo_note.get()))/16))==0:
           int_var.set(int(1)) 
          else:
           if len(db_list)>80:
            if  int((int(lbel_var.get()))+1)>=int((len(list_timeline(combo_note.get()))/16)+1):   
             if int((int(lbel_var.get()))+1)<int((len(list_timeline(combo_note.get()))/16)+2):
              int_var.set(int(lbel_var.get())+1)
             
              show_Teed() 
           else: 
            int_var.set(int(1))     
            show_Teed()
          
def back_number():
    if int((int(lbel_var.get())-1))>=1:
        int_var.set(int(lbel_var.get())-1)
        show_Teed()
    else:
        int_var.set(1) 
        #show_Teed()

button_next=Button(root,command=note_number,text="➕",font=("Arial",12,"bold"))
button_back=Button(root,command=back_number,text="➖",font=("Arial",12,"bold"))
db_list=[]
lbel_var=Entry(root, textvariable=int_var,font=("Arial",12,"bold"),background="grey") 

def show_Teed():
 frame2=tk.Frame(root)  
 canvas_1 = tk.Canvas(frame2)
 scrollbar_1 = ttk.Scrollbar(frame2, orient="vertical", command=canvas_1.yview)
 scrollable_frame_1 = ttk.Frame(canvas_1)

 scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all")
    )
)

 canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
 canvas_1.configure(yscrollcommand=scrollbar_1.set)

 def create_page(db_list_,s):
  if db_list_!=[] and db_list_!=None:
  
    n=16*(s-1)
    l=s*16
    for note in db_list_[n:l]:
     try:
      if note["pubkey"] in list(user_metadata.values()):
        value=list(user_metadata.values()).index(note["pubkey"])    
        context0="Nickname "+list(user_metadata.keys())[value]+"\n"
      else:  
         context0="Pubkey "+note['pubkey']+"\n"
      if note['tags']!=[]:
        context1="Content lenght "+str(len(note["content"]))+"\n"
        context2="\n"
        if tags_string(note,"title")!=[]: 
         xnote= "Title: "+str(tags_string(note,"title")[0])
         context2=context2+str(xnote) +"\n"
        else: 
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
           number=list(db_list).index(entry)
           print("number ", number," of ", len(db_list))
           show_print_test(entry)       
                          
      def print_var(entry):
                print(entry["content"])
           
      button=Button(scrollable_frame_1,text=f"Print me ", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s,column=1,padx=5,pady=5)      
   
      s=s+2  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.35,rely=0.22,relwidth=0.30,relheight=0.4)
    
    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
        button_next.place_forget()
        button_back.place_forget()
        lbel_var.place_forget()
        button_f_close.place_forget()
    
    button_next.place(relx=0.55,rely=0.17, anchor="n")
    button_back.place(relx=0.40,rely=0.17, anchor="n",x=1)
    lbel_var.place(relx=0.475,rely=0.17, anchor="n",relwidth=0.02)

    def close_number() -> None :
        frame2.destroy()    
        button_frame.place_forget()
        button_next.place_forget()
        button_back.place_forget()
        lbel_var.place_forget()
        button_f_close.place_forget()
        
    button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"))
    button_f_close.place(relx=0.6,rely=0.17)      
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.44,rely=0.65,relwidth=0.1)  
    
 s=1
 create_page(list_timeline(combo_note.get()), int(lbel_var.get()))
 root.update_idletasks()
 
button_id=tk.Button(root,command=show_Teed,text="Read",font=("Arial",12,"normal"))
button_id.place(relx=0.26,rely=0.08)

def show_print_test(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3)
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
   if note["pubkey"] in list(user_metadata.values()):
      value=list(user_metadata.values()).index(note["pubkey"])
      context0="Pubkey: "+list(user_metadata.keys())[value]+"\n"+"Tag d: "+tags_string(note,"d")[0]+"\n"
   else:
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
   second_label10 = tk.Text(scrollable_frame_2, padx=8, height=5, width=28, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   second_label10.insert(END,context1+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label10.yview )
   second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
      
   def print_zap(entry):
            stringa_nota.set(entry["id"])
            amount_zap()

   def print_var(entry):
        if entry["tags"]!=[]:
          if tags_string(entry,"image")!=[]: 
           print("see this photo: ", tags_string(entry,"image")[0])
           photo_print(entry)

   def print_content(entry):
       result=show_note_from_id(entry)
       if result!=None and result!=[]: 
        s=1
        for jresult in result:
           try:  
             if jresult['pubkey'] in list(user_metadata.values()):
                 value=list(user_metadata.values()).index(jresult["pubkey"])
                 context00="Pubkey: "+list(user_metadata.keys())[value]+"\n "+str(jresult["created_at"])+"\n"
             else:
                context00="Pubkey : "+jresult['pubkey']+"\n"+"Time: "+str(jresult["created_at"])+"\n"
             if jresult['tags']!=[]:
              context11="\n"+jresult['content']+"\n"
              tag_note=""
              for note_x in note["tags"]:
                tag_note=tag_note+ str(note_x)+"\n"
                context22="[[ Tags ]]"+"\n" +tag_note
             else: 
              context11="content: "+"\n"+jresult['content']+"\n"
              context22=""
             var_id_1=StringVar()
             label_id_1 = Message(scrollable_frame_2,textvariable=var_id_1, relief=RAISED,width=300,font=("Arial",12,"normal"))
             var_id_1.set(context00)
             label_id_1.grid(pady=2,column=0, columnspan=3)
             scroll_bar_mini_2 = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_2.grid( sticky = NS,column=4,pady=5,row=s+6)
             second_label20 = tk.Text(scrollable_frame_2, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini_2.set, font=('Arial',14,'bold'),background="#D9D6D3")
             second_label20.insert(END,context11+"\n"+str(context22))
             scroll_bar_mini_2.config( command = second_label20.yview )
             second_label20.grid(padx=10, column=0, columnspan=3,row=s+6) 
             s=s+2
           except TypeError as e:
              print (e)      
              
   button=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Tips ", command=lambda val=note: print_zap(val))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
   button_grid3=Button(scrollable_frame_2,text=f"this a reply ", command=lambda val=note: print_content(val))
   button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()    

   button_frame=Button(scrollable_frame_2,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.grid(row=s+3,column=1,padx=5,pady=5)
   frame3.place(relx=0.65,rely=0.31,relwidth=0.3,relheight=0.45 ) 

def db_list_id(json_list):
    db_list_with_id=[]
    for json_z in json_list:
        if json_z["id"] not in db_list_with_id:
          db_list_with_id.append(json_z["id"]) 
    return db_list_with_id       

def db_list_nota(nota_id):
    #global list
    for nota_x in db_list:
        if nota_x["id"]==nota_id:
            return nota_x

def show_note_from_id(note):
      try:  
        quote_e=nota_reply_id(note)
        replay_light=[]
        db_already=[]
        items=[]
        if quote_e!=[]:
           for replay_x in quote_e:
               if replay_x not in db_list_id(db_list):
                  replay_light.append(replay_x) 
               else:
                   db_already.append(replay_x)
           if replay_light!=[]: 
            print("search")         
            items=get_note(asyncio.run(Get_event_id(replay_light)))
           if db_already!=[]:
               for db_x in db_already:
                   if db_x  in db_list_id(db_list):
                    items.append(db_list_nota(db_x)) 
        else:
            print("quote_e empty")
            
        coord_event=""    
        if note["kind"]==int(30023):
           coord = Coordinate(Kind(note["kind"]),PublicKey.parse(note["pubkey"]),str(tags_string(note,"d")[0]))
           coordinate = Nip19Coordinate(coord, [])
           tag_id=Coordinate.parse(coordinate.to_bech32())
           
           coord_event=str(tag_id)
           resp_answer=asyncio.run(Get_A_tag(coord_event))
        if resp_answer!=None:
            for resp_x in resp_answer:
             if resp_x not in items:
              items.append(resp_x)
        if items!=[]:     
         for itemsj in items:
            if itemsj not in db_list:
                db_list.append(itemsj)   
         return items
        else:
           return None   
      except TypeError as e:
         print (e)
         return None  
       
def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id                

async def Get_A_tag(event_):
      
    client = Client(None)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          relay_url_list = RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
    else:
         relay_url_1=RelayUrl.parse("wss://nostr.mom/")
         relay_url_2=RelayUrl.parse("wss://purplerelay.com/")
         relay_url_3=RelayUrl.parse("wss://relay.primal.net")
         await client.add_relay(relay_url_1)
         await client.add_relay(relay_url_2)
         await client.add_relay(relay_url_3)
    
    await client.connect()
    
    test_id = await get_a_ers_Event(client,event_)
    if test_id!=[]:
     return get_note(test_id)

async def get_a_ers_Event(client, event_):
   
    f=Filter().kinds([Kind(1111),Kind(1)]).custom_tag(SingleLetterTag.lowercase(Alphabet.A),event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    print(f.as_json(),len(z))
    return z

async def get_answers_Event(client, event_):
    f = Filter().events(evnts_ids(event_)).kinds([Kind(1),Kind(1111)]).limit(int(10*len(event_)))
    
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_one_Event(client, event_):
    f = Filter().id(evnt_id(event_))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_answer_Event(client, event_):
    f = Filter().event(evnt_id(event_)).kinds([Kind(1),Kind(1111)]).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_notes_(client, e_ids):
     f = Filter().ids([EventId.parse(e_id) for e_id in e_ids])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec() if event.verify()]
     return z

async def get_one_note(client, e_id):
    f = Filter().id(EventId.parse(e_id))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_event_id(e_id):
    client = Client(None)
    relay_url_1=RelayUrl.parse("wss://nostr.mom/")
    relay_url_2=RelayUrl.parse("wss://purplerelay.com/")
    relay_url_3=RelayUrl.parse("wss://purplerelay.com/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    await client.add_relay(relay_url_3)
    await client.connect()
    await asyncio.sleep(2.0)

    if isinstance(e_id, list):
         print("list")
         test_id = await get_notes_(client,e_id)
         resp_answer=await get_answers_Event(client,e_id)
         if resp_answer!=[]:
          for resp in resp_answer:
            if resp not in test_id:
             test_id.append(resp)
    else:
        print("str")
        test_id = await get_one_note(client,e_id)
        resp_answer=await get_answer_Event(client, e_id)
        if resp_answer!=[]:
         for resp in resp_answer:
          if resp not in test_id:
           test_id.append(resp)
    return test_id

async def get_one_Event(client, event_):
    f = Filter().id(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_id(event_):
    
    client = Client(None)
    
    relay_url_1=RelayUrl.parse("wss://nostr.mom/")
    relay_url_2=RelayUrl.parse("wss://purplerelay.com/")
    relay_url_3=RelayUrl.parse("wss://relay.primal.net")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    await client.add_relay(relay_url_3)

    await client.connect()
    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        print("errore")
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

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
    
    relay_url_1=RelayUrl.parse("wss://relay.damus.io/")
    relay_url_2=RelayUrl.parse("wss://purplerelay.com/")
    relay_url_3=RelayUrl.parse("wss://relay.primal.net")
    relay_url_4=RelayUrl.parse("wss://nos.lol/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    await client.add_relay(relay_url_3)
    await client.add_relay(relay_url_4)

    await client.connect()
    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_relays_z(client, authors)
    else:
        combined_results = await get_relay_z(client, authors)
    
    return combined_results    

#photo

def url_spam_image(x):
 if tags_string(x,"image")!=[]:
  z=tags_string(x,"image")[0]
  for j in z.split():
    if j[0:5]=="https":
        return str(j)

def codifica_link(x):
   f=url_spam_image(x)
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

def photo_print(note):
  if codifica_link(note)=="pic":
   frame_pic=tk.Frame(root,height=20,width= 80)
   stringa_pic=StringVar()
   stringa_pic.set(url_spam_image(note))
   label_pic = Entry(frame_pic, textvariable=stringa_pic)
   image_label = tk.Label(frame_pic)
   image_label.grid(column=0,row=0, padx=10,pady=10)
   if label_pic.get()!="":
      try:
       headers = {"User-Agent": "Mozilla/5.0"}
       response = requests.get(label_pic.get(),headers=headers, stream=True)
       
       response.raise_for_status()  
        
   
       if response.ok==TRUE:
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
        
        button_close.grid(column=2,row=0,padx=10)
        frame_pic.place(relx=0.8,rely=0.01,relwidth=0.3,relheight=0.3,anchor="n")
      except TypeError as e: 
        print(e)  
      except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")  
#Zap

def reply_id_zap():
   event=pre_nota_tag.get()
   search_id=evnt_id(event)
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
    if callback!="" and callback!=None:
        request,amount_=asyncio.run(zap_request(note, callback))
    else:
       return None,None,None
   if __name__ == '__main__':
     invoice,preimage=asyncio.run(main_2(callback,amount_))
   return invoice,request,preimage  

pre_image_tag = tk.Label(root, text="call lnurlp")
entry_preimage=ttk.Entry(root,justify='left')

def zap_id_note2():
  if pre_nota_tag.get()!="":
   invoice,request,preimage=zap_id_note()
   pre_image_tag.place(relx=0.75,rely=0.9,relwidth=0.1,relheight=0.05 )
   entry_preimage.place(relx=0.75,rely=0.95,relwidth=0.2 ) 
   if __name__ == '__main__':
       if preimage!=None:
          asyncio.run(zap_ing(invoice,preimage,request))
          
   else:
          print("Error")
          entry_preimage.insert(0, "Error ") 

stringa_nota=tk.StringVar()
pre_nota_lab = tk.Label(root, text="Inser a noteId")
pre_nota_tag = tk.Entry(root, textvariable=stringa_nota)
button_zap_id=tk.Button(root,text="send zap id", background="darkgrey", command=zap_id_note2)

async def zap_request(test, callback):
    keys = Keys.generate()
    signer = NostrSigner.keys(keys)
   
    client = Client(signer)
    relay_url_1=RelayUrl.parse("wss://nostr.mom")
    await client.add_relay(relay_url_1)
    await client.connect()
    metadata = MetadataRecord(
        name="Just The Second",
        display_name="Just The Second",
        lud16="wildcat35@coinos.io") 
        #about="",
        #picture="",
        #banner="", 
        #nip05="",
        

    metadata_obj = Metadata.from_record(metadata)
    await client.set_metadata(metadata_obj)
       
    public_key_ = PublicKey.parse(test['pubkey'])
    relays = [RelayUrl.parse("wss://nostr.mom/")]
    msg = "Zap!"
    amount_=int(int(select_number.get())*1000)
    url=callback
    data = ZapRequestData(public_key_, relays).message(msg).amount(amount_).lnurl(url)
    public_zap_ = EventBuilder.public_zap_request(data).sign_with_keys(keys)               #to_event(keys)
    return public_zap_,amount_

async def zap_ing(invoice,preimage,public_zap_):
    # Compose client
    keys = Keys.generate()
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    relay_url_1=RelayUrl.parse("wss://relay.damus.io/")
    relay_url_2=RelayUrl.parse("wss://purplerelay.com/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)

    await client.connect()
    metadata = MetadataRecord(
        name="Just The Second",
        display_name="Just The Second",
        lud16="wildcat35@coinos.io") 
        #about="",
        #picture="",
        #banner="", 
        #nip05="",
        

    metadata_obj = Metadata.from_record(metadata)
    await client.set_metadata(metadata_obj)
        
    eventis_= EventBuilder.zap_receipt(invoice,preimage,public_zap_ )
    await client.send_event_builder(eventis_)
       
    print(f"Public zap event: {eventis_}\n")
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     if event.verify():
         print(event.as_json())

def fetch_lud_16(note):
 public_key_=PublicKey.parse(note['pubkey'])
 kind_0=search_kind(public_key_,0)
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

def qrcode_f(invoice):
    for j in invoice.split():
        if j[0:4]=="lnbc":
         import qrcode
         img = qrcode.make(invoice)
         img.show()

pre_image_tag_1 = tk.Label(root, text="call lnurlp")
entry_preimage_1=ttk.Entry(root,justify='left')

async def main_2(url,amount_):
    # create the background task
    task = asyncio.create_task(background())
    # allow the background task to start executing
    await asyncio.sleep(0)
    pre_image_tag_1.place(relx=0.55,rely=0.9,relwidth=0.1,relheight=0.05 )
    entry_preimage_1.place(relx=0.55,rely=0.95,relwidth=0.2 ) 
    entry_preimage_1.insert(0,url)
    
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
         data_test3=json.loads(r4.text)
         print(data_test3)
         data_test4= data_test3["pr"]
     except KeyError as e:
        print(e)
        return None,None    
    qrcode_f(data_test4)
    task2 = await background2(data_test3)
    if task2:
     return data_test4,task2
    else:
       
       return None,None

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

async def background():
    while True:
        print('Running in the background...')
        await asyncio.sleep(0.01)

def val_number(number:int):
   number_string.set(number)

def amount_zap():
    number_string.set(0)
    zap_long_split()
    button_zap_1=tk.Button(root,text="5", background="darkgrey", command=lambda val=5: val_number(val))
    button_zap_1.place(relx=0.7,rely=0.76)   
    button_zap_2=tk.Button(root,text="10", background="darkgrey", command=lambda val=10: val_number(val))
    button_zap_2.place(relx=0.75,rely=0.76)   
    button_zap_3=tk.Button(root,text="20", background="darkgrey", command=lambda val=20: val_number(val))
    button_zap_3.place(relx=0.8,rely=0.76)   
    button_zap_4=tk.Button(root,text="50", background="darkgrey", command=lambda val=50: val_number(val))
    button_zap_4.place(relx=0.7,rely=0.8)   
    button_zap_5=tk.Button(root,text="100", background="darkgrey", command=lambda val=100: val_number(val))
    button_zap_5.place(relx=0.75,rely=0.8)   
    button_zap_6=tk.Button(root,text="200", background="darkgrey", command=lambda val=200: val_number(val))
    button_zap_6.place(relx=0.8,rely=0.8)  
    select_number.place(relx=0.7,rely=0.85)

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
       pre_image_tag.place_forget()
       entry_preimage.place_forget()
       pre_image_tag_1.place_forget()
       entry_preimage_1.place_forget()
      
    button_zap_c=tk.Button(root,text="close X", command=close_stuff,fg="red")
    button_zap_c.place(relx=0.85,rely=0.76)       
    button_zap_o1=tk.Button(root,text=f"Zap", background="grey", command=zap_id_note2)
    button_zap_o1.place(relx=0.8,rely=0.85)    

button_zap_o=tk.Button(root,text="Zap it!", background="darkgrey", command=amount_zap)
number_string=IntVar()
select_number=Entry(root, textvariable=number_string,font=('Arial',12,'bold'),width=10)
mortage=IntVar() 
percent_value=tk.Entry(root, textvariable=mortage)

def zap_long_split():
   pubkey,relay,percent,note=zap_recepient_split()
   if (len(pubkey)==int(1) and note["pubkey"]==pubkey[0]) or pubkey==[]:
      pass
      #as usually
   else:   
      def on_select_pub(event):
        if combo_pox.get() in list(user_metadata.values()):
         value=list(user_metadata.values()).index(combo_pox.get())
         selected_name = list(user_metadata.keys())[value]
         name_key["text"]=str(selected_name)
         name_key.place(relx=0.92,rely=0.85)
         selected_item = combo_pox.get()
        else:
          selected_item = combo_pox.get()  
          name_key["text"]=""
        mortage.set(int((tags_values(pubkey,percent,selected_item)/100)*int(select_number.get())))
      name_key = tk.Label(root, text="")  
      combo_pox = ttk.Combobox(root, values=pubkey)
      combo_pox.place(relx=0.88,rely=0.9)
      combo_pox.set("Zap_user")
      combo_pox.bind("<<ComboboxSelected>>", on_select_pub)    
      
      
      percent_value.place(relx=0.8,rely=0.9,relwidth=0.05)
      def zap_pubkey_note():
       if int(percent_value.get())>0: 
        if __name__ == '__main__':
          callback=fetch_lud_16_pubkey(combo_pox.get())
          if callback!="" and callback!=None:
           request,amount_=asyncio.run(zap_request_split(combo_pox.get(),int(percent_value.get()),callback))
          else:
             return None,None,None

        if __name__ == '__main__':
          invoice,preimage=asyncio.run(main_2(callback,amount_))
          return invoice,request,preimage  
       else:
           return None,None,None
   
      def zap_pubkey_note2():
        if pre_nota_tag.get()!="":
          invoice,request,preimage=zap_pubkey_note()
          pre_image_tag.place(relx=0.55,rely=0.9,relwidth=0.1,relheight=0.05 )
          entry_preimage.place(relx=0.55,rely=0.95,relwidth=0.2 ) 
          if __name__ == '__main__':
            if preimage!=None:
              asyncio.run(zap_ing(invoice,preimage,request))
            else:
                if int(percent_value.get())<=0: 
                   pre_image_tag['text']="Error"
                   entry_preimage.insert(0, "Error value")
                else:
                 print("Error")
                 entry_preimage.insert(0, "Error ") 

      def close_o():
       entry_preimage.place_forget()
       pre_image_tag.place_forget()
       button_c.place_forget()
       button_zap_user.place_forget()
       combo_pox.place_forget()  
       percent_value.place_forget()
       name_key.place_forget()

      button_c=tk.Button(root,text="close X", background="darkgrey", command=close_o)
      button_c.place(relx=0.95,rely=0.8)   
      button_zap_user=tk.Button(root,text="Zap-Split",command=zap_pubkey_note2)
      button_zap_user.place(relx=0.7,rely=0.9)    

def zap_recepient_split():
   note=reply_id_zap()
   pubkey=[]
   relay=[]
   percent=[]
   if tags_string(note,"zap")!=[]:
      for tags_z in tags_str(note,"zap"):
         pubkey.append(tags_z[1])
         relay.append(tags_z[2])
         percent.append(int(tags_z[3]))
   if len(pubkey)==len(relay)==len(percent):       
    return pubkey,relay,percent,note       

def tags_values(key:list,value:list,s:str):
    if s in key:
       index=key.index(s) 
       
    return value[index]

def fetch_lud_16_pubkey(hex_pubkey):
 public_key_=PublicKey.parse(hex_pubkey)
 kind_0=search_kind(public_key_,0)
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

async def zap_request_split(hex_npub,percent, callback):
    # Compose client
    keys = Keys.generate()
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    relay_url_1=RelayUrl.parse("wss://nostr.mom")
    await client.add_relay(relay_url_1)
    await client.connect()
        
    public_key_ = PublicKey.parse(hex_npub)
    relays = [RelayUrl.parse("wss://nostr.mom/")]
    msg = "Zap!"
    amount_=int(int(percent))*1000
    url=callback
    data = ZapRequestData(public_key_, relays).message(msg).amount(amount_).lnurl(url)
    public_zap_ = EventBuilder.public_zap_request(data).sign_with_keys(keys)               #to_event(keys)
    return public_zap_,amount_       

root.mainloop()         
        


