#threads write
import tkinter as tk
from tkinter import *
from tkinter import ttk
import asyncio
from nostr_sdk import *
from datetime import timedelta
from tkinter import messagebox
from cryptography.fernet import Fernet
import time
import json

root = Tk()
root.title("Test Threads")
root.geometry("1250x800")

#threads

threads_frame = ttk.LabelFrame(root, text="Threads Post", labelanchor="n", padding=10)
note_tag_t = tk.Label(root, text="Note",font=('Arial',12,'normal'))
scroll_bar_mini = tk.Scrollbar(root)
entry_t_4=tk.Text(root, font=('Arial',12,'normal'),yscrollcommand = scroll_bar_mini.set)
tag_1=StringVar()
tag_note_1=ttk.Entry(root,justify='left', font=('Arial',12,'normal'),textvariable=tag_1,width=10)
hash_tag = tk.Label(root, text="Hahstag",font=('Arial',12,'bold'))
hash_tag_list=[]
button_topic=tk.Button(root, text="Add Topic")

def open_threads():
         
    threads_frame.place(relx=0.17,rely=0.1,relwidth=0.32,relheight=0.33,anchor='n' )
    note_title.place(relx=0.1,rely=0.15)
    label_title.place(relx=0.05,rely=0.15)  
    note_tag_t.place(relx=0.15,rely=0.26,relwidth=0.1,anchor='n' )
    entry_t_4.place(relx=0.17,rely=0.3,relwidth=0.25,relheight=0.1,anchor='n' )
    scroll_bar_mini.place(relx=0.31,rely=0.3,relheight=0.1,anchor='n' )
    tag_note_1.place(relx=0.1,rely=0.2)
    hash_tag.place(relx=0.04,rely=0.2)
    scroll_bar_mini.config( command = entry_t_4.yview )

    def add_hashtag():
       if tag_note_1.get()!="":
          if len(hash_tag_list)<2: #0 #1
            if tag_note_1.get() not in hash_tag_list:
                hash_tag_list.append(tag_note_1.get())
                print(hash_tag_list)
          tag_1.set("")
          
    button_topic['command']=add_hashtag
    button_topic.place(relx=0.21,rely=0.2,relwidth=0.05,relheight=0.03,anchor='n')

    def Preview():
     if entry_t_4.get('1.0', 'end-1c')!="": 
        frame1=Frame(root, width=310, height=100)
   
        canvas_1 = Canvas(frame1)
        canvas_1.pack(side="left", fill=BOTH, expand=True)

        canvas_1.bind(
    "<Configure>",
    lambda e: canvas_1.configure(scrollregion=canvas_1.bbox("all")))
        
        scrollable_frame_2 = Frame(canvas_1)
        canvas_1.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
    
        def create_note(note_text, s):
           if len(note_text)<241:
            str_title=str("Title "+note_title.get()+"\n")
            text_h=str("")
            if hash_tag_list!=[]:
               for hash_x in hash_tag_list:
                  if hash_tag_list.index(hash_x)==0:
                    text_h=text_h + str("Topic "+hash_x+ " ")
                  else:
                     text_h=text_h + str("\n"+ "SubTopic "+hash_x+ " ")
                    

               text_h=text_h +"\n"+"\n"   
                
            message = Message(scrollable_frame_2,text=str_title+text_h+note_text, width=240, font=('Arial',12,'normal'))
            message.grid(row=s, column=0, columnspan=3, padx=5, pady=10)
            Button(scrollable_frame_2, text="Print Note", command=lambda: share(note_text)).grid(row=0, column=2, padx=5, pady=5)
           else:
            message = Message(scrollable_frame_2, text=str_title+text_h+note_text[0:240]+"...",  width=240, font=('Arial',12,'normal'))
            message.grid(row=s, column=0, columnspan=3, padx=5, pady=10)
            Button(scrollable_frame_2, text="Print Note", command=lambda: share(note_text)).grid(row=0, column=2, padx=5, pady=5)
       
        s = 1
        
        while s<2:
         if entry_t_4.get('1.0', 'end-1c')!="":
            create_note(entry_t_4.get('1.0', 'end-1c'), s)
         s += 2   

        frame1.place(relx=0.05,rely=0.5, relheight=0.3,relwidth=0.28)  
        
        def close_canvas():
            scrollable_frame_2.place_forget()
            canvas_1.destroy()
            frame1.destroy()
            
        button_close=Button(scrollable_frame_2, command=close_canvas, text="Close X")
        button_close.grid(row=0, column=1, padx=5, pady=10)
        
    button_pre_t["command"]= Preview
    button_pre_t.place(relx=0.1,rely=0.45,relwidth=0.1, anchor="n") 
    button_reply_t.place(relx=0.2,rely=0.45,relwidth=0.1,relheight=0.05,anchor='n' )
    close_t["command"] = close_question
    close_t.place(relx=0.28,rely=0.15,relwidth=0.05,relheight=0.03,anchor='n' )
        
button_create=Button(root,text="Create Thread", command=open_threads)
button_create.place(relx=0.1,rely=0.05)

def share(note_text):
    print(f"Note: \n {note_text}")    

def round1_note():  #have the root
  if entry_t_4.get('1.0', 'end-1c')!="":
     #if __name__ == '__main__':
     tag=tag_thread()
    
     note=entry_t_4.get('1.0', 'end-1c')
     
     asyncio.run(start_thread(note,tag))
     close_question()

def tag_thread():
   tag_list_add=[]
   if note_title.get()!="":
    if hash_tag_list!=[]:
       tag_list_add.append(Tag.custom(TagKind.TITLE(), [note_title.get()]))
       for jlist in hash_tag_list:
        tag_list_add.append(Tag.hashtag(jlist))
    else:
       tag_list_add.append(Tag.custom(TagKind.TITLE(), [note_title.get()]))
   return tag_list_add         

close_t=Button(root,text="Close X",highlightcolor='WHITE',width=10,
              font=('Arial',12,'normal'))
note_title=ttk.Entry(root,justify='center', font=('Arial',12,'normal'))
button_pre_t=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))
label_title=tk.Label(root, text="Title ",font=('Arial',12,'bold'))
button_reply_t=tk.Button(root,text="Send Note", background="darkgrey", 
                         command=round1_note, font=('Arial',12,'normal'))

relay_list=[]

def close_question():
    threads_frame.place_forget()
    note_title.place_forget()
    note_title.delete(0, END)
    label_title.place_forget()
    note_tag_t.place_forget()
    entry_t_4.place_forget()
    scroll_bar_mini.place_forget()
    button_pre_t.place_forget()
    close_t.place_forget()
    button_reply_t.place_forget()
    entry_t_4.delete("1.0", "end") 
    hash_tag.place_forget()
    tag_1.set("")
    tag_note_1.place_forget()
    button_topic.place_forget()
    
async def start_thread(start_point,tag):
   init_logger(LogLevel.INFO)
    
   key_string=log_these_key()
   if key_string!=None: 
     keys = Keys.parse(key_string)
     signer = NostrSigner.keys(keys)
     client = Client(signer)
     list_p=[PublicKey.parse(keys.public_key().to_hex())]
     Get_outbox_relay(10002,list_p)
     if outbox_list!=[]:
        for jrelay in outbox_list:
          await client.add_relay(RelayUrl.parse(jrelay))
     else:
      await client.add_relay(RelayUrl.parse("wss://nostr.mom"))
      await client.add_relay(RelayUrl.parse("wss://nos.lol"))
     await client.connect()
     builder =  EventBuilder(Kind(11),start_point).tags(tag).pow(int(21))
     test= await client.send_event_builder(builder)
     print("Event sent:","\n",test.success,"\n",test.id)               
                                       
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

outbox_list=[]
public_list=[]

def get_note(z):
    f=[]
    import json
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

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z 

def Relay_write(x):
     """Write Relays"""
     i=0
     c=[]
     relays=tags_str(x,'r')
     j=len(relays)
     while i<j:
         if len(relays[i])>2:
             if relays[i][2]=="write":
              c.append(relays[i][1])
         else:
             c.append(relays[i][1])
         i=i+1
         
     return c

def Get_outbox_relay(key:int,public_p:list):
     """Key = kind number \n
        10002 = nostr relay 
        public_p = first Publickey
     """
     test=[]
     test_kinds = [Kind(key)]
     if isinstance(public_p,list):
        public_list.append(public_p[0])
     else:
        print("error") 
     if __name__ == "__main__":   
      
      test = asyncio.run(Get_event_from(test_kinds))
      if test is not None:
       relay_user=get_note(test)
       if relay_user!=[]:
           outbox_list.clear()
           public_list.clear()
           i=0
           
           while i<len(relay_user):
            if i<2:
             if relay_user[i]["kind"]==10002:
              x_relay=Relay_write(relay_user[i])
              for xrelay in x_relay:
               if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay[6:9]!="127":
               
                if xrelay not in outbox_list:
                 outbox_list.append(xrelay)
            i=i+1     

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)

    # Add relays and connect
    relay_url_1=RelayUrl.parse("wss://nostr.mom/")
    relay_url_2=RelayUrl.parse("wss://relay.damus.io/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    
    if relay_list!=[]:
        for xrelay in relay_list:
            relay_url_list=RelayUrl.parse(xrelay)
            await client.add_relay(relay_url_list)
    await client.connect()
    await asyncio.sleep(2.0)
     
    if isinstance(event_, list):
        test_kind = await get_kind(client, event_)
        if test_kind:
           return test_kind    
    else:
        print("error")

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

#Topic

my_dict = {"Sebastix": "06639a386c9c1014217622ccbcf40908c4f1a0c33e23f8d6d68f4abf655f8f71", 
           "Cody": "8125b911ed0e94dbe3008a0be48cfe5cd0c0b05923cfff917ae7e87da8400883",
             "Dawn": "c230edd34ca5c8318bf4592ac056cde37519d395c0904c37ea1c650b8ad4a712", 
             "Silberengel": "fd208ee8c8f283780a9552896e4823cc9dc6bfd442063889577106940fd927c1", 
             "il_lost_": "592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"}

my_list = list(my_dict.values())
my_name = list(my_dict.keys())

def on_select(event):
    selected_item = combo_box.get()
    entry_id_note.set(my_dict[selected_item])
    label_entry_id["text"]=my_dict[selected_item][0:9]
    relay_list.clear()
    search_relay()

def on_relay(event):
   db_list.clear()
   print(combo_relay.get())

db_list=[]
list_event=[Kind(11)]
db_note=[]
frame1=tk.Frame(root)    
Profile_frame = ttk.LabelFrame(root, text="Thread", labelanchor="n", padding=10)
Profile_frame.place(relx=0.36,rely=0.03,relwidth=0.2,relheight=0.27)
label = tk.Label(root, text="Name",font=('Arial',12,'normal'))
label.place(relx=0.38,rely=0.11)
combo_box = ttk.Combobox(root, values=["Sebastix","Cody","Dawn","Silberengel","il_lost_"],font=('Arial',12,'normal'),width=15)
combo_box.place(relx=0.42,rely=0.11)
combo_box.set("Some Users")
combo_box.bind("<<ComboboxSelected>>", on_select)

combo_relay = ttk.Combobox(root, values=[],font=('Arial',14,'normal'),width=18)
combo_relay.place(relx=0.37,rely=0.19)
combo_relay.set("wss://....")
combo_relay.bind("<<ComboboxSelected>>", on_relay)
entry_id_note=StringVar()
entry_note_note=StringVar()
label_entry_id=tk.Label(root, text="Pubkey",font=("Arial",12,"normal"))
label_entry_id.place(relx=0.43,rely=0.06)
label_rel_id=tk.Label(root, text="Relay",font=("Arial",12,"normal"))
label_rel_id.place(relx=0.43,rely=0.15)
value=float(720*3600/86400)

def search_relay():
   if __name__ == "__main__":
    asyncio.run(outboxes())

async def get_outbox(client):

  if my_list!=[]:
   if my_dict[combo_box.get()] in list(my_dict.values()): 
    print("ok")
    f = Filter().authors(user_convert([my_dict[combo_box.get()]])).kinds([Kind(10002),Kind(10012),Kind(1),Kind(0)])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

relay_list_extra=[]

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

async def outboxes():
    init_logger(LogLevel.INFO)
    client = Client(None)
    
    if relay_list!=[]:
       
       for jrelay in relay_list:
          relay_url_list=RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
             
    else:
        relay_url_1=RelayUrl.parse("wss://nostr.mom/")
        relay_url_2=RelayUrl.parse("wss://purplerelay.com/")
        await client.add_relay(relay_url_1)
        await client.add_relay(relay_url_2)
     
    await client.connect()
    db_note.clear()
    note_result= await get_outbox(client)
    if note_result!=None:
     relay_add=get_note(note_result)
     if relay_add!=[]:
           i=0
           
           while i<len(relay_add):
            if relay_add[i]["kind"]==10002:
             for xrelay in tags_string(relay_add[i],'r'):
              if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay[6:9]!="127":
               
               if xrelay not in relay_list:
                 relay_list.append(xrelay)
            if relay_add[i]["kind"]==10012:
               for xrelay in tags_string(relay_add[i],'relay'):
                if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay[6:9]!="127":
                    if xrelay not in relay_list_extra:
                        relay_list_extra.append(xrelay)
               combo_relay['values']=relay_list_extra            
               
            else:
                db_note.append(relay_add[i])      
            i=i+1             
    await asyncio.sleep(2.0)

def test_relay(): 
 if combo_relay.get()!="wss://....":
   tm=note_list_r()
   print(len(tm))
   return tm
  
def note_list_r():
    L=[]
    if __name__ == "__main__":
     
     combined_results = asyncio.run(main_feed())
    L=get_note(combined_results)
    return L

label_relay=ttk.Label(root,text="Relay List", font=('Arial',12,'bold'))
label_relay.place(relx=0.37,rely=0.32)     

def search_():
   result=test_relay()
   if result !=None:
    note=label_relay['text']
    list_note= str(note).split()
    if combo_relay.get() not in list_note:
         if len(list_note)<5:
            zeta= len(list_note)
            note=note+ "\n"+"n° "+str(zeta-1)+" "+ combo_relay.get()
            label_relay.config(text=str(note))
    timeline_created(db_list,result)
    for db_x in db_list:
       if tags_string(db_x,"t")!=[]:
          for tags_t in tags_string(db_x,"t"):
             if tags_t not in combo_t_tag:
              combo_t_tag.append(tags_t) 
    if combo_t_tag!=[]:   
     list_value_tag()
     combo_tag.set("Number of topic "+ str(len(combo_t_tag)))      
     combo_t_tag.sort()    
     combo_tag['values']=combo_t_tag

def list_value_tag():
    for topic in combo_t_tag:
       topic_list=[]
       pubkey_topic=[]
       for note_x in db_list:
         if float(int(time.time())-note_x["created_at"])/(86400)<value:
            if topic in tags_string(note_x,"t"):
               if note_x not in topic_list:
                  topic_list.append(note_x)
                  if note_x["pubkey"] not in pubkey_topic:
                     pubkey_topic.append(note_x["pubkey"])    

def timeline_created(db_list,list_new):
  new_note=[] 
  if db_list!=[]:
   for new_x in list_new:
     if new_x not in db_list:
        new_note.append(new_x) 
   i=0
    
   while i<len(new_note):
     j=0
     while j< len(db_list): 
      if db_list[j]["created_at"]>(new_note[i]["created_at"]):
         j=j+1
      else:
         db_list.insert(j,new_note[i])
         break
     i=i+1
   return db_list   
  else:
        for list_x in list_new:
            db_list.append(list_x)
        return db_list 
    

async def get_note_relays(client):
    f = Filter().kinds(list_event).limit(500)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def main_feed():
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    
    if relay_list_extra!=[]:
       
       if combo_relay.get() in relay_list_extra:
            relay_url = RelayUrl.parse(combo_relay.get())
            await client.add_relay(relay_url)

    await client.connect()
    await asyncio.sleep(1.0)
    combined_results = await get_note_relays(client)
    return combined_results

button_tm=tk.Button(root,command= search_,text="Search note", font=("Arial",12,"normal"))
button_tm.place(relx=0.43,rely=0.24)

Checkbutton_e = IntVar()
combo_t_tag=[]
Checkbutton_e.set(0)
note_topic = tk.Label(root, text="",font=('Arial',14,'normal'))

def Restore(event):
    Checkbutton_e.set(0)   
    if combo_t_tag!=[]:
      note_topic.place_forget()          
      combo_tag.set("Number of topic "+ str(len(combo_t_tag)))
      combo_t_tag.sort()
      combo_tag['values']=combo_t_tag

def Search_select(event):
   if Checkbutton_e.get()==0:
    Checkbutton_e.set(1)   
   topic=type_topic()
   if topic!=[] and topic!=None:
       show_print_test() 
   else:
      pass
      
def note_time(note):
    value=int((float(int(time.time())-note["created_at"])/(60)))
    if value>60:
        if value>1440:
            if value>2880:
              return str(int((float(int(time.time())-note["created_at"])/(86400))))+str(" days ago") 
            else:
               return str(int((float(int(time.time())-note["created_at"])/(86400))))+str(" day ago") 
        else:
            if value>120:   
              return str(int((float(int(time.time())-note["created_at"])/(3600))))+str(" hours ago") 
            else:
               return str(int((float(int(time.time())-note["created_at"])/(3600))))+str(" hour ago") 
    else:
        if value>2:
           return str(int((float(int(time.time())-note["created_at"])/(60))))+str(" minutes ago")    
        else:
           return str(int((float(int(time.time())-note["created_at"])/(60))))+str(" minute ago")     

def type_topic():
   
   if combo_tag.get()!="Tag List" and combo_tag.get().startswith("Number")==False:
      
      topic_list=[]
      topic=combo_tag.get()
      for note_x in db_list:
         if float(int(time.time())-note_x["created_at"])/(86400)<value:
          if topic in tags_string(note_x,"t"):
             if note_x not in topic_list:
                topic_list.append(note_x)
      return topic_list          
                       

combo_tag = ttk.Combobox(root, values=combo_t_tag,font=('Arial',12,'normal'),width=15)
combo_tag.place(relx=0.6,rely=0.05,relheight=0.045)
combo_tag.set("Tag List")
combo_tag.bind("<<ComboboxSelected>>", Search_select)
combo_tag.bind('<Button-3>', Restore) 
Pubkey_Metadata={}

def show_print_test():
 frame3=tk.Frame(root,height=150)  
 canvas_2 = tk.Canvas(frame3,width=410)
 scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
 scrollable_frame_2 = ttk.Frame(canvas_2,width=380)

 scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")))
 canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
 canvas_2.configure(yscrollcommand=scrollbar_2.set)

 def val_topic_two(topic):
    if topic in combo_t_tag:
     combo_tag.set(topic)
    if Checkbutton_e.get()==0:
      Checkbutton_e.set(1)   
    topic=type_topic()
    if isinstance(topic,str):
      pass
    else:
      frame3.destroy()
      show_print_test() 
    
                     
 s=1
 if db_list!=[]:
  for note in db_list:
   
   if float(int(time.time())-note["created_at"])/(86400)<value:  
     if note["kind"]==6:       
         context0= "RT "+" By "+note["pubkey"][0:9]
     else: 
      if note["pubkey"] in list(Pubkey_Metadata.keys()):
        context0="Nickname " +str(Pubkey_Metadata[note["pubkey"]])
      else: 
         context0="Pubkey: "+note['pubkey'][0:9]
   
     str_time=note_time(note)
     context0=context0+"\n"+"Time: "+str(str_time)
      
     if note["kind"]==6:
           try: 
            context1= str(json.loads(note["content"])["content"]+"\n")
            context2= str(json.loads(note["content"])["tags"])
           except json.decoder as e:
              print(e)
     else:
           if Checkbutton_e.get()==1: 
            if combo_tag.get() in tags_string(note,"t") and tags_string(note,"t")!=[]: 
              context1=note['content']+"\n"
              tag_note=""
              for note_x in note["tags"]:
               tag_note=tag_note+ str(note_x)+"\n"
              context2="[[ Tags ]]"+"\n" +tag_note

            else:
              context0=""
              context1=""
              context2=""


           else:
              context1=note['content']+"\n"
              tag_note=""
              for note_x in note["tags"]:
                tag_note=tag_note+ str(note_x)+"\n"
              context2="[[ Tags ]]"+"\n" +tag_note
   else:
      break        
              
   
   
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=180,font=("Arial",12,"normal"),foreground="grey")
   if context0!="":
    var_id.set(context0)
    label_id.grid(pady=2,column= 2, columnspan=2,row=s,padx=2)
    if tags_string(note,"t")!=[]:
      if len(tags_string(note,"t"))==2:
        if combo_tag.get() in tags_string(note,"t"):
          if tags_string(note,"t").index(combo_tag.get())==0: 
            button_6 = tk.Button(scrollable_frame_2, text="Subtopic \n"+ str(tags_string(note,"t")[1][0:20]), command=lambda val=tags_string(note,"t")[1]: val_topic_two(val),font=("Arial",12,"bold"),fg="blue")
            button_6.grid(column=0,row=s,padx=1,pady=5)
            context1=""
            context2=""
          else:
            button_6=Button(scrollable_frame_2,text="Topic \n"+ str(tags_string(note,"t")[0]), command=lambda val=note: Tag_topic(val),font=("Arial",12,"bold"),fg="green")   
            button_6.grid(column=0,row=s,padx=1,pady=5)
        else:
           button_6=Button(scrollable_frame_2,text="Topic \n"+ str(tags_string(note,"t")[0]), command=lambda val=note: Tag_topic(val),font=("Arial",12,"bold"),fg="green") 
           button_6.grid(column=0,row=s,padx=1,pady=5)
        
        
                    
      else:
         button_6=Button(scrollable_frame_2,text=str(tags_string(note,"t")[0]), command=lambda val=note: Tag_topic(val),font=("Arial",12,"bold"))
         button_6.grid(column=0,row=s,padx=1,pady=5)
    if context1!="":     
     scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
     scroll_bar_mini.grid( sticky=NS,column=4,row=s+1,pady=5)
     second_label10 = tk.Text(scrollable_frame_2, padx=2, height=5, width=32, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
     second_label10.insert(END,context1+"\n"+str(context2))
     scroll_bar_mini.config( command = second_label10.yview )
     second_label10.grid(padx=2, column=0, columnspan=4, row=s+1) 
      
   def print_note(entry):
           print(entry)

   def create_topic(entry):
            open_threads()
            if len(tags_string(entry,"t"))==1:
             hash_tag_list.clear()
             tag_1.set(str(tags_string(entry,"t")[0]))
            if len(tags_string(entry,"t"))==2:
             hash_tag_list.clear()
             tag_1.set(str(tags_string(entry,"t")[1]))
            #Messagebox  
            

   def Tag_topic(entry):
      if tags_string(entry,"t")!=[]:
         combo_tag.set(tags_string(entry,"t")[0])
         if Checkbutton_e.get()==0:
            Checkbutton_e.set(1)   
         topic=type_topic()
         if isinstance(topic,str):
            pass
         else:
            frame3.destroy()
            show_print_test() 
         
   if context0!="" and context1!="":      
    button_grid2=Button(scrollable_frame_2,text="Stamp", command=lambda val=note: print_note(val),background="#b0aba6")
    button_grid2.grid(row=s+2,column=0,padx=5,pady=5)
    if tags_string(note,"t")!=[]:
        button_grid2=Button(scrollable_frame_2,text="Create topic", command=lambda val=note: create_topic(val),background="#b0aba6")
        button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
                       
   s=s+3
   def close_frame():
     frame3.destroy()
     note_topic.config(text="")      

   button_frame=Button(scrollable_frame_2,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.grid(row=0,column=0,padx=5,pady=5)
 frame3.place(relx=0.57,rely=0.12,relwidth=0.38,relheight=0.4) 
 scrollbar_2.pack(side="right", fill="y",pady=20) 
 canvas_2.pack( fill="y", expand=True) 
 root.update_idletasks() 

button_id=tk.Button(root,command=show_print_test,text="Feed", background="grey",font=("Arial",12,"bold"))
button_id.place(relx=0.73,rely=0.05)

root.mainloop()                                       