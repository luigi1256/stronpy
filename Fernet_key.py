from cryptography.fernet import Fernet
from nostr_sdk import Keys

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
def generate_new_key_store():
    key = Fernet.generate_key()
    #print(key)
    
    write_txt_note("fernet_key_test",key)                

def use_the_key(note:str):
    test_key= Open_txt_note("fernet_key_test")
    #print(test_key[1])
    fernet=Fernet(test_key[1:])
    encMessage = fernet.encrypt(note.encode())
    return encMessage

def save_content(message:str):
  try: 
   test_note=Open_txt_note("message_test")
   if test_note==None: 
    phrase=use_the_key(message)    
    write_txt_note("message_test",phrase)
  except TypeError as e:
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

def Generation_key():
    generate_new_key_store()
    save_content(Keys.secret_key(Keys.generate()).to_bech32())

Generation_key()

