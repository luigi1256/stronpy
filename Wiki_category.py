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

#no canonical
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

def selected_id(value):
   list_value=[]
   for db_note in db_note_list:
    if tags_string(db_note,"c")!=[]:  
      if value in tags_string(db_note,"c"):
         if db_note not in list_value:
           list_value.append(db_note)
   return len(list_value),list_value

def category_list():
   for db_note in db_note_list:
    if tags_string(db_note,"c")!=[]:
     for cat_x in tags_string(db_note,"c"):
      if cat_x not in list_category:
        list_category.append(cat_x)
   return list_category   

def convert_user(x):
    other_user_pk = PublicKey.parse(x)
    return other_user_pk

def user_convert(x):
    l=[]
    for j in x:
        l.append(convert_user(j))
    return l

text_var_1=IntVar()
labeL_n=Label(root,textvariable=text_var_1,font=('Arial',12,'normal'))
scroll_bar_text = tk.Scrollbar(root, background="darkgrey")
entry_text=tk.Text(root, background="grey", yscrollcommand = scroll_bar_text.set, font=('Arial',14,'bold'))
scroll_bar_text.config( command = entry_text.yview )

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
    list_add_relay=["wss://nos.lol/","wss://nostr.mom/"]
    for x_relay in list_add_relay:
      if x_relay not in relay_list:
         relay_list.append(x_relay)
    await Search_status(client=Client(None),list_relay_connect=relay_list)     
    if relay_list!=[]:
       
       for relay_j in relay_list:
            await client.add_relay(RelayUrl.parse(relay_j))
    
    await client.connect()
    await asyncio.sleep(2.0)

    combined_results = await get_note_cluster(client, type_of_event)
    return combined_results

def pubkey_timeline():
   for note in db_note_list:
      if note["pubkey"] not in timeline_people:
         timeline_people.append(note["pubkey"])

def list_pubkey_id():
  pubkey_timeline()
  if timeline_people !=[]:
      
   metadata_note=search_kind(0)
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
         print(b)                   
          

number_category=[10,20,30,40]
value=int(10)

def on_server(event):
  global value
  value=int(combo_bo_r.get())
    
combo_bo_r = ttk.Combobox(root, font=('Arial',12,'normal'),values=number_category,width=10)
combo_bo_r.grid(column=3,row=5,pady=5,padx=2)
combo_label = ttk.Label(root, font=('Arial',12,'normal'),text="Category")
combo_label.grid(column=3, row=4,pady=5,padx=2)
combo_bo_r.set("Number")
combo_bo_r.bind("<<ComboboxSelected>>", on_server)

def show_noted():
  """Widget function \n
   Open feed Horizontal, 3 Row
   """
  frame2=tk.Frame(root)  
  if len(db_note_list)<=3:
     canvas_1 = tk.Canvas(frame2)
  else:   
    canvas_1 = tk.Canvas(frame2,width=620)
  scrollbar_1 = ttk.Scrollbar(frame2, orient=HORIZONTAL,command=canvas_1.xview)
  scrollable_frame_1 = tk.Frame(canvas_1,background="#E3E0DD")
  scrollbar_2 = ttk.Scrollbar(frame2, orient=VERTICAL,command=canvas_1.yview)
  scrollable_frame_1.bind(
         "<Configure>",
            lambda e: canvas_1.configure(
            scrollregion=canvas_1.bbox("all") ))

  canvas_1.create_window((0, 0), window=scrollable_frame_1, anchor="nw")
  canvas_1.configure(xscrollcommand=scrollbar_1.set,yscrollcommand=scrollbar_2.set)
  if db_note_list!=[]:
  
   frame_list=tk.Frame(scrollable_frame_1)
   button_1=Button(frame_list,text=f"Metadata Users", command=list_pubkey_id)
   button_1.grid(column=0,row=1,padx=5,pady=5)

   def print_people(): 
    if db_note_list!=[]:  
      
                                                
     s=4     
     if search_cat.get()!="Number":
      test1=list_category[0:value]
     else:
        test1=list_category 
     ra=0
     sz=0
     labeL_button=Label(frame_list,text="Category"+str(len(test1)))
     labeL_button.grid(row=3,column=0,padx=5,pady=5) 
     test1.sort()          
     while ra<len(test1):
                lenght,note_p=selected_id(test1[ra])
                
                sz=sz+1           
                button_grid1=Label(frame_list,text=f"{test1[ra][0:9]} note {lenght}",width=20)
                button_grid1.grid(row=s,column=0,padx=2,pady=5,)
                button_grid2=Button(frame_list,text=f"print", command= lambda val=note_p: show_ntd(val))
                button_grid2.grid(row=s,column=1,padx=2,pady=5) 
                s=s+1
                ra=ra+1   
     labeL_button.config(text="Number of Category "+str(len(test1))+"  ")
     root.update_idletasks()
     frame_list.grid(column=0,columnspan=2,row=2,rowspan=len(test1)+5)
   
   button_people_=tk.Button(scrollable_frame_1,text="List of Category",command=print_people, font=('Arial',12,'bold'))
   button_people_.grid(column=0,row=1,padx=5,pady=5,columnspan=2)
   string_search=ttk.Entry(scrollable_frame_1,justify='left', textvariable=search_cat)
   string_search.grid(column=0,row=0,padx=5,pady=5)
   button_s_c=tk.Button(scrollable_frame_1,text="Go",command=lambda: show_ntd(search_category_note()), font=('Arial',12,'bold'))
   button_s_c.grid(column=1,row=0,padx=5,pady=5)
   
   def show_ntd(db_note_max):
    i=0
    frame_center=tk.Frame(scrollable_frame_1)
    for note in db_note_max:   
    
      if db_note_max!=[]: 
       s=1
       title=tags_string(db_note_max[0],"c")[0]
       var_title=StringVar()
       label_title = Message(frame_center,textvariable=var_title, relief=RAISED,width=150,font=('Arial',14,'bold'))
       var_title.set(title) 
        
       label_title.grid(pady=2,padx=10, column=3, row=0)
       for note in db_note_max:
        var_id=StringVar()
        label_id = Message(frame_center,textvariable=var_id, relief=RAISED,width=150)
        var_id.set(str(tags_string(note,"d")[0])) 
        
        label_id.grid(pady=2,column=3,row=s+3)
        button_grid2=Button(frame_center,text=str(tags_string(note,"d")[0])+"- ", command=lambda val=note: print_id(val),widt=40)
        button_grid2.grid(row=s+3,column=4,padx=5,pady=5)
        if tags_string(note,"title")!=None and tags_string(note,"title")!=[]:
         label_text=Label(frame_center,text=str("\n Title \n"+str(tags_string(note,"title")[0])[0:60]+" " +"\n"+str(tags_string(note,"title")[0])[60:120]+ " "),font=('Arial',12,'normal'))
         label_text.grid(row=s+1,column=3,columnspan=2,rowspan=2)
        else: 
         label_text=Label(frame_center,text=str("\n No Title"+"\n"),font=('Arial',12,'normal'))
         label_text.grid(row=s+1,column=3,columnspan=2,rowspan=2)
        root.update()  
        s=s+4
        
        def print_id(test):
           try: 
            print("title ",tags_string(test,"title")[0])
            print("hashtag ",tags_string(test,"t"))
            print(str("https://")+str(tags_string(test,"d")[0]))
                                    
           except IndexError as e:
              print (e) 
                                              
                                                  
       
       def print_id(entry):
            if entry["tags"]!=[]:
              print(db_note_list.index(entry)+1)
              show_print_test_tag(entry)
       
    if len(db_note_max)>4:
        frame_center.grid(column=0,columnspan=2,row=0,rowspan=14)
                
    else:
         if len(db_note_max)>0:
          frame_center.grid(column=2,columnspan=2,row=0,rowspan=4)     
                  
    def close_center():
      button_grid_c.place_forget()
      frame_center.destroy()       
    
    if len(db_note_max)>0:
     button_grid_c=Button(root,text="Close ❌",font=("Arial",12,"normal"), command=close_center)
     button_grid_c.place(relx=0.42,rely=0.15)          
   scrollbar_1.pack(side="bottom", fill="x",padx=20)
   scrollbar_2.pack(side=LEFT, fill="y",pady=5,padx=2)
   canvas_1.pack( fill="both", expand=True)
   frame2.place(relx=0.01,rely=0.18,relwidth=0.85,relheight=0.65)

   def close_frame():
        frame2.destroy()    
        button_frame_1.place_forget()
        entry_text.place_forget()
        scroll_bar_text.place_forget()
        
   button_frame_1=Button(root,command=close_frame,text="Close ❌",font=("Arial",12,"normal"))
   button_frame_1.place(relx=0.5,rely=0.82,relwidth=0.1)      

   def show_print_test_tag(note):
    frame3=tk.Frame(frame2,height=150,width=160)  
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
    label_id_3 = Message(scrollable_frame_2,textvariable=var_id_3, relief=RAISED,width=320,font=("Arial",12,"normal"))
    label_id_3.grid(pady=1,padx=8,row=s,column=0, columnspan=3)
    if note['pubkey'] in list(Pubkey_Metadata.keys()):
         
         var_id_3.set("Nickname " +Pubkey_Metadata[note["pubkey"]])
    else: 
         var_id_3.set("Author: "+note['pubkey'])

    scroll_bar_mini = tk.Scrollbar(scrollable_frame_2)
    scroll_bar_mini.grid( sticky = NS,column=4,row=s+1)
    second_label_10 = tk.Text(scrollable_frame_2, height=8, width=30, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
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
    if tags_string(note,"alt")!=[]:
      for xnote in tags_string(note,"alt"):
         context2=context2+"\n"+"Alt "+str(xnote) +"\n"
    if tags_string(note,"title")!=[]:  
      for ynote in tags_string(note,"title"):
         context2=context2+"\n"+"Title "+str(ynote) +"\n" 
    if tags_string(note,"summary")!=[]:  
      for znote in tags_string(note,"summary"):
         context2=context2+"\n"+"Summary "+str(znote) +"\n"   
               
    second_label_10.insert(END,str(context2)+"\n"+note["content"])
    scroll_bar_mini.config( command = second_label_10.yview )
    second_label_10.grid(padx=2, column=0, columnspan=3, row=s+1) 

                                                                                  
    def print_content(entry):
       result=tags_string(entry,"e")
       if result!=[]: 
        z=5
        for jresult in result:
           for j_result in db_note_list:
            if jresult!=entry["id"] and j_result["id"]==jresult:  
             var_id_r=StringVar()
             label_id_r = Message(scrollable_frame_2,textvariable=var_id_r, relief=RAISED,width=320,font=("Arial",12,"normal"))
             label_id_r.grid(pady=1,row=z,column=0, columnspan=3)
             if j_result['pubkey'] in list(Pubkey_Metadata.keys()):
         
               var_id_r.set("Nickname " +Pubkey_Metadata[j_result["pubkey"]])
             else: 
               var_id_r.set("Author: "+j_result['pubkey'])
        
         
             scroll_bar_mini_r = tk.Scrollbar(scrollable_frame_2)
             scroll_bar_mini_r.grid( sticky = NS,column=4,row=z+1)
             second_label10_r = tk.Text(scrollable_frame_2, height=8, width=30, yscrollcommand = scroll_bar_mini_r.set, font=('Arial',14,'bold'),background="#D9D6D3")
             context22=""  
             if tags_string(j_result,"e")!=[]:
              if four_tags(j_result,"e"):
                for F_note in four_tags(note,"e"):
                     context22=context22+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              
             if tags_string(j_result,"alt")!=[]:
               for xnote in tags_string(j_result,"alt"):
                  context22=context22+"\n"+"Alt "+str(xnote) +"\n"
             if tags_string(j_result,"title")!=[]:  
               for ynote in tags_string(j_result,"title"):
                  context22=context22+"\n"+"Title "+str(ynote) +"\n" 
             if tags_string(j_result,"summary")!=[]:  
               for znote in tags_string(j_result,"summary"):
                  context22=context22+"\n"+"Summary "+str(znote) +"\n"   
             
             second_label10_r.insert(END,str(context22)+"\n"+j_result["content"])
             scroll_bar_mini_r.config( command = second_label10_r.yview )
             second_label10_r.grid(padx=1, column=0, columnspan=3, row=z+1) 
             button_grid3=Button(scrollable_frame_2,text=f"Read Content", command=lambda val= j_result["content"]: print(val))
             button_grid3.grid(row=z+2,column=0,padx=5,pady=5)                          
             button_grid4=Button(scrollable_frame_2,text=f"Read tags", command=lambda val= j_result["tags"]: print(val))
             button_grid4.grid(row=z+2,column=1,padx=5,pady=5)           
           z=z+3

    button_grid2=Button(scrollable_frame_2,text=f"Read Content", command=lambda val=note["content"]: print(val))
    button_grid2.grid(row=s+2,column=0,padx=5,pady=5)                          
    button_grid2=Button(scrollable_frame_2,text=f"Read tags", command=lambda val=note["tags"]: print(val))
    button_grid2.grid(row=s+2,column=1,padx=5,pady=5)           
    if tags_string(note,"e")!=[]:
     button_grid3=Button(scrollable_frame_2,text=f"Read reply", command=lambda val=note: print_content(val))
     button_grid3.grid(row=s+2,column=2,padx=5,pady=5)    

    scrollbar_2.pack(side="right", fill="y",padx=5,pady=10) 
    canvas_2.pack( fill="y", expand=True)
   
    def close_frame_2():
     button_frame.place_forget()
     frame3.destroy()    
    
    button_frame=Button(root,command=close_frame_2,text="Close ❌",font=("Arial",12,"normal"))
    button_frame.place(relx=0.6,rely=0.15) 
    frame3.place(relx=0.62,rely=0.15,relwidth=0.38)
            
#search
async def get_answers_Event(client, event_):
   
    f=Filter().kind(Kind(30818)).custom_tags(SingleLetterTag.lowercase(Alphabet.C),event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    #print(f.as_json(),len(z))
    return z

async def get_list_Event(client):
   
    f=Filter().kind(Kind(30818)).limit(200) #.since(timestamp=Timestamp.from_secs(since_day(int(360)))).until(timestamp=Timestamp.from_secs(since_day(int(200))))
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
    await client.add_relay(RelayUrl.parse("wss://relay.damus.io/"))
    await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
    await client.add_relay(RelayUrl.parse("wss://relay.nostr.band/"))
    await client.connect()

    await asyncio.sleep(2.0)
    if event_==[]:
      print("ok")
      resp_answer=await get_list_Event(client)
    else:
       print("2")
       resp_answer=await get_answers_Event(client, event_)
                                        
    return resp_answer

async def get_search_relay(client):
   f=Filter().kind(Kind(10102)).limit(10)
   events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
   z = [event.as_json() for event in events.to_vec() if event.verify()]
   return z

async def search_box_relay():
    init_logger(LogLevel.INFO)
    client = Client(None)
    list_add_relay=["wss://nos.lol/","wss://pyramid.fiatjaf.com/"]
    for x_relay in list_add_relay:
      if x_relay not in relay_list:
         relay_list.append(x_relay)
    await Search_status(client=Client(None),list_relay_connect=relay_list) 
    if relay_list!=[]:
       
       for jrelay in relay_list:
         await client.add_relay(RelayUrl.parse(jrelay))
             
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
           print(relay_search_list)      

def Search_Relay():
   if __name__ == "__main__":
    asyncio.run(search_box_relay())

button_close_search=tk.Button(root, text='Search Relay',font=('Arial',12,'bold'), command=Search_Relay)  
button_close_search.grid(column=1,row=4, padx=10,pady=5)

def search_note():
   event=[]
   if __name__ == "__main__":
    result=asyncio.run(Get_id(event))
    result_note=get_note(result)
    print(len(result_note))
    for result_x in result_note:
       if result_x not in db_note_list:
          db_note_list.append(result_x)
    test_list=category_list()
    print(len(test_list))      

button_close_search=tk.Button(root, text='Search Note',font=('Arial',12,'bold'), command=search_note)  
button_close_search.grid(column=1,row=5,pady=5,padx=10)
button_search=tk.Button(root, text='Show Note',font=('Arial',12,'bold'), command=show_noted)
button_search.grid(column=1,row=6,pady=5,padx=10)
search_cat=StringVar()

def search_category_note():
  if search_cat.get()!="":
   event=[]
   event.append(search_cat.get())
   if __name__ == "__main__":
    result=asyncio.run(Get_id(event))
    result_note=get_note(result)
    if (len(result_note))>0:
     for result_x in result_note:
       if result_x not in db_note_list:
          db_note_list.append(result_x)
    else:
       search_cat.set("")      
    return result_note
    
def since_day(number):
    import datetime
    import calendar
    date = datetime.date.today() - datetime.timedelta(days=number)
    t = datetime.datetime.combine(date, datetime.time(1, 2, 1))
    z=calendar.timegm(t.timetuple())
    return z

def print_list_tag(): 
   """Widget function \n
      List of hashtag
   """
   if db_note_list!=[]:  
    frame3=tk.Frame(root)
    canvas = tk.Canvas(frame3)
    scrollbar = ttk.Scrollbar(frame3, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
     
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)
    s=1     
    def remove_entry(entry):
       if list_category!=[]:
        if entry in list_category:
           list_category.remove(entry)
           print(len(list_category),entry)
           entry_tag.config(text=str(len(list_category)))


    if list_category==[]:
     category_list()
    test1=list_category
    test1.sort()
    if test1!=None and test1!=[]:
            ra=0
            se=1
            while ra<len(test1):
            
                button_grid1=Button(scrollable_frame,text=f"{test1[ra]} ", command=lambda val=test1[ra]: remove_entry(val))
                button_grid1.grid(row=0,column=s,padx=5,pady=2)
                
                if len(test1)>se:
                 button_grid2=Button(scrollable_frame,text=f"{test1[ra+1][0:10]}", command= lambda val=test1[ra+1]: remove_entry(val))
                 button_grid2.grid(row=1,column=s,padx=5,pady=2)
            
                root.update()  
                s=s+1
                se=se+2
                ra=ra+2   

    else:
         print("error") #It didn't find a channel

    if test1!=None and test1!=[]:
     scrollbar.pack(side="bottom", fill="x",padx=20)
     canvas.pack(side="left", fill="x", expand=True)
     frame3.place(relx=0.3,rely=0.01,relwidth=0.4,relheight=0.12)  

    def Close_print():
       frame3.destroy()  
       
    button_close_=tk.Button(scrollable_frame,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.grid(column=0,row=0,pady=5,padx=5)    
   else:
      print("error")
      
button_tag=tk.Button(root,text="Category",command=print_list_tag, font=('Arial',12,'bold'))
button_tag.grid(row=5,column=2,padx=10)

entry_tag=tk.Label(root,text="",font=('Arial',12,'bold'))
entry_tag.grid(row=4,column=2)
button_people_2=Button(root,text=f"Metadata User ", command=list_pubkey_id,font=('Arial',12,'bold'))

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
    canvas = tk.Canvas(frame3,width=270)
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
                  button_grid1=Label(scrollable_frame,text=f"{Pubkey_Metadata[test1[ra]][0:20]} note {lenght}",width=20)
                 else:
                  button_grid1=Label(scrollable_frame,text=f"{test1[ra][0:9]} note {lenght}",width=20)
                 button_grid1.grid(row=s,column=1,padx=2,pady=5,columnspan=1,rowspan=2)
                 button_grid2=Button(scrollable_frame,text=f"Wiki Note", command= lambda val=note_p: show_lst_ntd(val))
                 button_grid2.grid(row=s,column=2,padx=2,pady=5) 
                 if test1[ra] in list(photo_profile.keys()):
                   if str(photo_profile[test1[ra]])!=None: 
                     button_photo=Button(scrollable_frame, text="Photo ", command=lambda  val=str(photo_profile[test1[ra]]): print_photo_url(val),font=('Arial',12,'normal'))
                     button_photo.grid(row=s+1, column=2, padx=2, pady=5)
                 root.update()  
              
                s=s+2
            
                ra=ra+1   
    labeL_button.config(text="Number of pubkey "+str(len(test1))+"  "+"\n"+"Number of poster one note "+ str(sz))
    canvas.pack(side="left", fill="y", expand=True)
    button_people_2.place(relx=0.05,rely=0.6) 
    if len(test1)>5:
     scrollbar.pack(side="right", fill="y")  
    frame3.place(relx=0.01,rely=0.28,relwidth=0.26, relheight=0.3)      

    def Close_print():
       frame3.destroy()  
       button_people_2.place_forget()
       
    button_close_=tk.Button(frame3,text="🗙",command=Close_print, font=('Arial',12,'bold'),foreground="red")
    button_close_.pack(pady=5,padx=5)                 

button_people_=tk.Button(root,text="List of People",command=print_people, font=('Arial',12,'bold'))
button_people_.grid(row=6,column=2,pady=5,padx=2) 

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
       title=tags_string(note,"c")
       if title!=[]:
        context0= context0 +"\n"+"Category "+ str(title[0]) 
  
 
       context1=note['content']+"\n"
       context2=" "
       if note['tags']!=[]: 
        context2=""+"\n"   
        if tags_string(note,"e")!=[]:
              if four_tags(note,"e"):
                for F_note in four_tags(note,"e"):
                   if len(F_note)>3:  
                     context2=context2+str(" < "+ F_note[0]+" > ")+F_note[3]+ "\n"
              
       
        if tags_string(note,"alt")!=[]:
         for xnote in tags_string(note,"alt"):
          context2=context2+"\n"+"Alt "+str(xnote) +"\n"
        if tags_string(note,"title")!=[]:  
         for ynote in tags_string(note,"title"):
          context2=context2+"\n"+"Title "+str(ynote) +"\n" 
        if tags_string(note,"summary")!=[]:  
         for znote in tags_string(note,"summary"):
            context2=context2+"\n"+"Summary "+str(znote) +"\n"   
       
        if tags_string(note,"t")!=None and tags_string(note,"t")!=[] :
           s=0
           for xnote in tags_string(note,"t"):
            if s<5:
             context2=context2+"#"+str(xnote) +" "
            s=s+1
        
          
       var_id=StringVar()
       label_id = Message(scrollable_frame_1,textvariable=var_id, relief=RAISED,width=310,font=("Arial",12,"normal"))
       var_id.set(context0)
       label_id.grid(pady=1,padx=10,row=0,column=s1, columnspan=3)
       scroll_bar_mini = tk.Scrollbar(scrollable_frame_1)
       scroll_bar_mini.grid( sticky = NS,column=s1+3,row=1)
       second_label10 = tk.Text(scrollable_frame_1, padx=8, height=8, width=30, yscrollcommand = scroll_bar_mini.set, font=('Arial',14,'bold'),background="#D9D6D3")
       second_label10.insert(END,str(context2)+"\n"+context1)
       scroll_bar_mini.config( command = second_label10.yview )
       second_label10.grid(padx=10, column=s1, columnspan=3, row=1) 
      
       def print_id(entry):
            if entry["tags"]!=[]:
              print(db_note_list.index(entry)+1)
              print(entry["tags"])
              
       def print_var(entry):
                print(entry)

                                                                                                  
       button=Button(scrollable_frame_1,text=f"Print note", command=lambda val=note: print_var(val))
       button.grid(column=s1,row=2,padx=5,pady=5)
       button_grid2=Button(scrollable_frame_1,text=f"Click to read", command=lambda val=note: print_id(val))
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

label_image = Label(root,text="",)

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
                    
                    
                    if stats.bytes_received()>0:  #Auth ort other stuff
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

root.mainloop()