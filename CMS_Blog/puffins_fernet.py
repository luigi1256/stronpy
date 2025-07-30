#notification + reply
import tkinter as tk
from tkinter import *
from tkinter import ttk
import asyncio
from nostr_sdk import *
import json
from datetime import timedelta
import re
import requests
import shutil
from PIL import Image, ImageTk
from tkinter import messagebox 
from nostr_sdk import *
import asyncio
from datetime import timedelta
import io
from cryptography.fernet import Fernet

#Nostr static function

def get_note(z):
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f

def convert_user(x):
    try:
     other_user_pk = PublicKey.parse(x)
     return other_user_pk
    except NostrSdkError as e:
       print(e,"this is the hex_npub ",x)

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

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

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

root = Tk()
root.title("Test")
root.geometry("1250x800")
frame1=tk.Frame(root,height=100,width=200)

comment_frame = ttk.LabelFrame(root, text="Comment Post", labelanchor="n", padding=10)
preview_c_frame = ttk.LabelFrame(root, text="Preview Post", labelanchor="n", padding=10)
note_c_tag = tk.Label(root, text="Note",font=('Arial',12,'normal'))
entry_c_4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
enter_c_note = tk.Label(root, text="Comment Note")
entry_c_note=ttk.Entry(root,justify='left')
enter_c_root = tk.Label(root, text="Root Note")
entry_c_root=ttk.Entry(root,justify='left')

async def get_nostr_tags(client, event_kind,event_identifier,event_publickey):
     f = Filter().kind(event_kind).author(event_publickey).identifier(event_identifier)
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec()]
     return z

async def get_one_nostr_tags(client, event_kind,event_identifier,event_publickey):
    f =Filter().kind(event_kind).author(event_publickey).identifier(event_identifier)
    #print(f.as_json())    
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_coord_url(value):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    event_kind = Coordinate.parse(value).kind()
    event_identifier = Coordinate.parse(value).identifier()
    event_publickey = Coordinate.parse(value).public_key()
    
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    await client.try_connect(timeout=timedelta(seconds=10))

    await asyncio.sleep(2.0)
    await client.connect()
    
    if isinstance(value, list):
         print("list0")
         test_id = await  get_nostr_tags(client,event_kind,event_identifier,event_publickey)
    else:
        print("str0")
        test_id = await get_one_nostr_tags(client,event_kind,event_identifier,event_publickey)
       
    return test_id

def found_root(note):
   try_note=get_note(note)
   Test_root=[]
   if tags_string(try_note[0],"A")!=[]:
     test_note=asyncio.run(Get_coord_url(str(tags_string(try_note[0],"A")[0])))
     return test_note
   if tags_string(try_note[0],"E")!=[]:
     found_nota=asyncio.run(Get_id(tags_string(try_note[0],"E")))
     return found_nota
   if tags_string(try_note[0],"I")!=[]:
     print(tags_string(try_note[0],"I")[0])          

async def reply(note,tag):
  # Init logger
  init_logger(LogLevel.INFO)
  key_string=log_these_key()
  if key_string!=None: 
    keys = Keys.parse(key_string)
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay("wss://nostr.mom")
     await client.add_relay("wss://nos.lol")
    await client.connect()
    event_to_comment:dict=tag
    if event_to_comment!=NONE:
     if Event.from_json(f"{event_to_comment}").kind().as_u16()!=(1,1111):    
      print(Event.from_json(f"{event_to_comment}").kind().as_u16()) 
      builder =EventBuilder.comment(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_comment}"),None)
      print(builder)
      test = await client.send_event_builder(builder)
     
      if first_reply==[]:
       pass
       first_reply.append(test.id.to_hex())
      else:
       
       first_reply.clear()

       first_reply.append(test.id.to_hex())

      metadata = MetadataRecord(
        name="Just The Second",
        display_name="Just The Second") 
        #about="",
        #picture="",
        #banner="", 
        #nip05="",
        #lud16="")

      metadata_obj = Metadata.from_record(metadata)
      await client.set_metadata(metadata_obj)

      print("Event sent:")
    
      await asyncio.sleep(2.0)

    # Get events from relays
      print("Getting events from relays...")
      f = Filter().authors([keys.public_key()])
      events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
      for event in events.to_vec():
       print(event.as_json())

def round_3_comment():      
  if entry_c_note.get()!="" and entry_c_root.get()!="":
    search_list_id=[]
    event=entry_c_note.get()
    search_id_2=entry_c_root.get()
    search_list_id.append(event) 
    search_list_id.append(search_id_2)
    print(search_list_id)
    found_nota=asyncio.run(Get_id(search_list_id))
    
    return found_nota 

def second_reply():
  if entry_c_4.get()!="":
    note=entry_c_4.get()
    tag=round_3_comment()
    if len(tag)>=2 and tag!=None:  
        if __name__ == '__main__':
         asyncio.run(the_second_reply(note,tag[0],tag[1]))  #need to check if tag[0] is the reply and tag[1] is the root
    else:
       print(len(tag),"\n", tag) 
    close_comment()

button_reply_c=tk.Button(root,text="send comment", background="darkgrey", command=second_reply, font=('Arial',12,'normal'))
note_c_tag1 = tk.Label(root, text="e"+" event_id",font=('Arial',12,'normal'))
button_pre_c=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))
close_c=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))

root_thread_list=[]
first_reply=[]
other_reply=[]
relay_list=[] 

def third_open(note):
   list_root=found_root(note)
   list_root_get=get_note(list_root)
   if root_thread_list==[] and len(note["id"])==64:
    root_thread_list.append(list_root_get[0])
    note_c_tag1['text']="id " +note["id"][0:9]
    entry_c_note.delete(0, END)
    entry_c_note.insert(0, note["id"])
    entry_c_root.delete(0, END)
    entry_c_root.insert(0, root_thread_list[0]["id"])
    comment_frame.place(relx=0.82,rely=0.1,relwidth=0.3,relheight=0.33,anchor='n' )
    note_c_tag.place(relx=0.74,rely=0.13,relwidth=0.1,relheight=0.1,anchor='n' )
    entry_c_4.place(relx=0.82,rely=0.2,relwidth=0.25,relheight=0.1,anchor='n' )
    #entry_layout-right
    enter_c_note.place(relx=0.7,rely=0.02,relwidth=0.1 )
    entry_c_note.place(relx=0.7,rely=0.06,relwidth=0.1)
    enter_c_root.place(relx=0.83,rely=0.02,relwidth=0.1 )
    entry_c_root.place(relx=0.83,rely=0.06,relwidth=0.1)
    note_c_tag1.place(relx=0.92,rely=0.16,anchor='n' )
    
    close_c["command"] = close_comment
    close_c.place(relx=0.82,rely=0.13,anchor='n' )

    def Preview():
     if entry_c_4.get()!="": 
        frame1=Frame(root, width=310, height=100)
   
        canvas = Canvas(frame1)
        canvas.pack(side="left", fill=BOTH, expand=True)

        canvas.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Frame scrollabile
        scrollable_frame = Frame(frame1)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
        def create_note(note_text, s):
          if len(note_text)<241:
            message = Message(scrollable_frame, text=note_text, width=280, font=('Arial',12,'normal'))
            message.grid(row=s, column=0, columnspan=3, padx=5, pady=10)
            
          else:
            message = Message(scrollable_frame, text=note_text[0:240]+"...", width=280, font=('Arial',12,'normal'))
            message.grid(row=s, column=0, columnspan=3, rowspan=2, padx=5, pady=10)
          
        s = 1
        while s<2:
         if entry_c_4.get()!="":
            create_note(entry_c_4.get(), s)
         s += 2   
        frame1.place(relx=0.8,rely=0.45, relheight=0.25,relwidth=0.2)  

        def close_canvas():
            scrollable_frame.forget()
            canvas.destroy()
            frame1.destroy()
            root_thread_list.clear()
            preview_frame.place_forget()
            
        button_c_close=Button(scrollable_frame, command=close_canvas, text="Close X")
        button_c_close.grid(column=1,row=0, padx=10,pady=10)   
        
    button_pre_c["command"]= Preview
    button_pre_c.place(relx=0.78,rely=0.33,relwidth=0.1, anchor="n") 
    button_reply_c.place(relx=0.88,rely=0.33,relwidth=0.1,relheight=0.05,anchor='n' )
        
def close_comment():
  button_reply_c.place_forget() 
  comment_frame.place_forget()
  button_pre_c.place_forget()  
  note_c_tag.place_forget()  
  entry_c_4.place_forget()
  enter_c_note.place_forget()
  entry_c_note.place_forget()
  note_c_tag1.place_forget()
  close_c.place_forget()
  entry_c_4.delete(0, END)
  enter_c_root.place_forget()
  entry_c_root.place_forget()

def Open_json_fake_note(name):
            stringaJson=""
            try: 
             with open(name+str(".json"),"r") as file:
              for line in file:
               stringaJson+=line
              datoEstratto=json.loads(stringaJson)
              #print (datoEstratto, type(datoEstratto))            
              return datoEstratto
            except FileNotFoundError as e:
               print(e)

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

async def the_second_reply(note,tag, root):
    # Init logger
  init_logger(LogLevel.INFO)
  key_string=log_these_key()
  if key_string!=None: 
    keys = Keys.parse(key_string)
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay("wss://nostr.mom")
     await client.add_relay("wss://nos.lol")
    await client.connect()
    event_to_comment:dict=tag
    event_to_start:dict=root
    if event_to_comment!=NONE and event_to_start!=None:
     if Event.from_json(f"{event_to_comment}").kind().as_u16()==1111:
      if Event.from_json(f"{event_to_start}").kind().as_u16()== (30023):
        builder =EventBuilder.comment(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_start}"),None)
    
      test= await client.send_event_builder(builder)

     if other_reply==[]:
      other_reply.append(test.id.to_hex())
     else:
      
      other_reply.append(test.id.to_hex())
     metadata = MetadataRecord(
        name="Just The Second",
        display_name="Just The Second") 
        #about="",
        #picture="",
        #banner="", 
        #nip05="",
        #lud16="")

     metadata_obj = Metadata.from_record(metadata)
     await client.set_metadata(metadata_obj)
     await asyncio.sleep(2.0)
    # Get events from relays
     print("Getting events from relays...")
     f = Filter().authors([keys.public_key()])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     for event in events.to_vec():
      print(event.as_json())

async def get_more_Event(client, event_list):
    f = Filter().ids(event_list)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_one_Event(client, event_):
    f = Filter().id(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay(" wss://nostr.mom/")
     await client.add_relay("wss://nos.lol/")
     await client.add_relay("wss://relay.primal.net")
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        test_kind = await get_more_Event(client, event_)
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

def reply_note():
  if entry4.get()!="" and entry_note.get()!="": 
    if __name__ == '__main__':
     note=entry4.get()
     tag=reply_note_comment()
     if tag!=None:
      asyncio.run(reply(note,tag))
  close_answer()

Reply_frame = ttk.LabelFrame(root, text="Reply Post", labelanchor="n", padding=10)
button_reply_t=tk.Button(root,text="send reply", background="darkgrey", command=reply_note, font=('Arial',12,'normal'))
preview_frame = ttk.LabelFrame(root, text="Preview Post", labelanchor="n", padding=10)
note_tag = tk.Label(root, text="Note",font=('Arial',12,'normal'))
entry4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
enter_note = tk.Label(root, text="Root Note")
entry_note=ttk.Entry(root,justify='left') 
button_pre=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))
note_tag1 = tk.Label(root, text="e"+" event_id",font=('Arial',12,'normal'))
close_=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))

def close_answer():
  button_reply_t.place_forget() 
  Reply_frame.place_forget()
  button_pre.place_forget()  
  note_tag.place_forget()  
  entry4.place_forget()
  enter_note.place_forget()
  entry_note.delete(0, END)
  entry_note.place_forget()
  note_tag1.place_forget()
  close_.place_forget()
  entry4.delete(0, END)

def reply_note_comment():   
  if entry_note.get()!="":
    event=entry_note.get()
    search_id=evnt_id(event)
    found_nota=asyncio.run(Get_id(search_id))
    return found_nota[0]

def test_open(note):
   if note["kind"]==30023:
    if root_thread_list!=[]:
       root_thread_list.clear()
    root_thread_list.append(note["id"])
    note_tag1['text']=str("id " +str(root_thread_list[0][0:9]))
    entry_note.delete(0, END)
    entry_note.insert(0, root_thread_list[0])
    Reply_frame.place(relx=0.5,rely=0.1,relwidth=0.3,relheight=0.33,anchor='n' )
    note_tag.place(relx=0.42,rely=0.13,relwidth=0.1,relheight=0.1,anchor='n' )
    entry4.place(relx=0.5,rely=0.2,relwidth=0.25,relheight=0.1,anchor='n' )
    #entry_layout-right
    enter_note.place(relx=0.35,rely=0.02,relwidth=0.1 )
    entry_note.place(relx=0.35,rely=0.06,relwidth=0.1)
    note_tag1.place(relx=0.58,rely=0.16,anchor='n' )
    
    close_["command"] = close_answer
    close_.place(relx=0.5,rely=0.13,anchor='n' )

    def Preview():
     if entry4.get()!="": 
        frame1=Frame(root, width=310, height=100)
   
        canvas = Canvas(frame1)
        canvas.pack(side="left", fill=BOTH, expand=True)

        canvas.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Frame scrollabile
        scrollable_frame = Frame(frame1)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
        def create_note(note_text, s):
          if len(note_text)<241:
            message = Message(scrollable_frame, text=note_text, width=240, font=('Arial',12,'normal'))
            message.grid(row=s, column=0, columnspan=3, padx=5, pady=10)
            
          else:
            message = Message(scrollable_frame, text=note_text[0:240]+"...", width=240, font=('Arial',12,'normal'))
            message.grid(row=s, column=0, columnspan=3, rowspan=2, padx=5, pady=10)
            
        s = 1
        while s<2:
         if entry4.get()!="":
            create_note(entry4.get(), s)
         s += 2   
        frame1.place(relx=0.38,rely=0.45, relheight=0.3,relwidth=0.35)  

        def close_canvas():
            scrollable_frame.forget()
            canvas.destroy()
            frame1.destroy()
            root_thread_list.clear()
            preview_frame.place_forget()
            
        button_close=Button(scrollable_frame, command=close_canvas, text="Close X")
        button_close.grid(column=1,row=0, padx=10,pady=10)   
        #preview_frame.place(relx=0.45,rely=0.4,relwidth=0.3,relheight=0.3,anchor='n' )
    
    button_pre["command"]= Preview
    button_pre.place(relx=0.45,rely=0.33,relwidth=0.1, anchor="n") 
    button_reply_t.place(relx=0.55,rely=0.33,relwidth=0.1,relheight=0.045,anchor='n' )
   else:
      if root_thread_list!=[]:
       root_thread_list.clear()
      third_open(note) 
    
note_tag = tk.Label(root, text="Note",font=('Arial',12,'bold'))
entry4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
str_test=StringVar()
entry_note=ttk.Entry(root,justify='left', textvariable=str_test)

relay_list=[]
List_note_write=[]

button_pre=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',12,'bold'))

close_=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))

event_idone=Button(root,text="Search_event_one", font=('Arial',12,'normal') ) 

def Open_json_fake_note(name):
            stringaJson=""
            try: 
             with open(name+str(".json"),"r") as file:
              for line in file:
               stringaJson+=line
              datoEstratto=json.loads(stringaJson)
              #print (datoEstratto, type(datoEstratto))            
              return datoEstratto
            except FileNotFoundError as e:
               print(e)

def Re_Action(note_text):
    if List_note_write!=[]:
       
       for jnote in get_note(List_note_write):
          if jnote["kind"]==int(6) or jnote["kind"]==int(7):
             if note_text["id"] in tags_string(jnote,"e"):
                print(jnote["content"])         #label
                
def Re_kind1(note_text):
    if List_note_write!=[]:
       for jnote in get_note(List_note_write):
          if jnote["kind"]==int(1):
             if note_text["id"] in tags_string(jnote,"e"):
                print("npub "+jnote["pubkey"]+"\n"+jnote["content"])                     

#metadata_account
colour1=''
colour2='grey'
colour3='#65e7ff'
colour4='BLACK'

def open_relay():
    frame_account=tk.Frame(frame1, background="darkgrey")
    structure_relay = tk.Label(frame_account, text="relay",font=("Arial",12,"bold"))
    entry_relay=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"))
    structure_relay.grid(column=11, row=1, padx=5,pady=5) 
    button_beau.place_forget()

    def relay_class():
     if entry_relay.get()!="":
        if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/":
           
            if entry_relay.get() not in relay_list:
                relay_list.append(entry_relay.get())
                #print(relay_list)  
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=1)
            entry_relay.delete(0, END)
            combo_bo_r['value']=relay_list
            
            return relay_list  
     else:
       if relay_list!=[]:  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
           
       else:
          upload_relay_list("relay")  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
    
    def remove_one_relay():
     if combo_bo_r.get()!="":
        if combo_bo_r.get() in relay_list:
            number=relay_list.index(combo_bo_r.get())
            relay_list.pop(number)
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=1)
            combo_bo_r['value']=relay_list
            return relay_list  
     else:
       if relay_list!=[]:  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
           
       else:
          upload_relay_list("relay")  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list           

    relay_button = tk.Button(frame_account, text="Check!", font=("Arial",12,"normal"),background="grey", command=relay_class)
    counter_relay=Label(frame_account,text="count")
    entry_relay.grid(column=11, row=2, padx=10,pady=5)
    relay_button.grid(column=12, row=2, padx=10,pady=5)
    relay_d_button = tk.Button(frame_account, text="Remove [R]", font=("Arial",12,"normal"),background="grey", command=remove_one_relay)
    relay_d_button.grid(column=13, row=3, padx=10,pady=5)

    def Close_profile(event):
       frame_account.destroy()
       
       button_beau.place(relx=0.22,rely=0.15) 
         
    button_close=tk.Button(frame_account, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=0, padx=5, columnspan=1) 
    
    def on_server(event):
       label_relay["text"] = combo_bo_r.get()[6:]
      
    label_relay = tk.Label(frame_account, text="Name relay",font=('Arial',12,'bold'))
    label_relay.grid(column=13,row=1,pady=5)
    combo_bo_r = ttk.Combobox(frame_account, font=('Arial',12,'normal'))
    combo_bo_r.grid(column=13,row=2,pady=5)
    combo_bo_r.set("Relays set")
    combo_bo_r.bind("<<ComboboxSelected>>", on_server)
    frame_account.grid(row=1,column=9,rowspan=2, columnspan=4,pady=5)

button_beau=tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2,
                  highlightcolor='WHITE',
                  text='Relay',
                  font=('Arial',12,'bold'),
                  command=open_relay  )
button_beau.place(relx=0.22,rely=0.15) 

def write_json_relay(name,note_text):
       with open(name+".txt", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text))

def download_file_relay():
    if relay_list!=[]:
     write_json_relay("relay",relay_list)
    #message_box       

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

button_dwn=tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2,
                  highlightcolor='WHITE',
                  text='⏬ Relays',
                  font=('Arial',12,'bold'),
                  command=download_file_relay          
                  )

button_dwn.place(relx=0.22,rely=0.25)
test_check = IntVar() 
Button_check = Checkbutton(root, text = "Column", variable = test_check, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, width = 10,font=('Arial',16,'normal'))
Button_check.place(relx=0.19,rely=0.46)

def found_root(note):
   try_note=note
   
   if tags_string(try_note,"A")!=[]:
     test_note=asyncio.run(Get_coord_url(str(tags_string(try_note,"A")[0])))
     return test_note
   if tags_string(try_note,"E")!=[]:
     found_nota=asyncio.run(Get_id(tags_string(try_note,"E")))
     return found_nota
   if tags_string(try_note[0],"I")!=[]:
     print(tags_string(try_note[0],"I")[0]) 

def rep_event_():
    note=Open_json_fake_note("article")
    if (note!=""or note!=[]) and note!=None:
     notes=[]
     for xnote in note:
        notes.append(xnote["id"])
     if __name__ == '__main__':
      test_print=get_note(asyncio.run(Get_id(notes)))
      if test_print!=[]:
       notification_plot()
       #messagebox.showinfo("Success", "You have access to \n this note")
       def return_note():
        if test_check.get()==0:
         re_view_note()
        else:
          re_view_col_note()
       button_rep_1=tk.Button(root,text="read note", background="darkgrey", command=return_note, font=('Arial',12,'normal'))
       button_rep_1.place(relx=0.22,rely=0.35)   

      else:
        messagebox.showerror("Fail", "List, is empty")
    else:
      messagebox.showerror("Fail", "Error, not line")
     
button_rep=tk.Button(root,text="Search Note", background="darkgrey", command=rep_event_, font=('Arial',12,'normal'))
button_rep.place(relx=0.112,rely=0.48)

async def get_more_Event(client, event_):
    f = Filter().ids(evnts_ids(event_))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_answers_Event(client, event_):
   
    f=Filter().kind(Kind(1111)).custom_tags(SingleLetterTag.lowercase(Alphabet.A),event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    #print(f.as_json(),len(z))
    return z

async def get_one_Event(client, event_):
    f = Filter().id(evnt_id(event_))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_answer_Event(client, event_):
    f = Filter().event(evnt_id(event_)).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay(" wss://nostr.mom/")
     await client.add_relay("wss://nos.lol/")
     await client.add_relay("wss://relay.primal.net")
    await client.connect()

    await asyncio.sleep(2.0)
    List_note_write.clear()
    if isinstance(event_, list):
        test_kind = await get_more_Event(client, event_)
        test_long=get_note(test_kind)
        coord_event=[]
        for test_x in test_long:
          if test_x["kind"]==int(30023):
           coord = Coordinate(Kind(test_x["kind"]),PublicKey.parse(test_x["pubkey"]),str(tags_string(test_x,"d")[0]))
           coordinate = Nip19Coordinate(coord, [])
           tag_id=Coordinate.parse(coordinate.to_bech32())
           
           coord_event.append(str(tag_id))
        #print(coord_event)   
        resp_answer=await get_answers_Event(client, coord_event)
        if resp_answer!=[]:
         for resp in resp_answer:
           test_kind.append(resp)
    else:
        test_kind = await get_one_Event(client, event_)
        resp_answer=await get_answer_Event(client, event_)
        if resp_answer!=[]:
         for resp in resp_answer:
           test_kind.append(resp)
    List_note_write.extend(test_kind)       
    return test_kind

def re_view_note():
      
        frame1=Frame(root, width=400, height=100)
        canvas = Canvas(frame1)
        canvas.pack(side="left", fill=BOTH, expand=True)

        scrollbar = Scrollbar(frame1, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
    
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    
        scrollable_frame = Frame(canvas, background="#E3E0DD")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        s = 0

        def create_note(note_text, s):
         if date_entry.get()!="":
          if note_text["created_at"]>int(date_entry.get()):
           string_note=StringVar()
           if note_text["kind"]==int(1):
            string_note.set("id "+str(note_text["id"])+"\n"+"Content " +"\n"+note_text["content"])
           if note_text["kind"]==int(7):   
            string_note.set(str(note_text["kind"]) +"\n"+note_text["content"]+"\n"+ "refer to "+ tags_string(note_text,"e")[0])   
           if note_text["kind"]==int(30023):
            string_note.set("id "+str(note_text["id"])+"\n"+"Article " +"\n"+tags_string(note_text,"title")[0])          
           else:
            
            string_note.set("id "+str(note_text["id"])+"\n"+"Content " +"\n"+note_text["content"])
           message = Message(scrollable_frame, textvariable= string_note, width=360, font=('Arial',12,'normal'))
           message.grid(row=s, column=0, columnspan=3, padx=5,pady=5)
           test_1 = tk.Button(scrollable_frame,text="test", command=lambda: test_open(note_text))
           test_1.grid(row=s + 1, column=2,pady=5)
           test_2 = tk.Button(scrollable_frame, text="Re k 1", command=lambda: Re_kind1(note_text))
           test_2.grid(row=s + 1, column=1,pady=5)
           test_3 = tk.Button(scrollable_frame, text="Re ks 6 7", command=lambda: Re_Action(note_text))
           test_3.grid(row=s + 1, column=0,pady=5)
                    
        if List_note_write!=[]:
                s=1
                list_note=get_note(List_note_write)
                
                for note_x in list_note:
                 create_note(note_x, s)
                 s += 2   
                
                root.update_idletasks()
                
        else:
           print("the list is empty")    
        
        frame1.place(relx=0.38,rely=0.5, relheight=0.45,relwidth=0.4)  

        def close_canvas():
            scrollable_frame.forget()
            canvas.destroy()
            frame1.destroy()
            lbel_var.place_forget()
       
        button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal'))
        button_close.grid(column=1,row=0,pady=5) 
        
int_var=IntVar()
lbel_var=Entry(root, textvariable=int_var,font=("Arial",12,"bold"),background="grey")   

def re_view_col_note():
        frame1=Frame(root, width=100, height=100)
        canvas_1 = tk.Canvas(frame1)
        scrollbar_1 = ttk.Scrollbar(frame1, orient=HORIZONTAL,command=canvas_1.xview)
        scrollable_frame = tk.Frame(canvas_1,background="#E3E0DD")

        scrollable_frame.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all")))

        canvas_1.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_1.configure(xscrollcommand=scrollbar_1.set)
        s = 1

        def create_note(note_text, s):
         if date_entry.get()!="":
          if int(note_text["created_at"])>int(date_entry.get()):
            string_note=StringVar()
            if note_text["kind"]==int(30023):
               string_note.set("title " +"\n"+tags_string(note_text,"title")[0])
            else:
             string_note.set("Content " +"\n"+note_text["content"])
            message = Message(scrollable_frame, textvariable= string_note, width=360, font=('Arial',12,'normal'))
            message.grid(row=0, column=s, columnspan=3, padx=5)
            test_1 = tk.Button(scrollable_frame,text="test", command=lambda: test_open(note_text))
            test_1.grid(row=2, column=s + 1,pady=5)
            
            def forget_messages():
                message.destroy()  
                button_cl.grid_forget()
                test_1.grid_forget()
            
            button_cl=Button(scrollable_frame, command=forget_messages, text="X",font=('Arial',12,'normal'))
            button_cl.grid(column=s+1,row=1,pady=5,padx=5)
            
        if List_note_write!=[]:
         
            for entry_note in get_note(List_note_write):
                create_note(entry_note, s)
                s += 3   
        else:
           print("the list is empty")    
        scrollbar_1.pack(side="bottom", fill="x",padx=10)
        canvas_1.pack( fill="y", expand=True)
        frame1.place(relx=0.35,rely=0.45, relheight=0.3,relwidth=0.4)  
        
        def close_canvas():
            scrollable_frame.forget()
            canvas_1.destroy()
            frame1.destroy()
        
        button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal'))
        button_close.grid(column=0,row=0,pady=5) 

frame1.grid()    

def notification_plot():
    import matplotlib.pyplot as plt
    import numpy as np
    kind_1=[]
    kind_6=[]
    kind_7=[]
    kind_1111=[]
    kind_9735=[]
    note=Open_json_fake_note("article")
    if (note!=""or note!=[]) and note!=None:
     notes=[]
     for znote in note:
        notes.append(znote["id"])
    if List_note_write!=[]:
     for xnote in get_note(List_note_write):
       
       if xnote["kind"]==int(1):
        if date_entry.get()!="":
         if xnote["created_at"]>int(date_entry.get()): 
          if xnote not in kind_1: 
           kind_1.append(xnote)
        else:
           if xnote not in kind_1: 
            kind_1.append(xnote)
              
       if xnote["kind"]==int(6):
          if date_entry.get()!="":
            if xnote["created_at"]>int(date_entry.get()): 
             if xnote not in kind_6:  
              kind_6.append(xnote)
          else:
              if xnote["id"] not in kind_6:  
                kind_6.append(xnote)   
       if xnote==int(7):
        if date_entry.get()!="":
         if xnote["created_at"]>int(date_entry.get()): 
          if xnote not in kind_7:    
           kind_7.append(xnote)
        else:
           if xnote not in kind_7:    
            kind_7.append(xnote)   
       if xnote["kind"]==int(1111):
        if date_entry.get()!="":
         if xnote["created_at"]>int(date_entry.get()):
          if xnote not in kind_1111:      
            kind_1111.append(xnote)  
        else:
           if xnote not in kind_1111:      
            kind_1111.append(xnote)    
       if xnote["kind"]==int(9735):
        if date_entry.get()!="":
         if xnote["created_at"]>int(date_entry.get()):  
          if xnote not in kind_9735: 
           kind_9735.append(xnote) 
        else:
           if xnote not in kind_9735: 
            kind_9735.append(xnote)      
     
     if kind_1!=[] or kind_6!=[] or kind_7!=[] or kind_1111!=[] or kind_9735!=[]:
        x = np.array(["Note", "Reposts", "Reaction","Comment", "Zap"])
        y = np.array([len(kind_1), len(kind_6), len(kind_7),len(kind_1111), len(kind_9735)])
        plt.bar(x, y, color = "#4CAF50")
        plt.show()

def next_since():
   since_variable.set(int(since_entry.get()) + 1)
   text_variable.set(int(since_entry.get()) + 1)
   since_day_time()

def back_since():
   if int(since_entry.get())- 1<1:
      since_variable.set(int(1))
      menu_slider1.set(int(1))
      since_day_time()
   else:
    since_variable.set(int(since_entry.get())- 1)  
    menu_slider1.set(int(since_entry.get())- 1)  
    since_day_time()

def since_day_time():
    import datetime
    import calendar
    date = datetime.date.today() - datetime.timedelta(days=int(since_entry.get()))
    t = datetime.datetime.combine(date, datetime.time(1, 2, 1))
    date=datetime.datetime.combine(date, datetime.time(1, 2, 1)).timestamp()
    text_variable.set(str(int(date)))

since_variable=IntVar(value=1)
since_entry=Entry(root,textvariable=since_variable,font=("Arial",12,"normal"),width=4)
since_entry.place(relx=0.12,rely=0.7)
button_mov=tk.Button(root,text="➕",command=next_since)       
button_mov.place(relx=0.12,rely=0.65,relwidth=0.03)
button_back=tk.Button(root,text="➖",command=back_since)       
button_back.place(relx=0.12,rely=0.74,relwidth=0.03) 

text_variable=StringVar()
date_entry=Entry(root,text=text_variable )
date_entry.place(relx=0.2,rely=0.70,relwidth=0.06,relheight=0.03,anchor='n' )

def slide_r1():
   since_variable.set(int(menu_slider1.get()))
   since_day_time()

menu_slider1=Scale(root,orient=HORIZONTAL,variable=since_variable,font=('Arial',12,'bold'))
menu_slider1.place(relx=0.13,rely=0.57)
button_slider1=Button(root,command=slide_r1, text="check",font=('Arial',12,'bold'))
button_slider1.place(relx=0.18,rely=0.65,relheight=0.035)

root.mainloop()

