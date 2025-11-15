#widget 1 
import asyncio
from nostr_sdk import Client, Filter, Keys, NostrSigner, init_logger, LogLevel, EventBuilder, Metadata,Kind
from nostr_sdk import *
from nostr_sdk import Keys,Filter,Client, Event,EventBuilder,Metadata,PublicKey,EventId,Nip19Event,Nip19,Nip19Profile,Nip21,Timestamp
from datetime import timedelta 
import textwrap
import json
import ast
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import calendar
from asyncio import get_event_loop
import requests
import shutil
from PIL import Image, ImageTk

root = Tk()
root.title("Search Items")
root.geometry("1300x800")
db_pin=[{"Sell item":30402},{"Bookmark sets":30003},{"Book review":31025},{"Book progress":30250} ]
my_kind = { "Sell item":30402,
             "Bookmark sets":30003,
             "Book review":31025,
             "Book progress":30250 }
db=[]
db_note=[]
relay_list=[]
public_list=[]
my_tag = list(my_kind.keys())
entry_channel=StringVar()
amount_price=IntVar()
sats_ = IntVar() 
alt_string= IntVar()

def tags_string(x,obj):
    f=x['tags']
    z=[]
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

def Open_source(key):
  
     test=[]
     if __name__ == "__main__":
      test_kinds = [Kind(my_kind[key])]  
      test = asyncio.run(Get_event_from(test_kinds))
     if test!=[]:
      note= get_note(test)
      for xnote in note:
        if xnote not in db_note:
         db_note.append(xnote)
         hash_list_notes.append(xnote) 

async def get_kind_relay(client, event_):
    f = Filter().kinds(event_).limit(16)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_kind(client, event_):
    if public_list!=[]:
     f = Filter().kinds(event_).author(public_list[0])
    else:
       
       f = Filter().kinds(event_).limit(50)
    try:
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10)) 
     z=[] 
     for event in events.to_vec():
      if event.tags().identifier()!=None:
       if event.verify_signature():
          
          z.append(event.as_json())
     if z!=[]:      
      return z
    except NostrSdkError as e:
       print (e)
           
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

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z   

def url_photo_print(nota):
  if tags_str(nota,"image")!=[]:
   url_=[]
   for url_x in  tags_string(nota,"image"):
      if url_x not in url_:
         url_.append(url_x)
   if url_!=[]:
      return url_      

def photo_list_frame_2(note):
 frame_pic=tk.Frame(root,height=80,width= 80) 
 
 list_note1=url_photo_print(note)
 int_var=IntVar()
 lbel_var=Entry(frame_pic, textvariable=int_var)    
 if list_note1!=None: 
   
   def next_number():
      if int((int(lbel_var.get())+1))< len(list_note1):
       int_var.set(int(lbel_var.get())+1)
       print_photo()
      else:
          int_var.set(int(0)) 
          print_photo()
     
   stringa_pic=StringVar()
   number_note=Label(frame_pic,text="N° Photo "+str(len(list_note1)), font=("SF Pro",14,"bold"))
   number_note.grid(column=1,row=0,columnspan=2)
   def print_photo():
     s=1 
     stringa_pic.set(list_note1[int(lbel_var.get())])
     label_pic = Entry(frame_pic, textvariable=stringa_pic)
     image_label = tk.Label(frame_pic)
     image_label.grid(column=1,row=s, columnspan=2)
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
        number=float(image.width/image.height)
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
      except TypeError as e: 
        print(e)  
      except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")    
   print_photo()     
   frame_pic.place(relx=0.7,rely=0.3,relwidth=0.3) 
     
 else:
     print("error", "[]")

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)

    # Add relays and connect
    relay_url_x = RelayUrl.parse("wss://nostr.mom/")
    relay_url_1 = RelayUrl.parse("wss://relay.damus.io/")
    await client.add_relay(relay_url_x)
    await client.add_relay(relay_url_1)
    
    if relay_list!=[]:
      for jrelay in relay_list:
         relay_url = RelayUrl.parse(jrelay)
         await client.add_relay(relay_url)
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

def print_text():  
    
    frame3=tk.Frame(root,height=120,width= 250)
    canvas = tk.Canvas(frame3,width=250)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    s=1    
    if db_pin!=[]: 
        for note in db_pin:
           
            var_id=StringVar()
            label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=340)
            var_id.set(note[list(note.keys())[0]]) 
            label_id.grid(pady=2,column=1,row=s)
            
            def print_var(test):
                                
                if list(test.keys())[0]=="Sell item":
                   
                   var_id_test=StringVar()
                   label_id_test = Message(scrollable_frame,textvariable=var_id_test, relief=RAISED)
                   var_id_test.set("This is kind of event 30402 and than is multiple things like craiglist") 
            
                   label_id_test.grid(pady=2,column=0,row=s+1, columnspan=2)
                after_tag()  
                number_event= search_for_kind(test[list(test.keys())[0]])
                show_noted()
                                              
            button=Button(scrollable_frame,text=f"{list(note.keys())[0]}", command=lambda val=note: print_var(val))
            button.grid(column=0,row=s,padx=20,pady=5)
            button_grid2=Button(scrollable_frame,text=f"Search kind ", command=lambda val=note: Open_source(list(val.keys())[0]))
            button_grid2.grid(row=s,column=2,padx=5,pady=5)
            root.update()  
            s=s+1
   
    canvas.pack(side="left", fill="y", expand=True)
    scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.01,rely=0.33,relwidth=0.27)      

    def Close_print():
       frame3.destroy()  
       entry_t.place_forget()
       button_s.place_forget()
       label_title.place_forget()
       entry_string.place_forget()
       button_s_1.place_forget()
       label_title_1.place_forget()

    entry_t.place(relx=0.04,rely=0.78,relwidth=0.17)
    button_s.place(relx=0.22,rely=0.77)
    label_title.place(relx=0.07,rely=0.74)
    
    entry_string.place(relx=0.04,rely=0.88)
    button_s_1.place(relx=0.15,rely=0.87)
    label_title_1.place(relx=0.07,rely=0.84)
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)       

hash_list_notes=[]

def search_for_kind(kind_int:int):
     Notes=db_note
     if Notes!=[]:
        hash_list_notes.clear()
        for note_x in Notes:
            if note_x["kind"]==kind_int:  
               hash_list_notes.append(note_x)
        return hash_list_notes   

def after_tag():
     Notes=db_note
     if Notes:
        hash_list_notes.clear()
        for note_x in Notes:
            hash_list_notes.append(note_x)
        return hash_list_notes    

def search_for_channel(note_hash):
     Notes=db_note
     if Notes:
        hash_list_notes.clear()
        for note_x in Notes:
            if note_hash in tags_string(note_x,"t"): 
               hash_list_notes.append(note_x)
        return hash_list_notes    

def Alt_tag(note):
   if alt_string.get()==1:
     try:   
       if tags_string(note,"alt")!=[]:
         if tags_string(note,"alt")[0]!="":
            return note
     except NostrSdkError as e:
        print(e)      
   else:
      return(note)
      
def show_noted():
 frame2=tk.Frame(root,)  
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
 if hash_list_notes!=[]:
  
  s=1
  s1=0
  list_note=is_price_amount(hash_list_notes)
  if list_note!=None:
   for note in hash_list_notes:
    if price_amount(note):
     if Alt_tag(note): 
      try:
       context0=str("")
       context2=str("")
       context0=context0+str("Author: ")+str(note['pubkey'])
       if tags_string(note,"title")!=[]:
        for ynote in tags_string(note,"title"):
         context0=context0+"\n"+"Title "+str(ynote) 
       for xnote in tags_string(note,"alt"):
         context2=context2+"\n"+str(xnote) +"\n"
       if tags_string(note,"summary")!=[]: 
         for xnote in tags_string(note,"summary"):
          context2=context2+"\n"+"Summary "+tags_string(note,"summary")[0]+"\n"
       if len(tags_string(note,"t"))==1:
         for xnote in tags_string(note,"t"):
          context2=context2+"Category "+str(xnote) +" "  
       else:
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context2=context2+"#"+str(xnote) +" "
            s=s+1
       price=""     
       for xnote_z in tags_str(note,"price"):
          price=price+" "+ str(xnote_z)+" "
       if price!="":   
        context2=context2+"\n"+"Price "+str(price) +"\n"        
       if note["kind"]!=30402:
            context2=context2+"\n"+"kind "+str(note["kind"]) +"\n"                                  
            for xnote_a in tags_string(note,"d"):
             context2=context2+"\n"+"identifier "+str(xnote_a) +"\n"    
            for xnote_z in tags_string(note,"i"):
                context2=context2+"\n"+str(xnote_z) +"\n"    
            for xnote_x in tags_string(note,"k"):
              context0=context0+"\n"+str(xnote_x) +"\n"       
            for xnote_c in tags_string(note,"unit"):
              context2=context2+"\n"+"Unit "+str(xnote_c) +"\n"   
             
            for xnote_v in tags_string(note,"current"):
               context2=context2+"\n"+"Current page "+str(xnote_v) +"\n"    

            for xnote_b in tags_string(note,"max"):

               context2=context2+"\n"+"Max Page "+str(xnote_b) +"\n"     
            for xnote_n in tags_string(note,"started"):
              context2=context2+"\n"+"Started "+str(xnote_n) +"\n"
            if tags_string(note,"rating")!=[]:   
             for xnote_s in tags_string(note,"rating"):
               context2=context2+"\n"+"Rating "+str(xnote_s) +"\n"
            if tags_string(note,"raw")!=[]:   
             for xnote_d in tags_string(note,"raw"):
               context2=context2+"\n"+"Raw "+str(xnote_d) +"\n"      

        
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=6, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=1) 
      
       def print_id(entry):
           number=list(hash_list_notes).index(entry)
           if tags_string(entry,"t")==[]:
              print(entry['tags'])
           
           def print_content(entry):
             test1=[]
             for hashtag_x in tags_string(entry,"t"):
              if hashtag_x not in test1:
                 test1.append(hashtag_x)
             if test1!=[]:
               s=5
               ra=0
               se=1
               ti=2
               
               def show_tag(entry):
                  hashtag_list=search_for_channel(entry)
                  if hashtag_list:
                    if len(hashtag_list)>1: 
                     show_noted()
               #for word in test1:
               #if word in block_hashtag_word:
               #test1.remove(word)
               test1.sort()
     
               while ra<len(test1):
   
                  button_grid1=Button(scrollable_frame_1,text=f"{test1[ra]} ", command=lambda val=test1[ra]: show_tag(val),background="darkgrey")
                  button_grid1.grid(row=s,column=0+number*4,padx=5,pady=5)
 
                  if len(test1)>se:
                     button_grid2=Button(scrollable_frame_1,text=f"{test1[ra+1]}", command= lambda val=test1[ra+1]: show_tag(val),background="darkgrey")
                     button_grid2.grid(row=s,column=1+number*4,padx=5,pady=5)
                  if len(test1)>ti:
                     button_grid3=Button(scrollable_frame_1,text=f"{test1[ra+2]}", command= lambda val=test1[ra+2]: show_tag(val),background="darkgrey")
                     button_grid3.grid(row=s,column=2+number*4,padx=5,pady=5)   
     
                  root.update()  
                  s=s+1
                  se=se+3
                  ra=ra+3
                  ti=ti+3   
           print_content(entry)
            
       def print_var(entry):
                print(entry["content"])
                share_naddr(entry)
                shopstr_event(entry)
                               
       button=Button(scrollable_frame_1,text=f"Print me ", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
       button_grid2.grid(row=2,column=s1+1,padx=5,pady=5)    
       if tags_string(note,"image")!=[]:
        button_grid3=Button(scrollable_frame_1,text=f"Click to see", command=lambda val=note: photo_list_frame_2(val))
        button_grid3.grid(row=2,column=s1+2,padx=5,pady=5)  
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="bottom", fill="x",padx=20)
   scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
   canvas_1.pack( fill="y", expand=True)
   frame2.place(relx=0.35,rely=0.35,relwidth=0.31) 

   def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.5,rely=0.74,relwidth=0.1)      

button_read=Button(root,text="Stamp", command=show_noted,font=("Arial",12,"normal"))

def list_hashtag_fun():
    hashtag_list=[]
    if db_note!=[]:
        for note_x in db_note:
            if tags_string(note_x,"t")!=[]:
                for hash_y in tags_string(note_x,"t"):
                    if hash_y not in hashtag_list:
                        hashtag_list.append(hash_y)
        return hashtag_list      

def is_price_amount(list_note):
   is_empty=[]
   if list_note!=[]:
      for note_x in list_note:
         tag_note=price_amount(note_x)
         if tag_note!=None and tag_note not in is_empty:
            is_empty.append(tag_note)
   if is_empty!=[]:
      return is_empty
               
def price_amount(note):
 if sats_.get()==1: 
  try: 
   if tags_string(note,"price")!=[]:
      
      if tags_str(note,"price")[0][2]=="SATS" or tags_str(note,"price")[0][2]=="SAT":
        if int(tags_string(note,"price")[0])>amount_price.get():
           return note
  except IndexError as e:
     print(e)  
     print(tags_str(note,"price"))
 else:
    return note    

def print_list_tag(): 
   if db_note!=[]:  
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=250)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas,border=2)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    s=1     
    test1=list_hashtag_fun()
    if test1:
            test1.sort()    
            def print_id(test):
                entry_channel.set(test)
                Channel_frame = ttk.LabelFrame(root, text="Associated tag", labelanchor="n", padding=10)
                Channel_frame.place(relx=0.52,rely=0.01,relheight=0.18,relwidth=0.4) 
                button_open=Button(root, command=show_noted, text="Open Tag",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
                Alt_tag= Checkbutton(root, text = "Alt Tag ", 
                    variable = alt_string,
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    font=('Arial',14,'bold'))
                Alt_tag.place(relx=0.83,rely=0.1)  
                
                def slide_r1():
                    amount_price.set(int(menu_slider1.get())*1000)
                    label_amount_2.place_forget()
                    label_amount_2.config(text=f" {int(menu_slider1.get())} K SATS ")
                    label_amount_2.place(relx=0.38,rely=0.04)

                cash_frame = ttk.LabelFrame(root, text="Cash", labelanchor="n", padding=10)
                cash_frame.place(relx=0.28,rely=0.01,relheight=0.18,relwidth=0.22)   
                sats_only= Checkbutton(root, text = " ", 
                    variable = sats_,
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    font=('Arial',16,'normal'))
                sats_only.place(relx=0.42,rely=0.05)   
                label_amount=Label(root,text="Amount", font=("SF Pro",14,"bold"))
                label_amount.place(relx=0.3,rely=0.04)
                entry_amount=Entry(root,textvariable=amount_price)
                label_amount_2=Label(root,text=f"K SATS", font=("SF Pro",14,"bold"))
                label_amount_2.place(relx=0.4,rely=0.04)
                entry_amount.place(relx=0.3,rely=0.08,relwidth=0.08)
                menu_slider1=Scale(root,orient=HORIZONTAL)
                menu_slider1.place(relx=0.3,rely=0.11) 
                button_slider1=Button(root,command=slide_r1, text="Check",font=('Arial',12,'bold'))
                button_slider1.place(relx=0.41,rely=0.12)
                
                def close_cash():
                   button_clo_1.place_forget()
                   label_amount.place_forget()
                   label_amount_2.place_forget()
                   entry_amount.place_forget()
                   menu_slider1.place_forget() 
                   button_slider1.place_forget()
                   cash_frame.place_forget()
                   sats_only.place_forget()

                button_clo_1=Button(root,text="X", command=close_cash,font=('Arial',12,'bold'),foreground="red")
                button_clo_1.place(relx=0.47,rely=0.04)   
                number_list=search_for_channel(test)
                label_number=tk.Label(root,text=str(len(number_list)),font=("Arial",12,"bold"))
                entry_space=tk.Entry(root, textvariable=entry_channel, width=30)
                entry_space.place(relx=0.55,rely=0.11,relwidth=0.15)
                Label_channel_name=tk.Label(root, text="Hashtag",font=("Arial",12,"bold"))
                Label_channel_name.place(relx=0.57,rely=0.06)
                button_open.place(relx=0.71,rely=0.09)
                label_number.place(relx=0.75,rely=0.05)

                def close_button():
                   entry_channel.set("")
                   entry_space.place_forget()
                   button_clo.place_forget()
                   Label_channel_name.place_forget()
                   button_open.place_forget()
                   Channel_frame.place_forget()
                   Alt_tag.place_forget()
                   label_number.config(text="")
                   label_number.place_forget()

                button_clo=Button(root,text="Close", command=close_button,font=('Arial',12,'bold'),foreground="red")
                button_clo.place(relx=0.84,rely=0.04)   
           
            ra=0
            se=1
            
            while ra<len(test1):
            
                button_grid1=Button(scrollable_frame,text=f"{test1[ra]} ", command=lambda val=test1[ra]: print_id(val))
                button_grid1.grid(row=s,column=1,padx=5,pady=5)
                
                if len(test1)>se:
                 button_grid2=Button(scrollable_frame,text=f"{test1[ra+1][0:10]}", command= lambda val=test1[ra+1]: print_id(val))
                 button_grid2.grid(row=s,column=2,padx=5,pady=5)
            
                root.update()  
                s=s+1
                se=se+2
                ra=ra+2   

    else:
         print("error") #It didn't find a channel

    canvas.pack(side="left", fill="y", expand=True)
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.01,rely=0.33,relwidth=0.27)   

    def Close_print():
       frame3.destroy()  
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)    
   else:
      pass

label_event_ = tk.Label(root, text="Kind Events ", font=('Arial',12,'bold'))
label_event_.place(relx=0.02,rely=0.19)
label_tag = tk.Label(root, text="Hashtag ", font=('Arial',12,'bold'))
label_tag.place(relx=0.02,rely=0.26)
button4=tk.Button(root,text="? ",command=print_text,font=('Arial',12,'bold'))
button4.place(relx=0.1,rely=0.18)
button_tag=tk.Button(root,text="# ",command=print_list_tag, font=('Arial',12,'bold'))
button_tag.place(relx=0.08,rely=0.25)

def share_naddr(note):
    coord = Coordinate(Kind(note["kind"]),PublicKey.parse(note["pubkey"]),str(tags_string(note,"d")[0]))
    coordinate = Nip19Coordinate(coord, [])
    print(f" Coordinate (encoded): {coordinate.to_bech32()}")
    print(f" https://njump.me/{coordinate.to_bech32()}")

def shopstr_event(note):
    if tags_string(note,"client")!=[]:
       if tags_string(note,"client")[0]=="Shopstr":
        coord = Coordinate(Kind(note["kind"]),PublicKey.parse(note["pubkey"]),str(tags_string(note,"d")[0]))
        coordinate = Nip19Coordinate(coord, [])
        #print(f" Coordinate (encoded): {coordinate.to_bech32()}")
        print(f" https://shopstr.store/listing/{coordinate.to_bech32()}")
        market=note["pubkey"]
        print(f" https://shopstr.store/marketplace/{PublicKey.parse(market).to_bech32()}")

def search_title(string):
   if db_note!=[]:
      note_list=[]
      for note_x in db_note:
        if tags_string(note_x,"title")!=[]:
         for title in tags_string(note_x,"title"):
            title_list=title.split(" ")
            title_list = [str(title).lower() for title in title_list]
            if string in title_list:
               if note_x not in note_list:
                  note_list.append(note_x)
      
      if note_list!=[]:
       #print(len(note_list),"\n",note_list[0])            
       return note_list    

def search_for_note(note_found:list):
     if note_found!=[]:
        hash_list_notes.clear()
        for note_x in note_found:
            if note_x not in hash_list_notes: 
               hash_list_notes.append(note_x)
        return hash_list_notes    

def search_title_c(string):
   if string!="":
    search_note= []
    title_string=string.split(" ")
    title_string = [str(string_).lower() for string_ in title_string]
    for string_in in title_string:
      note_list=search_title(string_in)
      if note_list!=None: 
        for note_x in note_list:
         if note_x not in search_note:
            search_note.append(note_x) 
    if search_note!=[]:
       print("Search, ",string,"\n","Number of note ",len(search_note))
       title_s.set("")
       search_for_note(search_note)
       show_noted()
       return search_note     
    


title_s=StringVar()
entry_t=tk.Entry(root, textvariable=title_s, width=15,font=('Arial',12,'normal'))
button_s=Button(root,text="Search", command=lambda: search_title_c(entry_t.get()),font=('Arial',12,'normal'))
label_title=Label(root,text="Title", font=("SF Pro",14,"bold"))

def search_d_tag(string):
   if string!="":
    search_note= []
    if db_note!=[]:
       for j_note in db_note:
          if string in tags_string(j_note,"d"):
            if j_note not in search_note:
             search_note.append(j_note) 
    if search_note!=[]:
       print("Search, ",string,"\n","Number of note ",len(search_note))
       d_string.set("")   
       search_for_note(search_note)
       show_noted()
       return search_note     
    

d_string=StringVar()
entry_string=tk.Entry(root, textvariable=d_string, width=15,font=('Arial',12,'normal'))
button_s_1=Button(root,text="Search", command=lambda: search_d_tag(entry_string.get()),font=('Arial',12,'normal'))
label_title_1=Label(root,text="d Tag", font=("SF Pro",14,"bold"))

root.mainloop()

