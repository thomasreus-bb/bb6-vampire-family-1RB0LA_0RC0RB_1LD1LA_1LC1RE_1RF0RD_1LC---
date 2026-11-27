import sys; sys.path.insert(0,'/tmp/an'); import learn, subprocess
def evrun(TM,q,tape,evs,mx=10**10):
    """run synth repeatedly until a left record in a state of evs"""
    r=subprocess.run(['/tmp/an/synthev',TM,q,'0',str(mx),evs],input=tape+'\n',capture_output=True,text=True).stdout.split()
    if r[0]=='HALT': return ('HALT',int(r[2]))
    if r[0]=='REC': return (r[1],int(r[2]),r[3])
    return (r[0],)
