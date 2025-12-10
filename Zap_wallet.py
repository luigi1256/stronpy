#Zap_people
import tkinter as tk
from tkinter import *
from tkinter import ttk
import asyncio
from nostr_sdk import *
import json
from datetime import timedelta
from tkinter import messagebox 

root = tk.Tk()
root.geometry("1300x800")
root.title("Zap Note")

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

my_dict = {"Pablo": "fa984bd7dbb282f07e16e7ae87b26a2a7b9b90b7246a44771f0cf5ae58018f52", 
           "jb55": "32e1827635450ebb3c5a7d12c1f8e7b2b514439ac10a67eef3d9fd9c5c68e245",
             "Vitor": "460c25e682fda7832b52d1f22d3d22b3176d972f60dcdc3212ed8c92ef85065c", 
             " hodlbod": "97c70a44366a6535c145b333f973ea86dfdc2d7a99da618c40c64705ad98e322", 
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
     print(len(db_note)) 
  
frame1=tk.Frame(root)    
Profile_frame = ttk.LabelFrame(root, text="Profile", labelanchor="n", padding=10)
Profile_frame.place(relx=0.01,rely=0.03,relwidth=0.2,relheight=0.3)
label = tk.Label(root, text="Name",font=('Arial',12,'normal'))
label.place(relx=0.08,rely=0.07)
combo_box = ttk.Combobox(root, values=["Pablo","jb55","Vitor"," hodlbod","il_lost_"],font=('Arial',12,'normal'),width=15)
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
combo_note = ttk.Combobox(root, values=["Total","My In","Inbox","Big Zap","my hashtag","my time"],width=10, font=("Arial",12,"normal"))
combo_note.place(relx=0.23,rely=0.08)
combo_note.set("Type of feed")
combo_note.bind("<<ComboboxSelected>>", None)
Timeline=[]
My_post=[]
Inbox=[]
Big_Zap=[]
my_hashtag=[]
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
    button_count_1.place(relx=0.41,rely=0.18) 
    time_pm.place(relx=0.38,rely=0.15,relwidth=0.13,relheight=0.2)
   else:
    button_count_1.place_forget() 
    time_pm.place_forget()
    label_id_amount_time.place_forget()
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
            
                if db_x["pubkey"]!=entry_id.get():
                 Inbox.append(db_x)     
         return Inbox
      if Value=="Big Zap": 
         Big_Zap.clear()
         for db_x in db_list:
           invoice=lnbc_zap(db_x)
           if invoice:
              amount=bolt11_amount(invoice)
              if amount: 
               if amount>50:  
                if db_x not in Big_Zap:
                 Big_Zap.append(db_x)     
         return Big_Zap
      if Value=="my hashtag":
         my_hashtag.clear()
         for db_x in db_list:
            if db_x["pubkey"]==entry_id.get():
              if tags_string(db_x,"t")!=[]:
               my_hashtag.append(db_x)
         return my_hashtag   
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

In_out=IntVar()
Button_check_3 = Checkbutton(root, text ="My Zap" , variable = In_out, onvalue = 1, offvalue = 0, height = 1,font=('Arial',12,'bold'))
#Button_check_3.place(relx=0.27,rely=0.27)

async def get_note_text(client, user):
  try:
   if WoT_check.get()==1:
    f = Filter().authors(user).kinds([Kind(9734),Kind(9735)]).pubkey(PublicKey.parse(my_dict[combo_box.get()])).limit(80)
   else:
    if In_out.get()==1:
     f = Filter().kinds([Kind(9734),Kind(9735)]).author(PublicKey.parse(my_dict[combo_box.get()])).limit(80)   
     print(f)
    else:
        f = Filter().kinds([Kind(9734),Kind(9735)]).pubkey(PublicKey.parse(my_dict[combo_box.get()])).limit(80)   
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
    relay_url_1=RelayUrl.parse("wss://nostr.mom/")
    relay_url_2=RelayUrl.parse("wss://nos.lol/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    if relay_list!=[]:
       
       for jrelay in relay_list:
          relay_url_list=RelayUrl.parse(jrelay)
          await client.add_relay(relay_url_list)
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
   if test_note:
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
    
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear Not: ",background="darkgrey")
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
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
      pubkey,amount=kind_9735(note)
      if amount:
       if pubkey:
        if pubkey in list(user_metadata.keys()):
         context2=context2+ str(user_metadata[pubkey])+str(" zap ")+str(amount)+"\n"
        else:     
         context2=context2+ str(pubkey[0:9])+str(" zap ")+str(amount)+"\n"    
      
      kind_9734=tag_description(note)
      if kind_9734:
       if tags_string(kind_9734,"e")!=[]:
        if four_tags(kind_9734,"e"):
            for F_note in four_tags(kind_9734,"e"):
                if len(F_note)>3:
                 context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
                else:
                 context2=context2+str(" < "+ F_note[0]+" > " + " NO NIP-10"+ "\n")   
      
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
      
            
      def print_id(entry):
           if entry["kind"]==9734 or  entry["kind"]==9735:
              if entry["tags"]!=[]:
               
               kind_note=tag_description(entry)
               if kind_note:
                if tags_string(kind_note,"e")!=[]:
                 show_print_test_tag(kind_note)
              else:
                 print(kind_note["kind"])
                          
      def print_var(entry):
                print(entry)
                kind_note=tag_description(entry)
                if kind_note:
                   print(kind_note)
           
      button=Button(scrollable_frame_1,text=f"Print me ", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s+3,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"click to read ", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s+3,column=1,padx=5,pady=5)  
      s=s+4  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.25,rely=0.45,relwidth=0.28,relheight=0.4)
    
    def close_frame():
        frame2.destroy()   
        button_frame.place_forget()
        button_next.place_forget()
        button_back.place_forget()
        lbel_var.place_forget()
        button_f_close.place_forget()
        int_var.set(1)
    
    button_next.place(relx=0.40,rely=0.4, anchor="n")
    button_back.place(relx=0.35,rely=0.4, anchor="n",x=1)
    lbel_var.place(relx=0.3,rely=0.4, anchor="n",relwidth=0.02,relheight=0.04)

    def close_number() -> None :
        frame2.destroy()    
        button_frame.place_forget()
        button_next.place_forget()
        button_back.place_forget()
        lbel_var.place_forget()
        button_f_close.place_forget()
        
    button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"))
    button_f_close.place(relx=0.45,rely=0.4)      
    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.4,rely=0.9,relwidth=0.1)  
    
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

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list 

async def get_outbox(client):

  if my_list!=[]:
   if my_dict[combo_box.get()] in list(my_dict.values()): 
    print("ok")
    f = Filter().authors(user_convert([my_dict[combo_box.get()]])).kinds([Kind(10002),Kind(9734),Kind(9735)])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

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

def print_text(): 
   if db_list!=[]:
    db_user=[]  
    if user_metadata=={}:
     for note in db_list:
        note1=tag_description(note)
        if note1:
         if note1["pubkey"] not in db_user:
          db_user.append(note1["pubkey"])
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

Pubkey_Metadata={}
photo_profile={}
db_list_note_follow=[]
search_pubkey_list=[]

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

since_variable=IntVar(value=0)
since_entry=Entry(root,textvariable=since_variable,font=("Arial",12,"normal"),width=6)
text_var=StringVar()
date_entry=Entry(root,textvariable=text_var,font=("Arial",12,"normal"),width=11)
entry_Home_title=ttk.Label(frame1,text="Send Tag Note", justify='left',font=("Arial",20,"bold"), background="darkgrey",border=2)
entry_Home_title.place(relx=0.4,rely=0.05,relwidth=0.2)
relay_list=[]
frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
list_tag=[]

def share(note_text):
    print(f"Note: \n {note_text}")

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
   if tags_string(note,"amount")!=[]:
        for note_tags in tags_string(note,"amount"):
            context2=context2+str(" Amount ")+note_tags+" msats"+"\n"
   if tags_string(note,"alt")!=[]:
     for no_tags in tags_string(note,"alt"):
         context2=context2+str(" Alt ")+no_tags+"\n"
   
   if tags_string(note,"e")!=[]:
        if four_tags(note,"e"):
            for F_note in four_tags(note,"e"):
                if len(F_note)>3:
                  context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
                else:
                   context2=context2+str(" < "+ F_note[0]+" > " + " NO NIP-10"+ "\n")   
        else:         
         for e_x in tags_str(note,"e"):
            context2=context2+str(" < "+ e_x[0]+" > ")+e_x[1][0:9]+ "\n"
   second_label_10.insert(END,note["content"]+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label_10.yview )
   second_label_10.grid(padx=10, column=0, columnspan=3, row=s+1) 

   def print_content(entry):
       result=show_note_from_id(entry)
       if result!=None: 
        z=4
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             if jresult["pubkey"] in list(user_metadata.keys()):
              context0="Nickname " +str(user_metadata[jresult["pubkey"]])
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
                   
    
   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply!", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    

   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     button_frame.place_forget()
     frame3.destroy()    
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.6,rely=0.05) 
   frame3.place(relx=0.66,rely=0.01,relheight=0.35,relwidth=0.33) 

def show_note_from_id(note):
        replay=nota_reply_id(note)
        if replay!=[]:
           replay_note=[]
           for note_x in db_note:
              if note_x["id"] in replay:
                replay_note.append(note_x)
                replay.remove(note_x["id"])
           if replay!=[]:     
            items=get_note(asyncio.run(Get_event_id(replay)))
            for item in items:
               if item not in db_note:
                  db_note.append(item)
            if replay_note!=[]:
               for replay_x in replay_note:
                  if replay_x not in items:
                     items.append(replay_x)
            return items   
           else:
              return replay_note
            
async def get_notes_(client, e_ids):
     f = Filter().ids([EventId.parse(e_id) for e_id in e_ids])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec() if event.verify()]
     return z

async def get_reply_note(client, e_id):
    f = Filter().event(EventId.parse(e_id)).kind(Kind(1))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z


async def Get_event_id(e_id):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       
       for jrelay in relay_list:
         relay_url = RelayUrl.parse(jrelay)
         await client.add_relay(relay_url)
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
        test_id = await get_reply_note(client,e_id)
       
    return test_id        
        
def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id    

def kind_9735(x):
        try: 
         Nota=tag_description(x)
         invoice=lnbc_zap(x)
         if bolt11_amount(invoice)==None:
          return None,None
         else:
           return Nota['pubkey'], bolt11_amount(invoice)
        except TypeError as e:
           print(e,x) 
     
def tag_description(x):
    l=x['tags']
    s:dict
    import json
    for j in l:
        if j[0] =='description':
            s=json.loads(j[1])
            return s

def lnbc_zap(v):
    if tags_string(v, 'bolt11')!=[]:
     x:str=tags_string(v, 'bolt11')[0]
     if x[0:4]=='lnbc':
       return x
           
def lnb_invoice(string:str):
    s=0
    if string.startswith("lnbc"):
       import_str=string[4:]
       for j in import_str:
            if j=="n":
                print(int(s/10))
                return int(s/10)
            else:
                if j=="u":
                    
                    print(int(s)*100)
                    return int(s)*100
                else:
                 s=s+int(j)
       
def bolt11_amount(invoice: str):
    import re

    match = re.match(r"^lnbc(\d+)([munp]?)", invoice)
    if not match:
        return None  

    value, unit = match.groups()
    value = int(value)

    # conversione in BTC
    if unit == "m":  # milli
        btc = value * 1e-3
    elif unit == "u":  # micro
        btc = value * 1e-6
    elif unit == "n":  # nano
        btc = value * 1e-9
    elif unit == "p":  # pico 
        btc = value * 1e-12
    else:  
        btc = value * 1.0

    # conversione BTC → satoshi
    sats = int(round(btc * 100_000_000))
    
    return sats
import time

def count_sats():
   zap_list=[]
   for note in db_list:
      if note["kind"]==9735:
         if note["created_at"]>int(float(time.time()-604800)):
            if note not in zap_list:
               zap_list.append(note)
   if zap_list!=[]:
      var_id_amount.set("")
      s=0
      for note_x in zap_list:
         invoice=lnbc_zap(note_x)
         if invoice:
            amount=bolt11_amount(invoice)
            if amount:
             s=s+amount
      if s>0:          
        print("for ",len(zap_list), "note receveid Sats ",s)   
        var_id_amount.set("for "+str(len(zap_list))+ " note receveid Sats "+str(s)) 
        label_id_amount.place(relx=0.54,rely=0.23)

def Count_Sats_Day():
   zap_list=[]
   for note in db_list:
     if date_entry_0.get()!="":
      if note["kind"]==9735:
         if note["created_at"]>int(date_entry_0.get()):
            if note not in zap_list:
               zap_list.append(note)
   if zap_list!=[]:
      var_id_amount_time.set("")
      s=0
      for note_x in zap_list:
         invoice=lnbc_zap(note_x)
         if invoice:
            amount=bolt11_amount(invoice)
            if amount:
             s=s+amount
      if s>0:          
        print("for ",len(zap_list), "note receveid Sats ",s)   
        var_id_amount_time.set("for "+str(len(zap_list))+ " note receveid Sats "+str(s)) 
        label_id_amount_time.place(relx=0.41,rely=0.23)        
   else:
      var_id_amount_time.set("")     
                  
time_am = ttk.LabelFrame(root, text="Total Week", labelanchor="n", padding=10)
time_pm = ttk.LabelFrame(root, text="Amount Days", labelanchor="n", padding=10)
time_am.place(relx=0.51,rely=0.15,relwidth=0.13,relheight=0.2)
button_count=Button(root,command=count_sats,text="Amount",font=("Arial",12,"normal"))
button_count.place(relx=0.54,rely=0.18) 
button_count_1=Button(root,command=Count_Sats_Day,text="Amount Day",font=("Arial",12,"normal"))
var_id_amount=StringVar()
label_id_amount = Message(root,textvariable=var_id_amount, relief=RAISED,width=0.1,font=("Arial",12,"normal"))
var_id_amount_time=StringVar()
label_id_amount_time = Message(root,textvariable=var_id_amount_time, relief=RAISED,width=0.1,font=("Arial",12,"normal"))


def return_date_tm(note):
    import datetime
    date_2= datetime.datetime.fromtimestamp(float(note["created_at"])).strftime("%a"+", "+"%d "+"%b"+" %Y")
    date= date_2+ " "+ datetime.datetime.fromtimestamp(float(note["created_at"])).strftime('%H:%M')
   
    return date

def widget_function():  
   """Widget function \n
   View of PIN
   """
   if db_list!=[]: 
    frame3=tk.Frame(root,height=120,width= 700)
    canvas = tk.Canvas(frame3,width=600)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")  ))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    s=1    
    db_note_out=[]
    if db_list!=[]: 
       for note in db_list:
        if len(note["content"])<20:
         if len(db_note_out)<50:
           db_note_out.append(note)   
           try:
            var_id2=StringVar()
            label_id_2 = Message(scrollable_frame,textvariable=var_id2, relief=RAISED,width=200)
            var_id2.set(str(note["kind"])) 
            
            label_id_2.grid(pady=5,column=1,row=s)
            var_id=StringVar()
            label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=200)
            var_id.set(return_date_tm(note)) 
            label_id.grid(pady=5,column=0,row=s)
            invoice=lnbc_zap(note)
            var_id_3=StringVar()
            label_id_3 = Message(scrollable_frame,textvariable=var_id_3, relief=RAISED,width=200)
            if invoice:
              amount=bolt11_amount(invoice)
              if amount:
                var_id_3.set(str(amount)+ " sats") 
                label_id_3.grid(pady=5,column=2,row=s)
            Nota=tag_description(note)    
            var_id_4=StringVar()
            label_id_4 = Message(scrollable_frame,textvariable=var_id_4, relief=RAISED,width=200)
            if Nota:
               pubkey=Nota["pubkey"]
               if pubkey in list(user_metadata.keys()):
                  var_id_4.set(str(user_metadata[pubkey]) )
               else:
                  var_id_4.set(pubkey[0:9])   
               label_id_4.grid(pady=5,column=3,row=s)   

            
            scroll_bar_mini1 = tk.Scrollbar(scrollable_frame)
            scroll_bar_mini1.grid( sticky = NS,column=4,row=s+1)
            second_label2 = tk.Text(scrollable_frame, padx=8, height=3, width=27, yscrollcommand = scroll_bar_mini1.set, font=('Arial',14,'bold'),background="#D9D6D3")
            context_tags=""
            for note_x in note["tags"]:
               context_tags=context_tags+str(note_x)+"\n"
            second_label2.insert(END,str(context_tags))
            scroll_bar_mini1.config( command = second_label2.yview )
            second_label2.grid(padx=10, column=1, row=s+1,pady=5,columnspan=3) 
            def print_id(test):
               try: 
                if tags_string(test,"title")!=None and tags_string(test,"title")!=[]:
                 print("title ",tags_string(test,"title")[0])
                print("hashtag ",tags_string(test,"t"))
                
          
               except IndexError as e:
                  print (e) 

            def print_var(test):
                print(test)

            def value_result(test):
               if test["kind"]==9735:
                nota_=tag_description(test)
                if nota_:
                    show_print_test_tag(nota_)
               
                    
            button=Button(scrollable_frame,text=f"Print note ", command=lambda val=note: print_var(val))
            button.grid(column=0,row=s+1,padx=10,pady=5)
            button_grid2=Button(scrollable_frame,text=f"Note info ", command=lambda val=note: value_result(val))
            button_grid2.grid(row=s,column=4,padx=10,pady=5)
            root.update_idletasks()
            s=s+2
           except IndexError as e:
              print(e) 
   
    canvas.pack(side="left", fill="y", expand=True)
    scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.35,rely=0.4,relwidth=0.6)      
    
    def Close_print():
       frame3.destroy()  
    
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)       

button_close_=tk.Button(root,text="Widget",command=widget_function, font=('Arial',12,'bold'))
button_close_.place(relx=0.55,rely=0.42)       

root.mainloop()