import asyncio
from datetime import timedelta
from nostr_sdk import Keys, Client, NostrSigner
from nostr_sdk import PublicKey,ZapRequestData,Metadata,SecretKey
from nostr_sdk import Tag, init_logger, LogLevel,ClientBuilder,SingleLetterTag,TagStandard
from nostr_sdk import EventId,EventBuilder, Filter, Metadata,Kind,NostrConnectUri,NostrConnect, NostrSdkError,uniffi_set_event_loop
import json
import requests
import time
from asyncio import get_event_loop
from nostr_sdk import Kind,Nip19Event,Nip19Enum,SubscribeOutput,SubscribeOptions,FilterRecord,Alphabet,Nip21,Coordinate
from nostr_sdk import TagKind
import requests
import shutil
from PIL import Image, ImageTk

def init_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    get_event_loop()
    return loop

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk 

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f

def search_kind(user,x):
    if __name__ == "__main__":
     # Example usage with a single key
     single_author = user 
     single_results = asyncio.run(feed(single_author))
    Z=[]
    note=get_note(single_results)
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z   

def convert_note(note):
 if len(note)==64:
    return note
   
 else:
    if len(note)==63:
      test=EventId.parse(note)
      note_ex=test.to_hex()
      return note_ex

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def npub_class():
   if len(npub_entry.get())==63:
      Npub=PublicKey.parse(npub_entry.get())
      return Npub
   if len(npub_entry.get())==64:
      Npub=PublicKey.parse(npub_entry.get())
      return Npub   

def tags_string(x,obj):
    f=x["tags"]
    z=[]
    if f!=[]:
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

def search_three(notes,x):
    note=get_note(notes)
    Z=[]
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z

def scope_Coracle(type_feed,npub):
   try:  
    scope_type=["network","follow", "follower","follow_follow"]
    with open("social_graph_ju.json", "r") as f:   #social_graph
     t=f.readline()
     testo=json.loads(t)
     rank=testo['followLists']
     people=testo['uniqueIds']
     test_=[]
   
     for zpeople in people:
        if zpeople[0]==npub:
           number=zpeople[1]
     for j in rank:
      if j[0]==number:
        for x in j[1]:
            for z in rank:
                if x==z[0]:
                    test_.append(z[1])
     if type_feed in scope_type:
        if type_feed=="follow_follow":
          follow_follow=[]
          for jtest in test_:
                for xtest in jtest:
                    if xtest not in follow_follow:
                        follow_follow.append(xtest)  
          print(len(follow_follow))                  
          return follow_follow
                
        if type_feed=="follow":
            
            follow_=[]
            for j in rank:
              if j[0]==number:
                for x in j[1]:   
                  for jpeople in people:
                    if jpeople[1]==x:
                      follow_.append(jpeople[0]) 
            print(len(follow_),follow_[0])
            return follow_
            
        if type_feed=="follower":
            follower=[]
            for j in rank:
              for x in j[1]:   
                if x==number:
                 for jpeople in people:
                    if jpeople[1]==j[0]:
                     follower.append(jpeople[0])
            print(len(follower),follower[0])    
            return follower     
        if type_feed=="network":    
           network=[]
           for j in rank:
              if j[0]==number:
                for x in j[1]:  
                    for jpeople in people:
                     if jpeople[1]==x:
                       network.append(jpeople[0])  
                  
           for j in rank:
              for x in j[1]:   
                if x==number:
                 for jpeople in people:
                    if jpeople[1]==j[0]:
                     if jpeople[0] not in network:
                       network.append(jpeople[0])
           print(len(network))       
           return network            
   except UnboundLocalError as e:
       print(e)   
            
#Get_tag_id not use
#custom feed search

async def get_one_nostr_tags(client, event_kind,event_identifier,event_publickey):
    f =Filter().kind(event_kind).author(event_publickey).identifier(event_identifier)
    print(f.as_json())    
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_list_(client, event_publikey):
     d_identifiers=[]
     for xevent_ in event_publikey:
        d_identifiers.append(xevent_[71:])
     print(d_identifiers)   
     f = Filter().kind(Kind(30000)).identifiers(d_identifiers)
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec()]
     return z


async def get_nostr_tags(client, event_kind,hashtag,list_pubkey):
    if event_kind!=None: 
       f = Filter().kinds([Kind(int(event)) for event in event_kind]).limit(200)  
       if hashtag!=None:
             f = Filter().kinds([Kind(int(event)) for event in event_kind]).hashtags(hashtag).limit(200)
             if list_pubkey:
              f = Filter().kinds([Kind(int(event)) for event in event_kind]).hashtags(hashtag).authors(user_convert(list_pubkey)).limit(200)      
       else:
          if list_pubkey:
              f = Filter().kinds([Kind(int(event)) for event in event_kind]).authors(user_convert(list_pubkey)).limit(200)    
    else:
           if hashtag!=None:
             f = Filter().hashtags(hashtag).limit(200)  
             if list_pubkey:
               f = Filter().hashtags(hashtag).authors(user_convert(list_pubkey)).limit(200)
           else:
              if list_pubkey:
               f = Filter().authors(user_convert(list_pubkey)).limit(200)    
              else:
                 f = Filter().limit(200)
       
    #print(f)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Nostr_coord_feed(tag_nostr_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    event_kind=None
    event_hash=None
    event_publikey=None
    client = Client(None)
    for jrelay in tag_nostr_:
     if jrelay[0]=="relay":
        event_relay=jrelay[1:]
       
    # Add relays and connect
        if event_relay:
          for xrelay in event_relay:
           try: 
     
                await client.add_relay(xrelay)
      
           except:
                print("error",xrelay)
    await client.add_relay("wss://relay.primal.net")
    await client.connect()

    await asyncio.sleep(2.0)
    
    #await client.connect()
    for jkind in tag_nostr_:
     if jkind[0]=="kind":
        event_kind=jkind[1:]

    for jhash in tag_nostr_:
     if jhash[0]=="tag":
        event_hash=jhash[2:]    

    for jpub in tag_nostr_:
     if jpub[0]=="list":  #incorrect  #addresses
        event_publikey=jpub[1]["addresses"]      
    list_pubkey=[]
    if event_publikey:
     list_note= await get_list_(client, event_publikey)
     for event_list in get_note(list_note):
       for xperson in tags_string(event_list,'p'):
        list_pubkey.append(xperson)
    else:
       for jpub in tag_nostr_:
         if jpub[0]=="scope":
          i=1
          if npub_class():
           while i<len(jpub): 
            list_npub=scope_Coracle(jpub[i],npub_class().to_hex())
            if list_npub:
              for list_x in list_npub:
                 if list_x not in list_pubkey:
                   list_pubkey.append(list_x)
            i=i+1        
    await asyncio.sleep(2.0)

    if isinstance(tag_nostr_, list):
         print("list0")
         
         test_id = await  get_nostr_tags(client,event_kind,event_hash,list_pubkey)
    else:
        print("str0")
    return test_id

def search_Nostr_id():
   if len(search_nota_id.get())==64: 
    if entry_text.get(1.0, "end-1c")!="":
      button_search_id.config(text="Update Feed",foreground="green") 
      entry_text.delete("1.0","end")
    if entry4.get(1.0, "end-1c")!="":
       entry4.delete("1.0","end") 

    test_ids1 = search_nota_id.get()
    test_id1 = asyncio.run(Get_id(test_ids1))
    test_note1=get_note(test_id1)
    db_note_list.clear()
    filter_note=[]
    for note1 in test_note1:  #reverse
         entry4.insert(END,"note: "+note1["content"] +"\n")
         entry4.insert(END,"time: "+str(note1["created_at"])+"\n")
         xnote1 = tags_string(note1,"feed")
             
         for xnote in json.loads(xnote1[0]):
                  filter_note.append(xnote)
         for note_tag in note1["tags"]:
            entry4.insert(END,str(note_tag)+"\n")
         entry4.insert(END,"-----------"+"\n")
         button_search_id.config(text="Update Selection",foreground="green") 

    def second_cor_filter():
     second_filter=asyncio.run(Nostr_coord_feed(filter_note))
     event_print=get_note(second_filter)
     timeline_created(event_print)
     show_noted()           

    button_open=Button(root,command=second_cor_filter, text="Read Note", font=('Arial',12,'normal'))
    button_open.place(relx=0.2,rely=0.3,anchor='n' )       

db_note_list=[]

def timeline_created(list_new):
  new_note=[] 
  global db_note_list
  if db_note_list!=[]:
   for new_x in list_new:
     if new_x not in db_note_list:
        new_note.append(new_x) 
   i=0
    
   while i<len(new_note):
     j=0
     while j< len(db_note_list): 
      if db_note_list[j]["created_at"]>(new_note[i]["created_at"]):
         j=j+1
      else:
         db_note_list.insert(j,new_note[i])
         break
     i=i+1
   return db_note_list   
  else:
        for list_x in list_new:
            db_note_list.append(list_x)
        return db_note_list  
  
#UI 

import tkinter as tk
from tkinter import *
from tkinter import ttk
root = tk.Tk()
root.geometry('1200x800') 

colour1=''
colour2='grey'
colour3='#65e7ff'
colour4='BLACK'

#entry_layout_left

frame1=tk.Frame(root,height=100,width=200,background="lightgrey")
note_tag = tk.Label(frame1, text="Note")
note_tag.grid(column=12, row=0,padx=10,pady=5,ipadx=1,ipady=1)
scroll_bar_4 = tk.Scrollbar(frame1, background="darkgrey")
entry4=tk.Text(frame1,font=('Arial',12,'bold'),width=40, height=5,yscrollcommand = scroll_bar_4.set)
entry4.grid(column=12, row=1,rowspan=2, padx=10,pady=5, ipadx=2,ipady=2)
scroll_bar_4.config( command = entry4.yview )
scroll_bar_4.grid(column=13, row=1,rowspan=2, padx=10,pady=5, ipadx=2,ipady=25)
stringa_id=tk.StringVar()
search_nota_id = tk.Entry(frame1, textvariable=stringa_id, width=30)
search_nota_id.grid(column=14, row=2,columnspan=1,padx=5,ipadx=1,ipady=1) 
button_search_id=tk.Button(frame1,text="Search a Feed", command=search_Nostr_id)
button_search_id.grid(column=14, row=3,ipadx=1,ipady=1,pady=2) 

async def get_one_Event(client, event_):
    f = Filter().id(EventId.parse(event_))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    await client.add_relay("wss://relay.damus.io/")
    await client.add_relay("wss://nos.lol/")
    await client.connect()
   
    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        print("errore")
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

def evnt_id(id):
     test2=EventId.parse(id)
     return test2

scroll_bar_text = tk.Scrollbar(root, background="darkgrey")
entry_text=tk.Text(root, background="grey", yscrollcommand = scroll_bar_text.set, font=('Arial',14,'bold'))
scroll_bar_text.config( command = entry_text.yview )
string_kind=IntVar()        
user_kind=Entry(root,textvariable=string_kind)         
#user_kind.place(relx=0.1,rely=0.7,relwidth=0.1,relheight=0.05  )     
  
async def get_relays(client, authors):
    f = Filter().authors(authors)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_relay(client, user):
    f = Filter().author(user).kinds([Kind(int(user_kind.get())),Kind(10014),Kind(31890)])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def feed(authors):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    
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

def timeline_feed():
      if npub_class(): 
       entry_text.place(relx=0.45,rely=0.3,relwidth=0.4,relheight=0.6,anchor='n' )
       scroll_bar_text.place(relx=0.67,rely=0.3,relheight=0.6,anchor='n' )
       kind_1=search_three(asyncio.run(feed(npub_class())),31890)
       if entry_text.get(1.0, "end-1c")!="": 
        entry_text.delete("1.0","end")
      
       if kind_1!=None:
         for j in kind_1:
          if tags_string(j,"e")==[]:
           entry_text.insert(END,"id: "+j["id"]+"\n"+"pubkey: "+j['pubkey']+"\n"+j['content']+"\n")
           for prime in j["tags"]:
             if prime[0]=="title":
                entry_text.insert(END,str(prime)+"\n"+"______________"+"\n"+"\n")
             if prime[0]=="feed":
              entry_text.insert(END,str(prime)+"\n")
            
           entry_text.insert(END,"\n"+"..................."+"\n")       
         my_list={}
         for j in kind_1:
          my_list[tags_string(j,'title')[0]] = j['id']
         my_id = list(my_list.values())
         my_title = list(my_list.keys())
        
         def on_List(event):
            selected_item = combo_list.get()
            stringa_id.set(my_list[selected_item])
            button_search_id.config(text="Search a Feed",foreground="black") 
                        
         label_title = tk.Label(frame1, text="Title: ", font=('Arial',12,'bold'))
         label_title.grid(column=14, row=0,padx=5,pady=5,ipadx=1,ipady=1)
         combo_list = ttk.Combobox(frame1, values=my_title,font=('Arial',12,'bold'))
         combo_list.grid(column=14, row=1,padx=5,pady=5,ipadx=2,ipady=1)
         combo_list.set("Type of List")
         combo_list.bind("<<ComboboxSelected>>", on_List)              

name=StringVar()
npub_label=Label(root,text="Pubkey",font=('Arial',12,'bold'))
npub_label.place(relx=0.03,rely=0.06,relwidth=0.1)
npub_entry=Entry(root,textvariable=name,font=('Arial',12,'normal'))
npub_entry.place(relx=0.03,rely=0.1,relwidth=0.1)
npub_button_2=Button(root,text="Open", command=timeline_feed,font=('Arial',12,'normal'))
npub_button_2.place(relx=0.14,rely=0.09) 

async def search_kind_(user,x):
    single_author = user 
    single_results = await asyncio.create_task(feed(single_author))
    Z=[]
    note=get_note(single_results)
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z        

#request kind_event

async def get_kind(client, event_):
    f = Filter().kinds(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get(event_):
    # Init logger
    init_logger(LogLevel.INFO)

    client = Client(None)

    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://nostr.land/")
    await client.connect()
    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        test_kind = await get_kind(client, event_)
    else:
        print("errore")
    
    return test_kind

frame1.pack()

def show_noted():
  """Widget function \n
   Open feed Horizontal, 3 Row
   """
  frame2=tk.Frame(root)  
  if len(db_note_list)<=3:
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
  if db_note_list!=[]:
  
   s=1
   s1=0
   se=0         
   for note in db_note_list:   
    
      if db_note_list.index(note)% 80==False:
        s1=0
        se=int(db_note_list.index(note)//80)*4    
  
      try:
       context0="Author: "+note['pubkey']
       
       if note['tags']!=[]:
        if tags_string(note,"title")!=[]:
         for xnote in tags_string(note,"title"):
          context0=context0+"\n"+"Title "+str(xnote) 
        context1=note['content']+"\n"
        context2=" "
        
        for xnote in tags_string(note,"alt"):
         context2=context2+"\n"+str(xnote) +"\n"
        if note["content"]=="": 
         for xnote in tags_string(note,"summary"):
          context2=context2+"\n"+"Summary "+tags_string(note,"summary")[0][0:140]+"\n"
        if len(tags_string(note,"t"))==1:
         for xnote in tags_string(note,"t"):
          context2=context2+"Category "+str(xnote) +" "  
        else:
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context2=context2+"#"+str(xnote) +" "
            s=s+1
        if note["kind"]==30003:    
            for xnote_z in tags_string(note,"i"):
                context2=context2+"\n"+str(xnote_z) +"\n"    
       else: 
        context1="\n"+note['content'][0:100]+"\n"
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=se,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=se+1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=se+1) 
      
       def print_id(entry):
           print(db_note_list.index(entry))
           print(entry['tags'])
                  
       def print_var(entry):
                print(entry)
                print(entry["content"])

       def print_photo(entry):
            if len(more_spam(entry))<2: 
              photo_print(entry)
            else:
               
               if tags_string(entry,"imeta")!=[]:
                photo_list_2(entry)
               else:
                  if len(more_spam(entry))==2:
                    photo_list(more_spam(entry))         
               
       button=Button(scrollable_frame_1,text=f"Print me!", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=se+2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read!", command=lambda val=note: print_id(val))
       button_grid2.grid(row=se+2,column=s1+1,padx=5,pady=5)    
       if tags_string(note,"image")!=[] or tags_string(note,"imeta")!=[]:
        button_grid3=Button(scrollable_frame_1,text=f"Click to see",command=lambda val=note: print_photo(val))
        button_grid3.grid(row=se+2,column=s1+2,padx=5,pady=5)  
     
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="bottom", fill="x",padx=20)
   scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
   canvas_1.pack( fill="y", expand=True)
   frame2.place(relx=0.25,rely=0.3,relwidth=0.65,relheight=0.62)

   def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
        entry_text.place_forget()
        scroll_bar_text.place_forget()
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.5,rely=0.92,relwidth=0.1)      

button_read=Button(root,text="Stamp", command=show_noted,font=("Arial",12,"normal"))

def url_spam(x):
 z=x['content']
 for j in z.split():
    if j[0:5]=="https":
        return str(j)

def more_spam(x):
 z=x['content']
 notes_link=[]
 for j in z.split():
    if j[0:5]=="https":
        notes_link.append(str(j))
 return notes_link       

def codifica_link(x):
   f=url_spam(x)
   list=['mov','mp4']
   img=['png','jpg','JPG','gif']
   img1=['jpeg','webp'] 
   tme=["https://t.me/"]
   xtwitter=["https://x.com/"]
   if f==None:
                 return "no spam"
   if f[-3:] in list:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   if f[0:13] in tme:
            return "tme"
   if f[0:14] in xtwitter:
            return "tme"
   else:
       return "spam"  

def photo_print(note):
 
  if codifica_link(note)=="pic":
   
   frame_pic=tk.Frame(root,height=20,width= 80)
   stringa_pic=StringVar()
   stringa_pic.set(url_spam(note))
   label_pic = Entry(frame_pic, textvariable=stringa_pic)
   image_label = tk.Label(frame_pic)
   image_label.grid(column=0,row=0, padx=10,pady=10)
   if label_pic.get()!="":
       try:
        response = requests.get(label_pic.get(), stream=True)
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        image.thumbnail((250, 250))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image_names= photo
       
        def close_pic():
            image_label.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)
            frame_pic.destroy()
  
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        frame_pic.columnconfigure(0,weight=1)
        frame_pic.rowconfigure(0,weight=3)
        
        button_close.grid(column=0,row=1,padx=10)
        frame_pic.place(relx=0.01,rely=0.4,relwidth=0.23,relheight=0.25,anchor="n")
       except TypeError as e: 
        print(e)  

def more_link(f):
   
   list=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
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

def photo_list(list_note):
 frame_pic=tk.Frame(root,height=80,width= 80) 
 s=0
 list_note1=[]
 for xnote in list_note:
  if more_link(xnote)=="pic":
     list_note1.append(xnote)
 if list_note1!=[]:  
  for note in list_note1:  
   if list_note.index(note)<4:
  
    stringa_pic=StringVar()
    stringa_pic.set(note)
    label_pic = Entry(frame_pic, textvariable=stringa_pic)
    image_label = tk.Label(frame_pic)
    image_label.grid(column=1,row=s, columnspan=2)
    if label_pic.get()!="":
         
       response = requests.get(label_pic.get(), stream=True)
       if response.ok==True:
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        image.thumbnail((250, 200))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image_names= photo
  
        def close_pic():
            image_label.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)
            frame_pic.destroy()
  
        s=s+3
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        button_close.grid(column=2,row=s+1,sticky="n")
        s=s+2
  frame_pic.place(relx=0.01,rely=0.4,relwidth=0.18)

def balance_photo_print(nota):
  if tags_str(nota,"imeta")!=[]:
   balance=[]
   url_=[]
   for dim_photo in tags_str(nota,"imeta"):
     if more_link(dim_photo[1][4:])=="pic": 
      url_.append(dim_photo[1][4:])
      
      for jdim in dim_photo:
       if jdim[0:3]=="dim":
        list_number=dim_photo.index(jdim)   
        for xdim in dim_photo[list_number][4:]:
         if xdim=="x":
          number=dim_photo[list_number].index(xdim)
       
          numberx=number
          numbery=number+1
          balx=dim_photo[list_number][4:numberx]
          baly=dim_photo[list_number][numbery:]  
          
          balance.append(float(int(balx)/int(baly)))
   
   return balance,url_       

def photo_list_2(note):
 frame_pic=tk.Frame(root,height=80,width= 80) 
 
 balance,list_note1=balance_photo_print(note)
 int_var=IntVar()
 lbel_var=Entry(frame_pic, textvariable=int_var)    
 if list_note1!=[] and balance!=[]: 
  if list_note1!=None and balance!=None:
   
   def next_number():
      
      if int((int(lbel_var.get())+1))< len(list_note1):
       int_var.set(int(lbel_var.get())+1)
       print_photo()
      else:
          int_var.set(int(0)) 
          print_photo()
           
   stringa_pic=StringVar()

   def print_photo():
     s=0  
     stringa_pic.set(list_note1[int(lbel_var.get())])
     label_pic = Entry(frame_pic, textvariable=stringa_pic)
    
     image_label = tk.Label(frame_pic)
     image_label.grid(column=1,row=s, columnspan=2)
     if label_pic.get()!="":
         
       response = requests.get(label_pic.get(), stream=True)
       if response.ok==True:
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        number=balance[int(lbel_var.get())]
        test1=int(float(number)*200)
        if test1>400:
           test1=int(400)
        if test1<150:
           test1=int(160)   
        image.thumbnail((test1, 200))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image_names= photo
  
        def close_pic():
            image_label.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)
            frame_pic.destroy()

        def close_one_pic():
            image_label.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)    
            next_number()

        s=s+3
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        button_close.grid(column=2,columnspan=1,row=s+1)
        button_close_photo=Button(frame_pic,command=close_one_pic,text="Next",font=("Arial",12,"bold"))
        button_close_photo.grid(column=1,row=s+1)
        s=s+2
   print_photo()     
   frame_pic.place(relx=0.01,rely=0.4,relwidth=0.24) 
  else:
     print("error", "none")        
 else:
     pass
     #print("error", "[]","maybe a video")

root.mainloop()  