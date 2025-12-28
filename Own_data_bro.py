#Own_data_bro

from tkinter import *
import sqlite3
import json
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox 
import asyncio
from nostr_sdk import *
import json
from datetime import timedelta

root = Tk() 
root.geometry("1300x800")
root.title("Event test") 

relay_list=[]
my_dict = {}  #"name",pubkey
my_list = list(my_dict.values())

def on_select(event):
    selected_item = combo_box.get()
    relay_list.clear()
    search_relay()

def since_day_time(day_ago:int):
    import datetime
    date_one = datetime.date.today() - datetime.timedelta(days=day_ago)
    date_two=datetime.datetime.combine(date_one, datetime.time(1, 2, 1)).timestamp()
    return int(date_two)

frame_root=Frame(root,height=100,width=200)
label_profile = Label(frame_root, text="Profile", width=10,font=('Arial',14,'bold'))
label_profile.grid(column=0,row=0,pady=2,columnspan=2)
combo_box = ttk.Combobox(frame_root, values=list(my_dict.keys()),width=15)
combo_box.grid(column=0,row=1,pady=1,padx=10)
combo_box.set("User")
combo_box.bind("<<ComboboxSelected>>", on_select)
Checkbutton6 = IntVar() 
Button6 = Checkbutton(frame_root, text = "NOTIFICATION", variable = Checkbutton6,  onvalue = 1, offvalue = 0, height = 2, width = 10)
Button6.grid(column=1,row=1,pady=1,padx=10)

def open_settings():
    open_new_user()
    open_frame1()
    frame_del()

def close_settings():
    close_new_user()
    close_frame1()
    frame_del_close()    

def frame_del():
        if Check_open_del.get()==1:
            Check_open_del.set(0)
        frame_delete.place(relx=0.34,rely=0.3,relheight=0.3,relwidth=0.28)

def frame_del_close():
    if Check_open_del.get()==0:  
        Check_open_del.set(1)
    frame_delete.place_forget()

frame_delete=Frame(root,height=100,width=200)
Check_open_del = IntVar() 
Check_open_del.set(1)
kind_note=IntVar()
label_delete = Label(frame_delete, text="Delete", width=10,font=('Arial',14,'bold'))
label_delete.grid(column=0,row=1,pady=10,columnspan=2)
label_delete_k = Label(frame_delete, text="kind", width=10,font=('Arial',10,'bold'))
label_delete_k.grid(column=0,row=2,padx=3)
label_delete_d = Label(frame_delete, text="Day", width=10,font=('Arial',10,'bold'))
label_delete_d.grid(column=0,row=3,padx=3)
label_number = Entry(frame_delete, textvariable=kind_note, width=10)
label_number.grid(column=1,row=2,pady=10)
kind_day=IntVar()
label_number_d = Entry(frame_delete, textvariable=kind_day, width=10)
label_number_d.grid(column=1,row=3,pady=10)
numb_d=Button(frame_delete, command=lambda:delete_note(kind_note.get()), text="Delete kind")
numb_d.grid(column=2,row=2,pady=10,padx=2) 
numb_d1=Button(frame_delete, command=lambda: delete_time(kind_day.get()), text="Del day time")
numb_d1.grid(column=2,row=3,pady=10,padx=2) 
numb_close_d=Button(frame_delete, command=frame_del_close, text="Close x")
numb_close_d.grid(column=2,row=1,pady=10,padx=5)    

frame_user=Frame(root,height=100,width=200)
label_user = Label(frame_user, text="Add an User", width=10,font=('Arial',14,'bold'))
label_user.grid(column=0,row=0,pady=10,columnspan=2)
label_user = tk.Label(frame_user, text="Name")
label_user.grid(column=0,row=1,pady=2,padx=10)
label_pubkey = tk.Label(frame_user, text="Pubkey")
label_pubkey.grid(column=1,row=1,pady=2,padx=10)
user_name=StringVar()
label_number = Entry(frame_user, textvariable=user_name, width=15)
label_number.grid(column=0,row=2,pady=2,padx=10)
key_string=StringVar()
label_key = Entry(frame_user, textvariable=key_string, width=15)
label_key.grid(column=1,row=2,pady=2,padx=10)
button_add=Button(frame_user, command=lambda:add_user(user_name.get(),key_string.get()), text="add User")
button_add.grid(column=0,row=3,pady=4,padx=2)

Check_open_2 = IntVar() 
Check_open_2.set(1)

def open_new_user():
    if my_dict=={}:
        if Check_open_2.get()==1:
            Check_open_2.set(0)
        frame_user.place(relx=0.34,rely=0.1,relheight=0.2,relwidth=0.28)

def close_new_user():
    if Check_open_2.get()==0:  
        Check_open_2.set(1)
    frame_user.place_forget()

def open_frame1():
    if Check_open.get()==1:
        Check_open.set(0)
    frame_root.place(relx=0.34,rely=0.005,relheight=0.1,relwidth=0.25)

def close_frame1():
    if Check_open.get()==0:  
        Check_open.set(1)
    frame_root.place_forget()

numb_close_u=Button(frame_user, command=close_new_user, text="Close x")
numb_close_u.grid(column=1,row=3,pady=10,padx=5)    
numb_close_r=Button(frame_root, command=close_frame1, text="Close x")
numb_close_r.grid(column=3,row=1,pady=10,padx=10)    
Check_open = IntVar() 
Check_open.set(1)

def search_relay():
    if __name__ == "__main__":
        asyncio.run(outboxes())

async def get_outbox(client):
  
  if my_dict[combo_box.get()]!="": 
    
    f = Filter().authors(user_convert([my_dict[combo_box.get()]])).kind(Kind(10002))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Search_connection(client:Client):
      try: 
                                                 
       await client.connect()
       relays = await client.relays()
       i=0
       while i<2:
         for url, relay in relays.items():
            
            
            print(f"Relay: {url}")
            print(f"Connected: {relay.is_connected()}")
            print(f"Status: {relay.status()}")
            stats = relay.stats()
            print("Stats:")
            print(f"    Attempts: {stats.attempts()}")
            print(f"    Success: {stats.success()}")
            if stats.success()==1 and relay.is_connected()==True:
               if url not in relay_list:
                  relay_list.append(url)
         await asyncio.sleep(1.0)        
         i=i+1        
      
      except IOError as e:
               print(e) 

async def outboxes():
    init_logger(LogLevel.INFO)
    client = Client(None)
    if relay_list!=[]:
        for jrelay in relay_list:
           await client.add_relay(jrelay)
    else:
       relay_url_3 = RelayUrl.parse("wss://nostr.mom/")
       relay_url_4 = RelayUrl.parse("wss://purplerelay.com/")
       await client.add_relay(relay_url_3)
       await client.add_relay(relay_url_4)
       
    await client.connect()
    result_note=await get_outbox(client)
    if result_note!=None:
     relay_add=get_note(result_note)
     if relay_add !=None and relay_add!=[]:
        i=0
        while i<len(relay_add):
                for xrelay in tags_string(relay_add[i],'r'):
                    if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay[6:9]!="127":
                        if RelayUrl.parse(xrelay) not in relay_list:
                            await client.add_relay(RelayUrl.parse(xrelay))
                await Search_connection(client)         
                i=i+1             
    await asyncio.sleep(2.0)

def test_relay():
    if combo_box.get()!="User":
        if __name__ == "__main__":
            combined_results = asyncio.run(Get_random_kind())
            if combined_results:
                return combined_results 
            else:
                print("not found")
    else:
        test_list=combo_box['values']
        if test_list!="":
            open_frame1()
        open_new_user()    

def no_id(event,Nostr_note):
    Nostr_note_id=[]
           
    for Nostr_x in Nostr_note:
        Nostr_note_id.append(Nostr_x["id"])
    if event.id().to_hex() not in Nostr_note_id: 
        return event

def add_Rel_event(event_,name_db):
    try:
        conn = sqlite3.connect(str(name_db)+'.db')
        c = conn.cursor()
        event=json.loads(event_.as_json())
       
        c.execute('''
        INSERT INTO events (id,pubkey, created_at,kind,tags,content, sig )
        VALUES (?, ?,?, ?,?, ?,?)
        ''', (
            event['id'],event['pubkey'],event['created_at'],event['kind'],json.dumps(event['tags']),event['content'],event['sig']
            ))
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error during the addition of the event: {e}")
    finally:
        if conn:
            conn.close() 
    
def test_input():
    list_event=test_relay()
    if list_event!=None:
        if Checkbutton6.get()==0:   
            list_db=kind1_data_name()
            if list_db:    
                for event in list_event[::-1]:
                    if no_id(event,list_db)!=None:
                        add_Rel_event(event,"historyc2")
                messagebox.showinfo("DB add event","Ok")        
            else:  
                for event in list_event[::-1]:                  
                    add_Rel_event(event,"historyc2")
                messagebox.showinfo("DB add event","Ok")    
        else:
            list_not=kind1_data_name_table("nohistoryc2")
            if list_not:
                for event in list_event[::-1]:
                    if no_id(event,list_not)!=None:
                        add_Rel_table(event,"historyc2","nohistoryc2")
            else:  
                for event in list_event[::-1]:               
                    add_Rel_table(event,"historyc2","nohistoryc2")

def fetch_content(name_db):
    try:
        conn = sqlite3.connect(str(name_db)+'.db')
        c = conn.cursor()
        c.execute('SELECT * FROM events')
        events = c.fetchall()
        return events
    except sqlite3.Error as e:
        print(f"Error while reading events: {e}")
        return []
    finally:
        if conn:
            conn.close()

def initialize_table_relay(name_db,table_event):
    try:
        conn = sqlite3.connect(str(name_db)+'.db')
        c = conn.cursor()
        c.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_event}  (
            id          CHAR(64)    PRIMARY KEY,
            pubkey      CHAR(64)    NOT NULL,
            created_at  BIGINT      NOT NULL,
            kind        INTEGER     NOT NULL,
            tags        List     NOT NULL,  
            content     TEXT        NOT NULL,  
            sig         CHAR(128)   NOT NULL
            )
            ''') 
        conn.commit()
        messagebox.showinfo("DB initialize","Ok")
    except sqlite3.Error as e:
        print(f"Error during the initialization of the database: {e}")
    finally:
        if conn:
            conn.close()

def add_Rel_table(event_,name_db,table_event):
    try:
        conn = sqlite3.connect(str(name_db)+'.db')
        c = conn.cursor()
        event=json.loads(event_.as_json())
       
        c.execute(f'''
        INSERT INTO {table_event} (id,pubkey, created_at,kind,tags,content, sig )
        VALUES (?, ?,?, ?,?, ?,?)
        ''', (
            event['id'],event['pubkey'],event['created_at'],event['kind'],json.dumps(event['tags']),event['content'],event['sig']
            ))
        conn.commit()
        messagebox.showinfo("DB add event","Ok")
    except sqlite3.Error as e:
        print(f"Error during the addition of the event: {e}")
    finally:
        if conn:
            conn.close() 
    
def fetch_content_table(name_db,table_event):
    try:
        conn = sqlite3.connect(str(name_db)+'.db')
        c = conn.cursor()
        c.execute(f' SELECT * FROM {table_event}')
        events = c.fetchall()
        return events
    except sqlite3.Error as e:
        print(f"Error while reading events: {e}")
        return []
    finally:
        if conn:
            conn.close()            

def kind1_data_name():
   try:
    note=fetch_content("historyc2")  
    events=[]
    for j in note:
        val_json=valore_json(j)
        if Event.from_json(str(val_json)).verify():
            events.append(valore_tupla(j))
    
    return events   
   except NostrSdkError as e:
    print(e)                  

def kind1_data_name_table(table_event):
    try:
        note=fetch_content_table("historyc2",table_event)  
        events=[]
        for j in note:
            val_json=valore_json(j)
            if Event.from_json(str(val_json)).verify():
                events.append(valore_tupla(j))
        return events   
    except NostrSdkError as e:
        print(e)                  

def initialize_data_relay(name_db):
    try:
        conn = sqlite3.connect(str(name_db)+'.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id          CHAR(64)    PRIMARY KEY,
            pubkey      CHAR(64)    NOT NULL,
            created_at  BIGINT      NOT NULL,
            kind        INTEGER     NOT NULL,
            tags        List     NOT NULL,  
            content     TEXT        NOT NULL,  
            sig         CHAR(128)   NOT NULL
            )
            ''') 
        conn.commit()
        messagebox.showinfo("DB initialize","Ok")
    except sqlite3.Error as e:
        print(f"Error during the initialization of the database: {e}")
    finally:
        if conn:
            conn.close()

def count_note(n:int):
    list_event=[]
    number_event=kind1_data_name()
    for numb_x in number_event:
        if numb_x["kind"]==n:
            list_event.append(numb_x)
    return list_event    

def Tag_open(string):
    Nostr_note=kind1_data_name()
    tags_one=[]
    if string=="":
        for x in Nostr_note:
            if x['tags']!=[]:
                if tags_string(x, "t")!=[]:
                    for h_tags in tags_string(x, "t"):
                        if h_tags not in tags_one:
                            tags_one.append(h_tags)
    else:
        for v in Nostr_note:
            if v["tags"]!=[]:
                if tags_string(v,"t")!=[]:
                    if string in tags_string(v,"t"):
                        tags_one.append(v)        
    return tags_one

def OpenColumn():
    text_var = StringVar()
    frame3=Frame(root,width=70,height=70, border=5,background="lightgrey")  
    Checkbutton5 = IntVar() 
    frame3.config(background="lightgrey")
    Button5 = Checkbutton(frame3, text = "🔒", variable = Checkbutton5,  onvalue = 1, offvalue = 0, height = 2, width = 10)

    def five_event():
        if Checkbutton5.get() == 1:
            initialize_data_relay(str(input_PC.cget('text')))
        else:
            if Checkbutton6.get()==1:
                initialize_table_relay(str(input_PC.cget('text')),"no"+str(input_PC.cget('text')))

    input_PC = Button(frame3, text = "historyc2", command =five_event, height = 2, width = 10)
    input_PC.grid(column=0, row=0)
    Button5.grid(column=1, row=0)
    entry_t= Entry(frame3, textvariable=text_var,width=60)
    entry_t.grid(column=0,row=1, columnspan=2)
    scroll_bar_mini = tk.Scrollbar(frame3)
    Text_t=Text(frame3, width=45,height=30,wrap="word",undo=True,yscrollcommand = scroll_bar_mini.set)
    scroll_bar_mini.config( command = Text_t.yview )
    scroll_bar_mini.grid( sticky = NS,column=2,row=2,rowspan=3,pady=5)
    Text_t.grid(column=0, row=2, columnspan=2,rowspan=3) 
    Send_pc_message=Button(frame3, command=test_input, text="Send message")
    Send_pc_message.grid(column=0, row=5)

    def Sel_id(id_value):
     try:
        name=input_PC.cget('text')
        conn = sqlite3.connect(str(name)+'.db')
        c = conn.cursor()
        c.execute('SELECT * FROM events WHERE id = ?', (id_value,))
        events = c.fetchall()
        
        return events
     except sqlite3.Error as e:
        print(f"Error while reading events: {e}")
        return []
     finally:
        if conn:
            conn.close()            
    
    def Select_id_tag():    #UI
        if len(entry_t.get())==64:
            event_list=Sel_id(entry_t.get())
            s0=1
            for test in event_list:
                val_json=valore_json(test)
                if Event.from_json(str(val_json)).verify(): 
                    test_x=valore_tupla(test)
                    test_note="note n " +str(s0)+"\n"+  "pubkey: "+str(test_x['pubkey'])+"\n"+"id: "+str(test_x["id"])+"\n"+"Time: "+str(test_x["created_at"])+"\n"+"Content: "+ str(test_x["content"])+"\n"+"\n"
                    Text_t.insert(END,test_note)  
                    s0=s0+1 
    
    def return_note():
        if Checkbutton5.get() == 1:
            Nostr_note=kind1_data_name()[::-1]
            if len(Nostr_note)>0:
                Text_t.delete("1.0","end")
                if entry_t.get()=="":
                    for x in Nostr_note:
                        Text_t.insert(END,"pubkey: "+str(x['pubkey'])+"\n"+"Time: "+str(x['created_at'])
                                      +"\n"+"Content: "+ x['content']+"\n"+"\n")  
                else:
                    for v in Nostr_note:
                        if tags_string(v,"t")!=[]:
                            if entry_t.get() in tags_string(v,"t"):
                                Text_t.insert(END,"pubkey: "+str(v['pubkey'])+"\n"+"Time: "+str(v['created_at'])+"\n"+"Content: " +v['content']+"\n"+"\n"
                                +"Tags:" +"\n"+ str(tags_string(v,"t"))+"\n")       
                        else:
                            None                   

    def return_Tags():
        if Checkbutton5.get() == 1:
                Text_t.delete("1.0","end")
                tag_one=Tag_open(entry_t.get())
                if entry_t.get()=="":
                    for z in tag_one:
                        Text_t.insert(END,"Tags: "+ str(z) +"\n")  
                else:
                    for v in tag_one:                
                        Text_t.insert(END,"pubkey: "+str(v['pubkey'])+"\n"+"Time: "+str(v['created_at'])+"\n"+"kind: "+str(v['kind'])+"\n"+"\n"+"Content: " +v['content']+"\n"
                                    +"Tags:" +"\n"+ str(tags_string(v,"t"))+"\n"+"---------------------"+"\n")             
                    
    def number_count_note(kind:int):
        list_event=count_note(kind)
        if kind==1:
           numb_lab.config(text=str(len(list_event)))
        if kind==30023:
           numb_lab_2.config(text=str(len(list_event)))
                   
    receive_pc_message=Button(frame3, command=return_note, text="return note")
    receive_pc_message.grid(column=1, row=5,pady=2)   
    receive_pc_message=Button(frame3, command=return_Tags, text="return Tags")
    receive_id_message=Button(frame3, command=Select_id_tag, text="return ID")
    receive_pc_message.grid(column=1, row=6,pady=2)              
    receive_id_message.grid(column=0, row=6,pady=2)              
    numb_message=Button(frame3, command=lambda:number_count_note(1), text="numb note")
    numb_message.grid(column=0, row=7,pady=2) 
    numb_post=Button(frame3, command=lambda:number_count_note(30023), text="numb post")
    numb_post.grid(column=1, row=7,pady=2) 
    numb_lab=Label(frame3,text="")
    numb_lab.grid(column=0,row=8)
    numb_lab_2=Label(frame3,text="")
    numb_lab_2.grid(column=1,row=8)
    frame3.grid()
    
    def delete_column(): 
        if Checkbutton5.get() == 0:
            frame3.destroy()
        else:
            print("Error "+" ") 

    button_delete=Button(frame3,command=delete_column,text="❌")  
    button_delete.grid(column=2,row=0) 

#End Column

def valore_tupla(event):
   event_list=list(event)
   id = event_list[0]
   pubkey=event_list[1] 
   created_at=event_list[2]
   kind=event_list[3]
   tags=json.loads(event_list[4])
   content=event_list[5] 
   sig=event_list[6]
   event_note={"id":id,"pubkey":pubkey,"created_at":created_at,"kind":kind,"tags":tags,"content":content,"sig":sig} 
   return event_note

def valore_json(event):
    event_list=list(event)
    id = event_list[0]
    pubkey=event_list[1] 
    created_at=event_list[2]
    kind=event_list[3]
    tags=json.loads(event_list[4])
    content=event_list[5] 
    sig=event_list[6]
    event_note={"id":id,"pubkey":pubkey,"created_at":created_at,"kind":kind,"tags":tags,"content":content,"sig":sig} 
    json_data = json.dumps(event_note, ensure_ascii=False, indent=4)
    return json_data

def get_note(z):
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f

def tags_string(x,obj):
    f=x["tags"]
    z=[]
    if f!=[]:
     for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

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

async def get_author_event(client):
    if Checkbutton6.get()==1:
        f= Filter().pubkey(user_convert([my_dict[combo_box.get()]])[0]).kinds([Kind(1111),Kind(1)]).limit(300)
    else:
       f= Filter().author(user_convert([my_dict[combo_box.get()]])[0]).kinds([Kind(0),Kind(10002),Kind(3),Kind(30023),Kind(10050),Kind(10012),Kind(1)]).limit(300)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
    z=[]  
    for event in events.to_vec():
        if event.verify()==True:
            z.append(event)
    if z!=[]: 
     return z   
   
async def Get_random_kind():
        
    client = Client(None)
    if relay_list!=[]:
        for jrelay in relay_list:
            await client.add_relay(jrelay)
    else:
        relay_url_1 = RelayUrl.parse("wss://nos.lol/")
        await client.add_relay(relay_url_1)
        relay_url_x = RelayUrl.parse("wss://nostr.mom/")
        await client.add_relay(relay_url_x)
       
    await client.connect()
    await asyncio.sleep(2.0)
   
    test_kind = await get_author_event(client)
    return test_kind   

frame_menu=Frame(root,width=20,height=1)
menu = Menu(frame_menu)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New User", command=open_new_user)
filemenu.add_command(label="Profile", command=open_frame1)
filemenu.add_command(label="Database", command=OpenColumn)
filemenu.add_command(label="Delete", command=frame_del)
filemenu.add_command(label="Settings", command=open_settings)
frame_menu.grid()
relay_list=[]

def add_user(name:str,key:str):
    try: 
        if name!="":  
            if (len(key)==64 or len(key)==63):
                value_key=PublicKey.parse(key)
                if name not in my_dict:
                    my_dict[name]=value_key.to_hex()
                    combo_box["values"]=list(my_dict.keys())
                    frame_user.place_forget()
                    open_frame1()
            else:
                user_name.set("")
                key_string.set("")
                messagebox.showerror("Add User", "key must be npub or hex Pubkey")
        else:        
            messagebox.showerror("Add User", "the name must be at least one character")
            key_string.set("")

    except NostrSdkError as e:
        print(e)            
        frame_user.place_forget()

#search_bar

title_s=StringVar()
entry_title=tk.Entry(root, textvariable=title_s, width=20,font=('Arial',12,'normal'))
entry_title.place(relx=0.6,rely=0.08,relwidth=0.18)

def search_title_c(string:str):
    search_note=[]
    
    if string!="":
        title_string_one = string.replace(", ", " ").replace(",", " ").split()
        title_string = [str(string_).lower() for string_ in title_string_one]

        for string_in in title_string:
            note_list=search_title(string_in)
            if note_list!=[]: 
                for note_x in note_list:
                    if note_x not in search_note:
                        search_note.append(note_x) 
        if search_note:    
            search_str.set("Number of note "+ str(len(search_note)))
        else:
            search_str.set("")    
        title_s.set("")
        search_for_note(search_note)
        close_settings()
        show_noted()
    return search_note 

def search_title(string):
    db_note=kind1_data_name()   
    note_list=[]
    for note_x in db_note[::-1]:
        if note_x["content"]!="":
            title=note_x["content"]
            title_string = title.replace(", ", " ").replace(",", " ").split()
            title_list = [str(title).lower() for title in title_string]
            if string in title_list:
                if note_x not in note_list:
                  note_list.append(note_x)
    return note_list      

hash_list_notes=[]

def search_for_note(note_found:list):
    hash_list_notes.clear()
    if note_found!=[]:
        for note_x in note_found:
            if note_x not in hash_list_notes: 
               hash_list_notes.append(note_x)
    return hash_list_notes                

def search_word_title():
    db_note=kind1_data_name() 
    note_words=[]
    note_words_2=[]
    list_words={}
    for note_x in db_note:
        if note_x["content"]!="":
            title= note_x["content"]
            title_string = title.replace(", ", " ").replace(",", " ").split()
            title_list = [str(title).lower() for title in title_string]
            for string_x in title_list:
               if type(string_x)==str and len(string_x)>3:
               
                if string_x not in note_words:
                  
                    note_words.append(string_x)
                    break
                else:
                    note_words_2.append(string_x)
                    break
    for note_l_word in note_words_2:
        list_words[note_l_word]=note_words_2.count(note_l_word)+1
    
    threeview_dict_l(list_words)  
    return list_words           

def new_dict(list_words:dict):
   value=list(list_words.values())
   value.sort()
   temp_list = []
   for i in value:
    if i not in temp_list:
        temp_list.append(i)
   new_value = temp_list
   new_diz={}
   for value in new_value:
      for list_x in list(list_words.keys()):
         if list_words[list_x]==value:
            new_diz[list_x]=value
   return new_diz

all_words=[]

def threeview_dict_l(list_words):
 if list_words!={} and  list_words!=NONE:
  list_words=new_dict(list_words)
  global all_words
  all_words=list(list_words.keys())   # was [0:100]
  print_people()
  treeview = ttk.Treeview(root, columns=("Value"),height=8)
  scrollbar_view = ttk.Scrollbar(root, orient=VERTICAL,command=treeview.yview)
  treeview.heading("#0", text="key")
  treeview.heading("Value", text="Value")
  db_list=[]
  for key,value in list_words.items():
      if value not in db_list:
       key_value = [key1 for key1, value1 in list_words.items() if value1 == value]

       level1 = treeview.insert("", tk.END, text=f"repeated words {value}")
       db_list.append(value)
       for key_one in key_value:
        treeview.insert(level1, tk.END,text=str(key_one),values=f"{value}")
  scrollbar_view.place(relx=0.88,rely=0.75,relheight=0.2)      
  treeview.place(relx=0.55,rely=0.75,relheight=0.2)   
  
  def close_tree():
     treeview.place_forget()
     scrollbar_view.place_forget()
     button_c2.place_forget()

  button_c2=Button(root,text="Close", command=close_tree,font=('Arial',12,'bold'))
  button_c2.place(relx=0.91,rely=0.82)

search_str=StringVar()
label_button=Label(root,text="..... words",font=('Arial',12,'normal'))
label_button.place(relx=0.62,rely=0.04)
label_search=Label(root,text="", textvariable=search_str,font=('Arial',12,'normal'))
label_search.place(relx=0.7,rely=0.04)
button_s=Button(root,text="Search", command=lambda: search_title_c(entry_title.get()),font=('Arial',12,'normal'))
button_s.place(relx=0.79,rely=0.07)
button_s2=Button(root,text="+", command=search_word_title,font=('Arial',12,'bold'))
button_s2.place(relx=0.85,rely=0.07)

def show_noted():
  """Widget function \n
   Open feed Horizontal
   """
  frame2=tk.Frame(root)  
  if len(hash_list_notes)<=3:
     canvas_1 = tk.Canvas(frame2)
  else:   
    canvas_1 = tk.Canvas(frame2,width=900)
  scrollbar_1 = ttk.Scrollbar(frame2, orient=HORIZONTAL,command=canvas_1.xview)
  scrollable_frame_1 = tk.Frame(canvas_1,background="#E3E0DD")
  scrollbar_2 = ttk.Scrollbar(frame2, orient=VERTICAL,command=canvas_1.yview)
  scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all") ))

  canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
  canvas_1.configure(xscrollcommand=scrollbar_1.set,yscrollcommand=scrollbar_2.set)
  if hash_list_notes!=[]:
   
   s=1
   s1=0
   for note in hash_list_notes:
     
      try:
       context0=""
       if note['tags']!=[]:
        if note["content"]!="": 
         context1=" "+"\n"+note['content']+"\n"
        else:
           context1=""+"\n"
        context2=" "
        
        for xnote in tags_string(note,"alt"):
         context2=context2+"\n"+str(xnote) +"\n"
        
         
        if len(tags_string(note,"t"))==1:
         for xnote in tags_string(note,"t"):
          context2=context2+"Category "+str(xnote) +" "  
        else:
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context2=context2+"#"+str(xnote) +" "
            s=s+1
       else: 
        context1="\n"+note['content']+"\n"
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       
       button_grid2=Button(scrollable_frame_1,text= "Author "+note['pubkey'][0:44], command=lambda val=note["pubkey"]: pubkey_id(val))
       button_grid2.grid(row=0,column=s1,padx=5,pady=5, columnspan=3)   
             
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=3)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=3) 
       
       def print_id(entry):
           print(entry['tags'])
          
       def print_var(entry):
                print(entry["content"])
                if entry["kind"]>=30000:
                 print("ok")
                                                                               
       button=Button(scrollable_frame_1,text=f"Print me", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=4,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Read Tags", command=lambda val=note: print_id(val))
       button_grid2.grid(row=4,column=s1+1,padx=5,pady=5)    
       
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="bottom", fill="x",padx=20)
   scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
   canvas_1.pack( fill="y", expand=True)

   def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   if len(hash_list_notes)<=3:
          button_frame.place(relx=0.4,rely=0.28,relwidth=0.1)   
          frame2.place(relx=0.33,rely=0.32,relwidth=0.32,relheight=0.28)
   else:
            button_frame.place(relx=0.4,rely=0.28,relwidth=0.1)      
            frame2.place(relx=0.33,rely=0.32,relwidth=0.64,relheight=0.28)

def pubkey_id(test):
    note_pubkey=[]
    db_note=kind1_data_name()   
    for note_x in db_note:
        if note_x["pubkey"] == test:
            if note_x not in note_pubkey:
                note_pubkey.append(note_x)
    if len(note_pubkey)>1:       
        search_for_note(note_pubkey)
        close_settings
        show_noted()

test_text=StringVar()
label_button_2=Label(root,textvariable=test_text,font=("Arial",12,"normal"))

def print_people(): 
   if all_words!=[]:  
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=200)
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
    
    test1=all_words
    dict_words={}
    for test_x in test1:
       if str(test_x)[0] in list(dict_words.keys()):
          list_in:list=dict_words[str(test_x)[0]]
          list_in.append(test_x)
          dict_words[str(test_x)[0]]=list_in
       else:
          list_in=[test_x]
          dict_words[str(test_x)[0]]=list_in
            
    ra=0
    sz=0
    test_2=list(dict_words.keys())
    labeL_button=Label(scrollable_frame,text="Number of Letters "+str(len(test_2)))
    labeL_button.grid(row=0,column=1,padx=5,pady=5,columnspan=2)        
    test_2.sort()   
    while ra<len(test_2):
                 sz=sz+1           
                 label_button_grid1=Label(scrollable_frame,text=f"{test_2[ra]} ",font=("Arial",12,"normal"))
                 label_button_grid1.grid(row=s,column=1,padx=5,pady=5)
                 button_grid2=Button(scrollable_frame,text=f"Open", command= lambda val=test_2[ra]: open_letter(val))
                 button_grid2.grid(row=s,column=2,padx=5,pady=5)
                                              
                 root.update()  
              
                 s=s+1
                 ra=ra+1   
    canvas.pack(side="left", fill="y", expand=True)

    def open_letter(key):
 
       ra=0
       
       test_1=dict_words[key]
       test_text2=""
       while ra<len(test_1):
            if ra<5:  
                test_text2=test_text2+ str(test_1[ra]) +"   "
                ra=ra+1        
            else:
               ra=len(test_1)                   
       test_text.set(test_text2)
       label_button_2.place(relx=0.6,rely=0.15)
              
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.325,rely=0.75,relwidth=0.2, relheight=0.2)      

    def Close_print():
       frame3.destroy()  
       test_text.set("")
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

def delete_note(n:int):
        list_event=[]
        number_event=kind1_data_name()  
        for numb_x in number_event:
            if numb_x["kind"]==n:
                list_event.append(numb_x)
        if list_event!=[]:     
            if messagebox.askyesno("Form", f"Do you want delete events kind {n}?" ):      
                for event_x in list_event:
                    delete_events(event_x["id"])
        else:
                kind_note.set("")  
          
def delete_events(id_event):
      try:
       name="historyc2"
       conn = sqlite3.connect(str(name)+'.db')
       try:
         if isinstance(id_event,str):
          id=id_event
         else:
            print(f"Error this is a {type(id_event)}")
                  
         c = conn.cursor()
         c.execute('DELETE FROM events WHERE id = ?', (id,))
         conn.commit()
         messagebox.showinfo("DB delete","Ok")
       except ValueError as e:  
          print(f"Error value while deleting events: {e}")
      except sqlite3.Error  as e:
        print(f"Error while deleting events: {e}")
      finally:
        if conn:
            conn.close()

def delete_l_events(id_event):
    try:
        name="historyc2"
        conn = sqlite3.connect(str(name)+'.db')
        try:
            if isinstance(id_event,list):
                c = conn.cursor()
                for del_id in id_event:
                    c.execute('DELETE FROM events WHERE id = ?', (del_id,))
                conn.commit()      
                messagebox.showinfo("DB delete","Ok")   
            else:
                print(f"Error this is a {type(id_event)}")
        
        except ValueError as e:  
          print(f"Error value while deleting events: {e}")
    except sqlite3.Error  as e:
        print(f"Error while deleting events: {e}")
    finally:
        if conn:
            conn.close()

def delete_events_table(id_event,table_event):
      try:
        name="historyc2"
        conn = sqlite3.connect(str(name)+'.db')
        try:
            if isinstance(id_event,str):
                id=id_event
            else:
                print(f"Error this is a {type(id_event)}")
            c = conn.cursor()
            c.execute(f'DELETE FROM {table_event} WHERE id = ?', (id,))
            conn.commit()
            messagebox.showinfo("DB delete","Ok")
        except ValueError as e:  
          print(f"Error value while deleting events: {e}")

      except sqlite3.Error  as e:
        print(f"Error while deleting events: {e}")
      finally:
        if conn:
            conn.close()


def delete_time(event_):
      event_time=since_day_time(event_)
      try:
        name="historyc2"
        conn = sqlite3.connect(str(name)+'.db')
        try:
           c = conn.cursor()
           c.execute('DELETE FROM events WHERE created_at < ?', (event_time,))
           conn.commit()
           messagebox.showinfo("DB delete","Ok")
        except ValueError as e:  
          print(f"Error value while deleting events: {e}")
      except sqlite3.Error  as e:
        print(f"Error while deleting events: {e}")
      finally:
        if conn:
            conn.close()

root.mainloop()