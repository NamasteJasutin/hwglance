# Monitor computer status
import psutil, os, time, datetime, sys, socket, requests, platform


## CREATE OBJECT ##

class pClr:
    P = '\033[95m'
    B = '\033[94m'
    G = '\033[92m'
    Y = '\033[93m'
    R = '\033[91m'
    E = '\033[0m'
    b = '\033[1m'
    u = '\033[4m'

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def k2m(input):
    global kb2
    kb = int(input)
    kb2 = int(input)
    if len(str(kb)) > 11:
        mb = int(kb / 1000 / 1000)
        mb = str(mb)
        mb = f"{mb[:-3]}.{mb[-3:]}"
        st = 'GB'
    else:
        mb = int(kb / 1000 / 1000)
        mb = f"{mb}"
        st = "MB"
    return mb, st

def getIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ipaddr = (s.getsockname()[0])
        s.close
    except:
        ipaddr = 'No network'
    return ipaddr

def outerIP():
    try:
        ip = requests.get('https://api.ipify.org?format=json').text
        ip = ip[7:-2]
    except:
        ip = 'No network'
    return ip

def c2g(input):
    kh = float(input)
    if len(str(kh)) > 4:
        gh = str(kh / 1000)
        gh = f"{gh[:4]} Ghz"
    else:
        gh = str(kh / 1000)
        gh = f"{gh} Mhz"
    return gh

def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def getTemp():
    try:
        temps = psutil.sensors_temperatures()
        for mon in temps:
            return int(temps[mon][0][1])
    except:
        return int('0')

def add0(data):
    data = str(data)
    if int(len(data)) < 2:
            output = f"0{data}"
    else:
        output = data
    return str(output)

def osLen():
    ostype = platform.platform()
    oslen = int(len(ostype))
    maxlen = 47
    seperate = maxlen - oslen
    oT = round((seperate / 2) + 0.2)
    oF = round((seperate / 2) - 0.2)
    total = int(len(str(ostype))) + oT + oF
    if int(len(str(total))) > 47:
        oF -= 1
        total = int(len(str(ostype))) + oT + oF
    oT = int(oT)
    oF = int(oF)
    return ostype, oT, oF, int(total)

## END OF OBJECT ##

go = True
tab = '\t'
nwl = '\n'
bck = '\b'
locIP = getIP()
outIP = outerIP()
color = time.localtime()[:-1]
colors = [pClr.P, pClr.B, pClr.G, pClr.Y, pClr.R]
ostype = platform.platform()
oslen = osLen()
cWave = ["⁓", "~", "~", "-", "~", "-"]
iWave = 0

def tWave():
    global iWave, cWave, sWave, leWave
    # sWave = f"{cWave[iWave::1]}{cWave[:iWave:1]}"
    sWave = ''.join(str(e) for e in cWave[iWave::1])
    sWave += ''.join(str(e) for e in cWave[:iWave:1])
    leWave = ''.join(str(e) for e in sWave)
    theWave = leWave * 7
    theWave = theWave[1::]
    if iWave == 5:
        iWave = 0
    else:
        iWave += 1
    return str(theWave)


while go == True:
    try:
        mem = psutil.virtual_memory()
        cpuf = psutil.cpu_freq()
        cputp = psutil.cpu_times_percent()
        disk = psutil.disk_usage('/')
        color = translate(int(str(time.localtime()[5])), 0, 60, 0, 4)
        hour = add0(time.localtime()[3])
        mint = add0(time.localtime()[4])
        scnd = add0(time.localtime()[5])
        # if int(len(scnd)) < 2:
        #     scnd = f"0{str(int(scnd))}"
        second = str(scnd)[-1:]
        color = int(color)
        rndClr = colors[color]
        if second == 1 or second == 3 or second == 5 or second == 7 or second == 9:
            tS = ':'
        else:
            tS = ' '
        if  int(len(k2m(mem[1])[0])) < 5:
            mT = 2
        else:
            mT = 1
        
        cls()
        print(f"{'#'*(6*8)}#")
        print(f"### {rndClr}Pywaremon -xJustiinsane- Exit with CTRL+C {pClr.E}###")
        if os.name:
            print(f"#{' ' * osLen()[1]}{osLen()[0]}{' ' * osLen()[2]}#")
        print(f"#{tab*6}#")
        print(f"# {pClr.R}Local time{tab}{hour}{tS}{mint}{tS}{scnd}{tab*3}{pClr.E}#")
        print(f"# {pClr.R}Date{tab*2}{time.localtime()[2]}-{time.localtime()[1]}-{time.localtime()[0]} Day {time.localtime()[6]}/7 {time.localtime()[7]}/365{tab}{pClr.E}#")
        print(f"#{tab*6}#")
        if int(len(c2g(cpuf[0]))) < 8:
            sT = 2
        else:
            sT = 1
        print(f"# {pClr.B}CPU{tab*2}Clock:{tab}{c2g(cpuf[0])}/{c2g(cpuf[2])}{pClr.E}{tab*sT}#")
        print(f"# {pClr.B}Usage{tab*2}User:{tab}{cputp[0]}%{tab*3}{pClr.E}#{nwl}#{pClr.B}{tab*2}System:{tab}{cputp[1]}%{tab*3}{pClr.E}#{nwl}#{pClr.B}{tab*2}Idle:{tab}{cputp[2]}%{tab*3}{pClr.E}#")
        print(f"#{tab*6}#")
        print(f"# {pClr.P}Memory{tab}Using:{tab}{k2m(mem[3])[0]}/{k2m(mem[0])[0]} {k2m(mem[0])[1]}{tab*2}{pClr.E}#{nwl}#{pClr.P}{tab*2}Free:{tab}{k2m(mem[1])[0]} {k2m(mem[1])[1]} ({mem[2]}%){tab*mT}{pClr.E}#")
        print(f"#{tab*6}#")
        if int(len(k2m(disk[1])[0])) < 7:
            sT = 2
        else:
            sT = 1
        if int(len(str(disk[3]))) < 4:
            sT2 = 2
        else:
            sT2 = 1
        print(f"# {pClr.G}Storage{tab}Using:{tab}{k2m(disk[1])[0]}/{k2m(disk[0])[0]} {k2m(disk[0])[1]}{tab*sT}{pClr.E}#{nwl}#{pClr.G}{tab*2}Free:{tab}{k2m(disk[2])[0]} {k2m(disk[0])[1]} ({disk[3]}%){tab*sT2}{pClr.E}#")
        print(f"#{tab*6}#")
        print(f"# {pClr.Y}IP Addr{tab}Local:{tab}{locIP}{tab*2}{pClr.E}#{nwl}#{pClr.Y}{tab*2}Outer:{tab}{outIP}{tab*2}{pClr.E}#")
        print(f"#{tab*6}#")
        if hasattr(psutil, "sensors_temperatures"):
            print(f"# {pClr.R}Temp{tab*2}CPU:{tab}{getTemp()}°C {tab*3}{pClr.E}#")
            print(f"#{tab*6}#")
        print(f"### {rndClr}{tWave()}{pClr.E} ###")
        #print(f"###{tab*5}      ###")
        print(f"{'#'*(6*8)}#")
        time.sleep(1)
    except KeyboardInterrupt:
        go = False
        sys.exit('Keyboard Interuption!')
    except:
        go = False
        print("Other error occured")
