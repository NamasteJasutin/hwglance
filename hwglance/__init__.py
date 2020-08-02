print("""   Loading. Please wait. Just grabbing stuff here, hold on buddy!
###############################################################################
#######           HWGlance: Glance on your computer status              #######
#######          https://github.com/NamasteJasutin/HWGlance             #######
#######            Works on everything running >Python3.7               #######
###############################################################################
                   Getting your IP Address can take a while
                If you don't want this, run hwglance -s False
""")

import psutil, time, datetime, sys, socket, requests, platform, os
from decimal import Decimal

class HWmon:
    def __init__(self, refresh=0.5, doWave=True, changeColor=True, useServices=False):
        self.refresh = refresh
        self.doWave = doWave
        self.changeColor = changeColor
        self.useServices = useServices

        # Checks, see main below
        try:
            if type(float(self.refresh)) != type(float(1.1)):
                if self.refresh == "" or self.refresh == None:
                    self.refresh = 0.5 # Set default self.refresh
        except:
            self.refresh = 0.5 # Set default self.refresh

        try:
            if type(bool(self.doWave)) != type(bool(True)):
                if self.doWave == "" or self.doWave == None:
                    self.doWave = True # Set default value for doWave
        except:
            self.doWave = True # Set default value for doWave

        try:
            if type(bool(self.changeColor)) != type(bool(True)):
                if self.changeColor == "" or self.changeColor == None:
                    self.changeColor = True # Set default value for changeColor
        except:
            self.changeColor = True # Set default value for changeColor

        try:
            if type(bool(self.useServices)) != type(bool(True)):
                if self.useServices == "" or self.useServices == None:
                    self.useServices = False # Set default value for useServices
        except:
            self.useServices = False # Set default value for useServices

        # After checks
        self.ec = '╳'
        self.el = '╲'
        self.ef = '╱'
        self.go = True # Ready to go, IDK why I like to do this.
        self.main() # Go to main

    def cls(self): 
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    class pClr: # I guess this is where it all started... Not using FNT from WizPrint.. ;)
        wh = "\033[97m"
        P = '\033[95m'
        B = '\033[94m'
        G = '\033[92m'
        Y = '\033[93m'
        R = '\033[91m'
        E = '\033[0m'
        b = '\033[1m'
        u = '\033[4m'
        i = '\033[3m'
        BM = '\x1b[44m'


    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

    def progBar(self, input, length, *reverse):
        ftab = ''
        space = length - 5
        progress = self.translate(input, 0, 100, 0, int(space))
        inputlen = int(len(str(input)))
        if reverse:
            fill = '░' * int(progress)
            space = '▓' * (int(space) - int(progress))
        elif not reverse:
            fill = '▓' * int(progress)
            space = '░' * (int(space) - int(progress))
        if inputlen == 5:
            ftab = ''
        elif inputlen == 4:
            ftab = self.tab
        elif inputlen == 3:
            ftab = f"{self.tab} "
        msg = f"{fill}{space}{ftab}{input}%{self.tab}"
        return str(msg)
    
    def k2m(self, input):
        self.kb = int(input)
        self.kb2 = int(input)
        if len(str(self.kb)) > 11:
            mb = int(self.kb / 1000 / 1000)
            mb = str(mb)
            mb = f"{mb[:-3]}.{mb[-2:]}"
            st = 'GB'
        else:
            mb = int(self.kb / 1000 / 1000)
            mb = f"{mb}"
            st = "MB"
        return mb, st

    def getIP(self):
        if self.useServices == True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("1.1.1.1", 80))
                self.ipaddr = (s.getsockname()[0])
                s.close
            except:
                self.ipaddr = 'No network'
        else:
            self.ipaddr = 'Disabled.'
        return self.ipaddr

    def outerIP(self):
        if self.useServices == True:
            try:
                ip = requests.get('https://api.ipify.org?format=json').text
                self.ip = ip[7:-2]
            except:
                self.ip = 'No network'
        else:
            self.ip = 'Disabled.'
        return self.ip

    def c2g(self, input):
        kh = float(input)
        if len(str(kh)) > 4:
            self.gh = str(kh / 1000)
            self.gh = f"{self.gh[:4]} Ghz"
        else:
            self.gh = str(kh / 1000)
            self.gh = f"{self.gh} Mhz"
        return self.gh


    def getTemp(self):
        try:
            self.temps = psutil.sensors_temperatures()
            for mon in self.temps:
                return int(self.temps[mon][0][1])
        except:
            return int('0')

    def add0(self, data):
        data = str(data)
        if int(len(data)) < 2:
                self.output = f"0{data}"
        else:
            self.output = data
        return str(self.output)

    def osLen(self):
        self.ostype = platform.platform()
        self.oslen = int(len(self.ostype))
        maxlen = 47
        seperate = maxlen - self.oslen
        self.oT = round((seperate / 2) + 0.2)
        self.oF = round((seperate / 2) - 0.2)
        self.total = int(len(str(self.ostype))) + self.oT + self.oF
        if int(len(str(self.ostype))) > 47:
            self.ostype = f"{self.ostype[:46]}…"
        if int(len(str(self.total))) > 47:
            self.oF -= 1
            self.total = int(len(str(self.ostype))) + self.oT + self.oF
        self.oT = int(self.oT)
        self.oF = int(self.oF)
        return self.ostype, self.oT, self.oF, int(self.total)

    def averager(self, cputype, value):
        if cputype == 'u':
            calc = (value + self.cpu_user_prev) / 2
            self.cpu_user_av = calc
            self.cpu_user_prev = value
        elif cputype == 'i':
            calc = (value + self.cpu_idle_prev) / 2
            self.cpu_idle_av = calc
            self.cpu_idle_prev = value
        elif cputype == 's':
            calc = (value + self.cpu_system_prev) / 2
            self.cpu_system_av = calc
            self.cpu_system_prev = value
        # calc = value + cpuvar[1]
        # cpuvar[0] = calc
        # cpuvar[1] = value
        calc = Decimal(calc).quantize(Decimal('.1'))
        return calc

    def tWave(self):
        # sWave = f"{cWave[iWave::1]}{cWave[:iWave:1]}"
        self.sWave = ''.join(str(e) for e in self.cWave[self.iWave::1])
        self.sWave += ''.join(str(e) for e in self.cWave[:self.iWave:1])
        self.leWave = ''.join(str(e) for e in self.sWave)
        self.theWave = self.leWave * 7
        self.theWave = self.theWave[1::]
        if self.iWave == 5:
            self.iWave = 0
        else:
            if self.doWave == True:
                self.iWave += 1
        return str(self.theWave)
    
    def construct(self):
        self.ec = f"{self.pClr.wh}{self.ec}"
        self.el = f"{self.pClr.wh}{self.el}"
        self.ef = f"{self.pClr.wh}{self.ef}"
        self.go = True
        self.tab = '\t'
        self.nwl = '\n'
        self.bck = '\b'
        self.locIP = self.getIP()
        self.outIP = self.outerIP()
        self.color = time.localtime()[:-1]
        self.colors = [self.pClr.P, self.pClr.B, self.pClr.G, self.pClr.Y, self.pClr.R]
        self.ostype = platform.platform()
        self.oslen = self.osLen()
        self.cWave = ["⍨", "⁓", "~", "⁓", "⁓", "~"]
        self.iWave = 0
        self.cpu_user_av = float(0)
        self.cpu_system_av = float(0)
        self.cpu_idle_av = float(0)
        self.cpu_user_prev = float(0)
        self.cpu_system_prev = float(0)
        self.cpu_idle_prev = float(0)
        return
    
    def uptime2(self):  
        with open('/proc/uptime', 'r') as f:
            self.uptime_seconds = float(f.readline().split()[0])
            return self.uptime_seconds
    
    def main(self):
        self.construct() # Construct other parts of the script to work
        try:
            while self.go == True:
                starttime = time.time()
                self.mem = psutil.virtual_memory()
                self.cpuf = psutil.cpu_freq()
                self.cputp = psutil.cpu_times_percent()
                self.disk = psutil.disk_usage('/')
                if self.changeColor == True:
                    self.color = self.translate(int(str(time.localtime()[5])), 0, 60, 0, 4)
                else:
                    self.color = 1
                self.hour = self.add0(time.localtime()[3])
                self.mint = self.add0(time.localtime()[4])
                self.scnd = self.add0(time.localtime()[5])
                self.time = time.time()
                if len(str(self.time)) == 18:
                    self.spacetime = (" " * 3)
                elif len(str(self.time)) == 17:
                    self.spacetime = (" " * 4)
                elif len(str(self.time)) == 16:
                    self.spacetime = (" " * 5)
                # if int(len(self.scnd)) < 2:
                #     self.scnd = f"0{str(int(self.scnd))}"
                second = str(self.scnd)[-1:]
                color = int(self.color)
                rndClr = self.colors[color]
                if second == 1 or second == 3 or second == 5 or second == 7 or second == 9:
                    tS = ':'
                else:
                    tS = ' '
                if  int(len(self.k2m(self.mem[1])[0])) < 5:
                    mT = 2
                else:
                    mT = 1
                docls5 = 0
                if docls5 < 6 or str(self.scnd)[-2:] == 00:
                    self.cls()
                    docls5 += 1
                print(f"{self.ef}{self.ec*((6*8)-1)}{self.el}")
                print(f"{self.ec}{self.ef} {rndClr}       HWglance   -   Exit with CTRL+C     {self.pClr.E} {self.el}{self.ec}")
                if os.name:
                    print(f"{self.ec}{' ' * self.osLen()[1]}{self.pClr.b}{self.osLen()[0]}{self.pClr.E}{' ' * self.osLen()[2]}{self.ec}")
                print(f"{self.ec}{self.tab*6}{self.ec}")
                print(f"{self.ec} {self.pClr.R}Local time{self.tab}{self.hour}{tS}{self.mint}{tS}{self.scnd} ({self.time}){self.spacetime}{self.pClr.E}{self.ec}")
                print(f"{self.ec} {self.pClr.R}Date{self.tab*2}{time.localtime()[2]}-{time.localtime()[1]}-{time.localtime()[0]} Day {time.localtime()[6]}/7 {time.localtime()[7]}/365{self.tab}{self.pClr.E}{self.ec}")
                print(f"{self.ec}{self.tab*6}{self.ec}")
                if int(len(self.c2g(self.cpuf[0]))) < 8:
                    sT = 2
                else:
                    sT = 1
                print(f"{self.ec} {self.pClr.B}CPU{self.tab*2}Clock:{self.tab}{self.c2g(self.cpuf[0])}/{self.c2g(self.cpuf[2])}{self.pClr.E}{self.tab*sT}{self.ec}")
                print(f"{self.ec} {self.pClr.B}Usage{self.tab*2}User:{self.tab}{self.progBar(self.averager('u', self.cputp[0]), 20)}{self.pClr.E}{self.ec}{self.nwl}{self.ec}{self.pClr.B}{self.tab*2}System:{self.tab}{self.progBar(self.averager('s', self.cputp[2]), 20)}{self.pClr.E}{self.ec}{self.nwl}{self.ec}{self.pClr.B}{self.tab*2}Idle:{self.tab}{self.progBar(self.averager('i', self.cputp[3]), 20, True)}{self.pClr.E}{self.ec}")
                print(f"{self.ec}{self.tab*6}{self.ec}")
                print(f"{self.ec} {self.pClr.P}Memory{self.tab}Using:{self.tab}{self.k2m(self.mem[3])[0]}/{self.k2m(self.mem[0])[0]} {self.k2m(self.mem[0])[1]}{self.tab*2}{self.pClr.E}{self.ec}{self.nwl}{self.ec}{self.pClr.P}{self.tab*2}{self.progBar(self.mem[2], 28)}{self.pClr.E}{self.ec}")
                print(f"{self.ec}{self.tab*6}{self.ec}")
                if int(len(self.k2m(self.disk[1])[0])) < 7:
                    sT = 2
                else:
                    sT = 1
                if int(len(str(self.disk[3]))) < 4:
                    sT2 = 2
                else:
                    sT2 = 1
                print(f"{self.ec} {self.pClr.G}Storage{self.tab}Using:{self.tab}{self.k2m(self.disk[1])[0]}/{self.k2m(self.disk[0])[0]} {self.k2m(self.disk[0])[1]}{self.tab*sT}{self.pClr.E}{self.ec}{self.nwl}{self.ec}{self.pClr.G}{self.tab*2}{self.progBar(self.disk[3], 28)}{self.pClr.E}{self.ec}")
                print(f"{self.ec}{self.tab*6}{self.ec}")
                print(f"{self.ec} {self.pClr.Y}IP Addr{self.tab}Local:{self.tab}{self.locIP}{self.tab*2}{self.pClr.E}{self.ec}{self.nwl}{self.ec}{self.pClr.Y}{self.tab*2}Outer:{self.tab}{self.outIP}{self.tab*2}{self.pClr.E}{self.ec}")
                print(f"{self.ec}{self.tab*6}{self.ec}")
                if hasattr(psutil, "sensors_temperatures"):
                    print(f"{self.ec} {self.pClr.R}Temp{self.tab*2}CPU:{self.tab}{self.getTemp()}°C {self.tab*3}{self.pClr.E}{self.ec}")
                    print(f"{self.ec}{self.tab*6}{self.ec}")
                print(f"{self.ec}{self.el} {rndClr} {self.tWave()} {self.pClr.E} {self.ef}{self.ec}")
                #print(f"{self.ec*3}{self.tab*5}      {self.ec*3}")
                print(f"{self.el}{self.ec*((6*8)-1)}{self.ef}")
                endtime = time.time() 
                diftime = float(endtime - starttime) # Calculate difference between start and end
                refresh = float("{:.2f}".format(float(float(self.refresh) - float(diftime)))) # Calculate left over time to accurately refresh every 0.5 or chosen seconds
                if float(refresh) < 0:
                    refresh = 0
                # print(refresh)
                time.sleep(refresh)
                print("\033[H")
        except KeyboardInterrupt:
            self.go = False
            print("\a")
            sys.exit('Keyboard Interuption!')
        except Exception as e:
            self.go = False
            print("Other error occured:\n" + str(e))


if __name__ == "__main__":
    HWmon()