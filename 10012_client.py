timeline_people=[]
draft_user=[]
relay_list=[]
db_note=[]
search_pubkey_list=[]
from nostr_sdk import *
import asyncio
import tkinter as tk
from tkinter import *
from tkinter import ttk
import json
from datetime import timedelta
import requests
import shutil
from PIL import Image, ImageTk
from tkinter import messagebox 
import time

root = tk.Tk()
root.geometry("1300x800")
root.title("Timeline People")

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

frame1=tk.Frame(root)    
Profile_frame = ttk.LabelFrame(root, text="Profile", labelanchor="n", padding=10)
Profile_frame.place(relx=0.01,rely=0.03,relwidth=0.2,relheight=0.3)
label = tk.Label(root, text="Name",font=('Arial',12,'normal'))
label.place(relx=0.02,rely=0.06)
combo_box = ttk.Combobox(root, values=["Sebastix","Cody","Dawn","Silberengel","il_lost_"],font=('Arial',12,'normal'),width=15)
combo_box.place(relx=0.06,rely=0.06)
combo_box.set("Some Users")
combo_box.bind("<<ComboboxSelected>>", on_select)

combo_relay = ttk.Combobox(root, values=[],font=('Arial',14,'normal'),width=18)
combo_relay.place(relx=0.03,rely=0.15)
combo_relay.set("")
combo_relay.bind("<<ComboboxSelected>>", on_relay)
entry_id_note=StringVar()
entry_note_note=StringVar()
label_entry_id=tk.Label(root, text="Pubkey",font=("Arial",12,"normal"))
label_entry_id.place(relx=0.07,rely=0.11)
value=float(1*3600/86400)

def on_time(event):
   select_time=int(combo_value.get())
   global value
   value=float(select_time*3600/86400)

combo_value = ttk.Combobox(root, values=[1,2,3,4,5,6,7,8],font=('Arial',12,'normal'),width=5)
combo_value.place(relx=0.04,rely=0.28)
combo_value.set(int(1))
combo_value.bind("<<ComboboxSelected>>", on_time)
label_entry_h=tk.Label(root, text="Hour",font=("Arial",12,"normal"))
label_entry_h.place(relx=0.12,rely=0.28)

def search_people():
   if db_list!=[]:
      for db_people in db_list:
         if db_people["pubkey"] not in timeline_people:
            timeline_people.append(db_people["pubkey"])
      list_pubkey_id()
      
button_2=tk.Button(root,text="Metadata Users",command=search_people,font=('Arial',12,'bold'))  #timeline
button_2.place(relx=0.1,rely=0.21)                

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
    
async def get_note_cluster(client, authors, type_of_event):
    f = Filter().authors(authors).kinds(type_of_event).limit(1000)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_relay(client, user):
    f = Filter().author(user).kind(Kind(10012))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def feed_cluster(authors,type_of_event):
    # Init logger
    init_logger(LogLevel.INFO)
   
    client = Client(None)
    #uniffi_set_event_loop(asyncio.get_running_loop())

    # Add relays and connect
    relay_url_1=RelayUrl.parse("wss://nostr.mom/")
    relay_url_2=RelayUrl.parse("wss://nos.lol/")
    relay_url_3=RelayUrl.parse("wss://nostr-pub.wellorder.net/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    await client.add_relay(relay_url_3)
   
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_note_cluster(client, authors, type_of_event)
    else:
        combined_results = await get_relay(client, authors)
    
    return combined_results

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

Pubkey_Metadata={}
photo_profile={}
db_list_note_follow=[]

def list_pubkey_id():
  
  if timeline_people !=[]:
   test_people=user_convert(timeline_people)    #not cover people are already on metadata
   metadata_note=search_kind(test_people,0)
   if metadata_note!=[]:
       for single in metadata_note:
        if single not in db_list_note_follow:
           db_list_note_follow.append(single)
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
         
         if "picture" in list(single_1.keys()):
          if single_1["picture"]!="":
                      
           if single["pubkey"] not in list(photo_profile.keys()):
              if single_1["picture"]!="":
               photo_profile[single["pubkey"]]=single_1["picture"]
                       
                        
        except KeyError as e:
          print("KeyError ",e) 
       print("Profile ",len(Pubkey_Metadata)," Profile with image ",len(photo_profile))   

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

async def get_relays_z(client, authors):
    f = Filter().authors(authors).kind(Kind(0))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_relay_z(client, user):
    f = Filter().author(user).kind(Kind(0))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def feed(authors):
      
    client = Client(None)
    
    # Add relays and connect
    relay_url_1=RelayUrl.parse("wss://relay.damus.io/")
    await client.add_relay(relay_url_1)
    relay_url_2=RelayUrl.parse("wss://nos.lol/")
    await client.add_relay(relay_url_2)
    
    if relay_list!=[]:
       
       for jrelay in relay_list:
          relay_url_list=RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_relays_z(client, authors)
    else:
        combined_results = await get_relay_z(client, authors)
    
    return combined_results    

def metadata_0(nota,y):
   import json
   try:
    test=json.loads(nota["content"])
    if y in list(test.keys()):
     return str(test[y])
   except KeyError as e:
      print(e)

def metadata_p_0(pubkey,list_note):
  import json
  try:
   for n0ta in list_note:
    if n0ta["kind"]==0 and n0ta["pubkey"]==pubkey:
     test:dict=json.loads(n0ta["content"])
     if test!={}:
        return test
  except KeyError as e:
      print(e)

def layout():
   if Pubkey_Metadata!={}: 
    frame1=Frame(root, width=330, height=100)
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
    s=1  

    def one_note(pubkey):
       for note_text in db_list:
        if note_text["pubkey"]==pubkey:
         show_print_test_tag(note_text)
         close_canvas()
         break 

    for name_pubkey in list(Pubkey_Metadata.keys())[0:100]:
        if name_pubkey not in draft_user:
         var_npub =StringVar()
         var_npub.set("Nickname " +Pubkey_Metadata[name_pubkey])
         if name_pubkey in search_pubkey_list:   
            s=1   
            var_npub.set("Nickname " +Pubkey_Metadata[search_pubkey_list[0]])
         def print_photo_url(url):
            if url!="":
             response = requests.get(url, stream=True)
             if response.ok==True:
              with open('my_image.png', 'wb') as file:
                shutil.copyfileobj(response.raw, file)
              del response
              from PIL import Image
              
              image = Image.open('my_image.png')
              image.thumbnail((250,150))  # Resize image if necessary
              photo = ImageTk.PhotoImage(image)
              label_image.config(image=photo)
              label_image.image_names= photo 
              button_photo_close.place(relx=0.95,rely=0.68)
              label_image.place(relx=0.75,rely=0.7)     
              return url   
             else:
                label_image.place_forget()

         def close_image():
            label_image.place_forget()         
            button_photo_close.place_forget()
         button_photo_close=Button(root, text="X", command=close_image,font=('Arial',12,'normal'))
         Message_npub= Message(scrollable_frame, textvariable=var_npub, width=300,font=('Arial',12,'bold'),foreground="grey") 
         Message_npub.grid(row=s+2,column=0, columnspan=3, padx=30, pady=2, sticky="w") 
         var_time =StringVar()
         Message_time= Message(scrollable_frame, textvariable=var_time, width=300, font=('Arial',12,'bold'), foreground="grey")
         label_image = Label(root,text="",)
         if name_pubkey in list(photo_profile.keys()):
          if str(photo_profile[name_pubkey])!=None:
            label_image.place(relx=0.75,rely=0.7)       
         Message_time.grid(row=s, column=0, columnspan=3, padx=50, pady=5, sticky="w")   
         scroll_bar_mini = tk.Scrollbar(scrollable_frame)
         scroll_bar_mini.grid( sticky = NS,column=4,row=s+3,pady=5)
         second_label10 = tk.Text(scrollable_frame, padx=8, height=5, width=30, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
         meta_test=metadata_p_0(name_pubkey,db_list_note_follow)
         if meta_test!=None:
            key_value=""
            for key_x,value_y in meta_test.items():
               key_value=key_value+"- "+str(key_x)+" " +str(value_y) +"\n"
               second_label10.insert(END,str(key_value))
         else:
            second_label10.insert(END,name_pubkey+"\n") 
         scroll_bar_mini.config( command = second_label10.yview )
         second_label10.grid(padx=10, column=0, columnspan=3, row=s+3) 
         if name_pubkey in list(photo_profile.keys()):
          if str(photo_profile[name_pubkey])!=None:    
            button_photo=Button(scrollable_frame, text="Photo", command=lambda  val=str(photo_profile[name_pubkey]): print_photo_url(val),font=('Arial',12,'normal'))
            button_photo.grid(row=s+4, column=0, padx=5, pady=5) 
         blo_label = Button(scrollable_frame, text=f"One note of {str(Pubkey_Metadata[name_pubkey][0:9])}",font=('Arial',12,'normal'),command=lambda val=name_pubkey: one_note(val) )
         blo_label.grid(row=s + 4, column=1, padx=2, pady=5)
         Button(scrollable_frame, text="Print Metadata",command=lambda val=meta_test: print(val),font=('Arial',12,'normal')).grid(row=s +4, column=2, padx=5, pady=2)   
        s += 5   
        root.update_idletasks() 
    frame1.place(relx=0.65,rely=0.12, relheight=0.45,relwidth=0.35)      

    def close_canvas():
     scrollable_frame.forget()
     canvas.destroy()
     frame1.destroy()
     label_image.place_forget()
     button_close_s.place_forget()
     entry_nick.place_forget()
     button_close_1.place_forget() 
    
    if Pubkey_Metadata=={}:
        close_canvas()    

    def search_nickname():
     if entry_nick.get()!="":
      search_pubkey_list.clear()
      Name_value=list(Pubkey_Metadata.values())
      Name_key=list(Pubkey_Metadata.keys())
      if entry_nick.get() in Name_value:
       for key_x in Name_key:
          if Pubkey_Metadata[key_x]==entry_nick.get():
             print(entry_nick.get(),"\n",key_x)      
             search_pubkey_list.append(key_x)    
             close_canvas()
             layout()       

    entry_nick=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))          
    entry_nick.place(relx=0.67,rely=0.1,relwidth=0.12,relheight=0.04) 
    button_close_1=Button(root, command=search_nickname, text="Find ",font=('Arial',12,'normal'), fg="blue")
    button_close_1.place(relx=0.8,rely=0.1)
    button_close_s=Button(root, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close_s.place(relx=0.86,rely=0.1)    

button_open=Button(root, command=layout, text="Scroll User",highlightcolor='WHITE',background="grey",font=('Arial',12,'bold'))
button_open.place(relx=0.85,rely=0.02, anchor="n")            

def show_print_test():
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
 for note in db_list:
    
  if float(int(time.time())-note["created_at"])/(86400)<value: 
   if note["kind"]==6:       
    context0= "RT "+" By "+note["pubkey"][0:9]
   else: 
    if note["pubkey"] in list(Pubkey_Metadata.keys()):
     context0="Nickname " +str(Pubkey_Metadata[note["pubkey"]])
    else: 
     context0="Pubkey: "+note['pubkey']
   try:
    context0=context0+"\n"+"Time: "+str(int((float(int(time.time())-note["created_at"])/(60))))+str(" min") 
    if note['tags']!=[]:
        if note["kind"]==6:
           try: 
            context1= str(json.loads(note["content"])["content"]+"\n")
            context2= str(json.loads(note["content"])["tags"])
           except json.decoder as e:
              print(e)
        else:
           if Checkbutton_e.get()==1 and tags_string(note,"e")==[]:
            context1=note['content']+"\n"
            tag_note=""
           
            for note_x in note["tags"]:
             tag_note=tag_note+ str(note_x)+"\n"
            context2="[[ Tags ]]"+"\n" +tag_note
           if Checkbutton_e.get()==1 and tags_string(note,"e")!=[]:
              context0=""
              context1=""
              context2=""
           if Checkbutton_e.get()==0: 
               context1=note['content']+"\n"
               tag_note=""
               for note_x in note["tags"]:
                tag_note=tag_note+ str(note_x)+"\n"
               context2="[[ Tags ]]"+"\n" +tag_note
     
     
     
    else: 
        if note["kind"]==6:
         context1= str(json.loads(note["content"])["content"])+"\n"
         context2=""
        else:
           context1=note['content']+"\n"
           context2=""
   except TypeError as e:
      print(e)        
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=350,font=("Arial",12,"normal"))
   if context0!="":
    var_id.set(context0)
    label_id.grid(pady=2,column=0, columnspan=3,row=s)
    scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
    scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
    second_label10 = tk.Text(scrollable_frame_2, padx=2, height=5, width=32, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
    second_label10.insert(END,context1+"\n"+str(context2))
    scroll_bar_mini.config( command = second_label10.yview )
    second_label10.grid(padx=5, column=0, columnspan=3, row=s+1) 
      
   def print_note(entry):
           print(entry)

   def print_var(entry):
        if entry["tags"]!=[]:
          photo_print(entry)
          
   if context0!="":      
    button=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val))
    button.grid(column=0,row=s+2,padx=5,pady=5)
    button_grid2=Button(scrollable_frame_2,text="Stamp", command=lambda val=note: print_note(val))
    button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
    Button(scrollable_frame_2, text="Open", command=lambda val=note: respond_to(val)).grid(row=s + 2, column=2, padx=5, pady=5)
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   s=s+3
   def close_frame():
     frame3.destroy()    

   button_frame=Button(scrollable_frame_2,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.grid(row=0,column=1,padx=5,pady=5)
   frame3.place(relx=0.22,rely=0.12,relwidth=0.4,relheight=0.5 ) 
  root.update_idletasks() 

button_id=tk.Button(root,command=show_print_test,text="Feed", background="grey",font=("Arial",12,"bold"))
button_id.place(relx=0.25,rely=0.05)

Checkbutton_e = IntVar()
Type_feed = Checkbutton(root, variable = Checkbutton_e, onvalue = 1, offvalue = 0,text="No reply",background="grey",font=("Arial",12,"bold"),command=show_print_test)
Type_feed.place(relx=0.35,rely=0.05)
def test_relay(): 
 if combo_relay.get()!="":
   tm=note_list_r()
   return tm
  
def note_list_r():
    L=[]
    if __name__ == "__main__":
     
     combined_results = asyncio.run(main_feed())
    L=get_note(combined_results)
    return L

def search_():
   result=test_relay()
   if result !=None:
    timeline_created(db_list,result)

def Block_space():
   if list_event!=[]: 
    frame1=Frame(root, width=200, height=50)
    canvas = Canvas(frame1, width=150, height=30)
    canvas.pack(side="left", fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame1, orient=VERTICAL, command=canvas.yview)
   
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Frame scrollabile
    scrollable_frame = Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    string_kind=IntVar()
    def create_note(block_n, s):
        if s%2!=0: 
         message = Message(scrollable_frame, text=" "+str(block_n), width=100)
         message.grid(row=s, column=0, columnspan=2, padx=10, pady=5, sticky="w")
         # Button down
         Button(scrollable_frame, text="Print", command=lambda: print(block_n)).grid(row=s + 1, column=0, padx=5, pady=5)
         blo_label = Button(scrollable_frame, text="delete", command=lambda: list_event.remove(block_n))
         blo_label.grid(row=s + 1, column=1, padx=5, pady=5)
        else: 
         message2 = Message(scrollable_frame, text=" "+str(block_n), width=100)
         message2.grid(row=s-3, column=3,columnspan=2, padx=10, pady=5, sticky="w")
         button=Button(scrollable_frame, text="Print", command=lambda: print(block_n)).grid(row=s-2, column=3, padx=5, pady=5)
         blo_label2 = Button(scrollable_frame, text="delete", command=lambda: list_event.remove(block_n))
         blo_label2.grid(row=s-2, column=4, padx=5, pady=5)

    entry_kind=Entry(root,textvariable=string_kind,width=10)
    s=6
    def add_event():
            if isinstance(int(entry_kind.get()),int):
              
              if Kind(int(entry_kind.get())) not in list_event:
                 
                 list_event.append(Kind(int(entry_kind.get())))
                 print(list_event)
                 string_kind.set(0)
                 
            else:
               print((entry_kind.get()))     

    blo_add = Button(root, text="ADD", command=add_event)
    blo_add.place(relx=0.7,rely=0.9)
    entry_kind.place(relx=0.75,rely=0.9,relheight=0.03)       

    
    s = 1
    for nblock in list_event: 
     create_note(nblock, s)
     s += 3   
    
    frame1.place(relx=0.7,rely=0.6, relheight=0.25,relwidth=0.21)  
    
    def close_canvas():
        scrollable_frame.forget()
        canvas.destroy()
        frame1.destroy()
        entry_kind.place_forget()
        blo_add.place_forget()
        button_close.place_forget()

    button_close=Button(root, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close.place(relx=0.85,rely=0.9)      

    if list_event==[]:
     close_canvas()    
       
button_block_npub=Button(root, command=Block_space, text="Events",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',12,'bold'))
button_block_npub.place(relx=0.7,rely=0.02)

db_list=[]
list_event=[Kind(1),Kind(30023),Kind(6)]
button_tm=tk.Button(root,command= search_,text="View note", font=("Arial",12,"normal"))
button_tm.place(relx=0.03,rely=0.21)

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

def respond_to(note_text):
    show_print_test_tag(note_text)

def show_print_test_tag(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = tk.Frame(canvas_2, background="#E3E0DD")

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")))

   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
              
   var_id_3=StringVar()
   label_id_3 = Message(scrollable_frame_2,textvariable=var_id_3, relief=RAISED,width=290,font=("Arial",12,"normal"))
   label_id_3.grid(pady=1,padx=8,row=s,column=0, columnspan=3)
   if note["pubkey"] in list(Pubkey_Metadata.keys()):
    var_id_3.set("Nickname " +str(Pubkey_Metadata[note["pubkey"]])+"\n" +"Time: "+str(int((float(int(time.time())-note["created_at"])/(60))))+str(" min"))
   else:
    var_id_3.set("Author: "+note["pubkey"]+"\n" +"Time: "+str(int((float(int(time.time())-note["created_at"])/(60))))+str(" min"))
   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid( sticky = NS,column=4,row=s+1)
   second_label_10 = tk.Text(scrollable_frame_2, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   context2=""  
   if note["tags"]!=[]: 
    if tags_string(note,"t")!=[]:
        for note_tags in tags_string(note,"t"):
            context2=context2+str("#")+note_tags+" "
    if tags_string(note,"e")!=[]:
     if four_tags(note,"e"):
         for F_note in four_tags(note,"e"):
             context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"        
   else:
           context2=""  
     
   second_label_10.insert(END,note["content"]+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label_10.yview )
   second_label_10.grid(padx=10, column=0, columnspan=3, row=s+1) 

   def print_var(entry):
            if entry["tags"]!=[]:
                photo_print(entry)
         
   def print_content(entry):
       result=show_note_from_id(entry)
       if result!=None: 
        z=4
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             if jresult["pubkey"] in list(Pubkey_Metadata.keys()):
              var_id_r.set("Nickname " +str(Pubkey_Metadata[jresult["pubkey"]])+"\n" +"Time: "+str(int((float(int(time.time())-jresult["created_at"])/(60))))+str(" min"))
             else:
              var_id_r.set(" Author: "+jresult["pubkey"]+"\n" +"Time: "+str(int((float(int(time.time())-jresult["created_at"])/(60))))+str(" min"))
         
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             context22="---> tags: <--- "+"\n"   
             if tags_string(jresult,"e")!=[]:
              if four_tags(jresult,"e")!=None:
                for F_note in four_tags(jresult,"e"):
                     context22=context22+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
                     if F_note[2]!="" and F_note not in relay_list:
                        relay_list.append(F_note[2])
              
             else:
               context22="---> Root  <--- "  
             second_label10_r.insert(END,jresult["content"]+"\n"+str(context22))
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
             button_photo=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=jresult: print_var(val))
             button_photo.grid(column=0,row=z+2,padx=5,pady=5)
             button_print=Button(scrollable_frame_2,text=f"Print ", command=lambda val=jresult: print(val))
             button_print.grid(column=1,row=z+2,padx=5,pady=5)
           z=z+3
           
                   
   button=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text=f"Print", command=lambda val=note: print(val))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
   if tags_string(note,"e")!=None:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply ", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    
   else:
    if tags_string(note,"imeta")!=None:
     button_grid3=Button(scrollable_frame_2,text=f"See video ", command="")
     button_grid3.grid(row=s+2,column=2,padx=5,pady=5)        
   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
 
   def close_frame():
    frame3.destroy()    
   button_frame=Button(frame3,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.pack()   
   frame3.place(relx=0.65,rely=0.2,relheight=0.4,relwidth=0.3) 

def show_note_from_id(note):
        result:str=note["id"]
        replay=nota_reply_id(note)
        
        if replay!=[]:
           items=get_note(asyncio.run(Get_event_id(replay)))
        else:
           items=get_note(asyncio.run(Get_event_id(result)))
        return items   

def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[] and tags_string(nota,"e")!=None:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id          

async def get_notes_(client, e_ids):
     f = Filter().ids([EventId.parse(e_id) for e_id in e_ids])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec() if event.verify()]
     return z

async def get_one_note(client, e_id):
    f = Filter().event(EventId.parse(e_id)).kinds(list_event).limit(100)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_event_id(e_id):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
      try: 
       for jrelay in relay_list:
         print(jrelay)
         relay_url = RelayUrl.parse(jrelay)
         await client.add_relay(relay_url)
      except NostrSdkError as e:
         print(e)   
    else:
     relay_url_1 = RelayUrl.parse("wss://nos.lol/")
     await client.add_relay(relay_url_1)
     relay_url_x = RelayUrl.parse("wss://nostr.mom/")
     await client.add_relay(relay_url_x)
     relay_url_2 = RelayUrl.parse("wss://purplerelay.com/")
     await client.add_relay(relay_url_2)

    
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(e_id, list):
         print("list")
         test_id = await get_notes_(client,e_id)
    else:
        print("str")
        test_id = await get_one_note(client,e_id)
       
    return test_id

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
       headers = {"User-Agent": "Mozilla/5.0"}
       response = requests.get(label_pic.get(),headers=headers, stream=True)
       
       response.raise_for_status()  
       if response.ok==TRUE:
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
        frame_pic.place(relx=0.35,rely=0.65,relwidth=0.3,relheight=0.3,anchor="n")
      except TypeError as e: 
        print(e)  
      except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")  

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
   list_video=['mov','mp4']
   img=['png','jpg','JPG','gif']
   img1=['jpeg','webp'] 
   ytube=['https://youtu.be']
   tme=["https://t.me/"]
   xtwitter=["https://x.com/"]
   if f==None:
                 return "no spam"
   if f[-3:] in list_video:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   if f[0:16] in ytube:
            return 'ytb'
   if f[0:13] in tme:
            return "tme"
   if f[0:14] in xtwitter:
            return "tme"
   
   else:
       return "spam"  

root.mainloop()