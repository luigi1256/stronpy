#threads write
import tkinter as tk
from tkinter import *
from tkinter import ttk
import asyncio
from nostr_sdk import *
from datetime import timedelta
from tkinter import messagebox
from cryptography.fernet import Fernet

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

root.mainloop()                                       