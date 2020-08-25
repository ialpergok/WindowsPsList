#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
try:
    import os
    import struct
    import argparse
    import logging
    from src.eprocess import EPROCESS
    from src.dbgkd_debug_data_header import DBGKD_DEBUG_DATA_HEADER32
    from src.kddebugger_data import KDDEBUGGER_DATA32
    from src.list_entry import LIST_ENTRY32
except ImportError as e:
    print("Libraries can't loaded \n"+str(e))
    sys.exit(1)

class ProcessList:
    def __init__(self, _image):
        logging.basicConfig(level=logging.INFO)
        self.logger=logging.getLogger(__name__)
        self.image=_image
        self.kdbg_signature=b"\x00\x00\x00\x00\x00\x00\x00\x00KDBG"
        self.kdbgIndex=0
        self.PsActiveProcessHead=0
    def find_kdbg(self):
        self.kdbgIndex=self.image.find(self.kdbg_signature)
        if(self.kdbgIndex==-1):
            logger.info('Kernel Debugger Bulunamadı..!')
            sys.exit(1)
        logger.info('Kernel Debugger Bulundu..!')
        kdgb_header_length_constant = 16
        kdgb_data_length_constant = 88
        headerArray=self.image[self.kdbgIndex-8: self.kdbgIndex + kdgb_header_length_constant]
        DataArray=self.image[self.kdbgIndex+16: self.kdbgIndex + kdgb_data_length_constant]
        kdbg=KDDEBUGGER_DATA32.KDDEBUGGER_DATA32(DataArray,headerArray)
        self.PsActiveProcessHead=kdbg.PsActiveProcessHead
        print(kdbg.get())
        return self.PsActiveProcessHead
    def ListProcesses(self,Addr):
        TravelIndex=-1
        index=0
        FirstProc=0
        eproc_length_constant = 196
        ActiveProcessLinks=Addr
        EprocessData=self.image[ActiveProcessLinks-184: ActiveProcessLinks +eproc_length_constant]
        self.Flink=self.image[ActiveProcessLinks:ActiveProcessLinks +4]
        self.FirstFlink=self.image[ActiveProcessLinks:ActiveProcessLinks +4]
        self.FirstEproc_Blink=self.image[ActiveProcessLinks+4:ActiveProcessLinks+8]
        Eprocess=EPROCESS.EPROCESS(EprocessData)
        print(Eprocess.get())
        while(True):
            TravelIndex=self.image.find(self.Flink,TravelIndex+1)
            if(self.Flink==self.FirstEproc_Blink and index!=0):
                print("...Listeleme Sonlandı...")
                print("Proses Sayısı..:",index)
                break
            if(TravelIndex==-1):
                logger.info('Proses Bulunamadı..!')
                break
            if(TravelIndex==ActiveProcessLinks):
                continue
            DataIndex=TravelIndex-4
            EprocData=self.image[DataIndex-184:DataIndex+eproc_length_constant]
            Eproc=EPROCESS.EPROCESS(EprocData)
            if(Eproc.Last==2 or Eproc.Last==3):
                if(Eproc.ProcName.find(".")==-1):
                    if(Eproc.ProcName.find("System")!=-1):
                        index=index+1
                        if(index==1):
                            FirstProc=TravelIndex
                        print(index,".PROSES..:",end='')
                        print(Eproc.ProcName)
                        ##print("ARANAN FLİNK..:",self.Flink)
                        ##print("BULUNAN İNDEX..:",TravelIndex)
                        self.Flink=self.image[DataIndex:DataIndex+4]
                        ##print("YENİ FLİNK..:",self.Flink)
                        if(TravelIndex==ActiveProcessLinks and index!=0):
                            print("...Listeleme Sonlandı...")
                            print("Proses Sayısı..:",index)
                            break
                        TravelIndex=-1
                    continue
                index=index+1
                if(index==1):
                    FirstProc=TravelIndex
                print(index,".PROSES..:",end='')
                print(Eproc.ProcName)
                ##print("ARANAN FLİNK..:",self.Flink)
                ##print("BULUNAN İNDEX..:",TravelIndex)
                self.Flink=self.image[DataIndex:DataIndex+4]
                ##print("YENİ FLİNK..:",self.Flink)
                TravelIndex=-1
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    logging.basicConfig(level=logging.INFO)
    logger=logging.getLogger(__name__)
    parser.add_argument('-f','--file',type=str, action='store',help='Image path paramater')
    parser.add_argument('--version', action='version',version='%(prog)s 1.0')
    results = parser.parse_args()
    filename=results.file
    logger.info('Parametre atandı...')
    if(os.path.exists(filename) and os.path.isfile(filename)):
        logger.info('Dosya Bulundu...')
    else:
        logger.info('Geçerli bir imaj yolu giriniz..!')
        sys.exit(1)
    with open(filename,"rb") as f:
        image=f.read()
        logger.info('Dosya Okundu..!')
    f.close()
    logger.info('Dosya Kapandı..!')
    offSet=2147483648
    logger.info('Nesne Oluşturuldu..!')
    ps=ProcessList(image)
    PsActiveProcessHead=ps.find_kdbg()
    
    ActiveProcessLinks=(int(PsActiveProcessHead,16)-offSet)
    ps.ListProcesses(ActiveProcessLinks)
    logger.info('Prosesler Listelendi..!')