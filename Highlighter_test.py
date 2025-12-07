from nostr_sdk import *
import asyncio
from datetime import timedelta
import tkinter as tk
from tkinter import *
from tkinter import ttk
import json
from cryptography.fernet import Fernet

root = tk.Tk()
root.title("Highlighter Example")
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

Checkbutton5 = IntVar() 
frame_time=tk.Frame(root,height=100,width=200)

def five_event():
     if Checkbutton5.get() == 0:
        Button5.config(text= " 60 day")
        frame_time.grid_forget()
        
     else:
       
        Button5.config(text= "Time")
        frame_time.grid(column=0,row=5, columnspan=9,rowspan=3)

frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
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
entry_var=Entry(root, textvariable=entry_variable,font=("Arial",12,"bold"),width=15)
entry_var.place(relx=0.42,rely=0.25)

async def get_result_w(client):
    if Checkbutton5.get() == 1:
          f = Filter().identifier(entry_var.get()).kind(Kind(30023)).since(timestamp=Timestamp.from_secs(since_day(int(since_entry.get())))).until(timestamp=Timestamp.from_secs(since_day(int(until_entry.get())))).limit(10)
    else:
           f = Filter().identifier(entry_var.get()).kind(Kind(30023)).since(timestamp=Timestamp.from_secs(since_day(int(60)))).until(timestamp=Timestamp.from_secs(since_day(int(0)))).limit(10)

    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

db_list_note=[]
relay_search_list=[]

async def Search_d_tag():
    # Init logger
    init_logger(LogLevel.INFO)
    client = Client(None)
    # Add relays and connect
    if relay_search_list!=[]:
       for jrelay in relay_search_list:
          await client.add_relay(RelayUrl.parse(jrelay))
       await client.connect()
       await asyncio.sleep(2.0)

       combined_results = await get_result_w(client)
       return combined_results
     
    await search_box_relay()
    print("found ", len(relay_search_list), " relays")

def call_text():
  if entry_var.get()!="":
   if __name__ == "__main__":
    response=asyncio.run(Search_d_tag())
    if response:

     note_=get_note(response)
     for jnote in note_:
       if jnote not in db_list_note:
          db_list_note.append(jnote)
       if len(jnote["content"])<800:
          second_label10.insert(END,str(jnote["content"]))
       else:
             second_label10.insert(END,str(jnote["tags"]))
       second_label10.insert(END,"\n"+"____________________"+"\n")
       second_label10.insert(END,"\n"+"\n")

    else:
       print("empty")
  else:     
       if relay_search_list==[]:
          if __name__ == "__main__":
            response=asyncio.run(Search_d_tag())
          if len(relay_search_list)>0:
             button_close_search["text"]="Search 🔍"

public_list=[]
label_d_search=tk.Label(root, text='Article d Tag',font=('Arial',12,'bold'))    
label_d_search.place(relx=0.43,rely=0.21 ) 
button_close_search=tk.Button(root, text='Search Relay',font=('Arial',12,'bold'), command=call_text)    
button_close_search.place(relx=0.55,rely=0.24 ) 

async def get_search_relay(client):
   if public_list!=[]:
    f=Filter().authors(public_list).kind(Kind(10007))
   else: 
    f=Filter().kind(Kind(10007)).limit(10)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec()]
   return z

relay_url_list=[]

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

async def search_box_relay():
        
    client = Client(None)
    
    if relay_url_list!=[]:
       
       for jrelay in relay_url_list:
          await client.add_relay(jrelay)
             
    else:
       await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
       
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
           await Search_status(client=Client(None),list_relay_connect=relay_search_list)        
    
relay_search_list=[]
Bad_relay_connection=["wss://relay.noswhere.com/","wss://relay.purplestr.com/"]
scroll_bar_mini = tk.Scrollbar(frame1)
scroll_bar_mini.grid( sticky = NS,column=4,row=0,rowspan=3)
second_label10 = tk.Text(frame1, padx=10, height=5, width=25, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'))
scroll_bar_mini.config( command = second_label10.yview )
second_label10.grid(padx=10, column=1, columnspan=3, row=0, rowspan=3) 
frame1.grid(column=5,columnspan=11, row=0, rowspan=3)

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

 def create_page(db_list_:list,s:int):
  if db_list_!=[] and db_list_!=None:
      
    for note in db_list_:
     try:
      context0="Pubkey "+note['pubkey']+"\n"
      if note['tags']!=[]:
        context1="Content lenght "+str(len(note["content"]))+"\n"+"kind "+str(note["kind"])+"\n"
        context2="\n"
        if tags_string(note,"title")!=[]: 
         xnote= "Title: "+str(tags_string(note,"title")[0])
         context2=context2+str(xnote) +"\n"
        else: 
         context1="there is no Title"+ " kind "+str(note["kind"])
         context2=""
        if tags_string(note,"summary")!=[] and str(tags_string(note,"summary")[0])!="": 
          xnote= "\n"+"Summary: "+str(tags_string(note,"summary")[0])
          context2=context2+str(xnote) +"\n"
      else:
          context1="no tags"+ " kind "+str(note["kind"])
          context2=""   
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0+context1+context2)
      label_id.grid(pady=2,column=0, columnspan=3)

      def print_id(entry):
           
           number=list(db_list_note).index(entry)
           print(number)
           show_print_test(entry)     

      def print_fork(entry):
         number=list(db_list_note).index(entry)
         print(number)
         show_fork_test(entry)       
                          
      def print_var(entry):
                print(entry["content"])
                          
      button=Button(scrollable_frame_1,text=f"Print me ", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"Highlight it ", command=lambda val=note: print_fork(val))
      button_grid2.grid(row=s,column=2,padx=5,pady=5) 
      button_grid3=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
      button_grid3.grid(row=s,column=1,padx=5,pady=5)      
   
      s=s+2  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.35,rely=0.3,relwidth=0.30,relheight=0.4)
    
    def close_number() -> None :
        frame2.destroy()    
        button_f_close.place_forget()
        
    button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"),fg="red")
    button_f_close.place(relx=0.63,rely=0.24)      
       
 s=1
 create_page(db_list_note, s)
 root.update_idletasks()

frame_3=tk.Frame(root,height=20,width=80) 
frame_id=tk.Frame(frame_3,height=30,width= 100)  
frame_T=tk.Frame(frame_3,height=20,width= 30)      
button_id=tk.Button(root,command=show_Teed,text="Go Result")
button_id.place(relx=0.35,rely=0.25)
frame_T.grid(column=0, row=1, columnspan=2)
frame_id.grid(column=2, row=1, columnspan=4, rowspan=3)
frame_3.grid()

def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def show_fork_test(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = ttk.Frame(canvas_2)

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")
    )
)

   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
   
   scroll_bar_f = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_f.grid( sticky = NS,column=4,row=0,rowspan=3)
   second_labelf = tk.Text(scrollable_frame_2, padx=2, height=12, width=37, yscrollcommand = scroll_bar_f.set, font=('Arial',12,'bold'))
   scroll_bar_f.config( command = second_labelf.yview )
   second_labelf.insert(END,note["content"],str)
   second_labelf.grid(padx=2, column=0, columnspan=3, row=0) 
   context0="npub: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
   if note['tags']!=[]:
        if tags_string(note,"title")!=[]: 
            context1 = "\n"+"Title: "+str(tags_string(note,"title")[0])
        
            context2="\n"+"d: "+str(tags_string(note,"d")[0])
   else: 
        context1="content: "+"\n"+note['content']+"\n"
        context2=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   var_id.set(context0+context1+context2)
   label_id.grid(pady=2,column=0, columnspan=4,padx=5)
      
   def print_zap(entry):
            if second_labelf.get("1.0",END)!="":
               value=print_var(entry)
               if value:
                  print(value)
                  corny_book(entry,value)
               
   def print_var(entry):
     
      try:
       second_labelf.tag_configure("warning", background="yellow", foreground="blue",underline=True)
       sel_start,sel_end=second_labelf.tag_ranges("sel")
       if sel_start and sel_end:
        selected_text = second_labelf.get(sel_start, sel_end)
        
        
        if selected_text in entry["content"]:
            
            second_labelf.tag_add("warning",sel_start, sel_end)    
            return selected_text
        
       else:
         print("no") 
      except ValueError as e:
        print(e)  
   
   button=Button(scrollable_frame_2,text=f"highlight test ", command=lambda val=note: print_var(val))
   button.grid(row=s,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Send event", command=lambda val=note: print_zap(val))
   button_grid2.grid(row=s,column=1,padx=5,pady=5)
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()  
     button_frame.place_forget()

   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.02,rely=0.15)
   frame3.place(relx=0.01,rely=0.2,relwidth=0.31,relheight=0.4 ) 

def show_print_test(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = ttk.Frame(canvas_2)

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")
    )
)

   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
   context0="npub: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
   if note['tags']!=[]:
        if tags_string(note,"title")!=[]: 
         xnote= "\n"+"Title: "+str(tags_string(note,"title")[0])
         context1=xnote+"\n"+"\n"+note['content']+"\n"
        else: 
            context1="\n"+note['content']+"\n" 
        context2="\n"+"[[ Tags ]]"+"\n"
        for tags_note in note["tags"]:
           context2=context2+str(tags_note)+"\n" 
   else: 
        context1="content: "+"\n"+note['content']+"\n"
        context2=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   var_id.set(context0)
   label_id.grid(pady=2,column=0, columnspan=3,padx=5)
   scroll_bar_1 = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_1.grid( sticky = NS,column=4,row=s+1,rowspan=3)
   second_label2 = tk.Text(scrollable_frame_2, padx=2, height=5, width=35, yscrollcommand = scroll_bar_1.set, font=('Arial',12,'bold'))
   scroll_bar_1.config( command = second_label2.yview )
   second_label2.insert(END,context1+context2,str)
   second_label2.grid(padx=2, column=0, columnspan=3, row=s+1) 
      
   def print_tags(entry):
            print(entry["tags"])
            

   def print_var(entry):
            print(entry["id"])
   
   def print_content(entry):
       result=show_note_from_id(entry)
       if result!=None: 
        z=s+3
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             context00="npub: "+jresult['pubkey']+"\n"+"id: "+jresult["id"]+"\n"
             if jresult['tags']!=[]:
              context11="\n"+jresult['content']+"\n"
              context22="[-[-[Tags]-]-]"+"\n"+str((jresult)["tags"])
             else: 
              context11=jresult['content']+"\n"
              context22=""
             var_id_1=StringVar()
             label_id_1 = Message(scrollable_frame_2,textvariable=var_id_1, relief=RAISED,width=310,font=("Arial",12,"normal"))
             var_id_1.set(context00)
             label_id_1.grid(pady=2,column=0, columnspan=3,padx=5,row=z)
             scroll_bar_2 = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_2.grid( sticky = NS,column=4,row=z+1)
             second_label4 = tk.Text(scrollable_frame_2, padx=2, height=5, width=35, yscrollcommand = scroll_bar_2.set, font=('Arial',12,'bold'))
             scroll_bar_2.config( command = second_label4.yview )
             second_label4.insert(END,context11+context22,str)
             second_label4.grid(padx=2, column=0, columnspan=3, row=z+1) 
             z=z+2
                   
   button=Button(scrollable_frame_2,text=f"id ", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
   button_grid3=Button(scrollable_frame_2,text=f"Tags ", command=lambda val=note: print_tags(val))
   button_grid3.grid(row=s+2,column=1,padx=5,pady=5) 
   button_grid3=Button(scrollable_frame_2,text=f"this a reply ", command=lambda val=note: print_content(val))
   button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()  
     button_frame.place_forget()

   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.9,rely=0.12)
   frame3.place(relx=0.67,rely=0.17,relwidth=0.33,relheight=0.4 ) 

def db_list_id(json_list):
    db_list_with_id=[]
    for json_z in json_list:
        if json_z["id"] not in db_list_with_id:
          db_list_with_id.append(json_z["id"]) 
    return db_list_with_id       

def db_list_nota(nota_id):
    #global list
    for nota_x in db_list:
        if nota_x["id"]==nota_id:
            return nota_x

def show_note_from_id(note):
        result=note["id"]
        quote_e=nota_reply_id(note)
        
        replay_light=[]
        db_already=[]
        items=[]
        if quote_e!=[]:
           for replay_x in quote_e:
               if replay_x not in db_list_id(db_list):
                  replay_light.append(replay_x) 
               else:
                   db_already.append(replay_x)
           if replay_light!=[]:          
            items=get_note(asyncio.run(Get_event_id(replay_light)))
           if db_already!=[]:
               for db_x in db_already:
                   if db_x  in db_list_id(db_list):
                    items.append(db_list_nota(db_x)) 
        else:
            print("quote_e empty")
            items=get_note(asyncio.run(Get_event_id(result)))
             
        for itemsj in items:
            if itemsj not in db_list:
                db_list.append(itemsj)   
        return items   

def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id                

def get_note(z):
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f

def evnt_id(id):
    try: 
     test2=EventId.parse(id)
     return test2
    except NostrSdkError as e:
       print(e,"input ",id)

def evnts_ids(list_id):
     Event=[]
     for j in list_id:
        if evnt_id(j):
         Event.append(evnt_id(j))
     return Event       

async def get_answers_Event(client, event_):
    f = Filter().events(evnts_ids(event_)).kinds([Kind(1),Kind(1111)]).limit(int(10*len(event_)))
    
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_one_Event(client, event_):
    f = Filter().id(evnt_id(event_))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_answer_Event(client, event_):
    f = Filter().event(evnt_id(event_)).kinds([Kind(1),Kind(1111)]).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_notes_(client, e_ids):
     f = Filter().ids([EventId.parse(e_id) for e_id in e_ids])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec()]
     return z

async def get_one_note(client, e_id):
    f = Filter().id(EventId.parse(e_id))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_event_id(e_id):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.add_relay(RelayUrl.parse("wss://purplerelay.com/"))
    
    await client.connect()
    
    await asyncio.sleep(2.0)

    if isinstance(e_id, list):
         print("list")
         test_id = await get_notes_(client,e_id)
         resp_answer=await get_answers_Event(client,e_id)
         if resp_answer!=[]:
          for resp in resp_answer:
            if resp not in test_id:
             test_id.append(resp)
    else:
        print("str")
        test_id = await get_one_note(client,e_id)
        resp_answer=await get_answer_Event(client, e_id)
        if resp_answer!=[]:
         for resp in resp_answer:
          if resp not in test_id:
           test_id.append(resp)
    return test_id

frame2=Frame(root)
db_list=[]

def add_db_list():
        
        Frame_2=Frame(root)
        Frame_block=Frame(Frame_2,width=50, height=20)
               
        def Close_block(event):
            Frame_block.destroy()
            Frame_2.place_forget()
        
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=17, row=1, padx=5, columnspan=1) 
        
    
        def search_block_list():
            label_string_block1.set(len(db_list_note))    

        def delete_block_list():
            db_list_note.clear()
            label_string_block1.set(len(db_list_note))    
    
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey")
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ")
        random_block1.grid(column=1,row=0,padx=5,pady=5)
        label_string_block1=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1)
        label_block_list1.grid(column=1,row=1,pady=5)
        Frame_block.grid(column=0,row=6, columnspan=3, rowspan=2)
        Frame_2.place(relx=0.75,rely=0.05)

button_block=tk.Button(root, highlightcolor='WHITE',text='DB count',font=('Arial',12,'bold'),command=add_db_list)
button_block.place(relx=0.68,rely=0.05) 
frame2.grid(column=0, row=0,columnspan=3, rowspan=4,pady=10)

def note_to_naddr(note,relay):
    coord = Coordinate(Kind(note["kind"]),PublicKey.parse(note["pubkey"]),str(tags_string(note,"d")[0]))
    if coord.verify()==True:
     coordinate = Nip19Coordinate(coord, [RelayUrl.parse(relay)])
     return coordinate.to_bech32()
    else:
       return None


async def stick_note(tag,high_note):
   try:
    init_logger(LogLevel.INFO)
  
    key_string=log_these_key()
    if key_string!=None: 
     keys = Keys.parse(key_string)
     signer=NostrSigner.keys(keys)
     client = Client(signer)
     signer=NostrSigner.keys(keys)
     client = Client(signer)
     
     for rel_x in relay_search_list:
       await client.add_relay(RelayUrl.parse(rel_x))
            # Add relays and connect
     await client.add_relay(RelayUrl.parse("wss://relayb.uid.ovh/"))
     await client.add_relay(RelayUrl.parse("wss://relay.chatbett.de/"))
    
     await client.connect()
     
     builder = EventBuilder(Kind(9802),high_note).tags(tag)
    
     await client.send_event_builder(builder)
        
     await asyncio.sleep(2.0)

     f = Filter().authors([keys.public_key()]).kind(Kind(9802))
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     for event in events.to_vec():
      print(event.as_json())
   except TypeError as e:
      print(e)  
        
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

def share_note(entry:dict):
    pubkey_note.set(entry["pubkey"])
    id_note.set(str(entry["id"]))
    a_coordinate=note_to_naddr(entry,relay_search_list[0])
    p_show()
    e_show()
    if a_coordinate:
       a_string.set(a_coordinate)
       a_show()
    print(list_a,list_e,list_p)   

def corny_book(entry,value):
   share_note(entry)
   check_square()
   note=value
   lists_id=[] 
   if button_entry1.cget('foreground')=="green":
    
      if list_e!=[]:  
        for xlist in list_e:
          
            lists_id.append(Tag.from_standardized(TagStandard.EVENT_TAG(xlist,RelayUrl.parse(relay_search_list[0]),None,None,FALSE)))
            
      if list_a!=[]:        
        for jlist in list_a:
            lists_id.append(Tag.from_standardized(TagStandard.COORDINATE_TAG(Coordinate.parse(jlist),RelayUrl.parse(relay_search_list[0]),FALSE)))
            
      
      if list_p!=[]:        
        for alist in list_p:
            lists_id.append(Tag.from_standardized(TagStandard.PUBLIC_KEY_TAG(PublicKey.parse(alist),RelayUrl.parse(relay_search_list[0]),None,FALSE)))       
                  
    
      if __name__ == '__main__':
         
         asyncio.run(stick_note(lists_id,note))
        
         button_entry1.config(text="■",foreground="grey")
         list_p.clear()
         list_e.clear()
         list_a.clear()
         e_view.config(text="")  
         a_view.config(text="Article:")
         r_view.config(text="link:")
         p_view.config(text="")
         error_label.config(text="Problem:")
         print_label.config(text="Wait for the highlights", font=("Arial",12,"bold"),foreground="black")

def check_square():
    if list_e!=[] or list_a!=[]:
       
        print_label.config(text="Quote ", font=("Arial",12,"bold"),foreground="blue")
        button_entry1.config(text="■",foreground="green")
        error_label.config(text="ok")
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for Tag", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")
        
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
button_entry1.place(relx=0.64,rely=0.03,relwidth=0.05, relheight=0.1,anchor="n" )
frame_1=tk.Frame(root,height=100,width=200, background="darkgrey")
error_label = tk.Label(frame_1, text="Problem:",font=("Arial",12))
error_label.grid(column=2, rowspan=2, row=0, pady=5,padx=5)
print_label = ttk.Label(frame_1, text="Wait for the label",font=("Arial",12))
print_label.grid(column=2, columnspan=2, row=2, pady=5,padx=10)

frame_1.grid(column=18,columnspan=5, row=0, rowspan=3)
Check_raw =IntVar()
e_tag = tk.Label(root, text="e-Tag",font=("Arial",12,"bold"))
id_note=StringVar()
e_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12),textvariable=id_note)
pubkey_note = StringVar()
p_tag = tk.Label(root, text="p-Tag",font=("Arial",12,"bold"))
entryp_tag=ttk.Entry(root,justify='left',font=("Arial",12),textvariable=pubkey_note)
p_view = tk.Label(root, text="p tag?: ", font=("Arial",12))

Checkbutton8 = IntVar() 
Type_band = Checkbutton(root, text = "More p tag", variable = Checkbutton8, onvalue = 1, offvalue = 0, height = 2, width = 10,font=('Arial',16,'normal'))
 
def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        button_close.place(relx=0.8,rely=0.15)
        e_tag.place(relx=0.7,rely=0.21,relwidth=0.1 )
        e_tag_entry.place(relx=0.7,rely=0.25,relwidth=0.2)
        e_button.place(relx=0.7,rely=0.30)
        e_view.place(relx=0.77,rely=0.30,relwidth=0.2 )
        p_tag.place(relx=0.1,rely=0.75,relwidth=0.1 )
        Type_band.place(relx=0.29,rely=0.77,relwidth=0.1,relheight=0.05,anchor='e')  
        p_view.place(relx=0.22,rely=0.85,relwidth=0.1 )
        p_button.place(relx=0.1,rely=0.85)
        a_tag.place(relx=0.7,rely=0.41,relwidth=0.1)
        entry_a.place(relx=0.7,rely=0.45,relwidth=0.2 )
        a_button.place(relx=0.7,rely=0.50,relwidth=0.1)
        a_view.place(relx=0.85,rely=0.5)
        r_tag.place(relx=0.7,rely=0.55,relwidth=0.1 )
        r_summary.place(relx=0.7,rely=0.6,relwidth=0.2 )
        r_button.place(relx=0.7,rely=0.65,relwidth=0.1)
        r_view.place(relx=0.7,rely=0.7,relwidth=0.3)
        entryp_tag.place(relx=0.1,rely=0.8,relwidth=0.2 )

   else:
    Check_raw.set(0) 
    e_tag.place_forget()
    e_tag_entry.place_forget()
    e_button.place_forget()
    e_view.place_forget()
    p_tag.place_forget()
    Type_band.place_forget() 
    p_view.place_forget()
    p_button.place_forget()    
    a_tag.place_forget()
    entry_a.place_forget()
    a_button.place_forget()
    a_view.place_forget()
    r_tag.place_forget()
    r_summary.place_forget()
    r_button.place_forget()
    r_view.place_forget()
    entryp_tag.place_forget()
    button_close.place_forget()

button_close=Button(root, background='red', text='❌',font=('Arial',12,'bold'), command=raw_label)    
lab_button = tk.Button(root, text="Open Tag", font=("Arial",12,"bold"), command=raw_label)
lab_button.place(relx=0.8,rely=0.05)      

list_p=[]

def p_show():
    title=entryp_tag.get()
    
    if len(title)==64:
       
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
                list_p.append(title)
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END) 
                return list_p
          else:
                list_p.append(title)
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

list_e=[]

def e_show():
    title=e_tag_entry.get()
    print(title)
    if len(title)==64:
       
        if evnt_id(title):
         if title not in list_e:
          list_e.append(evnt_id(title))
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
          return list_e    
       
list_a=[]

def a_show():
    a_tag_entry=entry_a.get()
    if a_tag_entry!="":
      try:  
        event_kind = Coordinate.parse(a_tag_entry).kind()
        event_identifier = Coordinate.parse(a_tag_entry).identifier()
        event_publickey = Coordinate.parse(a_tag_entry).public_key()
        
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
            
list_r=[]      

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
                
e_button = tk.Button(root, text="e_show", font=("Arial",12,"bold"), command=e_show)
e_view = tk.Label(root, text="e tag?: ", font=("Arial",12))

a_tag = tk.Label(root, text="a-Tag",font=("Arial",12,"bold"))
a_string=StringVar()
entry_a=ttk.Entry(root,justify='left',font=("Arial",12),textvariable=a_string)
a_button = tk.Button(root, text="a tag", font=("Arial",12,"bold"), command=a_show)
a_view = tk.Label(root, text="Article: ", font=("helvetica",13,"bold"),justify="center")

r_tag = tk.Label(root, text="r-Tag",font=("Arial",12,"bold"))
r_summary=ttk.Entry(root,justify='left',font=("Arial",12))
r_button = tk.Button(root, text="R tag", font=("Arial",12,"bold"), command=r_show)
r_view = tk.Label(root, text="link: ", font=("helvetica",13,"bold"),justify="center")

import requests
import shutil
from PIL import Image, ImageTk

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
   
#Parse id in note
str_test=StringVar()
entry_note=ttk.Entry(root,justify='left', textvariable=str_test)
entry_note.place(relx=0.13,rely=0.66,relwidth=0.1, anchor="n")

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

async def get_list_Event(client, event_):
    tag_event=[]
    if event_!=[]:
     for event in event_:
       tag_event.append(EventId.parse(event))
     f = Filter().ids(tag_event)
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec()]
     return z

async def get_one_Event(client, event_):
    f = Filter().id(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

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

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_url_list!=[]:
       
       for jrelay in relay_url_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
     await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
     await client.add_relay(RelayUrl.parse("wss://relay.primal.net"))
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(event_, list):
      test_kind=await get_list_Event(client, event_)
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

event_idone=Button(root,text="Search event one", font=('Arial',12,'normal'),command=reply_event ) 
event_idone.place(relx=0.25,rely=0.65,anchor='n' )

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
            if xrelay not in relay_url_list:
               relay_url_list.append(xrelay)
         return decode_nevent.event_id().to_hex()
         
label_var=StringVar()
label_entry=ttk.Entry(root,justify='left',textvariable=label_var,font=("Arial",12))
Check_lab_entry =IntVar(root,0,"raw_lab")
List_note_write=[]

async def Search_status(client:Client,list_relay_connect:list):
    try: 
        if list_relay_connect!=[]:
            for relay_y in list_relay_connect:
                await client.add_relay(RelayUrl.parse(relay_y))
            await client.connect()
            relays = await client.relays()
            await asyncio.sleep(1.0)   
            for url, relay in relays.items():
                i=0
                while i<2:   
            
                    print(f"Relay: {url}")
                    print(f"Connected: {relay.is_connected()}")
                    print(f"Status: {relay.status()}")
                    stats = relay.stats()
                    print("Stats:")
                    print(f"    Attempts: {stats.attempts()}")
                    print(f"    Success: {stats.success()}")
                    
                    if i==1:
                        if stats.bytes_received()>0:  #Auth ort other stuff
                           if str(url) in list_relay_connect:
                            list_relay_connect.remove(str(url))
                            break
                        if stats.success()==0 and relay.is_connected()==False:
                            if str(url) in list_relay_connect:
                                list_relay_connect.remove(str(url))
                        
                    i=i+1 
    except IOError as e:
        print(e) 
    except ValueError as b:
        print(b)                   

root.mainloop()