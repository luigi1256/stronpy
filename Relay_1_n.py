import asyncio
from datetime import timedelta
from asyncio import get_event_loop
from nostr_sdk import *
import requests
import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
root = tk.Tk()
root.geometry("1250x800")
root.title("Relay")

def on_call_server(event):
    label_n_lay.config(text="Relay: "+ str(len(relay_list)))
    call_r_lay()
    combo_list_lay["values"]=relay_list
    label_n_lay.config(text="Relay: "+ str(len(relay_list)))
    combo_list_lay.set("Relay List")

async def get_result_(client,relay_1):
    
    f = Filter().kind(Kind(10002)).reference(relay_1).limit(10)
    
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Search_r_lay(relay_1):
      try: 
       init_logger(LogLevel.INFO)
       client = Client(None)
       uniffi_set_event_loop(asyncio.get_running_loop())
       relay_url = RelayUrl.parse(relay_1)
       await client.add_relay(relay_url)
       
       await client.connect()
       relays = await client.relays()
       i=0
       document_relay=get_nostr_relay_info(relay_1)
       if document_relay:
        for doc in list(document_relay.keys()):
         print(doc, " : ", document_relay[doc], "\n")
        while i<2:
         for url, relay in relays.items():
            
            
            print(f"Relay: {url}")
            print(f"Connected: {relay.is_connected()}")
            print(f"Status: {relay.status()}")
            stats = relay.stats()
            print("Stats:")
            print(f"    Attempts: {stats.attempts()}")
            print(f"    Success: {stats.success()}")
         await asyncio.sleep(1.0)        
         i=i+1        
        if stats.success()==1 and relay.is_connected()==True:
            await asyncio.sleep(1.0)
            combined_results = await get_result_(client,relay_1)
            if combined_results:
                return combined_results
            else:
                try:
                    number=relay_list.index(relay_1)
                    relay_list.pop(number)
                except ValueError as b:
                    print(b,"\n",relay_list,relay_1) 
      
      except IOError as e:
               print(e) 

relay_list=[]

def call_r_lay():
  if combo_list_lay.get()!="Relay List":
   if __name__ == "__main__":
    response=asyncio.run( Search_r_lay(combo_list_lay.get()))
    if response:

     note_=get_note(response)
     for jnote in note_:
      for relay_x in tags_string(jnote,"r"):
         if relay_x[0:6]=="wss://" and relay_x[-1]=="/" and relay_x not in relay_list:
            if len(relay_list)<int(label_r_lay.get()):
                relay_list.append(relay_x)

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

frame1=tk.Frame(root,height=100,width=200,background="grey")
max_relay=IntVar()
max_relay.set(6)

label_n_lay = tk.Label(frame1, text="Relay: ", font=('Arial',12,'bold'))
label_lay = tk.Label(frame1, text="Max: ", font=('Arial',12,'bold'))
label_r_lay = tk.Entry(frame1, textvariable=max_relay, font=('Arial',12,'bold'),width=10)
label_n_lay.grid(column=7, row=0,padx=20,pady=5,ipadx=1,ipady=1)
label_lay.grid(column=8, row=2,padx=2,pady=5,ipadx=1,ipady=1)
label_r_lay.grid(column=7, row=2,padx=5,pady=5,ipadx=1,ipady=1)
combo_list_lay = ttk.Combobox(frame1, values=relay_list,font=('Arial',12,'bold'),width=15)
combo_list_lay.grid(column=7, row=1,padx=20,pady=5,ipadx=2,ipady=1)
combo_list_lay.set("Relay List")
combo_list_lay.bind("<<ComboboxSelected>>", on_call_server) 
frame1.place(relx=0.1,rely=0.06)
frame2=tk.Frame(root,height=100,width=200)

def open_relay():
    frame_account=tk.Frame(frame2, background="darkgrey")
    structure_relay = tk.Label(frame_account, text="relay",font=("Arial",12,"bold"))
    entry_relay=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"))
    structure_relay.grid(column=11, row=1, padx=5,pady=5) 
    button_beau.place_forget()
    
    def relay_class():
     if entry_relay.get()!="": 
        if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/":
         if len(relay_list)<int(label_r_lay.get()): 
           
            if entry_relay.get() not in relay_list:
                relay_list.append(entry_relay.get())
                #print(relay_list)  
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=1)
            entry_relay.delete(0, END)
            combo_bo_r['value']=relay_list
            combo_list_lay['value']=relay_list
            label_n_lay.config(text="Relay: "+ str(len(relay_list)))
            combo_list_lay.set("Relay List")
            combo_bo_r.set("Relays set")
            label_relay.config(text="Name relay")
            return relay_list  
         else:
            entry_relay.delete(0, END)
          
     else:
       if relay_list!=[]:  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
          combo_list_lay['value']=relay_list
          label_n_lay.config(text="Relay: "+ str(len(relay_list))) 
          combo_list_lay.set("Relay List")
          combo_bo_r.set("Relays set")
          label_relay.config(text="Name relay")
       else:
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
          combo_list_lay['value']=relay_list
          label_n_lay.config(text="Relay: "+ str(len(relay_list)))
          combo_list_lay.set("Relay List")
          combo_bo_r.set("Relays set")
          label_relay.config(text="Name relay")

    def remove_one_relay():
     if combo_bo_r.get()!="":
        if combo_bo_r.get() in relay_list:
            number=relay_list.index(combo_bo_r.get())
            relay_list.pop(number)
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=1)
            combo_bo_r['value']=relay_list
            combo_list_lay['value']=relay_list
            label_n_lay.config(text="Relay: "+ str(len(relay_list)))
            combo_list_lay.set("Relay List")
            combo_bo_r.set("Relays set")
            label_relay.config(text="Name relay")
            return relay_list  
     else:
       if relay_list!=[]:  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
          combo_list_lay['value']=relay_list
          label_n_lay.config(text="Relay: "+ str(len(relay_list)))
          combo_list_lay.set("Relay List")
          combo_bo_r.set("Relays set")
          label_relay.config(text="Name relay")
           
       else:
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list       
          combo_list_lay['value']=relay_list     
          label_n_lay.config(text="Relay: "+ str(len(relay_list)))  
          combo_list_lay.set("Relay List")
          combo_bo_r.set("Relays set")
          label_relay.config(text="Name relay")

    relay_button = tk.Button(frame_account, text="Add [R] ", font=("Arial",12,"normal"),background="grey", command=relay_class)
    counter_relay=Label(frame_account,text="count",font=("Arial",12,"normal"))
    entry_relay.grid(column=11, row=2, padx=10,pady=5)
    relay_button.grid(column=12, row=2, padx=10,pady=5)
    relay_d_button = tk.Button(frame_account, text="Remove [R]", font=("Arial",12,"normal"),background="grey", command=remove_one_relay)
    relay_d_button.grid(column=13, row=3, padx=10,pady=5)

    def Close_profile(event):
       frame_account.destroy()
       button_beau.place(relx=0.45,rely=0.1) 
        
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
    frame_account.grid(row=1,column=0,rowspan=2, columnspan=4,pady=5)
    frame2.place(relx=0.35,rely=0.06,relwidth=0.42,relheight=0.3)

button_beau=tk.Button(root,  highlightcolor='WHITE',text='Relay',font=('Arial',12,'bold'),command=open_relay )
button_beau.place(relx=0.45,rely=0.1) 

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


root.mainloop()