from nostr_sdk import *
import asyncio
from datetime import timedelta
import time
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
import io
import json
from cryptography.fernet import Fernet

list_notes=[]

def write_txt_note(name,note_text):
       with open(name+".txt", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text)) 

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

root = tk.Tk()
root.title("Kanban note")
root.geometry("1300x800")

def convert_user(x):
    try:
     other_user_pk = PublicKey.parse(x)
     return other_user_pk
    except NostrSdkError as e:
       print(e,"this is the hex_npub ",x)

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

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
   
def evnt_id(id):
    try: 
     test2=EventId.parse(id)
     return test2
    except NostrSdkError as e:
       print(e,"input ",id)

def get_note(z):
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f     

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z     

def event_string(note):
  quoted=note
  if quoted!=None:
   
   list=['npub1','note1']
   img=['nevent1']
   img1=['nprofile']
   other=['naddr1']
   normal=[]
   addressable=[]
   nip_19=[]
   if quoted==None:
        pass
   if quoted[0:5] in list:
        normal.append(quoted)
   if quoted[0:7] in img:
        nip_19.append(quoted) 
   if quoted[0:8] in img1:
        nip_19.append(quoted) 
   if quoted[0:6] in other:
       addressable.append(quoted)
     
   return normal,nip_19,addressable
   
  else:
     print("2")    
     return None,None,None

def nevent_example(note):
   normal,nip_19,addressable=event_string(note)
   if nip_19:
    for event in nip_19:
      if event[0:8]=="nprofile":
        decode_nprofile = Nip19Profile.from_nostr_uri("nostr:"+event)      
        print(f" Profile (decoded): {decode_nprofile.public_key().to_hex()}")

      if event[0:7]=="nevent1":
         decode_nevent = Nip19Event.from_nostr_uri("nostr:"+event)
         print(f" Event (decoded): {decode_nevent.event_id().to_hex()}")
         print(f" Event (decoded): {decode_nevent.relays()}")
         for xrelay in decode_nevent.relays():
           if xrelay[0:6]=="wss://" and xrelay[-1]=="/":
            if xrelay not in relay_list:
               relay_list.append(xrelay)
         return decode_nevent.event_id().to_hex()
      
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
              
async def kanban_note(tag):
   
   init_logger(LogLevel.INFO)
   key_string=log_these_key()
   if key_string!=None: 
    keys = Keys.parse(key_string)
    
    
    signer=NostrSigner.keys(keys)
    client = Client(signer)
    if relay_list!=[]:
       
       for jrelay in relay_list:
          relay_url_list=RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
    

    await client.connect()
     
    builder = EventBuilder(Kind(2323),"").tags(tag)
   
    test= await client.send_event_builder(builder)
    
    print(test.id)

    print("Event sent:")
    await asyncio.sleep(2.0)
    
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()]).kind(Kind(2323))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     print(event.as_json())
       
def Gm_status():
   check_square()
   lists_id=[] 
   if button_entry1.cget('foreground')=="green":
    if list_title!=[] or list_summary!=[] or list_description!=[] or list_r!=[] :   
      if list_title!=[]:  
        for xlist in list_title:
            lists_id.append(Tag.custom(TagKind.TITLE(), [xlist]))
      if list_summary!=[]:        
        for jlist in list_summary:
            lists_id.append(Tag.custom(TagKind.SUMMARY(), [jlist]))
      if list_description!=[]:        
        for hlist in list_description:
            lists_id.append(Tag.custom(TagKind.DESCRIPTION(), [hlist]))       
           
      if list_p!=[]:        
        for alist in list_p:
            lists_id.append(Tag.public_key(alist))
      if list_r!=[]:        
        for zlist in list_r:
            lists_id.append(Tag.reference(zlist))     
         
    if __name__ == '__main__':
               
        if lists_id!=[]:
         asyncio.run(kanban_note(lists_id))
    clear_list()
    error_label.config(text="Problem:")
    print_label.config(text="Wait for the card note",foreground="blue")

since_variable=IntVar(value=0)
since_entry=Entry(root,textvariable=since_variable,font=("Arial",12,"normal"),width=6)
text_var=StringVar()
date_entry=Entry(root,textvariable=text_var,font=("Arial",12,"normal"),width=11)

def check_square():
    
    if list_title!=[] or list_description!=[] or list_summary!=[] or list_r!=[]:
       
        print_label.config(text="Card ready", font=("Arial",12,"bold"),foreground="blue")
        button_entry1.config(text="■",foreground="green")
        error_label.config(text="ok")
       
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for Tag", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")
        
button_send=tk.Button(root,text="Card Note",command=Gm_status, background="darkgrey",font=("Arial",14,"bold"))
button_send.place(relx=0.5,rely=0.35,relwidth=0.1,relheight=0.08,anchor='n' )

button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
button_entry1.place(relx=0.57,rely=0.35,relwidth=0.05, relheight=0.08,anchor="n" )
frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
error_label = tk.Label(frame1, text="Problem:",font=("Arial",12))
error_label.grid(column=3, rowspan=2, row=0, pady=5,padx=5)
print_label = ttk.Label(frame1, text="Wait for the card note",font=("Arial",12))
print_label.grid(column=3, columnspan=2, row=2, pady=5,padx=10)
frame1.pack(side=TOP,fill=X)
p_tag = tk.Label(root, text="p-Tag",font=("Arial",12,"bold"))
entryp_tag=ttk.Entry(root,justify='left',font=("Arial",12),)
p_view = tk.Label(root, text="p tag?: ", font=("Arial",12))
Checkbutton8 = IntVar() 
Type_band = Checkbutton(root, text = "More p tag", variable = Checkbutton8, onvalue = 1, offvalue = 0, height = 2, width = 10,font=('Arial',16,'normal'))
list_p=[]

def p_show():
    title=entryp_tag.get()
    
    if len(title)==64 or len(title)==63:
        if len(title)==63:
           title=PublicKey.parse(title).to_hex()
       
        if convert_user(title)!=None:
         if title not in list_p:
          if Checkbutton8.get()==0:
            if len(list_p)>=1:
                i=1
                while len(list_p)>i:
                 list_p.pop(1)
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END)  
            else:  
                list_p.append(convert_user(title))
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END) 
                return list_p
          else:
                list_p.append(convert_user(title))
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END) 
                return list_p 
          
         else:
              p_view.config(text=str(len(list_p)))
              
              entryp_tag.delete(0, END) 
              return list_p
        else:
         p_view.config(text=str(len(list_p)))
         entryp_tag.delete(0, END) 
    else:
       entryp_tag.delete(0, END) 
       if len(list_p)>0:
        p_view.config(text=str(len(list_p)))

p_button = tk.Button(root, text="p_show", font=("Arial",12,"bold"), command=p_show)
list_title=[]
list_summary=[]
list_description=[]
list_r=[] 

def t_show():
    title=t_tag_entry.get()
    print(title)
    if list_title==[]:
         if title!="": 
          list_title.append(title)
          t_view.config(text=str(len(list_title)))
          t_tag_entry.delete(0, END) 
         
    else:
         print("title")
         t_view.config(text=str(len(list_title)))
         t_tag_entry.delete(0, END)    
        
def s_show():
    summary=entry_s.get()
    if list_summary==[]:
            if summary!="": 
             list_summary.append(summary)
             s_view.config(text=str(len(list_summary)))
             entry_s.delete(0, END) 
    else:   
        if len(list_summary)>0:
              s_view.config(text=str(len(list_summary)))
              entry_s.delete(0, END) 
              
def d_show():
    description=entry_d.get()
    print(description)
    if list_description==[]:
          if description!="": 
            list_description.append(description)
            d_view.config(text=str(len(list_description)))
            entry_d.delete(0, END) 
    else:   
        if len(list_description)>0:
              d_view.config(text=str(len(list_description)))
              entry_d.delete(0, END) 
              
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

Check_raw =IntVar()

def clear_list():
   """Remove Tags and Update"""
   list_p.clear()
   list_r.clear()
   list_title.clear()
   list_description.clear()
   list_summary.clear()
   r_view.config(text="link: ")
   s_view.config(text="Summary: ")
   d_view.config(text="Description: ")
   t_view.config(text="Title: ")
   p_view.config(text="p tag?: ")
   button_entry1.cget('foreground')=="grey"

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.68,rely=0.12,relheight=0.85,relwidth=0.3)  
        t_button.place(relx=0.82,rely=0.2)
        t_view.place(relx=0.77,rely=0.30,relwidth=0.2 )
        t_tag.place(relx=0.7,rely=0.2,relwidth=0.1 )
        t_tag_entry.place(relx=0.7,rely=0.25,relwidth=0.2)
        s_tag.place(relx=0.7,rely=0.35,relwidth=0.1)
        entry_s.place(relx=0.7,rely=0.4,relwidth=0.2 )
        s_button.place(relx=0.82,rely=0.35,relwidth=0.1)
        s_view.place(relx=0.82,rely=0.45)
        button_clear.place(relx=0.7,rely=0.9)
        d_tag.place(relx=0.7,rely=0.55,relwidth=0.1)
        entry_d.place(relx=0.7,rely=0.6,relwidth=0.2 )
        d_button.place(relx=0.82,rely=0.54)
        d_view.place(relx=0.82,rely=0.65)

        r_tag.place(relx=0.7,rely=0.7,relwidth=0.1 )
        r_summary.place(relx=0.7,rely=0.75,relwidth=0.2 )
        r_button.place(relx=0.7,rely=0.8,relwidth=0.1)
        r_view.place(relx=0.82,rely=0.8)
        Type_band.place(relx=0.29,rely=0.82,relwidth=0.1,relheight=0.05,anchor='e')  
        p_view.place(relx=0.22,rely=0.9,relwidth=0.1 )
        p_button.place(relx=0.1,rely=0.9)
        p_tag.place(relx=0.1,rely=0.8,relwidth=0.1 )
        entryp_tag.place(relx=0.1,rely=0.85,relwidth=0.2 )
   
   else:
      Check_raw.set(0)
      stuff_frame.place_forget() 
      t_tag.place_forget()
      t_tag_entry.place_forget()
      t_button.place_forget()
      t_view.place_forget()
      s_tag.place_forget()
      entry_s.place_forget()
      s_button.place_forget()
      s_view.place_forget()
      r_tag.place_forget()
      r_summary.place_forget()
      r_button.place_forget()
      r_view.place_forget()
      Type_band.place_forget() 
      p_view.place_forget()
      p_button.place_forget()
      p_tag.place_forget()
      entryp_tag.place_forget()
      d_tag.place_forget()
      entry_d.place_forget()
      d_button.place_forget()
      d_view.place_forget()
      button_clear.place_forget()
    
lab_button = tk.Button(frame1, text="Add Tags", font=("Arial",12,"bold"), command=raw_label)
lab_button.place(relx=0.75,rely=0.2)
stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)
button_clear=Button(root,text="Remove", command=clear_list, font=("Arial",12,"bold"))
t_button = tk.Button(root, text="title tag", font=("Arial",12,"bold"), command=t_show)
t_view = tk.Label(root, text="Title: ", font=("Arial",12,"bold"))
t_tag = tk.Label(root, text="title-Tag",font=("Arial",12,"bold"))
t_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12))
s_tag = tk.Label(root, text="summary-Tag",font=("Arial",12,"bold"))
entry_s=ttk.Entry(root,justify='left',font=("Arial",12))
s_button = tk.Button(root, text="summary tag", font=("Arial",12,"bold"), command=s_show)
s_view = tk.Label(root, text="Summary: ", font=("helvetica",13,"bold"),justify="center")
d_tag = tk.Label(root, text="description-Tag",font=("Arial",12,"bold"))
entry_d=ttk.Entry(root,justify='left',font=("Arial",12))
d_button = tk.Button(root, text="description tag", font=("Arial",12,"bold"), command=d_show)
d_view = tk.Label(root, text="Description: ", font=("helvetica",13,"bold"),justify="center")
r_tag = tk.Label(root, text="r-Tag",font=("Arial",12,"bold"))
r_summary=ttk.Entry(root,justify='left',font=("Arial",12))
r_button = tk.Button(root, text="reference tag", font=("Arial",12,"bold"), command=r_show)
r_view = tk.Label(root, text="link: ", font=("helvetica",13,"bold"),justify="center")
entry_Home_title=ttk.Label(frame1,text="Send Card Note", justify='left',font=("Arial",20,"bold"), background="darkgrey",border=2)
entry_Home_title.place(relx=0.4,rely=0.05,relwidth=0.2)
relay_list=[]

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
       
       for jrelay in relay_list:
          relay_url_list=RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
    else:
     relay_url_1=RelayUrl.parse("wss://nostr.mom/")
     relay_url_2=RelayUrl.parse("wss://nos.lol/")
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

    relay_button = tk.Button(frame_account, text="Check!", font=("Arial",12,"normal"),background="grey", command=relay_class)
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

button_beau=tk.Button(root,   highlightcolor='WHITE',text='Relay',font=('Arial',12,'bold'), command=open_relay)
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

button_dwn=tk.Button(root, highlightcolor='WHITE',text='⏬ Relays',font=('Arial',12,'bold'),command=download_file_relay)
button_dwn.place(relx=0.05,rely=0.15)
db_note=[]

def Open_card(key:int):
     """Key = kind number \n
        2323 = notes of kind 2323 
     """
     test=[]
     if __name__ == "__main__":
      test_kinds = [Kind(key)]  
      test = asyncio.run(Get_event_from(test_kinds))
     if test!=[] and test!=None:
      note= get_note(test)
      for xnote in note:
        if xnote not in db_note:
         db_note.append(xnote)
         list_notes.append(xnote) 
      show_noted()   
 
button4=tk.Button(frame1,text="Search Card Note",command=lambda: Open_card(2323),font=('Arial',12,'bold'))
button4.place(relx=0.22,rely=0.15)

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)

    # Add relays and connect
    relay_url_1=RelayUrl.parse("wss://nostr.mom/")
    relay_url_2=RelayUrl.parse("wss://wot.utxo.one/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    
    if relay_list!=[]:
        for xrelay in relay_list:
          if xrelay!="wss://yabu.me/":
            relay_url_list=RelayUrl.parse(xrelay)
            await client.add_relay(relay_url_list)
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

public_list=[]

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
       for xnote in tags_string(note,"title"):
         context0=context0+"\n"+"Title "+str(xnote) 
       context1=note['content']  
       if note['tags']!=[]:
        
        context2=" "
        if tags_string(note,"alt")!=[]:
         for xnote in tags_string(note,"alt"):
          context2=context2+"\n"+str(xnote) +"\n"
        if tags_string(note,"summary")!=[]:
         for xnote in tags_string(note,"summary"):
           context2=context2+"\n"+"- Summary "+tags_string(note,"summary")[0]+"\n"
        if tags_string(note,"description")!=[]: 
                context2=context2+"\n" +"- Description "+str(tags_string(note,"description")[0]) +"\n"    
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
                print(entry["content"])
                                               
       button=Button(scrollable_frame_1,text=f"Print me!", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=3,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read!", command=lambda val=note: print_id(val))
       button_grid2.grid(row=3,column=s1+1,padx=5,pady=5)    
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="bottom", fill="x",padx=20)
    scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.35,rely=0.53,relwidth=0.32,relheight=0.4)

    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.55,rely=0.47,relwidth=0.1)      

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