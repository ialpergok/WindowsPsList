class LIST_ENTRY32:
    def __init__(self,_flink,_blink):
        self.Flink=_flink
        self.Blink=_blink
    def get(self):
        return "Flink..:"+self.Flink+"         Blink..:"+self.Blink
    

