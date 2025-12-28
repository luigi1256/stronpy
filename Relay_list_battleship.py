import asyncio
from nostr_sdk import *
from datetime import timedelta
import json
import requests
import shutil
from PIL import Image, ImageTk
import time

dict_pubkey_relay={}
less_pubkey_relay={}
db_note_list=[]

def get_note(z):
    f=[]
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

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
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
    zeta=[]
    if __name__ == "__main__":
        single_author = user 
        single_results = asyncio.run(main(single_author,x))
        note=get_note(single_results)
        for r in note:
            if (r)['kind']==x:
                zeta.append(r)
    return zeta

def search_kind_list(list_follow,x):
    note=note_list(list_follow,x)
    Z=[]
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z

def note_list(list_follow,x):
    let=[]
    if __name__ == "__main__":
        test_people = list_follow
        combined_results = asyncio.run(main(test_people,x))
        let=get_note(combined_results)
    return let

def relay_t(x):
    """Write Relays"""
    i=0
    c=[]
    relays=tags_str(x,'r')
    j=len(relays)
    while i<j:
        if len(relays[i])>2:
            if relays[i][2]=="write":
                c.append(relays[i][1])
        else:
            c.append(relays[i][1])
        i=i+1
         
    return c

def relay_v(x):
    """Read Relays"""
    i=0
    c=[]
    relays=tags_str(x,'r')
    j=len(relays)
    while i<j:
        if len(relays[i])>2:
            if relays[i][2]=="read":
                c.append(relays[i][1])
        else:
            c.append(relays[i][1])
        i=i+1
         
    return c

def list_battle(list_one):
    wu=[]
    zeta=[]
    c=[]
    list_10002_pubkey=[]
    
    User=user_convert(list_one)
    print("User", " ",len(User))
    zeta=search_kind_list(User,10002)
    for v in zeta:
        db_note_list.append(v)
        wu.append(relay_t(v))
    print(len(zeta)) 
    for z_z in zeta:
        if z_z["pubkey"] not in list_10002_pubkey:
            list_10002_pubkey.append(z_z["pubkey"])
            i=0
            relay_npub=[]
            relays=tags_str(z_z,'r')
            j=len(relays)
            while i<j:
                if len(relays[i])>2:
                    if relays[i][2]=="write":
                        relay_npub.append(relays[i][1])
                        c.append(relays[i][1])
                else:
                    relay_npub.append(relays[i][1])
                    c.append(relays[i][1])
                i=i+1
            dict_pubkey_relay[z_z["pubkey"]]=relay_npub
            if len(relay_npub)<5:
                less_pubkey_relay[z_z["pubkey"]]=relay_npub
      
    list_people= list(dict_pubkey_relay.keys())
    
    print("relay list ",len(zeta),"unique publickey ",len(list_10002_pubkey),"\n"," list normal ", len(dict_pubkey_relay),"\n","list less 5 relays ",len(less_pubkey_relay))
    
    return wu

import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox

root = tk.Tk()
root.geometry("1300x800")

#frame_login

frame_login=Frame(root, width=50, height=50)
stringa_=tk.IntVar()
label_name=Label(frame_login,text="Insert a Pubkey: ",font=("Arial",16,"normal"))
label_name.grid(column=0,row=0)
Text_base = tk.Text(frame_login, height=2, width=35,font=("Arial",16,"normal"))
Text_base.grid(row=1, column=0, padx=30,columnspan=3,ipadx=10)
frame_login.grid(columnspan=3,rowspan=3)

#frame_relay
frame_relay=Frame(root,width=100, height=50)
label_relay=Label(frame_relay,text="Show Relays: ",font=("Arial",16,"normal"))
label_relay.grid(column=0,row=0)
scroll_bar_mini = tk.Scrollbar(frame_relay)

Text_relay = tk.Text(frame_relay, height=10, width=50, yscrollcommand = scroll_bar_mini.set)
scroll_bar_mini.config( command = Text_relay.yview )
Text_relay.grid(row=1, column=0,padx=30, columnspan=3,ipadx=10)
scroll_bar_mini.grid( sticky = NS,column=4,row=1,pady=5)
frame3=tk.Frame(root,height=20,width= 80)
frame4=tk.Frame(root,height=20,width= 80)
Checkbutton5 = IntVar() 
check_relay=Checkbutton(frame_relay, text = "+ kind 3", variable = Checkbutton5, onvalue = 1, 
                    offvalue = 0, height = 2, width = 10)
check_relay.grid(column=1,row=0)

def to_follows(x,y):
    h=[]
   
    for j in x:
        if j in y:
            h.append(j)
    return h

def npub_class():
    if len(Text_base.get("1.0","end-1c"))==63:
        Npub=PublicKey.parse(Text_base.get("1.0","end-1c"))
        return Npub
    if len(Text_base.get("1.0","end-1c"))==64:
        Npub=PublicKey.parse(Text_base.get("1.0","end-1c"))
        return Npub

def relay_print():
    if npub_class()!=None:
        z=search_kind(npub_class(),3)
        people=tags_string(z[0],'p') 
        result=list_battle(people)
        return result

def outrageous():
    i=0
    j=1
    Pu=[]
    test=[]
    Wu=relay_print()
    if Wu:
        z=len(Wu)
        while j<z:
            t=to_follows(Wu[i],Wu[j])
            if t!=[]:
                Pu.append(t)
            i=i+2
            j=j+2
    
    for y in Pu:
        for v in y:
         if v not in test:
            test.append(v)
    relay_simil=[]
    for j in test:
        if j+str("/") not in test:
            relay_simil.append(j)
    return relay_simil

def stamp_relay():
    if npub_class()!=None:
        relays=outrageous()
        if relays!=[]:
                
                if Text_relay.get("1.0","end-1c")!="":
                    Text_relay.delete("1.0","end")
                    for relay in relays:
                        Text_relay.insert(END," Relay: "+relay +"\n")
                else:
                    for relay in relays:    
                        Text_relay.insert(END," Relay: "+relay+"\n")  

        else:
            print("None")            

def list_battle_():
    Wu=[]
    zeta=[]
    veta=[]
    list=people()
    User=user_convert(list)
    z=search_kind_list (User,10002)
    if z!=None and z!=[]:
        for h in z:   
            zeta.append(h)
             
    z2=search_kind_list(User,3)
    if z2!=[]:
        for h2 in z2:   
            veta.append(h2)    
    for v in zeta:
        Wu.append(relay_t(v))
    for c in veta:
        Wu.append(relay_c(c))  
    return Wu

def relay_choice_List(list_relay):
    relay_n=[]
    relay=[]
    for list_one_relay in list_relay:
        for j in list_one_relay:
            s,l=where_is(j,list_relay)
            for x in l:
                if l not in relay_n:
                    relay_n.append(l)
                    relay.append(j)
    relay_simil=[]
    for j in relay:
        if j+str("/") not in relay:
            relay_simil.append(j)
    return relay_simil

def stamp_relay_all():
   if npub_class()!=None: 
        rellays=list_battle_()
        relays_connect=[]
        for rel in rellays:
            if rel!=[] and rel!=None:
                relays_connect.append(rel)
        relays=relay_choice_List(relays_connect)
        if relays!=None and relays!=[]:
       
            if Text_relay.get("1.0","end-1c")!="":
                Text_relay.delete("1.0","end")
                Text_relay.insert(END,"More Relay, kind 3, kind 10002"  +"\n")
                for relay in relays:
                   if relay!=[] and relay!=None: 
                    Text_relay.insert(END," Relay: "+str(relay) +"\n")
            else:
                Text_relay.insert(END,"More Relay, kind 3, kind 10002"  +"\n")
                for relay in relays:  
                    if relay!=[] and relay!=None:   
                        Text_relay.insert(END," Relay: "+str(relay)+"\n")  

        else:
            print("None",relays)           

def where_is(wss,Wu):
    i=0
    s=0
    l=[]
    while i<len(Wu):
        j=0
        while j<len(Wu[i]):
            if wss == Wu[i][j]:
                s=s+1
                l.append(i)
            j=j+1
            
        i=i+1
    return s,l

def people():
    if npub_class()!=None: 
        z=search_kind(npub_class(),3)
        people=tags_string(z[0],'p') 
        return people
  
def relay_c(x):
    
    if x['content']!="":
        if len(x)==7:
            try:
                zeta=json.loads(x['content'])
                if type(zeta)=="dict":
                    z=list(zeta.keys())
                    return z
                
                else:
                    pass #print(type(zeta))   
            except:
                pass   
            
button_relay=Button(frame_relay,width=5, command=stamp_relay,text= "10002", font=("Arial",14,"normal"),foreground="blue")
button_relay.grid(column=1, row=0,pady=5)
button_relay=Button(frame_relay,width=8, command=stamp_relay_all,text= "3+10002", font=("Arial",14,"normal"),foreground="blue")
button_relay.grid(column=2, row=0)
frame_relay.grid(columnspan=3,rowspan=2,pady=5)

async def get_relays(client, authors,x):
    if x==int(1):
        f = Filter().authors(authors).kind(Kind(x)).limit(500)
    else:
        f = Filter().authors(authors).kind(Kind(x))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_relay(client, user,x):
    f = Filter().author(user)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def feed_note(authors,x):
            
    client = Client(None)
    if relay_note_list!=[]:
        for relay_x in relay_note_list:
           await client.add_relay(RelayUrl.parse(relay_x))
        for i,relay in enumerate(relay_note_list):    
            print(str(i) +" "+ str(relay)+"\n")     
        await client.connect()
        combined_results = await get_relays(client, authors,x)
        return combined_results

async def main(authors,x):
    # Init logger
    #init_logger(LogLevel.INFO)
    
    client = Client(None)
    
    # Add relays and connect
    if isinstance(authors, list):
        if x==10002:
            await client.add_relay(RelayUrl.parse("wss://purplepag.es/"))
            await client.add_relay(RelayUrl.parse("wss://indexer.coracle.social/"))
        else:
            await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
            await client.add_relay(RelayUrl.parse("wss://relay.noswhere.com/"))
            await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
            await client.add_relay(RelayUrl.parse("wss://relay.primal.net/"))
        await client.connect()
        combined_results = await get_relays(client, authors,x)
        
    else:
         await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
         await client.add_relay(RelayUrl.parse("wss://relay.noswhere.com/"))
         await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
         await client.add_relay(RelayUrl.parse("wss://relay.primal.net/"))
         await client.add_relay(RelayUrl.parse("wss://relay.mostr.pub/"))
         await client.connect()
         combined_results = await get_relay(client, authors,x)
    
    return combined_results  

frame3.grid(row=0,column=4,rowspan=2,columnspan=4)
photo_profile={}
Pubkey_Metadata={}
timeline_people=[]
db_list_note_follow=[]

def pubkey_timeline():
    for note in db_note_list:
        if note["pubkey"] not in timeline_people:
            timeline_people.append(note["pubkey"])

def list_pubkey_id():
    pubkey_timeline()
    if timeline_people !=[]:
        metadata_note=search_kind(user_convert(timeline_people),0)
        if metadata_note!=[]:
          try:  
            for single in metadata_note:
                if single not in db_list_note_follow:
                    db_list_note_follow.append(single)
         
                single_1=json.loads(single["content"])
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
             print(b,"\n","Pubkey ",single["pubkey"])  
            


def pubkey_id(test):
    note_pubkey=[]
    for note_x in db_note_list:
        if note_x["pubkey"] == test and note_x not in note_pubkey:
            note_pubkey.append(note_x)
    return len(note_pubkey),test

def relay_id(test):
    note_pubkey=[]
    select=None
    if test.startswith("wss://") and test.endswith("/"):
        select=test
    if test.startswith("wss://") and test.endswith("/")==False:
        select=test+str("/")
    s=0
    if select:
        for note_x in list(dict_pubkey_relay.keys()):
            if select in dict_pubkey_relay[note_x]:
                s=s+1
                note_pubkey.append(note_x)
        return s,note_pubkey  
    else:
       return None,None
     
dict_relay_number={}

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
        scrollregion=canvas.bbox("all")))
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    s=1 
    relay_list=[]    
    for key in list(dict_pubkey_relay.keys()):
        for relay_x in dict_pubkey_relay[key]:
           if str(relay_x).startswith("wss://"):
            if str(relay_x).endswith("/"):
              if relay_x not in relay_list:
                relay_list.append(relay_x)
            else:
              select=relay_x+"/"
              if select not in relay_list:
                relay_list.append(select)
    test1=relay_list
    
    ra=0
    sz=0
    labeL_button=Label(scrollable_frame,text="Number of Relays "+str(len(test1)))
    labeL_button.grid(row=0,column=1,padx=5,pady=5,columnspan=2)           
    while ra<len(test1):
               if str(test1[ra]).endswith("/"):
                lenght,note_p=relay_id(test1[ra])
                if lenght!=None:
                 if lenght>1:
                  dict_relay_number[test1[ra]]=lenght
                  sz=sz+1           
                 
                  button_grid1=Label(scrollable_frame,text=f"{test1[ra][6:]} note {lenght}",width=20,font=('Arial',12,'normal'))
                  button_grid1.grid(row=s,column=1,padx=2,pady=5,columnspan=1,rowspan=2)
                  button_grid2=Button(scrollable_frame,text=f"Note ", command= lambda val=note_p: show_lst_ntd(val),font=('Arial',12,'normal'))
                  button_grid2.grid(row=s,column=2,padx=2,pady=5) 
                root.update()  
              
                s=s+2
               ra=ra+1   
    labeL_button.config(text="Number of Relays "+str(len(test1))+"  "+"\n"+"Number of Relay more than one Note "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
     
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.02,rely=0.5,relwidth=0.26, relheight=0.35)      

    def Close_print():
       frame3.destroy()  
             
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

button_people_c=tk.Button(root,text="Relay & Notes",command=print_people, font=('Arial',12,'bold'))

label_image = Label(root,text="")

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
    button_photo_close.place(relx=0.45,rely=0.65)
    label_image.place(relx=0.4,rely=0.7)       

label_relay_w_r = Label(root,text="",font=("Arial",12,"normal"))

def show_lst_ntd(list_note_p):
 frame2=tk.Frame(root)  
 canvas_1 = tk.Canvas(frame2,width=800)
 scrollbar_1 = ttk.Scrollbar(frame2, orient=HORIZONTAL,command=canvas_1.xview)
 scrollable_frame_1 = tk.Frame(canvas_1,background="#E3E0DD")
 scrollbar_2 = ttk.Scrollbar(frame2, orient=VERTICAL,command=canvas_1.yview)
 label_relay_w_r.config(text="")
 scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all")))
 canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
 canvas_1.configure(xscrollcommand=scrollbar_1.set,yscrollcommand=scrollbar_2.set)
 if list_note_p!=[]:
  
  s=1
  s1=0
  for note in db_note_list:
    if note["pubkey"] in list_note_p:
         
      try:
       if note['pubkey'] in list(Pubkey_Metadata.keys()):
         
         context0="Nickname " +Pubkey_Metadata[note["pubkey"]]
       else: 
         context0="Author: "+note['pubkey']
      
       context1=note['content']+"\n"
       context2=" Minutes "+str(int(float(int(time.time())-note["created_at"])/(60)))+"\n"
       context3=str("")
       if note['tags']!=[]: 
        
        if tags_string(note,"r")!=[]:
            context2=context2+str("Numbers of relays "+str(len(tags_string(note,"r")))) +"\n"
            write_relays=relay_t(note)
            for relay in write_relays:
                if str(relay).startswith("wss://"):       
                    context2=context2+"W Relay: "+str(relay) +"\n"
            read_relays=relay_v(note)
            for relay_r in read_relays:
             if str(relay_r).startswith("wss://"):       
                context2=context2+"\n"+"R Relay: "+str(relay_r) +"\n"        
        
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
       
       label_relay_w_r.place(relx=0.7,rely=0.01,relheight=0.2,relwidth=0.3)

       def print_id(entry):
           
            if entry["kind"]==10002:
             c_relay=relay_t(entry)
             test_relay=str("")
             z=0
             for relay_x in c_relay:
                z=z+1
                if z<6:
                 test_relay=test_relay+  "W Relay: "+str(relay_x)+"\n"
                
                

             print("Relay for Write Outbox "+str(len(c_relay))+"\n")
             print(test_relay)
             label_relay_w_r.config(text="Relay for Write Outbox \n"+str(len(c_relay))+"\n"+test_relay)
             label_relay_w_r.place(relx=0.7,rely=0.01,relheight=0.2,relwidth=0.3)

       def print_var(entry):
            read_relay=relay_v(entry)
            test_relay = str("")
            s=0
            for relay_x in read_relay:
                s=s+1
                if s<6:
                 test_relay =test_relay+  "R Relay: "+str(relay_x)+"\n"
               
               
            print("Relay for Read (Inbox) \n"+ str(len(read_relay))+"\n")
            print(test_relay)
            label_relay_w_r.config(text="Relay for Read (Inbox) \n"+ str(len(read_relay))+"\n"+test_relay)
            label_relay_w_r.place(relx=0.7,rely=0.01,relheight=0.2,relwidth=0.3)

                                                                                                  
       button=Button(scrollable_frame_1,text=f"Relay to read", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Relay to write ", command=lambda val=note: print_id(val))
       button_grid2.grid(row=2,column=s1+1,padx=5,pady=5)    
       s=s+2  
       s1=s1+4

      except NostrSdkError as c:
           print(c, "maybe there is an Error") 

  scrollbar_1.pack(side="bottom", fill="x",padx=5)
  scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
  canvas_1.pack( fill="y", expand=True)
  if len(list_note_p)==1:
    frame2.place(relx=0.68,rely=0.2,relwidth=0.62,relheight=0.35)
  else:
    frame2.place(relx=0.39,rely=0.28,relwidth=0.55,relheight=0.35)

  def close_frame():
        frame2.destroy()    
        button_frame.place_forget()
        label_relay_w_r.place_forget()
    
  button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
  if len(list_note_p)==1:
    button_frame.place(relx=0.75,rely=0.6,relwidth=0.1)      
  else:
     button_frame.place(relx=0.7,rely=0.66,relwidth=0.1)      

Outboxes=[]
Outbox_list={}

def Fun_outbox(Number:int,my_relay:list):
   global Outboxes
   Outboxes=my_relay
   for keys in list(dict_pubkey_relay.keys()):
      Outbox_user=[]
      if len(dict_pubkey_relay[keys])>Number:
         for out_relay in Outboxes:
           if str(out_relay).endswith("/"):
            if (out_relay in dict_pubkey_relay[keys] or out_relay[:-1] in dict_pubkey_relay[keys]) and len(Outbox_user)<Number:
                    Outbox_user.append(out_relay)
            
            if str(out_relay) in dict_pubkey_relay[keys] and len(Outbox_user)<Number:
             Outbox_user.append(out_relay)


      if len(Outbox_user)<Number:
        for Relay_x in dict_pubkey_relay[keys]:
           if len(Outbox_user)<Number:
            Outbox_user.append(Relay_x)
            if Relay_x not in Outboxes:
              Outboxes.append(Relay_x)
      
      Outbox_list[keys]=Outbox_user    
   
         
   print("ok" ,len(Outboxes),"\n" ,Outboxes)

my_relay=[]

def relay_numbers_list():
    relay_ten_list=list(dict_relay_number.values())
    relay_ten_list.sort(reverse=True)
    relay_sort=[]
    for relay_in in relay_ten_list:
        for keys_one in list(dict_relay_number.keys()):
            if dict_relay_number[keys_one] == relay_in:
                if len(relay_sort)<10:
                        if keys_one not in relay_sort:
                            relay_sort.append(keys_one)
                else:
                   break            
    return relay_sort         

def outbox_model():
    my_relay1=relay_numbers_list()
    print(my_relay1)
    Fun_outbox(2,my_relay1)
    if my_relay1!=[]:
        button_people_b.grid(row=6,column=1,pady=5,padx=5) 
        button_people_c.grid(row=6,column=2,pady=5,padx=5) 

button_people_a=tk.Button(root,text="List of Relays",command=outbox_model, font=('Arial',12,'bold'))
button_people_a.grid(column=0,row=6,padx=5,pady=5)
list_pubkey_relay=[]
relay_note_list=[]

def Outbox_list_relays(): 
   
   if Outboxes!=[]:  
    
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=300)
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
    
    s=2 
    relay_list=[]
    for relay_x in Outboxes:
     if str(relay_x).startswith("wss://"):
        if str(relay_x).endswith("/"):
          if relay_x not in relay_list:
            relay_list.append(relay_x)
        else:
          select=relay_x+"/"
          if select not in relay_list:
            relay_list.append(select)

    def search_note():
       if relay_note_list!=[]:
        list_pubkey=list_pubkey_relay
        author_pubkey=user_convert(list_pubkey)
        list_str=asyncio.run(feed_note(authors=author_pubkey,x=1))
        if list_str!=[]: 
           note_upload=get_note(list_str)
           show_list_note(note_upload[0:100])
           
    test1=Outboxes
   
    def Add_relay(value):
      list_pubkey=[]
      new_pubkey=[]
      if str(value).startswith("wss://"):
       if str(value).endswith("/"):
         if value not in relay_note_list:
          relay_note_list.append(value)
       else:
            select=value+"/"
            if select not in relay_list:
                relay_note_list.append(select)
       for relay_y in relay_note_list:
          lenght,note_p=relay_id(relay_y)  
          if note_p!=None:
             for note_x in note_p:
                for note_y in db_note_list:
                 if note_x==note_y["pubkey"]:
                  if note_y["pubkey"] not in list_pubkey:
                   list_pubkey.append(note_y["pubkey"])
                   if note_y["pubkey"] not in list_pubkey_relay:
                    list_pubkey_relay.append(note_y["pubkey"])
                   if relay_y ==value:
                     new_pubkey.append(note_y["pubkey"])
       print(value, "\n", relay_note_list)            
       print("Number of Pubkey ",len(list_pubkey), " new pubkey ",len(new_pubkey) )
       if len(new_pubkey)>2:
              test_missing,test_relays=list_follow_missing(list_pubkey)
              print("- People ",len(test_missing),"\n")
              print("-Relays ",len(test_relays),"\n",test_relays)
              if len(test_relays)>0:
               relay_add=[]
               for relay_test in test_relays:
                    if str(relay_test).startswith("wss://"):
                        if str(relay_test).endswith("/"):
                            if relay_test not in Outboxes:
                                Outboxes.append(relay_test)
                                relay_add.append(relay_test)
                        else:
                                select_1=relay_test+"/"
                                if select_1 not in Outboxes:
                                    Outboxes.append(select_1)
                                    relay_add.append(select_1)
               if relay_add!=[]:                      
                print("New relay add ", len(relay_add))
               else:   
                print_people_from_relay(list_pubkey) 
                 
       else:
              pass                      
                       
    
    ra=0
    sz=0
    labeL_button=Label(scrollable_frame,text="Number of Relays "+str(len(test1)),width=40)
    labeL_button.grid(row=1,column=1,padx=5,pady=5,columnspan=2)           
    while ra<len(test1):
               if str(test1[ra]).endswith("/"): 
                lenght,note_p=relay_id(test1[ra])
                if lenght:
                 if lenght>int(2):
                  dict_relay_number[test1[ra]]=lenght
                  sz=sz+1           
                 
                  button_grid1=Label(scrollable_frame,text=f"{test1[ra][6:]} note {lenght}",width=20,font=('Arial',12,'normal'))
                  button_grid1.grid(row=s,column=1,padx=2,pady=5,columnspan=1,rowspan=2)
                  button_grid2=Button(scrollable_frame,text=f"Note ", command= lambda val=note_p: show_lst_ntd(val),font=('Arial',12,'normal'))
                  button_grid2.grid(row=s,column=2,padx=2,pady=5) 
                  button_grid3=Button(scrollable_frame,text=f"Add Relay ", command= lambda val=test1[ra]: Add_relay(val),font=('Arial',12,'normal'))
                  button_grid3.grid(row=s+1,column=2,padx=2,pady=5) 
                root.update()  
              
                s=s+3
            
               ra=ra+1   
    labeL_button.config(text="Number of Relays on lists "+str(len(test1))+"  "+"\n"+"Number of Relay more than two Note "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
     
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.02,rely=0.5,relwidth=0.3, relheight=0.35)      

    def Close_print():
       frame3.destroy()  
             
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)
    button_open_=tk.Button(scrollable_frame,text="Search Note",command=search_note, font=('Arial',12,'bold'))
    button_open_.grid(column=1,row=0)      
   
button_people_b=tk.Button(root,text="List of Outbox Relays",command=Outbox_list_relays, font=('Arial',12,'bold'))

def list_follow_missing(list_people):
    follow_list=people()
    if follow_list:
        missing_people=[]
        missing_relays=[]
        for people_x in follow_list:
            if people_x not in list_people:
                if people_x in list(Pubkey_Metadata.keys()):
                    missing_people.append(Pubkey_Metadata[people_x])
                else:
                    missing_people.append(people_x)
                if people_x in list(Outbox_list.keys()):
                    relay=Outbox_list[people_x]
                    print(relay)
                    for relax in relay:
                        if relax not in missing_relays:
                            missing_relays.append(relax)
                
        return missing_people,missing_relays    

def print_people_from_relay(list_fun:list): 
   if list_fun!=[]:  
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3,width=250)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    s=2     
    
    test1=list_fun
        
    ra=0
    sz=0
    labeL_button=Label(scrollable_frame,text="Number of pubkey "+str(len(test1))+"\n")
    labeL_button.grid(row=1,column=1,padx=5,pady=10,columnspan=2)           
    while ra<len(test1):
              
               lenght,note_p=pubkey_id(test1[ra])
               
               sz=sz+1           
               if test1[ra] in Pubkey_Metadata.keys():
                  button_grid1=Label(scrollable_frame,text=f"{Pubkey_Metadata[test1[ra]]} ",width=20,font=('Arial',12,'normal'))
               else:
                button_grid1=Label(scrollable_frame,text=f"{test1[ra][0:9]}",width=20,font=('Arial',12,'normal'))
               button_grid1.grid(row=s,column=1,padx=2,pady=5,columnspan=1,rowspan=2)
                
               button_grid2=Button(scrollable_frame,text=f"Note ", command= lambda val=[note_p]: show_lst_ntd(val),font=('Arial',12,'normal'))
               button_grid2.grid(row=s,column=2,padx=2,pady=5) 
                
               root.update()  
              
               s=s+2
           
               ra=ra+1   
    labeL_button.config(text="Number of pubkey "+str(len(test1))+"  "+"\n"+"Number of poster more than one note "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
     
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.4,rely=0.2,relwidth=0.26, relheight=0.35)      

    def Close_print():
       frame3.destroy()  
             
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

def show_list_note(list_outrelay:list):
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
  for note in list_outrelay:            
   var_id_3=StringVar()
   label_id_3 = Message(scrollable_frame_2,textvariable=var_id_3, relief=RAISED,width=270,font=("Arial",12,"normal"))
   label_id_3.grid(pady=1,padx=8,row=s,column=0, columnspan=3)
   if note['pubkey'] in list(Pubkey_Metadata.keys()):
         
         var_id_3.set("Nickname " +Pubkey_Metadata[note["pubkey"]])
   else: 
         var_id_3.set("Author: "+note['pubkey'])

   scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
   scroll_bar_mini.grid( sticky = NS,column=4,row=s+1)
   second_label_10 = tk.Text(scrollable_frame_2, padx=5, height=5, width=27, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
   context2=""   
   if tags_string(note,"t")!=[]:
        for note_tags in tags_string(note,"t"):
            context2=context2+str("#")+note_tags+" "
   if tags_string(note,"e")!=[]:
        context2=context2+str(tags_string(note,"e"))+ "\n"
                    
   second_label_10.insert(END,note["content"]+"\n"+str(context2))
   scroll_bar_mini.config( command = second_label_10.yview )
   second_label_10.grid(padx=10, column=0, columnspan=3, row=s+1)
   if tags_string(note,"imeta")!=[]:
    button=Button(scrollable_frame_2,text=f"Photo ", command=lambda val=note: print_var(val))
    button.grid(column=0,row=s+2,padx=5,pady=5)
   button_grid2=Button(scrollable_frame_2,text=f"Print Note ", command=lambda val=note: print(val))
   button_grid2.grid(row=s+2,column=1,padx=5,pady=5)     
   if tags_string(note,"e")!=[]:
    button_grid3=Button(scrollable_frame_2,text=f"Print reply ", command=lambda val=note: print_content(val))
    button_grid3.grid(row=s+2,column=2,padx=5,pady=5)     
   s=s+3 

  def print_var(entry):
       if tags_string(entry,"imeta")!=[]:
        balance,urL_list=balance_photo_print(entry)
        if urL_list:
         print_photo_url(url=urL_list[0])    

  def print_content(entry):
       print("Reply \n",tags_string(entry,"e"))                                          
                                          
  scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
  canvas_2.pack( fill="y", expand=True)
   
  def close_frame():
     button_frame.place_forget()
     frame3.destroy()    
    
  button_frame=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
  button_frame.place(relx=0.75,rely=0.04) 
  frame3.place(relx=0.66,rely=0.1,relheight=0.35,relwidth=0.33) 

def four_tags(x,obj):
   tags_list=[]
   
   if tags_string(x,obj)!=[]:
      for jtags in tags_str(x,obj):
        if len(jtags)>2:
          for xtags in jtags[2:]:
           if jtags not in tags_list:
             tags_list.append(jtags)
      return tags_list 

root.mainloop()