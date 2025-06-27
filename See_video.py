#to do LabelFrame
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
root.title("Search Example")
root.geometry("1300x800")
db_pin=[{"h_video_1":21},{"v_video":22}, {"h_video":34235},{"v_video_1":34236}]
my_kind = { "h_video_1":21,"v_video":22,"h_video":34235,"v_video_1":34236 }
my_tag = list(my_kind.keys())
db=[]
db_note=[]
hash_list_notes=[]
relay_list=[]
public_list=[]
frame1=tk.Frame(root,height=100,width=200, background="darkgrey")

def on_server(event):
    label_r_lay.config(text="Relay: "+ str(len(relay_list)))
    call_r_lay()
    combo_list_lay["values"]=relay_list
    label_r_lay.config(text="Relay: "+ str(len(relay_list)))

relay_watch=[{"relays":10002}]
label_r_lay = tk.Label(frame1, text="Relay: ", font=('Arial',12,'bold'))
label_r_lay.grid(column=7, row=0,padx=20,pady=5,ipadx=1,ipady=1)
combo_list_lay = ttk.Combobox(frame1, values=relay_list,font=('Arial',12,'bold'))
combo_list_lay.grid(column=7, row=1,padx=20,pady=5,ipadx=2,ipady=1)
combo_list_lay.set("Relay List")
combo_list_lay.bind("<<ComboboxSelected>>", on_server) 

async def get_result_(client,relay_1):
    
    f = Filter().kind(Kind(10002)).reference(relay_1).limit(10)
   
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Search_r_lay(relay_1):
       init_logger(LogLevel.INFO)
       client = Client(None)
    
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

def pubkey_id(test):
   note_pubkey=[]
   for note_x in db_note:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   if len(note_pubkey)>1:       
    search_for_note(note_pubkey)
    show_noted()

def pubkey_id_ver(test):
   note_pubkey=[]
   for note_x in db_note:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   if len(note_pubkey)>1:       
    search_v_note(note_pubkey)
    layout()
  
def Open_source(value_kind):
     test=[]
     if __name__ == "__main__":
      test_kinds = [Kind(my_kind[value_kind])]  
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
    z = [event.as_json() for event in events.to_vec()]
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
       if event.verify_signature():
          z.append(event.as_json())
     if z!=[]:      
      return z
    except NostrSdkError as e:
       print (e)
    
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

def list_hashtag_fun():
    hashtag_list=[]
    if db_note!=[]:
        for note_x in db_note:
            if tags_string(note_x,"t")!=[]:
                for hash_y in tags_string(note_x,"t"):
                    if hash_y not in hashtag_list:
                        hashtag_list.append(hash_y)
        return hashtag_list      

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z    

def more_link(f):
   
   list=['mov','mp4']
   list1=["webm"]
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list:
        return "video"
   if f[-4:] in list1:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam" 

def url_image(x):
 if tags_string(x,"image")!=[]:
  z=tags_string(x,"image")[0]
  for j in z.split():
    if j[0:5]=="https":
        return str(j)

def codifica_link(x):
   f=url_image(x)
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

def photo_print(note):
  
  if codifica_link(note)=="pic":
   frame_pic=tk.Frame(root,height=20,width= 80)
   stringa_pic=StringVar()
   stringa_pic.set(url_image(note))
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
        frame_pic.place(relx=0.85,rely=0.01,relwidth=0.3,relheight=0.3,anchor="n")
       except TypeError as e: 
        print(e)  

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)

    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    
    if relay_list!=[]:
        for xrelay in relay_list:
            await client.add_relay(xrelay)
    else:
       relay_list.append("wss://nostr.mom/")
       relay_list.append("wss://nos.lol/")
       combo_list_lay["values"]=relay_list
     
    await client.connect()
    await asyncio.sleep(2.0)
    if isinstance(event_, list):
        test_kind = await get_kind(client, event_)
    else:
        print("errore")

    if test_kind==[] and public_list!=[]:
       test_kind = await get_kind_relay(client, event_)
       print("from relay")
    return test_kind

frame1.grid()

def search_for_kind(kind_int:int):
     Notes=db_note
     if Notes!=[]:
        hash_list_notes.clear()
        for note_x in Notes:
            if note_x["kind"]==kind_int:  
               hash_list_notes.append(note_x)
        return hash_list_notes     

def search_ver_kind(kind_int:int):
     Notes=db_note
     if Notes!=[]:
        vertical_note.clear()
        for note_x in Notes:
            if note_x["kind"]==kind_int:  
               vertical_note.append(note_x)
        return vertical_note  

def print_text():  
    """Widget function \n
    Dict: List of Events    \n
    open feed video        \n
    Search kind

    """
    frame3=tk.Frame(root,height=120,width= 250)
    canvas = tk.Canvas(frame3,width=240)
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
                
                var_id_test=StringVar()
                label_id_test = Entry(scrollable_frame,textvariable=var_id_test, width=35, background="grey",font=('Arial',10,'bold'))
                label_id_test.grid(pady=10,column=0,row=s+1, columnspan=3) 
                if list(test.keys())[0]=="h_video":
                   number_event=search_for_kind(test[list(test.keys())[0]]) 
            
                   if number_event:
                    var_id_test.set("Event kind 34235, number " + str(len(number_event))) 
                    show_noted()
                   else:
                      var_id_test.set("Event kind 34235 for horizontal video") 
                  
                if list(test.keys())[0]=="v_video":
                   number_event=search_ver_kind(test[list(test.keys())[0]])  
           
                   if number_event:
                    var_id_test.set("Event kind 22, number " +str(len(number_event)))
                    layout()
                   else:
                      var_id_test.set("Event kind 22 for vertical video")
                  
                if list(test.keys())[0]=="h_video_1":
                   number_event= search_for_kind(test[list(test.keys())[0]]) 
                
                   if number_event:
                    var_id_test.set("Event kind 21, number " + str(len(number_event)))
                    show_noted()
                   else:
                      var_id_test.set("Event kind 21 for horizontal video")                  
                     
                if list(test.keys())[0]=="v_video_1":
                   number_event=search_ver_kind(test[list(test.keys())[0]]) 
            
                   if number_event:
                    var_id_test.set("Event kind 34236, number " + str(len(number_event)))
                    layout()
                   else:
                      var_id_test.set("Event kind 34236 for vertical video")                  
                                 
            button=Button(scrollable_frame,text=f"{list(note.keys())[0]}", command=lambda val=note: print_var(val),font=('Arial',10,'bold'))
            button.grid(column=0,row=s,padx=10,pady=5)
            button_grid2=Button(scrollable_frame,text=f"Search kind", command=lambda val=note: Open_source(list(val.keys())[0]))
            button_grid2.grid(row=s,column=2,padx=5,pady=5)
            root.update()       
            s=s+1
   
    canvas.pack(side="left", fill="y", expand=True)
    scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.01,rely=0.12,relwidth=0.25,relheight=0.28)      

    def Close_print():
       frame3.destroy()  

    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)       

button4=tk.Button(root,text="List Event",command=print_text,font=('Arial',12,'bold'))
button4.grid(column=0,row=3,pady=30,padx=2)

def search_for_channel(note_hash):
     Notes=db_note
     if Notes:
        hash_list_notes.clear()
        for note_x in Notes:
            if note_hash in tags_string(note_x,"t"): 
               hash_list_notes.append(note_x)
        return hash_list_notes    

def search_ver_channel(note_hash):
     Notes=db_note
     if Notes:
        vertical_note.clear()
        for note_x in Notes:
            if note_hash in tags_string(note_x,"t"): 
               vertical_note.append(note_x)
        return vertical_note       

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

photo_Show=IntVar()

def check_photo():
   if photo_Show.get()==1:
      Label_photo.config(text="Download the photos and show on the card")
      Label_photo.place(relx=0.02,rely=0.64)  
   else:
      Label_photo.config(text="show one photo, when click on Read Tags \n on the card")   
      Label_photo.place(relx=0.02,rely=0.64)  

photo_show= Checkbutton(root, text = "Photo", variable = photo_Show,onvalue = 1, offvalue = 0, height = 2, font=('Arial',14,'bold'), command=check_photo)
photo_show.place(relx=0.05,rely=0.55)  
Label_photo=Label(root,font=('Arial',12,'normal'))
     
def show_noted():
  """Widget function \n
   Open feed Horizontal
   """
  frame2=tk.Frame(root)  
  if len(hash_list_notes)<=3:
     canvas_1 = tk.Canvas(frame2)
  else:   
    canvas_1 = tk.Canvas(frame2,width=900)
  scrollbar_1 = ttk.Scrollbar(frame2, orient=HORIZONTAL,command=canvas_1.xview)
  scrollable_frame_1 = tk.Frame(canvas_1,background="#E3E0DD")
  scrollbar_2 = ttk.Scrollbar(frame2, orient=VERTICAL,command=canvas_1.yview)
  scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all") ))

  canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
  canvas_1.configure(xscrollcommand=scrollbar_1.set,yscrollcommand=scrollbar_2.set)
  if hash_list_notes!=[]:
   
   s=1
   s1=0
   for note in hash_list_notes:
     if Alt_tag(note): 
      try:
       context0=""
       if note["tags"]!=[]:
        if tags_string(note,"title")!=[]:  
         for xnote in tags_string(note,"title"):
          if xnote!="" and xnote!=" ":
            context0=context0+"\n"+"Title "+str(xnote)
       if note['tags']!=[]:
        if note["content"]!="": 
         context1=" "+"\n"+note['content']+"\n"
        else:
           context1=""+"\n"
        context2=" "
        
        for xnote in tags_string(note,"alt"):
         context2=context2+"\n"+str(xnote) +"\n"
        
         
        if len(tags_string(note,"t"))==1:
         for xnote in tags_string(note,"t"):
          context2=context2+"Category "+str(xnote) +" "  
        else:
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context2=context2+"#"+str(xnote) +" "
            s=s+1
       else: 
        context1="\n"+note['content'][0:100]+"\n"
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       
       button_grid2=Button(scrollable_frame_1,text= "Author "+note['pubkey'][0:44], command=lambda val=note["pubkey"]: pubkey_id(val))
       button_grid2.grid(row=0,column=s1,padx=5,pady=5, columnspan=3)   
       if note["tags"]!=[]:
        if tags_string(note,"title")!=[]:
         if tags_string(note,"title")[0]!="":    
          label_id.grid(pady=1,padx=10,row=1,column=s1, columnspan=3)
      
       def print_photo_url(url):
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
              return url   
          
       url=video_thumb(note)
       if url!=None: 
          if photo_Show.get()==1:
           label_image = Label(scrollable_frame_1,text="",background="#E3E0DD")
           photo=print_photo_url(url)
           if photo!=None:
            label_image.grid(pady=2,row=2,column=s1, columnspan=3)
       
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=3)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=3) 
       
       def print_id(entry):
           print(entry['tags'])
           if photo_Show.get()==0:
            photo_list_2(entry)
                  
       def print_var(entry):
                print(entry["content"])
                if entry["kind"]>=30000:
                 share_naddr(entry)
                zap_stream_event(entry) 
                if tags_string(entry,"image")!=[]:
                 if tags_string(entry,"image")[0]!="":
                    photo_print(entry)
               
       button=Button(scrollable_frame_1,text=f"Print me!", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=4,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Read Tags", command=lambda val=note: print_id(val))
       button_grid2.grid(row=4,column=s1+1,padx=5,pady=5)    
       
       if tags_string(note,"imeta")!=[]:
        
        button_grid3=Button(scrollable_frame_1,text=f"See this video", command=lambda val=note: balance_video(val))
        button_grid3.grid(row=4,column=s1+2,padx=5,pady=5)  
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="bottom", fill="x",padx=20)
   scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
   canvas_1.pack( fill="y", expand=True)
   def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   if len(hash_list_notes)<=3:
       if photo_Show.get()==1:
         frame2.place(relx=0.3,rely=0.22,relwidth=0.32,relheight=0.58)
         button_frame.place(relx=0.45,rely=0.82,relwidth=0.1)      
       else:
          button_frame.place(relx=0.6,rely=0.55,relwidth=0.1)   
          frame2.place(relx=0.3,rely=0.32,relwidth=0.32,relheight=0.35)
   else:
        if photo_Show.get()==1:
            button_frame.place(relx=0.6,rely=0.82,relwidth=0.1)   
            frame2.place(relx=0.3,rely=0.22,relwidth=0.64,relheight=0.58)
        else:
            button_frame.place(relx=0.45,rely=0.66,relwidth=0.1)      
            frame2.place(relx=0.3,rely=0.32,relwidth=0.64,relheight=0.4)

button_read=Button(root,text="Stamp", command=show_noted,font=("Arial",12,"normal"))
entry_channel=StringVar()
hashtag_title=StringVar()
sats_ = IntVar() 
alt_string= IntVar()

def print_list_tag(): 
   """Widget function \n
      List of hashtag
   """
   if db_note!=[]:  
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3)
    scrollbar = ttk.Scrollbar(frame3, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)
    s=1     
    test1=list_hashtag_fun()
    if test1!=None and test1!=[]:
           
            def print_id(test):
                entry_channel.set(test)
                Channel_frame = ttk.LabelFrame(root, text="Associated tag", labelanchor="n", padding=10)
                Channel_frame.place(relx=0.55,rely=0.01,relheight=0.18,relwidth=0.4) 
                if db_note[0]["kind"]==22 or db_note[0]["kind"]==34236:
                 button_open=Button(root, command=layout, text="Open Tag",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
                else:
                 button_open=Button(root, command=show_noted, text="Open Tag",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
        
                Alt_tag= Checkbutton(root, text = "Alt Tag ", 
                    variable = alt_string,
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    font=('Arial',14,'bold'))
                Alt_tag.place(relx=0.83,rely=0.1)  
                search_ver_channel(test)
                search_for_channel(test)
                entry_space=tk.Entry(root, textvariable=entry_channel, width=30)
                entry_space.place(relx=0.57,rely=0.11,relwidth=0.12)
                Label_channel_name=tk.Label(root, text="Hashtag",font=("Arial",12,"bold"))
                Label_channel_name.place(relx=0.57,rely=0.06)
                button_open.place(relx=0.71,rely=0.09)

                def close_button():
                   entry_channel.set("")
                   entry_space.place_forget()
                   button_clo.place_forget()
                   Label_channel_name.place_forget()
                   button_open.place_forget()
                   Channel_frame.place_forget()
                   Alt_tag.place_forget()

                button_clo=Button(root,text="Close", command=close_button,font=('Arial',12,'bold'),foreground="red")
                button_clo.place(relx=0.84,rely=0.04)   
           
            ra=0
            se=1
            while ra<len(test1):
            
                button_grid1=Button(scrollable_frame,text=f"{test1[ra]} ", command=lambda val=test1[ra]: print_id(val))
                button_grid1.grid(row=1,column=s,padx=5,pady=5)
                
                if len(test1)>se:
                 button_grid2=Button(scrollable_frame,text=f"{test1[ra+1][0:10]}", command= lambda val=test1[ra+1]: print_id(val))
                 button_grid2.grid(row=2,column=s,padx=5,pady=5)
            
                root.update()  
                s=s+1
                se=se+2
                ra=ra+2   

    else:
         print("error") #It didn't find a channel

    if test1!=None and test1!=[]:
     scrollbar.pack(side="bottom", fill="x",padx=20)
     canvas.pack(side="left", fill="x", expand=True)
     frame3.place(relx=0.27,rely=0.01,relwidth=0.25,relheight=0.18)  

    def Close_print():
       frame3.destroy()  
       
    button_close_=tk.Button(scrollable_frame,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.grid(column=0,row=0,pady=5,padx=5)    
   else:
      print("error")
      
button_tag=tk.Button(root,text="# List",command=print_list_tag, font=('Arial',12,'bold'))
button_tag.place(relx=0.06,rely=0.45)

def layout():
   """Widget function \n
   Vertical feed 
   """
   if db_note!=[]: 
    frame1=Frame(root, width=400, height=100)
    canvas = Canvas(frame1)
    canvas.pack(side="left", fill=BOTH, expand=True)
    scrollbar = Scrollbar(frame1, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    scrollable_frame = Frame(canvas, background="#E3E0DD")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    list_note_lib=[]
    
    def print_id(entry):
           print(entry['tags'])
           if photo_Show.get()==0:
            photo_list_2(entry)
                  
    def print_var(entry):
                print(entry["content"])
                if entry["kind"]>=30000:
                 share_naddr(entry)
                zap_stream_event(entry) 
                if tags_string(entry,"image")!=[]:
                 if tags_string(entry,"image")[0]!="":   
                    photo_print(entry)
         
    def create_note(note_text, s):
            
        if note_text["content"] not in list_note_lib:
         list_note_lib.append(note_text["content"])
         button_grid2=Button(scrollable_frame,text= "Author "+note['pubkey'][0:44], command=lambda val=note["pubkey"]: pubkey_id_ver(val))
         button_grid2.grid(row=s,column=0,padx=5,pady=5, columnspan=3)  
         scroll_bar_mini = tk.Scrollbar(scrollable_frame)
         scroll_bar_mini.grid( sticky = NS,column=4,row=s+2,pady=5)

         def print_photo_url(url):
             response = requests.get(url, stream=True)
             if response.ok==True:
              with open('my_image.png', 'wb') as file:
                shutil.copyfileobj(response.raw, file)
              del response
              from PIL import Image
              image = Image.open('my_image.png')
              number=float(image.height/image.width)
              
              test1=int(float(number)*300)
              
              if test1>350:
               test1=int(350)
               if test1<250:
                pass
              image.thumbnail((300,test1))  
              photo = ImageTk.PhotoImage(image)
              label_image.config(image=photo)
              label_image.image_names= photo     
              return url   
            
         url=video_thumb(note_text)
         if url!=None: 
          if photo_Show.get()==1:
           label_image = Label(scrollable_frame,text="",width=300,background="#E3E0DD")
           photo=print_photo_url(url)
           if photo!=None:
            label_image.grid(pady=2,row=s+1,column=0, columnspan=3)
          
         second_label10 = tk.Text(scrollable_frame, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
         context2=""   
         if tags_string(note_text,"t")!=[]:
            for note_tags in tags_string(note_text,"t"):
               context2=context2+str("#")+note_tags+" "
         else:
            context2=""  
         second_label10.insert(END,note_text["content"]+"\n"+str(context2))
         scroll_bar_mini.config( command = second_label10.yview )
         if tags_string(note_text,"content-warning")==[]:
          second_label10.grid(padx=10, column=0, columnspan=3, row=s+2) 
         else:
           second_label10.delete("1.0", "end")
           second_label10.grid(padx=10, column=0, columnspan=3, row=s+2) 

           def content_show(): 
            if messagebox.askokcancel("Show this Note!"+" "+str(tags_string(note_text,"content-warning")[0]),"Yes/No") == True:     
             second_label10.insert(END,note_text["content"]+"\n"+str(context2))     
             content.grid_forget()

           content = Button(scrollable_frame, text="show",font=('Arial',12,'normal'), command=content_show)
           content.grid(row=s+2, column=0, columnspan=3, padx=5, pady=5)  
     
         button=Button(scrollable_frame,text=f"Print me!", command=lambda val=note: print_var(val))
         button.grid(column=0,row=s+3,padx=5,pady=5)
         button_grid2=Button(scrollable_frame,text=f"read tags", command=lambda val=note: print_id(val))
         button_grid2.grid(row=s+3,column=1,padx=5,pady=5)    
       
         if tags_string(note,"imeta")!=[]:
           button_grid3=Button(scrollable_frame,text=f"see Video", command=lambda val=note: balance_video(val))
           button_grid3.grid(row=s+3,column=2,padx=5,pady=5)      
    s=1       
    n=0
    if vertical_note!=[]:
     for note in vertical_note:
      n=n+1
      create_note(note, s)
      s += 4   
    frame1.place(relx=0.3,rely=0.3, relheight=0.4,relwidth=0.31)  

    def close_canvas():
        scrollable_frame.forget()
        canvas.destroy()
        frame1.destroy()
        button_close.place_forget()

    if list_note_lib==[]:
     close_canvas()    
    
    button_close=Button(root, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close.place(relx=0.4,rely=0.22)   

def share_naddr(note):
    coord = Coordinate(Kind(note["kind"]),PublicKey.parse(note["pubkey"]),str(tags_string(note,"d")[0]))
    coordinate = Nip19Coordinate(coord, [])
    print(f" Coordinate (encoded): {coordinate.to_bech32()}")
    print(f" https://njump.me/{coordinate.to_bech32()}")

from smart_open import open
import os


def stream_uri(uri_in, uri_out, chunk_size=1 << 18):  # 256kB chunks
    """Write from uri_in to uri_out with minimal memory footprint."""
    with open(uri_in, "rb") as fin, open(uri_out, "wb") as fout:
        while chunk := fin.read(chunk_size):
            fout.write(chunk)

def balance_video(nota):
  if tags_str(nota,"imeta")!=[]:
   for dim_photo in tags_str(nota,"imeta"):
     print(more_link(dim_photo[1][4:]))
     if more_link(dim_photo[1][4:])=="video": 
      for jdim in dim_photo:
       if jdim[0:4]=="size":
        list_number=dim_photo.index(jdim)   
        number=dim_photo[list_number][5:]
        if number:
         
         if int(number)<int(13000000):
          try: 
           response = requests.get(dim_photo[1][4:], stream=True)
           if response.ok==True: 
            stream_uri(dim_photo[1][4:], "my_video.mp4")
          
            if messagebox.askyesno("Form", "Do you want to see the video?"): 
            
             print('playing video using native player')
             os.system('my_video.mp4')
          except FileNotFoundError as e:
              print(e)   
          
         print(float(round(int(number)/(1024**2),3)), "Megabyte")

def zap_stream_event(note):
        if note["kind"]>=30000:
         coord = Coordinate(Kind(note["kind"]),PublicKey.parse(note["pubkey"]),str(tags_string(note,"d")[0]))
         coordinate = Nip19Coordinate(coord, [])
         #print(f" Coordinate (encoded): {coordinate.to_bech32()}")
         print(f" https://zap.stream/{coordinate.to_bech32()}")
        market=note["pubkey"]
        print(f" https://zap.stream/p/{PublicKey.parse(market).to_bech32()}")

def video_thumb(nota):
  if tags_str(nota,"imeta")!=[]:
   url=""
   for dim_photo in tags_str(nota,"imeta"):
     if more_link(dim_photo[1][4:])=="video": 
           
      for jdim in dim_photo:
       if jdim[0:5]=="image" or jdim[0:5]=="thumb":
        list_number=dim_photo.index(jdim) 
        url=  str(dim_photo[list_number][6:])
   if url!="":
    return url       

def photo_list_2(note):
 frame_pic=tk.Frame(root,height=80,width= 80) 
 url=video_thumb(note)
 if url!=None: 
   stringa_pic=StringVar()

   def print_photo():
     s=0  
     stringa_pic.set(url)
     label_pic = Entry(frame_pic, textvariable=stringa_pic)
     image_label_2 = tk.Label(frame_pic)
     image_label_2.grid(column=1,row=s, columnspan=2)
     if label_pic.get()!="":
         
       response = requests.get(label_pic.get(), stream=True)
       if response.ok==True: 
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        image.thumbnail((250,250))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        image_label_2.config(image=photo)
        image_label_2.image_names= photo
  
        def close_pic():
            image_label_2.config(image="")
            button_close.place_forget()
            label_pic.delete(0, END)
            frame_pic.destroy()

        s=s+3
        button_close=Button(frame_pic,command=close_pic,text="Close",font=("Arial",12,"bold"))
        button_close.grid(column=3,columnspan=1,row=s)
        s=s+2
   print_photo()     
   frame_pic.place(relx=0.65,rely=0.012,relwidth=0.3) 

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
       print(len(note_list),"\n",note_list[0])            
       return note_list    

vertical_note=[]

def search_for_note(note_found:list):
     if note_found!=[]:
        hash_list_notes.clear()
        for note_x in note_found:
            if note_x not in hash_list_notes: 
               hash_list_notes.append(note_x)
        return hash_list_notes    
     
def search_v_note(note_found:list):
     if note_found!=[]:
        vertical_note.clear()
        for note_x in note_found:
            if note_x not in vertical_note: 
               vertical_note.append(note_x)
        return vertical_note        

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

def search_word_title():
   if db_note!=[]:
      note_words=[]
      note_words_2=[]
      list_words={}
      for note_x in db_note:
        if tags_string(note_x,"title")!=[]:
         for title in tags_string(note_x,"title"):
            title_list=title.split(" ")
            title_list = [str(title).lower() for title in title_list]
         for string_x in title_list:
               if type(string_x)==str and len(string_x)>3:
               
                if string_x not in note_words:
                  
                  note_words.append(string_x)
                else:
                
                 note_words_2.append(string_x)
      for note_l_word in note_words_2:
         
           list_words[note_l_word]=note_words_2.count(note_l_word)+1
      
      threeview_dict_l(list_words)  
      return list_words           

def threeview_dict_l(list_words):
 if list_words!={} and  list_words!=NONE:
  treeview = ttk.Treeview(root, columns=("Value"),height=8)
  treeview.heading("#0", text="key")
  treeview.heading("Value", text="Value")
  db_list=[]
  for key,value in list_words.items():
      if value not in db_list:
       key_value = [key1 for key1, value1 in list_words.items() if value1 == value]

       level1 = treeview.insert("", tk.END, text=f"repeated words {value}")
       db_list.append(value)
       for key_one in key_value:
        treeview.insert(level1, tk.END,text=str(key_one),values=f"{value}")
  treeview.place(relx=0.6,rely=0.8,relheight=0.2)   
  
  def close_tree():
     treeview.place_forget()
     button_c2.place_forget()

  button_c2=Button(root,text="Close", command=close_tree,font=('Arial',12,'bold'))
  button_c2.place(relx=0.91,rely=0.82)
       
title_s=StringVar()
entry_t=tk.Entry(root, textvariable=title_s, width=20,font=('Arial',12,'normal'))
entry_t.place(relx=0.02,rely=0.8,relwidth=0.2)
button_s=Button(root,text="search", command=lambda: search_title_c(entry_t.get()),font=('Arial',12,'normal'))
button_s.place(relx=0.24,rely=0.79)
button_s2=Button(root,text="Search Words", command=search_word_title,font=('Arial',12,'bold'))
button_s2.place(relx=0.1,rely=0.9)
   
root.mainloop()