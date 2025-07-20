#Combolink
import asyncio
from nostr_sdk import Client, Filter, Keys, NostrSigner, init_logger, LogLevel, PublicKey
from nostr_sdk import *
from nostr_sdk import Event,EventBuilder, Metadata,EventId,Kind
from datetime import timedelta
import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import shutil

def note_list(list_follow):
    L=[]
    if __name__ == "__main__":
     test_people = list_follow
     combined_results = asyncio.run(main(test_people))
    L=get_note(combined_results)
    return L

def note_user(user):
    if __name__ == "__main__":
     single_author = user  
     L = asyncio.run(main(single_author))
    note=get_note(L)
    return note

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f
def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z

def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def search_kind(user,x):
    if __name__ == "__main__":
     # Example usage with a single key
     single_author = user 
     single_results = asyncio.run(main(single_author))
    Z=[]
    note=get_note(single_results)
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

async def get_relays(client, authors):
    f = Filter().authors(authors).kind(Kind(1)).limit(700)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def get_relay(client, user):
    f = Filter().author(user).kind(Kind(3))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def main(authors):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    await client.add_relay("wss://nostr.mom/")
    await client.add_relay("wss://nos.lol/")
    if relay_list!=[]:
       s=0
       for relay_x in relay_list:
          if s<3:
           await client.add_relay(relay_x)
          s=s+1 
    await client.connect()
    await asyncio.sleep(1.0)

    if isinstance(authors, list):
        combined_results = await get_relays(client, authors)
    else:
        combined_results = await get_relay(client, authors)
    
    return combined_results

root = tk.Tk()
root.title("test link")
root.geometry("1250x800")
frame_top_box=tk.Frame(root,height=30,width=200,background="darkgrey")
frame2=tk.Frame(root,height=60,width=110)

my_dict = {"Pablo": "fa984bd7dbb282f07e16e7ae87b26a2a7b9b90b7246a44771f0cf5ae58018f52", 
           "jb55": "32e1827635450ebb3c5a7d12c1f8e7b2b514439ac10a67eef3d9fd9c5c68e245",
             "Vitor": "460c25e682fda7832b52d1f22d3d22b3176d972f60dcdc3212ed8c92ef85065c", 
             "Hodlbod": "97c70a44366a6535c145b333f973ea86dfdc2d7a99da618c40c64705ad98e322", 
             "me": "592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"}

my_list = list(my_dict.values())
my_name = list(my_dict.keys())
def on_select(event):
    selected_item = combo_box.get()
    label.config(text="Selected Item: " + my_dict[selected_item][0:9])

label = tk.Label(frame_top_box, text="Selected Item: ",font=("Arial",10,"bold"),width=20)
label.grid(row=1, column=5, columnspan=2,pady=5,padx=5 )
combo_box = ttk.Combobox(frame_top_box, values=["Pablo","jb55","Vitor","Hodlbod","me"],font=("Arial",10,"bold"))
combo_box.grid(row=0, column=5,columnspan=2, pady=5 )
combo_box.set("Option 1")
combo_box.bind("<<ComboboxSelected>>", on_select)
stringa=tk.IntVar()
select_kind=Label(frame_top_box,text="Links", font=("Arial",20,"bold"),background="lightgrey")
select_kind.grid(column=2, row=0,padx=10,columnspan=2,rowspan=2,pady=10)

def search_event(): 
 if combo_box.get()!="Option 1":
  user=convert_user(my_dict[combo_box.get()])
  z=search_kind(user,3)
  if z!=[]:
   people=tags_string(z[0],'p')
   User=user_convert(people)
   tm=note_list(User)
   return tm

def search_():
   result=search_event()
   if result !=None:
    for item_x in result:
       if item_x not in db_list:
         db_list.append(item_x)
    show_link()
    print_text()

frame1=tk.Frame(root,height=100,width=200)
button_tm=tk.Button(frame_top_box,command= search_,text="View note", font=("Arial",10,"bold"))
button_tm.grid(column=8, row=1,padx=5,pady=5)
db_link=[]
db_list=[]

def url_spam(x):
 z=x['content']
 for j in z.split():
    if j[0:5]=="https":
        return str(j)

def link_kind1():
   if db_list!=[]:
    kind1=db_list
    zeta=[]
    if kind1:
     for j in kind1:
        zeta.append(url_spam(j))   
     result=[]
     for x in zeta:
        if x !=None:
            result.append(x)
     return result  

def codifica_link_str(string):
   f=string
   list_v=['mov','mp4']
   list1=['webm']
   audio=['mp3']
   img=['png','jpg','gif']
   img1=['jpeg','webp']
   ytube=['https://youtu.be',"https://www.youtube.com/","https://m.youtube.com/","https://youtube.com/"] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_v:
        return "video"
   if f[-4:] in list1:
        return "video"
   if f[-3:] in audio:
        return "audio"
   if f[-3:] in img:
           return "pic" 
   if f[0:16] in ytube or  f[0:24] in ytube or f[0:22] in ytube or f[0:20] in ytube:
            return 'ytb'
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam"

def invidious(url):
   if url[0:17]=='https://youtu.be/':
      string=str("https://inv.nadeko.net/")+str(url[17:])
      string2=str("https://yewtu.be/")+str(url[17:])
      print(string,"\n",string2)
   if url[0:24]=="https://www.youtube.com/":   
      string=str("https://inv.nadeko.net/")+str(url[24:])
      string2=str("https://yewtu.be/")+str(url[24:])
      print(string,"\n",string2)
   if url[0:22]=="https://m.youtube.com/": 
      string=str("https://inv.nadeko.net/")+str(url[22:])
      string2=str("https://yewtu.be/")+str(url[22:])
      print(string,"\n",string2)  
   if url[0:20]=="https://youtube.com/": 
      string=str("https://inv.nadeko.net/")+str(url[20:])
      string2=str("https://yewtu.be/")+str(url[20:])
      print(string,"\n",string2)     

def show_link():
    result=link_kind1()
    if result!=None:
     for item in result:
      if item not in db_link:
       db_link.append(item)

frame3=tk.Frame(root,height=120,width= 100)
frame1=tk.Frame(root,height=100,width=200)
frame_top_box.grid(column=0,row=0,padx=5,rowspan=2,columnspan=4)
frame1.grid()
frame3.grid()

def add_db_list():
        button_block.grid_forget()
        Frame_block=Frame(root, height=30,width=200, background="darkgrey")
                
        def Close_block(event):
            Frame_block.place_forget()
            button_block.grid(column=9, columnspan=2, row=0, pady=5,padx=10) 
         
        button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',10,'bold'))    
        button_b_close.bind("<Double-Button-1>" ,Close_block)
        button_b_close.grid(column=17, row=0, padx=5, columnspan=1) 
        
        def search_block_list():
            label_string_block1.set(len(db_list))    

        def delete_block_list():
            db_list.clear()
            label_string_block1.set(len(db_list))   

        def link_count():
            label_link_var.set(len(db_link))

        def clear_db_link():
            db_link.clear()
            label_link_var.set(len(db_link))   
                   
        clear_block=Button(Frame_block, command=delete_block_list, text= "Clear DB: ",background="darkgrey")
        clear_block.grid(column=0,row=0,padx=5,pady=5)    
        random_block1=Button(Frame_block, command=search_block_list, text= "DB: ")
        random_block1.grid(column=1,row=0,padx=5,pady=5)
        clear_link=Button(Frame_block, command=clear_db_link, text= "Clear DB link: ",background="darkgrey")
        clear_link.grid(column=0,row=1,padx=5,pady=5)    
        random_count=Button(Frame_block, command=link_count, text= "DB_link: ")
        random_count.grid(column=1,row=1,padx=5,pady=5)
        label_string_block1=StringVar()
        label_link_var=StringVar()
        label_block_list1=Label(Frame_block, textvariable=label_string_block1)
        label_block_list1.grid(column=2,row=0,padx=5,pady=5)
        label_var_list1=Label(Frame_block, textvariable=label_link_var)
        label_var_list1.grid(column=2,row=1,padx=5,pady=5)
        
        Frame_block.place(relx=0.3,rely=0,relwidth=0.18,relheight=0.095)
        
button_block=tk.Button(root, highlightcolor='WHITE',
                  text='DB count',
                  font=("Arial",10,"bold"),
                  command=add_db_list)
button_block.grid(column=9, columnspan=2, row=0, pady=5,padx=10) 
frame2.place(relx=0.65,rely=0.15,relwidth=0.2,relheight=0.3)

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
 if db_list!=[]:
   
   s=1
   if List_note_out==[]:
      value=0
   else:   
    value=len(List_note_out)
   if value+50<len(db_list):
    for note in db_list[value:value+50]:
     if note not in List_note_out:
        List_note_out.append(note)
     try:
      context0="Pubkey "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
      if note['tags']!=[]:
        context1=note['content']+"\n"
        context2="\n"+" [  [ Tags ] ] "+"\n"+"\n"
        for xnote in note["tags"]:
         context2=context2+str(xnote) +"\n"
      else: 
        context1=note['content']+"\n"
        context2=""
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0)
      label_id.grid(pady=2,column=0, columnspan=3,row=s)
      scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
      scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
      second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
      second_label10.insert(END,context1+"\n"+str(context2))
      scroll_bar_mini.config( command = second_label10.yview )
      second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 
      
      def print_id(entry):
           number=list(db_list).index(entry)
           print(number)
                  
      def print_var(entry):
                print(entry["content"])
           
      button=Button(scrollable_frame_1,text=f"Content", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s+2,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"Number note", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s+2,column=1,padx=5,pady=5)      
      s=s+3  

     except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.44,rely=0.35,relwidth=0.30,relheight=0.4)

    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()

    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.5,rely=0.78,relwidth=0.1)      
   
def pic_show(x):
   response = requests.get(x, stream=True)
   if response.ok==True:
    with open('my_image.png', 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response
    from PIL import Image
    img = Image.open('my_image.png')
    img.show()

def show_one_photo():
    if entry_id.get()!="":
        if codifica_link_str(entry_id.get())=="pic":
            photo=entry_id.get()
            pic_show(photo)

def photo_print(url):
  
  if codifica_link_str(url)=="pic":
   frame_pic=tk.Frame(root,height=20,width= 80)
   stringa_pic=StringVar()
   stringa_pic.set(url)
   label_pic = Entry(frame_pic, textvariable=stringa_pic)
   image_label = tk.Label(frame_pic)
   image_label.grid(column=0,row=1, padx=10,pady=10)
   if label_pic.get()!="":
      try:
       response = requests.get(label_pic.get(), stream=True)
       if response.ok==True:
        with open('my_image.png', 'wb') as file:
         shutil.copyfileobj(response.raw, file)
        del response
        from PIL import Image
        image = Image.open('my_image.png')
       
        number=float(image.height/image.width) 
        
        test1=int(float(number*250))
        if number>1.5:
            test1=int(1.5*250)
     
        image.thumbnail((250, test1))  # Resize image if necessary
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
        frame_pic.rowconfigure(1,weight=3)
        
        button_close.grid(column=0,row=0,padx=10)
        frame_pic.place(relx=0.85,rely=0.5,relwidth=0.3,anchor="n")
         
      except TypeError as e: 
        print(e)  
      except ZeroDivisionError as d:
         print(d)
           

button_pic_ent=tk.Button(root, highlightcolor='Blue',text=' 📷 Photo',font=('Arial',12,'normal'),command=show_one_photo)
button_pic_ent.place(relx=0.42, rely=0.17,relheight=0.035)
button_read=Button(root,text="Stamp Note", command=show_Teed,font=("Arial",12,"normal"))
button_read.place(relx=0.2, rely=0.25)

def write_sticky_note(name,note_text):       #id of the note and name is the label
    import json
    list_event=Open_sticky_note(name)
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

label_combo_link=StringVar()      
entry_label_theme=tk.Entry(root, textvariable=label_combo_link)    
label_entry_theme=Label(root,text="label")

def show_note_link(note):
 frame2=tk.Frame(root)  
 canvas_1 = tk.Canvas(frame2)
 scrollbar_1 = ttk.Scrollbar(frame2, orient="vertical", command=canvas_1.yview)
 scrollable_frame_1 = ttk.Frame(canvas_1)
 label_entry_theme.place(relx=0.78,rely=0.35)
 entry_label_theme.place(relx=0.76,rely=0.4)  
 scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all")))

 canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
 canvas_1.configure(yscrollcommand=scrollbar_1.set)
 if db_list!=[]:
    s=1
    try:
      context0="Pubkey "+note['pubkey']+"\n"+"id: "+note["id"]+"\n"
      if note['tags']!=[]:
        context1=note['content']+"\n"
        context2="\n"+" [ [ Tags ]  ] "+"\n"+"\n"
        for xnote in note["tags"]:
         context2=context2+str(xnote) +"\n"
      else: 
        context1=note['content']+"\n"
        context2=""
           
      var_id=StringVar()
      label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
      var_id.set(context0)
      label_id.grid(pady=2,column=0, columnspan=3,row=s)
      scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
      scroll_bar_mini.grid( sticky = NS,column=4,row=s+1,pady=5)
      second_label10 = tk.Text(scrollable_frame_1, padx=8, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
      second_label10.insert(END,context1+"\n"+str(context2))
      scroll_bar_mini.config( command = second_label10.yview )
      second_label10.grid(padx=10, column=0, columnspan=3, row=s+1) 

      def print_id(entry):
           number=list(db_list).index(entry)
           print(number)

      def write_the_file(entry):
         if entry_label_theme.get()!="": 
          name_label=entry_label_theme.get()
          write_sticky_note(name_label,entry["id"])
                  
      def print_var(entry):
                print(entry["content"])
                              
      button=Button(scrollable_frame_1,text=f"Content!", command=lambda val=note: print_var(val))
      button.grid(column=0,row=s+2,padx=5,pady=5)
      button_grid2=Button(scrollable_frame_1,text=f"number note", command=lambda val=note: print_id(val))
      button_grid2.grid(row=s+2,column=1,padx=5,pady=5)      
      button_grid3=Button(scrollable_frame_1,text=f"label it", command=lambda val=note: write_the_file(val))
      button_grid3.grid(row=s+2,column=2,padx=5,pady=5)  
      
      s=s+3  

    except NostrSdkError as c:
           print(c, "maybe there is an Error") 

    scrollbar_1.pack(side="right", fill="y",pady=20)
    canvas_1.pack( fill="y", expand=True)
    frame2.place(relx=0.44,rely=0.35,relwidth=0.30,relheight=0.4)
    
    def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
        label_entry_theme.place_forget()
        entry_label_theme.place_forget() 

    button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.5,rely=0.78,relwidth=0.1)      

entry_id_note=StringVar()
entry_note_note=StringVar()
frame_id=tk.Frame(frame1,height=30,width= 100)
label_entry_id=tk.Label(root, text="entry note id",font=("Arial",12,"normal"))
label_entry_id.place(relx=0.13,rely=0.14)
entry_id=tk.Entry(root, textvariable=entry_id_note, width=50)
entry_note=tk.Entry(frame_id, textvariable=entry_note_note, width=50)
type_link=StringVar()
label_entry_id=tk.Label(root, textvariable=type_link,font=("Arial",12,"normal"))
label_entry_id.place(relx=0.23,rely=0.14)
entry_id.place(relx=0.1,rely=0.18)

def show_link_note():
   if entry_id.get()!="":
        for j_db in db_list:
            if url_spam(j_db)==entry_id.get():
                print (j_db)
                show_note_link(j_db)
                return j_db 
            
def show_url_note(url):
   if url!="":
        for j_db in db_list:
            if url_spam(j_db)==url:
                show_note_link(j_db)
                return j_db             

def show_save_note():
   if entry_id.get()!="":
        for j_db in db_list:
            if url_spam(j_db)==entry_id.get():
              pass #save id tag

button_id=tk.Button(root,command=show_link_note,text="Note",font=("Arial",12,"normal"))
button_id.place(relx=0.37,rely=0.17, relheight=0.035)
frame_id.grid(column=0, row=0, columnspan=4, rowspan=3)
List_note_out=[]

def print_text():  
    
    frame3=tk.Frame(root,height=120,width= 400)
    canvas = tk.Canvas(frame3,width=390)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    s=1    
    if db_link!=[]: 
     for note in db_link:
        
            var_id=StringVar()
            button=Label(scrollable_frame,text=f"{str(codifica_link_str(note))}",font=('Arial',12,'bold'))
            button.grid(column=0,row=s,padx=10,pady=10)
            label_id = Message(scrollable_frame,textvariable=var_id, relief=RAISED,width=370)
            if len(note)>50:
             var_id.set(note[0:50])
            else:
             var_id.set(note)    
            label_id.grid(pady=10,column=1,columnspan=3,row=s)

            def print_id(test):
                entry_id_note.set(test)
                type_link.set(codifica_link_str(test))
            
            def print_var(test):
                print(test)
            
            button=Button(scrollable_frame,text=f"print", command=lambda val=note: print_var(val))
            button.grid(column=0,row=s+1,padx=5,pady=10)
            button_grid2=Button(scrollable_frame,text=f"see url", command=lambda val=note: print_id(val))
            button_grid2.grid(row=s+1,column=1,padx=5,pady=10)
            button_grid3=Button(scrollable_frame,text="Note", command=lambda val=note: show_url_note(val))
            button_grid3.grid(row=s+1,column=2,padx=5,pady=10)
            if codifica_link_str(note)=="pic":
             button_grid4=Button(scrollable_frame,text="Photo", command=lambda val=note: photo_print(val))
             button_grid4.grid(row=s+1,column=3,padx=5,pady=10)
            if codifica_link_str(note)=="ytb":
               button_grid5=Button(scrollable_frame,text="Video", command=lambda val=note: invidious(val))
               button_grid5.grid(row=s+1,column=3,padx=5,pady=10)
              
            root.update()  
            s=s+2
   
     canvas.pack(side="left", fill="y", expand=True)
     scrollbar.pack(side="right", fill="y")  
     frame3.place(relx=0.01,rely=0.35,relwidth=0.4)      
    
     def Close_print():
       frame3.destroy()  

     button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
     button_close_.pack(pady=5,padx=5) 

button4=tk.Button(root,text="View Links",command=print_text, font=("Arial",12,"normal"))
button4.place(relx=0.1, rely=0.25) 
frame1.grid()
relay_list=[]

def open_relay():
    frame_account=tk.Frame(root, background="darkgrey")
    structure_relay = tk.Label(frame_account, text="relay",font=("Arial",12,"bold"))
    entry_relay=ttk.Entry(frame_account,justify='left',font=("Arial",12,"bold"))
    structure_relay.grid(column=11, row=1, padx=5,pady=5) 
    button_beau.place_forget()
    
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
       
       button_beau.place(relx=0.55,rely=0.02) 
        
    button_close=tk.Button(frame_account, background='red', text='❌',font=('Arial',12,'bold'))    
    button_close.bind("<Double-Button-1>" ,Close_profile) 
    button_close.grid(column=13, row=0, padx=5,pady=5, columnspan=1) 

    def on_server(event):
       label_relay["text"] = combo_bo_r.get()[6:]
       
    label_relay = tk.Label(frame_account, text="Name relay",font=('Arial',12,'bold'))
    label_relay.grid(column=13,row=1,pady=5)
    combo_bo_r = ttk.Combobox(frame_account, font=('Arial',12,'normal'))
    combo_bo_r.grid(column=13,row=2,pady=5)
    combo_bo_r.set("Relays set")
    combo_bo_r.bind("<<ComboboxSelected>>", on_server)
    frame_account.place(relx=0.5,rely=0.001,relheight=0.23,relwidth=0.4)

button_beau=tk.Button(root, highlightcolor='WHITE',text='Relay',font=('Arial',12,'bold'),command=open_relay )
button_beau.place(relx=0.55,rely=0.02) 

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

root.mainloop()