#   nostr_sdk 0.43 breakpoint


------

# Relay
## relay_url = RelayUrl.parse(jrelay)
##    await client.add_relay(relay_url)

Example

- relay_url_1 = RelayUrl.parse("wss://nostr.mom/")
- await client.add_relay(relay_url_1)
      
---
# Function


- def metadata_get():
- if Metadata_dict!={}: 
-            metadata = MetadataRecord(
-                name=Metadata_dict['name'],
-                display_name=Metadata_dict['display_name'],
-                about=Metadata_dict['about'],
-                picture=Metadata_dict['picture'],
-                lud16 =Metadata_dict['lud16'])
           
    # return metadata     

----

### metadata = metadata_get()
### if metadata!=:
## #     metadata_obj = Metadata.from_record(metadata)       