import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
from nostr_sdk import *
import asyncio
from datetime import timedelta
import json
import requests
import shutil
from PIL import Image, ImageTk
import time

relay_list=[]
db_note_list1=[]
db_note_list=[]
list_category=[]
timeline_people=[]
db_list_note_follow=[]
add_relay_list=[]
relay_search_list=[]
Bad_relay_connection=[]
photo_profile={}
Pubkey_Metadata={}

root = tk.Tk()
root.geometry('1300x800') 
value_max=21
value_min=1

value_max_int=IntVar(root,21)
value_min_int=IntVar(root,1)

def tags_string(x,obj):
    f=x["tags"]
    z=[]
    for j in f:
      if j[0]==obj:
          if len(j)>1:
           z.append(j[1])
    return z

def get_note(z):
    f=[]
    import json
    for j in z:
       f.append(json.loads(j))
    return f

def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list 
   
def tags_str(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j)
    return z       

def list_people_fun():
   people_list=[]
   if db_note_list!=[]:
         for note_x in db_note_list:
            if note_x["pubkey"] not in people_list:
               people_list.append(note_x["pubkey"])
            if note_x["pubkey"] not in timeline_people:
               timeline_people.append(note_x["pubkey"])     
         return people_list       
   else:
       return people_list

def pubkey_timeline():
   for note in db_note_list:
      if note["pubkey"] not in timeline_people:
         timeline_people.append(note["pubkey"])

def list_hashtag_fun()->list:
      hashtag_list=[]
      if db_note_list!=[]:
         for note_x in db_note_list:
            if tags_string(note_x,"t")!=[]:
               for hash_y in tags_string(note_x,"t"):
                  if str(hash_y).islower(): 
                     if hash_y not in hashtag_list:
                        hashtag_list.append(hash_y)
                  else:
                     break      
      
      return hashtag_list      

hash_list_notes=[]

def search_for_channel(note_hash:str):
     Notes=db_note_list
     if Notes:
        hash_list_notes.clear()
        for note_x in Notes:
            if note_hash in tags_string(note_x,"t"): 
               hash_list_notes.append(note_x)
        return hash_list_notes    

def print_list_tag(): 
   if db_note_list!=[]:  
      s=1     
      combo_Htag = ttk.Combobox(root, values=[],font=('Arial',12,'normal'),width=10)
      combo_Htag.set("Some Tags")
      test1=list_hashtag_fun()
      test1_value=sorted(test1,key=lambda x: len(x))
      combo_Htag["values"]=test1_value
      combo_Htag.place(relx=0.2,rely=0.09)
      
      def on_select(event):
         value_tag=combo_Htag.get()
         hashtag_list=search_for_channel(value_tag)
         if hashtag_list!=None and len(hashtag_list)>1:
            
            return people_in_tag(hashtag_list)
            
               
      
      combo_Htag.bind("<<ComboboxSelected>>", on_select)

      def people_in_tag(topic):
        list_pubkey_topic=[]
        for note_x in topic:
         if note_x["pubkey"] not in list_pubkey_topic and note_x["pubkey"] not in block_npub:
            list_pubkey_topic.append(note_x["pubkey"])
        if list_pubkey_topic!=[]:
         frame3=tk.Frame(root)
         canvas = tk.Canvas(frame3,width=250)
         scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
         scrollable_frame = ttk.Frame(canvas,border=2)
         scrollable_frame.bind(
            "<Configure>",
                  lambda e: canvas.configure(
                  scrollregion=canvas.bbox("all")))
         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
         canvas.configure(yscrollcommand=scrollbar.set)
         ra=0
         sz=0
         s=5
                                            

         labeL_button=Label(scrollable_frame,text="Number of Pubkey "+str(len(list_pubkey_topic)),font=('Arial',12,'normal'))
         labeL_button.grid(row=0,column=1,padx=5,pady=5,columnspan=2)      

         while ra<len(list_pubkey_topic):
               lenght,note_p=pubkey_id(list_pubkey_topic[ra])
               sz=sz+1           
               if list_pubkey_topic[ra] in list(Pubkey_Metadata.keys()):
                  button_grid1=Label(scrollable_frame,text=f"{Pubkey_Metadata[list_pubkey_topic[ra]][0:15]} note {lenght}",width=20,font=('Arial',12,'normal'))
               else:
                  button_grid1=Label(scrollable_frame,text=f"{list_pubkey_topic[ra][0:9]} note {lenght}",width=20,font=('Arial',12,'normal'))
               button_grid1.grid(row=s,column=1,padx=2,pady=5,columnspan=1,rowspan=1)
               button_grid4=Button(scrollable_frame,text=f"❌ ", command= lambda val=list_pubkey_topic[ra]: add_pubkey_list(val),font=('Arial',12,'normal'))
               button_grid4.grid(row=s,column=2,padx=2,pady=5) 
               button_grid2=Button(scrollable_frame,text=f"Note ", command= lambda val=note_p: show_lst_ntd(val),font=('Arial',12,'normal'))
               button_grid2.grid(row=s+1,column=1,padx=2,pady=5) 
               if list_pubkey_topic[ra] in list(photo_profile.keys()):
                  if str(photo_profile[list_pubkey_topic[ra]])!=None: 
                     button_photo=Button(scrollable_frame, text="Photo ", command=lambda  val=str(photo_profile[list_pubkey_topic[ra]]): print_photo_url(val),font=('Arial',12,'normal'))
                     button_photo.grid(row=s+1, column=2, padx=2, pady=5)
              
               root.update_idletasks()  
           
               s=s+2
               ra=ra+1   
         if len(list_pubkey_topic)!=sz:
          labeL_button.config(text="Number of pubkey "+str(len(list_pubkey_topic))+"  "+"\n"+f"Number of poster "+ str(sz))
         canvas.pack(side="left", fill="y", expand=True)
         scrollbar.pack(side="right", fill="y")
         frame3.place(relx=0.01,rely=0.3,relwidth=0.27)
         
         def Close_print():
            frame3.destroy()  
         
         button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
         button_close_.pack(pady=5,padx=5)    
   

button_tag=tk.Button(root,text="# ",command=print_list_tag, font=('Arial',12,'bold'))
button_tag.place(relx=0.22,rely=0.005)   

def list_pubkey_id():
  pubkey_timeline()
  if timeline_people !=[]:
      
   metadata_note=search_kind(0)
   if metadata_note!=[]:
     try:  
      for single in metadata_note:
         if single not in db_list_note_follow:
            db_list_note_follow.append(single)
            note_text=single["content"].replace("\n", "\\n")  #some errors
            if isinstance(note_text,str):
             single_1=json.loads(note_text)
             if "name" in list(single_1.keys()):
               if single_1["name"]!="":
                  if single["pubkey"] not in list(Pubkey_Metadata.keys()):
                     Pubkey_Metadata[single["pubkey"]]=single_1["name"]
              
             else:   
               if "display_name" in list(single_1.keys()):
                  if single_1["display_name"]!="":
                     if single["pubkey"]not in list(Pubkey_Metadata.keys()):
                        Pubkey_Metadata[single["pubkey"]]=single_1["display_name"]    
         
             if "picture" in list(single_1.keys()):
               if single_1["picture"]!="":
                  if single["pubkey"] not in list(photo_profile.keys()):
                     if single_1["picture"]!="":
                        photo_profile[single["pubkey"]]=single_1["picture"]
                       
      print("Profile ",len(Pubkey_Metadata)," Profile with image ",len(photo_profile))  

     except KeyError as e:
          print("KeyError ",e) 
     except json.JSONDecodeError as b:
         print(b, single["content"])
     except NostrSdkError as c:
      print(c)     

           
def update_button():
   global value_max
   global value_min
   if int(entry_min.get())!=value_min:
      if int(entry_min.get())>=value_min and int(entry_min.get())<=value_max-1:
         value_min=int(entry_min.get())
   if  int(entry_max.get())!=value_max:
      if int(entry_max.get())>=value_max:
         value_max=int(entry_max.get())  


button_people_2=Button(root,text=f"Metadata user ", command=list_pubkey_id,font=('Arial',12,'bold'))
button_min=tk.Label(root,text=f"Min ",font=('Arial',12,'bold'),width=4)
button_max=tk.Label(root,text=f"Max ",font=('Arial',12,'bold'),width=4)
entry_min=tk.Entry(root,textvariable =value_min_int,font=('Arial',12,'bold'),width=5)
entry_max=tk.Entry(root,textvariable =value_max_int,font=('Arial',12,'bold'),width=5)
button_update=Button(root,text=f"Update", command=update_button,font=('Arial',12,'bold'))

def search_note():
   event=[]
   
   result=asyncio.run(Get_id(event))
   result_note=get_note(result)
    
   for result_x in result_note:
      if result_x not in db_note_list:
         db_note_list.append(result_x)
    
async def get_answers_Event(client, event_):
   
   f=Filter().kind(Kind(1)).limit(300)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   
   return z

async def get_list_Event(client):
   
   f=Filter().kind(Kind(1)).limit(200)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   
   return z

# list

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_search_list!=[]:
       
       for jrelay in relay_search_list:
          await client.add_relay(RelayUrl.parse(jrelay))
    else:
     await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
     await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
     await client.add_relay(RelayUrl.parse("wss://pyramid.fiatjaf.com/"))
    await client.connect()

    await asyncio.sleep(2.0)
    if event_==[]:
      
      resp_answer=await get_list_Event(client)
    else:
       
       resp_answer=await get_answers_Event(client, event_)
                                        
    return resp_answer    

button_close_search=tk.Button(root, text='Search Note',font=('Arial',12,'bold'), command=search_note) 
button_close_search.grid(column=1,row=5,pady=2,padx=10)

def pubkey_id(test):
   note_pubkey=[]
   for note_x in db_note_list:
       if note_x["pubkey"] == test:
          if note_x not in note_pubkey:
             note_pubkey.append(note_x)
   return len(note_pubkey),note_pubkey   

def print_people(): 
   if db_note_list!=[]:  
    if messagebox.askokcancel("Metadata user ","Yes/No") == True:
     list_pubkey_id()
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=250)
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
    button_min.place(relx=0.02,rely=0.2)
    button_max.place(relx=0.02,rely=0.24)
    entry_min.place(relx=0.06,rely=0.2)
    entry_max.place(relx=0.06,rely=0.24)
    button_update.place(relx=0.05,rely=0.15)
    s=1     
    
    test1=list_people_fun()
    if block_npub!=[]:
       for user in block_npub:
         if user in test1:
            test1.remove(user)
            
    ra=0
    sz=0
    labeL_button=Label(scrollable_frame,text="Number of pubkey "+str(len(test1)))
    labeL_button.grid(row=0,column=1,padx=5,pady=5,columnspan=2)           
    while ra<len(test1):
                lenght,note_p=pubkey_id(test1[ra])
                if lenght>value_min and lenght<value_max:
                 sz=sz+1           
                 if test1[ra] in list(Pubkey_Metadata.keys()):
                  button_grid1=Label(scrollable_frame,text=f"{Pubkey_Metadata[test1[ra]][0:15]} note {lenght}",width=20,font=('Arial',12,'normal'))
                 else:
                  button_grid1=Label(scrollable_frame,text=f"{test1[ra][0:9]} note {lenght}",width=20,font=('Arial',12,'normal'))
                 button_grid1.grid(row=s,column=1,padx=2,pady=5,columnspan=1,rowspan=1)
                 button_grid4=Button(scrollable_frame,text=f"❌ ", command= lambda val=test1[ra]: add_pubkey_list(val),font=('Arial',12,'normal'))
                 button_grid4.grid(row=s,column=2,padx=2,pady=5) 
                 button_grid2=Button(scrollable_frame,text=f"Note ", command= lambda val=note_p: show_lst_ntd(val),font=('Arial',12,'normal'))
                 button_grid2.grid(row=s+1,column=1,padx=2,pady=5) 
                 if test1[ra] in list(photo_profile.keys()):
                  if str(photo_profile[test1[ra]])!=None: 
                    button_photo=Button(scrollable_frame, text="Photo ", command=lambda  val=str(photo_profile[test1[ra]]): print_photo_url(val),font=('Arial',12,'normal'))
                    button_photo.grid(row=s+1, column=2, padx=2, pady=5)
                 root.update()  
              
                s=s+2
                ra=ra+1   
    
    labeL_button.config(text="Number of pubkey "+str(len(test1))+"  "+"\n"+f"Number of poster more than {value_min} note \n and less then {value_max}, "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
    button_people_2.place(relx=0.12,rely=0.16)
    button_people_3.place(relx=0.13,rely=0.21) 
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    
    label_nick.place(relx=0.75,rely=0.08)     
    entry_nick.place(relx=0.75,rely=0.12,relwidth=0.12,relheight=0.04) 
    button_close_1['command']=search_nickname
    button_close_1.place(relx=0.88,rely=0.12)
    frame3.place(relx=0.01,rely=0.28,relwidth=0.26, relheight=0.35)      

    def Close_print():
       frame3.destroy()
       Close_search()  
     
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)  
    
    def Close_search():
       button_close_find.place_forget()
       button_close_1.place_forget()
       entry_nick.place_forget()
       label_nick.place_forget()
       entry_nick.delete(0, END)

    button_close_find=tk.Button(root,text="🗙",command=Close_search, font=('Arial',12,'bold'),foreground="red")
    button_close_find.place(relx=0.9,rely=0.07)                               

button_close_1=Button(root, text="Find ",font=('Arial',12,'normal'), fg="blue")
label_nick=ttk.Label(root,text="Search Name", font=('Arial',12,'bold'))
entry_nick=ttk.Entry(root,justify='left', font=('Arial',12,'normal'))
button_people_=tk.Button(root,text="List of People",command=print_people, font=('Arial',12,'bold'))
button_people_.grid(row=5,column=2,pady=5,padx=10) 
label_image = Label(root,text="")

def search_nickname():
 if entry_nick.get()!="" and entry_nick.get() not in block_npub:
  Name_value=list(Pubkey_Metadata.values())
  Name_key=list(Pubkey_Metadata.keys())
  if entry_nick.get() in Name_value:
   for key_x in Name_key:
      if Pubkey_Metadata[key_x]==entry_nick.get():
           
         lenght,note_p= pubkey_id(key_x)
         entry_nick.delete(0, END)
         if lenght>value_min and lenght<value_max:
            return show_lst_ntd(note_p)
         else:
            if key_x in list(photo_profile.keys()):
               if str(photo_profile[key_x])!=None: 
                  return print_photo_url(str(photo_profile[key_x]))
               else:
                  if lenght==1:
                    return print(note_p)

  else:
     if len(entry_nick.get())==64:
        lenght_2,note_2=pubkey_id(entry_nick.get()) 
        if lenght_2>0:
           return show_lst_ntd(note_2)    
        else:
           Metadata=search_user(entry_nick.get())     
           if Metadata:
              if Metadata.as_record().display_name:         
               if entry_nick.get() not in list(Pubkey_Metadata.keys()):
                  Pubkey_Metadata[entry_nick.get()]=Metadata.as_record().display_name
              else:
                 if Metadata.as_record().name:         
                  if entry_nick.get() not in list(Pubkey_Metadata.keys()):
                     Pubkey_Metadata[entry_nick.get()]=Metadata.as_record().name
              if  Metadata.as_record().picture:   
                  if entry_nick.get() not in list(photo_profile.keys()):
                     photo_profile[entry_nick.get()]=Metadata.as_record().picture
        entry_nick.delete(0, END)
        
def print_photo_url(url):
   if url!="":
     try: 
      headers = {"User-Agent": "Mozilla/5.0"}
      response = requests.get(url, headers,stream=True)
      response.raise_for_status()
      if response.ok==TRUE:
         with open('my_image.png', 'wb') as file:
            shutil.copyfileobj(response.raw, file)
         del response
         from PIL import Image
     
         image = Image.open('my_image.png')
         image.thumbnail((250,150))  # Resize image if necessary
         photo = ImageTk.PhotoImage(image)
         label_image.config(image=photo)
         label_image.image_names= photo 
         label_image.place(relx=0.1,rely=0.7)     
       
      def close_image():
        label_image.place_forget()         
        button_photo_close.place_forget()
    
      button_photo_close=Button(root, text="X", command=close_image,font=('Arial',12,'normal'))
      button_photo_close.place(relx=0.15,rely=0.65)
      label_image.place(relx=0.1,rely=0.7)       
     except TypeError as e: 
            print(e)  
     except requests.exceptions.RequestException as b:
         print(f"Error exceptions: {b}")  

def show_lst_ntd(list_note_p):
 frame2=tk.Frame(root)  
 canvas_1 = tk.Canvas(frame2,width=800)
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
  if list_note_p[0]["pubkey"] not in block_npub:
   
   s=1
   s1=0
   for note in list_note_p:
         
      try:
       if note['pubkey'] in list(Pubkey_Metadata.keys()):
         
         context0="Nickname " +Pubkey_Metadata[note["pubkey"]]
       else: 
         context0="Author: "+note['pubkey']
      
       context1=note['content']+"\n"
       context2=" Minutes "+str(int(float(int(time.time())-note["created_at"])/(60)))+"\n"
       context3=str("")
       if note['tags']!=[]: 
        
        if tags_string(note,"e")!=[]:
              if four_tags(note,"e"):
                for F_note in four_tags(note,"e"):
                   if len(F_note)>3:  
                     context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
        
        
        if tags_string(note,"alt")!=[]:
         for xnote in tags_string(note,"alt"):
          context2=context2+"\n"+"Alt "+str(xnote) +"\n"
        if tags_string(note,"a")!=[]:  
         for ynote in tags_string(note,"a"):
          context2=context2+"\n"+"A tag reply "+str(ynote) +"\n" 
        if tags_string(note,"p")!=[]: 
         tag_peple="" 
         
         for znote in tags_string(note,"p"):
            if znote in list(Pubkey_Metadata.keys()):
               tag_peple= tag_peple+" p " +Pubkey_Metadata[znote]+"\n"
            else: 
               tag_peple= tag_peple+" p " +str(znote)+"\n"
            
         context3=context3+"Tag "+"\n"+str(tag_peple) +"\n"   
       
        if tags_string(note,"t")!=[] :
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context3=context3+"#"+str(xnote) +" "
            s=s+1
        
          
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=8, width=30, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,str(context2)+"\n"+context1+"\n"+context3)
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=1) 
      
       def print_id(entry):
            show_print_test_tag(entry)
                       
            
              
       def print_var(entry):
                print(entry)

                                                                                                  
       button=Button(scrollable_frame_1,text=f"Print note", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read ", command=lambda val=note: print_id(val))
       button_grid2.grid(row=2,column=s1+1,padx=5,pady=5)    
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

   scrollbar_1.pack(side="bottom", fill="x",padx=5)
   scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
   canvas_1.pack( fill="y", expand=True)
   frame2.place(relx=0.28,rely=0.28,relwidth=0.62,relheight=0.35)

   def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
    
   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.91,rely=0.32)      

def search_user(pubkey):
    if __name__ == "__main__":
       single_results = asyncio.run(feed_metadata(pubkey))
       if single_results:
          return single_results

def search_kind(x):
   if __name__ == "__main__":
    # Example usage with a single key
    
    single_results = asyncio.run(feed_cluster([Kind(x)]))
   Z=[]
   note=get_note(single_results)
   for r in note:
      if (r)['kind']==x:
         Z.append(r)
   return Z       

async def feed_metadata(pubkey):
       
    client = Client(None)
    add_relay_list.clear()
    list_add_relay=["wss://nos.lol/","wss://nostr.mom/","wss://nostr-pub.wellorder.net/"]
    await Search_status(client=Client(None),list_relay_connect=list_add_relay)
    if list_add_relay!=[]:
       for x_relay in list_add_relay:
          if x_relay not in relay_list:
             relay_list.append(x_relay)
    if relay_list!=[]:
      
       for relay_j in relay_list:
           if RelayUrl.parse(relay_j) not in add_relay_list:
                add_relay_list.append(RelayUrl.parse(relay_j))
                await client.add_relay(RelayUrl.parse(relay_j))
    
    await client.connect()
    await asyncio.sleep(2.0)

    combined_results = await client.fetch_metadata(PublicKey.parse(pubkey),timeout=timedelta(seconds=10))
    return combined_results

async def get_note_cluster(client, type_of_event):
    if timeline_people!=[]:
     f = Filter().kinds(type_of_event).authors(user_convert(timeline_people)).limit(1000)
    else:
       f = Filter().kinds(type_of_event).limit(1000)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def feed_cluster(type_of_event):
    # Init logger
    init_logger(LogLevel.INFO)
   
    client = Client(None)
   
    add_relay_list.clear()
    list_add_relay=["wss://nos.lol/","wss://nostr.mom/"]
    await Search_status(client=Client(None),list_relay_connect=list_add_relay)
    if list_add_relay!=[]:
      for x_relay in list_add_relay:
         if x_relay not in relay_list:
            relay_list.append(x_relay)
    if relay_list!=[]:
      for relay_j in relay_list:
         if RelayUrl.parse(relay_j) not in add_relay_list:
               add_relay_list.append(RelayUrl.parse(relay_j))
               await client.add_relay(RelayUrl.parse(relay_j))
    await client.connect()
    await asyncio.sleep(2.0)

    combined_results = await get_note_cluster(client, type_of_event)
    return combined_results

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
   if note['pubkey'] in list(Pubkey_Metadata.keys()):
      var_id_3.set("Nickname " +Pubkey_Metadata[note["pubkey"]])
   else: 
      var_id_3.set("Author: "+note["pubkey"])
   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid( sticky = NS,column=4,row=s+1)
   second_label_10 = tk.Text(scrollable_frame_2, padx=5, height=3, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'normal'),background="#D9D6D3")
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
         if entry["tags"]!=[]:
            if tags_str(entry,"imeta")!=[]:
               photo_list_frame_2(entry)
            else:
               if tags_string(entry,"r"):
                  photo_r(entry)
               else:   
                  print(entry["tags"])        
            
   def print_content(entry):
       result=show_note_from_id(entry)
       if result!=None: 
        z=5
        for jresult in result:
           if jresult["id"]!=entry["id"]:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=270,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,padx=8,row=z,column=0, columnspan=3)
             if jresult['pubkey'] in list(Pubkey_Metadata.keys()):
               var_id_r.set("Nickname " +Pubkey_Metadata[jresult["pubkey"]])
             else: 
               var_id_r.set("Pubkey: "+jresult["pubkey"])
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, padx=8, height=3, width=24, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             context22="---> tags: <--- "+"\n"   
             if tags_string(jresult,"e")!=[]:
              if four_tags(jresult,"e"):
                for F_note in four_tags(note,"e"):
                     context22=context22+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              
             else:
               context22="\n ---> Root  <--- "  
             second_label10_r.insert(END,jresult["content"]+"\n"+str(context22))
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=10, column=0, columnspan=3, row=z+1) 
             if tags_string(jresult,"e")!=[]:
               button_grid31=Button(scrollable_frame_2,text=f"Read reply ", command=lambda val=jresult: print_content(val))
               button_grid31.grid(row=z+2,column=2,padx=5,pady=5)  
             else:    
               button_grid32=Button(scrollable_frame_2,text=f"Print note", command=lambda val=jresult: print(val))
               button_grid32.grid(row=z+2,column=1,padx=5,pady=5)  
             button_p=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=jresult: print_var(val))
             button_p.grid(column=0,row=z+2,padx=5,pady=5)  
               
                   
           z=z+3
   def print_root(note):
    e_id=[]
    if tags_string(note,"e")!=[]:
     for e_event in tags_string(note,"e"):
      e_id.append(e_event)
    if e_id!=[]:
     result= get_note(asyncio.run(Get_event_id(e_id)))   #list
    else:
     result= get_note(asyncio.run(Get_event_id(note["id"]))) 
    s=5
    if result!=None and result!=[]: 
      print(len(result))
      for jresult in result:
        context11=jresult['content']+"\n"
 
        if jresult['tags']!=[]:
                context00="npub: "+jresult['pubkey'][0:9]
                context22="[[ Tags ]]"+"\n"
                for tag_test in (jresult)["tags"]:
                  context22=context22+str(tag_test)+"\n"
  
        else: 
            context00="npub: "+jresult['pubkey']+"\n"+"id: "+jresult["id"]+"\n"
            context11=+jresult['content']+"\n"
            context22=""
        var_id_1=StringVar()
        label_id_1 = Message(scrollable_frame_2,textvariable=var_id_1, relief=RAISED,width=310,font=("Arial",12,"normal"))
        var_id_1.set(context00)
        label_id_1.grid(pady=2,column=0, columnspan=3,row=s) 
        scroll_bar_mini_o = tk.Scrollbar(scrollable_frame_2)
        scroll_bar_mini_o.grid( sticky = NS,column=4,row=s+1,pady=5)
        second_label_0 = tk.Text(scrollable_frame_2, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini_o.set, font=('Arial',14,'bold'),background="#D9D6D3")
        second_label_0.insert(END,context11+"\n"+str(context22))
        scroll_bar_mini_o.config( command = second_label_0.yview )
        second_label_0.grid(padx=5, column=0, columnspan=3, row=s+1) 
        s=s+3

   button=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val))
   button.grid(column=0,row=s+2,padx=5,pady=5)
     
   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Read reply ", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    
   else:
      button_grid3=Button(scrollable_frame_2,text=f"Read Rootply", command=lambda val=note: print_root(val))
      button_grid3.grid(row=s+2,column=2,padx=5,pady=5)         
   scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
   canvas_2.pack( fill="y", expand=True)
   def close_frame():
      button_frame.place_forget()
      frame3.destroy()    

   button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame.place(relx=0.6,rely=0.05) 
   frame3.place(relx=0.3,rely=0.001,relheight=0.25,relwidth=0.3)    

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

async def get_notes_(client, e_ids):
     f = Filter().ids([EventId.parse(e_id) for e_id in e_ids])
     events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))
     z = [event.as_json() for event in events.to_vec() if event.verify()]
     return z

async def get_reply_note(client, e_id):
    f = Filter().event(EventId.parse(e_id)).kind(Kind(1))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10)) 
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def Get_event_id(e_id):
    # Init logger
    init_logger(LogLevel.INFO)
    
    client = Client(None)
    if relay_list!=[]:
       
       for jrelay in relay_list:
         relay_url = RelayUrl.parse(jrelay)
         await client.add_relay(relay_url)
    else:
     relay_url_1 = RelayUrl.parse("wss://nos.lol/")
     await client.add_relay(relay_url_1)
     relay_url_x = RelayUrl.parse("wss://nostr.mom/")
     await client.add_relay(relay_url_x)
     relay_url_2 = RelayUrl.parse("wss://purplerelay.com/")
     await client.add_relay(relay_url_2)

    
    await client.connect()

    await asyncio.sleep(2.0)

    if isinstance(e_id, list):
         print("list")
         test_id = await get_notes_(client,e_id)
    else:
        print("str")
        test_id = await get_reply_note(client,e_id)
       
    return test_id

def photo_list_frame_2(note):
 frame_pic=tk.Frame(root,height=80,width= 80) 
 
 balance,list_note1=balance_photo_print(note)
 int_var=IntVar()
 lbel_var=Entry(frame_pic, textvariable=int_var)    
 if list_note1!=[]: 
  if list_note1!=None and balance!=None:
   stringa_pic=StringVar()

   def next_number():
      if int((int(lbel_var.get())+1))< len(list_note1):
       int_var.set(int(lbel_var.get())+1)
       print_photo()
      else:
          int_var.set(int(0)) 
          print_photo()
     
   def print_photo():
     s=0  
     stringa_pic.set(list_note1[int(lbel_var.get())])
     label_pic = Entry(frame_pic, textvariable=stringa_pic)
     image_label = tk.Label(frame_pic)
     image_label.grid(column=1,row=s, columnspan=2)
     if label_pic.get()!="":
      if codifica_link_(label_pic.get())=="pic":   
       
       try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(label_pic.get(),headers=headers, stream=True)
       
        response.raise_for_status()  
        
   
        if response.ok==TRUE:
         with open('my_image.png', 'wb') as file:
          shutil.copyfileobj(response.raw, file)
         del response
         from PIL import Image,UnidentifiedImageError
         image = Image.open('my_image.png','r')
        
         if balance!=[]:
          number=balance[int(lbel_var.get())]
         else:
           number=float(image.width//image.height) 
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
         button_close.grid(column=2,columnspan=1,row=s+1,pady=5)
         button_close_photo=Button(frame_pic,command=close_one_pic,text="Next",font=("Arial",12,"bold"))
         button_close_photo.grid(column=1,row=s+1,pady=5)
         s=s+2
       except TypeError as e: 
            print(e)  
       except requests.exceptions.RequestException as e:
        print(f"Error exceptions: {e}")  
      else:
          print(label_pic.get())
   print_photo()
   frame_pic.place(relx=0.3,rely=0.3,relwidth=0.3) 
  else:
     print("error", "none")        
 else:
     print("error", note["tags"])

def url_link(url):
 z=url
 if z[0:5]=="https":
        return str(z)

def codifica_link_(url):
   f=url_link(url)
   list_video=['mov','mp4']
   audio=['mp3']
   img=['jpg','png','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_video:
        return "video"
   if f[-3:] in audio:
        return "audio"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam"
   
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

def more_link(f):
   
   list_video=['mov','mp4']
   img=['png','jpg','gif']
   img1=['jpeg','webp'] 
   if f==None:
                 return "no spam"
   if f[-3:] in list_video:
        return "video"
   if f[-3:] in img:
           return "pic" 
   if f[-4:] in img1:
            return "pic"
   else:
       return "spam"    

def photo_r(note):
   if tags_str(note,"r")!=[]:
      link_0=tags_string(note,"r")[0]
      if codifica_link_(link_0)=="pic":
        try: 
         headers = {"User-Agent": "Mozilla/5.0"}
         response = requests.get(link_0,headers=headers, stream=True)
         response.raise_for_status()  
         with open('my_image.png', 'wb') as file:
            shutil.copyfileobj(response.raw, file)
         del response
         from PIL import Image,UnidentifiedImageError
         image = Image.open('my_image.png','r')
         number=float(image.width//image.height) 
         test1=int(float(number)*250)
         if test1>400:
            test1=int(400)
         if test1<150:
            test1=int(160)   
         image.thumbnail((test1, 250))  # Resize image if necessary
         photo = ImageTk.PhotoImage(image)
         image_label_2.config(image=photo)
         image_label_2.image_names= photo
         image_label_2.place(relx=0.3,rely=0.3,relwidth=0.3) 

         def close():
            pass
         button_close_photo=Button(root,command=close,text="close",font=("Arial",12,"bold"))
         button_close_photo.place(relx=0.35,rely=0.25) 
        except TypeError as e: 
            print(e)  
        except requests.exceptions.RequestException as b:
            print(f"Error exceptions: {b}")   

image_label_2=Label(root)

def relay_class():
          if entry_relay.get()!="":
            if entry_relay.get()[0:6]=="wss://" and entry_relay.get()[-1]=="/" and len(entry_relay.get())>7:
                
                if entry_relay.get() not in relay_list:
                    relay_list.append(entry_relay.get())
                add_relay_str.set("wss:// ")    
                counter_relay['text']=str(len(relay_list)) 
                counter_relay.place(relx=0.2,rely=0.1, relheight=0.04)
            else:
               print(entry_relay.get())   
            entry_relay.delete(0, END)
            add_relay_str.set("wss:// ") 


relay_button = tk.Button(root, text="Add Relay ", font=("Arial",12,"normal"),background="grey", command=relay_class)
counter_relay=Label(root,text="",background="darkgrey",font=('Arial',12,'normal'))
add_relay_str=StringVar()
entry_relay=ttk.Entry(root,justify='left',font=("Arial",12,"bold"),width=12,textvariable=add_relay_str)
add_relay_str.set("wss:// ")
entry_relay.place(relx=0.02,rely=0.09)
relay_button.place(relx=0.12,rely=0.08)   

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
                        if stats.bytes_received()>0:  #Auth ort other stuff
                           if str(url) in list_relay_connect:
                            list_relay_connect.remove(str(url))
                            break
                        if stats.success()==0 and relay.is_connected()==False:
                            if str(url) in list_relay_connect:
                                list_relay_connect.remove(str(url))
                        
                    i=i+1 
    except IOError as e:
        print(e) 
    except ValueError as b:
        print(b)                   

def user_not_in_list(): 
   frame3=tk.Frame(root)
   canvas = tk.Canvas(frame3,width=250)
   scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
   scrollable_frame = ttk.Frame(canvas)
   scrollable_frame.bind("<Configure>",lambda e: canvas.configure(
        scrollregion=canvas.bbox("all") ))
    
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
               if lenght>=value_max:
                  sz=sz+1           
                  if test1[ra] in Pubkey_Metadata.keys():
                     button_grid1=Label(scrollable_frame,text=f"{Pubkey_Metadata[test1[ra]][0:15]} note {lenght}",width=20,font=('Arial',12,'normal'))
                  else:
                     button_grid1=Label(scrollable_frame,text=f"{test1[ra][0:9]} note {lenght}",width=20,font=('Arial',12,'normal'))
                  button_grid1.grid(row=s,column=1,padx=2,pady=5,columnspan=1,rowspan=2)
                  button_grid2=Button(scrollable_frame,text=f"Note ", command= lambda val=note_p: show_lst_ntd(val),font=('Arial',12,'normal'))
                  button_grid2.grid(row=s,column=2,padx=2,pady=5) 
                  if test1[ra] in list(photo_profile.keys()):
                     if str(photo_profile[test1[ra]])!=None: 
                        button_photo=Button(scrollable_frame, text="Photo ", command=lambda  val=str(photo_profile[test1[ra]]): print_photo_url(val),font=('Arial',12,'normal'))
                        button_photo.grid(row=s+1, column=2, padx=2, pady=5)
                  
               root.update_idletasks()           
               s=s+2
               ra=ra+1   
    
   labeL_button.config(text="Number of pubkey "+str(len(test1))+"  "+"\n"+f"Number of posters with more notes than {value_max}, "+ str(sz)) 
   canvas.pack(side="left", fill="y", expand=True)
 
   if sz>2:
     scrollbar.pack(side="right", fill="y")  
    
   frame3.place(relx=0.01,rely=0.65,relwidth=0.26, relheight=0.3)      

   def Close_print():
      frame3.destroy()
         
     
   button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
   button_close_.pack(pady=5,padx=5)  
    
button_people_3=Button(root,text=f"Not in list ", command=user_not_in_list,font=('Arial',12,'bold'))

#second blob

label_npub_block1 = tk.Label(root, text="Selected: ",font=("Arial",12,"bold"))

def search_block_list():
   label_npub_block1["text"]="Selected: "+str(len(block_npub))
            
def delete_block_pubkey(pubkey_hex:str): 
   if pubkey_hex in block_npub:
      block_npub.remove(pubkey_hex)
   
   label_npub_block1["text"]="Selected: "+str(len(block_npub)) #Optimistic UI
   
block_npub=["592295cf2b09a7f9555f43adb734cbee8a84ee892ed3f9336e6a09b6413a0db9"]

def add_pubkey_list(pubkey_test:str):
   
      try:
         test_user=PublicKey.parse(pubkey_test)
         if test_user.to_hex() not in block_npub:
            block_npub.append(test_user.to_hex())
            search_block_list()
            
      except NostrSdkError as e:
            print(e)
            
def Block_space():
   if block_npub!=[]: 
      frame1=Frame(root, width=200, height=50)
      canvas = Canvas(frame1, width=150, height=30)
      canvas.pack(side="left", fill=BOTH, expand=True)

      scrollbar = Scrollbar(frame1, orient=VERTICAL, command=canvas.yview)
   
      canvas.configure(yscrollcommand=scrollbar.set)
      canvas.bind(
         "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
      scrollbar.pack(side=RIGHT, fill=Y)
            
      scrollable_frame = Frame(canvas)
      canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
      def create_note(block_n, s):
         # Message 
         message = Message(scrollable_frame, text="npub: "+block_n, width=180)
         message.grid(row=s, column=0, columnspan=3, padx=10, pady=5, sticky="w")
         # Button down
         Button(scrollable_frame, text="Result", command=search_block_list).grid(row=s + 1, column=0, padx=5, pady=5)
         blo_label = Button(scrollable_frame, text="Restore", command=lambda: delete_block_pubkey(block_n))
         blo_label.grid(row=s + 1, column=1, padx=5, pady=5)
         Button(scrollable_frame, text="Print Npub", command=lambda val=block_n: print(PublicKey.parse(val).to_bech32())).grid(row=s + 1, column=2, padx=5, pady=5)
    
      s = 1
      for nblock in block_npub: 
         create_note(nblock, s)
         s += 2   
      label_npub_block1.place(relx=0.9,rely=0.02 )
      frame1.place(relx=0.7,rely=0.65, relheight=0.25,relwidth=0.25)  
    
      def close_canvas():
        scrollable_frame.forget()
        canvas.destroy()
        frame1.destroy()
        Check_mod.set("0")
        label_npub_block1.place_forget()
        button_mod_npub.place_forget()

      if block_npub==[]:
         close_canvas()    
       
      button_close=Button(scrollable_frame, command=close_canvas, text="Close X",font=('Arial',12,'normal') )
      button_close.grid(column=1,row=0, padx=5,pady=5)  

      def Moderate_option():
         def add_npub_to_list():
            if len(stringa_block.get())==64 or len(stringa_block.get())==63 or len(stringa_block.get())==69:
               try:
                  test_user=PublicKey.parse(stringa_block.get())
                  if test_user.to_hex() not in block_npub:
                     block_npub.append(test_user.to_hex())
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

         Frame_block=Frame(root,width=55, height=10)
         stringa_bloc=StringVar()   
    
         stringa_block=Entry(Frame_block,textvariable=stringa_bloc,font=('Arial',12,'normal'),width=10)
         stringa_block.grid(column=0,row=1,padx=5,pady=5)
         random_block=Button(Frame_block, command=add_npub_to_list, text= "block npub",background="darkgrey",font=('Arial',12,'normal'))
         random_block.grid(column=1,row=1,padx=5,pady=5)
         label_string_block=StringVar()
         label_block=Label(Frame_block, textvariable=label_string_block,background="darkgrey",font=('Arial',12,'normal'))
         label_block.grid(column=2,row=1,padx=5,pady=5)
        
         def Close_block(event):
            Frame_block.place_forget()
        
         button_b_close=Button(Frame_block, background='red', text='❌',font=('Arial',12,'bold'))    
         button_b_close.bind("<Double-Button-1>" ,Close_block)
         button_b_close.grid(column=3, row=0, padx=5, rowspan=2) 
         Frame_block.place(relx=0.70,rely=0.88)
    
      button_mod_npub=Button(root, command=Moderate_option, 
                   text="--->",
                    highlightcolor='WHITE',border=2, 
                  font=('Arial',12,'bold'))
      button_mod_npub.place(relx=0.65,rely=0.88,relheight=0.05)
    
button_block_npub=Button(root, command=Block_space, 
                   text="Moderation",
                    highlightcolor='WHITE',
                  width=10,height=1,border=2, cursor='hand1',
                  font=('Arial',14,'bold'))
Check_mod = IntVar()
Check_right =IntVar(root,0,"test")

def state_sidebar():
   if Check_right.get()==1:
    Check_right.set(0)
    button_block_npub.place_forget()
   else:
     Check_right.set(1)
     button_block_npub.place(relx=0.8,rely=0.01)
     

sidebar_right = Button(root, text = "...", command=state_sidebar,font=('Arial',14,'bold'))
sidebar_right.place(relx=0.75,rely=0.01)  

root.mainloop()