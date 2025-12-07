#Kanbookmark
from nostr_sdk import *
import asyncio
from datetime import timedelta
from datetime import datetime
import uuid
import tkinter as tk
from tkinter import *
from tkinter import ttk
import uuid
import requests
from cryptography.fernet import Fernet
import json

def get_nostr_relay_info(relay_url: str):
    """
    Gets the NIP-11 information for a Nostr relay. \n
    relay_url: e.g., 'https://relay.damus.io/'
    
    """
    headers = {"Accept": "application/nostr+json"}

    if relay_url.startswith("ws://"):
        relay_url = relay_url.replace("ws://", "http://")
    elif relay_url.startswith("wss://"):
        relay_url = relay_url.replace("wss://", "https://")
    
    try:
        response = requests.get(relay_url, headers=headers, timeout=10)
        response.raise_for_status()
        info = response.json()
        return info
    except Exception as e:
        print(f"Error while requesting {relay_url}: {e}")
        return None

async def check_relay_dict(dict_relay:dict):
   
   for relay_x in list(dict_relay.keys()):
      if dict_relay[relay_x]!="bad":   
         if get_nostr_relay_info(relay_x):
            dict_relay[relay_x]="good"
         else:
            dict_relay[relay_x]="bad"           

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

def get_note(z):
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f

root = tk.Tk()
root.title("Bookmark Example")
root.geometry("1300x800")

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

Nostr_relay_list={"wss://relay.lnfi.network/":"","wss://relay.braydon.com/":""}

async def Can_book(tag,title_str):
    # Init logger
  init_logger(LogLevel.INFO)
   
  key_string=log_these_key()
  if key_string!=None: 
    keys = Keys.parse(key_string)
    signer = NostrSigner.keys(keys)
    
    client = Client(signer)
    # Add relays and connect
    if relay_list!=[]:
        for jrelay in relay_list:
            if jrelay not in list(Nostr_relay_list.keys()):
                Nostr_relay_list[jrelay]=""
                relay_list.remove(jrelay)
    await check_relay_dict(Nostr_relay_list)
    for relay_c,value in Nostr_relay_list.items():
        if value!="bad": 
            await client.add_relay(RelayUrl.parse(relay_c))        
    
    await client.connect()
     
    myUUID = uuid.uuid4()
    url_uid=str(myUUID)
    if title_str!="":
        tags=[Tag.custom(TagKind.TITLE(), [title_str])]
        builder = EventBuilder.bookmarks_set(url_uid,tag).tags(tags)
    else:
        builder = EventBuilder.bookmarks_set(url_uid,tag)
    result_test= await client.send_event_builder(builder)
    
    print("Event sent:", result_test.id.to_hex())
    
    await asyncio.sleep(2.0)

    # Get events from relays
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     print(event.as_json())
        
def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def create_bookmark():
   check_square()
   lists_id=[] 
   lists_ad=[] 
   list_bookmarks=[]  
   if button_entry1.cget('foreground')=="green":
    if list_e or list_a or list_r!=[]:
      if list_e!=[]:  
                  
            lists_id=[EventId.parse(xlist) for xlist in list_e] 
      if list_a!=[]:        
            lists_ad=[Coordinate.parse(jlist) for jlist in list_a]
      if list_r!=[]:        
            list_r 
          
    if __name__ == '__main__':
        note=""
        test=Bookmarks(event_ids=lists_id)
        
        #list_bookmark.coordinate=list_ad
        #list_bookmark.hashtags=list_h
        #list_bookmark.urls=list_r
        asyncio.run(Can_book(test,title_str=combo_to_do_list.get()))
        list_e.clear()
        lists_id.clear()
        e_view.config(text="e tag?: ")
        combo_to_do_list.set("")
        string_var_1.set("")
        error_label.config(text="Problem:")
        print_label.config(text="Wait for the bookmark",foreground="black")
    button_entry1.config(text="■",foreground="grey")    

#entry_layout

def check_square():
    if list_e or list_a or list_r!=[]:
       button_entry1.config(text="■",foreground="green")
       error_label.config(text="ok")
       print_label.config(text="ok! ", font=("Arial",12,"bold"),foreground="blue")
              
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for the bookmark", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")

list_h=[]
list_e=[]
list_a=[]
list_r=[]  
relay_list=[]
button_send=tk.Button(root,text="send bookmark",command=create_bookmark, background="darkgrey",font=("Arial",14,"bold"))
button_send.place(relx=0.82,rely=0.5,relwidth=0.2,relheight=0.1,anchor='n' )
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
button_entry1.place(relx=0.94,rely=0.5,relwidth=0.05, relheight=0.1,anchor="n" )

def select_type(event):
    selet_item=combo_to_do_list.get()
    if selet_item!="":
        string_var_1.set("Title "+selet_item)
        
        select_label.place(relx=0.85,rely=0.42)
    else:
        string_var_1.set("")
        select_label.place_forget()

string_var_1=StringVar()
select_label = ttk.Label(root, textvariable=string_var_1,font=("Arial",12,"bold"))
select_label_list = ttk.Label(root, text="Name List",font=("Arial",12,"bold"))
select_label_list.place(relx=0.74,rely=0.37)
combo_to_do_list = ttk.Combobox(root, values=["To do","Wish", "Done", "Possible" ],width=10,font=("Arial",12,"normal"))
combo_to_do_list.place(relx=0.74,rely=0.42)
combo_to_do_list.set("")
combo_to_do_list.bind("<<ComboboxSelected>>",select_type)

frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
error_label = tk.Label(frame1, text="Problem:",font=("Arial",12))
error_label.grid(column=3, rowspan=2, row=0, pady=5,padx=5)
print_label = ttk.Label(frame1, text="Wait for the bookmark",font=("Arial",12))
print_label.grid(column=3, columnspan=2, row=2, pady=5,padx=5)

frame1.pack(side=TOP,fill=X)

def evnt_id(id):
    try: 
     test2=EventId.parse(id)
     return test2
    except NostrSdkError as e:
       print(e,"input ",id)

def event_string_note(note):   
    quoted=note
    list_1=['nevent1','note1']
    if quoted!=None: 
     if len(quoted)==64:
       return note   
     else:
        if quoted[0:5] in list_1:
            return(EventId.parse(quoted).to_hex())
        if quoted[0:7] in list_1:
         decode_nevent = Nip19Event.from_nostr_uri("nostr:"+quoted)
         print(f" Event (decoded): {decode_nevent.event_id().to_hex()}")
         print(f" Event (decoded): {decode_nevent.relays()}")
         for xrelay in decode_nevent.relays():
           if xrelay[0:6]=="wss://" and xrelay[-1]=="/":
            if xrelay not in relay_list:
               relay_list.append(xrelay)
         return decode_nevent.event_id().to_hex()
              
def e_show():
    title_e=e_tag_entry.get()
    title=event_string_note(title_e)
    if title!=None:
     if len(title)==64:
       
        if evnt_id(title)!=None:
         if title not in list_e:
          list_e.append(title)
          e_view.config(text=str(len(list_e)))
          e_tag_entry.delete(0, END) 
          return list_e
          
         else:
              print("already present")
              e_view.config(text=str(len(list_e)))
              e_tag_entry.delete(0, END) 
              return list_e
        else:
         print("event_id")
         e_view.config(text=str(len(list_e)))
         e_tag_entry.delete(0, END)    
        
    else:
          
          e_tag_entry.delete(0, END) 
          return list_e    

def a_show():
    a_tag_entry=entry_a.get()
    if a_tag_entry!="":
      try:  
        event_kind = Coordinate.parse(a_tag_entry).kind()
        event_identifier = Coordinate.parse(a_tag_entry).identifier()
        event_publickey = Coordinate.parse(a_tag_entry).public_key()
        
        if a_tag_entry not in list_a:
            for j in a_tag_entry.split():
              if j[0:6]=="nostr:":
                  if j[6:] not in list_a:
                   
                   list_a.append(j[6:])
                   a_view.config(text=str(len(list_a)))
                   entry_a.delete(0, END)    
              else:
                  
                  list_a.append(a_tag_entry)
                  a_view.config(text=str(len(list_a)))
                  entry_a.delete(0, END) 
                  
        else:
             a_view.config(text="Enter an article naddr: " )         
             entry_a.delete(0, END) 
      except NostrSdkError as e:
          print(e)   
          entry_a.delete(0, END)     
    else:   
        if len(list_a)>0:
              a_view.config(text=str(len(list_a)))
              entry_a.delete(0, END) 
              
        else:
           a_view.config(text="Article: ") 

def r_show():
    if codifica_spam()=="spam":
     r_tag_entry=r_summary.get()
     if r_tag_entry!="":
        if r_tag_entry not in list_r:
            list_r.append(r_tag_entry)
            r_view.config(text=str(len(list_r)))
            r_summary.delete(0, END)
        else:
             r_view.config(text="Enter a link: " )         
             r_summary.delete(0, END)
     else:
            r_view.config(text="Sorry, this is uncorrect: ")             
            r_summary.delete(0, END)
    else:
        r_summary.delete(0, END)    

stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)
e_tag = tk.Label(root, text="e-Tag",font=("Arial",12,"bold"))
e_string_var=StringVar()
e_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12),textvariable=e_string_var)
e_button = tk.Button(root, text="Add Event", font=("Arial",12,"bold"), command=e_show)
e_view = tk.Label(root, text="e tag?: ", font=("Arial",12))
a_tag = tk.Label(root, text="A-Tag",font=("Arial",12,"bold"))
entry_a=ttk.Entry(root,justify='left',font=("Arial",12))
a_button = tk.Button(root, text="a tag", font=("Arial",12,"bold"), command=a_show)
a_view = tk.Label(root, text="Article: ", font=("helvetica",13,"bold"),justify="center")
r_tag = tk.Label(root, text="r-Tag",font=("Arial",12,"bold"))
r_summary=ttk.Entry(root,justify='left',font=("Arial",12))
r_button = tk.Button(root, text="R tag", font=("Arial",12,"bold"), command=r_show)
r_view = tk.Label(root, text="link: ", font=("helvetica",13,"bold"),justify="center")

#summary_button = tk.Button(root, text="view_Summary", font=("Arial",12,"bold"), command=summary_show)
#summary_button.place(relx=0.8,rely=0.50,relwidth=0.1)
#summary_view = tk.Label(root, text="Summary: ", font=("helvetica",13,"bold"),justify="center")
#summary_view.place(relx=0.7,rely=0.58,relwidth=0.3)

#wall=tk.Button(root, text="",background="lightgrey")
#wall.place(relx=0.7,rely=0.58,relheight=0.15,width=5, height=15)
#wall2=tk.Button(root, text="",background="lightgrey")
#wall2.place(relx=0.7,rely=0.75,relwidth=0.25, height=5)

entry_note=ttk.Label(frame1,text="Bookmarks", justify='left',font=("Arial",20,"bold"), background="darkgrey",border=2)
entry_note.place(relx=0.4,rely=0.05,relwidth=0.2)
Check_raw =IntVar()

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.72,rely=0.12,relheight=0.22,relwidth=0.2)  
        e_button.place(relx=0.75,rely=0.25)
        e_view.place(relx=0.85,rely=0.25 )
        e_tag.place(relx=0.75,rely=0.16)
        e_tag_entry.place(relx=0.75,rely=0.2,relwidth=0.15)
        #a_tag.place(relx=0.7,rely=0.35,relwidth=0.1,relheight=0.1 )
        #entry_a.place(relx=0.7,rely=0.45,relwidth=0.2 )
        #a_button.place(relx=0.7,rely=0.50,relwidth=0.1)
        #a_view.place(relx=0.85,rely=0.5)
        #r_tag.place(relx=0.7,rely=0.65,relwidth=0.1,relheight=0.1 )
        #r_summary.place(relx=0.7,rely=0.75,relwidth=0.2 )
        #r_button.place(relx=0.7,rely=0.8,relwidth=0.1)
        #r_view.place(relx=0.85,rely=0.8)
    
   else:
      Check_raw.set(0)
      stuff_frame.place_forget() 
      e_tag.place_forget()
      e_tag_entry.place_forget()
      e_button.place_forget()
      e_view.place_forget()
      a_tag.place_forget()
      entry_a.place_forget()
      a_button.place_forget()
      a_view.place_forget()
      r_tag.place_forget()
      r_summary.place_forget()
      r_button.place_forget()
      r_view.place_forget()
    
lab_button = tk.Button(frame1, text="Add Tags", font=("Arial",12,"bold"), command=raw_label)
lab_button.place(relx=0.75,rely=0.2)

def url_bookmark():
 z=r_summary.get()
 for j in z.split():
    if j[0:5]=="https":
        return str(j)   
    
def codifica_spam():
   f=url_bookmark()
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
  
def open_relay():
    frame_account=tk.Frame(root, background="darkgrey")
    structure_relay = tk.Label(frame_account, text="relay",font=("Arial",12,"bold"))
    entry_relay=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"))
    structure_relay.grid(column=11, row=1, padx=5,pady=5) 
    button_beau.destroy()
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

    relay_button = tk.Button(frame_account, text="Check", font=("Arial",12,"normal"),background="grey", command=relay_class)
    counter_relay=Label(frame_account,text="count", font=('Arial',12,'normal'))
    entry_relay.grid(column=11, row=2, padx=10,pady=5)
    relay_button.grid(column=12, row=2, padx=10,pady=5)

    def Close_profile(event):
       frame_account.place_forget()
       button_beau=tk.Button(root, 
                  highlightcolor='WHITE',
                  text='Relay',
                  font=('Arial',12,'bold'),
                  command=open_relay            
                  )
       button_beau.place(relx=0.15,rely=0.15) 
     
    button_close=tk.Button(frame_account, background='#F8F8F8', text='❌',font=('Arial',12,'bold'))    
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
    
    frame_account.place(relx=0.01,relheight=0.2,rely=0.25)

button_beau=tk.Button(root,   highlightcolor='WHITE',
                  text='Relay',
                  font=('Arial',12,'bold'),
                  command=open_relay            
                  )

button_beau.place(relx=0.15,rely=0.15) 

def write_json_relay(name,note_text):
       with open(name+".txt", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text))

def download_file_relay():
    if relay_list!=[]:
     write_json_relay("relay",relay_list)

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

button_dwn=tk.Button(root, 
                  highlightcolor='WHITE',
                  text='⏬ Relays',
                  font=('Arial',12,'bold'),
                  command=download_file_relay          
                  )

button_dwn.place(relx=0.05,rely=0.15)

db_note=[]
list_notes=[]
public_list=[]

def Open_kinds(list_int:list[int]):
     """list_int = kinds number \n
        2323 = notes of kind 2323 
        2424 = notes of kind 2424 
     """
     test_kinds=[]
     if __name__ == "__main__":
       for key in list_int:
        test_kinds.append(Kind(key))  
       test = asyncio.run(Get_event_from(test_kinds))
       if test!=[] and test!=None:
        note= get_note(test)
        for xnote in note:
         if xnote not in db_note:
            db_note.append(xnote)
            list_notes.append(xnote) 
        show_noted()   
  
button4=tk.Button(root,text="Search Card Note",command=lambda: Open_kinds([2323,2424]),font=('Arial',12,'bold'))
button4.place(relx=0.42,rely=0.15)

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)

    # Add relays and connect
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.add_relay(RelayUrl.parse("wss://purplerelay.com/"))
    
    if relay_list!=[]:
     for jrelay in relay_list:
        if jrelay not in list(Nostr_relay_list.keys()):
            Nostr_relay_list[jrelay]=""
            relay_list.remove(jrelay)
    await check_relay_dict(Nostr_relay_list)
    for relay_c,value in Nostr_relay_list.items():
      if value!="bad": 
        await client.add_relay(RelayUrl.parse(relay_c))     
    
    await client.connect()
    await asyncio.sleep(2.0)
    try:   
     if isinstance(event_, list):
        test_kind = await get_kind(client, event_)
     else:
        print("errore")

     if test_kind==[] and public_list!=[]:
       test_kind = await get_kind_relay(client, event_)
       print("from relay")
    except NostrSdkError as e:
       print(e)   
    return test_kind

async def get_kind(client, event_):
    if public_list!=[]:
     f = Filter().kinds(event_).author(public_list[0])
    else:
       
       f = Filter().kinds(event_).limit(50)
    try:
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10)) 
     z=[] 
     for event in events.to_vec():
     
       if event.verify_signature():
          
          z.append(event.as_json())
     if z!=[]:      
      return z
    except NostrSdkError as e:
       print (e)

async def get_kind_relay(client, event_):
    f = Filter().kinds(event_).limit(16)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

def show_noted():
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
 if list_notes!=[]:
    s=1
    s1=0
    
    for note in list_notes:
     
      try:
       context0="Author: "+note['pubkey']
       context0=context0+"\n"+"Kind "+str(note["kind"])
       if tags_string(note,"e")!=[]:
          if note["kind"]==2424:
           context1="Possible"
          else:
             context1="Update"
       else:
          if note["kind"]==2424:
            context1="Wish"
          else:
            context1="Todo or Done"          
       
       if note['tags']!=[]:
        
        context2=" "
        if tags_string(note,"title")!=[]:
            context2=context2+"\n"+"- Title "+str(tags_string(note,"title")[0]) +"\n"
        if tags_string(note,"summary")!=[]:
            context2=context2+"\n"+"- Summary "+tags_string(note,"summary")[0]+"\n"
        if tags_string(note,"description")!=[]: 
            context2=context2+"\n" +"- Description "+str(tags_string(note,"description")[0]) +"\n"
        if tags_string(note,"r")!=[]: 
            for tag_link in tags_string(note,"r"):
             context2=context2+"\n" +"- Link "+tag_link +"\n"    


       else: 
        
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       button_grid2=Button(scrollable_frame_1,text= "Author "+note['pubkey'][0:44], command=lambda val=note["pubkey"]: pubkey_id(val))
       button_grid2.grid(row=1,column=s1,padx=5,pady=5, columnspan=3)   
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=2)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=2) 
      
       def print_id(entry):
           number=list(list_notes).index(entry)
           print(number)
           print(entry['tags'])
                  
       def print_var(entry):
                print("event_id",entry["id"])

       def send_var(entry):
            e_string_var.set(entry["id"])                         
                               
       button=Button(scrollable_frame_1,text=f"Print id", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=3,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
       button_grid2.grid(row=3,column=s1+1,padx=5,pady=5)    
       button_grid3=Button(scrollable_frame_1,text=f"Add to bookmark ", command=lambda val=note: send_var(val))
       button_grid3.grid(row=3,column=s1+2,padx=5,pady=5) 
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="bottom", fill="x",padx=20)
    scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.4,rely=0.23,relwidth=0.3,relheight=0.4)

    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.58,rely=0.15,relwidth=0.1)      

def pubkey_id(test):
   note_pubkey=[]
   for note_x in db_note:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   if len(note_pubkey)>1:       
    search_for_note(note_pubkey)
    show_noted()

def search_for_note(note_found:list):
     if note_found!=[]:
        list_notes.clear()
        for note_x in note_found:
            if note_x not in list_notes: 
               list_notes.append(note_x)
        return list_notes 

root.mainloop()