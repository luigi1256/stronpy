import asyncio
from nostr_sdk import *
from nostr_sdk import EventId, Event,EventBuilder, Metadata,Kind
from datetime import timedelta
import json
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import *
from tkinter import ttk

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

relay_list=[]
root = tk.Tk()
root.title("Outbox")
root.geometry("1300x800")

out_relay = ttk.LabelFrame(root, text="Update relay", labelanchor="n", padding=10)
out_relay.place(relx=0.47,rely=0.05,relheight=0.25,relwidth=0.27)   
add_relay=Label(root,text="add_relay", font=("Arial",12,"normal"))
add_relay.place(relx=0.52,rely=0.11)
enter_relay=StringVar()
login_relay=Entry(root,textvariable=enter_relay)
login_relay.place(relx=0.5,rely=0.15)
counter_relay=Label(root,font=("Arial",12,"bold"))

def clear_relay_list():
   relay_list.clear()
   counter_relay['text']=str(len(relay_list)) 

relay_button_clear = tk.Button(root, text="Clear list", font=("Arial",12,"normal"),background="grey", command=clear_relay_list)
relay_button_clear.place(relx=0.52,rely=0.2)

def relay_class():
     if login_relay.get()!="":
        if login_relay.get()[0:6]=="wss://" and login_relay.get()[-1]=="/":
           
            if login_relay.get() not in relay_list:
                relay_list.append(login_relay.get())
                #print(relay_list)  
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.place(relx=0.64,rely=0.09)
            enter_relay.set("")
            
relay_button = tk.Button(root, text="Go Add!", font=("Arial",12,"normal"),background="grey", command=relay_class)
relay_button.place(relx=0.62,rely=0.14)

async def Outboxed():
    # Init logger
  init_logger(LogLevel.INFO)
  key_string=log_these_key()
  if key_string!=None: 
    keys = Keys.parse(key_string)
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    # Add relays and connect
    relay_url_x = RelayUrl.parse("wss://nostr.mom/")
    await client.add_relay(relay_url_x)
    
    if relay_list!=[]:
        for jrelay in relay_list:
         relay_url = RelayUrl.parse(jrelay)
         await client.add_relay(relay_url)
    await client.connect()
    test_relay={}
    if len(relay_list)<5:
     await search_box_relay()
    for relay in relay_list:
        test_relay[relay]=None
    if test_relay!={}:    
     builder = EventBuilder.relay_list(test_relay)
     await client.send_event_builder(builder)
    
     print("Getting events from relays...")
     f = Filter().authors([keys.public_key()]).kind(Kind(10002))
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     for event in events.to_vec():
      if event.verify():
        print(event.as_json())

def new_realy_list():
   if relay_list!=[]:
    L=[]
    if __name__ == "__main__":
     
     asyncio.run(Outboxed())
   
relay_button = tk.Button(root, text="Update list", font=("Arial",12,"normal"), command=new_realy_list)
relay_button.place(relx=0.62,rely=0.2)

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
    relay_d_button = tk.Button(frame_account, text="Remove [R]", font=("Arial",12,"normal"),background="grey", command=remove_one_relay)
    counter_relay=Label(frame_account,text="count", font=('Arial',12,'normal'))
    entry_relay.grid(column=11, row=2, padx=10,pady=5)
    relay_button.grid(column=12, row=2, padx=10,pady=5)
    relay_d_button.grid(column=13, row=4, padx=10,pady=5)

    def Close_profile(event):
       frame_account.place_forget()
       button_beau=tk.Button(root, 
                  highlightcolor='WHITE',
                  text='Relay',
                  font=('Arial',12,'bold'),
                  command=open_relay            
                  )
       button_beau.place(relx=0.2,rely=0.17) 
       out_pubkey.place(relx=0.02,rely=0.03,relheight=0.27,relwidth=0.4) 
     
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
    out_pubkey.place(relx=0.02,rely=0.03,relheight=0.46,relwidth=0.4)
    frame_account.place(relx=0.03,relheight=0.2,rely=0.27)

out_pubkey = ttk.LabelFrame(root, text=" Relay", labelanchor="n", padding=10)
out_pubkey.place(relx=0.02,rely=0.03,relheight=0.27,relwidth=0.4)   
button_beau=tk.Button(root,   highlightcolor='WHITE',text='Relay',font=('Arial',12,'bold'),command=open_relay )
button_beau.place(relx=0.2,rely=0.17) 

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

button_dwn.place(relx=0.1,rely=0.17)

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

async def get_outbox_relay(client):
   if public_list!=[]:
    f=Filter().authors(public_list).kind(Kind(10002))
   else: 
    f=Filter().kind(Kind(10002)).limit(10)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   return z

async def search_box_relay():
        
    client = Client(None)
    
    if relay_list!=[]:
       #print(relay_list)
       for jrelay in relay_list:
        relay_url = RelayUrl.parse(jrelay)
        await client.add_relay(relay_url)
             
    else:
        relay_url_1 = RelayUrl.parse("wss://nos.lol/")  
        await client.add_relay(relay_url_1)
        relay_url_x = RelayUrl.parse("wss://nostr.mom/")
        await client.add_relay(relay_url_x)
        relay_url_2 = RelayUrl.parse("wss://purplerelay.com/")
        await client.add_relay(relay_url_2)
    await client.connect()
    relay_add=get_note(await get_outbox_relay(client))
    if relay_add !=None and relay_add!=[]:
           i=0
           while i<len(relay_add):
            for xrelay in tags_string(relay_add[i],'r'):
             
              if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay not in Bad_relay_connection:
               if xrelay not in relay_list:
                if len(relay_list)<6:
                    relay_list.append(xrelay) 
              
            i=i+1          

Bad_relay_connection=[]

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

p_tag = tk.Label(root, text="Pubkey",font=("Arial",12,"bold"))
entryp_tag=ttk.Entry(root,font=("Arial",12),width=12)
p_tag.place(relx=0.08,rely=0.07,relwidth=0.1)
entryp_tag.place(relx=0.1,rely=0.11 )
p_view = tk.Label(root, text="", font=("Arial",12))
p_view.place(relx=0.05,rely=0.11 )
public_list=[]

def p_show():
    title=entryp_tag.get()
    
    if len(title)==64 or len(title)==63:
        if len(title)==63:
           title=PublicKey.parse(title).to_hex()
       
        if convert_user(title)!=None:
         if title not in public_list:
          
            if len(public_list)>=1:
                i=1
                while len(public_list)>i:
                 public_list.pop(1)
                p_view.config(text=str(len(public_list)))
                entryp_tag.delete(0, END)  
            else:  
                public_list.append(convert_user(title))
                p_view.config(text=str(len(public_list)))
                entryp_tag.delete(0, END) 
                return public_list
        
          
         else:
              p_view.config(text=str(len(public_list)))
              
              entryp_tag.delete(0, END) 
              return public_list
        else:
         p_view.config(text=str(len(public_list)))
         entryp_tag.delete(0, END) 
    else:
       entryp_tag.delete(0, END) 
       if len(public_list)>0:
        p_view.config(text=str(len(public_list)))

p_button = tk.Button(root, text="add Pubkey", font=("Arial",12,"bold"), command=p_show)
p_button.place(relx=0.2,rely=0.10)

def Clear_pubkey():
   public_list.clear()
   p_view.config(text="")

p_clear_button = tk.Button(root, text="x", font=("Arial",12,"bold"), command=Clear_pubkey)
p_clear_button.place(relx=0.3,rely=0.10)

root.mainloop()