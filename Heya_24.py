#Talk people
import tkinter as tk
from tkinter import *
from tkinter import ttk
import asyncio
from nostr_sdk import *
import json
from datetime import timedelta
import re
import requests
import shutil
from PIL import Image, ImageTk
from tkinter import messagebox 
from cryptography.fernet import Fernet


Nostr_relay_list={"wss://nos.lol/":"","wss://nostr.mom/":"","wss://nostr-pub.wellorder.net/":""}

async def check_relay_dict(dict_relay:dict):
   
   for relay_x in list(dict_relay.keys()):
      if dict_relay[relay_x]!="bad":   
         if get_nostr_relay_info(relay_x):
            dict_relay[relay_x]="good"
         else:
            dict_relay[relay_x]="bad"       

def get_nostr_relay_info(relay_url: str):
    """
    Gets the NIP-11 information for a Nostr relay. \n
    relay_url: e.g., 'https://relay.damus.io/'
    
    """
    headers = {"Accept": "application/nostr+json"}

    if relay_url.startswith("ws://"):
        relay_url = relay_url.replace("ws://", "http://")
    elif relay_url.startswith("wss://"):
        relay_url = relay_url.replace("wss://", "https://")
    
    try:
        response = requests.get(relay_url, headers=headers, timeout=10)
        response.raise_for_status()
        info = response.json()
        return info
    except Exception as e:
        print(f"Error while requesting {relay_url}: {e}")
        return None


root = tk.Tk()
root.geometry("1300x800")
root.title("Heya 24")

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

def get_note(z):
    f=[]
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

my_dict = {"Dawn": "c230edd34ca5c8318bf4592ac056cde37519d395c0904c37ea1c650b8ad4a712", 
           "Cesar Dias": "c6603b0f1ccfec625d9c08b753e4f774eaf7d1cf2769223125b5fd4da728019e",
             "Vitor": "460c25e682fda7832b52d1f22d3d22b3176d972f60dcdc3212ed8c92ef85065c", 
             "Laeserin": "dd664d5e4016433a8cd69f005ae1480804351789b59de5af06276de65633d319", 
             "il_lost_": "592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"}

my_list = list(my_dict.values())
my_name = list(my_dict.keys())
relay_list=[]

def on_select(event):
    selected_item = combo_box.get()
    entry_id_note.set(my_dict[selected_item])
    label_entry_id["text"]="Pubkey"
    relay_list.clear()
    search_relay()
    if db_note!=[]:
     button_frame_1.place(relx=0.85,rely=0.11,relwidth=0.1) 
  
frame1=tk.Frame(root)    
Profile_frame = ttk.LabelFrame(root, text="Profile", labelanchor="n", padding=10)
Profile_frame.place(relx=0.01,rely=0.03,relwidth=0.2,relheight=0.3)
label = tk.Label(root, text="Name",font=('Arial',12,'normal'))
label.place(relx=0.08,rely=0.07)
combo_box = ttk.Combobox(root, values=["Dawn","Cesar Dias","Vitor","Laeserin","il_lost_"],font=('Arial',12,'normal'),width=15)
combo_box.place(relx=0.06,rely=0.12)
combo_box.set("Cluster")
combo_box.bind("<<ComboboxSelected>>", on_select)
entry_id_note=StringVar()
entry_note_note=StringVar()
label_entry_id=tk.Label(root, text="Pubkey",font=("Arial",12,"normal"))
label_entry_id.place(relx=0.08,rely=0.18)
label_entry_name=tk.Label(root, text="",font=("Arial",12,"normal"))
time_frame = ttk.LabelFrame(root, text="Notification", labelanchor="n", padding=10)
time_frame.place(relx=0.21,rely=0.03,relwidth=0.13,relheight=0.3)
combo_note = ttk.Combobox(root, values=["Total","My In","Inbox","Hashtag","my PM","my time"],width=10, font=("Arial",12,"normal"))
combo_note.place(relx=0.23,rely=0.08)
combo_note.set("Type of feed")
combo_note.bind("<<ComboboxSelected>>", None)
Timeline=[]
My_post=[]
Inbox=[]
Hashtag=[]
my_pm=[]
my_time=[]
Frame_block=Frame(frame1,width=50, height=20)

def timeline_created(list_new):
  new_note=[] 
  global db_list
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

test_check = IntVar() 

def check_dash():
 if combo_note.get()!="Type of feed":
  if combo_note.get()=="my time":
   if test_check.get()==1:
    label_name.place(relx=0.42,rely=0.02)
    since_entry_0.place(relx=0.42,rely=0.06)
    button_mov.place(relx=0.47,rely=0.06,relwidth=0.03)
    button_backs.place(relx=0.38,rely=0.06,relwidth=0.03) 
    date_entry_0.place(relx=0.38,rely=0.1,relheight=0.04, x=0.01 )
   else:
    since_entry_0.place_forget()
    button_mov.place_forget()
    button_backs.place_forget()
    date_entry_0.place_forget()
    label_name.place_forget()
  else:
     print("this an other function ", combo_note.get())  
     if test_check.get()==1:
      test_check.set(0)
      combo_note.set("my time")
     since_entry_0.place_forget()
     button_mov.place_forget()
     button_backs.place_forget()
     date_entry_0.place_forget()
     label_name.place_forget()

Button_check_2 = Checkbutton(root, text ="" , variable = test_check, onvalue = 1, offvalue = 0, height = 1, command=check_dash)
Button_check_2.place(relx=0.3,rely=0.22)
label_time = tk.Label(root, text="Time",font=("Arial",12,"normal"))
label_time.place(relx=0.25,rely=0.22)
since_variable_0=IntVar(value=0)
since_entry_0=Entry(root,textvariable=since_variable_0,font=("Arial",12,"normal"),width=4)
label_name=Label(root,text="Day",font=("Arial",12,"normal"))

def next_since():
   since_variable_0.set(int(since_entry_0.get()) + 1)
   since_day_time()

def back_since():
   if int(since_entry_0.get())- 1<1:
      since_variable_0.set(int(1))
      since_day_time()
   else:
    since_variable_0.set(int(since_entry_0.get())- 1)  
    since_day_time()

button_mov=tk.Button(root,text="➕",command=next_since)
button_backs=tk.Button(root,text="➖",command=back_since)
text_variable_date=StringVar()
date_entry_0=Entry(root,text=text_variable_date,font=("Arial",12,"normal"),width=17)

def since_day_time():
    import datetime
    date_one = datetime.date.today() - datetime.timedelta(days=int(since_entry_0.get()))
    date_two=datetime.datetime.combine(date_one, datetime.time(1, 2, 1)).timestamp()
    text_variable_date.set(str(int(date_two)))

def list_timeline(Value):
  if Value!="Type of feed":  
   if Value in combo_note["values"]:
      if Value=="Total":
         timeline=[]
         for db_x in db_list:
            if db_x["pubkey"]!=entry_id.get():
               timeline.append(db_x)
         return timeline      
         
      if Value=="My In":
         My_post.clear()
         for db_x in db_list:
            if db_x["pubkey"]==entry_id.get():
               My_post.append(db_x)
         return My_post      
         
      if Value=="Inbox":
         Inbox.clear()
         for db_x in db_list:
           if tags_string(db_x,"p")!=[]:
            if len(tags_string(db_x,"p"))<=2:
                if db_x["pubkey"]!=entry_id.get():
                 Inbox.append(db_x)     
         return Inbox
      if Value=="Hashtag": 
         Hashtag.clear()
         for db_x in db_list:
           if tags_string(db_x,"t")!=[]:
              if db_x not in Hashtag:
                Hashtag.append(db_x)     
         return Hashtag
      if Value=="my PM":
         my_pm.clear()
         for db_x in db_list:
            if db_x["kind"]==24:
               my_pm.append(db_x)
         return my_pm   
      if Value=="my time":
        try: 
         my_time.clear()
         for db_x in db_list:
            if date_entry_0.get()!="":
             if int(db_x["created_at"])>int(date_entry_0.get()):
              if db_x["pubkey"]!=entry_id.get():
               my_time.append(db_x)
            else:
                since_day_time()
                if int(db_x["created_at"])>int(date_entry_0.get()):
                  my_time.append(db_x) 
         return my_time   
        except ValueError as e:
           print(e)
      
async def get_relay(client, user):
    f = Filter().author(user).remove_identifiers(["influenceScoresList"]).kinds([Kind(30000)]).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

WoT_check=IntVar()
Button_check_2 = Checkbutton(root, text ="WoT" , variable = WoT_check, onvalue = 1, offvalue = 0, height = 1,font=('Arial',12,'bold'))
Button_check_2.place(relx=0.25,rely=0.27)

async def get_note_text(client, user):
  try:
   if WoT_check.get()==1:
    f = Filter().authors(user).kinds([Kind(24)]).pubkey(PublicKey.parse(my_dict[combo_box.get()])).limit(80)
   else:
    f = Filter().kinds([Kind(24)]).pubkey(PublicKey.parse(my_dict[combo_box.get()])).limit(80)   
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   return z
  except RelayMessage as e:
      print(e)

draft_user=[]
user_metadata={}
List_three=[]

def list_note_draft(list_note):
   if list_note!=[]:
    if draft_user==[]:
      for jlist in list_note:
       if jlist["pubkey"] not in draft_user:
                 draft_user.append(jlist["pubkey"]) 
       for xuser in tags_string(jlist,"p"):
              if xuser not in draft_user:
                 draft_user.append(xuser)
                   
async def main_long_tk(authors):
   try: # Init logger
    client = Client(None)
      # Add relays and connect
    if relay_list!=[]:
      for jrelay in relay_list:
         if jrelay not in list(Nostr_relay_list.keys()):
            Nostr_relay_list[jrelay]=""
            relay_list.remove(jrelay)
    await check_relay_dict(Nostr_relay_list)
    for relay_c,value in Nostr_relay_list.items():
      if value!="bad": 
         await client.add_relay(RelayUrl.parse(relay_c))        
           
    await client.connect()     
    await asyncio.sleep(2.0)
    if WoT_check.get()==1:
     combined_results = await get_relay(client, authors)
     List_note=get_note(combined_results)
     if List_note:
       for jlist in List_note:
          if jlist not in List_three:
            List_three.append(jlist)
          for xuser in tags_string(jlist,"p"):
              if xuser not in draft_user:
                 draft_user.append(xuser)
     if draft_user!=[]:
      Draft_User=user_convert(draft_user)
     else:
        Draft_User=[] 
    else:
       Draft_User=[]    
    combined_note = await get_note_text(client, Draft_User)
    combine_get_note=get_note(combined_note)
    if combine_get_note!=[]:
      timeline_created(combine_get_note)
      list_note_draft(combine_get_note)
      return combine_get_note
   except NostrSdkError as e:
      print(e) 
   
def create_tm():
  if entry_id.get()!="":
   user=convert_user(entry_id.get())
   test_note=asyncio.run(main_long_tk(user))
   print(len(test_note),len(draft_user))   
   
entry_id=tk.Entry(root, textvariable=entry_id_note, width=20)
entry_note=tk.Entry(root, textvariable=entry_note_note, width=50)
entry_id.place(relx=0.06,rely=0.22)
button4=tk.Button(root,text="Notifications",command=create_tm,font=('Arial',12,'bold'))
button4.place(relx=0.07,rely=0.27) 
frame_upfront=Frame(root)
frame2=Frame(root)

def add_db_list():
        Frame_2=Frame(root)
        Frame_block=Frame(Frame_2,width=50, height=20)
               
        def Close_block(event):
            Frame_block.destroy()
        
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=1, row=0, padx=5, columnspan=1) 
            
        def search_block_list():
            label_string_block1.set(len(db_list))    

        def search_block_list2():
            label_string_1.set(len(db_note))        

        def search_block_list3():
            label_string_2.set(len(user_metadata))            

        def delete_block_list():
            db_list.clear()
            label_string_block1.set(len(db_list))    
    
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey")
        clear_block.grid(column=2,row=1,padx=5,pady=5)    
        random_block1=Button(Frame_block, command=search_block_list, text= "Notification: ")
        random_block1.grid(column=0,row=1,padx=5,pady=5)
        random_block2=Button(Frame_block, command=search_block_list2, text= "Personal Note: ")
        random_block2.grid(column=0,row=2,padx=5,pady=5)
        random_block3=Button(Frame_block, command=search_block_list3, text= "Messengers: ")
        random_block3.grid(column=0,row=3,padx=5,pady=5)
        label_string_block1=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1,font=('Arial',12,'bold'))
        label_block_list1.grid(column=1,row=1,padx=5,pady=5)
        label_string_1=StringVar()
        label_block_1=Label(Frame_block, textvariable=label_string_1,font=('Arial',12,'bold'))
        label_block_1.grid(column=1,row=2,padx=5,pady=5)
        label_string_2=StringVar()
        label_block_2=Label(Frame_block, textvariable=label_string_2,font=('Arial',12,'bold'))
        label_block_2.grid(column=1,row=3,padx=5,pady=5)
        Frame_block.grid(column=0,row=6, columnspan=3, rowspan=3)
        Frame_2.place(relx=0.05,rely=0.73)

button_block=tk.Button(root, highlightcolor='WHITE',text='DB count',font=('Arial',12,'bold'),command=add_db_list)
button_block.place(relx=0.08,rely=0.65) 
frame2.grid(column=0, row=0,columnspan=3, rowspan=4,pady=10)
frame_upfront.grid()
int_var=IntVar()
int_var.set(1)

def note_number():
    if db_list!=[]:
      if int((int(lbel_var.get())+1))< int((len(list_timeline(combo_note.get()))/16)+1):
          int_var.set(int(lbel_var.get())+1)
          show_Teed()
      else:
          if int((len(list_timeline(combo_note.get()))/16))==0:
           int_var.set(int(1)) 
          else:
           if len(db_list)>80:
            if  int((int(lbel_var.get()))+1)>=int((len(list_timeline(combo_note.get()))/16)+1):   
             if int((int(lbel_var.get()))+1)<int((len(list_timeline(combo_note.get()))/16)+2):
              int_var.set(int(lbel_var.get())+1)
             
              show_Teed() 
           else: 
            int_var.set(int(1))     
            show_Teed()
          
def back_number():
    if int((int(lbel_var.get())-1))>=1:
        int_var.set(int(lbel_var.get())-1)
        show_Teed()
    else:
        int_var.set(1) 
        
button_next=Button(root,command=note_number,text="➕",font=("Arial",12,"bold"))
button_back=Button(root,command=back_number,text="➖",font=("Arial",12,"bold"))
db_list=[]
lbel_var=Entry(root, textvariable=int_var,font=("Arial",14,"bold"),background="grey") 

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

 def create_page(db_list_,s):
  if db_list_!=[] and db_list_!=None:
  
    n=16*(s-1)
    l=s*16
    for note in db_list_[n:l]:
     try:
      if note["pubkey"] in list(user_metadata.keys()):
            context0="Nickname " +user_metadata[note["pubkey"]]
      else:
            context0="Pubkey "+note["pubkey"]
     
      context1="Time: "+ str(return_date_tm(note))
       
      context2=""   
      if tags_string(note,"t")!=[]:
        for note_tags in tags_string(note,"t"):
            context2=context2+str(" #")+note_tags+" "
        context2=context2+"\n"    
      else:
           context2=""  
      if tags_string(note,"e")!=[]:
        if four_tags(note,"e"):
            for F_note in four_tags(note,"e"):
                if len(F_note)>3:
                 context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
                else:
                 context2=context2+str(" < "+ F_note[0]+" > " + " NO NIP-10"+ "\n")   
      else:    
         pass            

           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"),background="#B6B2AE")
      var_id.set(context0)
      label_id.grid(pady=2,column=0, columnspan=3,row=s)
      var_id_1=StringVar()
      label_id_1 = Message(scrollable_frame_1,textvariable=var_id_1, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id_1.set(context1)
      label_id_1.grid(pady=2,column=0, columnspan=3,row=s+1)
      scroll_bar_mini2 = tk.Scrollbar(scrollable_frame_1)
      scroll_bar_mini2.grid( sticky = NS,column=4,row=s+2)
      second_label_20 = tk.Text(scrollable_frame_1, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini2.set, font=('Arial',14,'bold'),background="#D9D6D3")
      second_label_20.insert(END,note["content"]+"\n"+str(context2))
      scroll_bar_mini2.config( command = second_label_20.yview )
      second_label_20.grid(padx=10, column=0, columnspan=3, row=s+2) 
      
      def photo_var(entry):
            if len(more_spam(entry))<2: 
              photo_print(entry)
            else:
               
               if tags_string(entry,"imeta")!=[]:
                photo_list_2(entry)
               else:
                  if len(more_spam(entry))==2:
                    photo_list(more_spam(entry))

      def print_id(entry):
           if entry["kind"]==24:
                test_open(entry["pubkey"])
                close_frame()
                quote=quote_content(entry["content"])
                if quote:
                   print(quote)
                if tags_string(entry,"e")!=[] or tags_string(entry,"q")!=[]:
                  show_print_test_tag(entry)
           else: 
             if messagebox.askyesno("This create a new window","Do you want Reply? "):
                close_frame()
                if test_check.get()==1:
                   test_check.set(0)
                   check_dash()
                test_open(entry["pubkey"])
             else:   
              if entry["tags"]!=[]:
               print(db_list.index(entry)+1)
             
      def print_var(entry):
                print(entry["content"])
           
      button=Button(scrollable_frame_1,text=f"Print me ", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s+3,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s+3,column=1,padx=5,pady=5)  
      if note["tags"]!=[]: 
       if tags_string(note,"imeta")!=[] or tags_string(note,"image")!=[]:   
        button_grid3=Button(scrollable_frame_1,text=f"Photo ", command=lambda val=note: photo_var(val))
        button_grid3.grid(column=2,row=s+3,padx=5,pady=5)
      s=s+4  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.35,rely=0.22,relwidth=0.28,relheight=0.4)
    
    def close_frame():
        frame2.destroy()   
        button_frame.place_forget()
        button_next.place_forget()
        button_back.place_forget()
        lbel_var.place_forget()
        button_f_close.place_forget()
        int_var.set(1)
    
    button_next.place(relx=0.55,rely=0.17, anchor="n")
    button_back.place(relx=0.40,rely=0.17, anchor="n",x=1)
    lbel_var.place(relx=0.475,rely=0.17, anchor="n",relwidth=0.02,relheight=0.04)

    def close_number() -> None :
        frame2.destroy()    
        button_frame.place_forget()
        button_next.place_forget()
        button_back.place_forget()
        lbel_var.place_forget()
        button_f_close.place_forget()
        
    button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"))
    button_f_close.place(relx=0.6,rely=0.17)      
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.44,rely=0.65,relwidth=0.1)  
    
 s=1
 create_page(list_timeline(combo_note.get()), int(lbel_var.get()))
 root.update_idletasks()

button_id=tk.Button(root,command=show_Teed,text="Read",font=("Arial",12,"normal"))
button_id.place(relx=0.26,rely=0.15)
db_note=[]

def return_date_tm(note):
    import datetime
    date_2= datetime.datetime.fromtimestamp(float(note["created_at"])).strftime("%a"+", "+"%d "+"%b"+" %Y")
    date= date_2+ " "+ datetime.datetime.fromtimestamp(float(note["created_at"])).strftime('%H:%M')
    return date

def note_text_kind1():
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
  label_id_3.grid(pady=1,padx=3,row=s,column=0, columnspan=3)
  
  def photo_var(entry):
            if len(more_spam(entry))<2: 
              photo_print(entry)
            else:
               
               if tags_string(entry,"imeta")!=[]:
                photo_list_2(entry)
               else:
                  if len(more_spam(entry))==2:
                    photo_list(more_spam(entry))

  for note in db_note[0:100]:
   
   var_id_3.set("Author: "+note["pubkey"])
   var_id_4=StringVar()
   label_id_4 = Message(scrollable_frame_2,textvariable=var_id_4, relief=RAISED,width=290,font=("Arial",12,"normal"),background="#C8C3BD")
   label_id_4.grid(pady=1,padx=10,row=s+3,column=0, columnspan=3)
   var_id_4.set("Time: "+ str(return_date_tm(note)))
   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid( sticky = NS,column=4,row=s+1)
   second_label_10 = tk.Text(scrollable_frame_2, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   context2=""   
   if tags_string(note,"t")!=[]:
        for note_tags in tags_string(note,"t"):
            context2=context2+str("#")+note_tags+" "
        context2=context2+"\n"       
   else:
           context2=""  
   if tags_string(note,"e")!=[]:
        if four_tags(note,"e"):
            for F_note in four_tags(note,"e"):
                if len(F_note)>3:
                 context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
                else:
                 context2=context2+str(" < "+ F_note[0]+" > " + "NO NIP-10"+ "\n")   
                    
   else:
         pass          
     
   second_label_10.insert(END,note["content"]+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label_10.yview )
   second_label_10.grid(padx=10, column=0, columnspan=3, row=s+1) 

   button=Button(scrollable_frame_2,text=f"Print ", command=lambda val=note: print(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
   if note["tags"]!=[]: 
       if tags_string(note,"imeta")!=[] or tags_string(note,"image")!=[]:   
        button_2=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: photo_var(val))
        button_2.grid(column=1,row=s+2,padx=5,pady=5)
       
   scrollbar_2.pack(side="right", fill="y",padx=2,pady=5) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()    

   button_frame=Button(frame3,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.pack(pady=5)   
   frame3.place(relx=0.65,rely=0.22,relheight=0.43,relwidth=0.33) 
   s=s+3

button_frame_1=Button(root,command=note_text_kind1,text="Personal Note",font=("Arial",12,"normal"))
  
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

async def get_outbox(client):

  if my_list!=[]:
   if my_dict[combo_box.get()] in list(my_dict.values()): 
    print("ok")
    f = Filter().authors(user_convert([my_dict[combo_box.get()]])).kinds([Kind(10002),Kind(1),Kind(24)])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def outboxes():
    init_logger(LogLevel.INFO)
    client = Client(None)

    for relay_c,value in Nostr_relay_list.items():
      if value!="bad": 
        await client.add_relay(RelayUrl.parse(relay_c))
    if relay_list!=[]:
      for jrelay in relay_list:
         if jrelay not in list(Nostr_relay_list.keys()):
            Nostr_relay_list[jrelay]=""
            relay_list.remove(jrelay)
            await client.add_relay(RelayUrl.parse(jrelay))
    else:
      await client.add_relay(RelayUrl.parse("wss://purplerelay.com/"))
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
            else:
                db_note.append(relay_add[i])      
            i=i+1             
    await asyncio.sleep(2.0)

def search_relay():
   if __name__ == "__main__":
    asyncio.run(outboxes())

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
    if relay_list!=[]:
      for jrelay in relay_list:
         if jrelay not in list(Nostr_relay_list.keys()):
            Nostr_relay_list[jrelay]=""
            relay_list.remove(jrelay)
    await check_relay_dict(Nostr_relay_list)
    await client.add_relay(RelayUrl.parse("wss://relay.damus.io/"))
    for relay_c,value in Nostr_relay_list.items():
      if value!="bad": 
         await client.add_relay(RelayUrl.parse(relay_c))        
            
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_relays_z(client, authors)
    else:
        combined_results = await get_relay_z(client, authors)
    
    return combined_results    

def print_text(): 
   if db_list!=[]:
    db_user=[]  
    if user_metadata=={}:
     for note in db_list:
        if note["pubkey"] not in db_user:
         db_user.append(note["pubkey"])
     db_User=user_convert(db_user)
     kind_0=search_kind(db_User,0)    
     if kind_0 !=None and kind_0!=[]:
           
           zeta,pub0=metadata_list(kind_0,"name")
           for name, key in zip(zeta,pub0):
             if name!=None: 
              if len(name)>20:
                 name=name[0:20]
              if name=="":
                name="undefined" 
              user_metadata[key]=name
     print(len(user_metadata))

button4=tk.Button(root,text="Messengers",command=print_text, font=('Arial',12,'bold'))
button4.place(relx=0.07,rely=0.37) 

def metadata_list(List,y):
    """
    This function takes one list of note and a metadata tag and \n returns two list name metatag and pubkey.

    Parameters:
    List (list): The list.
    y (str): the metadata tag.

    Returns:
    list: name metatag {zeta} \n
    list: pubkey  {pub0}
    """
    zeta=[]
    pub0=[]
    for j in List:
        if metadata_0(j,y)!=None:
         zeta.append(metadata_0(j,y))
         pub0.append(j['pubkey'])
    return zeta,pub0

def metadata_0(nota,y):
   import json
   try:
        test=json.loads(nota["content"])
        if y in list(test.keys()):
            return str(test[y])
   except KeyError as e:
      print(e)
   except json.JSONDecodeError as b:
      print(b)   

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
  except json.JSONDecodeError as b:
   print(b)       

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
   list_v=['mov','mp4']
   img=['png','jpg','JPG','gif']
   img1=['jpeg','webp'] 
   ytube=['https://youtu.be']
   tme=["https://t.me/"]
   xtwitter=["https://x.com/"]
   if f==None:
                 return "no spam"
   if f[-3:] in list_v:
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
        frame_pic.place(relx=0.85,rely=0.01,relwidth=0.3,relheight=0.3,anchor="n")
      except TypeError as e: 
        print(e)  
      except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")         

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
  
        s=s+3
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        button_close.grid(column=2,row=s+1,sticky="n")
        s=s+2
  frame_pic.place(relx=0.7,rely=0.01,relwidth=0.18)

def more_link(f):
   
   list_v=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_v:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam"   
   
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
   frame_pic.place(relx=0.7,rely=0.01,relwidth=0.3) 
  else:
     print("error", "none")        
 else:
     pass

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

Check_open_2 = IntVar() 
Check_open_2.set(1)

def open_new_user():
 if len(my_dict)==5:
  if Check_open_2.get()==1:
   Check_open_2.set(0)
  frame_user.place(relx=0.02,rely=0.45,relheight=0.2,relwidth=0.28)

def close_new_user():
   if Check_open_2.get()==0:  
    Check_open_2.set(1)
    frame_user.place_forget()

def add_user(name,key):
   
    if name!="": 
     if len(key)==64 or len(key)==63:
      value_key=PublicKey.parse(key)
      if value_key.to_hex() not in list(my_dict.values()):
       if name not in my_name:     #1500 Dan
        my_dict[name]=value_key.to_hex()
        combo_box["value"]=list(my_dict.keys())
        frame_user.place_forget()

frame_user=Frame(root,height=100,width=200)
numb_close=Button(frame_user, command=close_new_user, text="Close x",font=('Arial',12,'normal'))
numb_close.grid(column=1,row=2,pady=10,padx=5,rowspan=2)
label_user = tk.Label(frame_user, text="Name",font=('Arial',12,'normal'))
label_user.grid(column=0,row=0,pady=2,padx=10)
label_pubkey = tk.Label(frame_user, text="Pubkey",font=('Arial',12,'normal'))
label_pubkey.grid(column=1,row=0,pady=2,padx=10)
user_name=StringVar()
label_number = Entry(frame_user, textvariable=user_name, width=15,font=('Arial',12,'normal'))
label_number.grid(column=0,row=1,pady=2,padx=10)
key_string=StringVar()
label_key = Entry(frame_user, textvariable=key_string, width=15,font=('Arial',12,'normal'))
label_key.grid(column=1,row=1,pady=2,padx=10)
button_add=Button(frame_user, command=lambda:add_user(user_name.get(),key_string.get()), text="add user",font=('Arial',12,'normal'))
button_add.grid(column=0,row=2,pady=4,padx=2)

frame_menu=Frame(root,width=20,height=1)
menu = Menu(frame_menu)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New User", command=open_new_user)
frame_menu.grid()

timeline_people=[]

def found_follow():
   if combo_box.get()!="Cluster": 
     type_event=""
     follow_kind=get_note(asyncio.run(feed_cluster(convert_user(my_dict[str(combo_box.get())]),type_event))) 
     if follow_kind!=[]:
        people=tags_string(follow_kind[0],"p")
        if people!=None:
         for people_x in people:
           if people_x not in timeline_people and people_x not in draft_user:
              timeline_people.append(people_x)
     list_pubkey_id()          

button_2=tk.Button(root,text="Follow List",command=found_follow,font=('Arial',12,'bold'))  #timeline
button_2.place(relx=0.71,rely=0.02)                

async def get_note_cluster(client, authors, type_of_event):
    f = Filter().authors(authors).kinds(type_of_event).limit(1000)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_relay(client, user):
    f = Filter().author(user).kind(Kind(3))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def feed_cluster(authors,type_of_event):
    # Init logger
    init_logger(LogLevel.INFO)
   
    client = Client(None)
    #uniffi_set_event_loop(asyncio.get_running_loop())

    # Add relays and connect
    for relay_c,value in Nostr_relay_list.items():
      if value!="bad": 
         await client.add_relay(RelayUrl.parse(relay_c))
    
    await client.connect()
    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_note_cluster(client, authors, type_of_event)
    else:
        combined_results = await get_relay(client, authors)
    
    return combined_results

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
        if single not in db_list_note_follow:
           db_list_note_follow.append(single)
        single_1=json.loads(single["content"])
       
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
      except json.JSONDecodeError as b:
         print(b)         
         

button_people_2=Button(root,text=f"Find People ", command=list_pubkey_id,font=('Arial',12,'bold'))
#button_people_2.place(relx=0.22,rely=0.45) 

search_pubkey_list=[]

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
         blo_label = Button(scrollable_frame, text=f"Reply to User",font=('Arial',12,'normal'),command=lambda val=name_pubkey :test_open(val) )
         blo_label.grid(row=s + 4, column=1, padx=2, pady=5)
         Button(scrollable_frame, text="Print Metadata",command=lambda val=meta_test: print(val),font=('Arial',12,'normal')).grid(row=s +4, column=2, padx=5, pady=2)
        s += 5   
        root.update_idletasks()
    frame1.place(relx=0.65,rely=0.22, relheight=0.45,relwidth=0.35)  
    
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
    entry_nick.place(relx=0.67,rely=0.17,relwidth=0.12) 
    button_close_1=Button(root, command=search_nickname, text="Find ",font=('Arial',12,'normal'), fg="blue")
    button_close_1.place(relx=0.81,rely=0.17,relheight=0.03)
    button_close_s=Button(root, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close_s.place(relx=0.9,rely=0.17)   

button_open=Button(root, command=layout, 
                   text="Scroll User",
                    highlightcolor='WHITE',
                    background="grey",
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))

button_open.place(relx=0.75,rely=0.1, anchor="n")
note_tag = tk.Label(root, text="Note",font=('Arial',12,'bold'))
entry4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
button_pre=Button(root,text="preview",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',12,'bold'))
close_=Button(root,text="Close X",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',12,'normal'))
outbox_list=[]

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
              for xrelay in tags_string(relay_user[i],'r'):
               if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay[6:9]!="127":
               
                if xrelay not in outbox_list:
                 outbox_list.append(xrelay)
            i=i+1     

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
      for jrelay in relay_list:
         if jrelay not in list(Nostr_relay_list.keys()):
            Nostr_relay_list[jrelay]=""
            relay_list.remove(jrelay)
    await check_relay_dict(Nostr_relay_list)
    
    for relay_c,value in Nostr_relay_list.items():
      if value!="bad": 
         await client.add_relay(RelayUrl.parse(relay_c))        
        
    await client.connect()
    await asyncio.sleep(2.0)
    try:   
     if isinstance(event_, list):
        test_kind = await get_kind(client, event_)
        if test_kind:
           return test_kind    
     else:
        print("error")

     if test_kind==[] and public_list!=[]:
       test_kind = await get_kind_relay(client, event_)
       print("from relay")
       return test_kind  
    except NostrSdkError as e:
       print(e)   
    
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
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

public_list=[]

async def Tag_note(note,tag):
  try: 
   init_logger(LogLevel.INFO)
   key_string=log_these_key()
   if key_string!=None: 
    keys = Keys.parse(key_string)
    
    
    signer=NostrSigner.keys(keys)
    client = Client(signer)
    if outbox_list!=[]:
       
       for jrelay in outbox_list:
         await client.add_relay(RelayUrl.parse(jrelay))
    else:
       if relay_list!=[]:
          for xrelay in relay_list:
            relay_url_1=RelayUrl.parse(xrelay)
            await client.add_relay(relay_url_1)
    await client.connect()
     
    builder = EventBuilder(Kind(24),note).tags(tag)
   
    test= await client.send_event_builder(builder)
    
    print(test.id)

    print("Event sent:")
    await asyncio.sleep(2.0)
    
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()]).kind(Kind(24)).limit(20)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     if event.verify():
      print(event.as_json())
  except NostrSdkError as e:
     print(e)    

list_q=[]
list_expiration=[]

def check_expitation():
   
   if expiration_tag.get()==1:
      list_expiration.clear()
      
   else:
      list_expiration.append("no expiration")
     
expiration_tag=IntVar()

def until_day_time(day_u:int):
    import datetime
    date = datetime.date.today() + datetime.timedelta(days=int(day_u))
    date_1=datetime.datetime.combine(date, datetime.time(0, 0, 0)).timestamp()
    
    return date_1

def Gm_status():
      
   if button_entry1.cget('foreground')!="green":
      check_square()
   if button_entry1.cget('foreground')=="green":
    lists_id=[]   
    if list_p!=[]:        
        for alist in list_p:
            if outbox_list!=[]:
              lists_id.append(Tag.from_standardized(TagStandard.PUBLIC_KEY_TAG(alist,RelayUrl.parse(outbox_list[0]),None,FALSE)))
            else:
               lists_id.append(Tag.from_standardized(TagStandard.PUBLIC_KEY_TAG(alist,None,None,FALSE)))
    if list_q!=[]:
       for jlist in list_q:
           lists_id.append(Tag.from_standardized(TagStandard.QUOTE(jlist,RelayUrl.parse(relay_list[0]),None)))       
    check_expitation()
    if list_expiration==[]:
      lists_id.append(Tag.expiration(Timestamp.from_secs(int(until_day_time(115)))))   

    if __name__ == '__main__':
        note=entry4.get(1.0, "end-1c")       
        if lists_id!=[] and note!="":
         
         asyncio.run(Tag_note(note,lists_id))
    clear_list()
    error_label.config(text="Problem:")
    print_label.config(text="Wait for the note",foreground="black")
    button_entry1.config(foreground="grey")

since_variable=IntVar(value=0)
since_entry=Entry(root,textvariable=since_variable,font=("Arial",12,"normal"),width=6)
text_var=StringVar()
date_entry=Entry(root,textvariable=text_var,font=("Arial",12,"normal"),width=11)

stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)
p_tag = tk.Label(root, text="p-Tag",font=("Arial",12,"bold"))
entry_p_var=StringVar()
entryp_tag=ttk.Entry(root,justify='left',font=("Arial",12),textvariable=entry_p_var)
p_view = tk.Label(root, text="p tag?: ", font=("Arial",12))
Checkbutton8 = IntVar() 
Type_band = Checkbutton(root, text = "More p tag", variable = Checkbutton8, onvalue = 1, offvalue = 0, height = 2, width = 10,font=('Arial',16,'normal'))
exp_show= Checkbutton(root, text = "Expiration", variable = expiration_tag,onvalue = 1, offvalue = 0, height = 2, font=('Arial',14,'bold'), command=check_expitation)
list_p=[]

entry_Home_title=ttk.Label(frame1,text="Send Tag Note", justify='left',font=("Arial",20,"bold"), background="darkgrey",border=2)
entry_Home_title.place(relx=0.4,rely=0.05,relwidth=0.2)
relay_list=[]

def check_square():
    Text=entry4.get(1.0, "end-1c")
    
    if list_p!=[] and Text!="":
        quote=quote_content(Text)
        if quote:
           if EventId.parse(quote) not in list_q:
            list_q.append(EventId.parse(quote))
        print_label.config(text="Ready", font=("Arial",12,"bold"),foreground="blue")
        button_entry1.config(text="■",foreground="green")
        error_label.config(text="ok")
        Get_outbox_relay(10002,list_p)
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for Tag or note", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")
        
button_send=tk.Button(root,text="Send Note",command=Gm_status, background="darkgrey",font=("Arial",14,"bold"))
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
error_label = tk.Label(frame1, text="Problem:",font=("Arial",12))
print_label = ttk.Label(frame1, text="Wait for the Tag note",font=("Arial",12))


def p_show():
    title=entryp_tag.get()
    
    if len(title)==64 or len(title)==63:
        if len(title)==63:
           title=PublicKey.parse(title).to_hex()
       
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
                list_p.append(convert_user(title))
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END) 
                return list_p
          else: 
                if convert_user(title) not in list_p:
                 list_p.append(convert_user(title))
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

def test_open(pubkey):
   lab_button.place(relx=0.25,rely=0.65)
   entry_p_var.set(pubkey)
   p_show()
   raw_label()
   button_send.place(relx=0.4,rely=0.8,relwidth=0.1,relheight=0.08,anchor='n' )
   button_entry1.place(relx=0.47,rely=0.8,relwidth=0.05, relheight=0.08,anchor="n" )

Check_raw =IntVar()

def clear_list():
   """Remove Tags and Update"""
   list_p.clear()
   list_q.clear()
   p_view.config(text="p tag?: ")
   entry4.delete("1.0","end")
   button_entry1.config(fg="grey")

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.35,rely=0.12,relheight=0.65,relwidth=0.28)  
        Type_band.place(relx=0.5,rely=0.6,relwidth=0.1,relheight=0.05)  
        exp_show.place(relx=0.5,rely=0.5)  
        p_view.place(relx=0.5,rely=0.7,relwidth=0.1 )
        p_button.place(relx=0.4,rely=0.7)
        p_tag.place(relx=0.4,rely=0.6,relwidth=0.1 )
        entryp_tag.place(relx=0.4,rely=0.65,relwidth=0.2 )
        entry4.place(relx=0.5,rely=0.2,relwidth=0.2,relheight=0.3,anchor='n' )
        error_label.grid(column=3, rowspan=2, row=0, pady=5,padx=5)
        print_label.grid(column=3, columnspan=2, row=2, pady=5,padx=10)
        frame1.place(relx=0.5,rely=0.8)
        button_send.place(relx=0.4,rely=0.8,relwidth=0.1,relheight=0.08,anchor='n' )
        button_entry1.place(relx=0.47,rely=0.8,relwidth=0.05, relheight=0.08,anchor="n" )
   
   else:
      Check_raw.set(0)
      stuff_frame.place_forget() 
      Type_band.place_forget() 
      exp_show.place_forget()
      p_view.place_forget()
      p_button.place_forget()
      p_tag.place_forget()
      entryp_tag.place_forget()
      button_clear.place_forget()
      entry4.delete("1.0","end")
      entry4.place_forget()
      frame1.place_forget()
      clear_list()
      check_square()
      button_send.place_forget()
      button_entry1.place_forget()
      lab_button.place_forget()
   
button_create=Button(root,text="Post", command=test_open,font=('Arial',12,'bold'),background="grey")
p_button = tk.Button(root, text="p_show", font=("Arial",12,"bold"), command=p_show)
entry4=tk.Text(root,border=2,highlightbackground="grey",font=("Arial",12,"normal"))
button_clear=Button(root,text="Remove", command=clear_list, font=("Arial",12,"bold"))
lab_button = tk.Button(root, text="Close Open", font=("Arial",12,"bold"), command=raw_label, fg="red")

def close_answer():
  button_send.place_forget() 
  button_pre.place_forget()  
  note_tag.place_forget() 
  if entry4.get()!="":
   entry4.delete(0, END)
  entry4.place_forget()
  entry_note.place_forget()
  event_idone.place_forget()
  close_.place_forget()

list_tag=[]
event_idone=Button(root,text="Search_event_one", font=('Arial',12,'normal') ) 

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

def share_note(note_text):
  test=EventId.parse(note_text["id"])
  if relay_list!=[]:
   test1=Nip19Event(test,PublicKey.parse(note_text["pubkey"]),Kind(note_text["kind"]),[RelayUrl.parse(relay_list[0])])
  else:
   test1=Nip19Event(test,PublicKey.parse(note_text["pubkey"]),Kind(note_text["kind"]),[])
  print(test1.to_nostr_uri())
  print("\n")
  print(str(test.to_nostr_uri()))

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
   if note["pubkey"] in list(user_metadata.keys()):
              context00="Nickname " +user_metadata[note["pubkey"]]
   else:
                context00="Pubkey "+note["pubkey"]
   var_id_3.set(context00)
   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid( sticky = NS,column=4,row=s+1)
   second_label_10 = tk.Text(scrollable_frame_2, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   context2=""   
   if tags_string(note,"t")!=[]:
        for note_tags in tags_string(note,"t"):
            context2=context2+str("#")+note_tags+" "
   else:
           context2=""  
   if tags_string(note,"e")!=[]:
        if four_tags(note,"e"):
            for F_note in four_tags(note,"e"):
                if len(F_note)>3:
                  context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
                else:
                   context2=context2+str(" < "+ F_note[0]+" > " + " NO NIP-10"+ "\n")   
   else:         
         pass            
   second_label_10.insert(END,note["content"]+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label_10.yview )
   second_label_10.grid(padx=10, column=0, columnspan=3, row=s+1) 

   def print_var(entry):
            if len(more_spam(entry))<2: 
              photo_print(entry)
            else:
               
               if tags_string(entry,"imeta")!=[]:
                photo_list_2(entry)
               else:
                  if len(more_spam(entry))==2:
                    photo_list(more_spam(entry))
                   
   def print_content(entry):
      
      result=show_note_from_id(entry)
      if result!=None: 
        z=4
        for jresult in result:
           if jresult["id"]!=entry["id"] and jresult["kind"]==24:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             if jresult["pubkey"] in list(user_metadata.keys()):
              context0="Nickname " +user_metadata[jresult["pubkey"]]
             else:
                context0="Pubkey "+jresult["pubkey"]
             var_id_r.set(context0)
         
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             context22="---> tags: <--- "+"\n"   
             if tags_string(jresult,"e")!=[]:
              if four_tags(jresult,"e"):
                for F_note in four_tags(note,"e"):
                     context22=context22+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              
             else:
               context22="---> Root  <--- "  
             second_label10_r.insert(END,jresult["content"]+"\n"+str(context22))
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
           z=z+2
                   
   button=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
     
   if tags_string(note,"e")!=[] or tags_string(note,"q")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply ", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)   
   button_grid2=Button(scrollable_frame_2,text=f"Nostr:URI ", command=lambda val=note: share_note(val))
   button_grid2.grid(column=1,row=s+2,padx=5,pady=5)
   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     button_frame.place_forget()
     frame3.destroy()    
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.8,rely=0.05) 
   frame3.place(relx=0.66,rely=0.1,relheight=0.4,relwidth=0.33) 

def show_note_from_id(note):
        replay=nota_reply_id(note)
        quote=quote_content(note["content"])
        if quote:
           replay.append(quote)
        if replay!=[]:
         replay_note=[]
         for note_x in db_list:
           if note_x["id"] in replay:
             if note_x not in replay_note:
              replay_note.append(note_x)
         for note_y in db_note:
           if note_y["id"] in replay:
             if note_y not in replay_note:
              replay_note.append(note_y)
         if replay_note!=[]:
            return replay_note
               
def nota_reply_id(nota):
   e_id=[]
   if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id) 
   if tags_string(nota,'q')!=[]:
    for event_q in tags_string(nota,'q'):
        if event_q not in e_id:
            e_id.append(event_q)              
            if four_tags(nota,"q")!=[]:
                for event_q in four_tags(nota,"q"):
                    if str(event_q[2]).startswith("wss://") and event_q[2] not in list(Nostr_relay_list.keys()) :
                        Nostr_relay_list[event_q[2]]="" 

   return e_id    

relay_url_list=[]

def quote_content(content:str):
   list_content=content.split()
   for string in list_content:
      quoted_event=event_string_note(string)
      if quoted_event:
          return quoted_event

def event_string_note(note:str):   
    quoted=note
    decode_nevent=""
    if quoted.startswith('nostr:nevent1'):
        decode_nevent = Nip19Event.from_nostr_uri(quoted)
    if quoted.startswith('nevent1'):
         decode_nevent = Nip19Event.from_nostr_uri("nostr:"+quoted)
    if decode_nevent!="":           
      for xrelay in decode_nevent.relays():
            if xrelay not in relay_url_list:
               relay_url_list.append(xrelay)
         
      return decode_nevent.event_id().to_hex()

root.mainloop()