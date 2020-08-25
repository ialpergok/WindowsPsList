import struct
from src.list_entry import LIST_ENTRY32
class DBGKD_DEBUG_DATA_HEADER32:
    def __init__(self,_image):
        self.Mystruct="LLQLL"
        data= list(map(lambda d: hex(d), struct.unpack(self.Mystruct, _image)))
        self.Mylist=LIST_ENTRY32.LIST_ENTRY32(data[0],data[1])
        self.OwnerTag=data[3]
        self.Size=data[4]
    def get(self):
        return self.Mylist.get()+"\n"+"OwnerTag..:"+self.OwnerTag+"       Size..:"+self.Size+"\n"


