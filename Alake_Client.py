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
 
root = Tk()
root.title("Alake CLient")
root.geometry("1250x800")

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
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f

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

def url_strange(url):
   if url[0:13]=="https://t.me/":
      return "tme"
   else:
      return "no spam"

def block_url_spam(x):
   z=x['content']
   for j in z.split():
    if j[0:5]=="https":
       if len(x['content'])==len(j) or len(x['content'])+5==len(j):
           return "no context"  
       else:
             return codifica_link(x)

block_content=[]
block_japanese=[]
db_list=[]
block_npub=[]
relay_list=[]

def block_word(x):
  z=x["content"]
  words11=["block chain","Block chain","block Chain","Block Chain","#blockchain","#Blockchain"]
  words10=["#plebchain","#Plebchain","blockchain", "Blockchain"]
  words9=["#zapathon", "#Zapathon","#NostrZap", "#NostrBTC","shitcoins","OP RETURN","OP_RETURN"]
  words8=["#bitcoin","#Bitcoin","#BITCOIN","#payjoin","shitcoin","'Bitcoin","vmess://"]
  words7=["bitcoin","Bitcoin","BITCOIN","wallets","Wallets","mempool","bullish","BULLISH","Bullish","#crypto","#stocks","#monero"]
  words6=["primal","Primal","crypto","Crypto","tokens","Tokens","monero","Monero","sat/vB","nonce:","#nostr","#Nostr","#plebs"]
  words5=["$MSTR","block","BIP39", "stake", "miner", "proof","#Moon","#Mars","Nostr","HUMBLE", "STACK","L-BTC","#sexy"]
  words4=["sats","Sats","SATs","hash","Hash","hodl","Hodl","HODL","TH/s","#zap","#Zap","#SOL","MSTR","#USD","#XMR","#BTC","#ETH","#LTC","#btc","#CME"]
  words3=["zap","Zap","XMR","xmr","BTC","Btc","btc","ETH", "eth"]
  words1=["₿","👀","🔔","🤖"]

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
    
def find_japanese(text):
    # Regex pattern for Hiragana, Katakana, and Kanji (CJK Ideographs)
    japanese_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]')
    return japanese_pattern.findall(text)    

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
    z = [event.as_json() for event in events.to_vec()]
    return z   
   
async def Get():
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay("wss://nostr.mom/")
     await client.add_relay("wss://nos.lol/")
       
    await client.connect()
    await asyncio.sleep(2.0)
   
    test_kind = await get_kind(client)
    return test_kind   

def search_o_tags(x):
   tags_list=[]
   
   if x["tags"]!=[]:
      for jtags in x["tags"]:
         if len(jtags)>2:
          for xtags in jtags[2:]:
           if xtags not in tags_list:
            tags_list.append(xtags)
   return tags_list 

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list 

type_words=["no context","pic","tme"]

def filter_test(List_note):
 List_note_out=[]
 for jnote in List_note:
    if jnote['pubkey'] not in block_npub:
     if block_word(jnote)==None and  find_japanese(jnote['content'])==[]:  
        if (jnote['tags']!=[] or jnote['tags']==[]) and tags_string(jnote,"a")==[]and tags_string(jnote,"q")==[] and "mention" not in search_o_tags(jnote):
                      
           if Checkbutton8.get()==1:
            type_content=block_url_spam(jnote)
            if type_content!=None and type_content not in type_words:    
             if jnote not in List_note_out:      
              if Check_reply.get()==1:
               if tags_string(jnote,"e")!=[]:
                 List_note_out.append(jnote)

              else:     
               if tags_string(jnote,"e")==[]:
                List_note_out.append(jnote) 
           else:   
             if jnote not in List_note_out: 
              if Check_reply.get()==1:
               if tags_string(jnote,"e")!=[]:
                 List_note_out.append(jnote)

              else:     
               if tags_string(jnote,"e")==[]:
                List_note_out.append(jnote)

 return List_note_out    

def filter_light_test(List_note):
 List_note_out=[]
 for jnote in List_note:
    if jnote['pubkey'] not in block_npub:
     if block_word(jnote)==None and  find_japanese(jnote['content'])==[]:  
        if (jnote['tags']!=[] or jnote['tags']==[]) and tags_string(jnote,"a")==[]and tags_string(jnote,"q")==[] and "mention" not in search_o_tags(jnote):
          if label_light!=[]:
            type_content=block_url_spam(jnote)
            if type_content!=None and type_content not in label_light:    
             if jnote not in List_note_out:      
              if Check_reply.get()==1:
               if tags_string(jnote,"e")!=[]:
                 List_note_out.append(jnote)

              else:     
               if tags_string(jnote,"e")==[]:
                List_note_out.append(jnote)
          else:   
             if jnote not in List_note_out:      
              if Check_reply.get()==1:
               if tags_string(jnote,"e")!=[]:
                 List_note_out.append(jnote)

              else:     
               if tags_string(jnote,"e")==[]:
                List_note_out.append(jnote)
 return List_note_out

frame2=Frame(root, background="grey")

def add_db_list():
        
        def add_npub_to_list():
         if len(stringa_block.get())==64 or len(stringa_block.get())==63 or len(stringa_block.get())==69:
          try:
            test_user=PublicKey.parse(stringa_block.get())
            if test_user.to_hex() not in block_npub:
             block_npub.append(test_user.to_hex())
             
            for dbpub in db_list:
              if dbpub["pubkey"]== test_user.to_hex():
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
       
        Frame_block=Frame(root,width=50, height=10)
        
        stringa_bloc=StringVar()   
        stringa_block=Entry(Frame_block,textvariable=stringa_bloc,font=('Arial',12,'normal'),width=10)
        stringa_block.grid(column=0,row=1,padx=5,pady=5)
        random_block=Button(Frame_block, command=add_npub_to_list, text= "block npub",background="darkgrey",font=('Arial',12,'normal'))
        random_block.grid(column=1,row=1,padx=5,pady=5)
        label_string_block=StringVar()
        label_block=Label(Frame_block, textvariable=label_string_block,background="darkgrey",font=('Arial',12,'normal'))
        label_block.grid(column=2,row=1,padx=5,pady=5)
                
        def Close_block(event):
            Frame_block.destroy()
        
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=3, row=0, padx=5, rowspan=2) 
        entry_relay=ttk.Entry(Frame_block,justify='left',font=("Arial",12,"bold"),width=10)
        
        def relay_class():
          if entry_relay.get()!="":
            if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/":
           
                if entry_relay.get() not in relay_list:
                    relay_list.append(entry_relay.get())
                 
                counter_relay['text']=str(len(relay_list)) 
                counter_relay.grid(column=2,row=4)
                entry_relay.delete(0, END)

        relay_button = tk.Button(Frame_block, text="Add Relay!", font=("Arial",12,"normal"),background="grey", command=relay_class)
        counter_relay=Label(Frame_block,text="",background="darkgrey",font=('Arial',12,'normal'))
        entry_relay.grid(column=0, row=4, padx=5,pady=5)
        relay_button.grid(column=1, row=4, padx=10,pady=5)    
    
        def search_block_list():
            label_string_block1.set(len(db_list))
           
        def delete_block_list():
            db_list.clear()
            label_string_block1.set(len(db_list))    
    
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey",font=('Arial',12,'normal'))
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ",background="darkgrey",font=('Arial',12,'normal'))
        random_block1.grid(column=1,row=0,padx=5,pady=5)
        label_string_block1=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1,background="darkgrey",font=('Arial',12,'normal'))
        label_block_list1.grid(column=2,row=0,padx=5,pady=5)
        Frame_block.grid(column=0,row=0, columnspan=3, rowspan=3)
        
button_block_1=tk.Button(root, highlightcolor='WHITE',text='DB count',command=add_db_list,
                  width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
button_block_1.place(relx=0.08,rely=0.2, anchor="n")

def Open_structure():
    test=test_relay()
    
    if test:
        db_list_=filter_test(test)
        timeline_created(db_list_)
        
def Open_str():
    test=test_relay()
    
    if test:
        db_list_=filter_light_test(test)
        timeline_created(db_list_)
       

def preset_block_r():
       if Checkbutton8.get()==1:  
        text_in=" ⛔   List  " +"\n"+"\n"
        for event in type_words:
           text_in= text_in + event +"\n"
        lab_r.config(text=text_in )
        lab_r.place(relx=0.5,rely=0.01)
       else:
              lab_r.config(text=" ")
              lab_r.place_forget()            

def preset_reply():
       if Check_reply.get()==1:  
        text_in="\n"+" Only"+ "\n"+ "Reply " 
        
        lab_e.config(text=text_in )
        lab_e.place(relx=0.6,rely=0.01)
       else:
              lab_e.config(text=" ")
              lab_e.place_forget()      

button_structure=tk.Button(root, highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',
                  text='DB Relay',font=('Arial',14,'bold'),command=Open_structure)
button_structure.place(relx=0.42,rely=0.2,relwidth=0.1,anchor='n')

button_str=tk.Button(root, highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',
                  text='DB Spam',font=('Arial',14,'bold'),command=Open_str)
button_str.place(relx=0.31,rely=0.2,anchor='n')
Checkbutton8 = IntVar() 
Type_feed = Checkbutton(root, text = "Type R", variable = Checkbutton8, onvalue = 1, offvalue = 0, 
                    height = 2, width = 10,font=('Arial',16,'normal'),command=preset_block_r)
Type_feed.place(relx=0.68,rely=0.22,relwidth=0.1,relheight=0.05,anchor='e')  
Check_reply = IntVar() 
Type_reply = Checkbutton(root, text = "Reply ", variable = Check_reply, onvalue = 1, offvalue = 0, 
                    height = 2, width = 10,font=('Arial',16,'bold'), command=preset_reply)
Type_reply.place(relx=0.545,rely=0.12) 

type_light=["no spam","video","pic","tme","spam"]
label_light=[]
Checkbutton9 = IntVar() 
string_var_l=StringVar()

label_note=Entry(root,textvariable=string_var_l,font=('Arial',12,'normal'))
label_note_number=Label(root,text="",font=('Arial',12,'bold'))
lab_spam = tk.Label(root, text="Name: ",font=('Arial',12,'normal'))
combo_spam = ttk.Combobox(root, values=type_light,font=('Arial',12,'normal'))
button_spam=Button(root,text="go!",background="darkgrey",font=('Arial',12,'normal'))
clear_Lab=Button(root, text= "Clear list ",background="darkgrey",font=('Arial',12,'normal'))
     
def add_db_light():
         
           combo_spam.place(relx=0.3,rely=0.12,relwidth=0.1)
           def go_spam():
            if label_note.get() in type_light:
               
               if label_note.get() not in label_light:
                 label_light.append(label_note.get())
                 string_var_l.set("")
                 label_note_number.place(relx=0.47,rely=0.04,relwidth=0.05)
                 label_note_number["text"]=len(label_light)
               else:
                  if len(label_light)>0:
                    string_var_l.set("")
                    label_note_number.place(relx=0.47,rely=0.04,relwidth=0.05)
                    label_note_number["text"]=len(label_light)  
           
           button_spam["command"]=go_spam
           
           def delete_filter_list():
            label_light.clear()
            label_note_number["text"]=len(label_light) 
            combo_spam.set("Option 1")
           clear_Lab["command"]=delete_filter_list
           if Checkbutton9.get()==1:
              string_var_l.set("")
              label_note.place(relx=0.3,rely=0.05,relwidth=0.1)
              button_spam.place(relx=0.41,rely=0.04,relwidth=0.05) 

              def spam_(event):
                selected_it = combo_spam.get()
                string_var_l.set(selected_it)
              
              combo_spam.set("Option 1")
              combo_spam.bind("<<ComboboxSelected>>",spam_)
              clear_Lab.place(relx=0.41,rely=0.11)      
              
           else:
              button_spam.place_forget()
              label_note.place_forget() 
              lab_spam.place_forget() 
              combo_spam.place_forget()
              label_note_number.place_forget()
              clear_Lab.place_forget()

Light_feed = Checkbutton(root, text = "Type S", variable = Checkbutton9, onvalue = 1, offvalue = 0, 
                    height = 2, width = 10,font=('Arial',16,'normal'),command=add_db_light)
Light_feed.place(relx=0.58,rely=0.22,relwidth=0.1,relheight=0.05,anchor='e')  
lab_r = tk.Label(root, text=" ",font=('Arial',12,'normal'))
lab_e = tk.Label(root, text=" ",font=('Arial',14,'normal'))

# Function buttons

def respond_to(note_text):
    show_print_test_tag(note_text)

def block_pubkey_out(note_):
        
         if len(note_["pubkey"])==64:
            test_user=PublicKey.parse(note_["pubkey"])
            
            if test_user.to_hex() not in block_npub:
             block_npub.append(test_user.to_hex())
            
            for dbpub in db_list:
              if dbpub["pubkey"]== test_user.to_hex():
                 db_list.remove(dbpub)
                 
         else:
            print("Error", " no pubkey")

def share(note_text):
    print(f"Note: \n {note_text}")

def layout():
   if db_list!=[]: 
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
         var_id=StringVar()
         label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
         label_id.grid(pady=1,padx=10,row=s,column=0, columnspan=3)
         var_id.set(" Author: "+note_text["pubkey"])
         
         scroll_bar_mini = tk.Scrollbar(scrollable_frame)
         scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
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
        
         Button(scrollable_frame, text="Open", command=lambda: respond_to(note_text)).grid(row=s + 2, column=0, padx=5, pady=5)
         blo_label = Button(scrollable_frame, text="😶",font=('Arial',12,'normal'), command=lambda: block_pubkey(note_text))
         blo_label.grid(row=s + 2, column=1, padx=5, pady=5)
         Button(scrollable_frame, text="Print Note", command=lambda: share(note_text)).grid(row=s + 2, column=2, padx=5, pady=5)
    s = 1
    n=0
    for note in db_list:
     n=n+1
     create_note(note, s)
     s += 3   
    
    frame1.place(relx=0.05,rely=0.3, relheight=0.4,relwidth=0.33)  
    def close_canvas():
        scrollable_frame.forget()
        canvas.destroy()
        frame1.destroy()

    if list_note_lib==[]:
     close_canvas() 

    def block_pubkey(note_):
        
         if len(note_["pubkey"])==64:
          
            test_user=PublicKey.parse(note_["pubkey"])
            if test_user.to_hex() not in block_npub:
             block_npub.append(test_user.to_hex())
             
             
            for dbpub in db_list:
              if dbpub["pubkey"]== test_user.to_hex():
                 db_list.remove(dbpub)
            if messagebox.askokcancel("Close feed!","Yes/No") == True:     
             close_canvas()     
         else:
            print("Error", " no pubkey")   

    button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
    button_close.grid(column=1,row=0, padx=5,pady=5)    

button_open=Button(root, command=layout, text="scroll",highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',font=('Arial',14,'bold'))
button_open.place(relx=0.2,rely=0.2, anchor="n")
frame_1=tk.Frame(root,height=100,width=200)
note_tag = tk.Label(root, text="Note",font=('Arial',12,'normal'))
entry4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
e_tag = tk.Label(root, text="e-Tag")
entry_tag=ttk.Entry(root,justify='left')
p_tag = tk.Label(root, text="p-Tag")
entryp_tag=ttk.Entry(root,justify='left')
enter_note = tk.Label(root, text="Enter Note")
str_test=StringVar()
entry_note=ttk.Entry(root,justify='left', textvariable=str_test)

def reply_event(note_val):
  
  str_test.set(note_val["id"])
  
  try:   
    event=entry_note.get()
    search_id=evnt_id(event)
    found_nota=asyncio.run(Get_id(search_id))
    
    nota=json.loads(found_nota[0].as_json())
    
    if nota!=[] and nota!=None:
        if entryp_tag.get()!="" or entry_tag.get()!="":
           entryp_tag.delete(0, END) 
           entry_tag.delete(0, END)
         
        entryp_tag.insert(0,nota['pubkey'])
        entry_tag.insert(0,nota['id'])
        note_tag1["text"] = "e: " + nota['id'][0:9]
    else:
      print("not found")
      entryp_tag.delete(0, END)
      entry_tag.delete(0, END)
      note_tag1.config(text="e"+" event_id")
      entry_note.delete(0, END)
     
      close_answer()

    return found_nota  
  except NostrSdkError as e:
    print(e)     

note_tag1 = tk.Label(root, text="e"+" event_id",font=('Arial',12,'normal'))
button_pre=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',12,'bold'))
close_=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))
event_idone=Button(root,text="Search_event_one", font=('Arial',12,'normal') ) 

def test_open(note_val):
    note_tag.place(relx=0.85,rely=0.01,relwidth=0.1,relheight=0.05,anchor='n' )
    entry4.place(relx=0.8,rely=0.05,relwidth=0.25,relheight=0.1,anchor='n' )
    
    e_tag.place(relx=0.82,rely=0.47,relwidth=0.1 )
    entry_tag.place(relx=0.82,rely=0.52,relwidth=0.1,relheight=0.05 )
    p_tag.place(relx=0.7,rely=0.47,relwidth=0.1 )
    entryp_tag.place(relx=0.7,rely=0.52,relwidth=0.1,relheight=0.05 )
    enter_note.place(relx=0.7,rely=0.59,relwidth=0.1 )
    entry_note.place(relx=0.7,rely=0.65,relwidth=0.1)
    note_tag1.place(relx=0.75,rely=0.01,relwidth=0.1,relheight=0.04,anchor='n' )
    event_idone["command"]= reply_event(note_val)
    event_idone.place(relx=0.88,rely=0.62,anchor='n' )
    close_["command"] = close_answer
    close_.place(relx=0.8,rely=0.7,relwidth=0.05,relheight=0.05,anchor='n' )
    
    def Preview():
      if entry4.get()!="": 
        frame1=Frame(root, width=310, height=100)
        canvas = Canvas(frame1)
        canvas.pack(side="left", fill=BOTH, expand=True)
        canvas.bind( "<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
        def create_note(note_text, s):
         
            if len(note_text)<200:
             message = Message(scrollable_frame, text=note_text, width=300, font=('Arial',12,'normal'))
             message.grid(row=s, column=0, columnspan=3, padx=5)
            else:
               note_text2=str(note_text[0:200])+" "+str("...Continue...")
               print(note_text2)
               message = Message(scrollable_frame, text=note_text2, width=300, font=('Arial',12,'normal'))
               message.grid(row=s, column=0, columnspan=3, padx=5)
            Button(scrollable_frame, text="Print Note", command=lambda: share(note_text)).grid(row=s + 1, column=4)

        s = 1
        while s<2:
         if entry4.get()!="":
            create_note(entry4.get(), s)
         s += 2   
        frame1.place(relx=0.7,rely=0.21, relheight=0.25,relwidth=0.3)  

        def close_canvas():
            scrollable_frame.forget()
            canvas.destroy()
            frame1.destroy()
          
        button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal'))
        button_close.grid(column=4,row=1) 
        
    button_pre["command"]= Preview
    button_pre.place(relx=0.75,rely=0.15,relwidth=0.1, anchor="n") 
    button_reply["command"]=lambda: reply_note(note_val)
    button_reply.place(relx=0.85,rely=0.15,relwidth=0.1,anchor='n' )
    if entry_tag.get()=="":
        close_answer()    

def close_answer():
  button_reply.place_forget() 
  button_pre.place_forget()  
  note_tag.place_forget() 
  if entry4.get()!="":
   entry4.delete(0, END)
  entry4.place_forget()
  e_tag.place_forget()
  entry_tag.place_forget()
  p_tag.place_forget()
  entryp_tag.place_forget()
  enter_note.place_forget()
  entry_note.place_forget()
  note_tag1.place_forget()
  event_idone.place_forget()
  close_.place_forget()

def reply_note(note):
  if entry4.get()!="" and entryp_tag.get()!="" and entry_tag.get()!="": 
   person=convert_user(entryp_tag.get())
   test = evnt_id(entry_tag.get())
   test_event=reply_event(note)
   if person !=None and test!=None:
    tags=Tag.from_standardized(TagStandard.EVENT_TAG(test,None,Marker.REPLY,person,FALSE)),Tag.from_standardized(TagStandard.PUBLIC_KEY_TAG(person,None,None,FALSE))
    if __name__ == '__main__':
     note=entry4.get()
     tag=tags
     asyncio.run(reply(note,tag,test_event[0]))
  close_answer()

button_reply=tk.Button(root,text="send reply", background="darkgrey", font=('Arial',12,'normal'))

def share(note_text):
    print(f"Note:\n{note_text}")

async def get_one_Event(client, event_):
    f = Filter().id(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z=[]  
    for event in events.to_vec():
     if event.verify()==True:
        z.append(event)
    if z!=[]: 
     return z   
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay("wss://nostr.mom/")
     await client.add_relay("wss://nos.lol/")
     await client.add_relay("wss://relay.primal.net/")
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(event_, list):
        print("errore")
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

async def reply(note,tag,test):
    # Init logger
    init_logger(LogLevel.INFO)
    keys = Keys.generate()
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     pass
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://nostr.oxtr.dev/")
    await client.add_relay("wss://nostr.stakey.net/")
    await client.connect()
    try:
     builder = EventBuilder.text_note_reply(note,test,test,relay_list[0])  #.tags(tag) 
     testNote= await client.send_event_builder_to(relay_list,builder)
     messagebox.showinfo("Result", "fail "+str(testNote.failed))
     print(str(testNote.success))
     print(str(testNote.id))
     print(str(testNote.id.to_bech32()))
     print("Getting events from relays...")
     f = Filter().authors([keys.public_key()])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     for event in events.to_vec():
      print(event.as_json())
    except NostrSdkError as e:
       print(e)
frame_1.grid(padx=20,pady=20)

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
     z = [event.as_json() for event in events.to_vec()]
     return z

async def get_one_note(client, e_id):
    f = Filter().id(EventId.parse(e_id))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_event_id(e_id):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay("wss://nos.lol/")
     await client.add_relay("wss://nostr.mom/")
     await client.add_relay("wss://purplerelay.com/")
    
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
        replay.append(result)
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
   button_grid2=Button(scrollable_frame_2,text=f"Answer!", command=lambda val=note: test_open(val))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)
    
   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply!", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    
   else:
    if tags_string(note,"imeta")!=[]:
     button_grid3=Button(scrollable_frame_2,text=f"See video!", command=lambda val=note: balance_video(val))
     button_grid3.grid(row=s+2,column=2,padx=5,pady=5)        

   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()    
   button_frame=Button(frame3,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.pack()   
   frame3.place(relx=0.4,rely=0.3,relheight=0.4,relwidth=0.3) 

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
     #print("error", "[]","maybe a video")

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
        
root.mainloop()
