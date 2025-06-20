
from cryptography.fernet import Fernet
from nostr_sdk import *
import asyncio
from datetime import timedelta
from nostr_sdk import PublicKey, SingleLetterTag
from nostr_sdk import Tag
from nostr_sdk import EventId,Event,Events,Nip19Event,Nip19
import time
from datetime import datetime
import uuid
import tkinter as tk
from tkinter import *
from tkinter import ttk
import io
from tkinter import messagebox 
import json
import requests
import shutil
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Speed Link")
root.geometry("1250x800")

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

def url_speed():
 z=d_title.get()
 for j in z.split():
    if j[0:8]=="https://":
        return str(j)   
    
def codifica_spam():
   f=url_speed()
   list=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jepg','webp'] 
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

def convert_user(x):
    try:
     other_user_pk = PublicKey.parse(x)
     return other_user_pk
    except NostrSdkError as e:
       print(e,"this is the hex_npub ",x)

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def url_bookmark():
 z=d_title.get()
 for j in z.split():
    if j[0:5]=="https":
        return str(j)   
    
def codifica_spam():
   f=url_bookmark()
   list=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jepg','webp'] 
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

def evnt_id(id):
    try: 
     test2=EventId.parse(id)
     return test2
    except NostrSdkError as e:
       print(e,"input ",id)

def get_note(z):
    f=[]
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

def event_string(note):
  quoted=note
  if quoted!=None:
   
   list=['npub1','note1']
   img=['nevent1']
   img1=['nprofile']
   other=['naddr1']
   normal=[]
   addressable=[]
   nip_19=[]
   if quoted==None:
        pass
   if quoted[0:5] in list:
        normal.append(quoted)
   if quoted[0:7] in img:
        nip_19.append(quoted) 
   if quoted[0:8] in img1:
       nip_19.append(quoted) 
   if quoted[0:6] in other:
       addressable.append(quoted)
     
   return normal,nip_19,addressable
   
  else:
     print("2")    
     return None,None,None

def nevent_example(note):
   normal,nip_19,addressable=event_string(note)
   if nip_19:
    for event in nip_19:
      if event[0:8]=="nprofile":
        decode_nprofile = Nip19Profile.from_nostr_uri("nostr:"+event)      
        print(f" Profile (decoded): {decode_nprofile.public_key().to_hex()}")

      if event[0:7]=="nevent1":
         decode_nevent = Nip19Event.from_nostr_uri("nostr:"+event)
         print(f" Event (decoded): {decode_nevent.event_id().to_hex()}")
         print(f" Event (decoded): {decode_nevent.relays()}")
         for xrelay in decode_nevent.relays():
           if xrelay[0:6]=="wss://" and xrelay[-1]=="/":
            if xrelay not in relay_list:
               relay_list.append(xrelay)
         return decode_nevent.event_id().to_hex()

def Open_sticky_note(name):
            stringaJson=""
            try: 
             with open(name+str(".json"),"r") as file:
              for line in file:
               stringaJson+=line
              datoEstratto=json.loads(stringaJson)
              return datoEstratto
            except FileNotFoundError as e:
               print(e)

async def link_it(tag,description):
   
   init_logger(LogLevel.INFO)
   key_string=log_these_key()
   if key_string!=None: 
    keys = Keys.parse(key_string)
       
    signer=NostrSigner.keys(keys)
    client = Client(signer)

    if relay_list!=[]:
       
     for jrelay in relay_list:
       await client.add_relay(jrelay)
     await client.connect()
    
     builder = EventBuilder(Kind(39701),description).tags(tag)
     test_result_post= await client.send_event_builder(builder)
     metadata = metadata_get()
     if metadata!=None:
      await client.set_metadata(metadata)
      await asyncio.sleep(2.0) 

      f = Filter().authors([keys.public_key()])
      events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
      for event in events.to_vec():
       print(event.as_json())
     return test_result_post    

def metadata_get():
  if Metadata_dict!={}: 
   if Metadata_dict['picture']=="":  #checkimage
            metadata = Metadata()\
                .set_name(Metadata_dict['name']) \
                .set_display_name(Metadata_dict['display_name']) \
                .set_about(Metadata_dict['about']) \
                .set_lud16(Metadata_dict['lud16'])

                     
            return metadata     
   else:
            metadata = Metadata()\
                .set_name(Metadata_dict['name']) \
                .set_display_name(Metadata_dict['display_name']) \
                .set_about(Metadata_dict['about']) \
                .set_picture(Metadata_dict['picture']) \
                .set_lud16(Metadata_dict['lud16'])
            
            return metadata     

def link_share():
   check_square()
   lists_id=[] 
   if button_entry1.cget('foreground')=="green":
    global d_identifier
    if d_identifier!="":
      
      lists_id.append(Tag.identifier(d_identifier))
      if list_title!=[]:   
         lists_id.append(Tag.title(list_title[0]))
         
         if combo_lab.get()!="Type of Hash-el":        
            lists_id.append(Tag.hashtag(combo_lab.get()))
         else:
            pass   

         if __name__ == '__main__':
          lists_id.append(Tag.custom(TagKind.PUBLISHED_AT() , [str( int(time.time()) )]))
          if list_content==[]:
             list_content.append("")
          test_result =asyncio.run(link_it(lists_id,list_content[0]))
          messagebox.showinfo("Result",str(test_result))
          button_entry1.config(text="■",foreground="grey")
          list_content.clear()
          list_title.clear()
          combo_lab.set("Type of Hash-el")
          d_identifier=""
          d_view.config(text="")  
          d_title.delete(0, END)
          descr_view.config(text="")
          r_view.config(text="")
          error_label.config(text="Problem:")
          print_label.config(text="Wait for Tag", font=("Arial",12,"bold"),foreground="black")
          
label_var=StringVar()
label_entry=ttk.Entry(root,justify='left',textvariable=label_var,font=("Arial",12))
Check_lab_entry =IntVar(root,0,"raw_lab")
button_enter_lab=tk.Button(root,text="Hash-el", background="darkgrey",font=("Arial",12,"bold"))

def update_list():
     
    if Check_lab_entry.get()==0:
      
      label_entry.place(relx=0.4,rely=0.18)
      Check_lab_entry.set(1)
            
      def entry_list():
         if label_entry.get().lower()!="" and label_entry.get().lower() not in Lab_list:
           Lab_list.append(label_entry.get().lower())
           label_var.set("")
           combo_lab["values"]=Lab_list
           button_enter_lab.place_forget()
           label_entry.place_forget()
           Check_lab_entry.set(0)
         else:
            label_var.set("")
            button_enter_lab.place_forget()
            label_entry.place_forget()
            Check_lab_entry.set(0)
      button_enter_lab['command']=entry_list 
      button_enter_lab.place(relx=0.45,rely=0.23)   
    else:
       Check_lab_entry.set(0)
       label_entry.place_forget()
       button_enter_lab.place_forget()

def write_json_lab(name,note_text):
       with open(name+".txt", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text))

def download_file_lab():
    if Lab_list!=[]:
     write_json_lab("label_test",Lab_list)

button_dwn_lab=tk.Button(root, 
                  highlightcolor='WHITE',
                  text='⏬ Label',
                  font=('Arial',12,'bold'),
                  command=download_file_lab          
                  )

#button_dwn_lab.place(relx=0.57,rely=0.115)

def upload_label_list(name):
    with open(name+".txt", 'r',encoding="utf-8") as file:
        global Lab_list 
        new_lab=file.read()
        new_lab = json.loads(new_lab.replace("'", '"'))
        
        for label_x in new_lab:
         if label_x!="":
            if label_x not in Lab_list:
                Lab_list.append(label_x)
                
        combo_lab["values"]=Lab_list        

frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
button_add_lab=tk.Button(frame1,text="add hash_el",command=update_list, font=("Arial",12,"bold"))  
button_add_lab.place(relx=0.2,rely=0.1)  
button_add_lab=tk.Button(root,text="Upload hash_el",command=lambda val="label_test":upload_label_list(val), font=("Arial",12,"bold"))  
button_add_lab.place(relx=0.32,rely=0.115)  
Lab_list=["energy","nostr","bitcoin","money","ai"]

def on_tags_event(event):
    selected_item=combo_lab.get()

combo_lab = ttk.Combobox(root, values=Lab_list,font=('Arial',14,'bold'))
combo_lab.place(relx=0.44,rely=0.12,relwidth=0.15)
combo_lab.set("Type of Hash-el")
combo_lab.bind("<<ComboboxSelected>>", on_tags_event)
list_h=[]
list_title=[]

def check_square():
    if d_identifier!="" and list_title!=[]:
       
       if combo_lab.get()!="Type of Hash-el":
        print_label.config(text="Hashtag "+combo_lab.get(), font=("Arial",12,"bold"),foreground="blue")
        button_entry1.config(text="■",foreground="green")
        error_label.config(text="ok")
       
       else:
        print_label.config(text="Hashtag "+combo_lab.get(), font=("Arial",12,"bold"),foreground="blue")
        button_entry1.config(text="■",foreground="green")
        error_label.config(text="ok, No Tag ")
  
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for Tag", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")
        
button_send=tk.Button(root,text="Speed Link",command=link_share, background="darkgrey",font=("Arial",14,"bold"))
button_send.place(relx=0.45,rely=0.65,relwidth=0.2,relheight=0.1,anchor='n' )
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
button_entry1.place(relx=0.57,rely=0.65,relwidth=0.05, relheight=0.1,anchor="n" )
error_label = tk.Label(frame1, text="Problem:",font=("Arial",12))
error_label.grid(column=3, rowspan=2, row=0, pady=5,padx=5)
print_label = ttk.Label(frame1, text="Wait for Tag",font=("Arial",12))
print_label.grid(column=3, columnspan=2, row=2, pady=5,padx=10)
Check_open =IntVar()

def Look_profile():
    frame_pic=tk.Frame(frame3,height=20,width= 80, background="darkgrey")
    name_label = tk.Label(frame_pic,text="Name ",font=('Arial',10,'bold'))
    name_label.grid(column=8,row=1,padx=10)
    label_about=Label(frame_pic, text="About ",font=('Arial',10,'bold'))
    label_about.grid(column=8,row=2,pady=2,padx=10)
    button_b_0.place(relx=0.15,rely=0.8)   
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
        
    button_view_note=tk.Button(frame_pic,
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
          
    button_rt_boost=tk.Button(frame_pic,
                  highlightcolor='WHITE',
                  text='Upload',
                  font=('Arial',12,'bold'),
                  command=Open_json            
                  )
    button_rt_boost.grid(column=11, row=2, padx=5,pady=5) 
    frame_pic.grid(row=4,column=0,rowspan=5, columnspan=4,pady=5)
    
    def Close_profile(event):
       frame_pic.destroy()
       button_b_0.place_forget() 
       Check_open.set(0)
       counter_dict.place_forget() 

    button_close=tk.Button(frame_pic, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=0, padx=5, columnspan=1) 
    frame3.place(relx=0.02,rely=0.12,relwidth=0.3,relheight=0.3)

button_beau_a=tk.Button(frame1, highlightcolor='WHITE',width=10,height=1,border=2, cursor='hand1',text='Account',font=('Arial',16,'bold'),command=Look_profile)
button_beau_a.place(relx=0.7,rely=0.1,relwidth=0.15)
frame1.pack(side=TOP,fill=X)
Check_raw =IntVar()

def raw_label():
   if Check_raw.get()==0:
        Check_raw.set(1)
        stuff_frame.place(relx=0.65,rely=0.12,relheight=0.75,relwidth=0.3)  
        r_tag.place(relx=0.7,rely=0.43,relwidth=0.1 )
        r_summary.place(relx=0.7,rely=0.47,relwidth=0.2 )
        r_button.place(relx=0.7,rely=0.52,relwidth=0.1)
        r_view.place(relx=0.85,rely=0.52)

        descr_tag.place(relx=0.7,rely=0.17,relwidth=0.1,relheight=0.1 )
        descr_summary.place(relx=0.7,rely=0.27,relwidth=0.2 )
        descr_button.place(relx=0.82,rely=0.2)
        descr_view.place(relx=0.7,rely=0.32,relwidth=0.23,relheight=0.1)

        d_button.place(relx=0.83,rely=0.59,relwidth=0.07)  
        d_tag.place(relx=0.75,rely=0.6 )
        d_title.place(relx=0.75,rely=0.65)

        d_view.place(relx=0.7,rely=0.7) 
   else:
      Check_raw.set(0)
      stuff_frame.place_forget() 
      r_tag.place_forget()
      r_summary.place_forget()
      r_button.place_forget()
      r_view.place_forget()

      descr_tag.place_forget()
      descr_summary.place_forget()
      descr_button.place_forget()
      descr_view.place_forget()

      d_button.place_forget()
      d_tag.place_forget()
      d_title.place_forget()

      d_view.place_forget()

lab_button = tk.Button(root, text="Raw Link", font=("Arial",12,"bold"), command=raw_label)
lab_button.place(relx=0.5,rely=0.01)
stuff_frame = ttk.LabelFrame(root, text="Stuff", labelanchor="n", padding=10)
d_tag = tk.Label(root, text="d-Tag",font=("Arial",12,"bold"))
d_title=ttk.Entry(root,justify='left',font=("Arial",12))
d_view = tk.Label(root, text="d-view ", font=("helvetica",13,"bold"),justify="center")
d_identifier=""

def d_tag_show():
    title=d_title.get()
    global d_identifier
    if title!="":
       if  codifica_spam()=="spam":
            d_identifier=title[8:]
            print(d_identifier)
            d_view.config(text=d_identifier[0:30]+"\n"+d_identifier[30:60]+"\n"+d_identifier[60:90])   
         
d_button = tk.Button(root, text="View d Tag", font=("Arial",12,"bold"), command=d_tag_show)
e_tag = tk.Label(root, text="e-Tag",font=("Arial",12,"bold"))
e_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12))
list_content=[]            

def r_show():
     r_tag_entry=r_summary.get()
     if r_tag_entry!="":
        if r_tag_entry not in list_content:
            list_content.append(r_tag_entry)
            r_view.config(text=str(len(list_content)))
            r_summary.delete(0, END)
        else:
             r_view.config(text="Enter a Content: " )         
             r_summary.delete(0, END)
     else:
            r_view.config(text="Uncorrect: ")             
            r_summary.delete(0, END)
       
r_tag = tk.Label(root, text="Content-Tag",font=("Arial",12,"bold"))
r_summary=ttk.Entry(root,justify='left',font=("Arial",12))
r_button = tk.Button(root, text="Content tag", font=("Arial",12,"bold"), command=r_show)
r_view = tk.Label(root, text="Content: ", font=("helvetica",13,"bold"),justify="center")

def show_descr():
    if len(list_title)<1:
     descr_entry=descr_summary.get()
     if descr_entry!="":
           if len(descr_entry)<105:
                
                descr_view.config(text=str(descr_entry[0:35]+"\n ")+ str(descr_entry[35:70]+"\n")+ str(descr_entry[70:105]))
           else:
            descr_view.config(text="Sorry, this is longer than a tweet: " + str(len(descr_entry))+"\n"+descr_entry[0:60])
                       
           def add_description():
             if len(list_title)<1:
              list_title.append(descr_summary.get())
              descr_view.config(text=str(len(list_title)))
              descr_summary.delete(0, END)
              add_button.place_forget()
             else:
               descr_summary.delete(0, END)
               add_button.place_forget()  

           add_button = tk.Button(root, text="Add", font=("Arial",12,"bold"), command=add_description)
           add_button.place(relx=0.91,rely=0.26) 
        
     else:
           
            if len(list_title)==1: 
                descr_view.config(text=str(len(list_title)))
            else:
                 descr_view.config(text="Uncorrect: ")                
            descr_summary.delete(0, END)
    else:
        descr_view.config(text=str(len(list_title)))
        descr_summary.delete(0, END)       
 
descr_tag = tk.Label(root, text="Title-Tag",font=("Arial",12,"bold"))
descr_summary=ttk.Entry(root,justify='left',font=("Arial",12))
descr_button = tk.Button(root, text="Preview ", font=("Arial",12,"bold"), command=show_descr)
descr_view = ttk.Label(root, text="Title: ", font=("helvetica",12,"bold"),justify='left')
entry_Home_title=ttk.Label(frame1,text="Speed Link", justify='left',font=("Arial",20,"bold"), background="darkgrey",border=2)
entry_Home_title.place(relx=0.35,rely=0.1,relwidth=0.2)
#Parse id in note
str_test=StringVar()
entry_note=ttk.Entry(root,justify='left', textvariable=str_test)
entry_note.place(relx=0.18,rely=0.6,relwidth=0.1, anchor="n")
List_note_write=[]
relay_list=[]

def reply_event():
     
  try:   
    event=entry_note.get()
    if event!="" and (len(event)==64 or len(event)==63):
    
     search_id=evnt_id(event)
     found_nota=asyncio.run(Get_id(search_id))
     nota=get_note(found_nota)
     print(nota[0])
     entry_note.delete(0, END) 
     return nota
    
    else:
       
        if event!="":
          event_hex=nevent_example(event) 
         
          if event_hex!=None:
         
            search_id=evnt_id(event_hex)
            found_nota=asyncio.run(Get_id(search_id))
            nota=get_note(found_nota)
            entry_note.delete(0, END) 
            print(nota[0])  #some sort of db_list to see the note
            return nota
         
  except NostrSdkError as e:
    print(e)     

async def get_list_Event(client, event_):
    tag_event=[]
    if event_!=[]:
     for event in event_:
       tag_event.append(EventId.parse(event))
     f = Filter().ids(tag_event)
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
     z = [event.as_json() for event in events.to_vec()]
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
       print(relay_list)
       for jrelay in relay_list:
          await client.add_relay(jrelay)
    else:
     await client.add_relay(" wss://nostr.mom/")
     await client.add_relay("wss://nos.lol/")
     await client.add_relay("wss://relay.primal.net")
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(event_, list):
      test_kind=await get_list_Event(client, event_)
    else:
        test_kind = await get_one_Event(client, event_)
    return test_kind

event_idone=Button(root,text="Search event one", font=('Arial',12,'normal'),command=reply_event ) 
event_idone.place(relx=0.18,rely=0.65,anchor='n' )
               
def rep_event_():
   if combo_lab.get()!= "Type of Hash-el":
    note=Open_sticky_note(combo_lab.get())   #tag
    if (note!=""or note!=[]) and note!=None:
     notes=[]
     for xnote in note:
        notes.append(xnote["id"])
     if __name__ == '__main__':
      test_print=get_note(asyncio.run(Get_id(notes)))
      if test_print!=[]:
       for event_x in test_print:
          List_note_write.append(event_x)
       
       def return_note():
          re_view_note()
       
       button_rep_1=tk.Button(root,text="read note", background="darkgrey", command=return_note, font=('Arial',12,'normal'))
       button_rep_1.place(relx=0.3,rely=0.45)   
       
       def close_read():
          button_rep_1.place_forget()
          button_close.place_forget()

       button_close=Button(root, command=close_read, text="Close X",font=('Arial',12,'normal'))
       button_close.place(relx=0.38, rely=0.45) 

      else:
        messagebox.showerror("Fail", "List, is empty")
    else:
      messagebox.showerror("Fail", "Error, not line")
      
button_rep=tk.Button(root,text="Search Note", background="darkgrey", command=rep_event_, font=('Arial',12,'normal'))
button_rep.place(relx=0.13,rely=0.45)

def re_view_note():
      
        frame1=Frame(root)
        canvas = tk.Canvas(frame1,width=330)
        scrollbar = ttk.Scrollbar(frame1, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas,border=2)

        scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
        scrollregion=canvas.bbox("all") ))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        int_var=IntVar()
        lbel_var=Entry(root, textvariable=int_var,font=("Arial",12,"bold"),background="grey") 
        s = 0

        def share(note_to_print):
           print(note_to_print["content"])
        
        def create_note(note_text, s):
           
           string_note=StringVar()
           if note_text["kind"]==int(1):
            string_note.set("id "+str(note_text["id"])+"\n"+"Content " +"\n"+note_text["content"])
           if note_text["kind"]==int(7):   
            string_note.set(str(note_text["kind"]) +"\n"+note_text["content"]+"\n"+ "refer to "+ tags_string(note_text,"e")[0])   
           if note_text["kind"]==int(30023):
            string_note.set("id "+str(note_text["id"])+"\n"+"Article " +"\n"+tags_string(note_text,"title")[0])          
           else:
            
            string_note.set("id "+str(note_text["id"])+"\n"+"Content " +"\n"+note_text["content"])
           message = Message(scrollable_frame, textvariable= string_note, width=320, font=('Arial',12,'normal'))
           message.grid(row=s, column=0, columnspan=3, padx=5,pady=5)
           test_1 = tk.Button(scrollable_frame, text="Print Note", command=lambda: share(note_text))
           test_1.grid(row=s + 1, column=2,pady=5)
                   
        z=0
         
        if List_note_write!=[]:
            
            def open_feed(): 
               s=1
               
               list_note=List_note_write
               create_note(list_note[int(lbel_var.get())], s)
               root.update_idletasks()
                            
               s += 2   

            z=z+1        
            button_open=Button(scrollable_frame, command=open_feed, text="see Note",font=('Arial',12,'normal'))
            button_open.grid(column=2,row=0,pady=5,padx=5)  
               
        else:
           print("the list is empty")    
        canvas.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")  
        frame1.place(relx=0.3,rely=0.3, relheight=0.3,relwidth=0.35)  
        
        def close_canvas():
            scrollable_frame.forget()
            canvas.destroy()
            frame1.destroy()
            button_next.place_forget()
            button_back.place_forget()
            lbel_var.place_forget()

        def note_number():
    
            if int((int(lbel_var.get())+1))< len(List_note_write):
       
                int_var.set(int(lbel_var.get())+1)
                open_feed()
            else:
                int_var.set(int(0)) 
                open_feed()

        def back_number():
    
            if int((int(lbel_var.get())-1))>=0:
      
                int_var.set(int(lbel_var.get())-1)
                open_feed()
            else:
                int_var.set(len(List_note_write)-1) 
                open_feed()

        lbel_var.place(relx=0.27,rely=0.35, anchor="n",relwidth=0.02)
        button_next=Button(root,command=note_number,text=" Next ",font=("Arial",12,"bold"))
        button_next.place(relx=0.27,rely=0.4, anchor="n")
        button_back=Button(root,command=back_number,text=" Back ",font=("Arial",12,"bold"))
        button_back.place(relx=0.27,rely=0.5, anchor="n",x=1)
        button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal'))
        button_close.grid(column=1,row=0,pady=5,padx=10) 

def metadata_stress():
    if Check_open.get()==0:
       Check_open.set(1)
       text=""
       for meta in Metadata_dict:
        if meta=="picture":    
         text=text+str(meta)+str(": ")+str(Metadata_dict[meta][0:25]) +"\n"
        else:
            text=text+str(meta)+str(": ")+str(Metadata_dict[meta]) +"\n"
       counter_dict['text']=text
       counter_dict.place(relx=0.75,rely=0.77)  
       
    else:
         Check_open.set(0)
         counter_dict.place_forget() 

button_b_0=tk.Button(root,text='Profile',font=('Arial',12,'normal'),command=metadata_stress)
counter_dict=Label(root,text="count",font=('Arial',12,'bold'))
frame2=tk.Frame(root,height=100,width=200)
frame3=tk.Frame(root,height=100,width=200)

def open_relay():
    frame_account=tk.Frame(frame2, background="darkgrey")
    structure_relay = tk.Label(frame_account, text="relay",font=("Arial",12,"bold"))
    entry_relay=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"))
    structure_relay.grid(column=11, row=1, padx=5,pady=5) 
    button_beau.destroy()
    
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

    relay_button = tk.Button(frame_account, text="Check!", font=("Arial",12,"normal"),background="grey", command=relay_class)
    counter_relay=Label(frame_account,text="count")
    entry_relay.grid(column=11, row=2, padx=10,pady=5)
    relay_button.grid(column=12, row=2, padx=10,pady=5)

    def Close_profile(event):
       frame_account.destroy()
       button_beau=tk.Button(root, 
                  highlightcolor='WHITE',
                  text='Relay',
                  font=('Arial',12,'bold'),
                  command=open_relay            
                  )
       button_beau.place(relx=0.45,rely=0.8) 
        
    button_close=tk.Button(frame_account, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=0, padx=5, columnspan=1) 

    def on_server(event):
       label_relay["text"] = combo_bo_r.get()[6:]
       
    label_relay = tk.Label(frame_account, text="Name relay",font=('Arial',12,'bold'))
    label_relay.grid(column=13,row=3,pady=5)
    combo_bo_r = ttk.Combobox(frame_account, font=('Arial',12,'normal'))
    combo_bo_r.grid(column=13,row=2,pady=5)
    combo_bo_r.set("Relays set")
    combo_bo_r.bind("<<ComboboxSelected>>", on_server)
    frame_account.grid(row=1,column=0,rowspan=2, columnspan=4,pady=5)
    frame2.place(relx=0.23,rely=0.75,relwidth=0.42,relheight=0.3)

button_beau=tk.Button(root,  highlightcolor='WHITE',text='Relay',font=('Arial',12,'bold'),command=open_relay )
button_beau.place(relx=0.45,rely=0.8) 

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

Metadata_dict={}
List_note_write=[]

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