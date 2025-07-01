#search result B0
import asyncio
from nostr_sdk import Client, Filter, Keys, NostrSigner, init_logger, LogLevel, EventBuilder, Metadata,Kind
from nostr_sdk import *
from nostr_sdk import Keys,Filter,Client, Event,EventBuilder,Metadata,PublicKey,EventId,Nip19Event,Nip19,Nip19Profile,Nip21,Timestamp
from datetime import timedelta 
import textwrap
import json
import ast
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import calendar
from bs4 import BeautifulSoup
import requests

# Widget funtion 
# open_profile # add_db_list # print_text # show_Teed #show_noted #print_people #print_list_tag

def get_site_description(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find("meta", attrs={"name": "description"})
        if description:
            return description.get("content", "No description found.")
        return "No meta description tag found."
    except requests.RequestException:
        return "Failed to fetch the site."

def is_site_up(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
   
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

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

def search_three(notes,x):
    note=get_note(notes)
    Z=[]
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z

def evnt_id(id):
     test2=EventId.parse(id)
     return test2

root = Tk()
root.title("Search Example")
root.geometry("1300x800")

def since_day(number):
    import datetime
    import calendar
    date = datetime.date.today() - datetime.timedelta(days=number)
    t = datetime.datetime.combine(date, datetime.time(1, 2, 1))
    z=calendar.timegm(t.timetuple())
    return z

def return_date_tm(note):
    import datetime
    date_2= datetime.datetime.fromtimestamp(float(note["created_at"])).strftime("%a"+", "+"%d "+"%b"+" %Y")
    date= date_2+ " "+ datetime.datetime.fromtimestamp(float(note["created_at"])).strftime('%H:%M')
    return date

frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
frame_time=tk.Frame(root,height=100,width=200)
public_list=[]
relay_list=[]
db_list_note=[]
db_pin=[]
relay_search_list=[]
Bad_relay_connection=["wss://r.kojira.io/","wss://relay.noswhere.com/","wss://relay.nostrils.band/", "wss://relay.roli.social/","wss://relay.siamdev.cc/","wss://relay.damus.io/", "wss://relay.notoshi.win/","wss://relay.mostr.pub/","wss://yabu.me/","wss://relay-jp.nostr.wirednet.jp/","wss://grownostr/","wss://relay.onlynostr.club/","wss://00bb97abe00326e97091a24c7b16a412053cd8394a5c2be997798ed53f4bbe67/","wss://0.0.0.3/"]
hash_list_notes=[]

def search_for_channel(note_hash):
     Notes=db_pin
     if Notes:
        hash_list_notes.clear()
        for note_x in Notes:
            if note_hash in tags_string(note_x,"t"): 
               hash_list_notes.append(note_x)
        return hash_list_notes      

def move_to_pin():
   """From note to PIN"""
   if db_list_note!=[]:
      for note_x in db_list_note:
         if note_x not in db_pin and note_x["kind"]==39701:
            db_pin.append(note_x)

def open_profile():
    """Widget function \n
    -- add a pubkey and relays to search
    """
    frame_account=tk.Frame(root, background="darkgrey")
    structure_tag0 = tk.Label(frame_account, text="Insert a pubkey",font=("Arial",12,"bold"))
    structure_tag0.grid(column=9, row=1, padx=5,pady=5) 
    entry_pubblished0=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"))
    entry_pubblished0.grid(column=9, row=2, padx=5,pady=5)
    button_beau.config(text="Account",foreground="black") 
    
    def npub_class():
     if len(entry_pubblished0.get())==63 or len(entry_pubblished0.get())==64:
      Npub=PublicKey.parse(entry_pubblished0.get())
      if Npub not in public_list:
       public_list.append(Npub)
      counter_npub['text']=str(len(public_list)) 
      counter_npub.grid(column=10,row=1)
      search_relay()
      counter_relay['text']=str(len(relay_list)) 
      counter_relay.grid(column=12,row=1)
      entry_pubblished0.delete(0, END)
      button_beau.config(text="New Account",foreground="black") 
      return Npub
    
    go_button = tk.Button(frame_account, text="Go!", font=("Arial",12,"normal"),background="grey", command=npub_class)
    go_button.grid(column=10, row=2, padx=10,pady=5)
    structure_relay = tk.Label(frame_account, text="Insert a relay",font=("Arial",12,"bold"))
    entry_relay=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"))
    structure_relay.grid(column=11, row=1, padx=5,pady=5) 
   
    def relay_class():
     if entry_relay.get()!="":
        if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/":
           
            if entry_relay.get() not in relay_list:
                relay_list.append(entry_relay.get())
                print(relay_list)  
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=1)
            entry_relay.delete(0, END)

            return relay_list  
    
    relay_button = tk.Button(frame_account, text="Go!", font=("Arial",12,"normal"),background="grey", command=relay_class)
    counter_relay=Label(frame_account,text="count")
    counter_npub=Label(frame_account,text="count")
    entry_relay.grid(column=11, row=2, padx=5,pady=5)
    relay_button.grid(column=12, row=2, padx=10,pady=5)

    def Close_profile(event):
       public_list.clear()
       relay_list.clear()
       frame_account.destroy()   
          
    button_close=tk.Button(frame_account, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=1, padx=5, columnspan=1) 
    frame_account.place(relx=0.5,rely=0.001,relheight=0.21,relwidth=0.45)

button_beau=tk.Button(frame1,highlightcolor='WHITE',text='Account',font=('Arial',12,'bold'),command=open_profile)
button_beau.grid(column=9, row=0, padx=10, columnspan=4,pady=5) 

def search_relay():
   if relay_list==[]:
    if __name__ == "__main__":
     asyncio.run(outboxes())
   else:
       search_search_relay() 
  
def search_search_relay():
    if relay_list!=[] and public_list!=[]:
     test_note=[]
     if __name__ == "__main__":
        test_note=asyncio.run(outboxes())
     if test_note!=None and test_note!=[]:   
        pin_note=search_three(test_note,39701)
        for pin_x in pin_note:
           if pin_x not  in db_list_note:
              db_list_note.append(pin_x)

scroll_bar_mini = tk.Scrollbar(frame1)
scroll_bar_mini.grid( sticky = NS,column=4,row=0,rowspan=3)
second_label10 = tk.Text(frame1, padx=10, height=5, width=25, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'))
scroll_bar_mini.config( command = second_label10.yview )
second_label10.grid(padx=10, column=1, columnspan=3, row=0, rowspan=3) 
frame_upfront=Frame(root)
db_frame = ttk.LabelFrame(root, text="DB", labelanchor="n", padding=10)


def url_speed(string):
 z=string
 for j in z.split():
    if j[0:8]=="https://":
        return str(j)[8:]   
    if j[0:7]=="http://":
      return str(j)[7:]  
    return str(string)  

def d_url_speed(string):
 j=string
 if j[0:8]=="https://":
        return str(j)   
 if j[0:7]=="http://":
      return str(j)  
 return str("https://"+string)  
 
def add_db_list():
        """Widget function \n
        Add notes to pin list"""
        
        Frame_block=Frame(root,width=50, height=20)
        db_frame.place(relx=0.69, rely=0.22,relwidth=0.24,relheight=0.23)       
        button10=tk.Button(Frame_block, highlightcolor='Blue',text='PINs',font=('Arial',12,'bold'),command=move_to_pin)

        def Close_block(event):
            Frame_block.destroy()
            db_frame.place_forget()
        
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=4, row=0, padx=5, columnspan=2,rowspan=2) 
            
        def search_block_list():
            label_string_block1.set(len(db_list_note))    

        def delete_block_list():
            db_list_note.clear()
            label_string_block1.set(len(db_list_note))   

        def PIN_count():
           label_link_var.set(len(db_pin))

        def clear_db_pin():
            db_pin.clear()
            label_link_var.set(len(db_pin))   
                 
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey",font=('Arial',12,'normal'))
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ",font=('Arial',12,'normal'))
        random_block1.grid(column=1,row=0,padx=5,pady=5)
        clear_link=Button(Frame_block, command=clear_db_pin, text= "Clear PIN: ",background="darkgrey",font=('Arial',12,'normal'))
        clear_link.grid(column=0,row=1,padx=5,pady=5)    
        random_count=Button(Frame_block, command=PIN_count, text= "DB PIN: ",font=('Arial',12,'normal'))
        random_count.grid(column=1,row=1,padx=5,pady=5)
        label_string_block1=StringVar()
        label_link_var=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1,font=('Arial',12,'normal'))
        label_block_list1.grid(column=2,row=0,pady=5)
        label_var_list1=Label(Frame_block, textvariable=label_link_var,font=('Arial',12,'normal'))
        label_var_list1.grid(column=2,row=1,pady=5)
        button10.grid(column=1, row=2, pady=5)
        Frame_block.place(relx=0.7,rely=0.25,relheight=0.19,relwidth=0.2)
        
button_block=tk.Button(root, highlightcolor='WHITE', text='DB count',font=('Arial',12,'bold'),command=add_db_list )
button_block.place(relx=0.75,rely=0.3)

async def get_outbox(client):
    if public_list!=[]:
       f = Filter().authors(public_list).kind(Kind(10002))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_public_pin(client):
   if public_list!=[]:
       f = Filter().authors(public_list).kind(Kind(39701))
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec()]
   return z
   
async def get_resutl(client):
    f = Filter().search(entry_var.get()).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_result_(client):
   if entry_var.get()!="":  
    if Checkbutton5.get() == 1:
          f = Filter().search(entry_var.get()).kind(Kind(39701)).since(timestamp=Timestamp.from_secs(since_day(int(since_entry.get())))).until(timestamp=Timestamp.from_secs(since_day(int(until_entry.get())))).limit(10)
    else:
          url=url_speed(entry_var.get())
          f = Filter().identifier(url).kind(Kind(39701)).since(timestamp=Timestamp.from_secs(since_day(int(60)))).until(timestamp=Timestamp.from_secs(since_day(int(0)))).limit(10)
          print(url)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_search_relay(client):
   if public_list!=[]:
    f=Filter().authors(public_list).kind(Kind(10007))
   else: 
    f=Filter().kind(Kind(10007)).limit(10)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec()]
   return z

#async function 
    
async def outboxes():
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       for jrelay in relay_list:
          await client.add_relay(jrelay)
       await client.connect()   
       note= await get_public_pin(client) 
       return note     
    else:
       await client.add_relay("wss://nostr.mom/")
       await client.add_relay("wss://relay.damus.io/")
       await client.add_relay("wss://nostr.wine/")
       await client.add_relay("wss://relay.primal.net/")
       await client.connect()
       relay_add=get_note(await get_outbox(client))
       if relay_add !=None and relay_add!=[]:
           i=0
           while i<len(relay_add):
            for xrelay in tags_string(relay_add[i],'r'):
              if xrelay[0:6]=="wss://" and xrelay[-1]=="/":
               if xrelay not in relay_list:
                 relay_list.append(xrelay) 
              else:
                 print(xrelay )   
            i=i+1             
    
async def search_box_relay():
        
    client = Client(None)
    
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(jrelay)
             
    else:
       await client.add_relay("wss://nostr.mom/")
       
    await client.connect()
    relay_add=get_note(await get_search_relay(client))
    if relay_add !=None and relay_add!=[]:
           i=0
           while i<len(relay_add):
            for xrelay in tags_string(relay_add[i],'relay'):
              if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay not in Bad_relay_connection:
               if xrelay not in relay_search_list:
                relay_search_list.append(xrelay) 
              
            i=i+1             
    
async def Search_text():
    init_logger(LogLevel.INFO)
    client = Client(None)
    
    if relay_search_list!=[]:
       for jrelay in relay_search_list:
          await client.add_relay(jrelay)
       await client.connect()
       await asyncio.sleep(2.0)

       combined_results = await get_result_(client)
       if combined_results:
        return combined_results
     
    await search_box_relay()
    print("found ", len(relay_search_list), " relays")

#call function

def call_text():
  if entry_var.get()!="":
   if __name__ == "__main__":
    response=asyncio.run(Search_text())
    if response:

     note_=get_note(response)
     for jnote in note_:
       if jnote not in db_list_note:
          db_list_note.append(jnote)
          
       if len(jnote["content"])<300:
          second_label10.insert(END, str("https://")+str(tags_string(jnote,"d")[0]+"\n"+jnote["content"]))
                    
       second_label10.insert(END,"\n"+"____________________"+"\n")
       second_label10.insert(END,"\n"+"\n")
     move_to_pin()   
       
    else:
       print("empty")
  else:     
       if relay_search_list==[]:
          if __name__ == "__main__":
            response=asyncio.run(Search_text())
          if len(relay_search_list)>0:
             button_close_search["text"]="Search 🔍 url" 
          
def call_hashtag():
  if relay_search_list!=[]:
  
   if __name__ == "__main__":
    response=asyncio.run(Get_kind_number(39701))
    if response!= None and response!=[]:
       for resp_x in get_note(response):
          if resp_x not in db_list_note:
             db_list_note.append(resp_x) 
       move_to_pin()

def five_event():
     if Checkbutton5.get() == 0:
        Button5.config(text= " 60 day")
        frame_time.grid_forget()
        
     else:
       
        Button5.config(text= "Time")
        frame_time.grid(column=0,row=5, columnspan=9,rowspan=3)

frame2=tk.Frame(root,height=100,width=200, background="darkgrey")
Checkbutton5 = IntVar()         
Button5 = Checkbutton(frame1, text = "60 day", variable = Checkbutton5, onvalue = 1, offvalue = 0, height = 2, width = 10,font=('Arial',16,'normal'),command=five_event)
Button5.grid(column=0, row=0,rowspan=3,padx=10)     
since_variable=IntVar(value=1)
since_entry=Entry(frame_time,textvariable=since_variable,font=("Arial",12,"normal"),width=5)
until_variable=IntVar()
until_entry=Entry(frame_time,textvariable=until_variable,font=("Arial",12,"normal"),width=5)

def next_since():
   since_variable.set(int(since_entry.get()) + 1)

def back_since():
   if int(since_entry.get())- 1<1:
      since_variable.set(int(1))
   else:
    if int(since_entry.get())- 1==int(until_entry.get()):
       since_variable.set(since_entry.get())
    else:   
     since_variable.set(int(since_entry.get())- 1)   

def next_until():
   if int(until_entry.get()) + 1>=int(since_entry.get()):
       until_variable.set(until_entry.get())
   else:    
    until_variable.set(int(until_entry.get()) + 1)

def back_until():
   if int(until_entry.get())- 1<0:
      until_variable.set(0)
   else:
    until_variable.set(int(until_entry.get())- 1) 

wall_2=tk.Label(frame_time, text="",background="lightgrey",height=4)
label_since=Label(frame_time,text="day since",font=("Arial",12,"normal"))
button_mov=tk.Button(frame_time,text="➕",command=next_since)   
button_back=tk.Button(frame_time,text="➖",command=back_since)  
label_until=Label(frame_time,text="day until",font=("Arial",12,"normal"))
label_until.grid(column=6,row=5,pady=10)
button_mov_dep=tk.Button(frame_time,text="➕",command= next_until)       
button_mov_dep.grid(column=7, row=5,padx=5,pady=5)
button_back_dep=tk.Button(frame_time,text="➖",command=back_until)       
button_back_dep.grid(column=7, row=6,padx=5,pady=5)
since_entry.grid(column=1,row=6,pady=10,padx=10)
until_entry.grid(column=6,row=6,pady=10)
wall_2.grid(column=0, row=5,pady=5, rowspan=2)
label_since.grid(column=1,row=5,pady=10)    
button_mov.grid(column=2, row=5,padx=5,pady=5)     
button_back.grid(column=2, row=6,padx=5,pady=5)     
entry_variable=StringVar()
entry_var=Entry(frame1, textvariable=entry_variable,font=("Arial",12,"bold"),width=17)
entry_var.place(relx=0.31,rely=0.78,relheight=0.18)
button_close_search=tk.Button(frame1, text='Search Relay',font=('Arial',12,'bold'), command=call_text)    
button_close_search.place(relx=0.6,rely=0.77 ) 

async def get_one_Event(client, event_):
    f = Filter().id(EventId.parse(event_))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_id(event_):
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    await client.add_relay("wss://relay.damus.io/")
    await client.add_relay("wss://nos.lol/")
    await client.connect()
    
    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        print("errore")
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

async def get_relays(client, authors):
    f = Filter().authors(authors)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_relay(client, user):
    f = Filter().author(user).kinds([Kind(10014),Kind(31890)])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def feed(authors):
    init_logger(LogLevel.INFO)
    client = Client(None)
    
    await client.add_relay("wss://nos.lol")
    await client.add_relay("wss://nostr.mom")
    await client.add_discovery_relay("wss://purplerelay.com/")

    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_relays(client, authors)
    else:
        combined_results = await get_relay(client, authors)
    
    return combined_results    

def print_text():  
   """Widget function \n
   horizontal view of PIN
   """
   if db_list_note!=[]: 
    frame3=tk.Frame(root,height=120,width= 550)
    canvas = tk.Canvas(frame3,width=500)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")  ))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    s=1    
    if db_pin!=[]: 
        for note in db_pin:
           
            var_id=StringVar()
            label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=300)
            var_id.set(str("https://")+str(tags_string(note,"d")[0])) 
            
            label_id.grid(pady=2,column=1,row=s)
            
            def print_id(test):
               try: 
                print("description ",get_site_description(str("https://")+str(tags_string(test,"d")[0])))
                print("title ",tags_string(test,"title")[0])
                print("hashtag ",tags_string(test,"t"))
                if is_site_up(str("https://")+str(tags_string(test,"d")[0]))==True:
                   print(str("https://")+str(tags_string(test,"d")[0]),"\n","site up? ", is_site_up(str("https://")+str(tags_string(test,"d")[0])))
          
               except IndexError as e:
                  print (e) 

            def print_var(test):
                print(test)
                    
            button=Button(scrollable_frame,text=f"Print me!", command=lambda val=note: print_var(val))
            button.grid(column=0,row=s,padx=10,pady=5)
            button_grid2=Button(scrollable_frame,text=f"Click me for info!", command=lambda val=note: print_id(val))
            button_grid2.grid(row=s,column=2,padx=10,pady=5)
            root.update()  
            s=s+1
   
    canvas.pack(side="left", fill="y", expand=True)
    scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.01,rely=0.33,relwidth=0.6)      
    
    def Close_print():
       frame3.destroy()  
    
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)       

def show_Teed():
   """Widget function \n
   Vertical feed of PINs
   """
   frame2=tk.Frame(root)  
   canvas_1 = tk.Canvas(frame2)
   scrollbar_1 = ttk.Scrollbar(frame2, orient="vertical", command=canvas_1.yview)
   scrollable_frame_1 = ttk.Frame(canvas_1)
   scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all") ))

   canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
   canvas_1.configure(yscrollcommand=scrollbar_1.set)
   if db_pin!=[]:
  
    s=1
    
    for note in db_pin:
     try:
      context0="id: "+note["id"]+"\n"+"Pubkey: "+note['pubkey']+"\n"+"\n"
      if note['tags']!=[]:
       if tags_string(note,"title")!=[]:
        linkl_url=d_url_speed(tags_string(note,"d")[0])
        context1=" "+"\n"+linkl_url+"\n"+note['content']+"\n"+tags_string(note,"title")[0]+"\n"+"\n"
        context2="\n"
        for xnote in tags_string(note,"t"):
         context2=context2+"#"+str(xnote) +"\n"
       else: 
        linkl_url=d_url_speed(tags_string(note,"d")[0])
        context1=linkl_url+"\n"+note['content']+"\n"
        context2="\n"
        for xnote in tags_string(note,"t"):
         context2=context2+"#"+str(xnote) +"\n"
      else: 
        context1="\n"+note['content']+"\n"
        context2=""
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0+context1+context2)
      label_id.grid(pady=2,column=0, columnspan=3)
      
      def print_id_2(entry):
           number=list(db_pin).index(entry)
           print(number)
           print(entry)
           print(db_pin[number]["tags"])
                  
      def print_var_2(entry):
              number=list(db_pin).index(entry)
              print(number)
              if number<=len(db_pin):
               note_number=db_pin[number]
              try:   
                print("d ",str(tags_string(note_number,"d")[0]))
                
                print("description ",get_site_description(str("https://")+str(tags_string(note_number,"d")[0])))
                if tags_string(note_number,"title")!=[]:
                 print("title ",tags_string(note_number,"title")[0])
                if tags_string(note_number,"t")!=[]: 
                 print("hashtag ",tags_string(note_number,"t"))
                if is_site_up(str("https://")+str(tags_string(note_number,"d")[0]))==True:
                   print(str("https://")+str(tags_string(note_number,"d")[0]),"\n","site up? ", is_site_up(str("https://")+str(tags_string(note_number,"d")[0])))
              except TypeError as e:
                 print(e)
          
      button=Button(scrollable_frame_1,text=f"Click me for info!", command=lambda val=note: print_var_2(val))
      button.grid(column=0,row=s,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"Number note", command=lambda val=note: print_id_2(val))
      button_grid2.grid(row=s,column=1,padx=5,pady=5)      
      s=s+2  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.37,rely=0.34,relwidth=0.31,relheight=0.35)
    
    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.45,rely=0.73,relwidth=0.1)      

button4=tk.Button(frame1,text="print text",command=print_text)
button4.grid(pady=5,padx=5) 

def open_frame():
 if Check_open.get()==1:
  Check_open.set(0)
  button_frame_c=Button(frame1,command=close_frame1,text="Close ❌",font=("Arial",12,"normal"))
  button_frame_c.grid(column=9, row=1, rowspan=2, padx=10, columnspan=4,pady=5)
  frame1.grid(column=5,columnspan=11, row=0, rowspan=3)

def close_frame1():
   if Check_open.get()==0:  
    Check_open.set(1)
    frame1.grid_forget()

Check_open = IntVar() 
Check_open.set(1)
button_read=Button(frame1,text="Stamp", command=show_Teed,font=("Arial",12,"normal"))
button_read.grid(column=9, row=3, padx=10, columnspan=4,pady=5) 
entry_channel=StringVar()

def show_noted():
   """Widget function \n
   Open the hashtag feed of the PIN
   """
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
   if hash_list_notes!=[]:
  
    s=1
    
    for note in hash_list_notes:
     try:
      context0="id: "+note["id"]+"\n"+"Pubkey: "+note['pubkey']+"\n"+"\n"
      if note['tags']!=[]:
       url_link=d_url_speed(tags_string(note,"d")[0])
       if tags_string(note,"title")!=[]:
        context1=url_link+" "+"\n"+note['content']+"\n"+"\n"+tags_string(note,"title")[0]+"\n"+"\n"
        context2="\n"
        for xnote in tags_string(note,"t"):
         context2=context2+"#"+str(xnote) +"\n"
       else: 
        d_url_speed(tags_string(note,"d")[0])
        context1=url_link+"\n"+note['content']+"\n"
        context2="\n"
        for xnote in tags_string(note,"t"):
         context2=context2+"#"+str(xnote) +"\n"
      else: 
        context1="\n"+note['content']+"\n"
        context2=""
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0+context1+context2)
      label_id.grid(pady=2,column=0, columnspan=3)
      
      def print_id(entry):
           number=list(hash_list_notes).index(entry)
           print(number)
                  
      def print_var(entry):
              note_number=entry
              try:   
                print(str(tags_string(note_number,"d")[0]))
                
                print("description ",get_site_description(str("https://")+str(tags_string(note_number,"d")[0])))
                print("title ",tags_string(note_number,"title")[0])
                print("hashtag ",tags_string(note_number,"t"))
                if is_site_up(str("https://")+str(tags_string(note_number,"d")[0]))==True:
                   print(str("https://")+str(tags_string(note_number,"d")[0]),"\n","site up? ", is_site_up(str("https://")+str(tags_string(note_number,"d")[0])))
              except TypeError as e:
                 print(e)
                              
      button=Button(scrollable_frame_1,text=f"Click me for info!", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"Number note!", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s,column=1,padx=5,pady=5)      
      s=s+2  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.36,rely=0.34,relwidth=0.32,relheight=0.35)

    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.5,rely=0.72,relwidth=0.1)      

def list_hashtag_fun():
    hashtag_list=[]
    if db_pin!=[]:
        for note_x in db_pin:
            if tags_string(note_x,"t")!=[]:
                for hash_y in tags_string(note_x,"t"):
                    if hash_y not in hashtag_list:
                        hashtag_list.append(hash_y)
        return hashtag_list       
    else:
       return hashtag_list       

def list_people_fun():
    people_list=[]
    if db_pin!=[]:
        for note_x in db_pin:
            if note_x["pubkey"] not in people_list:
                        people_list.append(note_x["pubkey"])
        return people_list       
    else:
       return people_list

def pubkey_id(test):
   print("Pubkey", test,"\n","Npub ",PublicKey.parse(test).to_bech32())
   client=Client(None)
   if __name__ == "__main__":
    asyncio.run(run_metadata(client,test))   
   
async def run_metadata(client,test):
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://relay.mostr.pub/")
    await client.connect()
    metadata = await Client.fetch_metadata(client,PublicKey.parse(test),timeout=timedelta(seconds=10))  
    if metadata!=None: 
     if metadata.get_name()!=None:
       print("name ",metadata.get_name())
     else:  
        print("display name ",metadata.get_display_name())
    else:
       print("undefined ")    
    
def print_people(): 
   """Widget function \n
   People write PINs  \n
   Pubkey print name
   """
   if db_pin!=[]:  
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
    test1=list_people_fun()
    ra=0
    se=1
            
    while ra<len(test1):
                button_grid1=Button(scrollable_frame,text=f"{test1[ra][0:10]} ", command=lambda val=test1[ra]: pubkey_id(val))
                button_grid1.grid(row=s,column=1,padx=5,pady=5)
                
                if len(test1)>se:
                 button_grid2=Button(scrollable_frame,text=f"{test1[ra+1][0:10]}", command= lambda val=test1[ra+1]: pubkey_id(val))
                 button_grid2.grid(row=s,column=2,padx=5,pady=5)
            
                root.update()  
                root.after(100)
                s=s+1
                se=se+2
                ra=ra+2  

    canvas.pack(side="left", fill="y", expand=True)
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.7,rely=0.6,relwidth=0.25)      

    def Close_print():
       frame3.destroy()  
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

button_people_=tk.Button(root,text="Print People",command=print_people, font=('Arial',12,'bold'))
button_people_.place(relx=0.75,rely=0.5) 

def print_list_tag(): 
   """Widget function \n
   List of hashtag

   """
   open_frame()
   if db_pin!=[]:  
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

                Channel_frame = ttk.LabelFrame(root, text="Associated tag", labelanchor="n", padding=10)
                Channel_frame.place(relx=0.51,rely=0.01,relheight=0.19,relwidth=0.4) 
                button_open=Button(root, command=show_noted, text="Open Tag",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
                button_search=tk.Button(root, text="Relay",font=('Arial',12,'bold'), command=call_text)    
                entry_channel.set(test)
                search_for_channel(test)
                entry_space=tk.Entry(root, textvariable=entry_channel, width=15,font=("Arial",12,"bold"))
                entry_space.place(relx=0.53,rely=0.11,relwidth=0.15,relheight=0.04,x=5)
                Label_channel_name=tk.Label(root, text="hashtag",font=("Arial",12,"bold"))
                Label_channel_name.place(relx=0.55,rely=0.06)
                button_go=Button(root,text="Update", command=call_hashtag,font=('Arial',12,'normal'),foreground="blue")
                button_go.place(relx=0.72,rely=0.06)
                button_open.place(relx=0.8,rely=0.05)
                button_search.place(relx=0.83,rely=0.12)

                def close_button():
                   button_go.place_forget()
                   entry_channel.set("")
                   entry_space.place_forget()
                   button_clo.place_forget()
                   Label_channel_name.place_forget()
                   button_open.place_forget()
                   Channel_frame.place_forget()
                   button_search.place_forget()

                button_clo=Button(root,text="Close", command=close_button,font=('Arial',12,'bold'),foreground="red")
                button_clo.place(relx=0.72,rely=0.12)   
           
            ra=0
            se=1
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
    frame3.place(relx=0.01,rely=0.33,relwidth=0.25)      

    def Close_print():
       frame3.destroy()  

    if test1!=[]:   
     button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
     button_close_.pack(pady=5,padx=5)    
    else:
       Close_print() 
   else:
      
      Channel_frame = ttk.LabelFrame(root, text="Associated tag", labelanchor="n", padding=10)
      Channel_frame.place(relx=0.51,rely=0.01,relheight=0.19,relwidth=0.4) 
      entry_space=tk.Entry(root, textvariable=entry_channel, width=15,font=("Arial",12,"bold"))
      entry_space.place(relx=0.53,rely=0.11,relwidth=0.15,relheight=0.04,x=5)
      Label_channel_name=tk.Label(root, text="hashtag",font=("Arial",12,"bold"))
      Label_channel_name.place(relx=0.55,rely=0.06)
      button_go=Button(root,text="Update", command=call_hashtag,font=('Arial',12,'normal'),foreground="blue")
      button_go.place(relx=0.72,rely=0.06)
      button_open=Button(root, command=show_noted, text="Open Tag",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
      button_open.place(relx=0.8,rely=0.05)
      button_search=tk.Button(root, text="Relay",font=('Arial',12,'bold'), command=call_text) 
      button_search.place(relx=0.83,rely=0.12)

      def close_button():
           button_go.place_forget()
           entry_channel.set("")
           entry_space.place_forget()
           button_clo.place_forget()
           Label_channel_name.place_forget()
           button_open.place_forget()
           Channel_frame.place_forget()
           button_search.place_forget()

      button_clo=Button(root,text="Close", command=close_button,font=('Arial',12,'bold'),foreground="red")
      button_clo.place(relx=0.72,rely=0.12)  
           
button_tag=tk.Button(root,text="# List",command=print_list_tag, font=('Arial',12,'bold'))
button_tag.place(relx=0.2,rely=0.24)

async def get_kind(client, event_):
    hashtag_list=list_hashtag_fun()
    if hashtag_list==[]:
     
     print(entry_channel.get())
     if entry_channel.get() not in hashtag_list:
       hashtag_list.append(str(entry_channel.get()))
    f = Filter().kind(Kind(event_)).hashtags(hashtag_list)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_kinds(client, event_):
    f = Filter().kinds(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_kind_number(event_):
    # Init logger
    init_logger(LogLevel.INFO)

    client = Client(None)

    # Add relays and connect
    if relay_search_list!=[]:
       for jrelay in relay_search_list:
          await client.add_relay(jrelay)
       await client.connect()
    
    if isinstance(event_, list):
        test_kind = await get_kinds(client, event_)
    else:
        test_kind = await get_kind(client, event_)
    
    await asyncio.sleep(2.0)
    return test_kind

frame2=Frame(root,width=20,height=1)
menu = Menu(frame2)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="Widget", menu=filemenu)
filemenu.add_command(label="Search frame", command=open_frame)
filemenu.add_command(label="# List", command=print_list_tag)
filemenu.add_separator()
filemenu.add_command(label="Random Relay", command=call_text)
filemenu.add_command(label="DB List", command=add_db_list)
filemenu.add_command(label="People List", command=print_people)

frame2.grid()

root.mainloop()

