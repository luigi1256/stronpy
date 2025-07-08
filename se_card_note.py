import asyncio
from nostr_sdk import Client, Filter, Keys, NostrSigner, init_logger, LogLevel, PublicKey,Kind, uniffi_set_event_loop
from datetime import timedelta
from asyncio import get_event_loop
from nostr_sdk import *
import json

def tags_string(x,obj):
    f=x["tags"]
    z=[]
    if f!=[]:
     for j in f:
      if j[0]==obj:
          z.append(j[1])
     return z
    
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

def number_kind(tm):
    z=[]
    for v in tm:
        if (v)['kind'] in z:
              None  
        else:
              z.append((v)['kind'])
    return z

def nota_reply_id(nota):
    e_id=[]
    if nota["tags"]!=[]:
      if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id  

def tags_str_long(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
       if len(j)>2:
         z.append(j[1:]) 
       else:    
          z.append(j[1])
    return z   

def tags_first(x):
   tags_list=[]
   tags_value=[]
   if x["tags"]!=[]:
      for jtags in x["tags"]:
         if jtags[0] not in tags_list:
            tags_list.append(jtags[0])
   if tags_list!=[]:
       for xtags in tags_list:
         for ztags in tags_str(x,xtags):
            tags_value.append(ztags)
   return tags_list,tags_value 

def tags_parameters(key,value,s):
    list_q=[]
    if s in key:
        for xvalue in value:
          if xvalue[0]==s:
              list_q.append(xvalue[1:])
    return list_q,s  

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z 

def search_3(note,x):
    Z=[]
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list 

def new_note_time(list_new:list):
   if timeline_list_kind!=[]:
      new_note_2=[]
      if list_new!=[]:
       for new_x in list_new:
        if new_x not in timeline_list_kind:
          new_note_2.append(new_x)  
       i=0
    
       while i<len(new_note_2):
         j=0
         while j< len(timeline_list_kind): 
          if timeline_list_kind[j]["created_at"]>(new_note_2[i]["created_at"]):
           j=j+1
          else:
           timeline_list_kind.insert(j,new_note_2[i])
           break
         i=i+1
       return timeline_list_kind
      else:
          return None
   else:
        for list_x in list_new:
            if list_x not in timeline_list_kind:
             timeline_list_kind.append(list_x)
        return timeline_list_kind 

def timeline_created(list_new):
  new_note=[] 
  global kind_db_list
 
  if kind_db_list!=[]:
   for new_x in list_new:
    if len(kind_db_list)<100: 
     if new_x not in kind_db_list:
        new_note.append(new_x) 
   i=0
    
   while i<len(new_note):
     j=0
     while j< len(kind_db_list): 
      if kind_db_list[j]["created_at"]>(new_note[i]["created_at"]):
         j=j+1
      else:
         kind_db_list.insert(j,new_note[i])
         break
     i=i+1
   return kind_db_list   
  else:
        for list_x in list_new:
            kind_db_list.append(list_x)
        return kind_db_list  

async def get_event(client, event_):
    tag_event=[]
    tag_identifiers=[]
    tag_pubkey=[]
    for tag_id in event_:
     if len(tag_id)==64:
      tag_event.append(EventId.parse(tag_id))
     else:
       try:
        if len(tag_id)>71 and tag_id[5]==":" and tag_id[70]==":":
         coord = Coordinate(Kind(int(tag_id[0:5])),PublicKey.parse(tag_id[6:70]),str(tag_id[71:]))
         if coord not in tag_identifiers:
           tag_identifiers.append(coord.identifier())
           tag_pubkey.append(coord.public_key())
       except NostrSdkError as e:
          print(e)     
    if tag_event!=[]: 
     tag_identifiers.clear()
     tag_pubkey=[]
     f = Filter().ids(tag_event)
    if tag_identifiers!=[]: 
     f = Filter().identifiers(tag_identifiers).authors(tag_pubkey)
     
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Selected_event(event_):
        
    client = Client(None)
    uniffi_set_event_loop(asyncio.get_running_loop())
    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    if relay_list!=[]:
        for xrelay in relay_list:
            await client.add_relay(xrelay)
    await client.connect()
    
    if isinstance(event_, list):
        test_kind = await get_event(client, event_)
    else:
        print("errore")
    await asyncio.sleep(2.0)
    
    return test_kind

async def get_note_cluster(client, authors, type_of_event):
    f = Filter().authors(authors).kinds(type_of_event).limit(1000)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_relay(client, user):
    f = Filter().author(user).kind(Kind(3))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_metadata(user):
    uniffi_set_event_loop(asyncio.get_running_loop())  
    client = Client(None)
    
    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://nostr-pub.wellorder.net/")
    if relay_list!=[]:
        for xrelay in relay_list:
            await client.add_relay(xrelay)
    await client.connect()
    if isinstance(user,list):
     f = Filter().authors(user).kind(Kind(0))
    else:
       f = Filter().author(user).kind(Kind(0)) 
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    await asyncio.sleep(2.0)
    await client.disconnect()
    return z
  
async def feed_cluster(authors,type_of_event):
    # Init logger
    init_logger(LogLevel.INFO)
   
    client = Client(None)
    uniffi_set_event_loop(asyncio.get_running_loop())

    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://nostr-pub.wellorder.net/")
    if relay_list!=[]:
        for xrelay in relay_list:
            await client.add_relay(xrelay)
    else:
       relay_list.append("wss://nostr.mom/")
       relay_list.append("wss://nos.lol/")
       combo_list_lay["values"]=relay_list
     
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_note_cluster(client, authors, type_of_event)
    else:
        combined_results = await get_relay(client, authors)
    
    return combined_results

timeline_list_kind=[]
timeline_people=[]
block_id=[]

def found_follow():
   if combo_box.get()!="Name": 
     type_event=""
     follow_kind=get_note(asyncio.run(feed_cluster(convert_user(my_dict[str(combo_box.get())]),type_event))) 
     if follow_kind!=[]:
        people=tags_string(follow_kind[0],"p")
        if people!=None:
         for people_x in people:
           if people_x not in timeline_people:
              timeline_people.append(people_x)

def timelines(): 
 if combo_box.get()!="Name": 
  type_event=[Kind(30023),Kind(1),Kind(7),Kind(6),Kind(9735)]
  if timeline_people!=[]:
   tm=get_note(asyncio.run(feed_cluster(user_convert(timeline_people),type_event)))
   new_note_time(tm)
   stamp_note()
   combo_list.place(relx=0.11,rely=0.4)
  else:
     found_follow()
      
my_dict = {"Pablo": "fa984bd7dbb282f07e16e7ae87b26a2a7b9b90b7246a44771f0cf5ae58018f52", 
           "jb55": "32e1827635450ebb3c5a7d12c1f8e7b2b514439ac10a67eef3d9fd9c5c68e245",
             "Vitor": "460c25e682fda7832b52d1f22d3d22b3176d972f60dcdc3212ed8c92ef85065c", 
             " Hodlbod": "97c70a44366a6535c145b333f973ea86dfdc2d7a99da618c40c64705ad98e322", 
             "me": "592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"}

import tkinter as tk
from tkinter import *
from tkinter import ttk
root = tk.Tk()
root.geometry("1250x800")
root.title("See Note")

frame1=tk.Frame(root,height=100,width=200,background="grey")
label = tk.Label(frame1, text="Selected Item: ",font=('Arial',12,'bold'))
label.grid(pady=10, column=0, columnspan=2, row=1)
my_list = list(my_dict.values())
my_name = list(my_dict.keys())

def on_select(event):
    selected_item = combo_box.get()
    label.config(text="Selected Item: " + my_dict[selected_item][0:9])
    combo_list.place_forget()

combo_box = ttk.Combobox(frame1, values=["Pablo","jb55","Vitor"," Hodlbod","me"],font=('Arial',12,'bold'))
combo_box.grid(pady=5,column=1, row=0,ipadx=1)
combo_box.set("Name")
combo_box.bind("<<ComboboxSelected>>", on_select)
label_name=tk.Label(frame1, text="Profile",font=('Arial',12))
label_name.grid(column=0, row=0,ipadx=1, padx=5)

label1=tk.Label(frame1, text= "Se note", font=('Arial',14,'bold'),background="grey", width=15)
label1.grid(column=4, row=0,padx=5,pady=5,ipadx=1,ipady=1,rowspan=2, columnspan=2)
frame4=tk.Frame(root,height=25,width= 100)
Channel_frame = ttk.LabelFrame(root, text="Relay", labelanchor="n", padding=10)
Channel_frame.place(relx=0.1,rely=0.21,relheight=0.15,relwidth=0.22)   
button3=tk.Button(root,text="Some Kinds",command=timelines,font=('Arial',14))  #read_Timeline
button3.place(relx=0.12,rely=0.26)   
button_2=tk.Button(root,text="kind 3",command=found_follow,font=('Arial',14))  #timeline
button_2.place(relx=0.24,rely=0.26)  

def count_follow_list():
       
       label_count_2.config(text=str(len(timeline_people)))
       label_count_2.place(relx=0.45,rely=0.25)
       button_3_c.place(relx=0.33,rely=0.24)

def clear_follow_list():
     timeline_people.clear()
     
     button_3_c.place_forget()
     label_count_2.place_forget()

Channel_frame_three = ttk.LabelFrame(root, text="Count", labelanchor="n", padding=10)
Channel_frame_three.place(relx=0.32,rely=0.21,relheight=0.15,relwidth=0.17) 
label_count_2=tk.Label(root, text=str(len(timeline_people)), font=('Arial',12,'bold'),foreground="darkgrey")
button_3=tk.Button(root,text="kind 3 len",command=count_follow_list,font=('Arial',14))  
button_3.place(relx=0.36,rely=0.24)  
label2=tk.Label(frame4, text="", font=('Arial',12,'bold'),foreground="darkgrey")
label_tm_1=tk.Label(root, text=str(len(timeline_list_kind)), font=('Arial',12,'bold'),foreground="darkgrey")

def count_note_list():
    label_tm_1=tk.Label(root, text=str(len(timeline_list_kind)), font=('Arial',12,'bold'),foreground="darkgrey")
    label_tm_1.place(relx=0.44,rely=0.31)

button_4=tk.Button(root,text="kind TM len",command=count_note_list,font=('Arial',12))  
button_4.place(relx=0.36,rely=0.3)     
kind_db_list=[]
note_lile=[]
button_3_c=tk.Button(root,text="C",command=clear_follow_list,font=('Arial',14, "bold"))  

def clear_kind_scroll():
   for kind_x in kind_db_list:
      block_id.append(kind_x["id"])  
   kind_db_list.clear() 
   label_count_id=Label(root,text="Block Id "+ str(len(block_id)),font=('Arial',14),fg="grey") 
   label_count_id.place(relx=0.75,rely=0.02) 

button_3_z=tk.Button(root,text="Scrolless",command=clear_kind_scroll,font=('Arial',14), background="grey") 
button_3_z.place(relx=0.85,rely=0.10, anchor="n") 
wall=tk.Label(frame1, text="",background="lightgrey",height=4)
wall.grid(column=3, row=0,padx=10,pady=5, rowspan=2)
frame1.place(relx=0.1,rely=0.06)
frame4.place(relx=0.1,rely=0.7)

def layout():
   if kind_db_list!=[]: 
    frame1=Frame(root, width=360, height=100)
    canvas = Canvas(frame1)
    canvas.pack(side="left", fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame1, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_frame = Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    list_note_lib=[]
    def create_note(note_text, s):
        # Message 
       
        if note_text["content"] not in list_note_lib:
         list_note_lib.append(note_text["content"])
         var_npub =StringVar()
         Message_npub= Message(scrollable_frame, textvariable=var_npub, width=350,font=('Arial',12,'normal')) 
         if note_text["pubkey"] in list(Pubkey_Metadata.keys()):
            var_npub.set("Nickname " +Pubkey_Metadata[note_text["pubkey"]])
         else:
            var_npub.set("Pubkey "+note_text["pubkey"])
         Message_npub.grid(row=s+1, column=0, columnspan=3, padx=10, pady=2, sticky="w") 
         var_time =StringVar()
         Message_time= Message(scrollable_frame, textvariable=var_time, width=350,font=('Arial',12,'normal'))
         var_time.set("Time: "+(str((note_text)["created_at"])))
         Message_time.grid(row=s, column=0, columnspan=3, padx=50, pady=5,sticky="w")

         scroll_bar_mini = tk.Scrollbar(scrollable_frame)
         second_label10 = tk.Text(scrollable_frame, padx=8, height=5, width=35, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
         scroll_bar_mini.config( command = second_label10.yview )
         context2=""   
         if note["tags"]!=[]:
          if tags_string(note_text,"t")!=[] :
            for note_tags in tags_string(note_text,"t"):
               context2=context2+str("#")+note_tags+" "
          if tags_string(note,"e")!=[]:
           
           if four_tags(note,"e") and note["kind"]!=30023:
            for F_note in four_tags(note,"e"):
             if len(F_note)>3:
              context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
         else:
          pass     
         if note_text["kind"]==6:       
           second_label10.insert(END,"RT "+str(note_text["kind"])+"\n"+json.loads(note_text["content"])["content"]+"\n"+str(context2))  
         else:
           second_label10.insert(END,note_text["content"]+"\n"+str(context2))  
         
         scroll_bar_mini.grid( sticky = NS,column=4,row=s+2,pady=5)
         second_label10.grid(padx=10, column=0, columnspan=3, row=s+2)  
         if note_text["kind"]==7:
            scroll_bar_mini.grid_forget()
            second_label10.grid_forget()    
            var_plus =StringVar()
            Message_plus= Message(scrollable_frame, textvariable=var_plus, width=350,font=('Arial',12,'normal'))
            var_plus.set("Note: "+(str((note_text)["content"])))
            Message_plus.grid(column=0, columnspan=4, row=s+2, pady=5,sticky="w")
         # Button down
         Button(scrollable_frame, text="Open", command=lambda: show_print_test_tag(note_text),font=('Arial',12,'normal')).grid(row=s+3, column=0, padx=5, pady=5)
         blo_label = Button(scrollable_frame, text="Share",font=('Arial',12,'normal'), command=lambda: share_note(note_text))
         blo_label.grid(row=s + 3, column=1, padx=2, pady=5)
         Button(scrollable_frame, text="Print Note", command=lambda: print(note_text), font=('Arial',12,'normal')).grid(row=s +3, column=2, padx=5, pady=2)
         
    s = 1
    for note in kind_db_list: 
     create_note(note, s)
     s += 4   
    
    frame1.place(relx=0.55,rely=0.21, relheight=0.4,relwidth=0.4)  
    
    def share_note(note_text):
      test=EventId.parse(note_text["id"])
      test1=Nip19Event(test,PublicKey.parse(note_text["pubkey"]),Kind(note_text["kind"]),[])
      print(test1.to_nostr_uri())
      
      print(str(test.to_nostr_uri()))

    def close_canvas():
        scrollable_frame.forget()
        canvas.destroy()
        frame1.destroy()
        
    if list_note_lib==[]:
     close_canvas()    
    
    button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close.grid(column=1,row=0, padx=5,pady=5)  
 
button_open=Button(root, command=layout, 
                   text="scroll",
                    highlightcolor='WHITE',
                    background="grey",
                  width=8,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))

button_open.place(relx=0.75,rely=0.10, anchor="n")

def on_server(event):
    label_r_lay.config(text="Relay: "+ str(len(relay_list)))
    call_r_lay()
    combo_list_lay["values"]=relay_list
    label_r_lay.config(text="Relay: "+ str(len(relay_list)))

async def get_result_(client,relay_1):
    
    f = Filter().kind(Kind(10002)).reference(relay_1).limit(10)
   
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Search_r_lay(relay_1):
       init_logger(LogLevel.INFO)
       client = Client(None)
       uniffi_set_event_loop(asyncio.get_running_loop())
       await client.add_relay(relay_1)
       await client.connect()
       await asyncio.sleep(2.0)

       combined_results = await get_result_(client,relay_1)
       if combined_results:
        return combined_results
     
def call_r_lay():
  if combo_list_lay.get()!="Relay List":
   if __name__ == "__main__":
    response=asyncio.run( Search_r_lay(combo_list_lay.get()))
    if response:

     note_=get_note(response)
     for jnote in note_:
      for relay_x in tags_string(jnote,"r"):
         if relay_x[0:6]=="wss://" and relay_x[-1]=="/" and relay_x not in relay_list:
            if len(relay_list)<6:
                relay_list.append(relay_x)

relay_list=[]
label_r_lay = tk.Label(frame1, text="Relay: ", font=('Arial',12,'bold'))
label_r_lay.grid(column=7, row=0,padx=20,pady=5,ipadx=1,ipady=1)
combo_list_lay = ttk.Combobox(frame1, values=relay_list,font=('Arial',12,'bold'))
combo_list_lay.grid(column=7, row=1,padx=20,pady=5,ipadx=2,ipady=1)
combo_list_lay.set("Relay List")
combo_list_lay.bind("<<ComboboxSelected>>", on_server) 

def show_print_test_tag(note):
   
   frame3=tk.Frame(root)  
   canvas_2 = tk.Canvas(frame3,width=490)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = ttk.Frame(canvas_2)

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")))

   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
   if note["pubkey"] in list(Pubkey_Metadata.keys()):
            context0="Nickname " +Pubkey_Metadata[note["pubkey"]]
   else:
            context0="Pubkey "+note["pubkey"]
   context0=context0+"\n"+"id: "+note["id"]+"\n"
   if note['tags']!=[]:
        context2="\n"+"[ [  Tags ] ]"+"\n"+"\n"
        context2=context2+"tags number: "+str(len(note["tags"])) +"\n"
   else: 
        context2=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   
   var_id.set(context0)
   s=0
   label_id.grid(pady=2,column=0, row=s,columnspan=3,rowspan=2)
   scroll_bar_mini_2 = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini_2.grid( sticky = NS,column=3,row=s+2,rowspan=2,pady=5)
   second_label_2 = tk.Text(scrollable_frame_2, padx=8, height=5, width=30, yscrollcommand = scroll_bar_mini_2.set, font=('Arial',14,'bold'),background="#D9D6D3")
   if note["tags"]!=[]:
         if note["kind"]==30023:
          context2=create_tags(note,note["kind"])
         if tags_string(note,"t")!=[] :
            for note_tags in tags_string(note,"t"):
               context2=context2+str("#")+note_tags+" "
         if tags_string(note,"e")!=[]:
           
           if four_tags(note,"e") and note["kind"]!=30023:
            for F_note in four_tags(note,"e"):
             if len(F_note)>3:
              context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
         else:
          pass            
   second_label_2.insert(END,note["content"]+"\n"+str(context2))
   scroll_bar_mini_2.config( command = second_label_2.yview )
   second_label_2.grid(padx=10, column=0, columnspan=3, row=s+2,rowspan=2)

   button_grid_1=Button(scrollable_frame_2,text="", width=10, height=3)
   button_grid_1.grid(row=s,column=5,padx=5,pady=5)    
                   
   def print_media(entry):
      if len(more_spam(entry))<2: 
              photo_print(entry)
      else:
               
               if tags_string(entry,"imeta")!=[]:
                photo_list_2(entry)
               else:
                  if len(more_spam(entry))==2:
                    photo_list(more_spam(entry))

   button_grid_2=Button(scrollable_frame_2,text="Read", command=lambda val=note: print_content(val),width=10, height=3)
   button_grid_2.grid(row=s+1,column=5,padx=5,pady=5)    
   button_grid_3=Button(scrollable_frame_2,text="Open Media", command=lambda val=note: print_media(val),width=10, height=3)
   button_grid_3.grid(row=s+2,column=5,padx=5,pady=5)
   button_grid_4=Button(scrollable_frame_2,text="Reply", command=lambda val=note: print_content(val),width=10, height=3)
   button_grid_4.grid(row=s+3,column=5,padx=5,pady=5)    
       
   def print_tags(entry):
                
                list_one,list_two=tags_first(entry)
                var_id_2=StringVar()
                label_id_2= Message(scrollable_frame_2,textvariable=var_id_2, relief=RAISED,width=220,font=("Arial",12,"normal"))
                s=5
                
                def val_tag(val):
                    s=5
                    list_z,par=tags_parameters(list_one,list_two,val)
                    var_id_2.set(str(list_z))
                    value=list_one.index(par)
                    label_id_2.grid(pady=2,column=1,row=s+value, columnspan=2)  
                button_list=[]
                if list_one:
         
                 z=0
         
                 while z<len(list_one):
          
                    button_grid2=Button(scrollable_frame_2,text=str(list_one[z]), command=lambda val=list_one[z]: val_tag(val))
                    button_grid2.grid(row=s,column=0,padx=5,pady=5) 
                    button_list.append(button_grid2)   
                    z=z+1
                    s=s+1 
                 button_stamp=Button(scrollable_frame_2,text="stamp", command=lambda val=var_id_2: stamp_var(val))
                 button_stamp.grid(column=0,row=s+1,padx=5,pady=5)
                 def close_Tags():
                    button_stamp.grid_forget()
                     
                    for button2 in  button_list:
                     button2.grid_forget()
                    
                    button_c_tags.grid_forget()
                    label_id_2.grid_forget()
                    
                 button_c_tags=Button(scrollable_frame_2,command=close_Tags,text="Tag ❌",font=("Arial",12,"normal"))
                 button_c_tags.grid()   
          
                if 'mention' in tags_str_long(entry,"e"):
                    print("e "+tags_str_long(entry,"e"))
                if 'mention' in tags_str_long(entry,"a"):   
                     print("a "+tags_str_long(entry,"a"))

   def stamp_var(entry):
                if entry.get()!="":
                 print(entry.get())                                  
   s=4        
   button=Button(scrollable_frame_2,text=f"Tags!", command=lambda val=note: print_tags(val))
   button.grid(column=0,row=s,padx=5,pady=5)

   def print_content(entry):
       result=show_note_from_id(entry)
       if result!=None: 
        z=3
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             if jresult["pubkey"] in list(Pubkey_Metadata.keys()):
                var_id_r.set("Nickname " +Pubkey_Metadata[jresult["pubkey"]])
             else:
                var_id_r.set(" Author: "+jresult["pubkey"])
                      
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             context22="---> tags: <--- "+"\n"   
             if tags_string(jresult,"e")!=[]:
              if four_tags(jresult,"e"):
                for F_note in four_tags(note,"e"):
                     if len(F_note)>3:
                      context22=context22+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              else:
                 if tags_string(jresult,"e"):
                    context22=context22+str(len(tags_string(jresult,"e")))+ "\n"
                 else:
                    context22="---> Root  <--- "     
             else:
               context22="---> Root  <--- "
             second_label10_r.insert(END,jresult["content"]+"\n"+str(context22))
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
           z=z+2
                          
   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply!", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s,column=2,padx=5,pady=5)    
   else:
    if is_video(note)!=None:
     button_grid3=Button(scrollable_frame_2,text=f"See video!")  #pass
     button_grid3.grid(row=s,column=2,padx=5,pady=5)        

   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()   

   button_frame=Button(frame3,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.pack(pady=5)   
   frame3.place(relx=0.55,rely=0.20,relheight=0.53,relwidth=0.45) 

def show_note_from_id(note):
        result=note["id"]
       
        replay=nota_reply_id(note)
        replay.append(result)
        if replay!=[]:
           items=get_note(asyncio.run(Selected_event(replay)))
        else:
           items=get_note(asyncio.run(Selected_event(result)))
        return items   

from PIL import Image, ImageTk
import requests
import shutil

def more_spam(x):
 z=x['content']
 notes_link=[]
 for j in z.split():
    if j[0:5]=="https":
        notes_link.append(str(j))
 return notes_link   

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
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        number=balance[int(lbel_var.get())]
        test1=int(float(number)*250)
        if test1>400:
           test1=int(400)
        if test1<150:
           test1=int(160)   
        image.thumbnail((test1, 250))  # Resize image if necessary
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
   frame_pic.place(relx=0.4,rely=0.6,relwidth=0.3) 
  else:
     print("error", "none")        
 else:
     pass
     
def is_video(nota):
   if nota["tags"]!=[]: 
    if tags_str(nota,"imeta")!=[]:
      url_=[]
      for dim_photo in tags_str(nota,"imeta"):
       if more_link(dim_photo[1][4:])=="video":
          url_.append(dim_photo[1][4:])
      if url_!=[]:
         print(url_)
         return url_     

def balance_photo_print(nota):
 if nota["tags"]!=[]: 
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
  else:
     return None,None
 else:
     return None,None 

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

def url_spam(x):
 z=x['content']
 for j in z.split():
    if j[0:5]=="https":
        return str(j)
    
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
  
        s=s+3
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        button_close.grid(column=2,row=s+1,sticky="n")
        s=s+2
  frame_pic.place(relx=0.45,rely=0.6,relwidth=0.18)    

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
        frame_pic.place(relx=0.45,rely=0.6,relwidth=0.3,relheight=0.3,anchor="n")
       except TypeError as e: 
        print(e)  

def search_kind(user,x):
    
     # Example usage with a single key
    single_author = user 
    single_results = asyncio.run(get_metadata(single_author))
    Z=[]
    note=get_note(single_results)
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z     

def list_people_fun():
    people_list=[]
    if timeline_list_kind!=[]:
        for note_x in timeline_list_kind:
            if note_x["pubkey"] not in people_list:
                        people_list.append(note_x["pubkey"])
        return people_list       
    else:
       return people_list

Pubkey_Metadata={}

def pubkey_id(test):
   
   metadata_note=search_kind(PublicKey.parse(test),0)
   if metadata_note!=[]:
       single=metadata_note[0]
       single_1=json.loads(single["content"])
       try:
        if "name" in list(single_1.keys()):
         if single_1["name"]!="":
           
           
           if test not in list(Pubkey_Metadata.keys()):
              Pubkey_Metadata[test]=single_1["name"]
             
        else:   
           if "display_name" in list(single_1.keys()):
            if single_1["display_name"]!="":
                    
                if test not in list(Pubkey_Metadata.keys()):
                  Pubkey_Metadata[test]=single_1["display_name"]    
                   
       except KeyError as e:
          print("KeyError ",e)     

def list_pubkey_id():
  people_list=list_people_fun()
  if people_list !=[]:
   test_people=user_convert(people_list)    #not cover people are already on metadata
   metadata_note=search_kind(test_people,0)
   if metadata_note!=[]:
       for single in metadata_note:
        single_1=json.loads(single["content"])
        try:
         if "name" in list(single_1.keys()):
          if single_1["name"]!="":
           
           
           if single["pubkey"] not in list(Pubkey_Metadata.keys()):
              Pubkey_Metadata[single["pubkey"]]=single_1["name"]
              
         else:   
            if "display_name" in list(single_1.keys()):
             if single_1["display_name"]!="":
               
                
                if single["pubkey"]not in list(Pubkey_Metadata.keys()):
                  Pubkey_Metadata[single["pubkey"]]=single_1["display_name"]   
                  
        except KeyError as e:
          print("KeyError ",e)             
   
button_people_2=Button(root,text=f"Find People ", command=list_pubkey_id,font=('Arial',12,'bold'))
button_people_2.place(relx=0.11,rely=0.50) 
sad_people=[]
sum_classification={}
list_kind_event=[]

def list_sad_people():
   if timeline_list_kind!=[]:
      for note_x in timeline_list_kind:
       if note_x["pubkey"] not in sad_people:
        sad_people.append(note_x["pubkey"])  
         
def pubkey_tot_id(test):
   note_pubkey=[]
   for note_x in timeline_list_kind:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   return len(note_pubkey),note_pubkey  

def pubkey_test_id(test):
   lenght,notes=pubkey_tot_id(test)
   if lenght>0 and notes!=[]:
    list_kind=[]
    for note_x in notes:
       list_kind.append(note_x["kind"])
    sum_notes=sum(list_kind)     
    sum_classification[test]=sum_notes

def sum_test_id(test):
   lenght,notes=pubkey_tot_id(test)
   if lenght>0 and notes!=[]:
    list_kind=[]
    for note_x in notes:
       list_kind.append(note_x["kind"])
    print(list_kind)

def numb_event_pubkey(test):
    lenght,tm=pubkey_tot_id(test)
    t=number_kind(tm)
    i=0
    number=[]
    while i<len(t):
        tip_i=[]
        for v in tm:
         if (v)['kind']==t[i]:
           tip_i.append(v)
        number.append(tip_i)
        i=i+1
    j=0
    label_event=""
    while j<len(number):
     label_event=label_event+str("kind number ")+ str(t[j]) +str(" number event ")+ str(len(number[j]))+"\n"
     
     j=j+1 
    if Pubkey_Metadata!={}: 
     if test in list(Pubkey_Metadata.keys()):
        print(Pubkey_Metadata[test],"\n",label_event) 
     else:
        print(label_event)   
    else:
       print(label_event) 
   
    return t, number    

def stamp_classification():
     if timeline_list_kind!=[]:
      list_sad_people()
      if sad_people!=[]:
       for person in sad_people:
          pubkey_test_id(person)
       print("ok") 
      else:
         print("error 2")
     else:
        print("error 1")       

def print_test_classification(test):
    #List
    if sum_classification=={}:
       stamp_classification()
    print(sum_classification[test])
    numb_event_pubkey(test)

def stamp_note():
       list_kind=[]
       for numb_x in timeline_list_kind:
          if numb_x["kind"] not in list_kind:
             list_kind.append(numb_x["kind"])  
       combo_list.set("Kind Event")      
       order_list=list_kind.sort()
       combo_list['values']=list_kind

def read_kind_note(n:int):
       list_kind_event.clear()
       list_kind=[]
       number_event=timeline_list_kind
       
       for numb_x in number_event:
          if numb_x["kind"]==n:
            list_kind_event.append(numb_x)
          if numb_x["kind"] not in list_kind:
             list_kind.append(numb_x["kind"])  
       if list_kind_event!=[]:  
        print("kind number ", n, " number of events ",len(list_kind_event))

def on_selection(event):
    selected_item = combo_list.get()
    kind_note.set(int(selected_item))
    read_kind_note(kind_note.get())
    show_Teed()

combo_list = ttk.Combobox(root, values=[],width=10, font=('Arial',12,'bold'))
combo_list.set("")
combo_list.bind("<<ComboboxSelected>>", on_selection)
kind_note=IntVar()

def create_contentxt(note,n):
   contentxt=""
   if n==1 or n==7:
      if len(note["content"])<100:
       contentxt=contentxt+note["content"]
      else:
          contentxt=contentxt+note["content"][0:100]+"\n" +"More..."
   if n==6: 
      z=(note)['content']
      import json
      if z!= "":
             j = json.loads(z)
             contentxt=contentxt + "RT "+ str(j["content"]) 
     
   if n==30023:
      contentxt=contentxt+"Lenght "+str(len(note["content"]))  
   if n in [1,6,7,30023]:   
    return contentxt 
   else:
      return str("kind ")+str(n)  

def create_tags(note,n):
   contentag=""
   if note["tags"]!=[]:
    if n==1: 
      if tags_string(note,"e")!=[]:
       contentag=contentag+"\n"+ "Reply" +"\n"
      if tags_string(note,"t")!=[]:
       contentag=contentag+"\n"+str(tags_string(note,"t")) +"\n" 
    
    if n==30023:
      if tags_string(note,"title")!=[]:
       contentag=contentag+"\n"+"Title "+str(tags_string(note,"title")[0])  
      if tags_string(note,"sumamry")!=[]:
       contentag=contentag+"\n"+"Summary "+str(tags_string(note,"summary")[0])   
    if n in [1,30023]:   
     return contentag 
   else:
      return str("\n"+"kind "+str(n))     

def show_Teed():
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

 def create_page(db_list_):
  if db_list_!=[] and db_list_!=None:
   if len(db_list_)>200:
    db_list_=db_list_[0:200] 
   s=1
   for note in db_list_:
     try:
      if note["pubkey"] in list(Pubkey_Metadata.keys()):
            context0="Nickname " +Pubkey_Metadata[note["pubkey"]]+" "+str(note["created_at"])+"\n"
      else:
            context0="Pubkey "+note['pubkey']+"\n"
      context1=create_contentxt(note,note["kind"])
      context2=create_tags(note,note["kind"])
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      if context2!=None:
       var_id.set(context0+str(context1)+context2)
      else:
         var_id.set(context0+str(context1))
      
      label_id.grid(pady=2,column=0, columnspan=3)

      def print_id(entry):
            show_print_test(entry)       
                          
      def print_var(entry):
                Pubkey_layout(entry["pubkey"])
           
      button=Button(scrollable_frame_1,text=f"Other Notes", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"Read Note!", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s,column=1,padx=5,pady=5) 
      button_grid3=Button(scrollable_frame_1,text=f"Value!", command=lambda val=note["pubkey"]: print_test_classification(val))
      button_grid3.grid(row=s,column=2,padx=5,pady=5)     
       
      s=s+2  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="right", fill="y",pady=20)
   canvas_1.pack( fill="y", expand=True)
   frame2.place(relx=0.22,rely=0.45,relwidth=0.28,relheight=0.4)
    
   def close_number() -> None :
        frame2.destroy()    
        button_f_close.place_forget()
        
   button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"))
   button_f_close.place(relx=0.45,rely=0.4)      
     
 create_page(list_kind_event)
 root.update_idletasks()
 
def show_print_test(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = ttk.Frame(canvas_2)

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")))
   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
   context0="Pubkey: "+note['pubkey']+"\n"+"id: "+note["id"]
   try:
    context1=note['content']+"\n"
    if note['tags']!=[]:
        tag_note=""
        for note_x in note["tags"]:
           tag_note=tag_note+ str(note_x)+"\n"
        context2="[[ Tags ]]"+"\n" +tag_note

    else: 
        context2=""
   except TypeError as e:
      print(e)        
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   var_id.set(context0)
   label_id.grid(pady=2,column=0, columnspan=3)
   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
   second_label10 = tk.Text(scrollable_frame_2, padx=8, height=5, width=28, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   second_label10.insert(END,context1+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label10.yview )
   second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
      
   def print_note(entry):
           print(entry)

   def print_var(entry):
        if entry["tags"]!=[]:
          if tags_string(entry,"image")!=[]: 
           print("see this photo: ", tags_string(entry,"image")[0])
           photo_list_2(entry)

   if tags_string(note,"imeta")!=[]:      
    button=Button(scrollable_frame_2,text=f"Photo!", command=lambda val=note: print_var(val))
    button.grid(column=0,row=s+2,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Stamp", command=lambda val=note: print_note(val))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()    

   button_frame=Button(scrollable_frame_2,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.grid(row=s+3,column=1,padx=5,pady=5)
   frame3.place(relx=0.67,rely=0.6,relwidth=0.3,relheight=0.35 ) 

def Pubkey_layout(test):
   note_pubkey=[]
   for note_x in timeline_list_kind:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   if len(note_pubkey)>1:      
    kind_db_list.clear() 
    timeline_created(note_pubkey)
    layout()

button_id=tk.Button(root,command=show_Teed,text="Go Kind")

root.mainloop()