import asyncio
from datetime import timedelta
from nostr_sdk import Keys, Client, NostrSigner
from nostr_sdk import PublicKey,ZapRequestData,Metadata,SecretKey
from nostr_sdk import Tag, init_logger, LogLevel,ClientBuilder,SingleLetterTag,TagStandard
from nostr_sdk import EventId,EventBuilder, Filter, Metadata,Kind,NostrConnectUri,NostrConnect, NostrSdkError,uniffi_set_event_loop
import json
import requests
import time
from asyncio import get_event_loop
from nostr_sdk import Kind,Nip19Event,Nip19Enum,SubscribeOutput,SubscribeOptions,FilterRecord,Alphabet,Nip21,Coordinate,RelayUrl
from nostr_sdk import TagKind
import requests
import shutil
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import *
from tkinter import ttk
root = tk.Tk()
root.geometry('1200x800') 
db_note_list=[]

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f

def timeline_created(list_new):
  new_note=[] 
  global db_note_list
  if db_note_list!=[]:
   for new_x in list_new:
    if block_word(list_x)==None and  find_japanese(list_x['content'])==[]:  
     if new_x not in db_note_list:
        new_note.append(new_x) 
   i=0
    
   while i<len(new_note):
     j=0
     while j< len(db_note_list): 
      if db_note_list[j]["created_at"]>(new_note[i]["created_at"]):
         j=j+1
      else:
         db_note_list.insert(j,new_note[i])
         break
     i=i+1
   return db_note_list   
  else:
        for list_x in list_new:
            if block_word(list_x)==None and  find_japanese(list_x['content'])==[]:  
             db_note_list.append(list_x)
        return db_note_list  

def tags_string(x,obj):
    f=x["tags"]
    z=[]
    if f!=[]:
     for j in f:
      if j[0]==obj:
          z.append(j[1])
     return z     

def codifica_link(x):
   f=url_spam(x)
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
   stringa_pic.set(url_spam(note))
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
        frame_pic.place(relx=0.4,rely=0.01,relwidth=0.23,relheight=0.25,anchor="n")
       except TypeError as e: 
        print(e)

list_note_out=[]

def show_noted():
  """Widget function \n
   Open feed Horizontal, 3 Row
   """
  frame2=tk.Frame(root)  
  if len(db_note_list)<=3:
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
  if db_note_list!=[] and len(list_note_out)!=len(db_note_list):
  
   s=1
   s1=0
   se=0         
   db_note_max=[]
   if len(db_note_list)>120:
      for note in db_note_list:
         if note not in list_note_out:
            list_note_out.append(note)
            if len(db_note_max)<120:
             db_note_max.append(note)
            else:
               break
                
   else:          
      db_note_max=db_note_list   
   for note in db_note_max:   
    
      if db_note_list.index(note)% 6==False:
        s1=0
        se=int(db_note_list.index(note)//6)*6    
  
      try:
       context0="Author: "+note['pubkey']
       context1=note['content']+"\n"
       context2=" "
       if note['tags']!=[]: 
        context2="---> tags: <--- "+"\n"   
        if tags_string(note,"e")!=[]:
              if four_tags(note,"e"):
                for F_note in four_tags(note,"e"):
                     context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              
        else:
               context2="---> Root  <--- "+"\n"
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
        context1=note['content']+"\n"
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=se,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=se+1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=se+1) 
      
       def print_id(entry):
            if entry["tags"]!=[]:
              print(db_note_list.index(entry)+1)
              if tags_string(entry,"e")!=[]:
                 show_print_test_tag(entry)
              else:
                 print(entry["tags"])   
                  
       def print_var(entry):
                print(entry)
                print(entry["content"])

       def print_photo(entry):
            if len(more_spam(entry))<2: 
              photo_print(entry)
            else:
               
               if tags_string(entry,"imeta")!=[]:
                photo_list_2(entry)
               else:
                  if len(more_spam(entry))==2:
                    photo_list(more_spam(entry))         
               
       button=Button(scrollable_frame_1,text=f"Print me 1!", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=se+2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read!", command=lambda val=note: print_id(val))
       button_grid2.grid(row=se+2,column=s1+1,padx=5,pady=5)    
       if note["tags"]!=[]:
        if tags_string(note,"image")!=[] or tags_string(note,"imeta")!=[]:
         button_grid3=Button(scrollable_frame_1,text=f"Click to see",command=lambda val=note: print_photo(val))
         button_grid3.grid(row=se+2,column=s1+2,padx=5,pady=5)  
     
       s=s+2  
       s1=s1+4
       root.update() 
      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="bottom", fill="x",padx=20)
   scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
   canvas_1.pack( fill="both", expand=True)
   frame2.place(relx=0.01,rely=0.3,relwidth=0.95,relheight=0.62)

   def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
        entry_text.place_forget()
        scroll_bar_text.place_forget()
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.5,rely=0.92,relwidth=0.1)      

scroll_bar_text = tk.Scrollbar(root, background="darkgrey")
entry_text=tk.Text(root, background="grey", yscrollcommand = scroll_bar_text.set, font=('Arial',14,'bold'))
scroll_bar_text.config( command = entry_text.yview )

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list 

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

def more_link(f):
   
   list=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam"   

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
       if response.ok==True:
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        image.thumbnail((250, 200))  # Resize image if necessary
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
  frame_pic.place(relx=0.4,rely=0.01,relwidth=0.18)

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

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z       

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
       if response.ok==True:
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
        number=balance[int(lbel_var.get())]
        test1=int(float(number)*200)
        if test1>400:
           test1=int(400)
        if test1<150:
           test1=int(160)   
        image.thumbnail((test1, 200))  # Resize image if necessary
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
   frame_pic.place(relx=0.4,rely=0.01,relwidth=0.24) 
  else:
     print("error", "none")        
 else:
     pass
     #print("error", "[]","maybe a video")

def test_relay():
   if __name__ == "__main__":
     
    combined_results = asyncio.run(Get_notes())
    List_note=get_note(combined_results)
   if List_note:
    
    return List_note    
   else:
      print("not found")
   
async def get_kind(client):
    f= Filter().kind(Kind(1)).limit(300)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z   

relay_list=[] 

async def Get_notes():
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
         relay_url = RelayUrl.parse(jrelay)
         await client.add_relay(relay_url)
    else:
     relay_url_1 = RelayUrl.parse("wss://nos.lol/")
     await client.add_relay(relay_url_1)
     relay_url_x = RelayUrl.parse("wss://nostr.mom/")
     await client.add_relay(relay_url_x)
    await client.connect()
    await asyncio.sleep(2.0)
   
    test_kind = await get_kind(client)
    return test_kind   

def second_one_filter():
     second_filter=test_relay()
     if second_filter:
         timeline_created(second_filter)
         print(len(db_note_list))
                
def show_read():
   show_noted()

button_RE=Button(root,command=second_one_filter, text="Relay Note", font=('Arial',12,'normal'))
button_RE.place(relx=0.2,rely=0.2,anchor='n' )  
button_open=Button(root,command=show_read, text="Read Note", font=('Arial',12,'normal'))
button_open.place(relx=0.2,rely=0.1,anchor='n' )  

def block_word(x):
  z=x["content"]
  if x["tags"]:
     if tags_string(x,"t")!=[]:
      for h_note in tags_string(x,"t"):
          if str("#"+h_note) not in z.split(" "):
           z=z+str("#")+str(h_note)+" "
         
             
  words11=["block chain","Block chain","block Chain","Block Chain","#blockchain","#Blockchain", "✄----------"]
  words10=["#plebchain","#Plebchain","blockchain", "Blockchain"]
  words9=["#zapathon", "#Zapathon","#NostrZap", "#NostrBTC","shitcoins","OP RETURN","OP_RETURN"]
  words8=["#bitcoin","#Bitcoin","#BITCOIN","#payjoin","shitcoin","'Bitcoin","vmess://"]
  words7=["bitcoin","Bitcoin","BITCOIN","wallets","Wallets","mempool","bullish","BULLISH","Bullish","#crypto","#stocks","#monero"]
  words6=["primal","Primal","crypto","Crypto","tokens","Tokens","monero","Monero","sat/vB","nonce:","#nostr","#Nostr","#plebs"]
  words5=["$MSTR","block","BIP39", "stake", "miner", "proof","#Moon","#Mars","Nostr","HUMBLE", "STACK","L-BTC","#sexy"]
  words4=["sats","Sats","SATs","hash","Hash","hodl","Hodl","HODL","TH/s","#zap","#Zap","#SOL","MSTR","#USD","#XMR","#BTC","#ETH","#LTC","#btc","#CME"]
  words3=["zap","Zap","XMR","xmr","BTC","Btc","btc","ETH", "eth"]
  words1=["₿","👀","🔔","🤖","🦀"]
  
  for j in z.split():
    if j[0:11] in words11:
        return str(j)
    if j[0:10] in words10:
        return str(j)
    if j[0:9] in words9:
        return str(j)
    if j[0:8] in words8:
        return str(j)
    if j[0:7] in words7:
        return str(j)
    if j[0:6] in words6:
        return str(j)
    if j[0:5] in words5:
        return str(j)
    if j[0:4] in words4:
        return str(j)
    if j[0:3] in words3:
        return str(j)
    if j[0:1] in words1:
        return str(j)
    
import re
    
def find_japanese(text):
    # Regex pattern for Hiragana, Katakana, and Kanji (CJK Ideographs)
    japanese_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]')
    return japanese_pattern.findall(text)    


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
   var_id_3.set("Author: "+note["pubkey"])
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
                context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
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
        z=3
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             var_id_r.set(" Author: "+jresult["pubkey"])
         
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
                   
   button=Button(scrollable_frame_2,text=f"Photo!", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
     
   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply!", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    

   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     button_frame.place_forget()
     frame3.destroy()    
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.75,rely=0.06) 
   frame3.place(relx=0.66,rely=0.1,relheight=0.35,relwidth=0.33) 

def show_note_from_id(note):
        result=note["id"]
        replay=nota_reply_id(note)
        if replay!=[]:
         replay_note=[]
         for note_x in db_note_list:
           if note_x["id"] in replay:
             if note_x not in replay_note:
              replay_note.append(note_x)
         if replay_note!=[]:
            return replay_note      

def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id    

def list_people_fun():
    people_list=[]
    if db_note_list!=[]:
        for note_x in db_note_list:
            if note_x["pubkey"] not in people_list:
                        people_list.append(note_x["pubkey"])
        return people_list       
    else:
       return people_list

def print_people(): 
   if db_note_list!=[]:  
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=280)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas,border=2)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    s=1     
    
    test1=list_people_fun()
    ra=0
    sz=0
    labeL_button=Label(scrollable_frame,text="Number of pubkey "+str(len(test1)))
    labeL_button.grid(row=0,column=1,padx=5,pady=5,columnspan=2)           
    while ra<len(test1):
                lenght,note_p=pubkey_id(test1[ra])
                if lenght>1:
                 sz=sz+1           
                 button_grid1=Button(scrollable_frame,text=f"{test1[ra][0:9]} ")
                 button_grid1.grid(row=s,column=1,padx=5,pady=5)
                 button_grid2=Button(scrollable_frame,text=f"{lenght}", command= lambda val=test1[ra]: pubkey_id(val))
                 button_grid2.grid(row=s,column=2,padx=5,pady=5)
                 button_grid2=Button(scrollable_frame,text=f"print", command= lambda val=note_p: show_lst_ntd(val))
                 button_grid2.grid(row=s,column=3,padx=5,pady=5) 
            
                 root.update()  
              
                s=s+1
            
                ra=ra+1   
    labeL_button.config(text="Number of pubkey "+str(len(test1))+"  "+"\n"+"Number of poster more than one note "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.3,rely=0.5,relwidth=0.28, relheight=0.3)      

    def Close_print():
       frame3.destroy()  
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

button_people_=tk.Button(root,text="List of People",command=print_people, font=('Arial',12,'bold'))
button_people_.place(relx=0.05,rely=0.1) 

def pubkey_id(test):
   note_pubkey=[]
   for note_x in db_note_list:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   return len(note_pubkey),note_pubkey          

def show_lst_ntd(list_note_p):
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
 if list_note_p!=[]:
  
  s=1
  s1=0
  
  for note in list_note_p:
         
      try:
       context0="Author: "+note['pubkey']
       context1=note['content']+"\n"
       context2=" "
       if note['tags']!=[]: 
        context2="---> tags: <--- "+"\n"   
        if tags_string(note,"e")!=[]:
              if four_tags(note,"e"):
                for F_note in four_tags(note,"e"):
                   if len(F_note)>3:  
                     context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              
        else:
               context2="---> Root  <--- "+"\n"
        for xnote in tags_string(note,"alt"):
         context2=context2+"\n"+str(xnote) +"\n"
       
        if tags_string(note,"t")!=None and tags_string(note,"t")!=[] :
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context2=context2+"#"+str(xnote) +" "
            s=s+1
        
       else: 
        context1=note['content']+"\n"
        context2=" "
           
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=1) 
      
       def print_id(entry):
            if entry["tags"]!=[]:
              print(db_note_list.index(entry)+1)
              if tags_string(entry,"e")!=[]:
                 show_print_test_tag(entry)
              else:
                 print(entry["tags"])   
                  
       def print_var(entry):
                print(entry["content"])

       def print_photo(entry):
            if len(more_spam(entry))<2: 
              photo_print(entry)
            else:
               
               if tags_string(entry,"imeta")!=[]:
                photo_list_2(entry)
               else:
                  if len(more_spam(entry))==2:
                    photo_list(more_spam(entry))                  
                                      
       button=Button(scrollable_frame_1,text=f"Print me!", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read!", command=lambda val=note: print_id(val))
       button_grid2.grid(row=2,column=s1+1,padx=5,pady=5)    
       if note["tags"]!=[]:
        if tags_string(note,"image")!=[] or tags_string(note,"imeta")!=[]:
         button_grid3=Button(scrollable_frame_1,text=f"Click to see",command=lambda val=note: print_photo(val))
         button_grid3.grid(row=2,column=s1+2,padx=5,pady=5)  
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

  scrollbar_1.pack(side="bottom", fill="x",padx=20)
  scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
  canvas_1.pack( fill="y", expand=True)
  frame2.place(relx=0.63,rely=0.5,relwidth=0.32,relheight=0.31)

  def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
  button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
  button_frame.place(relx=0.74,rely=0.83,relwidth=0.1)      

root.mainloop()
