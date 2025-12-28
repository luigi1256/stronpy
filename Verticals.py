#Verticals
import asyncio
import tkinter as tk
from tkinter import *
from tkinter import ttk
from nostr_sdk import *
from datetime import timedelta 
import time
from tkinter import messagebox
import requests
import shutil
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import ast

root = Tk()
root.title("Search Example")
root.geometry("1300x800")
db_pin=[{"Video":22},{"Video A":34236}]
my_kind = { "Video":22,"Video A":34236 }
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
frame1.grid()

async def get_result_(client,relay_1):
    
    f = Filter().kind(Kind(10002)).reference(relay_1).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Search_r_lay(relay_1):
       init_logger(LogLevel.INFO)
       client = Client(None)
       relay_url = RelayUrl.parse(relay_1)
       await client.add_relay(relay_url)
      
       await client.connect()
       await asyncio.sleep(2.0)

       combined_results = await get_result_(client,relay_1)
       if combined_results:
        return combined_results

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
     asyncio.run(Search_status(client=Client(None),list_relay_connect=relay_list))         

def pubkey_id_ver(test):
   note_pubkey=[]
   for note_x in db_note:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   if len(note_pubkey)>1:       
    search_v_note(note_pubkey)
    layout()

def timeline_created(list_new):
  new_note=[] 
  global db_note
  if db_note!=[]:
   for new_x in list_new:
     if new_x not in db_note:
        new_note.append(new_x) 
   i=0
    
   while i<len(new_note):
     j=0
     while j< len(db_note): 
      if db_note[j]["created_at"]>(new_note[i]["created_at"]):
         j=j+1
      else:
         db_note.insert(j,new_note[i])
         break
     i=i+1
   return db_note   
  else:
        for list_x in list_new:
            db_note.append(list_x)
        return db_note  

def Open_source(value_kind):
     test=[]
     if __name__ == "__main__":
      test_kinds = [Kind(my_kind[value_kind])]  
      test = asyncio.run(Get_event_from(test_kinds))
      if test!=[]:
       note= get_note(test)
       timeline_created(note)
       search_for_kind(my_kind[value_kind])
               
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
       if event.verify_signature():
          z.append(event.as_json())
     if z!=[]:      
      return z
    except NostrSdkError as e:
       print (e)
    
def get_note(z):
   try: 
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f   
   except TypeError as e:
      print(e)
      return []

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
   list_video=['mov','mp4']
   list1=["webm"]
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_video:
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
   list_video=['mov','mp4']
   img=['png','jpg','JPG','gif']
   img1=['jpeg','webp'] 
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

async def Get_event_from(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    client = Client(None)

    # Add relays and connect
    relay_url_1 = RelayUrl.parse("wss://nos.lol/")
    await client.add_relay(relay_url_1)
    relay_url_x = RelayUrl.parse("wss://nostr.mom/")
    await client.add_relay(relay_url_x)
    
    if relay_list!=[]:
     for jrelay in relay_list:
       
       await client.add_relay(RelayUrl.parse(jrelay))
    else:
       relay_list.append("wss://nostr.mom/")
       relay_list.append("wss://nos.lol/")
       combo_list_lay["values"]=relay_list
       label_r_lay.config(text="Relay: "+ str(len(relay_list)))
     
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
            label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=340,font=('Arial',11,'normal'))
            var_id.set(note[list(note.keys())[0]]) 
            label_id.grid(pady=2,column=1,row=s)

            def print_var(test):
                
                var_id_test=StringVar()
                label_id_test = Entry(scrollable_frame,textvariable=var_id_test, width=35, background="grey",font=('Arial',10,'bold'))
                label_id_test.grid(pady=10,column=0,row=s+1, columnspan=3) 
                                            
                                                                                                  
                if list(test.keys())[0]=="Video":
                   number_event=search_ver_kind(test[list(test.keys())[0]])  
           
                   if number_event:
                    var_id_test.set("Event kind 22, number " +str(len(number_event)))
                    layout()
                   else:
                      var_id_test.set("Event kind 22 for vertical video")
                  
                                                                                                                                          
                if list(test.keys())[0]=="Video A":
                   number_event=search_ver_kind(test[list(test.keys())[0]]) 
            
                   if number_event:
                    var_id_test.set("Event kind 34236, number " + str(len(number_event)))
                    layout()
                   else:
                      var_id_test.set("Event kind 34236 for vertical video")                  
                                 
            button=Button(scrollable_frame,text=f"{list(note.keys())[0]}", command=lambda val=note: print_var(val),font=('Arial',10,'bold'))
            button.grid(column=0,row=s,padx=10,pady=5)
            button_grid2=Button(scrollable_frame,text=f"Search kind", command=lambda val=note: Open_source(list(val.keys())[0]), font=('Arial',10,'normal'))
            button_grid2.grid(row=s,column=2,padx=5,pady=5)
            root.update()       
            s=s+1
   
    canvas.pack(side="left", fill="y", expand=True)
    scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.01,rely=0.2,relwidth=0.25,relheight=0.15)      

    def Close_print():
       frame3.destroy()  

    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)       

button4=tk.Button(root,text="List Event",command=print_text,font=('Arial',12,'bold'))
button4.grid(column=0,row=3,pady=30,padx=2)

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

def check_photo():
   if photo_Show.get()==1:
      Label_photo.config(text="Download the photos and show on the card")
      Label_photo.place(relx=0.02,rely=0.6)  
   else:
      Label_photo.config(text="show photo, when click on Open Tags on the card")   
      Label_photo.place(relx=0.02,rely=0.6)  

photo_Show=IntVar()
photo_show= Checkbutton(root, text = "Photo", variable = photo_Show,onvalue = 1, offvalue = 0, height = 2, font=('Arial',14,'bold'), command=check_photo)
photo_show.place(relx=0.05,rely=0.55)  
Label_photo=Label(root,font=('Arial',12,'normal'))
entry_channel=StringVar()
hashtag_title=StringVar()
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
                button_open=Button(root, command=layout, text="Open Tag",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
                                        
                Alt_tag= Checkbutton(root, text = "Alt Tag ", 
                    variable = alt_string,
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    font=('Arial',14,'bold'))
                Alt_tag.place(relx=0.83,rely=0.1)  
                number_list=search_ver_channel(test)
                label_number=tk.Label(root,text=str(len(number_list)),font=("Arial",12,"bold"))
                entry_space=tk.Entry(root, textvariable=entry_channel, width=30)
                entry_space.place(relx=0.57,rely=0.11,relwidth=0.12)
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
button_tag.grid(column=1,row=3,pady=30,padx=5)

def layout():
    """Widget function \n
    Vertical feed 
    """
    
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
        
    def print_id(entry):
           print(entry['tags'])
           show_print_test_tag(entry)
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
            
         button_grid2=Button(scrollable_frame,text= "Author "+note_text['pubkey'][0:44], command=lambda val=note_text["pubkey"]: pubkey_id_ver(val))
         button_grid2.grid(row=s,column=0,padx=5,pady=5, columnspan=3)  
         scroll_bar_mini = tk.Scrollbar(scrollable_frame)
         scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)

         def print_photo_url(url):
            try:
             headers = {"User-Agent": "Mozilla/5.0"}
             response = requests.get(url,headers=headers, stream=True)
             response.raise_for_status()  
             if response.ok==TRUE:
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
            
            except TypeError as e: 
             print(e)  
            except requests.exceptions.RequestException as e:
             print(f"Error exceptions: {e}") 

         second_label10 = tk.Text(scrollable_frame, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")    
         url=video_thumb(note_text)
         if url!=None: 
          if photo_Show.get()==1:
           label_image = Label(scrollable_frame,text="",width=300,background="#E3E0DD")
           photo=print_photo_url(url)
           if photo!=None:
            label_image.grid(pady=2,row=s+2,column=0, columnspan=3)
                  
         context1=""
         context2=""  
         if tags_string(note_text,"title")!=[] and str(tags_string(note,"title")[0])!="":
            for note_t in tags_string(note_text,"title"):
               context1=context1+str("- Title: ")+note_t+"\n"
         else:
            if tags_string(note_text,"alt")!=[] and str(tags_string(note,"alt")[0])!="":
             context1=context1+str("- Alt: ")+str(tags_string(note,"alt")[0])+"\n"
             alt=plain_imeta(note,"alt")
             if alt:
                  context1=context1+"- "+str(alt)+"\n"
         if tags_string(note_text,"t")!=[]:
            for note_tags in tags_string(note_text,"t"):
               context2=context2+str("#")+note_tags+" "
         else:
            context2=""  
         second_label10.insert(END,context1+"\n"+str(context2))
         scroll_bar_mini.config( command = second_label10.yview )
         if tags_string(note_text,"content-warning")==[]:
          second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
         else:
           second_label10.delete("1.0", "end")
           second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 

           def content_show(): 
            if messagebox.askokcancel("Show this Note!"+" "+str(tags_string(note_text,"content-warning")[0]),"Yes/No") == True:     
             second_label10.insert(END,note_text["content"]+"\n"+str(context2))     
             content.grid_forget()

           content = Button(scrollable_frame, text="show",font=('Arial',12,'normal'), command=content_show)
           content.grid(row=s+1, column=0, columnspan=3, padx=5, pady=5)  
     
         button=Button(scrollable_frame,text=f"Print me ", command=lambda val=note: print_var(val))
         button.grid(column=0,row=s+3,padx=5,pady=5)
         button_grid2=Button(scrollable_frame,text=f"Open tags", command=lambda val=note: print_id(val))
         button_grid2.grid(row=s+3,column=1,padx=5,pady=5)    
       
         if tags_string(note,"imeta")!=[]:
           button_grid3=Button(scrollable_frame,text=f"See Video", command=lambda val=note: balance_video(val))
           button_grid3.grid(row=s+3,column=2,padx=5,pady=5)      
    s=1       
    n=0
    if vertical_note!=[]:
     for note in vertical_note:
      n=n+1
      create_note(note, s)
      s += 4   
    else:
       close_canvas()  
    frame1.place(relx=0.3,rely=0.3, relheight=0.4,relwidth=0.31)  

    def close_canvas():
        scrollable_frame.forget()
        canvas.destroy()
        frame1.destroy()
        button_close.place_forget()

    button_close=Button(root, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close.place(relx=0.4,rely=0.22)   

def share_naddr(note):
    coord = Coordinate(Kind(note["kind"]),PublicKey.parse(note["pubkey"]),str(tags_string(note,"d")[0]))
    coordinate = Nip19Coordinate(coord, [])
    print(f" Coordinate (encoded): {coordinate.to_bech32()}")
    print(f" https://njump.to/{coordinate.to_bech32()}")

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
        else:
           if note["kind"]==22:
              nevent=Nip19Event(EventId.parse(note["id"]),PublicKey.parse(note["pubkey"]),Kind(note["kind"]),[RelayUrl.parse(relay_list[0])]).to_bech32()
              print(f" https://zaptok.social/{nevent}")
              print(f"https://plebs.app/#/video/{str(note['id'])}")
        
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

def plain_imeta(nota,tag):
  if tags_str(nota,"imeta")!=[]:
   alt=""
   for dim_photo in tags_str(nota,"imeta"):
      if more_link(dim_photo[1][4:])=="video": 
         for jdim in dim_photo:
            if str(jdim).startswith(tag):
               alt=str(jdim)
   if alt!=str(tag)+" " and alt!="":
    return alt       

def photo_list_2(note):
   url=video_thumb(note)
   photo_view(url)

def photo_view(url):
 if url!=None: 
   frame_pic=tk.Frame(root,height=80,width= 80) 
   stringa_pic=StringVar()
   
   def print_photo():
     s=0  
     stringa_pic.set(url)
     label_pic = Entry(frame_pic, textvariable=stringa_pic)
     image_label_2 = tk.Label(frame_pic)
     image_label_2.grid(column=1,row=s, columnspan=2)
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
      except TypeError as e: 
        print(e)  
      except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")  
                     
   print_photo()     
   frame_pic.place(relx=0.72,rely=0.55,relwidth=0.3) 

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
        if plain_imeta(note_x,"alt"):
           alt_text=plain_imeta(note_x,"alt")[4:]
           title_alt=alt_text.split(" ") 
           title_list_1 = [str(title_x).lower() for title_x in title_alt]
           if string in title_list_1:
            if note_x not in note_list:
               note_list.append(note_x)         
      
      if note_list!=[]:
                   
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
       search_v_note(search_note)
       layout()
       return search_note     

def search_word_title():
     if db_note!=[]:
      note_words=[]
      note_words_2=[]
      list_words={}
      for note_x in db_note:
        if tags_string(note_x,"title")!=[] and tags_string(note_x,"title")[0]!="":
            title= tags_string(note_x,"title")[0]
            title_list=title.split(" ")
            title_list_r = [str(title).lower() for title in title_list]
            for string_x in title_list_r:
               if type(string_x)==str and len(string_x)>3:
               
                if string_x not in note_words:
                  
                  note_words.append(string_x)
                else:
                
                 note_words_2.append(string_x)
      for note_l_word in note_words_2:
         
           list_words[note_l_word]=note_words_2.count(note_l_word)+1
      
      threeview_dict_l(list_words)  
      
      return list_words           

def new_dict(list_words:dict):
   value=list(list_words.values())
   value.sort()
   temp_list = []
   for i in value:
    if i not in temp_list:
        temp_list.append(i)
   new_value = temp_list
   new_diz={}
   for value in new_value:
      for list_x in list(list_words.keys()):
         if list_words[list_x]==value:
            new_diz[list_x]=value
   return new_diz

all_words=[]

def threeview_dict_l(list_words):
 if list_words!={} and  list_words!=NONE:
  list_words=new_dict(list_words)
  global all_words
  all_words=list(list_words.keys())[0:100]
  print_people()
  treeview = ttk.Treeview(root, columns=("Value"),height=8)
  scrollbar_view = ttk.Scrollbar(root, orient=VERTICAL,command=treeview.yview)
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
  scrollbar_view.place(relx=0.88,rely=0.75,relheight=0.2)      
  treeview.place(relx=0.55,rely=0.75,relheight=0.2)   
  
  def close_tree():
     treeview.place_forget()
     scrollbar_view.place_forget()
     button_c2.place_forget()

  button_c2=Button(root,text="Close", command=close_tree,font=('Arial',12,'bold'))
  button_c2.place(relx=0.91,rely=0.82)

def print_people(): 
   if all_words!=[]:  
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=200)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas,border=2)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    s=1     
    
    test1=all_words
    dict_words={}
    for test_x in test1:
       if str(test_x)[0] in list(dict_words.keys()):
          list_in:list=dict_words[str(test_x)[0]]
          list_in.append(test_x)
          dict_words[str(test_x)[0]]=list_in
       else:
          list_in=[test_x]
          dict_words[str(test_x)[0]]=list_in
            
    ra=0
    sz=0
    test_2=list(dict_words.keys())
    labeL_button=Label(scrollable_frame,text="Number of Words "+str(len(test_2)))
    labeL_button.grid(row=0,column=1,padx=5,pady=5,columnspan=2)        
    test_2.sort()   
    while ra<len(test_2):
                 sz=sz+1           
                 label_button_grid1=Label(scrollable_frame,text=f"{test_2[ra]} ",font=("Arial",12,"normal"))
                 label_button_grid1.grid(row=s,column=1,padx=5,pady=5)
                 button_grid2=Button(scrollable_frame,text=f"Open", command= lambda val=test_2[ra]: open_letter(val))
                 button_grid2.grid(row=s,column=2,padx=5,pady=5)
                                              
                 root.update()  
              
                 s=s+1
                 ra=ra+1   
    canvas.pack(side="left", fill="y", expand=True)

    def open_letter(key):
 
       ra=0
       
       test_1=dict_words[key]
       test_text2=""
       while ra<len(test_1):
            if ra<5:  
                test_text2=test_text2+ str(test_1[ra]) +"   "
                ra=ra+1        
            else:
               ra=len(test_1)                   
       test_text.set(test_text2)
       label_button_2.place(relx=0.02,rely=0.75)
              
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.325,rely=0.75,relwidth=0.2, relheight=0.22)      

    def Close_print():
       frame3.destroy()  
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

test_text=StringVar()
label_button_2=Label(root,textvariable=test_text,font=("Arial",12,"normal"))
title_s=StringVar()
entry_t=tk.Entry(root, textvariable=title_s, width=15,font=('Arial',12,'normal'), background="grey")
entry_t.place(relx=0.02,rely=0.8,relwidth=0.15, relheight=0.04)
button_s=Button(root,text="Search", command=lambda: search_title_c(entry_t.get()),font=('Arial',12,'normal'),background="grey")
button_s.place(relx=0.18,rely=0.8)
button_s2=Button(root,text="Search Words", command=search_word_title,font=('Arial',12,'bold'))
button_s2.place(relx=0.07,rely=0.87)

list_p=[]
outbox_list=[]

def show_print_test_tag(note):
   
   frame3=tk.Frame(root)  
   canvas_2 = tk.Canvas(frame3,width=420)
   scrollbar_2 = ttk.Scrollbar(frame3, orient="vertical", command=canvas_2.yview)
   scrollable_frame_2 = Frame(canvas_2,background="#E3E0DD")

   scrollable_frame_2.bind(
         "<Configure>",
            lambda e: canvas_2.configure(
            scrollregion=canvas_2.bbox("all")
    )
)

   canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor="nw")
   canvas_2.configure(yscrollcommand=scrollbar_2.set)
   s=1
   context0="Pubkey: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"+"- Time "+str(note["created_at"]) +"\n"
   if note['tags']!=[]:
        context1=""
        if tags_string(note,"d")!=[]:
         context1=context1+"- d Tag "+str(tags_string(note,"d")[0][0:10])+"\n"
        if tags_string(note,"alt")!=[] and str(tags_string(note,"alt")[0])!="":
         context1=context1+"- Alt "+str(tags_string(note,"alt")[0])+"\n"
         alt=plain_imeta(note,"alt")
         if alt:
            context1=context1+"- "+str(alt)+"\n"
        if tags_string(note,"client")!=[]:
         context1=context1+"- Client "+str(tags_string(note,"client")[0])+"\n" 
        if tags_string(note,"published_at")!=[]:
         context1=context1+"- Time first event "+str(tags_string(note,"published_at")[0])+"\n"  
        context2=""
        context2=context2+"- Tags number: "+str(len(note["tags"])) +"\n"
   else: 
        context1=""
        context2=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   
   var_id.set(context0+context1+context2)
   s=0
   label_id.grid(pady=2,column=0, row=s,columnspan=3,rowspan=4)
   
   def print_next(entry):
       
        value=db_note.index(entry)
        
        close_frame()
        if value+1<len(db_note):
            show_print_test_tag(db_note[value+1])

   def print_down(entry):
    
     value=db_note.index(entry)
     
     close_frame()
     if value-1>=0:
         show_print_test_tag(db_note[value-1])         
                                         
   def send_var(entry):
      e_string_var.set(entry["id"])   

   def print_content(entry):
    result=show_note_from_id(entry)
    if result!=[]: 
     z=6
     
     for jresult in result[::-1]:
       if jresult["id"]!=entry["id"]:
         var_id_r=StringVar()
         label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
         label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
         str_time_1=note_time_reply(entry,jresult)
         var_id_r.set(" Pubkey: "+jresult["pubkey"][0:30]+"\n" +"Time: "+str(str_time_1) +"\n" +"Comment")
         scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
         second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
         context22="\n"+ " Important tags: "+"\n"   
         if tags_string(jresult,"E")!=[]:
          if four_tags(jresult,"E"):
            for f_note in four_tags(jresult,"E"):
              context22=context22+str(" < "+ f_note[0]+" > ")+f_note[1][0:9]+ "\n"
              if f_note[2]!="" and f_note not in relay_list:
                      relay_list.append(f_note[2])
         else:
            context22=" < E > Probably some errors \n"              
         if tags_string(jresult,"e")!=[]:
          if four_tags(jresult,"e"):
            for F_note in four_tags(jresult,"e"):
                 context22=context22+str(" < "+ F_note[0]+" > ")+F_note[1][0:9]+ "\n"
                 if F_note[2]!="" and F_note not in relay_list:
                    relay_list.append(F_note[2])
         if tags_string(jresult,"P")!=[]:
            
            for pr in tags_string(jresult,"P"):
            
              context22=context22+str(" Author Thread: ")+pr[0:9]+ "\n"
         if tags_string(jresult,"p")!=[]:             
            for Pr in tags_string(jresult,"p"):
               context22=context22+str("Cited in the reply ")+Pr[0:9]+ "\n"  

         scroll_bar_mini_r.config( command = second_label10_r.yview )       
         if jresult["kind"]==7: 
            var_id_r.set(" Pubkey: "+jresult["pubkey"][0:32]+"\n" +"Time: "+str(str_time_1)+"\n"+"Like "+jresult["content"]+"\n")
            
         else:
            second_label10_r.insert(END,jresult["content"]+"\n"+str(context22))  
            second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
            scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)  
            button_grid4=Button(scrollable_frame_2,text=f"Comment ", command=lambda val=jresult: reply_to(val))
            button_grid4.grid(row=z+2,column=2,padx=5,pady=5)        
            if photo_Show.get()==0:
               button_photo=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=jresult: photo_list_2(val))
               button_photo.grid(column=1,row=z+2,padx=5,pady=5)
         button_print=Button(scrollable_frame_2,text=f"Print ", command=lambda val=jresult: print(val))
         button_print.grid(column=0,row=z+2,padx=5,pady=5)
         
         
       z=z+3     

   def reply_to(entry):
    if entry["kind"]==1111:
     list_p.clear()
     list_p.append(PublicKey.parse(entry["pubkey"]))
     Get_outbox_relay(10002,list_p)
     if tags_string(entry,"E")!=[]:
      var_entry_first.set(tags_string(entry,"E")[0])
      add_note_idto_comment() 
      var_entry_second.set(entry["id"])
      add_reply_idto_comment()
    else:
     if entry["kind"]==22:
         list_p.clear()
         list_p.append(PublicKey.parse(entry["pubkey"]))
         Get_outbox_relay(10002,list_p)
         var_entry_first.set(entry["id"])
         var_entry_second.set("")
         add_note_idto_comment()   

   def reply_root(entry):
     if entry["kind"]==22:
      list_p.clear()
      list_p.append(PublicKey.parse(entry["pubkey"]))
      Get_outbox_relay(10002,list_p)
      var_entry_first.set(entry["id"])
      var_entry_second.set("")       
      add_note_idto_comment()
           
   button_grid_2=Button(scrollable_frame_2,text="Read", command=lambda val=note: print_content(val),width=10, height=3)
   button_grid_2.grid(row=s+1,column=4,padx=5,pady=5)    
   button_grid_3=Button(scrollable_frame_2,text="Bookmarks", command=lambda val=note: send_var(val),width=10, height=3)
   button_grid_3.grid(row=s+2,column=4,padx=5,pady=5)
   button_grid_4=Button(scrollable_frame_2,text="Reply", command=lambda val=note: reply_root(val),width=10, height=3)
   button_grid_4.grid(row=s+3,column=4,padx=5,pady=5)        
   def print_tags(entry):
        
                list_one,list_two=tags_first(entry)
                var_id_2=StringVar()
                var_id_3=StringVar()
                label_id_2= Message(scrollable_frame_2,textvariable=var_id_2, relief=RAISED,width=220,font=("Arial",12,"normal"))
                s=6
                
                def val_tag(val):
                    s=6
                    list_z,par=tags_parameters(list_one,list_two,val)
                    var_id_2.set(str(list_z))
                    var_id_3.set(par)
                    value=list_one.index(par)
                    label_id_2.grid(pady=2,column=1,row=s+value, columnspan=2)  
                button_list=[]
                if list_one:
         
                 z=0
         
                 while z<len(list_one):
          
                    button_grid2=Button(scrollable_frame_2,text=str(list_one[z]), command=lambda val=list_one[z]: val_tag(val))
                    button_grid2.grid(row=s,column=0,padx=5,pady=5) 
                    button_list.append(button_grid2)   
                    z=z+1
                    s=s+1 
                 button_stamp=Button(scrollable_frame_2,text="stamp", command=lambda val=(var_id_2),val2=(var_id_3): stamp_var(val,val2))
                 button_stamp.grid(column=0,row=s+1,padx=5,pady=5)
                 def close_Tags():
                    button_stamp.grid_forget()
                     
                    for button2 in  button_list:
                     button2.grid_forget()                    
                    
                    button_c_tags.grid_forget()
                    label_id_2.grid_forget()
                    
                 button_c_tags=Button(scrollable_frame_2,command=close_Tags,text="Tags ❌",font=("Arial",12,"normal"))
                 button_c_tags.grid()   
          
                if 'mention' in tags_str_long(entry,"e"):
                    print("e "+tags_str_long(entry,"e"))
                if 'mention' in tags_str_long(entry,"a"):   
                     print("a "+tags_str_long(entry,"a"))
   def stamp_var(entry,obj):
      
      if  obj.get()=="imeta":
         imeta_tag(entry.get(),obj.get())
      else:   
            print(obj.get())   
            print(entry.get())                                  
                                           
   s=5        
   button=Button(scrollable_frame_2,text=f"Tags ", command=lambda val=note: print_tags(val),font=("Arial",12,"normal"))
   button.grid(column=0,row=s,padx=5,pady=5)
           
      
   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply ", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s,column=2,padx=5,pady=5)    
   else:
    if tags_string(note,"imeta")!=[]:
     button_grid3=Button(scrollable_frame_2,text=f"See video ",command=lambda val=note: balance_video(val),font=("Arial",12,"normal"))  
     button_grid3.grid(row=s,column=2,padx=5,pady=5)        
   button_grid4=Button(scrollable_frame_2,text="⬇️",command=lambda val=note: print_next(val),font=("Arial",14,"normal"))  
   button_grid4.grid(row=s,column=1,padx=5,pady=5)
   button_grid4=Button(scrollable_frame_2,text="⬆️",command=lambda val=note: print_down(val),font=("Arial",14,"normal")) 
   button_grid4.grid(row=s-1,column=1,padx=5,pady=5)                
   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()    
   button_frame=Button(frame3,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.7,rely=0.9)   
   frame3.place(relx=0.3,rely=0.3,relheight=0.55,relwidth=0.38) 

def tags_first(x):
   tags_list=[]
   tags_value=[]
   if x["tags"]!=[]:
      for jtags in x["tags"]:
         if jtags[0] not in tags_list:
            tags_list.append(jtags[0])
   if tags_list!=[]:
       for xtags in tags_list:
         for ztags in tags_str(x,xtags):
            tags_value.append(ztags)
   return tags_list,tags_value 

def tags_parameters(key,value,s):
    list_q=[]
    if s in key:
        for xvalue in value:
          if xvalue[0]==s:
              list_q.append(xvalue[1:])
    return list_q,s   

def tags_str_long(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
       if len(j)>2:
         z.append(j[1:]) 
       else:    
          z.append(j[1])
    return z         

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

def share(note_text):
    print(f"Note: \n {note_text}")

def reply_note():
  if entry4.get()!="" and entry_note.get()!="": 
    if __name__ == '__main__':
     note=entry4.get()
     tag=reply_note_comment()

     if tag!=None:
      asyncio.run(reply(note,tag))
      
  close_answer()

def reply_note_comment():   
  if entry_note.get()!="":
    event=entry_note.get()
    search_id=evnt_id(event)
    found_nota=asyncio.run(Get_id(search_id))
    if found_nota!=[]:
     return found_nota[0]

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

button_reply_c=tk.Button(root,text="send comment", background="darkgrey", command=second_reply, font=('Arial',12,'normal'))

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

def test_open():
   if root_thread_list!=[]:
    note_tag1['text']="id " +root_thread_list[0][0:9]
    entry_note.insert(1, root_thread_list[0])
    Reply_frame.place(relx=0.5,rely=0.65,relwidth=0.3,relheight=0.33,anchor='n' )
    note_tag.place(relx=0.4,rely=0.7,anchor='n' )
    entry4.place(relx=0.5,rely=0.75,relwidth=0.25,relheight=0.1,anchor='n' )
    #entry_layout-right
    enter_note.place(relx=0.4,rely=0.95,relwidth=0.1 )
    entry_note.place(relx=0.5,rely=0.95,relwidth=0.1)
    note_tag1.place(relx=0.45,rely=0.7,anchor='n' )
    
    close_["command"] = close_answer
    close_.place(relx=0.6,rely=0.68,anchor='n' )
    
    def Preview():
     if entry4.get()!="":
        frame1=Frame(root, width=310, height=100)
        canvas = Canvas(frame1)
        canvas.pack(side="left", fill=BOTH, expand=True)
        
        canvas.bind(
          "<Configure>",
          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

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
        frame1.place(relx=0.72,rely=0.65, relheight=0.35,relwidth=0.2)  
        def close_canvas():
            frame1.destroy()

        button_close=Button(scrollable_frame, command=close_canvas, text="Close X")
        button_close.grid(column=1,row=0, padx=10,pady=10)    
      
    button_pre["command"]= Preview
    button_pre.place(relx=0.45,rely=0.88,relwidth=0.1, anchor="n") 
    button_reply.place(relx=0.55,rely=0.88,relwidth=0.1,relheight=0.05,anchor='n' )
        

def third_open():
   if root_thread_list!=[] and first_reply!=[]: 
    note_c_tag1['text']="id " +first_reply[0][0:9]
    entry_c_note.insert(1, first_reply[0])
    entry_c_root.insert(1, root_thread_list[0])
    comment_frame.place(relx=0.4,rely=0.65,relwidth=0.3,relheight=0.33,anchor='n' )
    note_c_tag.place(relx=0.44,rely=0.69,relwidth=0.1,anchor='n' )
    entry_c_4.place(relx=0.4,rely=0.75,relwidth=0.25,relheight=0.1,anchor='n' )
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

        canvas.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

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
        
Reply_frame = ttk.LabelFrame(root, text="Reply Post", labelanchor="n", padding=10)
button_reply=tk.Button(root,text="send reply", background="darkgrey", command=reply_note, font=('Arial',12,'normal'))
preview_frame = ttk.LabelFrame(root, text="Preview Post", labelanchor="n", padding=10)
note_tag = tk.Label(root, text="Note",font=('Arial',12,'normal'))
entry4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
enter_note = tk.Label(root, text="Root Note")
entry_note=ttk.Entry(root,justify='left')
var_entry_first=StringVar()
var_entry_second=StringVar()
entry_first_note=ttk.Entry(root,justify='left',textvariable=var_entry_first)
entry_first_note.place(relx=0.04,rely=0.65)
button_create=Button(root,text="Reply Root", command=test_open,font=('Arial',10,'normal'))
button_create.place(relx=0.15,rely=0.64)
entry_second_note=ttk.Entry(root,justify='left',textvariable=var_entry_second)
entry_second_note.place(relx=0.04,rely=0.7)
button_create=Button(root,text="Re Comment", command=third_open,font=('Arial',10,'normal'))
button_create.place(relx=0.15,rely=0.69)
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
root_thread_list=[]
first_reply=[]
other_reply=[]

def evnt_id(id):
    try: 
     test2=EventId.parse(id)
     return test2
    except NostrSdkError as e:
       print(e,"input ",id)

def add_note_idto_comment():
    if entry_first_note.get()!="" and evnt_id(entry_first_note.get())!=None:
       if root_thread_list==[]:
        root_thread_list.append(entry_first_note.get())
       else:
         root_thread_list.clear()
         root_thread_list.append(entry_first_note.get())  
       print(root_thread_list)

async def get_more_Event(client, event_list):
    f = Filter().ids(event_list)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_one_note(client, e_id):
    f = Filter().event(EventId.parse(e_id)).kinds([Kind(1111),Kind(7)]).limit(100)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10)) 
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    SubscribeAutoCloseOptions()
    return z

async def get_one_Event(client, event_):
    f = Filter().id(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
      
       for jrelay in relay_list:
          await client.add_relay(RelayUrl.parse(jrelay))
    else:
     await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
     await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
     await client.add_relay(RelayUrl.parse("wss://relay.primal.net/"))
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        test_kind = await get_more_Event(client, event_)
    else:
        if isinstance(event_, str):
           print(type(event_))
           test_kind = await get_one_note(client, event_)
        else:
           print(type(event_))
           test_kind = await get_one_Event(client, event_)
        
        
    return test_kind

async def reply(note,tag):
    # Init logger
    init_logger(LogLevel.INFO)
    
    key_string=log_these_key()
    if key_string!=None: 
     keys = Keys.parse(key_string)
     signer=NostrSigner.keys(keys)
     client = Client(signer)
     if outbox_list!=[]:
   
      for jrelay in outbox_list:
        relay_url_list=RelayUrl.parse(jrelay)
        await client.add_relay(relay_url_list)
     else:
      await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
      await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
     await client.connect()
     event_to_comment:dict=tag
     if event_to_comment!=NONE:
      if Event.from_json(f"{event_to_comment}").kind().as_u16()!=(1111):    
       print(Event.from_json(f"{event_to_comment}").kind().as_u16()) 
       if outbox_list!=[]:
        builder =EventBuilder.comment(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_comment}"),RelayUrl.parse(outbox_list[0]))
       else:
          builder =EventBuilder.comment(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_comment}"),None)
       test = await client.send_event_builder(builder)
     
       if first_reply==[]:
        pass
       else:
          first_reply.clear()

       print("Event sent:")
         
       f = Filter().authors([keys.public_key()]).limit(10)
       events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
       for event in events.to_vec():
        print(event.as_json())

async def the_second_reply(note,tag, root):
    # Init logger
    init_logger(LogLevel.INFO)
    
    key_string=log_these_key()
    if key_string!=None: 
     keys = Keys.parse(key_string)
     signer = NostrSigner.keys(keys)
     client = Client(signer)
     if outbox_list!=[]:
   
      for jrelay in outbox_list:
       relay_url_list=RelayUrl.parse(jrelay)
       await client.add_relay(relay_url_list)
       
     else:
        await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
        await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
     await client.connect()
     event_to_comment:dict=tag
     event_to_start:dict=root
     if event_to_comment!=NONE and event_to_start!=None:
     
      if Event.from_json(f"{event_to_comment}").kind().as_u16()==1111:
       if Event.from_json(f"{event_to_start}").kind().as_u16()!= (1,1111):
        if outbox_list!=[]:
          builder =EventBuilder.comment(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_start}"),RelayUrl.parse(outbox_list[0]))
        else:
           builder =EventBuilder.comment(note,Event.from_json(f"{event_to_comment}"),Event.from_json(f"{event_to_start}"),None)
    
        test= await client.send_event_builder(builder)

     if other_reply==[]:
      other_reply.append(test.id.to_hex())
     else:
      
      other_reply.append(test.id.to_hex())
                                        
     await asyncio.sleep(2.0)

    # Get events from relays
     print("Getting events from relays...")
     f = Filter().authors([keys.public_key()]).kinds([Kind(11),Kind(1111),Kind(25)])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     for event in events.to_vec():
      print(event.as_json())

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

#bookmarks


db_list_note=[]

def convert_user(x:str):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def call_text():
  """Relay list \n 
  Search Bookmark"""
  if relay_list!=[]:
   if __name__ == "__main__":
    response=asyncio.run(Search_d_tag())
    if response:

     note_=get_note(response)
     for jnote in note_:
       if jnote not in db_list_note:
          db_list_note.append(jnote)
       if jnote["tags"]!=[]:
          second_label_g.insert(END,"- Kind "+str(jnote["kind"])+"\n"+str(jnote["tags"]))
       else:
             second_label_g.insert(END,str(" no tags"))
       second_label_g.insert(END,"\n"+"____________________"+"\n")
       second_label_g.insert(END,"\n"+"\n")

    else:
       print("empty")
  else: 
              
          if __name__ == "__main__":
            response=asyncio.run(Search_d_tag())
            if len(relay_list)>0:
             button_close_search["text"]="Search 🔍"
             scroll_bar_mini_g.place(relx=0.65,rely=0.01,relheight=0.15)
             second_label_g.place(relx=0.4,rely=0.01)
             button_close_text.place(relx=0.5,rely=0.18) 
            else:
             if response!=None:
                print(str(len(response)),"\n",response[0]) 

def close_text():
   scroll_bar_mini_g.place_forget()
   second_label_g.place_forget()
   button_close_text.place_forget()

button_close_text=tk.Button(root, text='Close x',font=('Arial',12,'bold'), command=close_text)  
button_close_search=tk.Button(root, text='Search Relay',font=('Arial',12,'bold'), command=call_text)  
button_close_search.place(relx=0.05,rely=0.45) 
p_tag = tk.Label(root, text="Pubkey",font=("Arial",12,"bold"))
entryp_tag=ttk.Entry(root,justify='left',font=("Arial",12,"normal"))
p_tag.place(relx=0.05,rely=0.37,relwidth=0.1 )
entryp_tag.place(relx=0.05,rely=0.4,relwidth=0.1 )
p_view = tk.Label(root, text="", font=("Arial",12,"normal"))
p_view.place(relx=0.15,rely=0.36,relwidth=0.1 )
npub_bookmark=[]
scroll_bar_mini_g = tk.Scrollbar(root)
second_label_g = tk.Text(root, padx=10, height=5, width=25, yscrollcommand = scroll_bar_mini_g.set, font=('Arial',14,'bold'))
scroll_bar_mini_g.config( command = second_label_g.yview )

def p_show():
    title=entryp_tag.get()
    
    if len(title)==64 or len(title)==63:
        if len(title)==63:
           title=PublicKey.parse(title).to_hex()
       
        if convert_user(title)!=None:
         if title not in npub_bookmark:
          
            if len(npub_bookmark)>=1:
                i=1
                while len(npub_bookmark)>i:
                 npub_bookmark.pop(1)
                p_view.config(text=str(len(npub_bookmark)))
                entryp_tag.delete(0, END)  
            else:  
                npub_bookmark.append(convert_user(title))
                p_view.config(text=str(len(npub_bookmark)))
                entryp_tag.delete(0, END) 
                return npub_bookmark
        
         else:
              p_view.config(text=str(len(npub_bookmark)))
              entryp_tag.delete(0, END) 
              return npub_bookmark
        else:
         p_view.config(text=str(len(npub_bookmark)))
         entryp_tag.delete(0, END) 
    else:
       entryp_tag.delete(0, END) 
       if len(npub_bookmark)>0:
        p_view.config(text=str(len(npub_bookmark)))

def Clear_pubkey():
   npub_bookmark.clear()
   p_view.config(text="")

p_button = tk.Button(root, text="add Pubkey", font=("Arial",12,"bold"), command=p_show)
p_button.place(relx=0.16,rely=0.39)
p_clear_button = tk.Button(root, text="x", font=("Arial",12,"bold"), command=Clear_pubkey)
p_clear_button.place(relx=0.25,rely=0.39)

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
        context1="kind "+str(note["kind"])+"\n"
        context2="\n"
        xnote=""
        if tags_string(note,"e")!=[]:
         for y_note in tags_string(note,"e"): 
          xnote= "e: "+ y_note +"\n"
         context2=context2+str(xnote) +"\n"
        else: 
         context1="the bookmark is empty"
         context2=""
        if tags_string(note,"client")!=[]: 
         znote= "Client: "+str(tags_string(note,"client")[0])
         context2=context2+str(znote) +"\n" 
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
       
      button=Button(scrollable_frame_1,text=f"Content ", command=lambda val=note: print_var(val))
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
    frame2.place(relx=0.28,rely=0.3,relwidth=0.35,relheight=0.4)
    
    def close_number() -> None :
        frame2.destroy()    
        #button_frame.place_forget()
        button_f_close.place_forget()
        
    button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"))
    button_f_close.place(relx=0.6,rely=0.24)      
  else:
     if npub_bookmark!=[]:
      if messagebox.askokcancel("New Bookmark","Do you want create a new bookmark?") == True:
        raw_label()

 s=1
 create_page(db_list_note, s)
 root.update_idletasks()

def show_edit_test(note):
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
   e_button.place(relx=0.82,rely=0.1)
   e_view.place(relx=0.7,rely=0.19)
   e_tag.place(relx=0.7,rely=0.1 )
   e_tag_entry.place(relx=0.68,rely=0.15,relwidth=0.2)
   context0="npub: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
   context1="content: "+"\n"+note['content']+"\n"
   context2=""
   if note['tags']!=[]:
        e_tag_id=""
        if tags_string(note,"e")!=[]:
            for e_tag_id in tags_string(note,"e"):
             context1 = "e "+ e_tag_id +"\n"        
            
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   var_id.set(context0+context1+context2)
   label_id.grid(pady=2,column=0, columnspan=3)
      
   def print_edit(entry):
           if button_grid2.cget('foreground')=="green":  
            list_e=edit_note(entry)
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
              
               test=asyncio.run(edit_can_book(bookmark_e,entry["pubkey"]))
               if test:
                button_grid2.config(fg="grey")
                close_frame()
               else:
                  print("error") 
                  button_grid2.config(fg="grey")
                  close_frame()

   def print_var(entry):
            print(edit_note(entry))
            button_grid2.config(fg="green")

   button=Button(scrollable_frame_2,text=f"Edit test ", command=lambda val=note: print_var(val))
   button.grid(row=s,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Send event", command=lambda val=note: print_edit(val))
   button_grid2.grid(row=s,column=1,padx=5,pady=5)
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
   
   def show_video(entry):
      if tags_string(entry,"e")!=[]:
       try:   
         e_id_vn=[]
         video_l=[]
         e_id=[]
         for ev in tags_string(entry,"e"):
          e_id.append(ev)
         if db_note!=[]:
          for note_x in db_note:
             
             if note_x["id"] in e_id:
                if note_x not in video_l: 
                  video_l.append(note_x)
                e_id.remove(note_x["id"])
            
            
         if e_id!=[]:
          for e_x in e_id:
               e_id_vn.append(EventId.parse(e_x))
              
                  
          if __name__ == '__main__':       
           result= get_note(asyncio.run(Get_id(e_id_vn)))
           if result!=[]:
            for res in result:
             if res not in video_l:
                video_l.append(res)
         if video_l!=[]:
            search_v_note(video_l)
            layout()
         else:
            print("Error")   
       except ValueError as e:
         print(e)    

   button=Button(scrollable_frame_2,text=f"id ", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Pubkey", command=lambda val=note: print_zap(val))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
   button_grid3=Button(scrollable_frame_2,text="Video", command=lambda val=note: show_video(val))
   button_grid3.grid(row=s+2,column=2,padx=5,pady=5)
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()  
     button_frame.place_forget()

   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.9,rely=0.16)
   frame3.place(relx=0.69,rely=0.22,relwidth=0.31,relheight=0.4 ) 

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.72,rely=0.12,relheight=0.22,relwidth=0.2)  
        e_button.place(relx=0.75,rely=0.25)
        e_view.place(relx=0.85,rely=0.25 )
        e_tag.place(relx=0.75,rely=0.16)
        e_tag_entry.place(relx=0.75,rely=0.2,relwidth=0.15)
        button_send.place(relx=0.82,rely=0.5,relwidth=0.2,relheight=0.1,anchor='n' )
        button_entry1.place(relx=0.94,rely=0.5,relwidth=0.05, relheight=0.1,anchor="n" )
        error_label.place(relx=0.7,rely=0.01)
        print_label.place(relx=0.7,rely=0.06)
        button_frame_label.place(relx=0.9,rely=0.06)
                                                                    
   else:
      Check_raw.set(0)
      button_frame_label.place_forget()
      error_label.place_forget()
      print_label.place_forget()
      button_send.place_forget()
      button_entry1.place_forget()
      stuff_frame.place_forget() 
      e_tag.place_forget()
      e_tag_entry.place_forget()
      e_button.place_forget()
      e_view.place_forget()

button_frame_label=Button(root,command=raw_label,text="Close ❌",font=("Arial",12,"normal"))

def e_show():
    title_e=e_tag_entry.get()
    title=event_string_note(title_e)
    if title!=None:
     if len(title)==64:
       
        if evnt_id(title)!=None:
         if title not in list_e:
          list_e.append(title)
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

stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)
e_tag = tk.Label(root, text="e-Tag",font=("Arial",12,"bold"))
e_string_var=StringVar()
button_id=tk.Button(root,command=show_Teed,text="Go Result",font=('Arial',12,'bold'))
button_id.place(relx=0.16,rely=0.45)
e_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12),textvariable=e_string_var)
e_button = tk.Button(root, text="Add Event", font=("Arial",12,"bold"), command=e_show)
e_view = tk.Label(root, text="e tag?: ", font=("Arial",12))
Check_raw =IntVar()
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

def create_bookmark():
   check_square()
   lists_id=[] 
   if button_entry1.cget('foreground')=="green":
    if list_e!=[]:
                        
            lists_id=[EventId.parse(xlist) for xlist in list_e] 
                                  
    if __name__ == '__main__':
        
        test=Bookmarks(event_ids=lists_id)
        
        asyncio.run(Can_book(test))
        list_e.clear()
        lists_id.clear()
        e_view.config(text="e tag?: ")
        error_label.config(text="Problem:")
        print_label.config(text="Wait for the bookmark",foreground="black")
    button_entry1.config(text="■",foreground="grey")    

def check_square():
    if list_e!=[]:
       button_entry1.config(text="■",foreground="green")
       error_label.config(text="ok")
       print_label.config(text="ok! ", font=("Arial",12,"bold"),foreground="blue")
              
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for the bookmark", font=("Arial",12,"bold"),foreground="black")
        button_entry1.config(text="■",foreground="grey")

button_send=tk.Button(root,text="send bookmark",command=create_bookmark, background="darkgrey",font=("Arial",14,"bold"))
error_label = tk.Label(root, text="Problem:",font=("Arial",12))
print_label = ttk.Label(root, text="Wait for the bookmark",font=("Arial",12))
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
Bad_relay_connection=["wss://relay.chakany.systems/","wss://nostrelites.org/","wss://feeds.nostr.band/","wss://relay.noswhere.com/","wss://relay.purplestr.com/","wss://relay.nostr.band/","wss://relay.momostr.pink/","wss://relay.phoenix.social/","wss://nostr.fmt.wiz.biz/"]
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
        if tags_note[0]=="e":
         global list_e
         if tags_note[1]not in list_e:
          list_e.append(tags_note[1])   
       return list_e

def edit_note(note_ex):
    test = edit_json(note_ex)               
    list_e=test.__list__()
    return list_e

async def Can_book(tag):
    # Init logger
  init_logger(LogLevel.INFO)
   
  key_string=log_these_key()
  if key_string!=None: 
    keys = Keys.parse(key_string)
    signer = NostrSigner.keys(keys)
    
    client = Client(signer)
    # Add relays and connect
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(RelayUrl.parse(jrelay))

    # Add relays and connect
    await client.add_relay(RelayUrl.parse("wss://relay.lnfi.network/"))
    await client.add_relay(RelayUrl.parse("wss://relay.braydon.com/"))
    await client.connect()
     
    builder = EventBuilder.bookmarks(tag)
    result_test= await client.send_event_builder(builder)
    
    print("Event sent:", result_test.id.to_hex())
    
    await asyncio.sleep(2.0)

    # Get events from relays
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()]).kind(Kind(10003))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     print(event.as_json())

async def edit_can_book(tag,pubkey):
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
    await client.connect()
    
    builder = EventBuilder.bookmarks(tag)
    test_result_post= await client.send_event_builder(builder)

    print("Event sent:")

    await asyncio.sleep(2.0)
    # Get events from relays
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()]).kind(Kind(10003))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     print(event.as_json())
    return test_result_post    
   else:
      print("no match", pubkey, "with \n", keys.public_key().to_hex())
  else:
      print("no key")     

async def get_result_w(client):
   try: 
    f = Filter().author(npub_bookmark[0]).kind(Kind(10003)).limit(10)
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
       if npub_bookmark!=[]:
        combined_results = await get_result_w(client)
        return combined_results
    # Init logger
    init_logger(LogLevel.INFO)
    client = Client(None)
     
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.connect()
    await search_box_relay()
    print("found ", len(relay_list), " relays")

async def get_outbox_relay(client):
   if npub_bookmark!=[]:
    f=Filter().authors(npub_bookmark).kind(Kind(10002))
   else: 
    f=Filter().kind(Kind(10002)).reference("wss://nos.lol/").limit(50)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec()]
   return z

async def search_box_relay():
        
    client = Client(None)
    
    if relay_list!=[]:
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

def note_time_reply(note,reply):
    value=int((float(reply["created_at"]-note["created_at"])/(60)))
    if value>1440:
            if value>2880:
               return str(int((float(reply["created_at"]-note["created_at"])/(86400))))+str(" days later") 
            else:
               return str(int((float(reply["created_at"]-note["created_at"])/(86400))))+str(" day later") 
    else:
      time_result=float(int(reply["created_at"]-note["created_at"]))  
      str_time="Time: "+str(int(float(time_result/3600)))+" Hour  & " +str(int(time_result/60)-int(time_result/(3600))*60)+" Minutes later"
      return str_time

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

def show_note_from_id(note):
        result:str=note["id"]
        replay=nota_reply_id(note)
        
        if replay!=[]:
           items=get_note(asyncio.run(Get_id(replay)))
        else:
           items=get_note(asyncio.run(Get_id(result)))
        return items   

def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[] and tags_string(nota,"e")!=None:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id          

def add_reply_idto_comment():
    if entry_second_note.get()!="" and evnt_id(entry_second_note.get())!=None:
       if first_reply==[]:
        first_reply.append(entry_second_note.get())
       else:
         first_reply.clear()
         first_reply.append(entry_second_note.get())  
       print(first_reply)

def stamp_balance_video(list_tag,obj):
  if obj=="imeta":
   list_tag_ast=ast.literal_eval(list_tag)
   
   for dim_photo in list_tag_ast:
     print("test",dim_photo[0][4:])
     if more_link(dim_photo[0][4:])=="video": 

      for jdim in dim_photo:
       if jdim[0:4]=="size":
        list_number=dim_photo.index(jdim)   
        number=dim_photo[list_number][5:]
        if number:
         if int(number)<int(13000000):
          stream_uri(dim_photo[0][4:], "my_video.mp4")
          
          if messagebox.askyesno("Form", "Do you want to see the video?"): 
            print('playing video using native player')
            os.system('my_video.mp4')
          
         print(float(round(int(number)/(1024**2),3)), "Megabyte")

def imeta_balance(list_tag,obj):
   if obj=="imeta":
      balance=[]
      url_=[]
      list_tag_imeta=ast.literal_eval(list_tag)
      for dim_photo in list_tag_imeta:
        if more_link(dim_photo[0][4:])=="pic": 
          url_.append(dim_photo[0][4:])
          for jdim in dim_photo:
            if str(jdim).startswith("dim"):
              list_number=jdim[4:]
              test2=list_number.split("x")
              balx=test2[0]
              baly=test2[1] 
              balance.append(float(int(balx)/int(baly)))
 
      return balance,url_       

def photo_from_tag(list_tag,obj):
    """imeta_balance ---> balance,url
    \n
    photo_tag ---> photo"""
    url_=video_thumb_tag(list_tag,obj)
    photo_view(url_)

def imeta_tag(list_tag,option):
    
    if option=="imeta":
      photo_from_tag(list_tag=list_tag,obj=option)  #note to tag1
      stamp_balance_video(list_tag,option)        #note to tag1   

def video_thumb_tag(list_tag,obj):
  if obj=="imeta":
   url=""
   list_tag_t=ast.literal_eval(list_tag)
   for dim_photo in list_tag_t:
     if more_link(dim_photo[0][4:])=="video": 
           
      for jdim in dim_photo:
       if jdim[0:5]=="image" or jdim[0:5]=="thumb":
        list_number=dim_photo.index(jdim) 
        url=  str(dim_photo[list_number][6:])
   if url!="":
    return url       

root.mainloop()