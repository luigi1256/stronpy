#you need run fernet_key before

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
from tkinter.filedialog import askopenfilename
from nostr_sdk import *
import asyncio
from datetime import timedelta
import io
from cryptography.fernet import Fernet

colour1=''
colour2='grey'
colour3="#5fb1c0"
colour4='BLACK'

def write_txt_note(name,note_text):
       with open(name+".txt", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text)) 

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

def evnts_ids(list_id):
     Event=[]
     for j in list_id:
        if evnt_id(j):
         Event.append(evnt_id(j))
     return Event

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

#Nostr static function

Metadata_dict={}

root = Tk()
root.title("Test")
root.geometry("1250x800")
frame1=tk.Frame(root,height=100,width=200)

note_tag = tk.Label(root, text="Note",font=('Arial',12,'bold'))
entry4=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
str_test=StringVar()
entry_note=ttk.Entry(root,justify='left', textvariable=str_test)

relay_list=[]

button_pre=Button(root,text="preview",highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',12,'bold'))

close_=Button(root,text="Close X",highlightcolor='WHITE',
              width=10,height=1,border=2, cursor='hand1',
              font=('Arial',12,'normal'))

event_idone=Button(root,text="Search_event_one", font=('Arial',12,'normal') ) 

def write_json_note(name,note_text):
       with open(name+".json", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text)) 

def Open_json_note(name):
      if name:
        try:
            with open(name+str(".json"), mode="r", encoding="utf-8") as f:
                content = f.read()
                test=content
                return test
                
        except json.JSONDecodeError as e:
            messagebox.showerror("Json Error", f" Error \n {e}")
        except Exception as e:
            messagebox.showerror("Error file", f" Error \n {e}")

def write_json_fake_note(name,note_text):
    import json
    list_event=Open_json_fake_note(name)
    if list_event==[] or list_event==None:
     my_Note = [{"id":str(note_text)}]
     stringaJson = json.dumps(my_Note,indent=4)
     with open(name+str(".json"),"w") as file:
      file.write(stringaJson)
    else:
     list_event.append({"id":str(note_text)})
     stringaJson = json.dumps(list_event,indent=4)
     with open(name+str(".json"),"w") as file:
      file.write(stringaJson)   

def Open_json_fake_note(name):
            stringaJson=""
            try: 
             with open(name+str(".json"),"r") as file:
              for line in file:
               stringaJson+=line
              datoEstratto=json.loads(stringaJson)
              print (datoEstratto, type(datoEstratto))            
              return datoEstratto
            except FileNotFoundError as e:
               print(e)

def test_open():
    note_tag.place(relx=0.5,rely=0.24,relwidth=0.1,relheight=0.05,anchor='n' )
    entry4.place(relx=0.5,rely=0.3,relwidth=0.3,relheight=0.1,anchor='n' )
        
    close_["command"] = close_answer
    close_.place(relx=0.6,rely=0.25,relwidth=0.05,relheight=0.04,anchor='n' )
    
    def Preview():
      if entry4.get()!="": 
        frame1=Frame(root, width=310, height=100)
   
        canvas = Canvas(frame1)
        canvas.pack(side="left", fill=BOTH, expand=True)

        canvas.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Frame scrollabile
        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
        def create_note(note_text, s):
         # Message 
            if len(note_text)<200:
             message = Message(scrollable_frame, text=note_text, width=300, font=('Arial',12,'normal'))
             message.grid(row=s, column=0, columnspan=3, padx=5)
            else:
               note_text2=str(note_text)
               print(note_text2)
               scroll_bar_mini = tk.Scrollbar(scrollable_frame)
               scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
               second_label10 = tk.Text(scrollable_frame, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
               second_label10.insert(END,note_text)
               scroll_bar_mini.config( command = second_label10.yview )
               second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
              
            Button(scrollable_frame, text="Print Note", command=lambda: share(note_text)).grid(row=s + 2, column=0,pady=2)

        s = 1
        while s<2:
         if entry4.get()!="":
            create_note(entry4.get(), s)
         s += 3   

        frame1.place(relx=0.35,rely=0.48, relheight=0.25,relwidth=0.3) 

        def close_canvas():
            scrollable_frame.forget()
            canvas.destroy()
            frame1.destroy()
          
        button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal'))
        button_close.grid(column=2,row=3, pady=2) 
       
    button_pre["command"]= Preview
    button_pre.place(relx=0.42,rely=0.41,relwidth=0.1, anchor="n") 
    button_send.place(relx=0.58,rely=0.41,relwidth=0.1,anchor='n' )
   
button_create=Button(root,text="Post", command=test_open,font=('Arial',12,'bold'),background="grey").place(relx=0.77,rely=0.25,relwidth=0.1,relheight=0.05,anchor='n' )

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

def send_event():
    note=entry4.get()
    if note!="":
     if __name__ == '__main__':
                
      list_tag=link_share()
      if list_tag==None:
         list_tag=[]
      asyncio.run(main_note(note,list_tag))
      
      messagebox.showinfo("Success", "You have sent \n this note")
      entry4.delete(0, END)
      list_pow.clear()
      list_content.clear()
      list_h.clear()
      pow_show()
      h_show()
      content_show()
      check_square()
    else:
      messagebox.showerror("Fail", "Error, write something")
      entry4.delete(0, END)

button_send=tk.Button(root,text="send note", background="darkgrey", command=send_event, font=('Arial',12,'normal'))         

async def main_note(note,tags):
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
          await client.add_relay(jrelay)
       await client.connect()
    # Send an event using the Nostr Signer
    if list_pow!=[]:
     builder = EventBuilder.text_note(note).tags(tags).pow(int(list_pow[0]))
    else:
     builder = EventBuilder.text_note(note).tags(tags)    
    testNote = await client.send_event_builder(builder)
    
    messagebox.showinfo("Result",str(testNote.failed.keys)+"\n"+str(testNote.success))
    write_json_fake_note("note",testNote.id.to_hex())
    metadata = metadata_get()
    if metadata!=None:
     await client.set_metadata(metadata)
     await asyncio.sleep(2.0)
   
def share(note_text):
    print(f"Note: \n {note_text}")

#metadata_account

def Look_profile():
    frame_pic=tk.Frame(frame1,height=20,width= 80, background="darkgrey")
    name_label = tk.Label(frame_pic,text="Name ",font=('Arial',10,'bold'))
    name_label.grid(column=8,row=1,padx=10)
    label_about=Label(frame_pic, text="About ",font=('Arial',10,'bold'))
    label_about.grid(column=8,row=2,pady=2,padx=10)
    
    second_name= tk.Label(frame_pic,text="Name ",font=('Arial',10,'bold'))
    second_name.grid(column=8,row=4,pady=2,padx=10)
    label_picture=tk.Label(frame_pic,text="Picture ",font=('Arial',10,'bold'))
    label_picture.grid(column=8,row=5,pady=2,padx=10)
    label_address=tk.Label(frame_pic,text="Address ",font=('Arial',10,'bold'))
    label_address.grid(column=8,row=6,pady=2,padx=10)
    stringa_pic=tk.StringVar()
    stringa_name=tk.StringVar()
    stringa_about=tk.StringVar()
    stringa_address=tk.StringVar()
    
    label_name = Entry(frame_pic, textvariable=stringa_name)
    label_name.grid(column=9,row=1,pady=2)
    
    label_about = Entry(frame_pic, textvariable=stringa_about)
    label_about.grid(column=9,row=2,pady=2)
       
    label_name = Entry(frame_pic, textvariable=stringa_name)
    label_name.grid(column=9,row=4,pady=2)

    label_pic = Entry(frame_pic, textvariable=stringa_pic)
    label_pic.grid(column=9,row=5,pady=2)

    entry_address = Entry(frame_pic, textvariable=stringa_address)
    entry_address.grid(column=9,row=6,pady=2)

    def write_json(name,note_text):
       with open(name+".json", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text)) 
    def call_profile_():
       
        Metadata_dict["name"]=label_name.get()
        Metadata_dict["about"]=label_about.get()
        Metadata_dict["display_name"]=label_name.get()
        Metadata_dict["picture"]=label_pic.get()
        Metadata_dict["lud16"]=email_check(entry_address.get())
        s=1
        for xvalues in list(Metadata_dict.values()):
         if xvalues=="":
          if s==5:
           messagebox.showerror("No metadata", "Please insert \n something")
           
           
           return None
          else:
            s=s+1
        
        if Metadata_dict['picture']=="":  #checkimage
            metadata = Metadata()\
           .set_name(Metadata_dict['name']) \
           .set_display_name(Metadata_dict['display_name']) \
           .set_about(Metadata_dict['about']) \
           
        else:
            metadata = Metadata()\
            .set_name(Metadata_dict['name']) \
            .set_display_name(Metadata_dict['display_name']) \
            .set_about(Metadata_dict['about']) \
            .set_picture(Metadata_dict['picture']) \
            .set_lud16(Metadata_dict['lud16'])
            
        write_json("metadata",metadata.as_json())
        
    button_view_note=tk.Button(frame_pic, background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2,
                  highlightcolor='WHITE',
                  text='Save!',
                  font=('Arial',12,'bold'),
                  command=call_profile_           
                 )
    button_view_note.grid(column=11, row=1, padx=5, pady=5) 

    def open_json_metadata(name):
        if name:
           try: 
            with open(name+str(".json"), mode="r", encoding="utf-8") as f:
                content = f.read()
                data = json.loads(content)  
                return data
           except json.JSONDecodeError as e:
            messagebox.showerror("Json Error", f" Error \n {e}")
           except Exception as e:
            messagebox.showerror("Error file", f" Error \n {e}")

    def Open_json():
                data=open_json_metadata("metadata")  
                if "picture" in data.keys():
                 stringa_pic.set(data["picture"])
                stringa_name.set(data["name"])
                stringa_about.set(data["about"])
                if "lud16" in data.keys():
                 stringa_address.set(data["lud16"])

                Metadata_dict["name"]=label_name.get()
                Metadata_dict["about"]=label_about.get()
                Metadata_dict["display_name"]=label_name.get()
                Metadata_dict["picture"]=label_pic.get()
                Metadata_dict["lud16"]=email_check(entry_address.get())
                s=1
                for xvalues in list(Metadata_dict.values()):
                 if xvalues=="":
                    if s==5:
                        messagebox.showerror("No metadata", "Please insert \n something")
                        return None
                    else:
                        s=s+1
          
    button_rt_boost=tk.Button(frame_pic, background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2,
                  highlightcolor='WHITE',
                  text='Upload',
                  font=('Arial',12,'bold'),
                  command=Open_json            
                  )

    button_rt_boost.grid(column=11, row=2, padx=5,pady=5) 
    frame_pic.grid(row=4,column=8,rowspan=5, columnspan=4,pady=5)
    
    def Close_profile(event):
       frame_pic.destroy()
        
    button_close=tk.Button(frame_pic, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=0, padx=5, columnspan=1) 

button_b0=tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2,
                  highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  text='Account',
                  font=('Arial',16,'bold'),
                  command=Look_profile            
                  )

button_b0.place(relx=0.7,rely=0.1,relwidth=0.1)

def metadata_get():
  if Metadata_dict!={}: 
   if Metadata_dict['picture']=="":  #checkimage
            metadata = Metadata()\
                .set_name(Metadata_dict['name']) \
                .set_display_name(Metadata_dict['display_name']) \
                .set_about(Metadata_dict['about']) \
                

                     
            return metadata     
   else:
            metadata = Metadata()\
                .set_name(Metadata_dict['name']) \
                .set_display_name(Metadata_dict['display_name']) \
                .set_about(Metadata_dict['about']) \
                .set_picture(Metadata_dict['picture']) \
                
            
            
            return metadata     

def metadata_stress():
   counter_dict['text']=str(len(Metadata_dict)) 
   counter_dict.place(relx=0.88,rely=0.42)  

#button_b0_str=tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,activeforeground=colour4, highlightbackground=colour2,highlightcolor='WHITE',border=2, cursor='hand1',text='count metadata',font=('Arial',12,'normal'),command=metadata_stress)
#button_b0_str.place(relx=0.7,rely=0.4,relwidth=0.15)   

counter_dict=Label(root,text="count",font=('Arial',12,'bold'))
         
def open_relay():
    frame_account=tk.Frame(frame1, background="darkgrey")
    structure_relay = tk.Label(frame_account, text="relay",font=("Arial",12,"bold"))
    entry_relay=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"))
    structure_relay.grid(column=11, row=1, padx=5,pady=5) 
    button_beau.place_forget()

    def relay_class():
     if entry_relay.get()!="":
        if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/":
           
            if entry_relay.get() not in relay_list:
                relay_list.append(entry_relay.get())
                #print(relay_list)  
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=1)
            entry_relay.delete(0, END)
            combo_bo_r['value']=relay_list
            
            return relay_list  
     else:
       if relay_list!=[]:  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
           
       else:
          upload_relay_list("relay")  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
    
    def remove_one_relay():
     if combo_bo_r.get()!="":
        if combo_bo_r.get() in relay_list:
            number=relay_list.index(combo_bo_r.get())
            relay_list.pop(number)
            counter_relay['text']=str(len(relay_list)) 
            counter_relay.grid(column=12,row=1)
            combo_bo_r['value']=relay_list
            return relay_list  
     else:
       if relay_list!=[]:  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list
           
       else:
          upload_relay_list("relay")  
          counter_relay['text']=str(len(relay_list)) 
          counter_relay.grid(column=12,row=1)
          combo_bo_r['value']=relay_list        

    relay_button = tk.Button(frame_account, text="Check!", font=("Arial",12,"normal"),background="grey", command=relay_class)
    counter_relay=Label(frame_account,text="count")
    entry_relay.grid(column=11, row=2, padx=10,pady=5)
    relay_button.grid(column=12, row=2, padx=10,pady=5)
    relay_d_button = tk.Button(frame_account, text="Remove [R]", font=("Arial",12,"normal"),background="grey", command=remove_one_relay)
    relay_d_button.grid(column=13, row=3, padx=10,pady=5)

    def Close_profile(event):
       frame_account.destroy()
       
       button_beau.place(relx=0.5,rely=0.1) 
     
    button_close=tk.Button(frame_account, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=0, padx=5, columnspan=1) 
    
    def on_server(event):
       label_relay["text"] = combo_bo_r.get()[6:]
       
    label_relay = tk.Label(frame_account, text="Name relay",font=('Arial',12,'bold'))
    label_relay.grid(column=13,row=1,pady=5)
    combo_bo_r = ttk.Combobox(frame_account, font=('Arial',12,'normal'))
    combo_bo_r.grid(column=13,row=2,pady=5)
    combo_bo_r.set("Relays set")
    combo_bo_r.bind("<<ComboboxSelected>>", on_server)
    
    frame_account.grid(row=1,column=9,rowspan=2, columnspan=4,pady=5)

button_beau=tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2,
                  highlightcolor='WHITE',
                  text='Relay',
                  font=('Arial',12,'bold'),
                  command=open_relay            
                  )

button_beau.place(relx=0.5,rely=0.1) 

def write_json_relay(name,note_text):
       with open(name+".txt", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text))

def download_file_relay():
    if relay_list!=[]:
     write_json_relay("relay",relay_list)
    #message_box       

import json

def upload_relay_list(name):
    with open(name+".txt", 'r',encoding="utf-8") as file:
        global relay_list 
        new_relay=file.read()
        new_relay = json.loads(new_relay.replace("'", '"'))
        
        for jrelay in new_relay:
         if jrelay!="":
          if jrelay[0:6]=="wss://" and jrelay[-1]=="/":
           
            if jrelay not in relay_list:
                relay_list.append(jrelay)

button_dwn=tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2,
                  highlightcolor='WHITE',
                  text='⏬ Relays',
                  font=('Arial',12,'bold'),
                  command=download_file_relay          
                  )

button_dwn.place(relx=0.6,rely=0.1)

frame1.grid()    

Check_raw =IntVar()

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.02,rely=0.5,relheight=0.45,relwidth=0.3)  
        h_tag.place(relx=0.04,rely=0.53)
        h_tag_entry.place(relx=0.1,rely=0.53,relwidth=0.1)
        h_button.place(relx=0.21,rely=0.52)
        h_view.place(relx=0.05,rely=0.57 )
        content_tag.place(relx=0.04,rely=0.65 )
        entry_content.place(relx=0.12,rely=0.65,relwidth=0.1 )
        content_button.place(relx=0.23,rely=0.64)
        content_view.place(relx=0.05,rely=0.7)
        entrypow_tag.place(relx=0.11,rely=0.8, relwidth=0.1 )
        pow_view.place(relx=0.05,rely=0.85 )
        pow_tag.place(relx=0.04,rely=0.8 )
        pow_button.place(relx=0.23,rely=0.79)
        button_list_id.place(relx=0.45,rely=0.8,anchor='n' )
        button_entry1.place(relx=0.38,rely=0.8,relwidth=0.05, relheight=0.05,anchor="n" )
       
   else:
      Check_raw.set(0)
      stuff_frame.place_forget() 
      h_tag.place_forget()
      h_tag_entry.place_forget()
      h_button.place_forget()
      h_view.place_forget()
      content_tag.place_forget()
      entry_content.place_forget()
      content_button.place_forget()
      content_view.place_forget()
      entrypow_tag.place_forget()
      pow_view.place_forget()
      pow_tag.place_forget()
      pow_button.place_forget()
      button_list_id.place_forget()
      button_entry1.place_forget()
      
lab_button = tk.Button(root, text="Raw tag", font=("Arial",12,"bold"), command=raw_label)
lab_button.place(relx=0.75,rely=0.35)
stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)
h_tag = tk.Label(root, text="Hashtag",font=("Arial",12,"bold"))
h_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12))
pow_tag = tk.Label(root, text="pow-Tag",font=("Arial",12,"bold"))
var_number=IntVar()
entrypow_tag=ttk.Entry(root,justify='left',textvariable=var_number ,font=("Arial",12))
pow_view = tk.Label(root, text="pow tag?: ", font=("Arial",12,"bold"))

list_pow=[]

def pow_show():
    title=entrypow_tag.get()
    
    if title!="":
     
      try:
       
        if int(title)>0 and int(title)<25:    
                  
            if list_pow!=[]:
                
                pow_view.config(text=str(len(list_pow)))
                entrypow_tag.delete(0, END)  
            else:  
                
                list_pow.append(title)
                pow_view.config(text=str(len(list_pow)))
                entrypow_tag.delete(0, END) 
                return list_pow
                    
        else:
          entrypow_tag.delete(0, END) 

      except ValueError as e:
         print(e)
         entrypow_tag.delete(0, END) 
           
    else:
       entrypow_tag.delete(0, END) 
       if len(list_pow)>0:
        pow_view.config(text=str(len(list_pow)))
       else:
         pow_view.config(text=str("pow tag?: "))


pow_button = tk.Button(root, text="pow_show", font=("Arial",12,"bold"), command=pow_show)

list_h=[]

def h_show():
    
    title=h_tag_entry.get()
    if title!="": 
        
         if title not in list_h:
          if len(list_h)<3:
           list_h.append(title.lower())
           h_view.config(text=str(len(list_h)))
           h_tag_entry.delete(0, END) 
           return list_h
          else:
             h_view.config(text=str(len(list_h)))
             #h_view.config(text=str("yap it present already"))
             h_tag_entry.delete(0, END) 
             return list_h
            
         else:
              print("already present")
              h_view.config(text=str(len(list_h)))
              #h_view.config(text=str("yap it present already"))
              h_tag_entry.delete(0, END) 
              return list_h
        
    else:
          if len(list_h)>0:   
           h_tag_entry.delete(0, END) 
           return list_h 
          else:
             h_view.config(text=str("h tag?: "))      
    
list_content=[]

def content_show():
    content_tag_entry=entry_content.get()
    if content_tag_entry!="":
      
        if content_tag_entry not in list_content:
          if list_content==[]:                  
            list_content.append(content_tag_entry)
            content_view.config(text=str(len(list_content)))
            entry_content.delete(0, END)    

          else:
             content_view.config(text=" " )         
             entry_content.delete(0, END) 
        else:
             content_view.config(text=" " )         
             entry_content.delete(0, END) 
       
    else:   
        if len(list_content)==1:
              content_view.config(text=str(len(list_content)))
              entry_content.delete(0, END) 
              
        else:
           content_view.config(text="content: ") 
            
h_button = tk.Button(root, text="h_show", font=("Arial",12,"bold"), command=h_show)
h_view = tk.Label(root, text="h tag?: ", font=("Arial",12,"bold"))
content_tag = tk.Label(root, text="content-Tag",font=("Arial",12,"bold"))
entry_content=ttk.Entry(root,justify='left',font=("Arial",12))
content_button = tk.Button(root, text="content tag", font=("Arial",12,"bold"), command=content_show)
content_view = tk.Label(root, text="content: ", font=("helvetica",13,"bold"),justify="center")

def link_share():
   check_square()
   lists_id=[] 
   if button_entry1.cget('foreground')=="green":
    if list_pow!=[] or list_h !=[] or list_content!=[]:
      if list_content!=[]:  
        
            lists_id.append(Tag.custom(TagKind.CONTENT_WARNING(),list_content))
      if list_h!=[]:        
        for jlist in list_h:
            lists_id.append(Tag.hashtag(jlist))
      return lists_id     
      
def check_square():
    if  list_pow!=[] or list_h !=[] or list_content!=[]:
      button_entry1.config(text="■",foreground="green")
     
    else:
        button_entry1.config(text="■",foreground="grey")
        
button_list_id=tk.Button(root,text="Tag",command=link_share, background="darkgrey",font=("Arial",14,"bold"))  #only for fun
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2) #only for fun

def email_check(test:str):
   i=0
   name=""
   suff=""
   while i <len(test):
    if test[i]=="@":
       name=test[0:i]
       suff=test[i+1:]
    i=i+1
   if name!="" and suff!="":
      return test 
   else:
      return ""

root.mainloop()