import json as js
with open(r"C:\Users\Ananya\Downloads\New document 1.json") as f:
    infor = js.load(f)
    print (infor)
print(infor.values())
