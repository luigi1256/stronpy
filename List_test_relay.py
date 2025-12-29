import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox 
from tkinter import font
root = tk.Tk()
root.geometry("1300x800")
import sqlite3
import uuid
import time
import json
from tkinter import messagebox 
defaultFont = font.nametofont("TkDefaultFont") 
defaultFont.configure(family="SF Pro", 
                                   size=12, 
                                   weight=font.NORMAL)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# create frames
frame1 = ttk.Frame(notebook, width=400, height=250)
frame3 = ttk.Frame(notebook, width=400, height=280)
frame4 = ttk.Frame(notebook, width=400, height=280)

frame4.pack()
container = ttk.Frame(frame1,width=380, height=180)
canvas = tk.Canvas(frame1,width=200, height=180)
scrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
scrollable_frame = ttk.Frame(frame1,width=340, height=160)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
canvas.configure(xscrollcommand=scrollbar.set)

#####################

####################

import asyncio
from nostr_sdk import *
from datetime import timedelta
Text_base = tk.Text(frame1, height=2, width=40,font=defaultFont)
Text_base.grid(row=0, column=0, columnspan=3, padx=5,pady=10)

def string_npub(string):
    if str(string).startswith("nprofile"):
        decode_nprofile = Nip19Profile.from_bech32(string)
        Npub=decode_nprofile.public_key()
        return Npub
   
def npub_class():
    try:
        if len(Text_base.get("1.0","end-1c"))==63:
            Npub=PublicKey.parse(Text_base.get("1.0","end-1c"))
            return Npub
        if len(Text_base.get("1.0","end-1c"))==64:
            Npub=PublicKey.parse(Text_base.get("1.0","end-1c"))
            return Npub
        if len(Text_base.get("1.0","end-1c"))>70:
            Npub=string_npub(Text_base.get("1.0","end-1c"))
            if Npub:
                return Npub
    except NostrSdkError as e:
        print(e)       
        Text_base.delete("1.0", "end") 

def search_three(notes,x):
    note=get_note(notes)
    Z=[]
    for r in note:
       if (r)['kind']==x:
          Z.append(r)
    return Z
def write_relay(x):
     i=0
     c=[]
     relays=tags_str(x,'r')
     j=len(relays)
     while i<j:
         if len(relays[i])>2:
             if relays[i][2]=="write":
              c.append(relays[i][1])
         i=i+1
         
     return c

async def get_relays(client, authors,kind):
    f = Filter().authors(authors).kind(Kind(kind))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_relay(client, user,kind):
    f = Filter().author(user).kind(Kind(kind))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def get_outbox(client, user,kind):
    f = Filter().author(user).kind(Kind(kind))
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec() if event.verify()]
    return z

async def main(authors,kind):
    # Init logger
    init_logger(LogLevel.INFO)
    client = Client(None)
    # Add relays and connect
    if combo_tag_list1.get() in list_relay:
        relay_list=list_relay[combo_tag_list1.get()]
        for relay_x in relay_list:
            await client.add_relay(RelayUrl.parse(relay_x))
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
    await client.connect()
    if isinstance(authors, list):
        combined_results = await get_relays(client, authors,kind)
    else:
        relay_add=get_note(await get_outbox(client,authors,10002))
        if relay_add !=None and relay_add!=[]:
            write_relay_list=write_relay(relay_add[0])
           
            if len(write_relay_list)>0:
                for xrelay in write_relay_list:
                    await client.add_relay(RelayUrl.parse(xrelay))
                await client.connect()
                combined_results = await get_relay(client, authors,kind)
            else:
                print(len(tags_string(relay_add[0],'r')))
                for yrelay in tags_string(relay_add[0],'r'):    #to do #while i=3
                    await client.add_relay(RelayUrl.parse(yrelay))  
                await client.connect()
                combined_results = await get_relay(client, authors,kind)  
        else: 
            print("simple")
            combined_results = await get_relay(client, authors,kind)
    
    return combined_results

async def get_Event(client, event_):
    f = Filter().ids(event_)
    events = await Client.fetch_events(client,f,timeout=timedelta(seconds=10))  
    z = [event.as_json() for event in events.to_vec()]
    return z

async def Get_id(event_):
    # Init logger
    init_logger(LogLevel.INFO)
    client = Client(None)
   
    # Add relays and connect
    await client.add_relay(RelayUrl.parse("wss://nostr.mom/"))
    await client.add_relay(RelayUrl.parse("wss://nos.lol/"))
    await client.add_relay(RelayUrl.parse("wss://relay.noswhere.com/"))
    await client.add_relay(RelayUrl.parse("wss://nostr.oxtr.dev/"))
    await client.add_relay(RelayUrl.parse("wss://relay.primal.net/"))
    await client.add_relay(RelayUrl.parse("wss://relay.mostr.pub/"))
    
    await client.connect()

    if isinstance(event_, list):
        test_kind = await get_Event(client, event_)
    else:
        print("errore")
    return test_kind

def search_kind_list(list_follow,x):
    note=note_list(list_follow,x)
    zeta=[]
    for r in note:
        if (r)['kind']==x:
          zeta.append(r)
    return zeta

def note_list(list_follow,kind):
    Let=[]
    if __name__ == "__main__":
     test_people = list_follow
     combined_results = asyncio.run(main(test_people,kind))
     Let=get_note(combined_results)
    return Let

def note_user(user):
    note=[]
    if __name__ == "__main__":
     single_author = user  
     Let = asyncio.run(main(single_author))
    note=get_note(Let)
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

def number_kind(tm):
    z=[]
    for v in tm:
        if (v)['kind'] in z:
              None  
        else:
              z.append((v)['kind'])
    return z

def event_number(tm):
    t=number_kind(tm)
    i=0
    number=[]
    while i<len(t):
        tip_i=[]
        for v in tm:
         if (v)['kind']==t[i]:
           tip_i.append(v)
        number.append(tip_i)
        i=i+1
    j=0
    while j<len(number):
        j=j+1
    return t, number

def Nostr_kind(t,number):
    f=input("choice a number:")
    x=json.loads(f)
    if x in t:
     i=0
     while i<len(t):
        if t[i]==x:
           z=number[i]
        i=i+1
     return z
    
def metadata_0(nota,y):
    test=json.loads(nota['content'])
    return test[y]  

def search_kind(user,x):
    zeta=[]
    if __name__ == "__main__":
     # Example usage with a single key
        single_author = user 
        single_results = asyncio.run(main(single_author,x))
        note=get_note(single_results)
        for r in note:
            if (r)['kind']==x:
                zeta.append(r)
    return zeta

def tags_string(x,obj):
    f=x['tags']
    z=[]
    for j in f:
      if j[0]==obj:
          z.append(j[1])
    return z

def evnt_id(id):
     test2=EventId.parse(id)
     return test2

def evnts_ids(list_id):
    Event=[]
    for j in list_id:
        Event.append(evnt_id(j))
    return Event

def note_list_d(list_id):
    let=[]
    if __name__ == "__main__":
     test_kinds = list_id  
     test_kind = asyncio.run(Get_id(test_kinds))
     let=get_note(test_kind)
    return let

#####################
db_list_note=[]

def obj_list():
    if npub_class(): 
        list_x=search_kind(npub_class(),30000)
        
        for note_x in list_x:
                db_list_note.append(note_x)
        title_list_option()      
        return list_x    
        
npub_list=[]

def print_base(jbase):
        context0=str("")
        context1=str("")
        if tags_string(jbase,"t")!=[]:
                context0=str("\n"+"pubkey: "+jbase['pubkey'][0:9]+"\n"+"id: "+jbase["id"][0:9]+"\n"+"Time: "+str(jbase["created_at"])+"\n")
                context1=str(jbase['content']+"\n")
        return context0,context1

def print_one_base(jbase):
    context0=str("")
    context1=str("")
    if jbase["pubkey"] not in block_npub:
        if str(jbase["pubkey"][0:9]) not in block_micro_npub:  
            context0=str("pubkey: "+jbase['pubkey'][0:9]+"\n"+"id: "+jbase["id"][0:9]+"\n"+"Time: "+str(jbase["created_at"])+"\n")
            context1=str(jbase['content']+"\n")  
    return context0,context1

block_micro_npub={}

def create_dropdown():
    list_list=obj_list()
    if list_list!=None:
        my_list_ = []
        for jlist in list_list:
            if tags_string(jlist,'title')!=[]  and tags_string(jlist,'title')[0] not in my_list_:
                my_list_.append(tags_string(jlist,'title')[0])
        combo_tag_list1['values']=my_list_            
        combo_tag_list1.set("Option List")    
        Text_relay.delete("1.0", "end")      

        def list_t(event):
            selected_it = combo_do_list.get()
            for xlist in list_list:
                if tags_string(xlist,'title')!=[]:
                    if tags_string(xlist,'title')[0]== selected_it:  
                        lab_list.config(text="number Lists: "+str(len(tags_string(xlist,'p'))))
        
        Frame_block=Frame(frame1)
        lab_list = tk.Label(Frame_block, text="List: ", background="grey")
        lab_list.grid(column=1, row=1,pady=5,padx=5, ipadx=2)
        combo_do_list = ttk.Combobox(Frame_block, values=my_list_,font=defaultFont )
        combo_do_list.grid(column=0, row=1,pady=5,padx=5, ipadx=2)
        combo_do_list.set("Option List")
        combo_do_list.bind("<<ComboboxSelected>>",list_t)
  
        def OpenFrame():
            frame_6=Frame(scrollable_frame)    
            frame_6.config(background="lightgrey")
            Checkbutton_8 = IntVar() 
            Button_8 = Checkbutton(frame_6, text = "🔒", variable = Checkbutton_8, 
                                onvalue = 1, offvalue = 0, width = 10)
            Button_8.grid(column=2, row=0)
            combo_do_list2 = ttk.Combobox(frame_6, values=my_list_, font=defaultFont)
            combo_do_list2.grid(column=0, row=0,pady=5,padx=5, ipadx=2)
            combo_do_list2.set("Lists")
            combo_do_list2.bind("<<ComboboxSelected>>",list_t)
         
            def return_j(j,s):  
                if Checkbutton_8.get() == 0:
                    if print_base(j):   
                        context0,context1=print_base(j)   
                        return context0,context1   
                else:
                    context0,context1=print_one_base(j)
                    return context0,context1   

            def Bookmark_b(Base):
                Text_t2.tag_configure('color',
                    foreground='#2271b3',
                    font=('Tempus Sans ITC', 13, 'bold'))
                Text_t2.tag_configure('color1',
                    foreground='#3d642d',
                    font=('Tempus Sans ITC', 12, 'bold')) 
                Text_t2.tag_configure('color2',
                    foreground='#512d64',
                    font=('Tempus Sans ITC', 12, 'bold')) 
                if Text_t2.get("1.0","end-1c")!="":
                    Text_t2.delete("1.0", "end")
                Text_t2.insert(END,str(len(Base))+"\n")
                s=1 
                for j in Base:
                    if return_j(j,s):
                        context0,context1=return_j(j,s)
                        if context0!="":
                            Text_t2.insert(END,str(s)+"\n",'color2')
                            Text_t2.insert(END,context0,'color1')
                            Text_t2.insert(END,context1,'color')
                            s+=1
                            if j['tags']!=[]:
                                context2="  [[ Tags]] "+"\n"
                                Text_t2.insert(END,context2,'color')
                                v=j['tags']
                                for tag in v:
                                    Text_t2.insert(END,str(tag)+"\n",'color2')
                                context4="\n" +"  ---------------------"+"\n"
                                Text_t2.insert(END,context4,'color')      
                            else:    
                                context4="\n" +"  ---------------------"+"\n"
                                Text_t2.insert(END,context4,'color')   
        
            def one_list():
                for xlist in list_list: 
                    list_=combo_do_list2.get()
                    if tags_string(xlist,'title')!=[]:
                        if tags_string(xlist,'title')[0]==list_:
                            tm=note_list(user_convert(tags_string(xlist,'p')),1)
                            Bookmark_b(tm)
                  
            input_list = Button(frame_6, text = "_show_", command =one_list, width = 10)
            input_list.grid(column=1, row=0,padx=5,pady=2)
            scroll_bar_mini = tk.Scrollbar(frame_6)        
            Text_t2=Text(frame_6, width=60,height=20,wrap="word",undo=True, yscrollcommand = scroll_bar_mini.set)
            scroll_bar_mini.config( command = Text_t2.yview )
            Text_t2.grid(column=0, row=2, columnspan=3)
            scroll_bar_mini.grid( sticky = NS,column=3,row=2,pady=5,padx=5)
            frame_6.pack(side="left",padx=2,pady=5)

            def delete_column_2(): 
                if Checkbutton_8.get() == 0:
                    frame_6.pack_forget()
                else:
                    messagebox.showerror("showerror", "Error")  
    
            button_delete_3=Button(frame_6,command=delete_column_2,text="❌")  
            button_delete_3.grid(column=4,row=0,pady=10)
    
    
        def update():
            frame1.after(1000, update)
        
        container.grid(pady=1, columnspan=8)
        canvas.grid(column=0, columnspan=7)
        scrollbar.grid(row=0,columnspan=7,ipadx=50)
        frame1.after(1000, update)
    
        def add_block_list():
            if len(stringa_block.get())==64:
                block_npub.append(stringa_block.get())
                stringa_bloc.set("")
                label_string_block.set(len(block_npub)+len(block_micro_npub))
            if len(stringa_block.get())==9:
                block_micro_npub[str(stringa_block.get())]="blocked"
                stringa_bloc.set("")
                label_string_block.set(len(block_npub)+len(block_micro_npub))
           
                
        stringa_bloc=StringVar()   
        stringa_block=Entry(Frame_block,textvariable=stringa_bloc,font=("Arial",10,"bold"),width=30)
        stringa_block.grid(column=0,row=0,padx=5,pady=5)
        random_block=Button(Frame_block, command=add_block_list, text= "block",background="darkgrey")
        random_block.grid(column=1,row=0,padx=5,pady=5)
        label_string_block=StringVar()
        label_block=Label(Frame_block, textvariable=label_string_block,background="darkgrey")
        label_block.grid(column=2,row=0,padx=5,pady=5)
        Frame_block.grid(row=0, column=4,pady=2)

        if npub_class():
            test_list=Button(Frame_block,command=OpenFrame,text="Open column list")
            test_list.grid(column=3, row=1,pady=5,padx=5, ipadx=2)   
        
        def delete_column_one(): 
            Frame_block.destroy()
        
        button_delete_o=Button(Frame_block,command=delete_column_one,text="❌")  
        button_delete_o.grid(column=4,row=0,pady=10)    
        
test_button=Button(frame1,command=create_dropdown,text="Access Key")
test_button.grid(column=3, row=0,pady=5,padx=5, ipadx=2)
block_npub=[]

# add frames to notebook
frame1.pack(pady=10)
notebook.add(frame1, text='Los Deck',padding=20)
Text_bar=Text(frame3, width=60,height=2,wrap="word",undo=True,foreground="grey",font=("sans-serif",12,"bold"))
Text_bar.pack(ipadx=2,ipady=2)

def close_profile():
    notebook.hide(frame1)

los_deck_info="""               Los Deck \n
    Deck has an entry widget where you can enter a key, such as hex |npub1|nprofile1
    Once you press the button, the lists will appear in the widget combobox. The default text is Option List.
    If you have lists in the selected relays, it will load the lists.
    You can see how many users are in the list or open Open Column List to read the notes.
    open 'Open Column List' to read the notes.
    There is another combobox with the lists. 
    If you have lists, select one and press the '_show_' button.
    If you press the padlock button, you cannot close the tab.
    The padlock button has two functions: it lets you read all the notes except for
    the entire *blocked users.
    If you press the '_show_' button without the lock, it only loads notes with t tags.
    "t" stands for hashtag.
    The version with the lock should have all the notes, barring errors.
    The notes are printed in a Text widget and there is no interaction.
    There is no graphics or rendering of photos or links.
"""
tab_relays="""          The Relays tab \n
    The relays tabs has a combobox with lists if you're logged in with your key.    
    If it's not empty,
    If the combobox is empty, you can't do anything.
    If the combobox has lists, you can select lists.
    Selecting a list loads the relays of the users in the list and shows you which ones are used.
    The used relays are added to a dictionary, {title: relay list}.
    These relays are used once you recall the notes in a list, when you press the '_show_' button in the 'deck Tab'.
    Also use default relays."""

django_tutorial_label = ttk.Label(text=str(los_deck_info)+"\n"+str(tab_relays))

notebook.add(frame4, text="Relays", padding=20)
notebook.add(django_tutorial_label, text="About", padding=20)

def delet_bar(): 
    if Text_bar.get(1.0, "end-1c")!="":
        Text_bar.delete("1.0","end")
    else:
        None

number_diplay=1 
notebook.pack(padx=10, pady=10, fill=tk.BOTH)
frame_relay=Frame(frame4,width=100, height=50)
label_relay=Label(frame_relay,text="Show Relays: ",font=("Arial",16,"normal"))
label_relay.grid(column=0,row=0)
scroll_bar_mini = tk.Scrollbar(frame_relay)
Text_relay = tk.Text(frame_relay, height=10, width=50, yscrollcommand = scroll_bar_mini.set)
scroll_bar_mini.config( command = Text_relay.yview )
Text_relay.grid(row=1, column=0,padx=30, columnspan=3,ipadx=10)
scroll_bar_mini.grid( sticky = NS,column=4,row=1,pady=5)

db_note_list=[]
dict_pubkey_relay={}
less_pubkey_relay={}

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

def to_follows(x,y):
    h=[]
   
    for j in x:
        if j in y:
            h.append(j)
    return h

def outrageous(people:list):
    i=0
    j=1
    Pu=[]
    test=[]
    Wu=list_battle(people)
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

def title_list_option():
    my_list=[]
    if db_list_note!=[]:
        for note_x in db_list_note:
           if tags_string(note_x,'title')!=[]:
                my_list.append(tags_string(note_x,'title')[0])
        combo_tag_list1["values"]=my_list 

list_relay={}           

def list_stamp_relay(event):
    select_item=combo_tag_list1.get()
    if select_item!="Option List":
        for note_x in db_list_note:
            if select_item in tags_string(note_x,"title"):
                people_list=tags_string(note_x,"p")
                relays=outrageous(people_list)
                list_relay[combo_tag_list1.get()]=relays
                print_relay_info(relays)
                break
      
combo_tag_list1 = ttk.Combobox(frame4, values=[],font=defaultFont )
combo_tag_list1.grid(column=0, row=1,pady=5,padx=5, ipadx=2)
combo_tag_list1.set("Option List")
combo_tag_list1.bind("<<ComboboxSelected>>",list_stamp_relay)
frame_relay.grid(columnspan=3,rowspan=2,pady=5)

def print_relay_info(list_rel):
    if list_rel!=[]:
        
        if Text_relay.get("1.0","end-1c")!="":
            Text_relay.delete("1.0","end")
            for relay in list_rel:
                Text_relay.insert(END," Relay: "+relay +"\n")
        else:
            for relay in list_rel:    
                Text_relay.insert(END," Relay: "+relay+"\n")  
    else:
        print("None Relays")     

root.mainloop()

def stamp_relay():
    if npub_class()!=None and db_list_note!=[]:
        
        list_people_=tags_string(db_list_note[1],"p")
        relays=outrageous(list_people_)
        if relays!=[]:
                
                if Text_relay.get("1.0","end-1c")!="":
                    Text_relay.delete("1.0","end")
                    for relay in relays:
                        Text_relay.insert(END," Relay: "+relay +"\n")
                else:
                    for relay in relays:    
                        Text_relay.insert(END," Relay: "+relay+"\n")  

        else:
            print("None Relays")     