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

def list_pubkey_id():
  pubkey_timeline()
  if timeline_people !=[]:
      
   metadata_note=search_kind(0)
   if metadata_note!=[]:
       for single in metadata_note:
        if single not in db_list_note_follow:
           db_list_note_follow.append(single)
        single_1=json.loads(single["content"])
        try:
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
                       
                        
        except KeyError as e:
          print("KeyError ",e) 
       print("Profile ",len(Pubkey_Metadata)," Profile with image ",len(photo_profile))       

button_people_2=Button(root,text=f"Metadata user ", command=list_pubkey_id,font=('Arial',12,'bold'))

def search_note():
   event=[]
   if __name__ == "__main__":
    result=asyncio.run(Get_id(event))
    result_note=get_note(result)
    print(len(result_note))
    for result_x in result_note:
       if result_x not in db_note_list:
          db_note_list.append(result_x)
    
async def get_answers_Event(client, event_):
   
    f=Filter().kind(Kind(1)).limit(300)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    #print(f.as_json(),len(z))
    return z

async def get_list_Event(client):
   
    f=Filter().kind(Kind(1)).limit(200)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    #print(f.as_json(),len(z))
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
      print("ok")
      resp_answer=await get_list_Event(client)
    else:
       print("2")
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
                 root.update()  
              
                s=s+2
            
                ra=ra+1   
    labeL_button.config(text="Number of pubkey "+str(len(test1))+"  "+"\n"+"Number of poster more than one note "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
    button_people_2.place(relx=0.1,rely=0.2) 
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.01,rely=0.28,relwidth=0.26, relheight=0.35)      

    def Close_print():
       frame3.destroy()  
             
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

button_people_=tk.Button(root,text="List of People",command=print_people, font=('Arial',12,'bold'))
button_people_.grid(row=5,column=2,pady=5,padx=10) 
label_image = Label(root,text="")

def print_photo_url(url):
   if url!="":
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers,stream=True)
    response.raise_for_status()
    
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
  
  s=1
  s1=0
  
  for note in list_note_p:
         
      try:
       if note['pubkey'] in list(Pubkey_Metadata.keys()):
         
         context0="Nickname " +Pubkey_Metadata[note["pubkey"]]
       else: 
         context0="Author: "+note['pubkey']
      
       context1=note['content']+"\n"
       context2=" Minutes "+str(round(float(int(time.time())-note["created_at"])/(60),4))+"\n"
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
            
         context3=context3+"\n"+"Tag "+str(tag_peple) +"\n"   
       
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
  button_frame.place(relx=0.7,rely=0.66,relwidth=0.1)      


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
    #uniffi_set_event_loop(asyncio.get_running_loop())
    add_relay_list.clear()
    if relay_list!=[]:
       
       for relay_j in relay_list:
           if RelayUrl.parse(relay_j) not in add_relay_list:
                add_relay_list.append(RelayUrl.parse(relay_j))
                await client.add_relay(RelayUrl.parse(relay_j))
    relay_url_1 = RelayUrl.parse("wss://nos.lol/")
    if relay_url_1 not in add_relay_list:
       add_relay_list.append(relay_url_1)
       await client.add_relay(relay_url_1)
    relay_url_x = RelayUrl.parse("wss://nostr.mom/")
    relay_url_2 = RelayUrl.parse("wss://nostr-pub.wellorder.net/")
    if relay_url_x not in add_relay_list:
       add_relay_list.append(relay_url_x)
       await client.add_relay(relay_url_x)
    if relay_url_2 not in add_relay_list:
       add_relay_list.append(relay_url_2)
       await client.add_relay(relay_url_2)
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
   frame_pic.place(relx=0.6,rely=0.01,relwidth=0.3) 
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
      image_label_2.place(relx=0.6,rely=0.01,relwidth=0.3) 

      def close():
         pass
      button_close_photo=Button(root,command=close,text="close",font=("Arial",12,"bold"))
      button_close_photo.place(relx=0.92,rely=0.01,relwidth=0.3) 

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
entry_relay.place(relx=0.02,rely=0.11)
relay_button.place(relx=0.12,rely=0.1)   

root.mainloop()