import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import asyncio
from nostr_sdk import *
from asyncio import get_event_loop
from datetime import timedelta
from PIL import Image, ImageTk
import requests
import shutil

root = tk.Tk()
root.title("Tags test")
root.geometry("1300x800")
public_list=[]
relay_list=[]
db_delete_card=[]

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f   

def tags_string(x,obj):
   try:  
    f=x["tags"]
    z=[]
    if f!=[]:
     for j in f:
      if j[0]==obj:
          z.append(j[1])
     return z    
   except IndexError as e:
       print(e,"\n",x)    

def convert_user(x):
    try:
     other_user_pk = PublicKey.parse(x)
     return other_user_pk
    except NostrSdkError as e:
       print(e,"this is the hex_npub ",x)

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list       
   
def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z     

def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[] and tags_string(nota,"e")!=None:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id 

def share_naddr(note):
    coord = Coordinate(Kind(note["kind"]),PublicKey.parse(note["pubkey"]),str(tags_string(note,"d")[0]))
    coordinate = Nip19Coordinate(coord, [])
    #print(f" Coordinate (encoded): {coordinate.to_bech32()}")
    print(f"https://njump.me/{coordinate.to_bech32()}")
  
List_combo_value={"To do":[],"Wish list":[], "Done":[], "To complete":[]}

def show_print_test_tag():
  if db_list_note!=[]: 
  
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
   s=0

   list_note=db_list_note
   
   for note in list_note:
    context0="id: "+note["id"][0:17]+"....."+note["id"][47:63]+"\n"
    if tags_string(note,"title")!=[]:
     for xnote in tags_string(note,"title"):
         context0=context0+"\n"+"Title "+str(xnote)
    if note['tags']!=[]:
        context2="[ [  Tags ] ]"+"\n"+"\n"
        if tags_string(note,"e")!=[]:
         context2=context2+"tags event number: "+str(len(tags_string(note,"e"))) +"\n"
    else: 
        context2=""
         
    if tags_string(note,"e")!=[]:
                                                                                  
      button_grid2=Button(scrollable_frame_2,text=context0, command=lambda val=note: print_content(val),font=("Arial",12,"normal"))
      
    else:
           button_grid2=Button(scrollable_frame_2,text=context0, command=lambda val=note: share_naddr(val),font=("Arial",12,"normal"))
    
    button_grid2.grid(pady=2,column=0, row=s,columnspan=3)
    scroll_bar_mini_2 = tk.Scrollbar(scrollable_frame_2)
    scroll_bar_mini_2.grid( sticky = NS,column=3,row=s+2,rowspan=2,pady=5)
    second_label_2 = tk.Text(scrollable_frame_2, padx=8, height=5, width=29, yscrollcommand = scroll_bar_mini_2.set, font=('Arial',14,'bold'),background="#D9D6D3")
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

    if note["tags"]!=[]:
      if tags_string(note,"r")!=[]:
       button_grid_2=Button(scrollable_frame_2,text="Read Link", command=lambda val=note: show_db_list(val),font=("Arial",12,"normal"))
       button_grid_2.grid(row=s+4,column=1,padx=5,pady=5)      
    if note["tags"]!=[]:
      if note["kind"]>30000:
        if tags_string(note,"a")!=[]:
           button_grid_2=Button(scrollable_frame_2,text="Read_a", command=lambda val=note: arrow_a_note(val),font=("Arial",12,"normal"))
           button_grid_2.grid(row=s+4,column=0,padx=5,pady=5)    

    s=s+5       
             
   def arrow_a_note(note):
     if note["tags"]!=[]:
      if tags_string(note,"a")!=[]:   
       blocco_note= asyncio.run(Get_coord_str(tags_string(note,"a")))   
       result1= get_note(blocco_note[::-1])  #reverse 
       z=5
       for jresult in result1:
           if jresult["id"]!=note["id"]:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=320,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
        
             var_id_r.set(" Author: "+jresult["pubkey"])
                      
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=28, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             context22=""
             if tags_string(jresult,"d")!=[]:
                context22=context22+str("d ")+str(tags_string(jresult,"d")[0])+ "\n"
             if tags_string(jresult,"title")!=[]:
                context22=context22+str("- Title ")+str(tags_string(jresult,"title")[0])+ "\n"
             if tags_string(jresult,"summary")!=[]:
                if str(tags_string(jresult,"summary")[0])!="":
                 context22=context22+str("- Summary ")+str(tags_string(jresult,"summary")[0])+ "\n"
              
             context22=context22+"------------ "+"\n"       
             second_label10_r.insert(END,str(context22)+"\n"+jresult["content"])
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
             button_grid_s=Button(scrollable_frame_2,text="Share", command=lambda val=jresult: share_naddr(val),font=("Arial",12,"normal"))
             button_grid_s.grid(row=z+2,column=0,padx=5,pady=5)  
           z=z+3        
   
   def print_link(entry):
      context2_r=""
      z=5
      for F_note in four_tags(entry,"r"):
             if len(F_note)>=3:
              button_grid_r=Button(scrollable_frame_2,text=f"{F_note[1][0:20]}  { F_note[2]}", command=lambda val=F_note[1]: print(val),font=("Arial",12,"normal"))
              button_grid_r.grid(row=z,column=0,columnspan=3,padx=5,pady=5)   
             z=z+3
                  
     
   def print_content(entry):
       list_of_id()
       valid_title=tags_string(entry,"title")[0]
       if valid_title in list(List_combo_value.keys()):
         title_list=List_combo_value[valid_title]
         
       if title_list!=[]:
            show_noted(valid_title)
       else:     
        result=show_note_from_id(entry)
        if result!=None and result!=[]: 
         for jresult in result:
            if jresult not in title_list:
                title_list.append(jresult)
         List_combo_value[valid_title]=title_list
         show_noted(valid_title)
                                  
   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()   

   button_frame=Button(frame3,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.pack(pady=5)   
   frame3.place(relx=0.05,rely=0.20,relheight=0.53,relwidth=0.31) 
     
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
      if tags_string(note,"summary")!=[]:
       contentag=contentag+"\n"+"Summary "+str(tags_string(note,"summary")[0])   
    if n in [1,30023]:   
     return contentag 
   else:
      return str("\n"+"kind "+str(n))

def show_note_from_id(note):
        result=note["id"]
       
        replay=nota_reply_id(note)
        #replay.append(result)
        if replay!=[] and db_delete_card==[]:
           items=get_note(asyncio.run(Get_event_id(replay)))
        else:
           items=get_note(asyncio.run(Get_event_id(result)))
        return items   

async def get_notes_(client, e_ids):
     f = Filter().ids([EventId.parse(e_id) for e_id in e_ids])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec() if event.verify()]
     return z

async def get_one_note(client, e_id):
    f = Filter().id(EventId.parse(e_id))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_event_id(e_id):
    # Init logger
    init_logger(LogLevel.INFO)
   
    client = Client(None)
    relay_url_1 = RelayUrl.parse("wss://nostr.mom/")
    relay_url_2 = RelayUrl.parse("wss://purplerelay.com/")
    # Add relays and connect
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
       
    if relay_list!=[]:
        for xrelay in relay_list:
          if xrelay[0:6]=="wss://" and xrelay[-1]=="/":  
            relay_url = RelayUrl.parse(xrelay)
            await client.add_relay(relay_url)
    await client.connect()
    
    await asyncio.sleep(2.0)

    if isinstance(e_id, list):
         print("list")
         test_id = await get_notes_(client,e_id)
    else:
        print("str")
        test_id = await get_one_note(client,e_id)
       
    return test_id      

async def get_list_a(client, event_publikey):
     d_identifiers=[]
     for xevent_ in event_publikey:
        if len(xevent_)>71:
         d_identifiers.append(xevent_[71:])
         d_kind=xevent_[0:5]
    
     f = Filter().kind(Kind(int(d_kind))).identifiers(d_identifiers)
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec() if event.verify()]
     return z

async def Get_coord_str(a_nostr_tag):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    relay_url_1 = RelayUrl.parse("wss://nostr.mom/")
    relay_url_2 = RelayUrl.parse("wss://nos.lol/")
    relay_url_3 = RelayUrl.parse("wss://thecitadel.nostr1.com")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    await client.add_relay(relay_url_3)
    await client.connect()

    await asyncio.sleep(2.0)
    
    if isinstance(a_nostr_tag, list):
         print("list0")
         test_id = await  get_list_a(client,a_nostr_tag)
    else:
        print("str0")
        
    return test_id

def select_type(event):
    selet_item=combo_to_do_list.get()

db_list_note=[]

combo_to_do_list = ttk.Combobox(root, values=["To do","Wish list", "Done", "To complete" ],width=10,font=("Arial",12,"normal"))
combo_to_do_list.set("")
combo_to_do_list.bind("<<ComboboxSelected>>",select_type)

def call_text():
  if relay_list!=[]:
   if __name__ == "__main__":
    response=asyncio.run(Search_d_tag())
    if response:

     note_=get_note(response)
     for jnote in note_:
       if jnote not in db_list_note:
          db_list_note.append(jnote)
     if db_list_note!=[]:
        show_print_test_tag()

    else:
       print("empty")
  else: 
              
          if __name__ == "__main__":
            response=asyncio.run(Search_d_tag())
          if len(relay_list)>0:
             button_close_search["text"]="Search 🔍"
          else:
             if response!=None:
                print(str(len(response)),"\n",response[0]) 

async def get_result_w(client):
   try: 
    if public_list!=[]:
          f = Filter().author(public_list[0]).kind(Kind(30003)).limit(10)
    else:
           f = Filter().author().kind(Kind(30003)).limit(10)

    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z
   except TypeError as e:
      print(e, " probably public list is empty")

async def Search_d_tag():
      
    # Add relays and connect
    if relay_list!=[]:
       client = Client(None)
       for jrelay in relay_list:
           relay_url = RelayUrl.parse(jrelay)
           await client.add_relay(relay_url)
       await client.connect()
       await asyncio.sleep(2.0)
       relay_url_1 = RelayUrl.parse("wss://nostr.mom/")
       await client.add_relay(relay_url_1)
       if public_list!=[]:
        await client.connect()
        combined_results = await get_result_w(client)
        return combined_results
    # Init logger
    init_logger(LogLevel.INFO)
    client = Client(None)
    relay_url_1 = RelayUrl.parse("wss://nostr.mom/") 
    await client.add_relay(relay_url_1)
    await client.connect()
    await search_box_relay()
    print("found ", len(relay_list), " relays")

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
       relay_url_2 = RelayUrl.parse("wss://purplerelay.com/")
       await client.add_relay(relay_url_1)
       await client.add_relay(relay_url_2)
    await client.connect()
    relay_add=get_note(await get_outbox_relay(client))
    if relay_add !=None and relay_add!=[]:
           i=0
           while i<len(relay_add):
            for xrelay in tags_string(relay_add[i],'r'):
             
              if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay not in Bad_relay_connection:
               if xrelay not in relay_list:
                relay_list.append(xrelay) 
              
            i=i+1             

Bad_relay_connection=["wss://relay.noswhere.com/","wss://relay.purplestr.com/","wss://relay.momostr.pink/"]
button_close_search=tk.Button(root, text='Search Relay',font=('Arial',12,'bold'), command=call_text)    
button_close_search.place(relx=0.3,rely=0.1 ) 
p_tag = tk.Label(root, text="Pubkey",font=("Arial",12,"bold"))
entryp_tag=ttk.Entry(root,justify='left',font=("Arial",12),)
p_tag.place(relx=0.05,rely=0.06,relwidth=0.1 )
entryp_tag.place(relx=0.05,rely=0.11,relwidth=0.1 )
p_view = tk.Label(root, text="", font=("Arial",12))
p_view.place(relx=0.02,rely=0.11 )

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
p_button.place(relx=0.16,rely=0.10)

def Clear_pubkey():
   public_list.clear()
   p_view.config(text="")

p_clear_button = tk.Button(root, text="x", font=("Arial",12,"bold"), command=Clear_pubkey)
p_clear_button.place(relx=0.25,rely=0.10)

def show_noted(title):
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
 if List_combo_value[title]!=[]:
    s=1
    s1=0
    
    for note in List_combo_value[title]:
     
      try:
       context0="Author: "+note['pubkey']
       for xnote in tags_string(note,"title"):
         context0=context0+"\n"+"Title "+str(xnote) 
       context1=note['content']  
       if note['tags']!=[]:
        
        context2=" "
        if tags_string(note,"alt")!=[]:
         for xnote in tags_string(note,"alt"):
          context2=context2+"\n"+str(xnote) +"\n"
        if tags_string(note,"e")!=[]:  
         context2=context2+"\n"+"Number Card "+str(len(tags_string(note,"e")))+ "\n"   
        if tags_string(note,"summary")!=[]:
         for xnote in tags_string(note,"summary"):
           context2=context2+"\n"+"- Summary "+tags_string(note,"summary")[0]+"\n"
        if tags_string(note,"description")!=[]: 
                context2=context2+"\n" +"- Description "+str_description(str(tags_string(note,"description")[0])) +"\n"    
        if note["kind"]==30003: 
                context2=context2+"\n"+"Task complete" +"\n"            
       else: 
        
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=2)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=2) 
      
                      
       def print_var(entry):
                print("event_id",entry["id"])
                
       button=Button(scrollable_frame_1,text=f"Print id", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=3,padx=5,pady=5)
       button_grid_2=Button(scrollable_frame_1,text="Delete", command=lambda val=note: delete_card(val),font=("Arial",12,"normal"))
       button_grid_2.grid(row=3,column=s1+1,padx=5,pady=5)   
       button_grid_3=Button(scrollable_frame_1,text="Check", command=lambda val=note["id"]: id_other_list(val),font=("Arial",12,"normal"))
       button_grid_3.grid(row=3,column=s1+2,padx=5,pady=5)    
          
       def delete_card(entry):
               if entry["id"] not in db_delete_card:
                  db_delete_card.append(entry["id"])  
               if entry in List_combo_value["To do"] and entry in List_combo_value["Done"]:
                  List_combo_value["To do"].remove(entry)     
                                    
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="bottom", fill="x",padx=20)
    scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.36,rely=0.25,relwidth=0.32,relheight=0.35)

    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
        button_move1.place_forget()

    def Clicked(event):
      
      global x_space
      x_space=x_space+float(0.31)
      if x_space>float(0.87):
        x_space=0.36
        
      frame2.place_forget()
      
      frame2.place(relx=x_space,relheight=0.4, rely=0.25,relwidth=0.35)
      button_move1.place(relx=x_space+0.1,rely=0.2) 
      button_frame.place(relx=x_space+0.2,rely=0.2)   
  
    button_move1=Button(root,text="↔️", fg="blue",font=("Arial",12,"bold"))  
    button_move1.place(relx=0.4,rely=0.2)    
    button_move1.bind("<Button-1>",Clicked)    
    
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.45,rely=0.2)      

x_space=0.36

def str_description(string: str) -> str:
    string = string.replace(":", "\n\n ")
    string = string.replace(". ", "\n\n")
    string = string.replace(",", "\n ")
    string = string.replace(";", "\n  ")
    string = string.replace("-", "\n   ")
    return string

def id_other_list(id_):
   value=[]
   if db_list_note!=[]:
      for db_note in db_list_note:
         if id_ in list_id[tags_string(db_note,"title")[0]]:
            value.append(tags_string(db_note,"title")[0])
       
      print(value)         

list_id={}

def list_of_id():
   if db_list_note!=[]:
      for db_note in db_list_note:
         if tags_string(db_note,"title")[0] in combo_to_do_list["values"]:
            if tags_string(db_note,"e")!=[]:
               list_id[tags_string(db_note,"title")[0]]=tags_string(db_note,"e")

def show_db_list(note_link:dict):
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
   
   if tags_string(note_link,"r")!=[] and tags_string(note_link,"r")!=None:
      reverse=tags_str(note_link,"r")   
      context00="Pubkey: "+note_link['pubkey']+"\n"+"id: "+note_link["id"]+"\n"   
      context11=str("") 
      s=2
      for jresult in reverse:
             if len(jresult)==3:      
              context11="- "+str(jresult[2])+"\n"+ str(jresult[1])+"\n"
              button_ph=Button(scrollable_frame_2,text=f" See link", command=lambda val=jresult[1]: print(val))
              button_ph.grid(column=3,row=s,padx=5,pady=5)
              var_id_l=StringVar()
              label_id_l = Message(scrollable_frame_2,textvariable=var_id_l, relief=RAISED,width=300,font=("Arial",12,"normal"))
              var_id_l.set(context11)
              label_id_l.grid(pady=2,column=0, columnspan=3,row=s)
              s=s+1     
      var_id_1=StringVar()
      label_id_1 = Message(scrollable_frame_2,textvariable=var_id_1, relief=RAISED,width=300,font=("Arial",12,"normal"))
      var_id_1.set(context00)
      label_id_1.grid(pady=2,column=0, columnspan=3,row=0,rowspan=2)
    

      root.update_idletasks()
       
      scrollbar_2.pack(side="right", fill="y",padx=5,pady=1) 
      canvas_2.pack( fill="y", expand=True)
      
      def close_frame():
       frame3.destroy()    
   
      button_frame=Button(scrollable_frame_2,bg="darkgrey",command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
      button_frame.grid(column=1, columnspan=2,pady=5)      
      if tags_string(note_link,"r")!=[] and tags_string(note_link,"r")!=None:
       test=len(tags_string(note_link,"r"))
       test_n=float(0.1*test)
       if test_n>=float(0.35):
          test_n=float(0.35)
       frame3.place(relx=0.6,rely=0.19,relheight=0.4+test_n,relwidth=0.32) 

root.mainloop()