#Topit
import tkinter as tk
from tkinter import *
from tkinter import ttk
import asyncio
from nostr_sdk import *
import json
from datetime import timedelta
import requests
import shutil
from PIL import Image, ImageTk
from tkinter import messagebox 
import time
from cryptography.fernet import Fernet
import datetime

my_dict = {"Sebastix": "06639a386c9c1014217622ccbcf40908c4f1a0c33e23f8d6d68f4abf655f8f71", 
           "Cody": "8125b911ed0e94dbe3008a0be48cfe5cd0c0b05923cfff917ae7e87da8400883",
            "Dawn": "c230edd34ca5c8318bf4592ac056cde37519d395c0904c37ea1c650b8ad4a712", 
            "ABH3PO": "c21b1a6cdb247ccbd938dcb16b15a4fa382d00ffd7b12d5cbbad172a0cd4d170", 
            "il_lost_": "592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"}

my_list = list(my_dict.values())
my_name = list(my_dict.keys())

def on_select(event):
   db_list.clear()
   alpha_list_topic.clear()
   combo_relay['values']=[]
   combo_tag['values']=[]
   combo_t_tag.clear()
   selected_item = combo_box.get()
   entry_id_note.set(my_dict[selected_item])
   label_entry_id["text"]=my_dict[selected_item][0:9]
   relay_list.clear()
   search_relay()

def on_relay(event):
   print("-topic: ",combo_relay.get())

root = tk.Tk()
root.geometry("1300x800")
root.title("Timeline People")
frame1=tk.Frame(root)    
Profile_frame = ttk.LabelFrame(root, text="Profile", labelanchor="n", padding=10)
Profile_frame.place(relx=0.01,rely=0.03,relwidth=0.2,relheight=0.3)
label = tk.Label(root, text="Name",font=('Arial',12,'normal'))
label.place(relx=0.02,rely=0.06)
combo_box = ttk.Combobox(root, values=["Sebastix","Cody","Dawn","ABH3PO","il_lost_"],font=('Arial',12,'normal'),width=15)
combo_box.place(relx=0.06,rely=0.06)
combo_box.set("Users")
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

def on_topic(event):
   if db_list!=[]:
      note_value=""
      number=1
      
      for topic_str in Value_combo_tag:
         if Value_combo_tag[topic_str][0]==combo_filter.get():
            if number<9: 
               note_value=note_value +"\n" +" n° "+ str(number)+ " "+str(topic_str) +"   "+ str(Value_combo_tag[topic_str][1])
               number=number+1
      value_topic.config(text=note_value)
      value_topic.place(relx=0.05,rely=0.7)    


combo_filter = ttk.Combobox(root, values=["Main topic","Low engagement topic", ""],font=('Arial',14,'normal'),width=10)
combo_filter.place(relx=0.1,rely=0.65)
combo_filter.set("")
combo_filter.bind("<<ComboboxSelected>>", on_topic)
test_label=Label(root,text="Type Filter",font=('Arial',12,'bold'))
test_label.place(relx=0.03,rely=0.65)

def restore_tab(event):
   value_topic.config(text="")
   combo_filter.set("")

combo_filter.bind('<Button-3>', restore_tab) 

def since_day_time(day_ago:int):
   date_one = datetime.date.today() - datetime.timedelta(days=day_ago)
   date_two=datetime.datetime.combine(date_one, datetime.time(1, 2, 1)).timestamp()
   return int(date_two)

def on_time(event):
   select_time=int(combo_value.get())
   global value
   Value_combo_tag.clear()
   value=float(select_time*3600/86400)
   list_value_tag()
   note_topic.place_forget()

combo_value = ttk.Combobox(root, values=[6,12,24,48,96,192,384,768],font=('Arial',12,'normal'),width=5)
combo_value.place(relx=0.04,rely=0.21)
combo_value.set(int(6))
combo_value.bind("<<ComboboxSelected>>", on_time)
label_entry_h=tk.Label(root, text="Hours",font=("Arial",12,"normal"))
label_entry_h.place(relx=0.12,rely=0.21)

def search_people():
   if db_list!=[]:
      for db_people in db_list:
         if db_people["pubkey"] not in timeline_people:
            timeline_people.append(db_people["pubkey"])
      list_pubkey_id()
      
button_2=tk.Button(root,text="Metadata Users",command=search_people,font=('Arial',12,'bold'))  #timeline
button_2.place(relx=0.1,rely=0.27)                

def get_note(z):
    f=[]
    import json
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

def tags_present(x,obj):
   f=x["tags"]
   zeta=[]
   if f!=[]:
      for j in f:
         if j[0]==obj:
            zeta.append(j[0])
   return zeta

def evnt_id(id):
   try: 
      test2=EventId.parse(id)
      return test2
   except NostrSdkError as e:
      print(e,"input ",id)

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
               if xtags != "":
                  if jtags not in tags_list:
                    tags_list.append(jtags)
                  break  
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

db_wot_note={}
off_topic_curators={}
user_removals={}

def wot_save():
   test_people=user_convert(list(my_dict.values())) 
   metadata_note=search_kind(test_people,1011)
   if metadata_note:
      for meta_n in metadata_note:
         if meta_n["content"]=="Marked as off-topic":
            if tags_string(meta_n,"e"):
               db_block_event.add(tags_string(meta_n,"e")[0])
               if tags_string(meta_n,"t")[0] in off_topic_curators:
                  topic_set_id=off_topic_curators[tags_string(meta_n,"t")[0]]
                  topic_set_id.add(tags_string(meta_n,"e")[0])
                  off_topic_curators[tags_string(meta_n,"t")[0]]=topic_set_id
               else:   
                  off_topic_curators[tags_string(meta_n,"t")[0]]={tags_string(meta_n,"e")[0]}
         if meta_n["content"]=="Removed user from topic":      
            if tags_string(meta_n,"p"):
               db_block_npub.add(tags_string(meta_n,"p")[0])
               if tags_string(meta_n,"t")[0] in user_removals:
                  topic_set_p=user_removals[tags_string(meta_n,"t")[0]]
                  topic_set_p.add(tags_string(meta_n,"p")[0])
                  user_removals[tags_string(meta_n,"t")[0]]=topic_set_p
               else:   
                  user_removals[tags_string(meta_n,"t")[0]]={tags_string(meta_n,"p")[0]}
         db_wot_note[meta_n["id"]]=meta_n

def recover_mooderation(topic:str):
   dict_topic_p={}
   dict_topic_id={}
   if db_wot_note!={}:
      notes_wot=list(db_wot_note.values())
      note_w_p=[]
      note_w_id=[]
      for note_w in notes_wot:
         if topic in tags_string(note_w,"t")!=[]:
            if tags_string(note_w,"p")!=[]:
               note_w_p.append(note_w)
            if tags_string(note_w,"e")!=[]:
               note_w_id.append(note_w)

      if topic in user_removals:
         for user_x in list(user_removals[topic]):  
            for note_x in note_w_p: 
               if user_x in tags_string(note_x,"p"):
                  if user_x in dict_topic_p:
                     pubclic_mood=dict_topic_p[user_x]            
                     pubclic_mood.add(note_x["pubkey"])
                     dict_topic_p[user_x]=pubclic_mood
                  else:
                     dict_topic_p[user_x]={note_x["pubkey"]}
   
      if topic in off_topic_curators:
         for event_id in list(off_topic_curators[topic]):
            for note_j in note_w_id: 
               if event_id in tags_string(note_j,"e"):
                  if event_id in dict_topic_id:  
                     event_mod=dict_topic_id[event_id]
                     event_mod.add(note_j["pubkey"])
                     dict_topic_id[event_id]=event_mod
                  else:
                     dict_topic_id[event_id]={note_j["pubkey"]}
   return dict_topic_p,dict_topic_id

def search_relay():
   if __name__ == "__main__":
      asyncio.run(outboxes())

async def get_outbox(client):
   if my_list!=[]:
      if my_dict[combo_box.get()] in list(my_dict.values()): 
         f = Filter().authors(user_convert([my_dict[combo_box.get()]])).kinds([Kind(10002),Kind(10015),Kind(0),Kind(1)]).limit(500)
         events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
         z = [event.as_json() for event in events.to_vec() if event.verify()]
         return z

alpha_list_topic=[]
timeline_people=[]
draft_user=[]
relay_list=[]
db_note=[]
search_pubkey_list=[]

async def outboxes():
   init_logger(LogLevel.INFO)
   client = Client(None)
    
   if relay_list!=[]:
      for jrelay in relay_list:
         await client.add_relay(RelayUrl.parse(jrelay))
             
   else:
        await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
        await client.add_relay(RelayUrl.parse("wss://purplerelay.com/"))
        await client.add_relay(RelayUrl.parse("wss://purplepag.es/"))
     
   await client.connect()
   db_note.clear()
   note_result= await get_outbox(client)
   await client.remove_all_relays()
   if note_result!=None:
      relay_add=get_note(note_result)
      if relay_add!=[]:
         i=0
         alpha_topic=set({})
         while i<len(relay_add):
            if relay_add[i]["kind"]==10002:
               for xrelay in tags_string(relay_add[i],'r'):
                  if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay[6:9]!="127":
                     if xrelay not in relay_list:
                        relay_list.append(xrelay) 
                 
            if relay_add[i]["kind"]==10015 and len(alpha_topic)<16:  
               for xtopic in tags_string(relay_add[i],'t'):
                  if str(xtopic).islower():
                        alpha_topic.add(str(xtopic).lower())
                    
            if relay_add[i]["kind"]==1 and tags_string(relay_add[i],'t') and len(alpha_topic)<16:
               
               for xtags in tags_string(relay_add[i],'t'):
                  if len(xtags)<30 and str(xtags).islower():
                     alpha_topic.add(str(xtags).lower()) 
                  
            i=i+1            
         for topic_f in list(alpha_topic):  
               alpha_list_topic.append(topic_f)
         combo_relay['values']=alpha_list_topic    
         await Search_status(client,relay_list)  
   await asyncio.sleep(2.0)

Pubkey_Metadata={}
photo_profile={}
db_list_note_follow=[]

def list_pubkey_id():
  
   if timeline_people !=[]:
      test_people=user_convert(timeline_people)    #not cover people are already on metadata
      metadata_note=search_kind(test_people,0)
      if metadata_note!=[]:
         try: 
            for single in metadata_note:
               if single["pubkey"] not in Pubkey_Metadata:   
                  db_list_note_follow.append(single)
                  name=metadata_0(single,"name")
                  if name:
                     Pubkey_Metadata[single["pubkey"]]=name
                  else:
                     dispay_name=metadata_0(single,"dispay_name")
                     if dispay_name:
                        Pubkey_Metadata[single["pubkey"]]=dispay_name    
                  picture=metadata_0(single,"picture")
                  if picture:
                     photo_profile[single["pubkey"]]=picture
                       
         except KeyError as e:
            print("KeyError ",e) 
         except json.JSONDecodeError as b:
            print(b)                   
      
def search_kind(user,x):
    zeta=[]
    if __name__ == "__main__":
      # Example usage with a single key
      single_author = user 
      single_results = asyncio.run(feed(single_author,x))
      note=get_note(single_results)
      for r in note:
         if (r)['kind']==x:
            zeta.append(r)
    return zeta        

async def get_relays_z(client, authors,x):
   if x==1011:
      f = Filter().authors(authors).kind(Kind(x)).since(Timestamp.from_secs(since_day_time(32)))
   else:   
      f = Filter().authors(authors).kind(Kind(x))
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   return z

async def get_relay_z(client, user,x):
    f = Filter().author(user).kind(Kind(x))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def feed(authors,x):
      
    client = Client(None)
    
    # Add relays and connect
    await client.add_relay(RelayUrl.parse("wss://relay.damus.io/"))
    await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
    
    if relay_list!=[]:
       
      for jrelay in relay_list:
         await client.add_relay(RelayUrl.parse(jrelay))
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_relays_z(client, authors,x)
    else:
        combined_results = await get_relay_z(client, authors,x)
    
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

def selection_mode():
   list_of_search=[]
   list_of_note,list_pubkey=list_topic_tuple()
   if list_pubkey: #if not topic select 
      
      if len(search_pubkey_list)==1:
         if search_pubkey_list[0] in list_pubkey:
            list_of_search.append(search_pubkey_list[0])
            list_pubkey.remove(search_pubkey_list[0])
      for pubkey_x in list_pubkey: 
         if pubkey_x in Pubkey_Metadata and len(list_of_search)<100:
            list_of_search.append(pubkey_x)  
      return list_of_search      
   if list_of_search==[] and len(search_pubkey_list)==1:   #if search for nickname
      
      for people in search_pubkey_list:
         if people in Pubkey_Metadata:
            list_of_search.append(people)
      return list_of_search            
   if len(search_pubkey_list)==0:
      
      for people_x in Pubkey_Metadata:
         if len(list_of_search)<100:
            list_of_search.append(people_x)
   return list_of_search

def layout():
   if Pubkey_Metadata!={}: 
      frame1=Frame(root, width=330, height=100)
      canvas = Canvas(frame1)
      canvas.pack(side="left", fill=BOTH, expand=True)
      scrollbar = Scrollbar(frame1, orient=VERTICAL, command=canvas.yview)
      scrollbar.pack(side=RIGHT, fill=Y)
      canvas.configure(yscrollcommand=scrollbar.set)
      canvas.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
      scrollable_frame = Frame(canvas)
      canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
      s=1  

      def one_note(pubkey):
         for note_text in db_list:
            if note_text["pubkey"]==pubkey:
               show_print_test_tag(note_text)
               close_canvas()
               break 
     
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
                     
      list_of_search=selection_mode()
      for name_pubkey in list_of_search:         
         var_npub =StringVar()
         var_npub.set("Nickname " +str(Pubkey_Metadata[name_pubkey]))
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
         button_test=Button(scrollable_frame, text="Note of tag", command= lambda val=name_pubkey: search_note(val),font=('Arial',12,'normal'))
         button_test.grid(row=s + 5, column=1, padx=2, pady=5)
         s += 6   
         root.update_idletasks() 
      frame1.place(relx=0.65,rely=0.12, relheight=0.45,relwidth=0.35)      

      def close_canvas():
         scrollable_frame.forget()
         canvas.destroy()
         frame1.destroy()
         label_image.place_forget()
         button_close_s.place_forget()
              
      if Pubkey_Metadata=={}:
        close_canvas()    

      button_close_s=Button(root, command=close_canvas, foreground="red",text="X",font=('Arial',12,'normal') )
      button_close_s.place(relx=0.96,rely=0.15)    

button_open=Button(root, command=layout, text="Users on the server",highlightcolor='WHITE',background="grey",font=('Arial',12,'bold'))
button_open.place(relx=0.85,rely=0.02, anchor="n")            

button_open2=Button(root, command=wot_save, text="WoT",highlightcolor='WHITE',background="grey",font=('Arial',12,'bold'))
button_open2.place(relx=0.65,rely=0.02, anchor="n")            

def search_nickname():
   search_pubkey_list.clear()
   if entry_nick.get()!="":
   
      Name_value=list(Pubkey_Metadata.values())
      Name_key=list(Pubkey_Metadata.keys())
      if entry_nick.get() in Name_value:
         for key_x in Name_key:
            if Pubkey_Metadata[key_x]==entry_nick.get():
               print(entry_nick.get(),"\n",key_x)      
               search_pubkey_list.append(key_x)    
               layout()
      else:
         if entry_nick.get() in combo_t_tag:
            combo_tag.set(entry_nick.get())
            if Checkbutton_e.get()==0:
               Checkbutton_e.set(1)   
            topic=type_topic()
            list_ev,list_p=list_topic_tuple()    
            if isinstance(topic,str):
               pass
            else:
               show_print_test(list_ev)
          
label_nick=ttk.Label(root,text="Search Name, Topic", font=('Arial',12,'bold'))
label_nick.place(relx=0.75,rely=0.08)     
entry_nick=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))          
entry_nick.place(relx=0.75,rely=0.12,relwidth=0.12,relheight=0.04) 
button_close_1=Button(root, command=search_nickname, text="Find ",font=('Arial',12,'normal'), fg="blue")
button_close_1.place(relx=0.88,rely=0.12)
db_block_npub=set({})
db_block_event=set({})
button_list=[]

def print_note(entry):
        print(entry)

def reply_root(entry):
   if entry["kind"]==1:
      list_p.clear()
      list_p.append(PublicKey.parse(entry["pubkey"]))
      Get_outbox_relay(10002,list_p)
      if tags_string(entry,"e")!=[]:
         var_entry_first.set(tags_string(entry,"e")[0])
         add_note_idto_comment() 
         var_entry_second.set(entry["id"])
         add_reply_idto_comment()
      else:
         var_entry_first.set(entry["id"])
         var_entry_second.set("")
         add_note_idto_comment()   
                                 
def like_upvote(entry):      
   if messagebox.askokcancel("Add Like ","Yes/No") == True:
      reply_re_action(entry,"good")
   
def like_downvote(entry):      
   if messagebox.askokcancel("Add Dislike ","Yes/No") == True:
      reply_re_action(entry,"bad")   
      db_block_event.add(entry["id"])

def note_of_topic(note,time_created,s):       
   if float(time_created-note["created_at"])/(86400)<value:  
         if note["kind"]==6:
           try:         
               context0= str("RT "+" By "+note["pubkey"][0:9])              
               context1= str(json.loads(note["content"])["content"]+"\n")
               context2= str(json.loads(note["content"])["tags"])
               return context0,context1,context2
           except json.decoder as e:
                   print(e)
         if note["kind"]==1:  
            if note["pubkey"] in Pubkey_Metadata:
               context0=str("Nickname ")+str(Pubkey_Metadata[note["pubkey"]][0:9])
            else: 
               context0=str("Pubkey: "+note['pubkey'][0:9])
            str_time=note_time(note)
            context0=context0+str("\n"+"Time: ")+str(str_time)  
            if Checkbutton_e.get()==1: 
               if combo_tag.get() in tags_string(note,"t"): 
                  if len(tags_string(note,"t"))<6 and note["id"] not in db_block_event and note["pubkey"] not in db_block_npub: 
                     context1=str(note['content']+"\n")
                     tag_note=""
                     for note_x in note["tags"]:
                        tag_note=tag_note+ str(note_x)+"\n"
                     context2=str("[[ Tags ]]"+"\n" +tag_note)
                  else:
                     if len(tags_string(note,"t"))>5:
                        context0=context0+str("\n"+"more tags ")+ str(len(tags_string(note,"t")))
                     else:
                        db_npub,db_event=recover_mooderation(combo_tag.get())
                        if note["pubkey"] in db_npub:  
                           note_value="Removed user from topic \n"
                           for note_x in db_npub[note["pubkey"]]:
                               note_value= note_value+ "by " +str(note_x[0:9]) 
                           context0=context0+str("\n"+"View blocked " +str(note_value) )
                        if note["id"] in db_event:   
                           note_value_e="Marked as off-topic \n"
                           for note_y in db_event[note["id"]]:
                              note_value_e= note_value_e+ "by " +str(note_y[0:9]) 
                           context0=context0+str("\n"+"View blocked " +str(note_value_e) )
                     context1=str("")
                     context2=str("")   
               else:
                  context0=str("")
                  context1=str("")
                  context2=str("")
            else:
               context1=str(note['content']+"\n")
               tag_note=""
               for note_x in note["tags"]:
                  tag_note=tag_note+ str(note_x)+"\n"
               context2=str("[[ Tags ]]"+"\n" +tag_note)  
            return context0,context1,context2

def create_note_topic(list_of_note):
   if Checkbutton_e.get()==1:      
      if len(list_of_note)>100:
         list_of_note1=list_of_note[0:100]
         return list_of_note1
      else:
         list_of_note1=list_of_note
         return list_of_note1
   else:
      list_of_note1=list_of_note[0:100]
      return list_of_note1
    
def show_print_test(list_of_note):
   frame3=tk.Frame(root,height=150)  
   canvas_2 = tk.Canvas(frame3,width=410)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = ttk.Frame(canvas_2,width=380)
   scrollable_frame_2.bind("<Configure>",lambda e: canvas_2.configure(scrollregion=canvas_2.bbox("all")))
   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
     
   def create_list_notes(list_of_note1):
      s=1   
      time_created=int(time.time())  
      for note in list_of_note1:
         if note_of_topic(note,time_created,s):
            context0,context1,context2=note_of_topic(note,time_created,s)
            var_id=StringVar()
            label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=180,font=("Arial",12,"normal"),foreground="grey")
            if context0!="":
               var_id.set(context0)
               label_id.grid(pady=2,column= 2, columnspan=2,row=s,padx=2)
               if context1=="":
                  button_grid4=Button(scrollable_frame_2,text="View", command=lambda val=note: show_print_test_tag(val),width=3,font=("Arial",12,"normal"))
                  button_grid4.grid(row=s,column=4,ipadx=1,pady=5)
               
               if len(tags_string(note,"t"))==2 and Checkbutton_e.get()==1:
                     if combo_tag.get() in tags_string(note,"t"):
                        if tags_string(note,"t").index(combo_tag.get())==0: 
                           button_6 = tk.Button(scrollable_frame_2, text="Subtopic \n"+ str(tags_string(note,"t")[1][0:15]), command=lambda val=tags_string(note,"t")[1]: val_topic_two(val),font=("Arial",12,"bold"),fg="blue",width=10)
                           button_6.grid(column=0,row=s,padx=1,pady=5)
                           context1=""
                           context2=""
                        else:
                           button_6=tk.Button(scrollable_frame_2,text="Topic \n"+ str(tags_string(note,"t")[0][0:15]), command=lambda val=note: Tag_topic(val),font=("Arial",12,"bold"),fg="green",width=10)   
                           button_6.grid(column=0,row=s,padx=1,pady=5)
                     else:
                        context0=""
                        context1=""
                        context2=""
               else:
                     button_6=tk.Button(scrollable_frame_2,text=str(tags_string(note,"t")[0][0:15]), command=lambda val=note: Tag_topic(val),font=("Arial",12,"bold"),width=10)
                     button_6.grid(column=0,row=s,padx=1,pady=5)
               
            if context0!="" and context1!="":
               scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
               scroll_bar_mini.grid( column=4,row=s+1,pady=5,ipady=30)
               second_label10 = tk.Text(scrollable_frame_2, padx=2, height=5, width=32, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
               second_label10.insert(END,context1+"\n"+str(context2))
               scroll_bar_mini.config( command = second_label10.yview )
               second_label10.grid(padx=2, column=0, columnspan=4, row=s+1) 
               button=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val),background="#b0aba6")
               button.grid(column=0,row=s+2,padx=5,pady=5)
               button_grid2=Button(scrollable_frame_2,text="Stamp", command=lambda val=note: print_note(val),background="#b0aba6")
               button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
               button_grid6=Button(scrollable_frame_2, text="Open Thread", command=lambda val=note: respond_to(val),background="#b0aba6")
               button_grid6.grid(row=s + 2, column=2, padx=5, pady=5)
               button_grid3=Button(scrollable_frame_2,text="Reply", command=lambda val=note: reply_root(val),background="#b0aba6")
               button_grid3.grid(row=s+2,column=3,padx=5,pady=5)
               button_grid4=Button(scrollable_frame_2,text=" ⬆️", foreground="#0096FF",command=lambda val=note: like_upvote(val),width=3,font=("Arial",12,"normal"))
               button_grid4.grid(row=s,column=4,ipadx=1,pady=5)
               button_grid5=Button(scrollable_frame_2,text=" ⬇️", foreground="#0096FF",command=lambda val=note: like_downvote(val),width=3, font=("Arial",12,"normal"))
               button_grid5.grid(row=s+2,column=4,ipadx=1,pady=5)   
            s=s+3
      root.update_idletasks()

   def val_topic_two(topic):
      if topic in combo_t_tag:
         combo_tag.set(topic)
         tag_topic_print()

   def Tag_topic(entry):
      if tags_string(entry,"t")!=[]:
         combo_tag.set(str(tags_string(entry,"t")[0]).lower())
         tag_topic_print()

   def tag_topic_print():
      if Checkbutton_e.get()==0:
            Checkbutton_e.set(1) 
      list_ev,list_p=list_topic_tuple()         
      topic=type_topic()
      if isinstance(topic,str):
         pass
      else:
         frame3.destroy()
         show_print_test(list_ev) 
   
   def close_frame():
      frame3.destroy()
      note_topic.config(text="")   
      for button_x in button_list:
         button_x.place_forget()  
   
   if db_list!=[]:
      of_note_=create_note_topic(list_of_note)
      create_list_notes(of_note_)
      button_frame=Button(scrollable_frame_2,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
      button_frame.grid(row=0,column=0,padx=5,pady=5)
      if Checkbutton_e.get()==0:
         number_x=len(db_list)-len(list_of_note)
         number_x+=100       
         if number_x> len(db_list):
            number_x=0
         button_more=Button(root,command=lambda: show_print_test(db_list[number_x:]),text="More",font=("Arial",12,"normal"))   
         button_more.place(relx=0.3,rely=0.65)
         button_list.append(button_more)
      else:
         if len(list_of_note)>100:
            number_z= 100
            button_more=Button(root,command=lambda: show_print_test(list_of_note[number_z:]),text="More",font=("Arial",12,"normal"))         
            button_more.place(relx=0.3,rely=0.65)   
            button_list.append(button_more)    
      frame3.place(relx=0.22,rely=0.12,relwidth=0.38,relheight=0.5 ) 
      scrollbar_2.pack(side="right", fill="y",pady=20) 
      canvas_2.pack( fill="y", expand=True)  

def print_var(entry):
   if entry["tags"]!=[]:
      photo_print(entry)

button_id=tk.Button(root,command=lambda: show_print_test(db_list),text="Feed", background="grey",font=("Arial",12,"bold"))
button_id.place(relx=0.25,rely=0.05)
Checkbutton_e = IntVar()
combo_t_tag=[]
Checkbutton_e.set(0)
note_topic = tk.Label(root, text="",font=('Arial',14,'normal'))

def list_topic_tuple():
   
   if combo_tag.get()!="Tag List" and combo_tag.get().startswith("Number")==False:
      pubkey_topic=[]
      topic_list=[]
      topic=combo_tag.get()
      for note_x in db_list:
         if float(int(time.time())-note_x["created_at"])/(86400)<value:
            if topic in tags_string(note_x,"t"):
               if note_x not in topic_list:
                  topic_list.append(note_x)
                  if note_x["pubkey"] not in pubkey_topic:
                     pubkey_topic.append(note_x["pubkey"])   
      return topic_list,pubkey_topic                
   else:
      return None,None

def type_topic():
   
   if combo_tag.get()!="Tag List" and combo_tag.get().startswith("Number")==False:
      pubkey_topic=[]
      topic_list=[]
      topic=combo_tag.get()
      for note_x in db_list:
         if float(int(time.time())-note_x["created_at"])/(86400)<value:
            if topic in tags_string(note_x,"t"):
               if note_x not in topic_list:
                  topic_list.append(note_x)
                  if note_x["pubkey"] not in pubkey_topic:
                     pubkey_topic.append(note_x["pubkey"])    
      if len(pubkey_topic)>1:
         if len(pubkey_topic)>10:
            note_topic.config(text= "Number of note is "+ str(len(topic_list))+"\n"+"Main topic,"+"\n"+ "Pubkey in " +str(len(pubkey_topic)))
            note_topic.place(relx=0.45,rely=0.01)          
         else:
            note_topic.config(text= "Number of note is "+ str(len(topic_list))+"\n"+"Low engagement topic,"+"\n"+ "Pubkey in " +str(len(pubkey_topic)))
            note_topic.place(relx=0.45,rely=0.01)          
      else:
         if topic_list!=[]:
            note_topic.config(text= "Number of note is "+ str(len(topic_list)))
            note_topic.place(relx=0.45,rely=0.05)          
         else:
            note_topic.config(text="") 
            note_topic.place_forget()
            return str("zero")      

def list_value_tag():
   for topic in combo_t_tag:
      topic_list=[]
      pubkey_topic=[]
      for note_x in db_list:
         if float(int(time.time())-note_x["created_at"])/(86400)<value:
            if topic in tags_string(note_x,"t") and len(tags_string(note_x,"t"))<6:
               if note_x not in topic_list:
                  topic_list.append(note_x)
                  if note_x["pubkey"] not in pubkey_topic:
                     pubkey_topic.append(note_x["pubkey"])    
      if len(pubkey_topic)>1:
         if len(pubkey_topic)>10:
            Value_combo_tag[topic]=["Main topic","Number of note is "+ str(len(topic_list))+ " Pubkey in " +str(len(pubkey_topic))]
         else:
             Value_combo_tag[topic]= ["Low engagement topic","Number of note is "+ str(len(topic_list))+ " Pubkey in " +str(len(pubkey_topic))]
      else:
         if topic_list!=[]:
            Value_combo_tag[topic]= ["","Number of note is "+ str(len(topic_list))]
   note_value=str("Main topic")
   number=1        
   for topic_str in Value_combo_tag:
        if Value_combo_tag[topic_str][0]=="Main topic":
           note_value=note_value +"\n" +" n° "+ str(number)+ " "+str(topic_str) +"   "+ str(Value_combo_tag[topic_str][1])
           number=number+1
   if number<1:       
     value_topic.config(text=note_value)
     value_topic.place(relx=0.05,rely=0.7)      

value_topic = tk.Label(root, text="",font=('Arial',14,'normal'))

def Search_select(event):
   if Checkbutton_e.get()==0:
    Checkbutton_e.set(1)
   list_ev,list_p=list_topic_tuple()    
   topic=type_topic()
   if isinstance(topic,str):
       pass
   else:
      show_print_test(list_ev) 

def Restore(event):
   Checkbutton_e.set(0)   
   if combo_t_tag!=[]:
      note_topic.place_forget()          
      combo_tag.set("Number of topic "+ str(len(combo_t_tag)))
      combo_t_tag.sort()
      combo_tag['values']=combo_t_tag
    
combo_tag = ttk.Combobox(root, values=combo_t_tag,font=('Arial',12,'normal'),width=18)
combo_tag.place(relx=0.3,rely=0.05,relheight=0.045)
combo_tag.set("Tag List")
combo_tag.bind("<<ComboboxSelected>>", Search_select)
combo_tag.bind('<Button-3>', Restore) 

#NIP-22 section
Reply_frame = ttk.LabelFrame(root, text="Reply Post", labelanchor="n", padding=10)
var_entry_first=StringVar()
var_entry_second=StringVar()
entry_first_note=ttk.Entry(root,justify='left',textvariable=var_entry_first)
entry_first_note.place(relx=0.04,rely=0.55)
entry_second_note=ttk.Entry(root,justify='left',textvariable=var_entry_second)
entry_second_note.place(relx=0.04,rely=0.6)
comment_frame = ttk.LabelFrame(root, text="Comment Post", labelanchor="n", padding=10)
preview_c_frame = ttk.LabelFrame(root, text="Preview Post", labelanchor="n", padding=10)
note_c_tag = tk.Label(root, text="Note",font=('Arial',12,'normal'))
entry_c_4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
enter_c_note = tk.Label(root, text="Comment Note")
entry_c_note=ttk.Entry(root,justify='left')
enter_c_root = tk.Label(root, text="Root Note")
entry_c_root=ttk.Entry(root,justify='left')
note_title=ttk.Entry(root,justify='center', font=('Arial',12,'normal'))
entry_note=ttk.Entry(root,justify='left')

note_tag1 = tk.Label(root, text="e"+" event_id",font=('Arial',12,'normal'))
note_c_tag1 = tk.Label(root, text="e"+" event_id",font=('Arial',12,'normal'))
button_pre=Button(root,text="Preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))
button_pre_t=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))
button_pre_c=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))
close_=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))
close_t=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))
close_c=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))
label_title=tk.Label(root, text="Title ",font=('Arial',12,'normal'))

def add_note_idto_comment():
    if entry_first_note.get()!="" and evnt_id(entry_first_note.get())!=None:
      if root_thread_list==[]:
         root_thread_list.append(entry_first_note.get())
      else:
         root_thread_list.clear()
         root_thread_list.append(entry_first_note.get())  
      print(root_thread_list)

def add_reply_idto_comment():
   if entry_second_note.get()!="" and evnt_id(entry_second_note.get())!=None:
      if first_reply==[]:
        first_reply.append(entry_second_note.get())
      else:
         first_reply.clear()
         first_reply.append(entry_second_note.get())  
      print(first_reply)

button_reply_event=Button(root,text="Insert ID", command=add_note_idto_comment)
#button_reply_event.place(relx=0.15,rely=0.495)

root_thread_list=[]
first_reply=[]
other_reply=[]

def third_open():
   if root_thread_list!=[] and first_reply!=[]: 
      note_c_tag1['text']="id " +first_reply[0][0:9]
      entry_c_note.delete(0, END)
      entry_c_root.delete(0, END)
      entry_c_note.insert(0, first_reply[0])
      entry_c_root.insert(0, root_thread_list[0])
      comment_frame.place(relx=0.4,rely=0.65,relwidth=0.3,relheight=0.33,anchor='n' )
      note_c_tag.place(relx=0.44,rely=0.69,relwidth=0.1,anchor='n' )
      entry_c_4.place(relx=0.4,rely=0.75,relwidth=0.25,relheight=0.1,anchor='n' )
         #entry_layout-right
      enter_c_note.place(relx=0.35,rely=0.91,relwidth=0.1,anchor='n' )
      entry_c_note.place(relx=0.45,rely=0.91,relwidth=0.1,anchor='n')
      enter_c_root.place(relx=0.35,rely=0.95,relwidth=0.1,anchor='n' )
      entry_c_root.place(relx=0.45,rely=0.95,relwidth=0.1,anchor='n')
      note_c_tag1.place(relx=0.5,rely=0.69,anchor='n' )
      close_c["command"] = close_comment
      close_c.place(relx=0.6,rely=0.65,anchor='n' )

      def Preview():
         if entry_c_4.get()!="": 
            frame1=Frame(root, width=310, height=100)
            canvas = Canvas(frame1)
            canvas.pack(side="left", fill=BOTH, expand=True)
            canvas.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
               # Frame scrollabile
            scrollable_frame = Frame(frame1)
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            def create_note(note_text, s):
               if len(note_text)<241:
                  message = Message(scrollable_frame, text=note_text, width=280, font=('Arial',12,'normal'))
                  message.grid(row=s, column=0, columnspan=3, padx=5, pady=10)
                  Button(scrollable_frame, text="Print Note", command=lambda: share(note_text)).grid(row=0, column=2, padx=5, pady=5)
               else:
                  message = Message(scrollable_frame, text=note_text[0:240]+"...", width=280, font=('Arial',12,'normal'))
                  message.grid(row=s, column=0, columnspan=3, rowspan=2, padx=5, pady=10)
                  Button(scrollable_frame, text="Print Note", command=lambda: share(note_text)).grid(row=0, column=2, padx=5, pady=5)
            s = 1
            while s<2:
               if entry_c_4.get()!="":
                  create_note(entry_c_4.get(), s)
                  s += 2   
            frame1.place(relx=0.02,rely=0.7, relheight=0.3,relwidth=0.2)  

            def close_canvas():
               scrollable_frame.forget()
               canvas.destroy()
               frame1.destroy()
           
            button_c_close=Button(scrollable_frame, command=close_canvas, text="Close X")
            button_c_close.grid(column=1,row=0, padx=10,pady=10)   
        
      button_pre_c["command"]= Preview
      button_pre_c.place(relx=0.35,rely=0.85,relwidth=0.1,relheight=0.05, anchor="n") 
      button_reply_c.place(relx=0.45,rely=0.85,relwidth=0.1,relheight=0.05,anchor='n' )
        
button_create=Button(root,text="Re Comment", command=third_open)
button_create.place(relx=0.15,rely=0.6)

def share(note_text):
    print(f"Note: \n {note_text}")

preview_frame = ttk.LabelFrame(root, text="Preview Post", labelanchor="n", padding=10)
note_tag = tk.Label(root, text="Note",font=('Arial',12,'normal'))
entry4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
enter_note = tk.Label(root, text="Root Note")
entry_note=ttk.Entry(root,justify='left')

def reply_note():
   if entry4.get()!="" and entry_note.get()!="": 
      note=entry4.get()
      tag=reply_note_comment()
      if tag!=None:
         if __name__ == '__main__':
            asyncio.run(reply(note,tag))
         close_answer()

button_reply=tk.Button(root,text="send reply", background="darkgrey", command=reply_note, font=('Arial',12,'normal'))

def second_reply():
   if entry_c_4.get()!="":
      note=entry_c_4.get()
      tag=round_3_comment()
      if len(tag)==2 and tag!=None:  
         if __name__ == '__main__':
            asyncio.run(the_second_reply(note,tag[0],tag[1]))  #need to check if tag[0] is the reply and tag[1] is th
      else:
         print(len(tag),"\n", tag) 
      close_comment()

button_reply_c=tk.Button(root,text="send comment", background="darkgrey", command=second_reply, font=('Arial',12,'normal'))

#entry_layout

def close_comment():
   button_reply_c.place_forget() 
   comment_frame.place_forget()
   button_pre_c.place_forget()  
   note_c_tag.place_forget()  
   entry_c_4.place_forget()
   enter_c_note.place_forget()
   entry_c_note.place_forget()
   note_c_tag1.place_forget()
   close_c.place_forget()
   entry_c_4.delete(0, END)
   enter_c_root.place_forget()
   entry_c_root.place_forget()

def close_answer():
   button_reply.place_forget() 
   Reply_frame.place_forget()
   button_pre.place_forget()  
   note_tag.place_forget()  
   entry4.place_forget()
   enter_note.place_forget()
   entry_note.delete(0, END)
   entry_note.place_forget()
   note_tag1.place_forget()
   close_.place_forget()
   entry4.delete(0, END)

def reply_note_comment():   
   if entry_note.get()!="":
      event=entry_note.get()
      search_id=evnt_id(event)
      found_nota=asyncio.run(Get_id(search_id))
      if found_nota!=[]:
         return found_nota[0]
  
def round_3_comment():      #have the root and the comment
   if entry_c_note.get()!="" and entry_c_root.get()!="":
      search_list_id=[]
      event=entry_c_note.get()
      search_id=evnt_id(event)
      search_id_2=evnt_id(entry_c_root.get())
      search_list_id.append(search_id) 
      search_list_id.append(search_id_2)
      found_nota=asyncio.run(Get_id(search_list_id))
      return found_nota  

def found_root(note):
   try_note=get_note(note)
   Test_root=[]
   if tags_string(try_note[0],"a")!=[]:
     test_note=asyncio.run(Get_coord_url(str(tags_string(try_note[0],"a")[0])))
     return test_note
   if tags_string(try_note[0],"e")!=[]:
     found_nota=asyncio.run(Get_id(tags_string(try_note[0],"e")))
     return found_nota
   if tags_string(try_note[0],"i")!=[]:
     print(tags_string(try_note[0],"i")[0])          

def round_comment_reply():      #have the root and the comment
   if entry_c_note.get()!="":
      search_list_id=[]
      event=entry_c_note.get()
      search_id=evnt_id(event)
      search_list_id.append(search_id) 
      found_nota=asyncio.run(Get_id(search_list_id))
      found_nota.append(found_root(found_nota))
      return found_nota    
  
async def reply(note,tag):
   key_string=log_these_key()
   if key_string!=None: 
      keys = Keys.parse(key_string)
      signer=NostrSigner.keys(keys)
      client = Client(signer)
      if outbox_list!=[]:
         for jrelay in outbox_list:
            await client.add_relay(RelayUrl.parse(jrelay))
      if relay_list!=[]:
         for j_relay in relay_list:
            await client.add_relay(RelayUrl.parse(j_relay))            
      else:
         await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
         await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
      await client.connect()
      event_to_comment:dict=tag
      if event_to_comment!=NONE:
         if Event.from_json(f"{event_to_comment}").kind().as_u16()!=(1):    
            print(Event.from_json(f"{event_to_comment}").kind().as_u16()) 
            if outbox_list!=[]:
               builder =EventBuilder.text_note_reply(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_comment}"),RelayUrl.parse(outbox_list[0]))
            else:
               builder =EventBuilder.text_note_reply(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_comment}"),None)
            test = await client.send_event_builder(builder)
            if len(test.success)>0:   
               print("Event sent:")      
               if first_reply==[]:
                     pass
               else:
                  first_reply.clear()    
               f = Filter().authors([keys.public_key()]).limit(10)
               events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
               for event in events.to_vec():
                  print(event.as_json())

async def the_second_reply(note,tag, root):
   key_string=log_these_key()
   if key_string!=None: 
      keys = Keys.parse(key_string)
      signer = NostrSigner.keys(keys)
      client = Client(signer)
      if outbox_list!=[]:
         for jrelay in outbox_list:
            await client.add_relay(RelayUrl.parse(jrelay))
      if relay_list!=[]:
         for j_relay in relay_list:
            await client.add_relay(RelayUrl.parse(j_relay))      
      else:
         await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
         await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
      await client.connect()
      event_to_comment:dict=tag
      event_to_start:dict=root
      if event_to_comment!=NONE and event_to_start!=None:
         if Event.from_json(f"{event_to_comment}").kind().as_u16()==1:
            if Event.from_json(f"{event_to_start}").kind().as_u16()== 1:
               if outbox_list!=[]:
                  builder =EventBuilder.text_note_reply(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_start}"),RelayUrl.parse(outbox_list[0]))
               else:
                  builder =EventBuilder.text_note_reply(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_start}"),None)
               test= await client.send_event_builder(builder)
               if other_reply==[]:
                  other_reply.append(test.id.to_hex())
               else:
                  other_reply.append(test.id.to_hex())
      
      await asyncio.sleep(2.0)
      
      f = Filter().authors([keys.public_key()]).kinds([Kind(1),Kind(7)]).limit(10)
      events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
      for event in events.to_vec():
         if event.verify():
            print(event.as_json())

async def get_more_Event(client, event_list):
    f = Filter().ids(event_list)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_one_Event(client, event_):
    f = Filter().id(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_id(event_):
   client = Client(None)
   if relay_list!=[]:
      for jrelay in relay_list:
         await client.add_relay(RelayUrl.parse(jrelay))
   else:
      await client.add_relay(RelayUrl.parse("wss://nostr.mom"))
      await client.add_relay(RelayUrl.parse("wss://nos.lol"))
      await client.add_relay(RelayUrl.parse("wss://relay.primal.net"))
   await client.connect()
   await asyncio.sleep(2.0)

   if isinstance(event_, list):
        test_kind = await get_more_Event(client, event_)
   else:
        test_kind = await get_one_Event(client, event_)
   return test_kind

def test_open():
   if root_thread_list!=[]:
      note_tag1['text']="id " +root_thread_list[0][0:9]
      entry_note.insert(0, root_thread_list[0])
      Reply_frame.place(relx=0.4,rely=0.65,relwidth=0.3,relheight=0.33,anchor='n' )
      note_tag.place(relx=0.4,rely=0.68,anchor='n' )
      entry4.place(relx=0.4,rely=0.75,relwidth=0.25,relheight=0.1,anchor='n' )
         #entry_layout-right
      enter_note.place(relx=0.3,rely=0.95,relwidth=0.1 )
      entry_note.place(relx=0.4,rely=0.95,relwidth=0.1)
      note_tag1.place(relx=0.47,rely=0.68,anchor='n' )
      close_["command"] = close_answer
      close_.place(relx=0.6,rely=0.68,anchor='n' )
    
      def Preview():
         if entry4.get()!="":
            frame1=Frame(root, width=310, height=100)
            canvas = Canvas(frame1)
            canvas.pack(side="left", fill=BOTH, expand=True)
            canvas.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
               # Frame scrollabile
            scrollable_frame = Frame(frame1)
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
            def create_note(note_text, s):
          
               if len(note_text)<241:
                  message = Message(scrollable_frame, text=note_text, width=240, font=('Arial',12,'normal'))
                  message.grid(row=s, column=0, columnspan=3, padx=5, pady=10)
                  Button(scrollable_frame, text="Print Note", command=lambda: share(note_text)).grid(row=0, column=2, padx=5, pady=5)
               else:
                  message = Message(scrollable_frame, text=note_text[0:240]+"...", width=240, font=('Arial',12,'normal'))
                  message.grid(row=s, column=0, columnspan=3, rowspan=2, padx=5, pady=10)
                  Button(scrollable_frame, text="Print Note", command=lambda: share(note_text)).grid(row=0, column=2, padx=5, pady=5)
          
            s = 1
            while s<2:
               if entry4.get()!="":
                  create_note(entry4.get(), s)
               s += 2   
            frame1.place(relx=0.02,rely=0.65, relheight=0.35,relwidth=0.2)  
         
            def close_canvas():
               frame1.destroy()

            button_close=Button(scrollable_frame, command=close_canvas, text="Close X")
            button_close.grid(column=1,row=0, padx=10,pady=10)    
      
      button_pre["command"]= Preview
      button_pre.place(relx=0.35,rely=0.88,relwidth=0.1, anchor="n") 
      button_reply.place(relx=0.45,rely=0.88,relwidth=0.1,relheight=0.05,anchor='n' )
        
button_create=Button(root,text="Reply Root", command=test_open)
button_create.place(relx=0.15,rely=0.55)

async def get_nostr_tags(client, event_kind,event_identifier,event_publickey):
   f = Filter().kind(event_kind).author(event_publickey).identifier(event_identifier)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec()]
   return z

async def get_one_nostr_tags(client, event_kind,event_identifier,event_publickey):
   f =Filter().kind(event_kind).author(event_publickey).identifier(event_identifier)    
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
   z = [event.as_json() for event in events.to_vec()]
   return z

async def Get_coord_url(value):
    
   client = Client(None)
    
   event_kind = Coordinate.parse(value).kind()
   event_identifier = Coordinate.parse(value).identifier()
   event_publickey = Coordinate.parse(value).public_key()
   await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
   await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
   await client.try_connect(timeout=timedelta(seconds=10))
   await asyncio.sleep(2.0)
   await client.connect()
    
   if isinstance(value, list):
         print("list0")
         test_id = await  get_nostr_tags(client,event_kind,event_identifier,event_publickey)
   else:
        print("str0")
        test_id = await get_one_nostr_tags(client,event_kind,event_identifier,event_publickey)
       
   return test_id      

def test_relay(): 
   if combo_relay["values"]!=[] or combo_relay.get()!="":
      tm=note_list_r()
      print(len(tm))
      return tm
  
def note_list_r():
   let=[]
   if __name__ == "__main__":
      combined_results = asyncio.run(main_feed())
      if combined_results:
         let=get_note(combined_results)
   return let

Value_combo_tag={}

def search_():
   result=test_relay()
   if result !=None:
      global db_list
      db_list_=timeline_created(db_list,result)
      for db_x in db_list_:
         if db_x["kind"]==10015:
            print(db_x)
         if tags_string(db_x,"t")!=[] and len(tags_string(db_x,"t"))<6:
            for tags_t in tags_string(db_x,"t"):
               if str(tags_t).islower()  and str(tags_t).lower() not in combo_t_tag:
                     combo_t_tag.append(str(tags_t).lower())     
            
      if combo_t_tag!=[]:   
         list_value_tag()
         combo_tag.set("Number of topic "+ str(len(combo_t_tag)))      
         combo_t_tag.sort()    
         combo_tag['values']=combo_t_tag

def Block_space():
   if list_event!=[]: 
      frame1=Frame(root, width=200, height=50)
      canvas = Canvas(frame1, width=150, height=30)
      canvas.pack(side="left", fill=BOTH, expand=True)
      scrollbar = Scrollbar(frame1, orient=VERTICAL, command=canvas.yview)
      canvas.configure(yscrollcommand=scrollbar.set)
      canvas.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
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
               print(entry_kind.get())     

      blo_add = Button(root, text="ADD", command=add_event)
      blo_add.place(relx=0.7,rely=0.9)
      entry_kind.place(relx=0.75,rely=0.9,relheight=0.03)       

      s = 1
      for nblock in list_event: 
         create_note(nblock, s)
         s += 3   
    
      frame1.place(relx=0.7,rely=0.7, relheight=0.15,relwidth=0.21)  
    
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
outbox_list=[]
public_list=[]
list_event=[Kind(1)]
button_tm=tk.Button(root,command= search_,text="View note", font=("Arial",12,"normal"))
button_tm.place(relx=0.03,rely=0.27)

async def get_note_relays(client):
   if combo_relay.get()=="":
      f = Filter().kinds(list_event).hashtags(combo_relay["values"]).since(Timestamp.from_secs(since_day_time(32))).limit(500)
   else:
      f = Filter().kinds(list_event).hashtag(combo_relay.get()).limit(100)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify() and len(event.tags().hashtags())<int(6)]
   return z

async def main_feed():
      # Init logger
   
   client = Client(None)
     # Add relays and connect
   await Search_status(Client(None),relay_list) 
   if relay_list!=[]:
      
      for relay_x in relay_list:
            relay_url = RelayUrl.parse(relay_x)
            await client.add_relay(relay_url)

      await client.connect()
      await asyncio.sleep(1.0)
      combined_results = await get_note_relays(client)
      return combined_results

def respond_to(note_text):
   show_print_test_tag(note_text)

def reply_to(entry):
   if entry["kind"]==1:
      list_p.clear()
      list_p.append(PublicKey.parse(entry["pubkey"]))
      Get_outbox_relay(10002,list_p)
      
      if tags_string(entry,"e")!=[]:
         var_entry_first.set(tags_string(entry,"e")[0])
         add_note_idto_comment() 
         var_entry_second.set(entry["id"])
         add_reply_idto_comment()
      else:
         var_entry_first.set(entry["id"])
         var_entry_second.set("")
         add_note_idto_comment()      

def show_print_test_tag(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = tk.Frame(canvas_2, background="#E3E0DD")
   scrollable_frame_2.bind(
   "<Configure>",lambda e: canvas_2.configure(scrollregion=canvas_2.bbox("all")))
   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   
   def create_note(note,s):
      var_id_3=StringVar()
      label_id_3 = Message(scrollable_frame_2,textvariable=var_id_3, relief=RAISED,width=290,font=("Arial",12,"normal"))
      label_id_3.grid(pady=1,padx=8,row=s,column=0, columnspan=3)
      str_time=note_time(note)
      #some label if there are 
      if note["pubkey"] in Pubkey_Metadata:
         var_id_3.set("Nickname " +str(Pubkey_Metadata[note["pubkey"]][0:9])+"\n" +"Time: "+str(str_time))
      else:
         var_id_3.set("Pubkey: "+note["pubkey"][0:9]+"\n" +"Time: "+str(str_time))
      scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
      scroll_bar_mini.grid( sticky = NS,column=4,row=s+1)
      second_label_10 = tk.Text(scrollable_frame_2, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
      context2=""  
      if tags_string(note,"t")!=[]:
            hashtag_note=str("") 
            for note_tags in tags_string(note,"t"):
               hashtag_note=hashtag_note+str("#")+str(note_tags)+" "
            context2=context2 +hashtag_note+"\n"
      if tags_string(note,"e")!=[]:
            if four_tags(note,"e"):
               for F_note in four_tags(note,"e"):
                  context2=context2+str(" < "+ F_note[0]+" > ")+F_note[1][0:9]+ "\n"        
        
      second_label_10.insert(END,note["content"]+"\n"+str(context2))
      scroll_bar_mini.config( command = second_label_10.yview )
      second_label_10.grid(padx=10, column=0, columnspan=3, row=s+1) 
      button=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s+2,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_2,text=f"Print", command=lambda val=note: print(val))
      button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
      if tags_string(note,"e")!=[]: 
         button_grid3=Button(scrollable_frame_2,text=f"Read reply ", command=lambda val=note: print_content(val))
         button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    
      else:
         button_grid3=Button(scrollable_frame_2,text=f"Read rootply ", command=lambda val=note: print_content(val))
         button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    

   def print_content(entry):
      result=show_note_from_id(entry)
      z=4
      if result: 
         for jresult in result[::-1]:
            if jresult["id"]!=entry["id"]:  
               var_id_r=StringVar()
               label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
               label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
               str_time_1=note_time_reply(entry,jresult)
               if jresult["pubkey"] in list(Pubkey_Metadata.keys()):
                  var_id_r.set("Nickname " +str(Pubkey_Metadata[jresult["pubkey"]][0:9])+"\n" +"Time: "+str(str_time_1))
               else:
                  var_id_r.set(" Pubkey: "+jresult["pubkey"][0:9]+"\n" +"Time: "+str(str_time_1))
               scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
               scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
               second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
               context22="\n"+ " -Tags: "+"\n"   
               if tags_string(jresult,"e")!=[]:
                  if four_tags(jresult,"e"):
                     for F_note in four_tags(jresult,"e"):
                        context22=context22+str(" < "+ F_note[0]+" > ")+F_note[1][0:9]+ "\n"
                        if F_note[2]!="" and F_note[2] not in relay_list:
                           relay_list.append(F_note[2])
               if tags_string(jresult,"p")!=[]:
                  for Pr in tags_string(jresult,"p"):
                     if Pr in Pubkey_Metadata:
                        context22=context22+"person in the reply " +str(Pubkey_Metadata[Pr])+ "\n"
                     else: 
                        context22=context22+str("person in the reply ")+Pr[0:9]+ "\n"    
               second_label10_r.insert(END,jresult["content"]+"\n"+str(context22))
               scroll_bar_mini_r.config( command = second_label10_r.yview )
               second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
               button_photo=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=jresult: print_var(val))
               button_photo.grid(column=0,row=z+2,padx=5,pady=5)
               button_print=Button(scrollable_frame_2,text=f"Print ", command=lambda val=jresult: print(val))
               button_print.grid(column=1,row=z+2,padx=5,pady=5)
               button_grid4=Button(scrollable_frame_2,text=f"Comment ", command=lambda val=jresult: reply_to(val))
               button_grid4.grid(row=z+2,column=2,padx=5,pady=5)        
            z=z+3
    
   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
 
   def close_frame():
      frame3.destroy()    
   
   if isinstance(note,dict):
      s=1
      create_note(note,1)

   button_frame=Button(frame3,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.pack()   
   frame3.place(relx=0.65,rely=0.2,relheight=0.4,relwidth=0.3) 

def show_note_from_id(note):
   result=note["id"]
   replay=nota_reply_id(note)
   if replay!=[]:
      items=get_note(asyncio.run(Get_event_id(replay)))
   else:
      items=get_note(asyncio.run(Get_event_id(result)))
   return items   

def nota_reply_id(nota):
   e_id=[]
   if tags_string(nota,'e')!=[]:
      for event_id in tags_string(nota,'e'):
         if event_id not in e_id:
            e_id.append(event_id)
      if e_id==[]:
         for event_q in tags_string(nota,'q'):
            if event_q not in e_id and len(event_q)==64:
               e_id.append(event_id)                  
   return e_id          

async def get_notes_(client, e_ids):
     f = Filter().ids([EventId.parse(e_id) for e_id in e_ids])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec() if event.verify()]
     return z

async def get_one_note(client, e_id):
    f = Filter().event(EventId.parse(e_id)).kinds([Kind(1)]).limit(100)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_event_id(e_id):
    # Init logger
 
   client = Client(None)
   if relay_list!=[]:
      try: 
       for jrelay in relay_list:
         
         await client.add_relay(RelayUrl.parse(jrelay))
      except NostrSdkError as e:
         print(e)   
   else:
      await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
      await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
      await client.add_relay(RelayUrl.parse("wss://purplerelay.com/"))

   await client.connect()
   await asyncio.sleep(2.0)

   if isinstance(e_id, list):
      test_id = await get_notes_(client,e_id)
   else:
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

def note_time(note):
   time_str=float(int(time.time())-note["created_at"])
   value=int(time_str/(60))
   if value>1440:
         if value>2880:
            return str(int(time_str/(86400)))+str(" days ago") 
         else:
            return str(int(time_str/(86400)))+str(" day ago") 
   else:
         if value>120:   
            return str(int(float(int(time_str/(3600)))))+str(" hours ago") 
         else:
            time_result=float(int(time.time()-note["created_at"]))  
            return "Time: "+str(int(float(time_result/3600)))+" Hour  & " +str(int(time_result/60)-int(time_result/(3600))*60)+" Minutes ago"
              
def note_time_reply(note,reply):
   time_str=float(reply["created_at"]-note["created_at"])
   value=int(time_str/(60))
   if value>1440:
      if value>2880:
         return str(int(time_str/(86400)))+str(" days later") 
      else:
         return str(int(time_str/(86400)))+str(" day later") 
   if value<0:
      time_result=float(int(note["created_at"]-reply["created_at"]))  
      str_time="Time: "+str(int(float(time_result/3600)))+" Hour  & " +str(int(time_result/60)-int(time_result/(3600))*60)+" minutes before"
      return str_time
   if value<1440 and value>0:
      time_result=float(int(reply["created_at"]-note["created_at"]))  
      str_time="Time: "+str(int(float(time_result/3600)))+" Hour  & " +str(int(time_result/60)-int(time_result/(3600))*60)+" Minutes later"
      return str_time

def search_note(entry):
   result_note=[]
   for note_x in db_list:
      if note_x["pubkey"]==entry:
         result_note.append(note_x)   

   if len(result_note)>1:
         print(len(result_note))
         show_print_test(result_note)
         
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
              for xrelay in tags_string(relay_user[i],'r'):
               if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay[6:9]!="127":
               
                if xrelay not in outbox_list:
                 outbox_list.append(xrelay)
            i=i+1     

list_p=[]

async def Get_event_from(event_):
   client = Client(None)

    # Add relays and connect
   relay_url_1=RelayUrl.parse("wss://nostr.mom/")
   relay_url_2=RelayUrl.parse("wss://relay.damus.io/")
   await client.add_relay(relay_url_1)
   await client.add_relay(relay_url_2)
    
   if relay_list!=[]:
      for xrelay in relay_list:
         await client.add_relay(RelayUrl.parse(xrelay))
   await client.connect()
   await asyncio.sleep(2.0)
     
   if isinstance(event_, list):
      test_kind = await get_kind(client, event_)
      if test_kind:
         return test_kind    
   else:
      print("error")

async def get_kind(client, event_):
   try:   
      if public_list!=[]:
         f = Filter().kinds(event_).author(public_list[0])
      else:
         f = Filter().kinds(event_).limit(50)
      events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10)) 
      z=[] 
      for event in events.to_vec():
         if event.verify_signature():
            z.append(event.as_json())
      if z:      
         return z
   except NostrSdkError as e:
       print (e)

def reply_re_action(note,behaviuour):
  
   test = EventId.parse(note["id"])
   public_key=convert_user(note["pubkey"])
   if public_key:
      if __name__ == '__main__':
         if behaviuour=="good":
            note_rea="⬆️"
         else:
            note_rea="⬇️"     
         type_event=Kind(int(note["kind"]))
         asyncio.run(reply_reaction(test,public_key,note_rea,type_event))    

def reply_re_action(note,behaviuour):
   if behaviuour=="good":
      note_rea="⬆️"
   else:
      note_rea="⬇️"     
   if __name__ == '__main__':   
      asyncio.run(reply_reaction(note,note_rea))    

async def reply_reaction(event_id,str_reaction):
   
   key_string=log_these_key()
   if key_string!=None: 
      keys = Keys.parse(key_string)
      signer = NostrSigner.keys(keys)
      client = Client(signer)
      client = Client(signer)
         # Add relays and connect
      for relay_c in relay_list:
        await client.add_relay(RelayUrl.parse(relay_c))
      await client.connect()
      
      f = Filter().id(EventId.parse(event_id["id"]))
      events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
      z = [event for event in events.to_vec() if event.verify()]
    
      # Send an event using the Nostr Signer
      if len(z)>0:
         builder = EventBuilder.reaction(z[0],str_reaction)               
         test_note=await client.send_event_builder(builder)
         print("Send to this relays", test_note.success, "\n", "Failed to send to this relays",test_note.failed)

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
                  if stats.attempts()==1 and relay.is_connected()==False:
                     if str(url) in list_relay_connect:
                        list_relay_connect.remove(str(url))
                  #if stats.success()==1 and relay.is_connected()==True:
               i=i+1 
       
   except IOError as e:
          print(e) 
   except ValueError as b:
      print(b)       

#Relays from list of people

db_note_list=[]
dict_pubkey_relay={}
less_pubkey_relay={}

def to_follows(x,y):
   h=[]
   for j in x:
      if j in y:
         h.append(j)
   return h

def outrageous(people:list):
   i=0
   j=1
   Pu=[]
   test=[]
   Wu=list_battle(people)
   if Wu:
        z=len(Wu)
        while j<z:
            t=to_follows(Wu[i],Wu[j])
            if t!=[]:
                Pu.append(t)
            i=i+2
            j=j+2
    
   for y in Pu:
        for v in y:
            if v not in test:
                test.append(v)
   relay_simil=[]
   for j in test:
        if j+str("/") not in test:
            relay_simil.append(j)
   return relay_simil

def relay_t(x):
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

def list_battle(list_one):
   wu=[]
   zeta=[]
   c=[]
   list_10002_pubkey=[]
   User=user_convert(list_one)
   print("User", " ",len(User))
   zeta=search_kind(User,10002)
   for v in zeta:
        db_note_list.append(v)
        wu.append(relay_t(v))
   print(len(zeta)) 
   for z_z in zeta:
        if z_z["pubkey"] not in list_10002_pubkey:
            list_10002_pubkey.append(z_z["pubkey"])
            i=0
            relay_npub=[]
            relays=tags_str(z_z,'r')
            j=len(relays)
            while i<j:
                if len(relays[i])>2:
                    if relays[i][2]=="write":
                        relay_npub.append(relays[i][1])
                        c.append(relays[i][1])
                else:
                    relay_npub.append(relays[i][1])
                    c.append(relays[i][1])
                i=i+1
            dict_pubkey_relay[z_z["pubkey"]]=relay_npub
            if len(relay_npub)<5:
                less_pubkey_relay[z_z["pubkey"]]=relay_npub
      
   list_people= list(dict_pubkey_relay.keys())
    
   print("relay list ",len(zeta),"unique publickey ",len(list_10002_pubkey),"\n"
   ," list normal ", len(dict_pubkey_relay),"\n","list less 5 relays ",len(less_pubkey_relay))
    
   return wu

def list_stamp_relay():
   list_ev,list_p=list_topic_tuple()   
   if list_p:
      relays=outrageous(list_p)
      for relay_x in relays:
         if relay_x not in relay_list:
            relay_list.append(relay_x)
      asyncio.run(Search_status(Client(None),relay_list))      

button_open_two=Button(root, command=list_stamp_relay, text="Add Relays",highlightcolor='WHITE',background="grey",font=('Arial',12,'bold'))
button_open_two.place(relx=0.7,rely=0.12, anchor="n")            

root.mainloop()