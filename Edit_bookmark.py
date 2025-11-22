#edit 30003
from nostr_sdk import *
import asyncio
from datetime import timedelta
from nostr_sdk import PublicKey
from nostr_sdk import Tag
from nostr_sdk import EventId,Event
import time
from datetime import datetime
import uuid
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import json
import io
from tkinter.filedialog import askopenfilename
from cryptography.fernet import Fernet

root = tk.Tk()
root.title("Edit Bookmark")
root.geometry("1300x800")
relay_list=[]
db_list_note=[]
public_list=[]

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

def since_day(number):
    import datetime
    import calendar
    date = datetime.date.today() - datetime.timedelta(days=number)
    t = datetime.datetime.combine(date, datetime.time(1, 2, 1))
    z=calendar.timegm(t.timetuple())
    #print(z)
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
        
frame1.grid(column=5,columnspan=11, row=0, rowspan=3)

async def get_result_w(client):
   try: 
    if Checkbutton5.get() == 1:
          f = Filter().author(public_list[0]).kind(Kind(30003)).since(timestamp=Timestamp.from_secs(since_day(int(since_entry.get())))).until(timestamp=Timestamp.from_secs(since_day(int(until_entry.get())))).limit(10)
    else:
           f = Filter().author(public_list[0]).kind(Kind(30003)).limit(10)

    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z
   except TypeError as e:
      print(e, " probably public list is empty")

async def Search_d_tag():
      
    # Add relays and connect
    if relay_list!=[]:
       client = Client(None)
       for jrelay in relay_list:
          await client.add_relay(RelayUrl.parse(jrelay))
       await client.connect()
       await asyncio.sleep(2.0)
       await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
       if public_list!=[]:
        combined_results = await get_result_w(client)
        return combined_results
    # Init logger
    init_logger(LogLevel.INFO)
    client = Client(None)
     
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.connect()
    await search_box_relay()
    print("found ", len(relay_list), " relays")

def call_text():
  if relay_list!=[]:
   if __name__ == "__main__":
    response=asyncio.run(Search_d_tag())
    if response:

     note_=get_note(response)
     for jnote in note_:
       if jnote not in db_list_note:
          db_list_note.append(jnote)
       if jnote["content"]!="":
          pass
       else: 
             second_label10.insert(END,str("- Kind ")+str(jnote["kind"])+"\n")
             second_label10.insert(END,str(jnote["tags"]))
             button_id.place(relx=0.36,rely=0.24)
       second_label10.insert(END,"\n"+"____________________"+"\n")
       second_label10.insert(END,"\n"+"\n")

    else:
       print("empty")
  else: 
              
          if __name__ == "__main__":
            response=asyncio.run(Search_d_tag())
          if len(relay_list)>0:
             button_close_search["text"]="🔍 Bookmarks"
          else:
             if response!=None:
                print(str(len(response)),"\n",response[0]) 

button_close_search=tk.Button(root, text='Search Relay',font=('Arial',12,'bold'), command=call_text)    
button_close_search.place(relx=0.5,rely=0.1 ) 
p_tag = tk.Label(root, text="Pubkey",font=("Arial",12,"bold"))
entryp_tag=ttk.Entry(root,justify='left',font=("Arial",12),)
p_tag.place(relx=0.05,rely=0.35,relwidth=0.1 )
entryp_tag.place(relx=0.05,rely=0.4,relwidth=0.1 )
p_view = tk.Label(root, text="", font=("Arial",12))
p_view.place(relx=0.15,rely=0.35,relwidth=0.1 )

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
p_button.place(relx=0.16,rely=0.39)

def Clear_pubkey():
   public_list.clear()
   p_view.config(text="")

p_clear_button = tk.Button(root, text="x", font=("Arial",12,"bold"), command=Clear_pubkey)
p_clear_button.place(relx=0.25,rely=0.39)

async def get_outbox_relay(client):
   if public_list!=[]:
    f=Filter().authors(public_list).kind(Kind(10002))
   else: 
    f=Filter().kind(Kind(10002)).reference("wss://nos.lol/").limit(50)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec()]
   return z

async def search_box_relay():
        
    client = Client(None)
    
    if relay_list!=[]:
       #print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(RelayUrl.parse(jrelay))
             
    else:
       await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
       await client.add_relay(RelayUrl.parse("wss://purplerelay.com/"))
    await client.connect()
    relay_add=get_note(await get_outbox_relay(client))
    if relay_add !=None and relay_add!=[]:
           i=0
           while i<len(relay_add):
            for xrelay in tags_string(relay_add[i],'r'):
             
              if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay not in Bad_relay_connection:
               if xrelay not in relay_list:
                if len(relay_list)<10:
                 relay_list.append(xrelay) 
              
            i=i+1             

Bad_relay_connection=["wss://relay.noswhere.com/","wss://relay.purplestr.com/","wss://relay.nostr.band/","wss://relay.momostr.pink/","wss://relay.phoenix.social/","wss://nostr.fmt.wiz.biz/"]
scroll_bar_mini = tk.Scrollbar(frame1)
scroll_bar_mini.grid( sticky = NS,column=4,row=0,rowspan=3)
second_label10 = tk.Text(frame1, padx=10, height=5, width=25, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'))
scroll_bar_mini.config( command = second_label10.yview )
second_label10.grid(padx=10, column=1, columnspan=3, row=0, rowspan=3) 

def show_Teed():
 frame2=tk.Frame(root)  
 canvas_1 = tk.Canvas(frame2)
 scrollbar_1 = ttk.Scrollbar(frame2, orient="vertical", command=canvas_1.yview)
 scrollable_frame_1 = ttk.Frame(canvas_1)

 scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all")
    )
)

 canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")

 canvas_1.configure(yscrollcommand=scrollbar_1.set)

 def create_page(db_list_:list,s:int):
  if db_list_!=[] and db_list_!=None:
      
    for note in db_list_:
     try:
      context0="Pubkey "+note['pubkey']+"\n"
      if note['tags']!=[]:
        context1="Number of cards "+str(len(tags_string(note,"e")))+"\n"+"kind "+str(note["kind"])+"\n"
        context2=""
        if tags_string(note,"title")!=[]: 
         xnote= "Title: "+str(tags_string(note,"title")[0])+"\n"
         context2=context2+str(xnote) 
        else: 
         context1="there is no Title"+ " kind "+str(note["kind"])
         context2=""
        if tags_string(note,"description")!=[]: 
         xnote= "- Description: "+str(tags_string(note,"description")[0])+"\n" 
         context2=context2+str(xnote) 
        if tags_string(note,"summary")!=[]:
          if str(tags_string(note,"summary")[0])!="": 
           xnote= "\n"+"- Summary: "+str(tags_string(note,"summary")[0])+"\n"
           context2=context2+str(xnote) 
      else:
          context1="no tags"+ " kind "+str(note["kind"])
          context2=""   
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0)
      label_id.grid(pady=2,column=0, columnspan=3, row=s)
      scroll_bar_mini_2 = tk.Scrollbar(scrollable_frame_1)
      scroll_bar_mini_2.grid( sticky = NS,column=4,row=s+1,pady=5)
      second_label_2 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini_2.set, font=('Arial',14,'bold'),background="#D9D6D3")
      second_label_2.insert(END,context1+"\n"+str(context2))
      scroll_bar_mini_2.config( command = second_label_2.yview )
      second_label_2.grid(padx=10, column=0, columnspan=3, row=s+1) 
         
      def print_id(entry):
           
           number=list(db_list_note).index(entry)
           print(number)
           show_print_test(entry)     

      def print_edit(entry):
         number=list(db_list_note).index(entry)
         print(number)
         show_edit_test(entry)       
                          
      def print_var(entry):
                if entry["content"]!="":
                  print(entry["content"])
                else:
                   print(entry)  
       
      button=Button(scrollable_frame_1,text=f"Content", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s+2,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"EDIT it ", command=lambda val=note: print_edit(val))
      button_grid2.grid(row=s+2,column=2,padx=5,pady=5) 
      button_grid3=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
      button_grid3.grid(row=s+2,column=1,padx=5,pady=5)      
      s=s+3  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.35,rely=0.32,relwidth=0.30,relheight=0.4)
    
    def close_frame():
        frame2.destroy()    
        #button_frame.place_forget()
        button_f_close.place_forget()
       
    def close_number() -> None :
        frame2.destroy()    
        #button_frame.place_forget()
        button_f_close.place_forget()
        
    button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"))
    button_f_close.place(relx=0.6,rely=0.24)      
              
 s=1
 create_page(db_list_note, s)
 root.update_idletasks()

frame_3=tk.Frame(root,height=20,width=80) 
frame_id=tk.Frame(frame_3,height=30,width= 100)  
frame_T=tk.Frame(frame_3,height=20,width= 30)      
button_id=tk.Button(root,command=show_Teed,text="Bookmarks",font=('Arial',12,'bold'))
frame_T.grid(column=0, row=1, columnspan=2)
frame_id.grid(column=2, row=1, columnspan=4, rowspan=3)
frame_3.grid()
new_list_e=[]

def e_show_new():
    title_e=e_tag_entry.get()
    title=event_string_note(title_e)
    if title!=None:
     if len(title)==64:
       
        if evnt_id(title)!=None:
         if title not in list_e and title not in new_list_e:
          new_list_e.append(title)
          e_view.config(text=str(len(new_list_e)))
          e_tag_entry.delete(0, END) 
          return new_list_e
          
         else:
              print("already present")
              e_view.config(text=str(len(new_list_e)))
              e_tag_entry.delete(0, END) 
              return new_list_e
        else:
         print("event_id")
         e_view.config(text=str(len(new_list_e)))
         e_tag_entry.delete(0, END)    
        
    else:
          
          e_tag_entry.delete(0, END) 
          return new_list_e  

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

e_tag = tk.Label(root, text="e-Tag",font=("Arial",12,"bold"))
e_string_var=StringVar()
e_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12),textvariable=e_string_var)
e_button = tk.Button(root, text="add", font=("Arial",12,"bold"), command=e_show_new)
e_view = tk.Label(root, text="e tag?: ", font=("Arial",12))

def show_edit_test(note):
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
   
   e_button.place(relx=0.82,rely=0.1)
   e_view.place(relx=0.7,rely=0.19)
   e_tag.place(relx=0.7,rely=0.1 )
   e_tag_entry.place(relx=0.68,rely=0.15,relwidth=0.2)
  

   context0="npub: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
   context1="content: "+"\n"+note['content']+"\n"
   context2=""
   if note['tags']!=[]:
        if tags_string(note,"title")!=[]: 
            context1 = "\n"+"Title: "+str(tags_string(note,"title")[0])
        
            context2="\n"+"d: "+str(tags_string(note,"d")[0])
   
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   var_id.set(context0+context1+context2)
   label_id.grid(pady=2,column=0, columnspan=3)
      
   def print_zap(entry):
           if button_grid2.cget('foreground')=="green":  
            tags,uid,list_e=edit_note(entry)
            lists_id=[]
            list_id=[]
            if list_e!=[]:
               for xlist in list_e:
                if xlist not in list_id:
                 list_id.append(xlist)
                 lists_id.append(EventId.parse(xlist)) 
            if new_list_e!=[]:
               for jlist in new_list_e:
                  if jlist not in list_id:
                   list_id.append(jlist)
                   lists_id.append(EventId.parse(jlist))
               bookmark_e=Bookmarks(event_ids=lists_id)
              
               test=asyncio.run(edit_can_book(bookmark_e,entry["pubkey"],uid,tags))
               if test:
                button_grid2.config(fg="grey")
                close_frame()
               else:
                  print("error") 
                  button_grid2.config(fg="grey")
                  close_frame()

   def print_var(entry):
            print(edit_note(entry))
            global d_identifier
            d_identifier=url_uid
            button_grid2.config(fg="green")

   def print_content(entry):
      reply_re_action(entry)
                  
   button=Button(scrollable_frame_2,text=f"Edit test ", command=lambda val=note: print_var(val))
   button.grid(row=s,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Send event", command=lambda val=note: print_zap(val))
   button_grid2.grid(row=s,column=1,padx=5,pady=5)
   button_grid3=Button(scrollable_frame_2,text=f"like this ", command=lambda val=note: print_content(val))
   button_grid3.grid(row=s,column=2,padx=5,pady=5)    
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()  
     button_frame.place_forget()
     e_button.place_forget()
     e_view.place_forget()
     e_tag.place_forget()
     e_tag_entry.place_forget()
     e_view.config(text="e tag?: ")
     new_list_e.clear()
   
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.91,rely=0.15)
   frame3.place(relx=0.65,rely=0.22,relwidth=0.33,relheight=0.4 ) 

def reply_re_action(note):
  
   test = EventId.parse(note["id"])
   public_key=convert_user(note["pubkey"])
   if __name__ == '__main__':
    note_rea="+"
    type_event=Kind(int(note["kind"]))
    asyncio.run(reply_reaction(test,public_key,note_rea,type_event))    

async def reply_reaction(event_id,public_key,str_reaction,type_event):
  key_string=log_these_key()
  if key_string!=None: 
    keys = Keys.parse(key_string)
    signer = NostrSigner.keys(keys)
    
    client = Client(signer)
    # Add relays and connect
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(RelayUrl.parse(jrelay))
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
    await client.connect()

    # Send an event using the Nostr Signer
    builder = EventBuilder.reaction_extended(event_id,public_key,str_reaction,type_event)
    test_note=await client.send_event_builder(builder)
    print("this relay is going good", test_note.success, "\n", "this relay is bad",test_note.failed)

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
   context0="npub: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
   if note['tags']!=[]:
        if tags_string(note,"title")!=[]: 
         xnote= "\n"+"Title: "+str(tags_string(note,"title")[0])
         context1=xnote+"\n"+"\n"+note['content']+"\n"
        else: 
            context1="\n"+note['content']+"\n" 
        context2="[-[-[Tags]-]-]"+"\n"
        for tags_note in (note)["tags"]:
           context2=context2 +"\n"+str(tags_note)
   else: 
        context1="content: "+"\n"+note['content']+"\n"
        context2=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
   var_id.set(context0)
   label_id.grid(pady=2,column=0, columnspan=3,row=s)
   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid(sticky="ns", column=4,row=s+1,pady=10)
   second_label_10 = tk.Text(scrollable_frame_2, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   second_label_10.insert(END,context1+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label_10.yview )
   second_label_10.grid(padx=10, column=0, columnspan=3, row=s+1)    
   
   def print_zap(entry):
            print("pubkey ",entry["pubkey"])
            
   def print_var(entry):
            print("id ", entry["id"])
  
   button=Button(scrollable_frame_2,text=f"id ", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Pubkey", command=lambda val=note: print_zap(val))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
  
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()  
     button_frame.place_forget()

   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.9,rely=0.16)
   frame3.place(relx=0.65,rely=0.22,relwidth=0.35,relheight=0.4 ) 

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
        
def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id                

frame2=Frame(root)
db_list=[]

def add_db_list():
        
        Frame_2=Frame(root)
        Frame_block=Frame(Frame_2,width=50, height=20)
        stuff_db = ttk.LabelFrame(Frame_2, text="DB", labelanchor="n", padding=10)
        stuff_db.grid(column=0,row=0, columnspan=3, rowspan=2)

        def Close_block(event):
            Frame_block.destroy()
        
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=17, row=1, padx=5, columnspan=1) 
       
        def search_block_list():
            label_string_block1.set(len(db_list_note))    

        def delete_block_list():
            db_list_note.clear()
            label_string_block1.set(len(db_list_note))    
    
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey",font=('Arial',12,'bold'))
        clear_block.grid(column=0,row=0,padx=2,pady=5)    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ",font=('Arial',12,'bold'))
        random_block1.grid(column=1,row=0,padx=2,pady=5)
        label_string_block1=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1,font=('Arial',12,'bold'))
        label_block_list1.grid(column=1,row=1,pady=5)
        Frame_block.grid(column=0,row=6, columnspan=3, rowspan=2)
        Frame_2.place(relx=0.05,rely=0.23)

button_block=tk.Button(root, highlightcolor='WHITE',text='DB count',font=('Arial',12,'bold'),command=add_db_list)
button_block.place(relx=0.02,rely=0.05) 
frame2.grid(column=0, row=0,columnspan=3, rowspan=4,pady=10)
published_at=""
list_e=[]

class edit_json:
    def __init__(self,json_note:dict):
        self.json_note=json_note
        
    def __str__(self):
        return f"{self.json_note}"
    def my_func(abc):
        print("hello my tag is "+ abc.json_note)
    def __list__(self):
       list_to_tag=[]
       #if self.count():
       for tags_note in self.json_note["tags"]:
        if tags_note[0]=="d":
         global url_uid  
         url_uid = str(tags_note[1])
        if tags_note[0]=="title":
         global title
         title= str(tags_note[1])  
        if tags_note[0]=="e":
         global list_e
         if tags_note[1]not in list_e:
          list_e.append(tags_note[1])   
        if tags_note[0]=="published_at":
         global published_at
         published_at= str(tags_note[1])  
           
       return url_uid,title,list_e,published_at

def edit_note(note_ex):
    test = edit_json(note_ex)               
    url_uid,title,list_e,published_at=test.__list__()
    tag_id=str(note_ex["kind"])+str(":")+str(note_ex["pubkey"])+str(":")+url_uid.lower()
    if Coordinate.parse(tag_id).verify()==True:
            if published_at=="": 
                       if title!="":
                        tags=Tag.custom(TagKind.PUBLISHED_AT() , [str((note_ex["created_at"]) )]),Tag.custom(TagKind.TITLE(), [title])
                       else:
                        tags=Tag.custom(TagKind.PUBLISHED_AT() , [str((note_ex["created_at"]) )])   
            else: 
               if title!="":
                  tags=Tag.custom(TagKind.PUBLISHED_AT() , [str((published_at) )]),Tag.custom(TagKind.TITLE(), [title])
               else:
                  tags=Tag.custom(TagKind.PUBLISHED_AT() , [str((published_at) )])
              
            return tags,url_uid,list_e

async def edit_can_book(tag,pubkey,url_uid,other_tag):
  key_string=log_these_key()
  if key_string!=None: 
   keys = Keys.parse(key_string)
   
   if pubkey==keys.public_key().to_hex():  
    signer=NostrSigner.keys(keys)
    client = Client(signer)
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(RelayUrl.parse(jrelay))
       
    await client.add_relay(RelayUrl.parse("wss://relay.lnfi.network/"))
    await client.add_relay(RelayUrl.parse("wss://relay.braydon.com/"))
    #await client.add_relay("")
    await client.connect()
    
    builder = EventBuilder.bookmarks_set(url_uid,tag).tags(other_tag)
    
    test_result_post= await client.send_event_builder(builder)

    print("Event sent:")

    await asyncio.sleep(2.0)
    # Get events from relays
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     print(event.as_json())
    return test_result_post    
   else:
      print("no match", pubkey, "with \n", keys.public_key().to_hex())
  else:
      print("no key")     

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

db_note=[]
list_notes=[]

def Open_kinds(list_int:list[int]):
     """list_int = kinds number \n
        2323 = notes of kind 2323 
        2424 = notes of kind 2424 
     """
     test_kinds=[]
     if __name__ == "__main__":
       for key in list_int:
        test_kinds.append(Kind(key))  
       test = asyncio.run(Get_event_from(test_kinds))
       if test!=[] and test!=None:
        note= get_note(test)
        for xnote in note:
         if xnote not in db_note:
            db_note.append(xnote)
            list_notes.append(xnote) 
        show_noted()   

button4=tk.Button(root,text="Search Card Note",command=lambda: Open_kinds([2323,2424]),font=('Arial',12,'bold'))
button4.place(relx=0.05,rely=0.5)

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)

    # Add relays and connect
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.add_relay(RelayUrl.parse("wss://purplerelay.com/"))
    
    if relay_list!=[]:
        for xrelay in relay_list:
          if xrelay!="wss://yabu.me/":
            await client.add_relay(RelayUrl.parse(xrelay))
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

async def get_kind_relay(client, event_):
    f = Filter().kinds(event_).limit(16)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
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
       context0=context0+"\n"+"Kind "+str(note["kind"]) 
       context1=note['content']  
       if note['tags']!=[]:
        
        context2=" "
        if tags_string(note,"title")!=[]:
         for xnote in tags_string(note,"title"):
          context2=context2+"\n"+"- Title "+str(xnote) +"\n"
        if tags_string(note,"summary")!=[]:
         for xnote in tags_string(note,"summary"):
           context2=context2+"\n"+"- Summary "+tags_string(note,"summary")[0]+"\n"
        if tags_string(note,"description")!=[]: 
                context2=context2+"\n" +"- Description "+str(tags_string(note,"description")[0]) +"\n"    
       else: 
        
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
       second_label10.insert(END,context1+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=2) 
      
       def print_id(entry):
           number=list(list_notes).index(entry)
           print(number)
           print(entry['tags'])
                  
       def print_var(entry):
                print("event_id",entry["id"])

       def send_var(entry):
            if tags_string(entry,"e")!=[]:
               if entry["kind"]==2424:
                  if messagebox.askyesno("kind "+str(entry["kind"]),"Possible card \n is the right bookmakrs?"):
                     e_string_var.set(entry["id"])
               else:
                 if messagebox.askyesno("kind "+str(entry["kind"]),"Update card \n is the right bookmakrs?"):
                    e_string_var.set(entry["id"])
                  
            else:
               if entry["kind"]==2424:
                       if messagebox.askyesno("kind "+str(entry["kind"]),"Wish card \n is the right bookmakrs?"):
                          e_string_var.set(entry["id"])
               else:
                  if messagebox.askyesno("kind "+str(entry["kind"]),"Todo Done card \n is the right bookmakrs?"):
                     e_string_var.set(entry["id"])    
                       
               
       button=Button(scrollable_frame_1,text=f"Print id", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=3,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read", command=lambda val=note: print_id(val))
       button_grid2.grid(row=3,column=s1+1,padx=5,pady=5)    
       button_grid3=Button(scrollable_frame_1,text=f"Add to bookmark", command=lambda val=note: send_var(val))
       button_grid3.grid(row=3,column=s1+2,padx=5,pady=5) 
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="bottom", fill="x",padx=20)
    scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.02,rely=0.55,relwidth=0.32,relheight=0.4)

    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.2,rely=0.50)      

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