from nostr_sdk import *
import asyncio
from datetime import timedelta
from nostr_sdk import PublicKey
from nostr_sdk import Tag
from nostr_sdk import EventId,Event
import time
from datetime import datetime
import uuid
import tkinter as tk
from tkinter import *
from tkinter import ttk
import json
import io
from tkinter.filedialog import askopenfilename
import requests
import shutil
from PIL import Image, ImageTk
from tkinter import messagebox 
from cryptography.fernet import Fernet

root = tk.Tk()
root.title("Wiki Example")
root.geometry("1250x800")
root.iconphoto(False, tk.PhotoImage(file="nòph.png"))

def OpenFile():
    entry4.delete("1.0","end")
    name = askopenfilename()
    if name!="":
     f = io.open(name, mode="r", encoding="utf-8")
     for j in name.split():
      if j[-5:]==".adoc": 
       print_label.config(text="ok",font=("Arial",12,"bold"),foreground="black")
       error_label.config(text="ok")
       test=f.readlines()
       if len(test)>20:
        for j in test:
         entry4.insert(END,j+"\n")
       else:
           error_label.config(text="Error lenght of Article")
           print_label.config(text="Error! ", font=("Arial",12,"bold"),foreground="blue")  
      else:
        error_label.config(text="Error the extension is "+ j[-5:]+"\n"+"try extension adoc")
        print_label.config(text="Error! ", font=("Arial",12,"bold"),foreground="red")
     f.close()   
    else:    
         error_label.config(text="Insert an Article")
         print_label.config(text="Error! ", font=("Arial",12,"bold"),foreground="black")

note_tag = tk.Label(root, text="Note from the file: ",font=("Arial",12,"bold"))
note_tag.place(relx=0.5,rely=0.12,relwidth=0.2,relheight=0.1,anchor='n' )

async def new_entry_wiki(note,tag):
   # Init logger
   init_logger(LogLevel.INFO)
   key_string=log_these_key()
   if key_string!=None: 
    keys = Keys.parse(key_string)
    signer = NostrSigner.keys(keys)
    
    client = Client(signer)
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(jrelay)
       await client.connect()
    
    builder = EventBuilder(Kind(30818),note).tags(tag)
    testNote= await client.send_event_builder(builder)
    
    messagebox.showinfo("Result",str(testNote.failed.keys)+"\n"+str(testNote.success))
    write_json_fake_note(d_identifier+"-wiki",testNote.id.to_hex())
    metadata = metadata_get()
    if metadata:
     await client.set_metadata(metadata)

def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def wiki_form():
   check_square()
   if button_entry1.cget('foreground')=="green":
    title=entry_title.get()
    summary=entry_summary.get()
    image=entry_image.get()
    tags=Tag.custom(TagKind.SUMMARY(), [summary]),Tag.custom(TagKind.TITLE(), [title]),Tag.identifier(d_identifier),Tag.custom(TagKind.IMAGE(), [image])   #Tag.custom
    note=entry4.get(1.0, "end-1c")
       
    if __name__ == '__main__':
     note=entry4.get(1.0, "end-1c")
     tag=tags
     asyncio.run(new_entry_wiki(note,tag))
     entry4.delete("1.0","end")
     entry_title.delete(0, END)
     entry_summary.delete(0, END)
     entry_image.delete(0,END)
     d_title.delete(0, END)
     button_entry1.config(text="■",foreground="grey")
     
   else:
       print("error")
       check_square() 

def check_square():
    Text=entry4.get(1.0, "end-1c")
    if Text!="":
       if len(Text)<200:
           button_entry1.config(text="■",foreground="grey")
           error_label.config(text="Error lenght of Article")
           print_label.config(text="Error! ", font=("Arial",12,"bold"),foreground="blue")  
    
       else:
            if d_identifier!="":
                button_entry1.config(text="■",foreground="green")
                error_label.config(text="ok")
                print_label.config(text="ok! ", font=("Arial",12,"bold"),foreground="blue")  
         
                if entry_title.get()!="":
                    button_entry1.config(text="■",foreground="green")
                    error_label.config(text="ok")
                    print_label.config(text="ok! ", font=("Arial",12,"bold"),foreground="blue")  
                else:
                  button_entry1.config(text="■",foreground="green")
                  error_label.config(text="ok, no title")
                  print_label.config(text="ok! ", font=("Arial",12,"bold"),foreground="blue")
          
                #image_call()
                
            else:
                button_entry1.config(text="■",foreground="grey")
                error_label.config(text="Error insert a d-identifier")
                print_label.config(text="Error! ", font=("Arial",12,"bold"),foreground="blue")  
  
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for the article", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")
        
entry4=tk.Text(root,border=2,highlightbackground="grey")
entry4.place(relx=0.5,rely=0.2,relwidth=0.3,relheight=0.4,anchor='n' )
button_send=tk.Button(root,text="Send wiki form",command=wiki_form, background="darkgrey",font=("Arial",14,"bold"))
button_send.place(relx=0.525,rely=0.65,relwidth=0.15,relheight=0.1,anchor='n' )
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
button_entry1.place(relx=0.62,rely=0.65,relwidth=0.05, relheight=0.1,anchor="n" )
frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
button_import=tk.Button(frame1,text="Import article",command=OpenFile,font=("Arial",12,),background="grey",highlightcolor='WHITE')
button_import.grid(column=2, row=1,padx=10,pady=5,ipadx=1,ipady=1)
error_label = tk.Label(frame1, text="Problem:",font=("Arial",12))
error_label.grid(column=3, rowspan=2, row=0, pady=5)
print_label = ttk.Label(frame1, text="Wait for the article",font=("Arial",12))
print_label.grid(column=3, columnspan=2, row=2, pady=5)
frame1.pack(side=TOP,fill=X)
title_tag = tk.Label(root, text="Title-Tag",font=("Arial",12,"bold"))  #entry_layout-right
title_tag.place(relx=0.7,rely=0.15,relwidth=0.1,relheight=0.1 )
entry_title=ttk.Entry(root,justify='left',font=("Arial",12))
entry_title.place(relx=0.7,rely=0.25,relwidth=0.2)
d_tag = tk.Label(root, text="d-Tag",font=("Arial",12,"bold"))
d_tag.place(relx=0.75,rely=0.8 )
d_title=ttk.Entry(root,justify='left',font=("Arial",12))
d_title.place(relx=0.75,rely=0.85)
d_view = tk.Label(root, text="d-view ", font=("helvetica",13,"bold"),justify="center")
d_identifier=""

def d_tag_show():
    title=d_title.get()
    if title!="":
        test=title.lower()
        i=0
        while i <len(test):
         if test[i]==" ":
            name=test[0:i]+"-"
            test=name+test[i+1:]
         i=i+1
        global d_identifier 
        d_identifier=test
        print(d_identifier)
        d_view.place(relx=0.7,rely=0.9,relwidth=0.3,bordermode=INSIDE)
        d_view.config(text=test,padx=5)            

d_button = tk.Button(root, text="View d Tag", font=("Arial",12,"bold"), command=d_tag_show)
d_button.place(relx=0.82,rely=0.79,relwidth=0.08)        

def title_show():
    title=entry_title.get()
    if title!="":
        if len(title)<60:
         title_view.config(text=title[0:30] +"\n"+ title[30:60])
        else:
            title_view.config(text="the lengh is over: " + str(len(title))) 
    else:
          title_view.config(text="Enter a title: " )       

def summary_show():
    summary=entry_summary.get()
    if summary!="":
        if len(summary)<140:
         summary_view.config(text=summary[0:35] +"\n"+ summary[35:70]+"\n"+ summary[70:105]+"\n"+ summary[105:140])
        else:
            summary_view.config(text="Sorry, this is longer than a tweet: " + str(len(summary))+"\n"+summary[0:35] +"\n"+ summary[35:70]+"\n"+ summary[70:105]+"\n"+ summary[105:140])
    else:
          summary_view.config(text="Enter a Summary: " )            

title_button = tk.Button(root, text="view_Title", font=("Arial",12,"bold"), command=title_show)
title_button.place(relx=0.7,rely=0.30,relwidth=0.07)
title_view = tk.Label(root, text="view?: ", font=("Arial",12))
title_view.place(relx=0.77,rely=0.30,relwidth=0.2 )
sumamry_tag = tk.Label(root, text="summary-Tag",font=("Arial",12,"bold"))
sumamry_tag.place(relx=0.7,rely=0.35,relwidth=0.1,relheight=0.1 )
entry_summary=ttk.Entry(root,justify='left',font=("Arial",12))
entry_summary.place(relx=0.7,rely=0.45,relwidth=0.2 )
summary_button = tk.Button(root, text="view_Summary", font=("Arial",12,"bold"), command=summary_show)
summary_button.place(relx=0.8,rely=0.50,relwidth=0.1)
summary_view = tk.Label(root, text="Summary: ", font=("helvetica",13,"bold"),justify="center")
summary_view.place(relx=0.69,rely=0.58,relwidth=0.3)
wall=tk.Button(root, text="",background="lightgrey")
wall.place(relx=0.70,rely=0.58,relheight=0.13,width=5, height=13)
wall2=tk.Button(root, text="",background="lightgrey")
wall2.place(relx=0.70,rely=0.725,relwidth=0.23, height=5)

def url_link():
 z=entry_image.get()
 for j in z.split():
    if j[0:5]=="https":
        return str(j)

def codifica_link():
   f=url_link()
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

def image_call():
 
 image=codifica_link()
 if image=="pic":
  item=entry_image.get()
  image_check.config(text="Ok, " + str(image))
 else:
     if entry_image.get()=="":
      pass
     else:
        entry_image.delete(0, END)
        image_check.config(text="No, " + str(image)) 

image_label = tk.Label(root)
image_label.place(relx=0.55,rely=0.77,relheight=0.22,relwidth=0.3, anchor="n" )

def photo_print():
  image=codifica_link()
  if image=="pic":
        response = requests.get(entry_image.get(), stream=True)
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        image = Image.open('my_image.png')
        image.thumbnail((250, 200))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image_names= photo
        def close_image():
           button_lose.place_forget()
           image_label.config(image="")
           entry_image.delete(0, END)
        button_lose=Button(root,command=close_image,text="X",font=("Arial",12,"bold"))
        button_lose.place(relx=0.62,rely=0.77,relwidth=0.05) 
  
button_print=Button(root,command=photo_print,text="Photo",font=("Arial",12,"bold"))
button_print.place(relx=0.25,rely=0.5,relwidth=0.05) 
image_tag = tk.Label(root, text="Image-Tag", font=("Arial",12,"bold"))
image_tag.place(relx=0.1,rely=0.4,relwidth=0.1 )
entry_image=ttk.Entry(root,justify='left')
entry_image.place(relx=0.02,rely=0.56,relwidth=0.28)
image_button = tk.Button(root, text="Check", font=("Arial",12,"bold"), command=image_call)
image_button.place(relx=0.02,rely=0.5,relwidth=0.05 )
image_check = tk.Label(root, text="Check?: ", font=("Arial",12,"bold"))
image_check.place(relx=0.12,rely=0.51,relwidth=0.1 )
entry_note=ttk.Label(frame1,text="Wekiwi", justify='left',font=("Arial",20,"bold"), background="darkgrey",border=2)
entry_note.place(relx=0.4,rely=0.05,relwidth=0.2)

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

Metadata_dict={}
List_note_write=[]
relay_list=[]
frame2=tk.Frame(root,height=100,width=200)
frame3=tk.Frame(root,height=100,width=200)
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
    
def Look_profile():
    frame_pic=tk.Frame(frame3,height=20,width= 80, background="darkgrey")
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
        
    button_view_note=tk.Button(frame_pic, highlightcolor='WHITE',text='Save!',font=('Arial',12,'bold'),command=call_profile_)
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
                Metadata_dict["name"]=label_name.get()
                Metadata_dict["about"]=label_about.get()
                Metadata_dict["display_name"]=label_name.get()
                Metadata_dict["picture"]=label_pic.get()
                s=1
                for xvalues in list(Metadata_dict.values()):
                 if xvalues=="":
                    if s==4:
                        messagebox.showerror("No metadata", "Please insert \n something")
                        return None
                    else:
                        s=s+1
          
    button_rt_boost=tk.Button(frame_pic, 
                  highlightcolor='WHITE',
                  text='Upload',
                  font=('Arial',12,'bold'),
                  command=Open_json)
    button_rt_boost.grid(column=11, row=2, padx=5,pady=5) 
    frame_pic.grid(row=4,column=0,rowspan=5, columnspan=4,pady=5)
    
    def Close_profile(event):
       frame_pic.destroy()
        
    button_close=tk.Button(frame_pic, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=0, padx=5, columnspan=1) 

button_b0=tk.Button(root, 
                  highlightcolor='WHITE',
                  width=10,border=2, cursor='hand1',
                  text='Account',
                  font=('Arial',16,'bold'),
                  command=Look_profile)
button_b0.place(relx=0.7,rely=0.01,relwidth=0.1)

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

Check_open =IntVar()
button_b0=tk.Button(root, 
                  highlightcolor='WHITE',
                  width=10,border=2, cursor='hand1',
                  text='Profile',
                  font=('Arial',12,'normal'),
                  command=metadata_stress)

button_b0.place(relx=0.5,rely=0.8,relwidth=0.1)   
counter_dict=Label(root,text="count",font=('Arial',12,'bold'))
          
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
          upload_relay_list("wiki_relay")  
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
                  command=open_relay)
       button_beau.place(relx=0.1,rely=0.12) 
       
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

button_beau=tk.Button(root, 
                  highlightcolor='WHITE',
                  text='Relay',
                  font=('Arial',12,'bold'),
                  command=open_relay)
button_beau.place(relx=0.1,rely=0.12) 

def write_json_relay(name,note_text):
       with open(name+".txt", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text))

def download_file_relay():
    if relay_list!=[]:
     write_json_relay("wiki_relay",relay_list)
    #message_box      

def upload_relay_list(name):
   try: 
    with open(name+".txt", 'r',encoding="utf-8") as file:
        global relay_list 
        new_relay=file.read()
        new_relay = json.loads(new_relay.replace("'", '"'))
        
        for jrelay in new_relay:
         if jrelay!="":
          if jrelay[0:6]=="wss://" and jrelay[-1]=="/":
           
            if jrelay not in relay_list:
                relay_list.append(jrelay)
   except FileNotFoundError as e:
      print(e)
      
button_dwn=tk.Button(root, 
                  highlightcolor='WHITE',
                  text='⏬ Relays',
                  font=('Arial',12,'bold'),
                  command=download_file_relay          
                  )

button_dwn.place(relx=0.15,rely=0.12)
frame2.place(relx=0.01,rely=0.62,relwidth=0.42,relheight=0.3)
frame3.place(relx=0.02,rely=0.18,relwidth=0.3,relheight=0.3)

root.mainloop()

#fork session
root = tk.Tk()
root.geometry("1250x800")

def since_day(number):
    import datetime
    import calendar
    date = datetime.date.today() - datetime.timedelta(days=number)
    t = datetime.datetime.combine(date, datetime.time(1, 2, 1))
    z=calendar.timegm(t.timetuple())
    return z

def return_date_tm(note):
    import datetime
    date_2= datetime.datetime.fromtimestamp(float(note["created_at"])).strftime("%a"+", "+"%d "+"%b"+" %Y")
    date= date_2+ " "+ datetime.datetime.fromtimestamp(float(note["created_at"])).strftime('%H:%M')
   
    return date

Checkbutton5 = IntVar() 
frame_time=tk.Frame(root,height=100,width=200)

def five_event():
     if Checkbutton5.get() == 0:
        Button5.config(text= " 60 day")
        frame_time.grid_forget()
        
     else:
       
        Button5.config(text= "Time")
        frame_time.grid(column=0,row=5, columnspan=9,rowspan=3)

frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
Button5 = Checkbutton(frame1, text = "60 day", variable = Checkbutton5, onvalue = 1, offvalue = 0, height = 2, width = 10,font=('Arial',16,'normal'),command=five_event)
Button5.grid(column=0, row=0,rowspan=3,padx=10)     
since_variable=IntVar(value=1)
since_entry=Entry(frame_time,textvariable=since_variable,font=("Arial",12,"normal"),width=5)
until_variable=IntVar()
until_entry=Entry(frame_time,textvariable=until_variable,font=("Arial",12,"normal"),width=5)

def next_since():
   since_variable.set(int(since_entry.get()) + 1)

def back_since():
   if int(since_entry.get())- 1<1:
      since_variable.set(int(1))
   else:
    if int(since_entry.get())- 1==int(until_entry.get()):
       since_variable.set(since_entry.get())
    else:   
     since_variable.set(int(since_entry.get())- 1)   

def next_until():
   if int(until_entry.get()) + 1>=int(since_entry.get()):
       until_variable.set(until_entry.get())
   else:    
    until_variable.set(int(until_entry.get()) + 1)

def back_until():
   if int(until_entry.get())- 1<0:
      until_variable.set(0)
   else:
    until_variable.set(int(until_entry.get())- 1) 

wall_2=tk.Label(frame_time, text="",background="lightgrey",height=4)
label_since=Label(frame_time,text="day since",font=("Arial",12,"normal"))
button_mov=tk.Button(frame_time,text="➕",command=next_since)   
button_back=tk.Button(frame_time,text="➖",command=back_since)  

label_until=Label(frame_time,text="day until",font=("Arial",12,"normal"))
label_until.grid(column=6,row=5,pady=10)
button_mov_dep=tk.Button(frame_time,text="➕",command= next_until)       
button_mov_dep.grid(column=7, row=5,padx=5,pady=5)
button_back_dep=tk.Button(frame_time,text="➖",command=back_until)       
button_back_dep.grid(column=7, row=6,padx=5,pady=5)

since_entry.grid(column=1,row=6,pady=10,padx=10)
until_entry.grid(column=6,row=6,pady=10)
wall_2.grid(column=0, row=5,pady=5, rowspan=2)

label_since.grid(column=1,row=5,pady=10)    
button_mov.grid(column=2, row=5,padx=5,pady=5)     
button_back.grid(column=2, row=6,padx=5,pady=5)
        
entry_variable=StringVar()
entry_var=Entry(root, textvariable=entry_variable,font=("Arial",12,"bold"),width=15)
entry_var.place(relx=0.35,rely=0.25)

frame1.grid(column=5,columnspan=11, row=0, rowspan=3)


async def get_result_w(client):
    if Checkbutton5.get() == 1:
          f = Filter().identifier(entry_var.get()).kind(Kind(30818)).since(timestamp=Timestamp.from_secs(since_day(int(since_entry.get())))).until(timestamp=Timestamp.from_secs(since_day(int(until_entry.get())))).limit(10)
    else:
           f = Filter().identifier(entry_var.get()).kind(Kind(30818)).since(timestamp=Timestamp.from_secs(since_day(int(60)))).until(timestamp=Timestamp.from_secs(since_day(int(0)))).limit(10)

    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

db_list_note=[]
relay_search_list=[]

async def Search_d_tag():
    # Init logger
    init_logger(LogLevel.INFO)
    client = Client(None)
    # Add relays and connect
    if relay_search_list!=[]:
       for jrelay in relay_search_list:
          await client.add_relay(jrelay)
       await client.connect()
       await asyncio.sleep(2.0)

       combined_results = await get_result_w(client)
       return combined_results
     
    await search_box_relay()
    print("found ", len(relay_search_list), " relays")

def call_text():
  if entry_var.get()!="":
   if __name__ == "__main__":
    response=asyncio.run(Search_d_tag())
    if response:

     note_=get_note(response)
     for jnote in note_:
       if jnote not in db_list_note:
          db_list_note.append(jnote)
       if len(jnote["content"])<800:
          second_label10.insert(END,jnote["content"])
       else:
             second_label10.insert(END,jnote["tags"])
       second_label10.insert(END,"\n"+"____________________"+"\n")
       second_label10.insert(END,"\n"+"\n")

    else:
       print("empty")
  else:     
       if relay_search_list==[]:
          if __name__ == "__main__":
            response=asyncio.run(Search_d_tag())
          if len(relay_search_list)>0:
             button_close_search["text"]="Search 🔍"

public_list=[]
label_d_search=tk.Label(root, text='d Tag',font=('Arial',12,'bold'))    
label_d_search.place(relx=0.38,rely=0.21 ) 
button_close_search=tk.Button(root, text='Search Relay',font=('Arial',12,'bold'), command=call_text)    
button_close_search.place(relx=0.48,rely=0.24 ) 

async def get_search_relay(client):
   if public_list!=[]:
    f=Filter().authors(public_list).kind(Kind(10007))
   else: 
    f=Filter().kind(Kind(10007)).limit(10)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec()]
   return z

async def search_box_relay():
        
    client = Client(None)
    
    if relay_list!=[]:
       
       for jrelay in relay_list:
          await client.add_relay(jrelay)
             
    else:
       await client.add_relay("wss://nostr.mom/")
       
    await client.connect()
    relay_add=get_note(await get_search_relay(client))
    if relay_add !=None and relay_add!=[]:
           i=0
           while i<len(relay_add):
            for xrelay in tags_string(relay_add[i],'relay'):
              if xrelay[0:6]=="wss://" and xrelay[-1]=="/" and xrelay not in Bad_relay_connection:
               if xrelay not in relay_search_list:
                relay_search_list.append(xrelay) 
              
            i=i+1             
    
relay_search_list=[]
Bad_relay_connection=["wss://relay.noswhere.com/","wss://relay.purplestr.com/"]
scroll_bar_mini = tk.Scrollbar(frame1)
scroll_bar_mini.grid( sticky = NS,column=4,row=0,rowspan=3)
second_label10 = tk.Text(frame1, padx=10, height=5, width=25, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'))
scroll_bar_mini.config( command = second_label10.yview )
second_label10.grid(padx=10, column=1, columnspan=3, row=0, rowspan=3) 


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
        context1="Content lenght "+str(len(note["content"]))+"\n"+"kind "+str(note["kind"])+"\n"
        context2="\n"
        if tags_string(note,"title")!=[]: 
         xnote= "Title: "+str(tags_string(note,"title")[0])
         context2=context2+str(xnote) +"\n"
        else: 
         context1="there is no Title"+ " kind "+str(note["kind"])
         context2=""
        if tags_string(note,"summary")!=[] and str(tags_string(note,"summary")[0])!="": 
          xnote= "\n"+"Summary: "+str(tags_string(note,"summary")[0])
          context2=context2+str(xnote) +"\n"
      else:
          context1="no tags"+ " kind "+str(note["kind"])
          context2=""   
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0+context1+context2)
      label_id.grid(pady=2,column=0, columnspan=3)

      def print_id(entry):
           
           number=list(db_list_note).index(entry)
           print(number)
           show_print_test(entry)     

      def print_fork(entry):
         number=list(db_list_note).index(entry)
         print(number)
         show_fork_test(entry)       
                          
      def print_var(entry):
                print(entry["content"])
                          
      button=Button(scrollable_frame_1,text=f"Print me!", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"fork it!", command=lambda val=note: print_fork(val))
      button_grid2.grid(row=s,column=2,padx=5,pady=5) 
      button_grid3=Button(scrollable_frame_1,text=f"click to read!", command=lambda val=note: print_id(val))
      button_grid3.grid(row=s,column=1,padx=5,pady=5)      
   
      s=s+2  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.35,rely=0.3,relwidth=0.30,relheight=0.4)
    
    def close_number() -> None :
        frame2.destroy()    
        button_f_close.place_forget()
        
    button_f_close=Button(root,command=close_number,text=" ❌ ",font=("Arial",12,"normal"),fg="red")
    button_f_close.place(relx=0.58,rely=0.24)      
       
 s=1
 create_page(db_list_note, s)
 root.update_idletasks()

frame_3=tk.Frame(root,height=20,width=80) 
frame_id=tk.Frame(frame_3,height=30,width= 100)  
frame_T=tk.Frame(frame_3,height=20,width= 30)      
button_id=tk.Button(root,command=show_Teed,text="Go Result")
button_id.place(relx=0.28,rely=0.25)
frame_T.grid(column=0, row=1, columnspan=2)
frame_id.grid(column=2, row=1, columnspan=4, rowspan=3)
frame_3.grid()

def show_fork_test(note):
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
   s=1
   
   scroll_bar_f = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_f.grid( sticky = NS,column=4,row=0,rowspan=3)
   second_labelf = tk.Text(scrollable_frame_2, padx=2, height=5, width=30, yscrollcommand = scroll_bar_f.set, font=('Arial',12,'bold'))
   scroll_bar_f.config( command = second_labelf.yview )
   second_labelf.insert(END,note["content"],str)
   second_labelf.grid(padx=2, column=0, columnspan=3, row=0) 
   context0="npub: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
   if note['tags']!=[]:
        if tags_string(note,"title")!=[]: 
            context1 = "\n"+"Title: "+str(tags_string(note,"title")[0])
        
            context2="\n"+"d: "+str(tags_string(note,"d")[0])
   else: 
        context1="content: "+"\n"+note['content']+"\n"
        context2=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=320,font=("Arial",12,"normal"))
   var_id.set(context0+context1+context2)
   label_id.grid(pady=2,column=0, columnspan=3)
      
   def print_zap(entry):
           if button_grid2.cget('foreground')=="green":  
             if second_labelf.get()!="":
               
               asyncio.run(new_entry_wiki(second_labelf.get(),fork_note(entry)))
               #Messagebox close
               button_grid2.config(fg="")

   def print_var(entry):
            print(fork_note(entry))
            global d_identifier
            d_identifier=url_uid
            button_grid2.config(fg="green")

   def print_content(entry):
      reply_re_action(entry)
                  
   button=Button(scrollable_frame_2,text=f"fork test!", command=lambda val=note: print_var(val))
   button.grid(row=s,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text="Send event", command=lambda val=note: print_zap(val))
   button_grid2.grid(row=s,column=1,padx=5,pady=5)
   button_grid3=Button(scrollable_frame_2,text=f"like this!", command=lambda val=note: print_content(val))
   button_grid3.grid(row=s,column=2,padx=5,pady=5)    
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()  
     button_frame.place_forget()

   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.9,rely=0.16)
   frame3.place(relx=0.65,rely=0.22,relwidth=0.33,relheight=0.4 ) 

def reply_re_action(note):
  
   test = EventId.parse(note["id"])
   public_key=convert_user(note["pubkey"])
   if __name__ == '__main__':
    note_rea="+"
    type_event=Kind(int(note["kind"]))
    asyncio.run(reply_reaction(test,public_key,note_rea,type_event))    

async def reply_reaction(event_id,public_key,str_reaction,type_event):
   key_string=log_these_key()
   if key_string!=None: 
    keys = Keys.parse(key_string)
    
    signer = NostrSigner.keys(keys)
    
    client = Client(signer)
    # Add relays and connect
    await client.add_relay("wss://nostr.mom")
    await client.add_relay("wss://nos.lol")
    await client.connect()

    # Send an event using the Nostr Signer
    builder = EventBuilder.reaction_extended(event_id,public_key,str_reaction,type_event)
    test_note=await client.send_event_builder(builder)
    print("this relay is going good", test_note.success, "\n", "this relay is bad",test_note.failed)

def show_print_test(note):
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
   s=1
   context0="npub: "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
   if note['tags']!=[]:
        if tags_string(note,"title")!=[]: 
         xnote= "\n"+"Title: "+str(tags_string(note,"title")[0])
         context1=xnote+"\n"+"\n"+note['content']+"\n"
        else: 
            context1="\n"+note['content']+"\n" 
        context2="[-[-[Tags]-]-]"+"\n"+str((note)["tags"])
   else: 
        context1="content: "+"\n"+note['content']+"\n"
        context2=""
           
   var_id=StringVar()
   label_id = Message(scrollable_frame_2,textvariable=var_id, relief=RAISED,width=360,font=("Arial",12,"normal"))
   var_id.set(context0+context1+context2)
   label_id.grid(pady=2,column=0, columnspan=3)
      
   def print_tags(entry):
            print(entry["tags"])
            

   def print_var(entry):
            print(entry["id"])

   def print_content(entry):
       result=show_note_from_id(entry)
       if result!=None: 
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             context00="npub: "+jresult['pubkey']+"\n"+"id: "+jresult["id"]+"\n"
             if jresult['tags']!=[]:
              context11="content: "+"\n"+jresult['content']+"\n"
              context22="[-[-[Tags]-]-]"+"\n"+str((jresult)["tags"])
             else: 
              context11="content: "+"\n"+jresult['content']+"\n"
              context22=""
             var_id_1=StringVar()
             label_id_1 = Message(scrollable_frame_2,textvariable=var_id_1, relief=RAISED,width=310,font=("Arial",12,"normal"))
             var_id_1.set(context00+context11+context22)
             label_id_1.grid(pady=2,column=0, columnspan=3)
                   
   button=Button(scrollable_frame_2,text=f"id!", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s,padx=5,pady=5)
   button_grid3=Button(scrollable_frame_2,text=f"Tags!", command=lambda val=note: print_tags(val))
   button_grid3.grid(row=s,column=1,padx=5,pady=5) 
   button_grid3=Button(scrollable_frame_2,text=f"this a reply!", command=lambda val=note: print_content(val))
   button_grid3.grid(row=s,column=2,padx=5,pady=5)    
   scrollbar_2.pack(side="right", fill="y",pady=20) 
   canvas_2.pack( fill="y", expand=True)
   
   def close_frame():
     frame3.destroy()  
     button_frame.place_forget()

   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.9,rely=0.16)
   frame3.place(relx=0.65,rely=0.22,relwidth=0.33,relheight=0.4 ) 

def db_list_id(json_list):
    db_list_with_id=[]
    for json_z in json_list:
        if json_z["id"] not in db_list_with_id:
          db_list_with_id.append(json_z["id"]) 
    return db_list_with_id       

def db_list_nota(nota_id):
    #global list
    for nota_x in db_list:
        if nota_x["id"]==nota_id:
            return nota_x

def show_note_from_id(note):
        result=note["id"]
        quote_e=nota_reply_id(note)
        
        replay_light=[]
        db_already=[]
        items=[]
        if quote_e!=[]:
           for replay_x in quote_e:
               if replay_x not in db_list_id(db_list):
                  replay_light.append(replay_x) 
               else:
                   db_already.append(replay_x)
           if replay_light!=[]:          
            items=get_note(asyncio.run(Get_event_id(replay_light)))
           if db_already!=[]:
               for db_x in db_already:
                   if db_x  in db_list_id(db_list):
                    items.append(db_list_nota(db_x)) 
        else:
            print("quote_e empty")
            items=get_note(asyncio.run(Get_event_id(result)))
             
        for itemsj in items:
            if itemsj not in db_list:
                db_list.append(itemsj)   
        return items   

def nota_reply_id(nota):
    e_id=[]
    if tags_string(nota,'e')!=[]:
            for event_id in tags_string(nota,'e'):
                  if event_id not in e_id:
                    e_id.append(event_id)   
    return e_id                

def get_note(z):
    f=[]
    for j in z:
       f.append(json.loads(j))
    return f

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

async def get_answers_Event(client, event_):
    f = Filter().events(evnts_ids(event_)).kinds([Kind(1),Kind(1111)]).limit(int(10*len(event_)))
    
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_one_Event(client, event_):
    f = Filter().id(evnt_id(event_))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_answer_Event(client, event_):
    f = Filter().event(evnt_id(event_)).kinds([Kind(1),Kind(1111)]).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

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
    
    # Add relays and connect
    await client.add_relay("wss://nos.lol/")
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://purplerelay.com/")
    
    await client.connect()
    
    await asyncio.sleep(2.0)

    if isinstance(e_id, list):
         print("list")
         test_id = await get_notes_(client,e_id)
         resp_answer=await get_answers_Event(client,e_id)
         if resp_answer!=[]:
          for resp in resp_answer:
            if resp not in test_id:
             test_id.append(resp)
    else:
        print("str")
        test_id = await get_one_note(client,e_id)
        resp_answer=await get_answer_Event(client, e_id)
        if resp_answer!=[]:
         for resp in resp_answer:
          if resp not in test_id:
           test_id.append(resp)
    return test_id

frame2=Frame(root)
db_list=[]

def add_db_list():
        
        Frame_2=Frame(root)
        Frame_block=Frame(Frame_2,width=50, height=20)
               
        def Close_block(event):
            Frame_block.destroy()
        
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=17, row=1, padx=5, columnspan=1) 
        
    
        def search_block_list():
            label_string_block1.set(len(db_list_note))    

        def delete_block_list():
            db_list_note.clear()
            label_string_block1.set(len(db_list_note))    
    
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey")
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ")
        random_block1.grid(column=1,row=0,padx=5,pady=5)
        label_string_block1=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1)
        label_block_list1.grid(column=1,row=1,pady=5)
        Frame_block.grid(column=0,row=6, columnspan=3, rowspan=2)
        Frame_2.place(relx=0.02,rely=0.65)

button_block=tk.Button(root, highlightcolor='WHITE',
                  text='DB count',
                  font=('Arial',12,'bold'),
                  command=add_db_list            
                  )

button_block.place(relx=0.05,rely=0.6) 
frame2.grid(column=0, row=0,columnspan=3, rowspan=4,pady=10)
image=""
summary =""

class fork_json:
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
        if tags_note[0]=="d":
         global url_uid  
         url_uid = str(tags_note[1])
        if tags_note[0]=="title":
         global title  
         title= str(tags_note[1])  
        if tags_note[0]=="summary":
         global summary
         summary= str(tags_note[1])      
       return url_uid,title,summary 
    
class fork:
    def __init__(self,tag_first:list[str],event:list["str"],relay:"str",mode:str):
        self.tag_a=tag_first
        self.event_a=event
        self.relay=relay
        self.mode=mode
    def __str__(self):
        return f"{self.tag_a,self.event_a,self.relay,self.mode}"
    def my_func(abc):
        print("hello my tag is "+ abc.tag_a)
    def __list__(self):
       list_to_tag=[]
       #if self.count():
       for tag_a,evn_x in zip(self.tag_a, self.event_a):
           list_to_single=[]
           list_to_single.append(tag_a)
           list_to_single.append(evn_x)
           list_to_single.append(self.relay)
           list_to_single.append(self.mode)
           list_to_tag.append(list_to_single)
       
       return list_to_tag      

def fork_note(note_ex):
    test = fork_json(note_ex)               
    test.__list__()
    tag_id=str(note_ex["kind"])+str(":")+str(note_ex["pubkey"])+str(":")+url_uid.lower()
    if Coordinate.parse(tag_id).verify()==True:
        p_one = fork(["a","e"],[tag_id, note_ex["id"]],"wss://relay.wikifreedia.xyz/","fork")

        p2_=p_one.__list__()    
        print(p2_)

        if p2_:
             
            tags=Tag.custom(TagKind.SUMMARY(), [summary]),Tag.custom(TagKind.TITLE(), [title]),Tag.identifier(url_uid),Tag.custom(TagKind.IMAGE(), [image]),Tag.custom(TagKind.PUBLISHED_AT() , [str( int(time.time()) )])   #Tag.custom
       
            l_list=list(tags)
       
            for p2_x in  p2_:
                l_list.append(Tag.parse(p2_x))
            tags=tuple(l_list)
    else:    
       tags=Tag.custom(TagKind.SUMMARY(), [summary]),Tag.custom(TagKind.TITLE(), [title]),Tag.identifier(url_uid),Tag.custom(TagKind.IMAGE(), [image])  
    return tags

root.mainloop()

# help me 818def corny_book():

root = tk.Tk()
root.geometry("1250x800")

def wiki_change():
   check_square_2()
   lists_id=[] 
   if button_entry_m.cget('foreground')=="green":
    if list_e!=[] or list_a!=[] :
      if list_e!=[]:  
        for xlist in list_e:
            lists_id.append(Tag.event(event_id=EventId.parse(xlist)))
            
      if list_a!=[]:        
        for jlist in list_a:
            if Coordinate.parse(jlist).verify()==True and Coordinate.parse(jlist).kind().as_u16()==30818:
              print(Coordinate.parse(jlist).kind().as_u16())
              lists_id.append(Tag.coordinate(Coordinate.parse(jlist),NONE))
            else:
               #EXIT
               print("false",jlist) 
               return jlist  
      if list_p!=[]:        
        for alist in list_p:
            lists_id.append(Tag.public_key(alist))
      if list_merge_e!=[]:
         lists_id.append(Tag.parse(list_merge_e))      
      
      
      
    if __name__ == '__main__':
        note=""
        if combo_lab.get()!="Type of status":
           print(lists_id)
           asyncio.run(request_merge(lists_id,combo_lab.get()))

button_send=tk.Button(root,text="request to merge",command=wiki_change, background="darkgrey",font=("Arial",14,"bold"))
button_send.place(relx=0.525,rely=0.65,relwidth=0.15,relheight=0.1,anchor='n' )

async def request_merge(tag,status):
   # Init logger
   init_logger(LogLevel.INFO)
   key_string=log_these_key()
   if key_string!=None: 
    keys = Keys.parse(key_string)
    signer=NostrSigner.keys(keys)
    client = Client(signer)

    # Add relays and connect
    await client.add_relay("wss://relay.lnfi.network/")
    await client.add_relay("wss://strfry.chatbett.de/")
    #await client.add_relay("")

    await client.connect()
     
    builder = EventBuilder(Kind(818),status).tags(tag)
      
    #await client.send_event_builder(builder,tag)
    await client.send_event_builder(builder)
    print("Event sent:")
    await asyncio.sleep(2.0)

    # Get events from relays
    print("Getting events from relays...")
    f = Filter().authors([keys.public_key()])
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    for event in events.to_vec():
     print(event.as_json())

status_list=["Maybe you'll like my version better","You might prefer my version","Hopefully you'll like the version I suggested.","Let me know if you prefer my version.","Just a suggestion, you might like my version more.","I’ve made a small edit, see if it works better for you."]

def on_tags_event(event):
    selected_item=combo_lab.get()

combo_lab = ttk.Combobox(root, values=status_list,font=('Arial',12,'bold'))
combo_lab.place(relx=0.45,rely=0.15,relwidth=0.15)
combo_lab.set("Type of status")
combo_lab.bind("<<ComboboxSelected>>", on_tags_event)

def check_square_2():
   
    if list_e!=[] and list_a!=[] and list_p!=[] and list_merge_e!=[]:
       
       if combo_lab.get()!="Type of status":
        print("status "+combo_lab.get())
        button_entry_m.config(text="■",foreground="green")
        print("ok")
       
       else:
        print("Problem:")
        print("Wait for status") 
        button_entry_m.config(text="■",foreground="grey")
  
    else:
        print("Problem:")
        print("Wait for Tag") 
        button_entry_m.config(text="■",foreground="grey")

button_entry_m=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square_2,background="lightgrey", border=2)
button_entry_m.place(relx=0.62,rely=0.65,relwidth=0.05, relheight=0.1,anchor="n" )
e_tag = tk.Label(root, text="e Tag",font=("Arial",12,"bold"))
e_tag.place(relx=0.7,rely=0.15,relwidth=0.1,relheight=0.1 )
e_tag_entry=ttk.Entry(root,justify='left',font=("Arial",12))
e_tag_entry.place(relx=0.7,rely=0.25,relwidth=0.2)
d_tag_search = tk.Label(root, text="d-Tag Search",font=("Arial",12,"bold"))
d_tag_search.place(relx=0.15,rely=0.15,relwidth=0.1,relheight=0.1 )
d_tag_entry_s=ttk.Entry(root,justify='left',font=("Arial",12))
d_tag_entry_s.place(relx=0.15,rely=0.25,relwidth=0.2)

def upload_d_tag_id():
   list_event=Open_json_fake_note(d_tag_entry_s.get()+"-"+"wiki")
   if list_event!=None:
    print(list_event[0]["id"])
    e_tag_entry_merge.insert(0, list_event[0]["id"])
    e_show_merge() 
    entryp_tag.delete(0, END)  

re_upload = tk.Button(root, text="re upload", font=("Arial",12,"bold"), command=upload_d_tag_id)
re_upload.place(relx=0.05,rely=0.24)

def call_text_mer():
  if d_tag_entry_s.get()!="":
   if __name__ == "__main__":
    response=asyncio.run(Search_d_tag_merge())
    if response:

     note_=get_note(response)
     for jnote in note_:
      
       if jnote not in db_list_note:
          db_list_note.append(jnote)
       
    else:
       print("empty")
  else:     
       if relay_search_list==[]:
          if __name__ == "__main__":
            response=asyncio.run(Search_d_tag())
          if len(relay_search_list)>0:
             button_close_search["text"]="Search 🔍"

async def get_result_merge(client):
    
    f = Filter().identifier(d_tag_entry_s.get()).kind(Kind(30818)).limit(10)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Search_d_tag_merge():
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    if relay_search_list!=[]:
       for jrelay in relay_search_list:
          await client.add_relay(jrelay)
       await client.connect()
       await asyncio.sleep(2.0)

       combined_results = await get_result_merge(client)
       return combined_results
     
    await client.add_relay("wss://relay.nostr.band/")
    await client.connect()
    await search_box_relay()
    print("found ", len(relay_search_list), " relays")


public_list=[]
button_close_search=tk.Button(root, text='Search Relay',font=('Arial',12,'bold'), command=call_text_mer)    
button_close_search.place(relx=0.37,rely=0.24 ) 
p_tag = tk.Label(root, text="p-Tag",font=("Arial",12,"bold"))
entryp_tag=ttk.Entry(root,justify='left',font=("Arial",12),)
p_tag.place(relx=0.1,rely=0.75,relwidth=0.1 )
entryp_tag.place(relx=0.1,rely=0.8,relwidth=0.2 )
p_view = tk.Label(root, text="p tag?: ", font=("Arial",12))
Checkbutton8 = IntVar() 
Type_band = Checkbutton(root, text = "More p tag", 
                    variable = Checkbutton8, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10,font=('Arial',16,'normal'))
Type_band.place(relx=0.29,rely=0.77,relwidth=0.1,relheight=0.05,anchor='e')  
p_view.place(relx=0.22,rely=0.85,relwidth=0.1 )
list_p=[]

def p_show():
    title=entryp_tag.get()
    
    if len(title)==64:
       
        if convert_user(title)!=None:
         if title not in list_p:
          if Checkbutton8.get()==0:
            if len(list_p)>=1:
                i=1
                while len(list_p)>i:
                 list_p.pop(1)
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END)  
            else:  
                list_p.append(title)
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END) 
                return list_p
          else:
                list_p.append(title)
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END) 
                return list_p 
          
         else:
              p_view.config(text=str(len(list_p)))
              
              entryp_tag.delete(0, END) 
              return list_p
        else:
         p_view.config(text=str(len(list_p)))
         entryp_tag.delete(0, END) 
    else:
       entryp_tag.delete(0, END) 
       if len(list_p)>0:
        p_view.config(text=str(len(list_p)))

p_button = tk.Button(root, text="p_show", font=("Arial",12,"bold"), command=p_show)
p_button.place(relx=0.1,rely=0.85)
list_e=[]

def e_show():
    title=e_tag_entry.get()
    
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

list_merge_e=[]
e_tag_merge = tk.Label(root, text="e-Tag Merge",font=("Arial",12,"bold"))
e_tag_merge.place(relx=0.7,rely=0.7,relwidth=0.1,relheight=0.1 )
e_tag_entry_merge=ttk.Entry(root,justify='left',font=("Arial",12))
e_tag_entry_merge.place(relx=0.7,rely=0.8,relwidth=0.2)
e_view_merge = tk.Label(root, text="e tag merg?: ", font=("Arial",12))
e_view_merge.place(relx=0.77,rely=0.85,relwidth=0.2 )

def e_show_merge():
    title=e_tag_entry_merge.get()
    
    if len(title)==64:
       
        if evnt_id(title)!=None:
         if title not in list_merge_e:
          #test_append=str("e")+title+str(" ")+str("source")
          list_merge_e.append(str("e"))
          list_merge_e.append(title)
          list_merge_e.append(" ")
          list_merge_e.append(str("source"))
          e_view_merge.config(text=str(len(list_merge_e)))
          e_tag_entry_merge.delete(0, END) 
          print(list_merge_e)
          return list_merge_e
          
         else:
              print("already present")
              e_view_merge.config(text=str(len(list_merge_e)))
              e_tag_entry_merge.delete(0, END) 
              return list_merge_e
        else:
         print("event_id")
         e_view_merge.config(text=str(len(list_e)))
         e_tag_entry_merge.delete(0, END)    
     
    else:
          
          e_tag_entry_merge.delete(0, END) 
          return list_merge_e   

e_button_merge = tk.Button(root, text="e_show merge", font=("Arial",12,"bold"), command=e_show_merge)
e_button_merge.place(relx=0.7,rely=0.85)
list_a=[]

def a_show():
    a_tag_entry=entry_a.get()
    if a_tag_entry!="":
      try:  
        event_kind = Coordinate.parse(a_tag_entry).kind()
        event_identifier = Coordinate.parse(a_tag_entry).identifier()
        event_publickey = Coordinate.parse(a_tag_entry).public_key()
        
        if event_publickey!=None:
            list_p.append(event_publickey)
            p_show()
       
        if a_tag_entry not in list_a:
            for j in a_tag_entry.split():
              if j[0:6]=="nostr:":
                  if j[6:] not in list_a:
                   
                   list_a.append(j[6:])
                   a_view.config(text=str(len(list_a)))
                   entry_a.delete(0, END)    
              else:
                  
                  list_a.append(a_tag_entry)
                  a_view.config(text=str(len(list_a)))
                  entry_a.delete(0, END) 
                  #print(list_a)
        else:
             a_view.config(text="Enter an article naddr: " )         
             entry_a.delete(0, END) 
      except NostrSdkError as e:
          print(e)   
          entry_a.delete(0, END)     
    else:   
        if len(list_a)>0:
              a_view.config(text=str(len(list_a)))
              entry_a.delete(0, END) 
              
        else:
           a_view.config(text="Article: ") 
            
e_button = tk.Button(root, text="e_show", font=("Arial",12,"bold"), command=e_show)
e_button.place(relx=0.7,rely=0.30)
e_view = tk.Label(root, text="e tag?: ", font=("Arial",12))
e_view.place(relx=0.77,rely=0.30,relwidth=0.2 )

a_tag = tk.Label(root, text="a-Tag",font=("Arial",12,"bold"))
a_tag.place(relx=0.7,rely=0.35,relwidth=0.1,relheight=0.1 )
entry_a=ttk.Entry(root,justify='left',font=("Arial",12))
entry_a.place(relx=0.7,rely=0.45,relwidth=0.2 )

a_button = tk.Button(root, text="a tag", font=("Arial",12,"bold"), command=a_show)
a_button.place(relx=0.7,rely=0.50,relwidth=0.1)
a_view = tk.Label(root, text="Article: ", font=("helvetica",13,"bold"),justify="center")
a_view.place(relx=0.7,rely=0.58,relwidth=0.3)

root.mainloop()