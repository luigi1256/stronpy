#call a pubkey like lumina 6300 for photo kind20 
import asyncio
from nostr_sdk import Client, Filter, Keys, NostrSigner, init_logger, LogLevel, PublicKey,Kind
from nostr_sdk import EventId, Event,EventBuilder, Metadata,Tags,Tag,RelayUrl
from datetime import timedelta
import json
import random

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z

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

def evnt_id(id):
     test2=EventId.parse(id)
     return test2

def evnts_ids(list_id):
     Event=[]
     for j in list_id:
        Event.append(evnt_id(j))
     return Event

#Tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
root = tk.Tk()
root.title("DVM Example")
root.geometry("1300x800")
from tkinter import messagebox 

Section_frame = ttk.LabelFrame(root, text="DVM Section", labelanchor="n", padding=10)
Section_frame.place(relx=0.01,rely=0.18,relheight=0.24,relwidth=0.24) 
database_frame = ttk.LabelFrame(root, text="DB Section", labelanchor="n", padding=10)
database_frame.place(relx=0.01,rely=0.45,relheight=0.24,relwidth=0.24) 
T = tk.Text(root, height=45, width=90 )
Frame_drop=tk.Frame(root,height=40,width= 80)

def content_string(x,obj):
    from ast import literal_eval
    f=x['content']
    z=[]
    if f!="":
     t=literal_eval(f)
     if t!=None:
      for j in t:
       if j!=None:
        if j[0]==obj:
         z.append(j[1])
    return z

def note_list_d(list_id):
    L=[]
    if __name__ == "__main__":
     test_kinds = list_id  
     test_kind = asyncio.run(Get_id(test_kinds))
    L=get_note(test_kind)
    return L

def search_user_kind(user:PublicKey,x:int):
    if __name__ == "__main__":
     # Example usage with a single key
     single_author = user 
     single_results = asyncio.run(main_simple_kind(single_author))
    Z=[]
    note=get_note(single_results)
    for r in note:
       if (r)['kind']==x:
          Z.append(r)

    return Z

def search_three():
   zeta_metadata=[]
   for event in db_six_three_list:
      if event["kind"]==int(0):
         zeta_metadata.append(event)
   return zeta_metadata

def number_kind(tm):
    z=[]
    for v in tm:
        if (v)['kind'] in z:
              None  
        else:
              z.append((v)['kind'])
    return z

def print_database():
   
    if db_six_three_list!=[]:
        print("number note"," ",len(db_six_three_list))
        t,number=event_number(db_six_three_list)
        print("first event kind", db_six_three_list[0]["kind"])

def event_number(tm):
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
    while j<len(number):
     print("kind number", t[j] ,"number event", len(number[j]))
     j=j+1
    return t, number

def more_link(f):
   
   list_video=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_video:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam" 

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

def photo_list_frame_2(note):
 frame_pic=tk.Frame(root,height=80,width= 80) 
 
 balance,list_note1=balance_photo_print(note)
 int_var=IntVar()
 lbel_var=Entry(frame_pic, textvariable=int_var)    
 if list_note1!=[]: 
  if list_note1!=None and balance!=None:
   stringa_pic=StringVar()

   def next_number():
      if int((int(lbel_var.get())+1))< len(list_note1):
       int_var.set(int(lbel_var.get())+1)
       print_photo()
      else:
          int_var.set(int(0)) 
          print_photo()
     
   def print_photo():
     s=0  
     stringa_pic.set(list_note1[int(lbel_var.get())])
     label_pic = Entry(frame_pic, textvariable=stringa_pic)
     image_label = tk.Label(frame_pic)
     image_label.grid(column=1,row=s, columnspan=2)
     if label_pic.get()!="":
      if codifica_link_(label_pic.get())=="pic" and label_pic.get().startswith("https://bitcointwitter.web.app/") is False:   
       print(label_pic.get())
       try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(label_pic.get(),headers=headers, stream=True)
       
        response.raise_for_status()
        
   
        
        with open('my_image.png', 'wb') as file:
          shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image,UnidentifiedImageError
        image = Image.open('my_image.png','r')
        
        if balance!=[]:
          number=balance[int(lbel_var.get())]
        else:
           number=float(image.width//image.height) 
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
        button_close.grid(column=2,columnspan=1,row=s+1,pady=5)
        button_close_photo=Button(frame_pic,command=close_one_pic,text="Next",font=("Arial",12,"bold"))
        button_close_photo.grid(column=1,row=s+1,pady=5)
        s=s+2
       except TypeError as e: 
            print(e)  
       except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")  
      else:
          print(label_pic.get())
   print_photo()
   frame_pic.place(relx=0.62,rely=0.2,relwidth=0.3) 
  else:
     print("error", "none")        
 else:
     print("error", note["tags"])

async def main_simple_kind(authors):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    relay_url_1 = RelayUrl.parse("wss://nostr.mom/")
    relay_url_2 = RelayUrl.parse("wss://nos.lol/")
    relay_url_3 = RelayUrl.parse("wss://relay.nostrdvm.com/")
    relay_url_4 = RelayUrl.parse("wss://nostr.oxtr.dev/")
    await client.add_relay(relay_url_1)
    await client.add_relay(relay_url_2)
    await client.add_relay(relay_url_3)
    await client.add_relay(relay_url_4)    
 
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(authors, list):
        combined_results = await get_relays(client, authors)
    else:
        combined_results = await get_relay(client, authors)
    
    return combined_results

async def get_relays(client, authors):
    f = Filter().authors(authors)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

people_list=[]
db_verify=[]
db_six_three_list=[]

def db_print_verify():
   if db_verify!=[]:
    print(len(db_verify)-len(db_six_three_list), " Error")
    print(db_verify[0])
    for verify_x in db_verify:
       if verify_x=="False":
          messagebox.showwarning("Maybe there is false", "there is a False")

async def get_relay(client, user):
    f = Filter().author(user).kinds([Kind(6300),Kind(5300),Kind(0)]).limit(100)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z=[]
    for event in events.to_vec():
       if event.verify_signature():
          db_verify.append(event.verify_signature())
          z.append(event.as_json())
       else:
          db_verify.append(event.verify_signature())
          print(event.as_json())   
    #z = [event.as_json() for event in events.to_vec()]
    if z!=[]:
     return z
 
async def get_Event(client, event_):
    f = Filter().ids(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    relay_url_1 = RelayUrl.parse("wss://nos.lol/")
    await client.add_relay(relay_url_1)
    relay_url_x = RelayUrl.parse("wss://nostr.mom/")
    await client.add_relay(relay_url_x)
    
    await client.connect()

    if isinstance(event_, list):
        test_kind = await get_Event(client, event_)
    else:
        print("errore")
    return test_kind

#not used now
def note_list(list_follow):
    L=[]
    if __name__ == "__main__":
     test_people = list_follow
     combined_results = asyncio.run(main_simple_kind(test_people))
    L=get_note(combined_results)
    return L

test1="4add3944eb596a27a650f9b954f5ed8dfefeec6ca50473605b0fbb058dd11306"
test="184c36270491232b7cbba2ca2e7cc10f965346755ff462d66f9efb517a867cd2"
Test_dvm=[test,test1]

def dvm_(event):
    if combo_dvm.get()!="": 
        
        if db_six_three_list!=[]:
         db_six_three_list.clear()
         button_op.place_forget()
        dvm_tm=search_user_kind(convert_user(combo_dvm.get()),6300)
        for dvm_note in dvm_tm:
              if dvm_note not in db_six_three_list:
               if content_string(dvm_note,"e")!=[]:
                db_six_three_list.append(dvm_note)
        if dvm_tm!=None:
            button_op.place(relx=0.33,rely=0.14)

combo_dvm = ttk.Combobox(root, values=Test_dvm,width=30)
combo_dvm.place(relx=0.02,rely=0.1)
combo_dvm.set("")
combo_dvm.bind("<<ComboboxSelected>>", dvm_)
lab_c_dvm = tk.Label(root, text="DVM Preset: ", font=('Arial',12,'bold'))
lab_c_dvm.place(relx=0.06,rely=0.06)
  
def create_dropdown():
 if combo_dvm.get()!="": 
  if db_six_three_list!=[]:
     db_six_three_list.clear()
  dvm_tm=search_user_kind(convert_user(combo_dvm.get()),6300)
  for dvm_note in dvm_tm:
    if dvm_note not in db_six_three_list:
     if content_string(dvm_note,"e")!=[]:
      db_six_three_list.append(dvm_note)
  if dvm_tm!=None:
   button_op.place(relx=0.33,rely=0.14)
   my_dvm_ = []
   for j in dvm_tm:
    if j['pubkey'] not in my_dvm_:
     my_dvm_.append(j['pubkey'])
   def dvm_(event):
    selected_it = combo_do.get()
    dvm_one=convert_user(selected_it)
    metadata=search_user_kind(dvm_one,0)
    for dvm_metadata in metadata:
     if dvm_metadata not in db_six_three_list:
      db_six_three_list.append(dvm_metadata)
    if len(metadata)> 0:
     
     if len(json.loads(metadata[0]['content'])['about'])<80:
        lab_dvm.config(text="Name: " + str(json.loads(metadata[0]['content'])['name']) +"\n"+str(json.loads(metadata[0]['content'])['about'][0:30]) +"\n"+ str(json.loads(metadata[0]['content'])['about'][30:60]))                    
                
    else:
        metadata_new=search_three()  #bug
        if metadata_new!=[]:
          lab_dvm.config(text="Name: " + str(json.loads(metadata_new[0]['content'])['name']) +"\n"+str(json.loads(metadata_new[0]['content'])['about'][0:30]) +"\n"+ str(json.loads(metadata_new[0]['content'])['about'][30:60]))                    

        else: 
            lab_dvm.config(text="Name:Not found ")

   lab_dvm = tk.Label(Frame_drop, text="Name: Summary: ", background="darkgrey",font=('Arial',12,'normal'),width=30)
   lab_dvm.grid(column=1,row=6,pady=5, ipadx=2,columnspan=2)
   combo_do = ttk.Combobox(Frame_drop, values=my_dvm_,width=20, font=('Arial',12,'normal'))
   combo_do.grid(column=1,row=5,pady=5, ipadx=2,columnspan=2)
   combo_do.set("Option 1")
   combo_do.bind("<<ComboboxSelected>>", dvm_)

   def creat_closure():
      Frame_drop.place_forget()
      if db_six_three_list==[]:
         button_op.place_forget()

   test_c_button=Button(Frame_drop,command=creat_closure,text="Closure",font=('Arial',12,'normal'))
   test_c_button.grid(column=2,row=4,pady=5,padx=5)
   Frame_drop.place(relx=0.02,rely=0.2)
  
test_button=Button(root,command=create_dropdown,text="Load DVM",font=('Arial',12,'normal'))
test_button.place(relx=0.03,rely=0.21)

def add_db_list():
        
        Frame_block=Frame(root,width=50, height=10)
        button_s_=Button(Frame_block, text='print',font=('Arial',12,'bold'), comman=print_database ) 
        button_s_.grid(column=1, row=2, padx=5,pady=5) 
        test_D_button=Button(Frame_block,command=db_print_verify,text="Verify", font=('Arial',12,'bold'))
        test_D_button.grid(column=0,row=2,padx=5,pady=5)
            
        def Close_block(event):
            Frame_block.place_forget()
           
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=3, row=0, padx=5, rowspan=2) 
           
        def search_block_list():
            label_string_block1.set(len(db_six_three_list))
            label_block_list1["background"]="darkgrey"
            
        def delete_block_list():
            db_six_three_list.clear()
            label_string_block1.set(len(db_six_three_list))  
            messagebox.askokcancel("What clear also verify?","Yes or No")
            db_verify.clear()

        def delete_first_note():
             if db_six_three_list!=[]:
              db_six_three_list.pop(0)
              label_string_block1.set(len(db_six_three_list))    

        random_block_2=Button(Frame_block, command=delete_first_note, text= "Delete 1: ",font=('Arial',12,'normal'))
        random_block_2.grid(column=2,row=2,padx=5,pady=5)      
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey",font=('Arial',12,'normal'))
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ",background="darkgrey",font=('Arial',12,'normal'))
        random_block1.grid(column=1,row=0,padx=5,pady=5)
        label_string_block1=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1,font=('Arial',12,'normal'))
        label_block_list1.grid(column=2,row=0,padx=5,pady=5)
        Frame_block.place(relx=0.02,rely=0.55)
        
button_block_1=tk.Button(root, highlightcolor='WHITE',
                  text='DB 6300',
                  command=add_db_list,height=1,border=2, cursor='hand1',
                  font=('Arial',12,'normal'))
button_block_1.place(relx=0.05,rely=0.5, anchor="n")
db_event_recipient=[]

def event_rand_num():
   if db_event_recipient>100:
      random.shuffle(db_event_recipient)
      return db_event_recipient[0:100]
   else:
      if db_event_recipient!=[]:
       number_var= random.Random.randint(0, len(db_event_recipient))
       return db_event_recipient[number_var:]

def show_print_test_tag(note):
   frame3=tk.Frame(root,height=150,width=200)  
   canvas_2 = tk.Canvas(frame3,height=450)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = ttk.Frame(canvas_2)

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")))

   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
   context0:str="Pubkey "+str(note['pubkey'])+"\n"+"Time: "+ str(return_date_tm(note))+"\n"
   if note['tags']!=[]:
        context1:str="Number of Note "+" "+str(len(content_string(note,"e")))+"\n"
        
        context2:str=""+"\n"
   else: 
        context1:str="content: "+"\n"+str(note['content'])+"\n"
        context2:str=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=250,font=("Arial",12,"normal"))
   var_id.set(str(context0+context1+context2))
   label_id.grid(pady=2,column=0, columnspan=3)

   def print_var(entry):
        pic_show(entry)

   def call_photo(entry):
    photo_list_frame_2(entry)     
        
   def print_content(entry):
      test=content_string(entry,"e")
      if test!=[]:
       test1=evnts_ids(test)
       reverse=note_list_d(test1)
       if reverse!=[]: 
        for result_x in reverse:
           if result_x not in db_event_recipient:
              db_event_recipient.append(result_x)
       if reverse!=[]: 
        if len(reverse)>80:
         reverse=reverse[0:80]
         print("too many note",len(reverse))
        else:
         pass 
        s=4        
        for jresult in reverse:
           if jresult["id"]!=entry["id"]:  
             context00="Pubkey: "+jresult['pubkey']+"\n"+"id: "+jresult["id"]+"\n"+"Time: "+ str(return_date_tm(jresult))+"\n"
             if jresult['tags']!=[]:
              context11=jresult['content']+"\n"
              context22="Tags"+"\n"+"Number of tags photo "+str(len(tags_str(jresult,"imeta")))
             else: 
              context11=jresult['content']+"\n"
              context22=""
             var_id_1=StringVar()
             label_id_1 = Message(scrollable_frame_2,textvariable=var_id_1, relief=RAISED,width=250,font=("Arial",12,"normal"))
             var_id_1.set(context00)
             label_id_1.grid(pady=2,column=0, columnspan=3,row=s)
             scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
             second_label10 = tk.Text(scrollable_frame_2, padx=4, height=5, width=28, yscrollcommand = scroll_bar_mini.set, font=('Arial',12,'bold'),background="#D9D6D3")
             second_label10.insert(END,context11+"\n"+str(context22))
             scroll_bar_mini.config( command = second_label10.yview )
             second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 

             button_ph=Button(scrollable_frame_2,text=f" See Photo", command=lambda val=jresult: print_var(val))
             button_ph.grid(row=s+2,column=0,padx=5,pady=5)
             button_ph_1=Button(scrollable_frame_2,text=f" slide Photo", command=lambda val=jresult: call_photo(val))
             button_ph_1.grid(row=s+2,column=1,padx=5,pady=5)
             root.update_idletasks()
             s=s+3      

   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply!", command=lambda val=note: print_content(val),font=("Arial",12,"normal"))
    button_grid3.grid(row=s,column=0,padx=5,pady=5)    
          
   scrollbar_2.pack(side="right", fill="y",padx=5,pady=1) 
   canvas_2.pack( fill="y", expand=0.9)
   
   def close_frame():
     frame3.destroy()    
   
   button_frame=Button(scrollable_frame_2,bg="darkgrey",command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.grid(row=s+1,column=1, columnspan=2,pady=5)      
   frame3.place(relx=0.3,rely=0.19,relheight=0.52,relwidth=0.25) 

def respond_to():
    if db_six_three_list!=[]:
     show_print_test_tag(db_six_three_list[0])

def return_date_tm(note):
    import datetime
    import calendar
    date_2= datetime.datetime.fromtimestamp(float(note["created_at"])).strftime("%a"+", "+"%d "+"%b"+" %Y")
    date= date_2+ " "+ datetime.datetime.fromtimestamp(float(note["created_at"])).strftime('%H:%M')
   
    return date

button_op=Button(root, text="Open", command=respond_to, font=("Arial",12,"normal"))

def show_db_list():
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
   

   def print_var(entry):
        #print(entry["id"])
        pic_show(entry)
        
   if db_event_recipient!=[]:
      reverse=db_event_recipient       
      for jresult in reverse:
             
             context00="Pubkey: "+jresult['pubkey']+"\n"+"id: "+jresult["id"]+"\n"+"Time: "+ str(return_date_tm(jresult))+"\n"
             if jresult['tags']!=[]:
              context11="content: "+"\n"+jresult['content']+"\n"
              context22="Tags"+"\n"+"Number of tags photo "+str(len(tags_str(jresult,"imeta")))
             else: 
              context11="content: "+"\n"+jresult['content']+"\n"
              context22=""
             var_id_1=StringVar()
             label_id_1 = Message(scrollable_frame_2,textvariable=var_id_1, relief=RAISED,width=300,font=("Arial",12,"normal"))
             var_id_1.set(context00+context11+context22)
             label_id_1.grid(pady=2,column=0, columnspan=3)
             button_ph=Button(scrollable_frame_2,text=f" See Photo", command=lambda val=jresult: print_var(val))
             button_ph.grid(column=0,columnspan=2,padx=5,pady=5)
             root.update_idletasks()
       
      scrollbar_2.pack(side="right", fill="y",padx=5,pady=1) 
      canvas_2.pack( fill="y", expand=True)
      
      def close_frame():
       frame3.destroy()    
   
      button_frame=Button(scrollable_frame_2,bg="darkgrey",command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
      button_frame.grid(column=1, columnspan=2,pady=5)      
      frame3.place(relx=0.6,rely=0.19,relheight=0.35,relwidth=0.32) 

#Image
import requests
import shutil
from PIL import Image, ImageTk

def pic_show(x):
   
   if tags_str(x,"imeta")!=[]:
    for dim_photo in tags_str(x,"imeta"):
     if codifica_link_(dim_photo[1][4:])=="pic": 
      try: 
       headers = {"User-Agent": "Mozilla/5.0"}
       response = requests.get(dim_photo[1][4:], headers,stream=True)
       response.raise_for_status()
       if response.status_code == 200:
        with open('my_image.png', 'wb') as file:
          shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image,UnidentifiedImageError
        img = Image.open('my_image.png')
        img.show()
       else:
        print("Error of image") 
      except TypeError as e: 
        print(e)  
      except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")  
      except (requests.exceptions.RequestException, ConnectionRefusedError,UnidentifiedImageError) as e:
       print(e)       

def url_link(url):
 z=url
 if z[0:5]=="https":
        return str(z)

def codifica_link_(url):
   f=url_link(url)
   list_video=['mov','mp4']
   audio=['mp3']
   img=['jpg','png','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_video:
        return "video"
   if f[-3:] in audio:
        return "audio"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam"

def note_recipient():
   if db_six_three_list!=[]:
    entry=db_six_three_list[0]
    test=content_string(entry,"e")
    if test!=[]:
       test1=evnts_ids(test)
       reverse=note_list_d(test1)
       if reverse!=[]: 
        for result_x in reverse:
           if result_x not in db_event_recipient:
              db_event_recipient.append(result_x)

def search_db_list():
            var_string_photo.set(len(db_event_recipient))
            label_string_["background"]="darkgrey"

Feed_frame = ttk.LabelFrame(root, text="Feed Section", labelanchor="n", padding=10)
Feed_frame.place(relx=0.58,rely=0.03,relheight=0.12,relwidth=0.35) 
button_db_frame=Button(root,bg="darkgrey",command=show_db_list,text="Show Open",font=("Arial",12,"normal"))
button_db_frame.place(relx=0.82,rely=0.08)
button_con_=Button(root,bg="darkgrey",command=note_recipient,text="Convert Note",font=("Arial",12,"normal"))
button_con_.place(relx=0.6,rely=0.08)               
random_db_note=Button(root, command=search_db_list, text= "DB photo: ",background="darkgrey",font=('Arial',12,'normal'))
random_db_note.place(relx=0.7,rely=0.08) 
var_string_photo=StringVar()
label_string_=Label(root, textvariable=var_string_photo,font=('Arial',12,'normal'))
label_string_.place(relx=0.78,rely=0.09) 
      
root.mainloop()