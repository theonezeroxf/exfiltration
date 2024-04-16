import os
import servicemanager
import shutil
import subprocess
import sys

import win32event
import win32service
import win32serviceutil
SRCDIR='D:\\cj\\work'
TGTDIR='C:\\Windows\TEMP'
class BHServiceSvc(win32serviceutil.ServiceFramework):
    _svc_name='BHServie'
    _svc_display_name_='BlackH Service'
    _svc_description_=("Executes VBScripts at regular intervals."+" What could possibly go wrong")
    def __init__(self,args):
        self.vbs=os.path.join(TGTDIR,'bhservice.vbs')
        self.timeout=1000*60

        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop=win32event.CreateEvent(None,0,0,None)
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENGING)
        win32event.setEvent(self.hWaitStop)
    def SvcDoRun(self):
        self.ReportServcieStatus(win32service.SERVICE_RUNNING)
        self.main()
    def main(self):
        while True:
            ret_code=win32event.WaitForSingleObject(self.hWaitStop,self.timeout)
            if ret_code==win32event.WAIT_OBJECT_O:
                servicemanager.LogInfoMsg("Service is stop")
                break
            src=os.path.join(SRCDIR,'bhservice_task.vbs')
            shutil.copy(src,self.vbs)
            subprocess.call("csript.exe %s"%self.vbs,shell=False)
            os.unlink(self.vbs)
    
if __name__=="__main__":
    if len(sys.argv)==1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(BHServiceSvc)
        servicemanager.StartServiceCtrlDispather()
    else:
        win32serviceutil.HandleCommandLine(BHServiceSvc)

