import struct
from src.list_entry import LIST_ENTRY32
class EPROCESS:
    def __init__(self,_image):
        self.__eproc_struct = "QQQQQQQQQQQQQQQQQQQQQQLLLLQQQQQQQQQQQQQQQQQQQQQLBBBBBBBBBBBBBBBB"
        eproc_data = list(map(lambda d: hex(d), struct.unpack(self.__eproc_struct, _image)))
        self.Mylist=LIST_ENTRY32.LIST_ENTRY32(eproc_data[24],eproc_data[25])
        self.ImageFileName1=chr(int(eproc_data[48], 16))
        self.ImageFileName2=chr(int(eproc_data[49], 16))
        self.ImageFileName3=chr(int(eproc_data[50], 16))
        self.ImageFileName4=chr(int(eproc_data[51], 16))
        self.ImageFileName5=chr(int(eproc_data[52], 16))
        self.ImageFileName6=chr(int(eproc_data[53], 16))
        self.ImageFileName7=chr(int(eproc_data[54], 16))
        self.ImageFileName8=chr(int(eproc_data[55], 16))
        self.ImageFileName9=chr(int(eproc_data[56], 16))
        self.ImageFileName10=chr(int(eproc_data[57], 16))
        self.ImageFileName11=chr(int(eproc_data[58], 16))
        self.ImageFileName12=chr(int(eproc_data[59], 16))
        self.ImageFileName13=chr(int(eproc_data[60], 16))
        self.ImageFileName14=chr(int(eproc_data[61], 16))
        self.ImageFileName15=chr(int(eproc_data[62], 16))
        self.ImageFileName16=chr(int(eproc_data[63], 16))
        self.Last=(int(eproc_data[63], 16))
        self.ProcName=self.ImageFileName1+self.ImageFileName2+self.ImageFileName3+self.ImageFileName4+self.ImageFileName5+self.ImageFileName6+self.ImageFileName7+self.ImageFileName8+self.ImageFileName9+self.ImageFileName10+self.ImageFileName11+self.ImageFileName12+self.ImageFileName13+self.ImageFileName14+self.ImageFileName15+self.ImageFileName16
    def get(self):
        return "\n...EPROCESS...\n"+"\nActivePRocessLinks.Flink..: "+self.Mylist.Flink+"        ActivePRocessLinks.Blink..: "+self.Mylist.Blink+"           Process Name..: "+self.ProcName+"\n"
    


