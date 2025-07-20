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
root.title("Wake Up note")
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
   list_v=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jepg','webp'] 
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
              
async def wake_note(tag,status):
   
  init_logger(LogLevel.INFO)
  try:
   key_string=log_these_key()
   if key_string!=None: 
    keys = Keys.parse(key_string)
    
    
    signer=NostrSigner.keys(keys)
    client = Client(signer)
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    

    await client.connect()
     
    builder = EventBuilder(Kind(2222),status).tags(tag)
   
    test= await client.send_event_builder(builder)
    
    print(test.id)

    print("Event sent:")
    await asyncio.sleep(2.0)
    
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()]).kind(Kind(2222))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     print(event.as_json())
  except NostrSdkError as e:
     print (e)  
       
def Gm_status():
   check_square()
   lists_id=[] 
   if button_entry1.cget('foreground')=="green":
    if list_e!=[] or list_a!=[] or list_r!=[] or return_data_action(6,10)!=None:   
      if list_e!=[]:  
        for xlist in list_e:
            lists_id.append(Tag.event(event_id=EventId.parse(xlist)))
      if list_a!=[]:        
        for jlist in list_a:
            lists_id.append(Tag.coordinate(coordinate=Coordinate.parse(jlist)))
      
      if list_p!=[]:        
        for alist in list_p:
            lists_id.append(Tag.public_key(alist))
      if list_r!=[]:        
        for zlist in list_r:
            lists_id.append(Tag.reference(zlist))     
         
      if date_entry.get()!="":               
            lists_id.append(Tag.expiration(Timestamp.from_secs(int(until_hour_time(10)))))
            
            
    #print(lists_id)  
    if __name__ == '__main__':
               
        if combo_lab.get()!="Type of wake":
         asyncio.run(wake_note(lists_id,combo_lab.get()))
         combo_lab.set("Type of wake")
         button_entry1.cget('foreground')=="grey"
         error_label.config(text="Problem:")
         print_label.config(text="Wait for the status")
         list_e.clear()
         list_a.clear()
         list_p.clear()
         list_r.clear()
         e_show()
         a_show()
         r_show()
         p_show()
         check_square()
         
since_variable=IntVar(value=0)
since_entry=Entry(root,textvariable=since_variable,font=("Arial",12,"normal"),width=6)
text_var=StringVar()
date_entry=Entry(root,textvariable=text_var,font=("Arial",12,"normal"),width=11)
since_entry.place(relx=0.45,rely=0.25,relheight=0.04)
date_entry.place(relx=0.5,rely=0.25,relheight=0.04  )

def return_data_action(until:int,since:int):
    import datetime
    import time

    date_2= datetime.datetime.fromtimestamp(float(time.time())).strftime("%a"+", "+"%d "+"%b"+" %Y")
    data= date_2+ " "+ datetime.datetime.fromtimestamp(float(time.time())).strftime('%H:%M')
    i=0
    while i <len(data):
     if data[i]==":":
       name=data[i-2:i]
       suff=data[i+1:]
     i=i+1  
    if int(name)<since and int(name)>until:
     #print(name,suff)
     since_variable.set(str(name+":"+suff)) 
     result=until_hour_time(since)
     text_var.set(result)
     return data

def until_hour_time(until_time:int):
    import datetime
    date = datetime.date.today() + datetime.timedelta(hours=int(until_time))
    date_1=datetime.datetime.combine(date, datetime.time(until_time, 0, 0)).timestamp()
    #print(int(float(date_1)))
    return date_1

button_1=tk.Button(root,text="Time",command=lambda:return_data_action(6,10),font=("Arial",12))
button_1.place(relx=0.6,rely=0.25,relwidth=0.04)
status_list=["announcement","There is a party tomorrow","Sorry was a mistake","There is a party but you are not invited in","OK goodbye"]

def on_tags_event(event):
    selected_item=combo_lab.get()
    note_label.config(text=selected_item)
    note_label.place(relx=0.4,rely=0.18)

note_label = tk.Label(root, text="",font=("Arial",12))
combo_lab = ttk.Combobox(root, values=status_list,font=('Arial',12,'bold'))
combo_lab.place(relx=0.45,rely=0.12,relwidth=0.1)
combo_lab.set("Type of wake")
combo_lab.bind("<<ComboboxSelected>>", on_tags_event)

#entry_layout

def check_square():
   if date_entry.get()!="": 
    if list_e!=[] or list_a!=[] or list_r!=[] or list_p!=[] or return_data_action(6,10)!=None:
       
       if combo_lab.get()!="Type of wake":
        print_label.config(text="status "+combo_lab.get(), font=("Arial",12,"bold"),foreground="blue")
        button_entry1.config(text="■",foreground="green")
        error_label.config(text="ok")
       
       else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for status", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")
  
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for Tag", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")
   else:      
      error_label.config(text="Problem:")
      print_label.config(text="Wait for Time", font=("Arial",12,"bold"),foreground="black") 
      button_entry1.config(text="■",foreground="grey")
        
button_send=tk.Button(root,text="Status",command=Gm_status, background="darkgrey",font=("Arial",14,"bold"))
button_send.place(relx=0.5,rely=0.35,relwidth=0.1,relheight=0.08,anchor='n' )

button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
button_entry1.place(relx=0.57,rely=0.35,relwidth=0.05, relheight=0.08,anchor="n" )
frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
error_label = tk.Label(frame1, text="Problem:",font=("Arial",12))
error_label.grid(column=3, rowspan=2, row=0, pady=5,padx=5)
print_label = ttk.Label(frame1, text="Wait for the status",font=("Arial",12))
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
       else: 
         p_view.config(text="p tag?: ")          

p_button = tk.Button(root, text="p_show", font=("Arial",12,"bold"), command=p_show)

list_e=[]

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
          if len(list_e)>0:
           e_view.config(text=str(len(list_e)))
          else:
             e_view.config(text="e tag?: ")
              
          return list_e      
     
list_a=[]
list_r=[] 

def a_show():
    a_tag_entry=entry_a.get()
    if a_tag_entry!="":
      try:  
        event_kind = Coordinate.parse(a_tag_entry).kind()
        event_identifier = Coordinate.parse(a_tag_entry).identifier()
        event_publickey = Coordinate.parse(a_tag_entry).public_key()
        if event_publickey!=None:
            list_p.append(event_publickey)
            p_show()
          
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
                  #print(list_a)
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
        if len(list_r)>0:
         r_view.config(text=str(len(list_r)))
        else: 
         r_view.config(text="link: ")             

Check_raw =IntVar()

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.68,rely=0.12,relheight=0.85,relwidth=0.3)  
        e_button.place(relx=0.7,rely=0.30)
        e_view.place(relx=0.77,rely=0.30,relwidth=0.2 )
        e_tag.place(relx=0.7,rely=0.15,relwidth=0.1,relheight=0.1 )
        e_tag_entry.place(relx=0.7,rely=0.25,relwidth=0.2)
        a_tag.place(relx=0.7,rely=0.35,relwidth=0.1,relheight=0.1 )
        entry_a.place(relx=0.7,rely=0.45,relwidth=0.2 )
        a_button.place(relx=0.7,rely=0.50,relwidth=0.1)
        a_view.place(relx=0.7,rely=0.58,relwidth=0.3)
        r_tag.place(relx=0.7,rely=0.65,relwidth=0.1,relheight=0.1 )
        r_summary.place(relx=0.7,rely=0.75,relwidth=0.2 )
        r_button.place(relx=0.7,rely=0.8,relwidth=0.1)
        r_view.place(relx=0.7,rely=0.85,relwidth=0.3)
        Type_band.place(relx=0.29,rely=0.82,relwidth=0.1,relheight=0.05,anchor='e')  
        p_view.place(relx=0.22,rely=0.9,relwidth=0.1 )
        p_button.place(relx=0.1,rely=0.9)
        p_tag.place(relx=0.1,rely=0.8,relwidth=0.1 )
        entryp_tag.place(relx=0.1,rely=0.85,relwidth=0.2 )
        event_idone.place(relx=0.25,rely=0.70,anchor='n' )
        entry_note.place(relx=0.15,rely=0.7,relwidth=0.1, relheight=0.04, anchor="n")

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
      Type_band.place_forget() 
      p_view.place_forget()
      p_button.place_forget()
      p_tag.place_forget()
      entryp_tag.place_forget()
      event_idone.place_forget()
      entry_note.place_forget()
    
lab_button = tk.Button(frame1, text="Add Tags", font=("Arial",12,"bold"), command=raw_label)
lab_button.place(relx=0.75,rely=0.2)
stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)
e_button = tk.Button(root, text="e tag", font=("Arial",12,"bold"), command=e_show)
e_view = tk.Label(root, text="e tag?: ", font=("Arial",12))
e_tag = tk.Label(root, text="e-Tag",font=("Arial",12,"bold"))
e_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12))
a_tag = tk.Label(root, text="a-Tag",font=("Arial",12,"bold"))
entry_a=ttk.Entry(root,justify='left',font=("Arial",12))
a_button = tk.Button(root, text="a tag", font=("Arial",12,"bold"), command=a_show)
a_view = tk.Label(root, text="Article: ", font=("helvetica",13,"bold"),justify="center")
r_tag = tk.Label(root, text="r-Tag",font=("Arial",12,"bold"))
r_summary=ttk.Entry(root,justify='left',font=("Arial",12))
r_button = tk.Button(root, text="R tag", font=("Arial",12,"bold"), command=r_show)
r_view = tk.Label(root, text="link: ", font=("helvetica",13,"bold"),justify="center")
entry_Home_title=ttk.Label(frame1,text="Send Status", justify='left',font=("Arial",20,"bold"), background="darkgrey",border=2)
entry_Home_title.place(relx=0.4,rely=0.2,relwidth=0.2)
str_test=StringVar()
entry_note=ttk.Entry(root,justify='left', textvariable=str_test,font=("Arial",12,"normal"))


def reply_event():
     
  try:   
    event=entry_note.get()
    if event!="" and (len(event)==64 or len(event)==63):
    
     search_id=evnt_id(event)
     found_nota=asyncio.run(Get_id(search_id))
     nota=get_note(found_nota)
  
     if nota!=[] and nota!=None:
        if entryp_tag.get()!="" or e_tag_entry.get()!="":
           entryp_tag.delete(0, END) 
           e_tag_entry.delete(0, END)
         
        entryp_tag.insert(0,nota[0]['pubkey'])
        e_tag_entry.insert(0,nota[0]['id'])
        e_show()
        p_show()
        entry_note.delete(0, END) 
       
     else:
      print("not found")
      entryp_tag.delete(0, END)
      e_tag_entry.delete(0, END)
      entry_note.delete(0, END)
      entry_note.delete(0, END) 
    else:
       
       if event!="":
        
        event_hex=nevent_example(event) 
        if event_hex!=None:
         
         search_id=evnt_id(event_hex)
         found_nota=asyncio.run(Get_id(search_id))
         nota=get_note(found_nota)
  
         if nota!=[] and nota!=None:
          if entryp_tag.get()!="" or e_tag_entry.get()!="":
           entryp_tag.delete(0, END) 
           e_tag_entry.delete(0, END)
         
          entryp_tag.insert(0,nota[0]['pubkey'])
          e_tag_entry.insert(0,nota[0]['id'])
          e_show()
          p_show()
          entry_note.delete(0, END) 
  except NostrSdkError as e:
    print(e)     

async def get_one_Event(client, event_):
    f = Filter().id(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

relay_list=[]

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay(" wss://nostr.mom/")
     await client.add_relay("wss://nos.lol/")
     await client.add_relay("wss://relay.primal.net")
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        print("errore")
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

event_idone=Button(root,text="Search Note", font=('Arial',12,'normal'),command=reply_event ) 


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

def Open_source(key:int):
     """Key = kind number \n
        2222 = notes of kind 2222 
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
   
button4=tk.Button(frame1,text="Search Status",command=lambda: Open_source(2222),font=('Arial',12,'bold'))
button4.place(relx=0.6,rely=0.2)

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)

    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://wot.utxo.one/")
    
    if relay_list!=[]:
        for xrelay in relay_list:
            await client.add_relay(xrelay)
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
      if event.tags().expiration()!=None:
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

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
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
       for xnote in tags_string(note,"expiration"):
         context0=context0+"\n"+"Time "+str(xnote) 
       if note['tags']!=[]:
        context1=note['content']+"\n"
        context2=" "
        
        for xnote in tags_string(note,"alt"):
         context2=context2+"\n"+str(xnote) +"\n"
        if note["content"]=="": 
         for xnote in tags_string(note,"summary"):
          context2=context2+"\n"+"Summary "+tags_string(note,"summary")[0][0:140]+"\n"
        if note["kind"]==30003:    
            for xnote_z in tags_string(note,"i"):
                context2=context2+"\n"+str(xnote_z) +"\n"    
       else: 
        context1=note['content']+"\n"
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
       second_label10.insert(END,context1+"\n"+str(context2))
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

button_read=Button(root,text="Stamp", command=show_noted,font=("Arial",12,"normal"))

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