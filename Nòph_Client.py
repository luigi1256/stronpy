from nostr_sdk import *
import asyncio
from datetime import timedelta
from nostr_sdk import PublicKey
from nostr_sdk import Tag
from nostr_sdk import EventId,Event
import time
from datetime import datetime
import uuid
import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from cryptography.fernet import Fernet
import requests
import shutil
from PIL import Image, ImageTk
from tkinter import messagebox 
from tkinter.filedialog import askopenfilename
import io

root = tk.Tk()
root.title("Blog Example")
root.geometry("1250x800")

colour1=''
colour2='grey'
colour3='#65e7ff'
colour4='BLACK'

def OpenFile():
    entry4.delete("1.0","end")
    name = askopenfilename()
    if name!="":
     f = io.open(name, mode="r", encoding="utf-8")
     for j in name.split():
      if j[-3:]==".md": 
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
        error_label.config(text="Error the extension is "+ j[-3:]+"\n"+"try extension markdown")
        print_label.config(text="Error! ", font=("Arial",12,"bold"),foreground="red")
     f.close()   
    else:    
         error_label.config(text="Insert an Article")
         print_label.config(text="Error! ", font=("Arial",12,"bold"),foreground="black")

note_tag = tk.Label(root, text="Note from the file: ",font=("Arial",12,"bold"))
note_tag.place(relx=0.5,rely=0.12,relwidth=0.2,relheight=0.1,anchor='n' )

async def Article_new(note,tag):
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
    try:   
        # Send an event using the Nostr Signer
        builder = EventBuilder.long_form_text_note(note).tags(tag)
      
        testNote= await client.send_event_builder(builder)
        
        messagebox.showinfo("Result",str(testNote.failed.keys)+"\n"+str(testNote.success))
        write_json_fake_note("article",testNote.id.to_hex())
        metadata = metadata_get()
        if metadata!=None:
         await client.set_metadata(metadata)
    except NostrSdkError as e:
           print (e)
    except TypeError as b:
       print(b)

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

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

def long_form():
   check_square()
   if button_entry1.cget('foreground')=="green":
    title=entry_title.get()
    summary=entry_summary.get()
    myUUID = uuid.uuid4()
    url_uid=str(myUUID)
    image=entry_image.get()
    p2=call_function()
    if p2:
       
       if image=="":
        tags=Tag.custom(TagKind.SUMMARY(), [summary]),Tag.custom(TagKind.TITLE(), [title]),Tag.identifier(url_uid),Tag.custom(TagKind.PUBLISHED_AT() , [str( int(time.time()) )])   #Tag.custom
       else:
          tags=Tag.custom(TagKind.SUMMARY(), [summary]),Tag.custom(TagKind.TITLE(), [title]),Tag.identifier(url_uid),Tag.custom(TagKind.IMAGE(), [image]),Tag.custom(TagKind.PUBLISHED_AT() , [str( int(time.time()) )])   #Tag.custom
       l_list=list(tags)
       
       for p2_x in  p2:
        l_list.append(Tag.parse(p2_x))
       tags=tuple(l_list)
    else:    
       if image=="":
        tags=Tag.custom(TagKind.SUMMARY(), [summary]),Tag.custom(TagKind.TITLE(), [title]),Tag.identifier(url_uid),Tag.custom(TagKind.PUBLISHED_AT() , [str( int(time.time()) )])   #Tag.custom
       else:
          tags=Tag.custom(TagKind.SUMMARY(), [summary]),Tag.custom(TagKind.TITLE(), [title]),Tag.identifier(url_uid),Tag.custom(TagKind.IMAGE(), [image]),Tag.custom(TagKind.PUBLISHED_AT() , [str( int(time.time()) )])   #Tag.custom
  
    note=entry4.get(1.0, "end-1c")
    
   
    if __name__ == '__main__':
     note=entry4.get(1.0, "end-1c")
     tag=tags
     asyncio.run(Article_new(note,tag))
     entry4.delete("1.0","end")
     entry_title.delete(0, END)
     entry_summary.delete(0, END)
     entry_image.delete(0,END)
     button_entry1.config(text="■",foreground="grey")
     error_label.config(text="Problem:")
     print_label.config(text="Wait for the article", font=("Arial",12))
     summary_view.config(text="Summary: ")
     title_view.config(text= "view?: ")
     
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
            if entry_title.get()!="":
                button_entry1.config(text="■",foreground="green")
                error_label.config(text="ok")
                print_label.config(text="ok! ", font=("Arial",12,"bold"),foreground="blue")  
                image_call()
                if image_check['text']=="ok, pic":
                  button_entry1.config(text="■",foreground="green")
                  error_label.config(text="ok")
                  print_label.config(text="ok! ", font=("Arial",12,"bold"),foreground="blue") 
                else:
                  button_entry1.config(text="■",foreground="green")
                  error_label.config(text="ok, no photo")
                  print_label.config(text="ok! ", font=("Arial",12,"bold"),foreground="blue")
            else:
                button_entry1.config(text="■",foreground="grey")
                error_label.config(text="Error insert a Title")
                print_label.config(text="Error! ", font=("Arial",12,"bold"),foreground="blue")  
  
    else:
        error_label.config(text="Problem:")
        print_label.config(text="Wait for the article", font=("Arial",12,"bold"),foreground="black") 
        button_entry1.config(text="■",foreground="grey")
        
entry4=tk.Text(root,border=2,highlightbackground="grey")
entry4.place(relx=0.5,rely=0.2,relwidth=0.3,relheight=0.4,anchor='n' )
button_send=tk.Button(root,text="send long form",command=long_form, background="darkgrey",font=("Arial",14,"bold"))
button_send.place(relx=0.525,rely=0.65,relwidth=0.15,relheight=0.1,anchor='n' )
button_entry1=tk.Button(root, text="■",font=("Arial",25,"bold"), foreground="grey",command=check_square,background="lightgrey", border=2)
button_entry1.place(relx=0.62,rely=0.65,relwidth=0.05, relheight=0.1,anchor="n" )
frame1=tk.Frame(root,height=100,width=200, background="darkgrey")
button_import=tk.Button(frame1,text="Import article",command=OpenFile,font=("Arial",12,),
                        background="grey",foreground=colour4,activebackground=colour3,
                        activeforeground=colour4, highlightbackground=colour2,highlightcolor='WHITE') 
button_import.grid(column=2, row=1,padx=10,pady=5,ipadx=1,ipady=1)
error_label = tk.Label(frame1, text="Problem:",font=("Arial",12))
error_label.grid(column=3, rowspan=2, row=0, pady=5)
print_label = ttk.Label(frame1, text="Wait for the article",font=("Arial",12))
print_label.grid(column=3, columnspan=2, row=2, pady=5)
frame1.pack(side=TOP,fill=X)

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

#entry_layout-right
title_tag = tk.Label(root, text="title-Tag",font=("Arial",12,"bold"))
entry_title=ttk.Entry(root,justify='left',font=("Arial",12))
title_button = tk.Button(root, text="view_Title", font=("Arial",12,"bold"), command=title_show)
title_view = tk.Label(root, text="view?: ", font=("Arial",12))
sumamry_tag = tk.Label(root, text="Summary-Tag",font=("Arial",12,"bold"))
entry_summary=ttk.Entry(root,justify='left',font=("Arial",12))
summary_button = tk.Button(root, text="view_Summary", font=("Arial",12,"bold"), command=summary_show)
summary_view = tk.Label(root, text="Summary: ", font=("helvetica",13,"bold"),justify="center")

check_raw=IntVar()

def Raw_tag():
   if check_raw.get()==0:
       check_raw.set(1)
       title_tag.place(relx=0.7,rely=0.15,relwidth=0.1,relheight=0.1 )
       entry_title.place(relx=0.7,rely=0.25,relwidth=0.2)
       title_button.place(relx=0.70,rely=0.30,relwidth=0.07)
       title_view.place(relx=0.77,rely=0.30,relwidth=0.2 )
       sumamry_tag.place(relx=0.7,rely=0.35,relwidth=0.1,relheight=0.1 )
       entry_summary.place(relx=0.7,rely=0.45,relwidth=0.2 )
       summary_button.place(relx=0.70,rely=0.50,relwidth=0.1)
       summary_view.place(relx=0.69,rely=0.58,relwidth=0.3)
      
       button_print.place(relx=0.25,rely=0.5,relwidth=0.05) 
       image_tag.place(relx=0.1,rely=0.4,relwidth=0.1 )
       entry_image.place(relx=0.02,rely=0.56,relwidth=0.28)
       image_button.place(relx=0.02,rely=0.5,relwidth=0.05 )
       image_check.place(relx=0.12,rely=0.5,relwidth=0.1 )
       p_tag.place(relx=0.02,rely=0.85,relwidth=0.1 )
       entryp_tag.place(relx=0.02,rely=0.9,relwidth=0.1 )
       relay_tag.place(relx=0.14,rely=0.85,relwidth=0.1 )
       entry_r_tag.place(relx=0.14,rely=0.9,relwidth=0.1 )
       p_view.place(relx=0.02,rely=0.94,relwidth=0.1 )
       relay_view.place(relx=0.14,rely=0.94,relwidth=0.1 )
       show_button.place(relx=0.25,rely=0.89)  
   else:
         check_raw.set(0)
         title_tag.place_forget()
         entry_title.place_forget()
         title_button.place_forget()
         title_view.place_forget()
         sumamry_tag.place_forget()
         entry_summary.place_forget()
         summary_button.place_forget()
         summary_view.place_forget() 
        
         button_print.place_forget()
         image_tag.place_forget()
         entry_image.place_forget()
         image_button.place_forget()
         image_check.place_forget()
         p_tag.place_forget()
         entryp_tag.place_forget()
         relay_tag.place_forget()
         entry_r_tag.place_forget()
         p_view.place_forget()
         relay_view.place_forget()
         show_button.place_forget()

raw_button = tk.Button(root, text="Open Tag", font=("Arial",12,"bold"), command=Raw_tag,
                background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2)

raw_button.place(relx=0.9, rely=0.02)

def url_link():
 z=entry_image.get()
 for j in z.split():
    if j[0:5]=="https":
        return str(j)

def codifica_link():
   f=url_link()
   list_v=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jepg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_v:
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
  image_check.config(text="ok, " + str(image))
 else:
     if entry_image.get()=="":
      pass
     else:
        entry_image.delete(0, END)
        image_check.config(text="No, " + str(image)) 

image_label = tk.Label(root)
image_label.place(relx=0.55,rely=0.77,relheight=0.22,relwidth=0.3, anchor="n" )

# Load the image

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
        button_lose.place(relx=0.64,rely=0.77,relwidth=0.05) 
  
button_print=Button(root,command=photo_print,text="photo",font=("Arial",12,"bold"))
image_tag = tk.Label(root, text="image-Tag", font=("Arial",12,"bold"))
entry_image=ttk.Entry(root,justify='left')
image_button = tk.Button(root, text="check", font=("Arial",12,"bold"), command=image_call)
image_check = tk.Label(root, text="check?: ", font=("Arial",12,"bold"))
entry_note=ttk.Label(frame1,text="Nòph or Blog", justify='left',font=("Arial",20,"bold"), background="darkgrey",border=2)
entry_note.place(relx=0.4,rely=0.05,relwidth=0.2)

Metadata_dict={}
List_note_write=[]

frame2=tk.Frame(root,height=100,width=200)
frame3=tk.Frame(root,height=100,width=200)
relay_list=[]

Check_open =IntVar()

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
  
#metadata_account

def Look_profile():
    frame_pic=tk.Frame(frame3,height=20,width= 80, background="darkgrey")
    name_label = tk.Label(frame_pic,text="Name ",font=('Arial',10,'bold'))
    name_label.grid(column=8,row=1,padx=10)
    label_about=Label(frame_pic, text="About ",font=('Arial',10,'bold'))
    label_about.grid(column=8,row=2,pady=2,padx=10)
    button_b_0.place(relx=0.7,rely=0.85)   
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
    frame_pic.grid(row=4,column=0,rowspan=5, columnspan=4,pady=5)
    
    def Close_profile(event):
       frame_pic.destroy()
       button_b_0.place_forget() 
       Check_open.set(0)
       counter_dict.place_forget() 

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
button_b0.place(relx=0.7,rely=0.01,relwidth=0.15)

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
        

button_b_0=tk.Button(root,text='Profile',font=('Arial',12,'normal'),command=metadata_stress)
counter_dict=Label(root,text="count",font=('Arial',12,'bold'))
         
def open_relay():
    frame_account=tk.Frame(frame2, background="darkgrey")
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
       
       button_beau.place(relx=0.1,rely=0.12) 
        
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
    frame_account.grid(row=1,column=0,rowspan=2, columnspan=4,pady=5)

button_beau=tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                  activeforeground=colour4, highlightbackground=colour2,
                  highlightcolor='WHITE',
                  text='Relay',
                  font=('Arial',12,'bold'),
                  command=open_relay )

button_beau.place(relx=0.1,rely=0.12) 

def write_json_relay(name,note_text):
       with open(name+".txt", 'w',encoding="utf-8") as file:
    
        file.write(str(note_text))

def download_file_relay():
    if relay_list!=[]:
     write_json_relay("relay",relay_list)
    #message_box     
    
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
button_dwn.place(relx=0.15,rely=0.12)

frame2.place(relx=0.01,rely=0.62,relwidth=0.42,relheight=0.3)
frame3.place(relx=0.02,rely=0.18,relwidth=0.3,relheight=0.3)

p_tag = tk.Label(root, text="pubkey",font=("Arial",12,"bold"))
entryp_tag=ttk.Entry(root,justify='left',font=("Arial",12),)
relay_tag = tk.Label(root, text="relay",font=("Arial",12,"bold"))
entry_r_tag=ttk.Entry(root,justify='left',font=("Arial",12),)
per_tag = tk.Label(root, text="per-Tag",font=("Arial",12,"bold"))
entryper_tag=ttk.Entry(root,justify='left',font=("Arial",12),text="0")
p_view = tk.Label(root, text="p tag?: ", font=("Arial",12))
relay_view = tk.Label(root, text="relay tag?: ", font=("Arial",12))
percent_view = tk.Label(root, text="percent tag?: ", font=("Arial",12))

list_p=[]
list_zap_relay=[]
list_per_zap=[]

def percent_lab():
 try:
  
   if int(entryper_tag.get())>0:
    list_per_zap.append(entryper_tag.get())
    entryper_tag.delete(0, END)
    percent_view.config(text=str(len(list_per_zap))) 
    return list_per_zap
   else:
    list_per_zap.append("1")
    percent_view.config(text=str(len(list_per_zap))) 
    entryper_tag.delete(0, END)
    return list_per_zap
 
 except ValueError as e:
    list_per_zap.append("1")
    if len(list_per_zap)>0:
       percent_view.config(text=str(len(list_per_zap))) 
    entryper_tag.delete(0, END)
    return list_per_zap
        
def p_zap_show():
   title=entryp_tag.get()
   if title!="": 
    if len(title)==64 or len(title)==63:
        if len(title)==63:
         title=PublicKey.parse(title).to_hex()
         print(title)  
        if convert_user(title)!=None:
         if title not in list_p:
                list_p.append(title)
                p_view.config(text=str(len(list_p)))
                entryp_tag.delete(0, END)  
                return list_p
            
         else:
              if len(list_p)>0:
               p_view.config(text=str(len(list_p)))
              entryp_tag.delete(0, END) 
             
        else:
         p_view.config(text=str(len(list_p)))
         entryp_tag.delete(0, END) 
    else:
       
       if entryp_tag.get()=="":
          pass
       else:
          entryp_tag.delete(0, END) 
          if len(list_p)>1:
            p_view.config(text=str(len(list_p)))

def relay_zap_class():
     if entry_r_tag.get()!="":
        if entry_r_tag.get()[0:6]=="wss://" and entry_r_tag.get()[-1]=="/":
            list_zap_relay.append(entry_r_tag.get())
            entry_r_tag.delete(0, END)
            relay_view.config(text=str(len(list_zap_relay)))
            return list_zap_relay
        else:
           entry_r_tag.delete(0, END)
           relay_view.config(text=str(len(list_zap_relay)))
     else:
        list_zap_relay.append(entry_r_tag.get())
        relay_view.config(text=str(len(list_zap_relay)))
        return list_zap_relay      
           
def call_option():
   if p_zap_show():
    if relay_zap_class(): 
     if percent_lab():
      print("ok")
     else:
      print("Insert a value")   
    else:
      print("Insert a relay")    
   else:
      print("Insert a npub")   

show_button = tk.Button(root, text="Zap Tag", font=("Arial",12,"bold"), command=call_option)


class Zap_split:
    def __init__(self,tag_first:str,pubkey:list["str"],relay:list["str"],percent:list["str"]):
        self.tag_zap=tag_first
        self.pubkey=pubkey
        self.relay=relay
        self.percent=percent
    def count(self):
       z=100
       for percent_x in self.percent:
          z=z-int(percent_x)
          if z<0:
             print("there is an error")
             number_per=len(self.percent)
             self.percent.clear()
             i=0
             while i<number_per:
                if int(i+1)==number_per:
                  value= 100-int(100/number_per)*number_per
                  self.percent.append(str(int(100/number_per)+value))
                self.percent.append(str(int(100/number_per)))
                i=i+1
             return self.percent   
       if z==0:
          return self.percent
       else: 
          number_per=len(self.percent)
          self.percent.clear()
          i=0
          while i<number_per:
                if int(i+1)==number_per:
                  value= 100-int(100/number_per)*number_per
                  self.percent.append(str(int(100/number_per)+value))
                self.percent.append(str(int(100/number_per)))
                i=i+1
          return self.percent   
    def __str__(self):
        return f"{self.tag_zap,self.pubkey,self.relay,self.percent}"
    def my_func(abc):
        print("hello my tag is "+ abc.tag_zap)
    def __list__(self):
       list_to_tag=[]
       #if self.count():
       for pub_x,relay_y,percent_Z in zip(self.pubkey,self.relay,self.percent):
           list_to_single=[]
           list_to_single.append(self.tag_zap)
           list_to_single.append(pub_x)
           list_to_single.append(relay_y)
           list_to_single.append(percent_Z)
           list_to_tag.append(list_to_single)
       
       return list_to_tag   
       
def call_function():
  if list_p!=[] and list_zap_relay!=[] and list_per_zap!=[]: 
   p1=Zap_split("zap",list_p,list_zap_relay,list_per_zap)
   p2=p1.__list__()   
   
   if p2:
     return p2           

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

root.mainloop()

