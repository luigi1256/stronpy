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
  
value_min=0
root = Tk()
root.title("Search Threads")
root.geometry("1300x800")
value_min_int=IntVar(root,0)

def update_button():
   global value_min
   if int(entry_min.get())!=value_min:
      if int(entry_min.get())>=0:
         value_min=int(entry_min.get())

button_update=Button(root,text=f"Update", command=update_button,font=('Arial',12,'bold'))
entry_min=tk.Entry(root,textvariable =value_min_int,font=('Arial',12,'bold'),width=5)
button_min=tk.Label(root,text=f"Min ",font=('Arial',12,'bold'),width=4)

def list_of_thread(event_scrooll):
    thread_list=[]
    for note_x in event_scrooll:
        event_id=get_root(note_x)
        if event_id:
          for event_x in event_id:
            thread_list.append(event_x)
                    
    return thread_list           
             
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

def get_note(z):
  try:  
    
    f=[]
    if z:
      for j in z:
       f.append(json.loads(j))
    return f
  except TypeError as e:
     print(e)
  
def convert_user(x):
    try:
     other_user_pk = PublicKey.parse(x)
     return other_user_pk
    except NostrSdkError as e:
       print(e,"this is the hex_npub ",x)

def evnt_id(id):
    try: 
     test2=EventId.parse(id)
     return test2
    except NostrSdkError as e:
       print(e,"input ",id)

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

def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z

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

def url_strange(url):
   if url[0:13]=="https://t.me/":
      return "tme"
   else:
      return "no spam"

def block_url_spam(x:dict):
   z=x['content']
   for j in z.split():
    if j[0:5]=="https":
       if len(j)+5>=len(z):
           return "no context"  
       else:
             return codifica_link(x)

def note_invidious(x):
    f1=url_spam(x)
    if f1!=None:
       invidious(f1)

def invidious(url):
   if url[0:17]=='https://youtu.be/':
      string=str("https://inv.nadeko.net/")+str(url[17:])
      print(string)

block_content=[]
block_japanese=[]
db_list=[]
block_npub=set({})
relay_list=[]

def block_word(x):
  z=x["content"]
  data_words={11:{"block chain","Block chain","block Chain","Block Chain","#blockchain","#Blockchain"},10:{"#plebchain","#Plebchain","blockchain", "Blockchain"},9:{"#zapathon", "#Zapathon","#NostrZap", "#NostrBTC","shitcoins","OP RETURN","OP_RETURN"},"words8":{"#bitcoin","#Bitcoin","#BITCOIN","#payjoin","shitcoin","'Bitcoin"},7:{"bitcoin","Bitcoin","BITCOIN","wallets","Wallets","mempool","bullish","BULLISH","Bullish","#crypto","#stocks","#monero"},6:{"primal","Primal","crypto","Crypto","tokens","Tokens","monero","Monero","sat/vB","nonce:","#nostr","#Nostr","#plebs"},5:{"$MSTR","block","Block","BIP39", "stake", "miner", "proof","#Moon","#Mars","Nostr","HUMBLE", "STACK","L-BTC","#sexy"},4:{"sats","Sats","SATs","hash","Hash","hodl","Hodl","HODL","TH/s","#zap","#Zap","#SOL","MSTR","#USD","#XMR","#BTC","#ETH","#LTC","#btc","#CME"},3:{"zap","Zap","XMR","xmr","BTC","Btc","btc","ETH", "eth"},1:{"₿","👀","🔔","🤖"}}
  for event_x in str(z).split():
    lenght_word = len(event_x)
    if str(event_x).startswith("vmess://e"):
       return event_x
    if lenght_word in data_words and event_x in data_words[lenght_word]:
      return event_x
  return None    

def find_japanese(text):
    # Regex pattern for Hiragana, Katakana, and Kanji (CJK Ideographs)
    japanese_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]')
    return japanese_pattern.findall(text)    

def find_arabic(text):
  arbaic_pattern = re.compile(r'[\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd92-\ufdc7\ufe70-\ufefc\uFDF0-\uFDFD]')
  return arbaic_pattern.findall(text)

def test_relay():
   if __name__ == "__main__":
     
    combined_results = asyncio.run(Get())
    List_note=get_note(combined_results)
    if List_note:
      return List_note    
    else:
      print("not found")
   
async def get_kind(client):
    f= Filter().kind(Kind(1)).limit(300)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z   
   
async def Get():
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    list_relay_set={"wss://nos.lol/","wss://nostr.mom/"}
    for relay_x in list_relay_set:
         if relay_x not in relay_list:
            relay_list.append(relay_x)
    await Search_status(client=Client(None),list_relay_connect=relay_list) 
    if relay_list!=[]:
      
      for jrelay in relay_list:
         await client.add_relay(RelayUrl.parse(jrelay))
    
    await client.connect()
    await asyncio.sleep(2.0)
   
    test_kind = await get_kind(client)
    return test_kind   

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

type_words=["tme"]

def language_block(note):
    if isinstance(block_word(note),str): 
        return None
    if find_japanese(note['content']):
        return None
    if  find_arabic(note['content']): 
       return None 
    return note

def filter_test(List_note):
  List_note_out=[]
  for jnote in List_note:
    if jnote['pubkey'] not in block_npub:
        if language_block(jnote):    
            
            if jnote not in List_note_out:      
                
                if Check_reply.get()==1:
                    if tags_string(jnote,"e"):
                        List_note_out.append(jnote)

                else:     
                    if tags_string(jnote,"e")==[]:
                        List_note_out.append(jnote) 

  return List_note_out    

frame2=Frame(root, background="grey")

def add_npub_to_list():
 if len(stringa_block.get())==64 or len(stringa_block.get())==63 or len(stringa_block.get())==69:
  try:
    test_user=PublicKey.parse(stringa_block.get())
    block_npub.add(test_user.to_hex())
     
    for dbpub in db_list:
      if dbpub["pubkey"] in block_npub:
         db_list.remove(dbpub)
    label_string_block.set(len(block_npub))
    search_block_list()
    stringa_bloc.set("")
  except NostrSdkError as e:
      print(e)
      stringa_bloc.set("")
      label_string_block.set(len(block_npub))
 else:
    stringa_bloc.set("")
    label_string_block.set(len(block_npub))

def relay_class():
  if entry_relay.get()!="":
    if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/":
   
        if entry_relay.get() not in relay_list:
            relay_list.append(entry_relay.get())
            print(relay_list)
        counter_relay['text']=str(len(relay_list)) 
        
        entry_relay.delete(0, END)

def search_block_list():
    label_string_block1.set(len(db_list))
   
def delete_block_list():
    db_list.clear()
    label_string_block1.set(len(db_list))    

Frame_block=tk.Frame(root,width=80)
stringa_bloc=StringVar()   
stringa_block=Entry(Frame_block,textvariable=stringa_bloc,font=('Arial',12,'normal'),width=10)
clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey",font=('Arial',12,'normal'))
random_block1=Button(Frame_block, command=search_block_list, text= "DB: ",background="darkgrey",font=('Arial',12,'normal'))
random_block=Button(Frame_block, command=add_npub_to_list, text= "block npub",background="darkgrey",font=('Arial',12,'normal'))
label_string_block=StringVar()
label_block=Label(Frame_block, textvariable=label_string_block,background="darkgrey",font=('Arial',12,'normal'))
label_string_block1=StringVar()
entry_relay=ttk.Entry(Frame_block,justify='left',font=("Arial",12,"bold"),width=10) 
counter_relay=Label(Frame_block,text="",background="darkgrey",font=('Arial',12,'normal'))
relay_button = tk.Button(Frame_block, text="Add Relay ", font=("Arial",12,"normal"),background="grey", command=relay_class)
label_block_list1=Label(Frame_block, textvariable=label_string_block1,background="darkgrey",font=('Arial',12,'normal'))
stringa_block.grid(column=0,row=1,padx=5,pady=2)
random_block.grid(column=1,row=1,padx=5,pady=2)
label_block.grid(column=2,row=1,padx=5,pady=2)
label_block_list1.grid(column=2,row=0,padx=5,pady=2)
clear_block.grid(column=0,row=0,padx=5,pady=2)
random_block1.grid(column=1,row=0,padx=5,pady=2)      
entry_relay.grid(column=0, row=2, padx=5,pady=2)
relay_button.grid(column=1, row=2, padx=10,pady=2)    
counter_relay.grid(column=2,row=2,padx=2,pady=2)
#Frame_block.grid(column=0,row=0,columnspan=3,rowspan=3) 
Check_raw =IntVar()
Check_raw_root =IntVar()

def show_root_event():
   if Check_raw_root.get()==1:
      Check_raw_root.set(0)   
      random_root.config(background="white")
      
   else:
    Check_raw_root.set(1)      
    random_root.config(background="darkgrey")
    
random_root=tk.Button(root, command=show_root_event, text="root", background="white",font=('Arial',12,'normal'))
random_root.place(relx=0.1,rely=0.18)

def add_db_list():
    if Check_raw.get()==0:
      Check_raw.set(1)   
      Frame_block.grid(column=0,row=0,columnspan=3,rowspan=3) 
      button_block_1.config(text="Close")
      button_block_1.place(relx=0.2,rely=0.05)
    
    else:
       if Check_raw.get()==1:
        Check_raw.set(0)   
        Frame_block.grid_forget() 
        button_block_1.config(text="Settings")
        button_block_1.place(relx=0.02,rely=0.18)

button_block_1=tk.Button(root, highlightcolor='WHITE',text='Settings',command=add_db_list,font=('Arial',12,'bold'),height=1)
button_block_1.place(relx=0.02,rely=0.18)

def Open_structure():
    test=test_relay()
    
    if test:
      db_list_=filter_test(test)
      timeline_created(db_list_)
      search_block_list()
      button_open1.place(relx=0.1,rely=0.25)
      button_open.place(relx=0.24,rely=0.25)
      button_open2.place(relx=0.17,rely=0.25)
        
def preset_reply():
       if Check_reply.get()==1:  
        text_in=" Only"+ "\n"+ "Reply " 
        
        lab_e.config(text=text_in )
        lab_e.place(relx=0.32,rely=0.12,anchor="n")
       else:
              lab_e.config(text=" ")
              lab_e.place_forget()      

button_structure=tk.Button(root, highlightcolor='WHITE',border=2, text="Some Notes",font=('Arial',14,'bold'),command=Open_structure)
button_structure.place(relx=0.32,rely=0.06,anchor='n')
Check_reply = IntVar() 
Type_reply = Checkbutton(root, text = "Reply ", variable = Check_reply, onvalue = 1, offvalue = 0, 
                    width = 10,font=('Arial',16,'bold'), command=preset_reply)
Type_reply.place(relx=0.25,rely=0.18) 

lab_e = tk.Label(root, text=" ",font=('Arial',14,'normal'))

# Function buttons

def respond_to(note_text):
  show_print_test_tag(note_text)

def block_pubkey_out(note_):
  test_user=PublicKey.parse(note_["pubkey"])
          
  block_npub.add(test_user.to_hex())
  
  for dbpub in db_list:
    if dbpub["pubkey"] in block_npub:
        db_list.remove(dbpub)                              

def share(note_text):
    print(f"Note: \n {note_text}")

timeline_people=[]
db_list_note_follow=[]
Pubkey_Metadata={}
photo_profile={}

def pubkey_timeline():
   db_list_pubkey=[]
   global timeline_people
   for note in db_list:
      if note["pubkey"] not in timeline_people and note["pubkey"] not in block_npub and note["pubkey"] not in list(Pubkey_Metadata.keys()):
         db_list_pubkey.append(note["pubkey"])
   timeline_people=db_list_pubkey      

def search_kind(x):
   zeta=[]
   if __name__ == "__main__":
    # Example usage with a single key
    
    single_results = asyncio.run(feed_cluster([Kind(x)]))
    
    note=get_note(single_results)
    for r in note:
      if (r)['kind']==x:
         zeta.append(r)
   return zeta       

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

def list_pubkey_id():
  
   pubkey_timeline()
   metadata_note=search_kind(0)
   if metadata_note:
    try:
      for single in metadata_note:
        if metadata_0(single,"name"):
           Pubkey_Metadata[single["pubkey"]]=metadata_0(single,"name")
        else:
            if metadata_0(single,"display_name"):
              Pubkey_Metadata[single["pubkey"]]=metadata_0(single,"display_name")   

        if metadata_0(single,"picture"):
          photo_profile[single["pubkey"]]=metadata_0(single,"picture")   
                      
      print("Profile ",len(Pubkey_Metadata)," \n","Profile with image ",len(photo_profile)) 
    except KeyError as e:
      print("KeyError ",e)
    except json.JSONDecodeError as b:
      print(b)            

def layout(list_of_note):
   if db_list!=[]: 
    list_count=[]
    if Pubkey_Metadata=={}:
      if messagebox.askokcancel("Metadata user ","Yes/No") == True:
        list_pubkey_id()
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
    
    def create_note(note_text, s):
      if len(note_text["content"])>140 and len(note_text["content"])<800:
        if note_text["content"] not in list_note_lib:
          list_note_lib.append(note_text["content"])
          list_count.append(note_text)
          var_id=StringVar()
          label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
          label_id.grid(pady=1,padx=10,row=s,column=0, columnspan=3)
          if note_text['pubkey'] in list(Pubkey_Metadata.keys()):
            var_id.set("Nickname " +str(Pubkey_Metadata[note_text["pubkey"]]))
          else: 
            var_id.set(" Author: "+note_text["pubkey"])
         
          scroll_bar_mini = tk.Scrollbar(scrollable_frame)
          scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
          second_label10 = tk.Text(scrollable_frame, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
          context2=""   
          if tags_string(note_text,"t")!=[]:
            for note_tags in tags_string(note_text,"t"):
               context2=context2+str("#")+note_tags+" "
          
          second_label10.insert(END,note_text["content"]+"\n"+str(context2))
          scroll_bar_mini.config( command = second_label10.yview )
          if tags_string(note_text,"content-warning")==[]:
            second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
          else:
            second_label10.delete("1.0", "end")
            second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
          
            def content_show(): 
              if messagebox.askokcancel("Show this Note "+" "+str(tags_string(note_text,"content-warning")[0]),"Yes/No") == True:     
                second_label10.insert(END,note_text["content"]+"\n"+str(context2))     
                content.grid_forget()
          
            content = Button(scrollable_frame, text="show",font=('Arial',12,'normal'), command=content_show)
            content.grid(row=s+1, column=0, columnspan=3, padx=5, pady=5)  
        
          Button(scrollable_frame, text="Open", command=lambda: respond_to(note_text)).grid(row=s + 2, column=0, padx=5, pady=5)
          blo_label = Button(scrollable_frame, text="😶",font=('Arial',12,'normal'), command=lambda: block_pubkey(note_text))
          blo_label.grid(row=s + 2, column=1, padx=5, pady=5)
          Button(scrollable_frame, text="Print Note", command=lambda: share(note_text)).grid(row=s + 2, column=2, padx=5, pady=5)
    s = 1
    n=0
    
    for note in list_of_note:
      if note["pubkey"] not in block_npub:
        n=n+1
        create_note(note, s)
        s += 3   
    if Check_raw_root.get()==1:    #root thread    
      if list_of_thread(list_count):    
        print("root found ", len(list_of_thread(list_count)))
        list_root=get_event_list_eid(list_of_thread(list_count))
        if list_root:
          show_lst_ntd(list_root)
    frame1.place(relx=0.05,rely=0.3, relheight=0.4,relwidth=0.33)  
    
    def close_canvas():
        scrollable_frame.forget()
        canvas.destroy()
        frame1.destroy()
        button_open1.config(foreground='BLACK')
        button_open2.config(foreground='BLACK')
        button_open.config(foreground='BLACK')

    def block_pubkey(note_):
      block_npub.add(note_["pubkey"])
      for dbpub in db_list:
        if dbpub["pubkey"] in block_npub:
          db_list.remove(dbpub)
      search_block_list() 
      if messagebox.askokcancel("Close feed ","Yes/No") == True:     
             close_canvas()    
             
    button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close.grid(column=1,row=0, padx=5,pady=5)    
    if list_note_lib==[]:
      close_canvas() 
      if db_list!=[]:
        if messagebox.askyesno("Form", "Do you want to see these notes?"): 
          for note_x in db_list:
            print(note_x, "\n")
            note_invidious(note_x)

call_db_list=[]

def search_o_tags(x):
   tags_list=[]
   
   if x["tags"]!=[]:
      for jtags in x["tags"]:
         if len(jtags)>2:
          for xtags in jtags[2:]:
           if xtags not in tags_list:
            tags_list.append(xtags)
   return tags_list 

def mention_bind():
    call_db_list.clear()
    button_open1.config(foreground='BLACK')
    button_open2.config(foreground='BLACK')
    button_open.config(foreground='BLUE')
    for note in db_list:
      if tags_string(note,"q")!=[]:
          if note not in call_db_list:
             call_db_list.append(note)
      else:       
        if "mentions" in set(search_o_tags(note)):     
          if note not in call_db_list:
            call_db_list.append(note)  
    if call_db_list!=[]:         
      layout(call_db_list)       
                 
def reply_bind():
    button_open.config(foreground='BLACK')
    button_open1.config(foreground='BLACK')
    button_open2.config(foreground='BLUE')
    call_db_list.clear()
    for note in db_list:
       if tags_string(note,"e")!=[]:
        if "mentions" not in set(search_o_tags(note)):
          if note not in call_db_list:
                call_db_list.append(note)
                
    if call_db_list!=[]:         
      layout(call_db_list)         
     
def clean_bind():
    call_db_list.clear()
    button_open.config(foreground='BLACK')
    button_open2.config(foreground='BLACK')
    button_open1.config(foreground='BLUE')
    for note in db_list:
       if tags_string(note,"e")==[] and tags_string(note,"q")==[]:
          if note not in call_db_list:
             call_db_list.append(note)
    if call_db_list!=[]:  
      layout(call_db_list)                  

button_open=Button(root, text="Mention",command=mention_bind,highlightcolor='WHITE',font=('Arial',14,'bold'))
button_open1=Button(root, text="Clean",command=clean_bind,highlightcolor='WHITE',font=('Arial',14,'bold'))
button_open2=Button(root, text="Reply", command=reply_bind,highlightcolor='WHITE',font=('Arial',14,'bold'))
note_tag = tk.Label(root, text="Note",font=('Arial',12,'normal'))
entry4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
e_tag = tk.Label(root, text="e-Tag")
entry_tag=ttk.Entry(root,justify='left')
p_tag = tk.Label(root, text="p-Tag")
entryp_tag=ttk.Entry(root,justify='left')
enter_note = tk.Label(root, text="Enter Note")
str_test=StringVar()
entry_note=ttk.Entry(root,justify='left', textvariable=str_test)

note_tag1 = tk.Label(root, text="e"+" event_id",font=('Arial',12,'normal'))
button_pre=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',12,'bold'))
close_=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))
event_idone=Button(root,text="Search_event_one", font=('Arial',12,'normal') ) 

def share_note(note_text):
      test=EventId.parse(note_text["id"])
      test1=Nip19Event(test,PublicKey.parse(note_text["pubkey"]),Kind(note_text["kind"]),[])
      print(test1.to_nostr_uri())
      
      get_nevent_root(note_text)
      
      print(str(test.to_nostr_uri()))

def share(note_text):
    print(f"Note:\n{note_text}")
    note_invidious(note_text)
    share_note(note_text)

async def get_quote_note(client,event_q):
    f = Filter().id(event_q).limit(10)     #.event(event_q)
  
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10)) 
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def whats_note(event_id):
    # Init logger
        
    client = Client(None)
    
    # Add relays and connect
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
    if relay_hint!=[]:
      for relay_x in relay_hint:
        print(relay_x)
        await client.add_relay(RelayUrl.parse(relay_x))
   
    if relay_list!=[]:
     for xrelay in relay_list:
        if xrelay!=None and xrelay!="":
         print(xrelay)
         await client.add_relay(RelayUrl.parse(xrelay))
        else:
           print("errore") 
     await client.connect()
    else:
        await client.connect()   

    await asyncio.sleep(2.0)

    combined_results = await get_quote_note(client, event_id)
    
    return combined_results    

async def get_one_Event(client, event_):
    f = Filter().id(event_).event(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    list_relay_set={"wss://nos.lol/","wss://nostr.mom/","wss://relay.primal.net/"}
    for relay_x in list_relay_set:
      if relay_x not in relay_list:
        relay_list.append(relay_x)
    await Search_status(client=Client(None),list_relay_connect=relay_list) 
    for relay_c in relay_hint:
       await client.add_relay(RelayUrl.parse(relay_c))
    if relay_list!=[]:
       
      for jrelay in relay_list:
          await client.add_relay(RelayUrl.parse(jrelay))
    
    await client.connect()
    await asyncio.sleep(2.0)

    test_kind = await get_one_Event(client, event_)
    return test_kind


#----------------- end test

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

def more_link(f:str):
  
  data_sinc= {"video":{'mov','mp4'},"pic":{'png','jpg','gif','jpeg','webp'}}
  
  if f[-3:] in data_sinc["video"]:
        return "video"
  if f[-3:]  in data_sinc["pic"] or f[-4:] in data_sinc["pic"]:
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
  
        s=s+3
        button_close=Button(frame_pic,command=close_pic,text="close",font=("Arial",12,"bold"))
        button_close.grid(column=2,row=s+1,sticky="n")
        s=s+2
      except TypeError as e: 
        print(e)  
      except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")   
  frame_pic.place(relx=0.7,rely=0.01,relwidth=0.18)

def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[]:
      for event_id in tags_string(nota,'e'):
        if event_id not in e_id:
          e_id.append(event_id)   
    return e_id             

def reply_id(reply_list):
    
     e_id=[]  
     for nota in reply_list:  
        if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                 e_id.append(event_id)
     reply_note= get_note(asyncio.run(Get_event_id(e_id)))
     return reply_note

async def get_notes_(client, e_ids):
     f = Filter().ids([EventId.parse(e_id) for e_id in e_ids])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec() if event.verify()]
     return z

async def get_one_note(client, e_id):
    f = Filter().event(EventId.parse(e_id)).kind(Kind(1))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_event_id(e_id):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    list_relay_set={"wss://nos.lol/","wss://nostr.mom/","wss://purplerelay.com/"}
    for relay_x in list_relay_set:
      if relay_x not in relay_list:
         relay_list.append(relay_x)
    await Search_status(client=Client(None),list_relay_connect=relay_list) 
    if relay_list!=[]:
      
      for jrelay in relay_list:
         await client.add_relay(RelayUrl.parse(jrelay))
      
      await client.connect()
      await asyncio.sleep(2.0)
      if isinstance(e_id, list):
         print("list")
         test_id = await get_notes_(client,e_id)
      else:
        print("str")
        test_id = await get_one_note(client,e_id)
      
      return test_id

def show_note_from_id(note):
        result=note["id"]
        replay=nota_reply_id(note)
        
        if replay!=[]:
           items=get_note(asyncio.run(Get_event_id(replay)))
        else:
           items=get_note(asyncio.run(Get_event_id(result)))
        return items   

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
              
   var_id_s3=StringVar()
   label_id_3 = Message(scrollable_frame_2,textvariable=var_id_s3, relief=RAISED,width=290,font=("Arial",12,"normal"))
   label_id_3.grid(pady=1,padx=8,row=s,column=0, columnspan=3)
   if note['pubkey'] in list(Pubkey_Metadata.keys()):
      var_id_s3.set("Nickname " +str(Pubkey_Metadata[note["pubkey"]]))
   else: 
      if note['pubkey'] in dict_name:
        var_id_s3.set("Name: "+str(dict_name[note['pubkey']]))
      else:   
        var_id_s3.set("Pubkey: "+note["pubkey"][0:9])
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
        if four_tags(note,"e")!=[]:
            for F_note in four_tags(note,"e"):
               if len(F_note)>3: 
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
                   
   def print_reply_show(entry):
       if dict_name=={}:
          result=show_note_from_id(entry)
       else:   
        result=level_(entry["id"]) 

       if result: 
        
        z=5
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             if jresult['pubkey'] in list(Pubkey_Metadata.keys()):
                var_id_r.set("Nickname " +str(Pubkey_Metadata[jresult["pubkey"]]))
             else: 
                if note['pubkey'] in dict_name:
                    var_id_r.set("Name: " +str(dict_name[jresult['pubkey']]))
                else:
                    var_id_r.set("Pubkey: "+jresult["pubkey"][0:9])
         
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=5, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             context22="---> tags: <--- "+"\n"   
             if tags_string(jresult,"e")!=[]:
               if four_tags(jresult,"e")!=[]:
                  for F_note in four_tags(jresult,"e"):
                     if len(F_note)>3:     
                        context22=context22+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              
             else:
               context22="---> Root  <--- "  
             second_label10_r.insert(END,jresult["content"]+"\n"+str(context22))
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
           z=z+2
                   
   button_grid1=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val))
   button_grid1.grid(column=0,row=s+2,padx=5,pady=5)
   if is_video(note):
    button_grid2=Button(scrollable_frame_2,text=f"See Video ", command=lambda val=note: balance_video(val))
    button_grid2.grid(row=s+2,column=0,padx=5,pady=5) 
   button_grid2=Button(scrollable_frame_2,text=f"Answer ", command=lambda: print(note))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
       
   if tags_string(note,"e") or tags_string(note,"q"): 
    button_grid3=Button(scrollable_frame_2,text=f"Read Reply ", command=lambda val=note: print_reply_show(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    
   else:
       button_grid3=Button(scrollable_frame_2,text=f"Read Rootply ", command=lambda val=note: print_reply_show(val))
       button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    

   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()    
   
   button_frame=Button(scrollable_frame_2,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.grid(column=0,row=0,pady=5)   
   frame3.place(relx=0.4,rely=0.15,relheight=0.3,relwidth=0.3) 

def photo_list_2(note):
  
 balance,list_note1=balance_photo_print(note)
 photo_tag(balance=balance,list_note1=list_note1)

from smart_open import open
import os

def stream_uri(uri_in, uri_out, chunk_size=1 << 18):  # 256kB chunks
    """Write from uri_in to uri_out with minimal memory footprint."""
    with open(uri_in, "rb") as fin, open(uri_out, "wb") as fout:
        while chunk := fin.read(chunk_size):
            fout.write(chunk)

def is_video(nota):
    video_url=set({})
    if tags_str(nota,"imeta"):
      for dim_photo in tags_str(nota,"imeta"):
        if more_link(dim_photo[1][4:])=="video": 
           video_url.add(dim_photo[1][4:])
    return video_url

def balance_video(nota):
  if tags_str(nota,"imeta")!=[]:
   for dim_photo in tags_str(nota,"imeta"):
     if more_link(dim_photo[1][4:])=="video": 
      for jdim in dim_photo:
       if jdim[0:4]=="size":
        list_number=dim_photo.index(jdim)   
        number=dim_photo[list_number][5:]
        if number:
         if int(number)<int(13000000):
          stream_uri(dim_photo[1][4:], "my_video.mp4")
          
          if messagebox.askyesno("Form", "Do you want to see the video?"): 
            print('playing video using native player')
            os.system('my_video.mp4')
          
         print(float(round(int(number)/(1024**2),3)), "Megabyte")

async def get_note_cluster(client, type_of_event):
    if timeline_people!=[]:
     f = Filter().kinds(type_of_event).authors(user_convert(timeline_people)).limit(1000)
    else:
       f = Filter().kinds(type_of_event).limit(1000)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
    z = [event.as_json() for event in events.to_vec()]
    return z

async def feed_cluster(type_of_event):
    # Init logger
    init_logger(LogLevel.INFO)
   
    client = Client(None)
    list_relay_set={"wss://nos.lol/","wss://nostr.mom/","wss://purplerelay.com/"}
    for relay_x in list_relay_set:
      if relay_x not in relay_list:
         relay_list.append(relay_x)
    await Search_status(client=Client(None),list_relay_connect=relay_list) 
    if relay_list:
      for relay_j in relay_list:
         await client.add_relay(RelayUrl.parse(relay_j))  
    
    await client.connect()
    await asyncio.sleep(2.0)

    combined_results = await get_note_cluster(client, type_of_event)
    return combined_results

async def Search_status(client:Client,list_relay_connect:list):
    try: 
        if list_relay_connect:
            
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
                    
                    
                    if stats.bytes_received()>0:  #Auth or other stuff
                           if str(url) in list_relay_connect:
                            list_relay_connect.remove(str(url))
                    if i==1:

                     if stats.success()==0 and relay.is_connected()==False:
                            if str(url) in list_relay_connect:
                                list_relay_connect.remove(str(url))
                        
                    i=i+1 
    except IOError as e:
        print(e) 
    except ValueError as b:
        print(b)                   

import time

def found_level1(list_of_event:list):
    
    note_level_1=[] 
    if list_of_event:
      for eg in list_of_event:
        if eg not in db_list:
          db_list.append(eg)    
        if len(tags_string(eg,"e"))==1 and eg["kind"]==1:
          note_level_1.append(eg) 
    if note_level_1:
        show_lst_ntd(note_level_1)           

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
       if note['pubkey'] in list(Pubkey_Metadata.keys()):
         
         context0="Nickname " +Pubkey_Metadata[note["pubkey"]]
       else: 
            if note["pubkey"] in list(dict_name.keys()):
                context0="Name: "+dict_name[note['pubkey']]
            else:
               context0="Pubkey: "+note['pubkey'][0:9]
       
       time_result=float(int(time.time())-note["created_at"])  
       str_time="Time: "+str(int(float(time_result/3600)))+" Hour  & " +str(int(time_result/60)-int(time_result/(3600))*60)+" Minutes "
       context0=context0+"\n"+ str_time
       context1=note['content']+"\n"
       context2=" "
       if note['tags']!=[]: 
        context2=""   
        if tags_string(note,"alt")!=[]:
              for F_note in tags_str(note,"alt"):
                   
                  context2=context2+str( F_note )+"\n"
              
        for xnote in tags_str(note,"p"):
         context2=context2+"\n"+str(xnote) +"\n"
       
        if tags_string(note,"e")!=None and tags_string(note,"e")!=[] :
           s=0
           for xnote in tags_str(note,"e"):
            if s<5:
             context2=context2+str(xnote) +"\n"
            s=s+1
        
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,
                          font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, 
                                yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,context1+"\n"+str(context2))
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=1) 
      
       def print_id(entry):
            if entry["tags"]!=[]:
              #print(db_list.index(entry)+1)
              print(entry["tags"])   
              show_print_test_tag(entry)
                  
       def print_var(entry):
                print(entry)
                print(str(round(float((time.time()-float(entry["created_at"]))/86400),3)), " days")

       button=Button(scrollable_frame_1,text=f"Print note", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
       button_grid2.grid(row=2,column=s1+1,padx=5,pady=5)    
          
       s=s+2  
       s1=s1+4
      except TypeError as e:
         print(e)
      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

  scrollbar_1.pack(side="bottom", fill="x",padx=20)
  scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
  canvas_1.pack( fill="y", expand=True)
  frame2.place(relx=0.38,rely=0.53,relwidth=0.32,relheight=0.31)

  def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
  button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
  button_frame.place(relx=0.6,rely=0.87,relwidth=0.1)   

Set_name=["Alice","Bob","Carol","Dave","Eve","Frank","Grace","Heidi","Ivan","Judy",
          "Mallory","Niaj","Olivia","Peggy","Rupert","Sybil", "Ted","Vanna", "Walter"]
dict_name={}

def Assist_thread(list_result:list,author_pubkey:str):
    list_pubkey=[]
         
    for note_x in list_result:
        if note_x["pubkey"] not in list_pubkey and note_x["pubkey"]!=author_pubkey:
            list_pubkey.append(note_x["pubkey"])
        
           
    i=0
    if list_pubkey!=[]:
        while i <(len(Set_name)) and i<len(list_pubkey):
            dict_name[list_pubkey[i]]=Set_name[i]
                
            i=i+1

        dict_name[author_pubkey]="Author"

relay_hint=[]
author_pubkey=str("")

def print_people(test_people_thread:list, list_note_list): 
   if list_note_list!=[]:  
    
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=290)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    s=1     
    
    test1=test_people_thread
    ra=0
    sz=0
    labeL_button=Label(scrollable_frame,text="Number of pubkey "+str(len(test1)))
    labeL_button.grid(row=0,column=0,padx=5,pady=5,columnspan=4)           
    while ra<len(test1):
                lenght,note_p=pubkey_id(test1[ra],list_note_list)
                if lenght>value_min:
                 sz=sz+1   
                 if test1[ra] in list(Pubkey_Metadata.keys()):
                    button_grid1=Label(scrollable_frame,text=f"{Pubkey_Metadata[test1[ra]]} note {lenght}",width=20)
                 else:
                    button_grid1=Label(scrollable_frame,text=f"{test1[ra][0:9]} note {lenght}",width=20)
                 button_grid1.grid(row=s,column=0,padx=2,pady=5)
                 button_grid2=Button(scrollable_frame,text=f"Reply", command= lambda val=note_p: show_lst_ntd(val))
                 button_grid2.grid(row=s,column=2,padx=2,pady=5) 
                 button_grid3=Label(scrollable_frame,text=f"{dict_name[test1[ra]]}",width=20)
                 button_grid3.grid(row=s,column=3,padx=2,pady=5) 
            
                 root.update()  
              
                s=s+1
            
                ra=ra+1   
    labeL_button.config(text="Number of pubkey "+str(len(test1))+"  "+"\n"+f"Number of poster more than {str(value_min)} note "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
    button_people_2.place(relx=0.85,rely=0.93) 
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.7,rely=0.55,relwidth=0.3, relheight=0.3)      

    def Close_print():
       frame3.destroy()  
       button_people_2.place_forget()
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

button_people_2=Button(root,text=f"Metadata Users ", command=list_pubkey_id,font=('Arial',12,'bold'))

def pubkey_id(test, list_of_result):
   note_pubkey=[]
   for note_x in list_of_result:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   return len(note_pubkey),note_pubkey   

note_thread=[]

def Search_note_kind():
 if  search_str_entry.get()!="":
  quoted=search_str_entry.get()
  
  if quoted!=None and len(quoted)>62:
   other={"note1","nevent1"}
   notable=[]
   fk=quoted
    
   for other_x in other:
        notable.append(fk) if str(fk).startswith(other_x) else None
   if notable:
    return notable

def notes_value():
   notable=Search_note_kind()
   
   if notable:
    try: 
     for event in notable:  
                                                
      if event[0:7]=="nevent1":
         decode_nevent = Nip19Event.from_nostr_uri("nostr:"+event)
                
         decode_nevent1 = EventId.parse(decode_nevent.event_id().to_hex())
         relays=decode_nevent.relays()
         for relay_x in relays:
          relay_hint.append(str(relay_x))
         if __name__ == "__main__":    
          Metadata_nota=get_note(asyncio.run(whats_note(decode_nevent1)))
          if Metadata_nota:
           nota_content=[]
           for jmet in Metadata_nota:  
            if jmet not in nota_content: #and jmet["kind"]==1: 
             nota_content.append(jmet)  
           return nota_content
   
      if event[0:5]=="note1" and len(event)==63:
        decode_nevent = EventId.parse(event)
        if __name__ == "__main__":    
          Metadata_nota=get_note(asyncio.run(whats_note(decode_nevent)))
          if Metadata_nota:
            nota_content=[]
            for jmet in Metadata_nota: 
              if jmet not in nota_content and jmet["kind"]==1:   
                nota_content.append(jmet)
            return nota_content
    except NostrSdkError as e:
       print(e)
#search_str
##found root first or first level_note

db_list_thread=[]

def print_reply(note):
    result=get_event_reply(note)
    if result:   
      Assist_thread(list_result=result[::-1],author_pubkey=note["pubkey"])
      found_level1(result)  #open reply level 1
      print_people(list(dict_name.keys()),result)  #open people in thread
      button_update.place(relx=0.84,rely=0.87)  
      entry_min.place(relx=0.78,rely=0.88)
      button_min.place(relx=0.73,rely=0.88)
      return result
      
def create_note(jresult,note):
      db_list_thread.append(jresult)
      if float(int(time.time())-jresult["created_at"])/(86400)<0.33:
        time_result=float(int(time.time())-jresult["created_at"])  
        str_time=" Time "+str(int(float(time_result/3600)))+" Hour  & " +str(int(time_result/60)-int(time_result/(3600))*60)+" Minutes "
        context11=str(jresult['content']+"\n")
        if jresult["pubkey"]==note["pubkey"]:
          context00=str("Author: "+jresult['pubkey'][0:9] +str_time)
        else:
            if jresult["pubkey"] in list(dict_name.keys()):
              context00=str("Name: "+dict_name[jresult['pubkey']] +str_time)
            else:
                context00=str("Pubkey: "+jresult['pubkey'][0:9] +str_time)
        if jresult['tags']!=[]:
            context22=str("[[ Tags ]]"+"\n")
            for tag_test in (jresult)["tags"]:
                  context22=context22+str(tag_test)+"\n"
        else: 
            context22=str(" ")
             
        if jresult["kind"]==7:
            if jresult["pubkey"] in dict_name:
              context00=str("Name: "+dict_name[jresult['pubkey']] +" Time "+str(int(float(time_result/3600)))+" Hour  & ") 
            else:
                if jresult["pubkey"]==note["pubkey"]:
                    context00=str("Author: "+jresult['pubkey'][0:9] +" Time "+str(int(float(time_result/3600)))+" Hour  & ") 
                else:
                    context00=str("Pubkey: "+jresult['pubkey'][0:9] +" Time "+str(int(float(time_result/3600)))+" Hour  & ")
            context11=str("")
            context22=str("")
        if jresult["kind"]==6:
            if jresult["pubkey"] in dict_name:
              context00=str("Name: "+dict_name[jresult['pubkey']] +" Time "+str(int(float(time_result/3600)))+" Hour  & ") 
            else:
                if jresult["pubkey"]==note["pubkey"]:
                  context00=str("Author: "+jresult['pubkey'][0:9] +" Time "+str(int(float(time_result/3600)))+" Hour  & ") 
                else:
                    context00=str("Pubkey: "+jresult['pubkey'][0:9] +" Time "+str(int(float(time_result/3600)))+" Hour  & ") 
            context11=str("")
            context22=str("")    
        return context00,context11,context22

def print_id_1(test):
          print(test)  

def stamp_var(entry,obj):
          imeta_tag(entry.get(),obj.get())
          if obj.get()!="imeta":
            print(obj.get()) 
            print(entry.get())

def search_str(): 
  frame3=tk.Frame(root)
  canvas = tk.Canvas(frame3)
  scrollable_frame = ttk.Frame(canvas)
  scrollbar = ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
  scrollable_frame.bind("<Configure>",
   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
  canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
  canvas.configure(yscrollcommand=scrollbar.set)
  research_note = search_str_entry.get()
  if research_note!="":  
    s=1     
    test1=notes_value()
    if test1:
      for note in test1:
        var_id=StringVar()
        label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=250)
        if isinstance(note,dict):
          time_result=float(int(time.time())-note["created_at"])  
          str_time_author=" Time "+str(int(float(time_result/3600)))+" Hour  & " +str(int(time_result/60)-int(time_result/(3600))*60)+" Minutes "
          if note["tags"]!=[]:
            var_id.set("Author: "+note['pubkey'][0:9]+"\n"+str_time_author+"\n"+note["content"]+"\n"+"tags: "+str(len(note["tags"]))+"\n")
          else:
              var_id.set("Author: "+note['pubkey'][0:9]+"\n"+str_time_author+"\n"+note["content"]+"\n")   
        else:
            var_id.set(str(note)+"\n")    
        label_id.grid(pady=2,column=0,row=s,columnspan=3)
        button_grid2=Button(scrollable_frame,text="Tags", command=lambda val=note: print_tags(val))
        button_grid2.grid(row=s+2,column=0,padx=5,pady=5)    
        button_grid2=Button(scrollable_frame,text=f"Print  note ", command=lambda val=note: print_id_1(val))
        button_grid2.grid(row=s+2,column=2,padx=3,pady=5)
        button_grid4=Button(scrollable_frame,text=f"Reply id ", command=lambda val=note: reply_answer(val))
        button_grid4.grid(row=s+2,column=1,padx=1,pady=5)
        s=s+3
      root.update_idletasks()  
      root.after(100)
           
      def print_tags(entry):
                list_one,list_two=tags_first(entry)
                var_id_2=StringVar()
                var_id_3=StringVar()
                label_id_2= Message(scrollable_frame,textvariable=var_id_2, relief=RAISED,width=250,font=("Arial",12,"normal"))
                s=4
                
                def val_tag(val):
                    s=4
                    list_z,par=tags_parameters(list_one,list_two,val)
                    var_id_2.set(str(list_z))
                    var_id_3.set(par)
                    value=list_one.index(par)
                    label_id_2.grid(pady=2,column=1,row=s+value, columnspan=3)  

                button_list=[]
                if list_one:
                  z=0        
                  while z<len(list_one):
                    button_grid2=Button(scrollable_frame,text=str(list_one[z]), command=lambda val=list_one[z]: val_tag(val))
                    button_grid2.grid(row=s,column=0,padx=5,pady=5) 
                    button_list.append(button_grid2)      
                    z=z+1
                    s=s+1 
                  button_stamp=Button(scrollable_frame,text="stamp", command=lambda val=(var_id_2),val2=(var_id_3): stamp_var(val,val2))
                  button_stamp.grid(column=0,row=s+1,padx=5,pady=5)
                  
                  def close_Tags():
                    button_stamp.grid_forget()
                    for button2 in  button_list:
                      button2.grid_forget()
                    button_c_tags.grid_forget()
                    label_id_2.grid_forget()
                    
                  button_c_tags=Button(scrollable_frame,command=close_Tags,text="Close ❌",font=("Arial",12,"normal"))
                  button_c_tags.grid(column=0,columnspan=2)   
                                             
      def reply_answer(note):
        list_note=print_reply(note)
        if list_note:
          button_grid_p=Button(root,text="People", command=lambda val=list(dict_name.keys()), val2=list_note: print_people(val,val2),font=("Arial",12,"normal"))
          button_grid_p.place(relx=0.9,rely=0.87)   
          button_grid_p1=Button(root,text="First Replica", command=lambda val=list_note: found_level1(val), font=("Arial",12,"normal"))
          button_grid_p1.place(relx=0.45,rely=0.87)    
          button_list_2=[]
          s=4  
          for jresult in list_note:
            if create_note(jresult,note):              
              context00,context11,context22=create_note(jresult,note)
              var_id_1=StringVar()
              label_id_1 = Message(scrollable_frame,textvariable=var_id_1, relief=RAISED,width=310,font=("Arial",12,"normal"))
              var_id_1.set(context00)
              label_id_1.grid(pady=2,column=0, columnspan=3,row=s) 
              scroll_bar_mini_o = tk.Scrollbar(scrollable_frame)
              button_list_2.append(label_id_1)
              second_label_0 = tk.Text(scrollable_frame, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini_o.set,font=('Arial',14,'bold'),background="#D9D6D3")
              second_label_0.insert(END,context11+"\n"+str(context22))
              scroll_bar_mini_o.config( command = second_label_0.yview )
              if context11!="" and context22!="":
                second_label_0.grid(padx=5, column=0, columnspan=3, row=s+1) 
                scroll_bar_mini_o.grid( sticky = NS,column=4,row=s+1,pady=5)
                button_list_2.append(second_label_0)
                button_list_2.append(scroll_bar_mini_o)
              s=s+3
                  
          def close_Tags():
              for button2 in  button_list_2:
                button2.grid_forget()
              button_c_reply.grid_forget()
                  
          button_c_reply=Button(scrollable_frame,command=close_Tags,text="Close ❌",font=("Arial",12,"normal"))
          button_c_reply.grid(column=0, columnspan=2)

          def close_button():
              button_grid_p.place_forget()
              button_grid_p1.place_forget()
              button_close_p.place_forget()
              button_update.place_forget()
              entry_min.place_forget()
              button_min.place_forget()

          button_close_p=tk.Button(root,text="Close List",command=close_button, font=('Arial',12,'bold'))   
          button_close_p.place(relx=0.75,rely=0.07) 

      canvas.pack(side="left", fill="y", expand=True)
      if len(Pubkey_Metadata)==0 or len(list(Pubkey_Metadata.keys()))>3:
        scrollbar.place(relx=0.95,rely=0.01,relheight=0.6,relwidth=0.05)
      else:
        scrollbar.place(relx=0.95,rely=0.01,relheight=0.6,relwidth=0.05)
      frame3.place(relx=0.7,rely=0.2,relwidth=0.3, relheight=0.35)      
      
      def Close_print():
        frame3.destroy()  
        button_close_.place_forget()
    
      button_close_=tk.Button(root,text="Close 🗙",command=Close_print, font=('Arial',12,'bold'))
      if Pubkey_Metadata!={} or (research_note!="" and (len(research_note)==63 or len(research_note)>64)):  
        button_close_.place(relx=0.85,rely=0.13)   
      else:
          search_str_var.set("") 
          frame3.destroy()  

button4=tk.Button(root,text="Searchstr",command=search_str, font=('Arial',12,'bold'))
search_note_label = tk.Label(root, text="Note Npub ",font=("Arial",10,"bold"))
search_str_var=StringVar()
search_str_var.set("nevent1")
search_str_entry=tk.Entry(root, textvariable=search_str_var, width=20)
button4.place(relx=0.55,rely=0.07) 
search_str_entry.place(relx=0.45,rely=0.08,relheight=0.03)            

def tags_first(x):
  try:
    tags_list=[]
    tags_value=[]
    if x["tags"]:
      for jtags in x["tags"]:
         if jtags[0] not in tags_list:
            tags_list.append(jtags[0])
    if tags_list!=[]:
       for xtags in tags_list:
         for ztags in tags_str(x,xtags):
            tags_value.append(ztags)
    return tags_list,tags_value 
  except TypeError as e:
    print(e, x,type(x))

def tags_parameters(key,value,s):
    list_q=[]
    if s in key:
        for xvalue in value:
          if xvalue[0]==s:
              list_q.append(xvalue[1:])
    return list_q,s   

def get_event_reply(note):
    e_id=[]
    if tags_string(note,"e")!=[]:
        for e_event in tags_string(note,"e"):
           e_id.append(e_event)
    if e_id!=[]:
       result= get_note(asyncio.run(Get_event_id(e_id)))   #list
    else:
       result= get_note(asyncio.run(Get_event_id(note["id"])))    
    return result   

def get_event_list_eid(list_eid:list):
    if list_eid!=[]:
       result= get_note(asyncio.run(Get_event_id(list_eid)))       
       return result   

def get_root(note):
  
    list_root=[]
    if four_tags(note,"e"):  #if
      for F_note in four_tags(note,"e"):  #ciclo
        if F_note[3]=="root":
           if F_note[1] not in list_root:
             list_root.append(F_note[1])
    if four_tags(note,"q"):
      for F_note in four_tags(note,"q"):
        if F_note not in list_root:
          list_root.append(F_note[1])         
    return list_root

def get_nevent_root(note):
  """problems
     root, relay, pubkey \n
     q tags
  """
  try:  
    if four_tags(note,"e"):  
      for F_note in four_tags(note,"e"):  
        if F_note[3]=="root":
          break
      if F_note[2]:
        relay_hint.append(F_note[2])
        if len(F_note)==5:
          test_nevent=Nip19Event(EventId.parse(F_note[1]),PublicKey.parse(F_note[4]),Kind(note["kind"]),[RelayUrl.parse(relay_h) for relay_h in relay_hint])
          search_str_var.set(test_nevent.to_nostr_uri()[6:])
                     
        else:
          test_nevent=Nip19Event(EventId.parse(F_note[1]),None,Kind(note["kind"]),[RelayUrl.parse(relay_h) for relay_h in relay_hint])
          search_str_var.set(test_nevent.to_nostr_uri()[6:])
                       
      else:
          test_nevent=Nip19Event(EventId.parse(F_note[1]),None,Kind(note["kind"]),[RelayUrl.parse(relay_h) for relay_h in relay_hint])
          search_str_var.set(test_nevent.to_bech32()) 
    else:
        if four_tags(note,"q"):
          for F_note in four_tags(note,"q"):
            if F_note[2]:
              relay_hint.append(F_note[2])
            q_event=F_note[1]
            test_nevent=Nip19Event(EventId.parse(q_event),None,Kind(note["kind"]),[RelayUrl.parse(relay_h) for relay_h in relay_hint])
            search_str_var.set(test_nevent.to_bech32())       
            
  except NostrSdkError as e:
    print(e,"\n",note)
  except IndexError as b:
     print(b,note)  
  except UnicodeEncodeError as c:
     print(c,note)

def default_phase():
    dict_name.clear()
    search_str_var.set("")

button5=tk.Button(root,text="Default",command=default_phase, font=('Arial',12,'bold'))
button5.place(relx=0.63,rely=0.07)     

def level_two(level1:str,db_thread):
    print("level two ", len(db_thread))    
    z=[]
    for note_x in db_thread:
      if level1 in tags_string(note_x,"e"):
            z.append(note_x)        
    return z                                                            
    
def level_(level1:str):
    
    z=[]
    sl=None
    for j, note_x in enumerate(db_list):
        if note_x["id"]==level1: 
           sl=j
           break
    
    if sl is not None:
        i =0    
        while i<len(db_list):
        
            if db_list[sl]["id"] in tags_string(db_list[i],"e"):
                sl=i
                if db_list[i] not in z:
                  z.append(db_list[i]) 
                i=-1  
            i=i+1    
    else:
       print("error on 1")  
       zeta=level_two(level1=level1,db_thread=db_list_thread)
       return zeta  
    return z

def imeta_balance(list_tag,obj):
 if obj=="imeta":
  try: 
    balance=[]
    url_=[]
    list_tag2=list_tag[2:-2]
    list_tag_one=list_tag2.split("], [")
    
    for list_tag_tot in list_tag_one:
      list_tag1=list_tag_tot.split("', ")
      if more_link(list_tag1[0][5:])=="pic": 
        url_.append(list_tag1[0][5:])
        for dim_photo_ in list_tag1:
          if str(dim_photo_).startswith("'dim"):
            dim_photo=dim_photo_[5:]
            if dim_photo!="":
             
              test2=dim_photo.split("x")
              balx=test2[0]
              baly=test2[1][0:-1]  
              balance.append(float(int(balx)/int(baly)))
   
    return balance,url_       

  except IndexError as e:
     print(e)          

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
    bal,url_=imeta_balance(list_tag,obj)
    photo_tag(balance=bal,list_note1=url_)

def photo_tag(balance,list_note1):
 
 frame_pic=tk.Frame(root,height=80,width= 80) 
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
   number_note=Label(frame_pic,text="N° Photo "+str(len(list_note1)), font=("SF Pro",14,"bold"))
   number_note.grid(column=1,row=0,columnspan=2)
   def print_photo():
     s=1  
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

import ast

def stamp_balance_video(list_tag,obj):
  if obj=="imeta":
   list_tag_ast=ast.literal_eval(list_tag)
   
   for dim_photo in list_tag_ast:
     print(dim_photo[0][4:])
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

def imeta_tag(list_tag,option):
    if option=="imeta":
      photo_from_tag(list_tag=list_tag,obj=option)  #note to tag1
      stamp_balance_video(list_tag,option)        #note to tag1   
    
root.mainloop()