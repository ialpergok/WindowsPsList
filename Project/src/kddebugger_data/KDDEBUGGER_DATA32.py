import struct
from src.dbgkd_debug_data_header import DBGKD_DEBUG_DATA_HEADER32
class KDDEBUGGER_DATA32:
    def __init__(self,_image,_headerImage):
        self.Mystruct="QQQLLLLQQQQ"
        data=list(map(lambda d: hex(d), struct.unpack(self.Mystruct, _image)))
        self.header=DBGKD_DEBUG_DATA_HEADER32.DBGKD_DEBUG_DATA_HEADER32(_headerImage)
        self.KernelBase=data[0]
        self.BreakpointWithStatus=data[1]
        self.SavedContext=data[2]
        self.ThCallbackStack=data[3]
        self.NextCallback=data[4]
        self.FramePointer=data[5]
        self.PaeEnabled=data[6]
        self.KiCallUserMode=data[7]
        self.KeUserCallbackDispatcher=data[10]
        self.PsLoadedModuleList=data[8]
        self.PsActiveProcessHead=data[9]
    def get(self):
        return "\n...KDBG HEADER...\n\n"+self.header.get()+"\n\n"+"...KDBG DATA...\n"+"\n"+"KernelBase..:"+self.KernelBase+"\n"+"PsLoadedModuleList...:"+self.PsLoadedModuleList+"\n"+"PsActiveProcessHead..:"+self.PsActiveProcessHead