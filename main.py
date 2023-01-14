import sys,os,time,re
import traceback
from time import perf_counter
from copy import copy
import SomeToolspbc.safely


debug = False

#IMPORT FILE PATH
IMPORT_PATH = [sys.path[0]+'\\',sys.path[0]+'\\lib\\']
#IMPORT FILE PATH END


#ERROR OBJ
ERROR_LIST = {'mean':'what is the * mean',
              'no_this':'no thing name *',
              'can_not':'can not * -- *',
              'no_file':'no file is *',
              'set':'set * must need *'}
def get_error(*er,etype='mean'):
    global ERROR_LIST,a,wrr,now,wr
    if etype in ERROR_LIST:
        aa = ERROR_LIST[etype]
        b = ''
        c = 0
        try:
            for i in range(len(aa)):
                if aa[i] != '*':
                    b += aa[i]
                else:
                    b += str(er[c])
                    c += 1
            print("ERROR:",b,'lines:',a,'(',wr[a],')',f'in:<{now}>')
        except Exception as r:
            print('SYSTEM_ERROR:raise error make error---error is "',r,'"')
        sys.exit(1)

#ERROR OB END



timeUp = False
if len(sys.argv) > 2:
    if sys.argv[2] == '-time':
        timeUp = True
    if sys.argv[2] == '-debug':
        debug = True
    
if len(sys.argv)<=1:
    print('ERROR:no file(-h to help)')
    #sys.exit()
    sys.argv=['f','hi.ccom']
if sys.argv[1]=='-h':
    print("""-h来帮你
-codeH教你一些关于comcat的代码
输入代码名以运行代码
-time查看运行时间
-h to help you
-codeH teaches you some code about comcat
Enter a code name to run the code
-time View the running time""")
    sys.exit()

elif sys.argv[1] == '-codeH':
    try:
        with open('./help.txt','r',encoding='utf-8') as file:
            print(file.read())
        file = None
    except Exception as r:
        print('ERROR:can not find the help file.')
    sys.exit(0)
else:
    try:
        with open(sys.argv[1],'r')as f:
            pass
        IMPORT_PATH.append('')
        PATH_SET = sys.argv[1]
        if '/' in PATH_SET:
            PATH_SET = PATH_SET.split('/')
        else:
            PATH_SET = PATH_SET.split('\\')
        for i in range(len(PATH_SET)):
            if i != len(PATH_SET)-1:
                IMPORT_PATH[2] += PATH_SET[i]+'/'
        #print(IMPORT_PATH)
    except Exception as r:
        print(f'ERROR:file {sys.argv[1]} can not open')
        sys.argv=['f','hi.txt']

def ifList(a):
    pass
def chvar(a,b,nows=''):
    global now,V
    try:
        if nows:
            if V[nows][a]:pass
            V[nows][a] = b
        else:
            if V[now][a]:pass
            V[now][a] = b
    except:
        try:
            if V['global'][a]:pass
            V['global'][a] = b
        except:
            #print(f'ERROR:no var name {a}')
            #sys.exit(0)
            get_error(a,etype='no_this')
def getvar(a):
    global now,V
    if a in V[now]:
        return V[now][a]
    elif a in V['global']:
        return V['global'][a]
    else:
        get_error(a)#raise error
def havar(a,b):
    global now,V
    try:
        if V[now][a]:pass
        V[now][a] = b
    except:
        try:
            if V['global'][a]:pass
            V['global'][a] = b
        except:return False
        else:
            return True
    return True

def typePlus(a):
    a = pluskoko(a)
    a = typeIf(a)
def andor(a):
    if a[1] == 'and':
        if a[0] and a[2]:
            return True
    if a[1] == 'or':
        if a[0] or a[2]:
            return True
    if a[1] == ':':
        if a[0]:
            return True
    return False
    
def ifif(dd):
    d = False
    try:
        if len(dd) == 3:
            a = dd[0]
            c = dd[1]
            b = dd[2]
            if c == '==' and a == b:
                d = True
            elif c == '>=' and a >= b:
                d = True
            elif c == '<=' and a <= b:
                d = True
            elif c == '<' and a < b:
                d = True
            elif c == '>' and a > b:
                d = True
            elif c == '!=' and a != b:
                d = True
        else:
            if dd[0]:
                d = True
        return d
    except:
        #print('ERROR:can not computer',dd)
        #sys.exit(1)
        get_error('compute',dd,etype='can_not')

def strdel(a,b=[]):
    c = ''
    for i in range(len(a)):
        if not i in b:
            c += a[i]
    return c
def typeIf(a):
    global V,importWord,spspot,now,inWord,mathWord,threeyuan
    if type(a) == str:
        try:
            if '.' in a:
                a = float(a)
            else:
                a = int(a)
        except Exception as r:
            if a in V[now]:
                a = V[now][a]
            elif a in V['global']:
                a = V['global'][a]
            elif a in importWord or a in inWord or a in spspot or \
                a in mathWord or a in threeyuan:
                pass
            elif a == 'True':
                a = True
            elif a == 'False':
                a = False
            elif a == 'Sans':
                a = None
            elif '"' in a:
                a = strdel(a,[0,len(a)-1])
            elif '.' in a:
                a = a.split('.',1)
                if a[1] in V[a[0]]:
                    a = V[a[0]][a[1]]
            else:
                #print(f'ERROR:what is the {a} mean?line:')
                #sys.exit(1)
                get_error(a,etype='mean')
    return a
def ints(a):
    return int(typeIf(a[1]))
def pluskoko(b):
    global a
    #print(a)
    c = []
    d = []
    for i in range(len(b)):
        if i%2 == 0:
            #print(typeIf(b[i]),b[i])
            c.append(typeIf(b[i]))
        else:
            d.append(typeIf(b[i]))
    #print(b)
    e = c[0]
    del c[0]
    for i in range(len(c)):
        if d[i] == '+':
            e += c[i]
        elif d[i] == '-':
            e -= c[i]
        elif d[i] == '*':
            e *= c[i]
        elif d[i] == '/':
            e /= c[i]
        elif d[i] == '%':
            e %= c[i]
        elif d[i] == '**':
            e = e**c[i]
        elif d[i] == '//':
            e = e//c[i]
        elif d[i] == '==':
            e = e == c[i]
        elif d[i] == '>':
            e = e > c[i]
        elif d[i] == '<':
            e = e < c[i]
        elif d[i] == '>=':
            e = e >= c[i]
        elif d[i] == '<=':
            e = e <= c[i]
        elif d[i] == '!=':
            e = e != c[i]
    return e

#COMCAT OBJECT
def listappend(who,a):#list ob
    global V,now
    if who in V[now]:
        V[now][who]['val']['list'].append(typeIf(a[1]))
    elif who in V['glb']:
        V['glb'][who]['val']['list'].append(typeIf(a[1]))
def listget(who,a):
    global V
    #print(getvar(who)['val']['list'])
    #print(typeIf(a[1]))
    return getvar(who)['val']['list'][typeIf(a[1])]
def listchange(who,a):
    global V,now
    a[1] = typeIf(a[1])
    if who in V[now]:
        V[now][who]['val']['list'][a[1]]=typeIf(a[2])
    elif who in V['glb']:
        V['glb'][who]['val']['list'][a[1]]=typeIf(a[2])
    #V[who]['val']['list'][a[1]] = typeIf(a[2])


def fileclose(who,a):#file ob
    global V,now
    if who in V[now]:
        V[now][who]['val']['file'].close()
        del V[now][who]
    elif who in V['glb']:
        V['glb'][who]['val']['file'].close()
        del V['glb'][who]
def filereadlines(who,a):
    return getvar(who)['val']['file'].readlines()
def fileread(who,a):
    return getvar(who)['val']['file'].read()
def filewrite(who,a):
    global V,now
    if who in V[now]:
        V[now][who]['val']['file'].write(typeIf(a[1]))
    elif who in V['glb']:
        V['glb'][who]['val']['file'].write(typeIf(a[1]))
#END

#import word
def opens(wrr):
    global classes
    a=None
    name = typeIf(wrr[1])
    if not os.path.exists(name):
        get_error(name,etype="no_this")
    a = open(name,typeIf(wrr[2]))
    b = copy(classes['file'])
    b['val']['file']=a
    a = None
    return b
def lists(wrr):
    global classes
    a = []
    for i in wrr[1:]:
        a.append(typeIf(i))
    b = copy(classes['list'])
    b['val']['list'] = copy(a)
    a = None
    return b
def new(wrr):
    #there is set a fun or class
    if wrr[1] == 'fun':
        del wrr[0]
        fun(wrr)
    elif wrr[1] == 'class':
        del wrr[0]
        pass###################class there
    else:
        get_error(wrr[1])
    
def elses(c):
    global V,ifs,spwait,a
    try:
        b = spwait['end'][len(spwait['end'])-1]
        if b[1]:
            spwait['end'][len(spwait['end'])-1][1]=False
            ifs += 1
        elif b[3]==0:
            ifs -= 1
            spwait['end'][len(spwait['end'])-1][1]=True
    except Exception as r:
        pass
def compute(a):
    global now
    b = a[1]
    del a[0]
    chvar(b,pluskoko(a))
    return None

def ifss(a):
    global threeyuan,threeword,ifs,manyIf
    del a[0]
    b = []
    c = []
    for i in a:
        if not i in threeyuan:
            b.append(i)
        else:
            c.append(pluskoko(b))
            if i != 'Then' and i != ':':
                c.append(i)
            b = []
    #print(c)
    if ifif(c):
        spwait['end'].append(['if',True,manyIf,0])
        return True
    else:
        spwait['end'].append(['if',False,manyIf,0])
        ifs += 1
        return False
def imports(c):
    global spwait,wr,a,now,IMPORT_PATH,V
    V[c[1]] = {}
    have_file = False
    for i in IMPORT_PATH:
        #print( os.path.isfile(i+c[1]+'.ccom'),i+c[1]+'.ccom')
        if os.path.isfile(i+c[1]+'.ccom'):
            with open(i+c[1]+'.ccom','r') as file:
                b = file.readlines()
                have_file = True
    if not have_file:
        #print(f"ERROR no model name '{c[1]}'")
        #sys.exit()
        get_error(c[1],etype='no_file')
    
    spwait['imports'].append([wr,a+1,now])#[code,line,now]
    now = c[1]
    wr = b
    a = -1
    deNoneThing()
    return None
def returns(aa):
    global V,now,a,spwait,wr##################
    del spwait['while'][len(spwait['end'])-1]
    pastFunName = now
    if now != 'main':
        a = spwait['fun'][len(spwait['fun'])-1][1]
        ret_name = spwait['fun'][len(spwait['fun'])-1][2]
        wr = spwait['fun'][len(spwait['fun'])-1][3]
        #print(ret_name)
        if ret_name:
            chvar(ret_name,typeIf(aa[1]),spwait['fun'][len(spwait['fun'])-1][0])
        now = spwait['fun'][len(spwait['fun'])-1][0]
        del spwait['fun'][len(spwait['fun'])-1]
        del spwait['end'][len(spwait['end'])-1]
    else:
        ending(aa)
    del V[pastFunName]
def globalss(a):
    global V
    if a[2] != '=':
        #sys.exit()
        #print('set must need '='',a[1])
        get_error('var','"="',etype='set')
    b = []
    for i in a:
        b.append(i)
    del b[0]
    del b[0]
    del b[0]

    vel = []
    val = False
    vall = b
    b = None
    b = []
    
    for i in range(len(vall)):
        if vall[i] in inWord:
            val = True
            vel.append(vall[i])
        elif val:
            if vall[i] == '}':
                val = False
                inWord[vel[0]](vel)
                vel = None
                vel = []
            else:vel.append(vall[i])
        else:
            if vall[i] == '}':
                print("Syntax Error:string in numbers.line:",*a)
                sys.exit(2)
            b.append(vall[i])
    
    e = pluskoko(b)
    V['global'][a[1]] = e
    return None

def elifs(c):
    global V,ifs,spwait,a
    try:
        del c[0]
        c[0],c[2]=typeIf(c[0]),typeIf(c[2])
        b = spwait['end'][len(spwait['end'])-1]
        if b[1]:
            spwait['end'][len(spwait['end'])-1][1]=False
            spwait['end'][len(spwait['end'])-1][3]=1
            ifs += 1
        elif ifif(c):
            ifs -= 1
            spwait['end'][len(spwait['end'])-1][1]=True
    except Exception as r:
        print(r)
        pass
def whiles(b):
    global spwait,a
    if ifss(b):
        #print(b,'s')
        c = 'go'# go is True
        del spwait['end'][len(spwait['end'])-1]
    else:
        del spwait['end'][len(spwait['end'])-1]
        c = 'break'# break is False
    spwait['end'].append(['while','while'])
    spwait['while'].append([c,a-1])
    

def end(c):
    global spwait,ifs,a,now,wr,manyIf,V
    
    try:
        b = spwait['end'][len(spwait['end'])-1]
        if b[0]=='fun':
            del spwait['while'][len(spwait['end'])-1]
            pastFunName = now
            now = spwait['fun'][len(spwait['fun'])-1][0]
            wr = spwait['fun'][len(spwait['fun'])-1][3]
            a = spwait['fun'][len(spwait['fun'])-1][1]
            ret_name = spwait['fun'][len(spwait['fun'])-1][2]
            if ret_name:
                chvar(ret_name,None)
            del spwait['fun'][len(spwait['fun'])-1]
            del V[pastFunName]
        elif b[0]=='if':
            ifs -= 1
            manyIf -= 1
        elif b[0]=='while':
            #print(spwait['while'],spwait['end'],sep='\n')
            #print('hello')
            #print(spwait['while'][len(spwait['while'])-1][0])
            if spwait['while'][len(spwait['while'])-1][0] == 'break':
                ifs -= 1
            elif spwait['while'][len(spwait['while'])-1][0] == 'go':
                a = spwait['while'][len(spwait['while'])-1][1]
            del spwait['while'][len(spwait['end'])-1]#可要可不要，用处是减少占用内存。
            #print(spwait['while'])
        del spwait['end'][len(spwait['end'])-1]#必要
        
        #print(spwait)
    except Exception as r:
        print(r)
        print(traceback.print_exc())
def var(a):
    global V,now,inWord
    if a[2] != '=':
        #print(f"ERROR:set var must need '=' at",*a)
        #sys.exit()
        get_error('var','"="',etype='set')
    b = []
    for i in a:
        b.append(i)
    del b[0]
    del b[0]
    del b[0]

    vel = []
    val = False
    vall = b
    b = None
    b = []
    
    for i in range(len(vall)):
        if vall[i] in inWord:
            val = True
            vel.append(vall[i])
        elif val:
            if vall[i] == '}':
                val = False
                b.append(inWord[vel[0]](vel))
                vel = None
                vel = []
            else:vel.append(vall[i])
        else:
            if vall[i] == '}':
                print("Syntax Error:string in numbers.line:",*a)
                sys.exit(2)
            b.append(vall[i])
    #print(b)
    e = pluskoko(b)
    if not now in V:
        V[now] = {}
    V[now][a[1]] = e
    return None
def getTime(a):
    global V,now
    #chvar(a[1],time.perf_counter())
    return time.perf_counter()
def ending(a):
    global runing,ret,start,timeUp
    ret = 0
    if timeUp:
        print(perf_counter()-start)#######################
    if len(a)>=2:
        print(a[1])
        ret = typeIf(a[1])
    runing = False

def fun(aa):#create a fun to use
    global wr,a
    del aa[0]
    name = aa[0]
    funs[aa[0]]={'var':None,'code':a,'codes':[]}
    #print(aa)
    if len(aa) >= 2:
        #print(vaa)
        #funs[aa[0]]['var']=aa[1].split(',')
        vaa = aa[1:]
        aa = 0
        aa = [name]
        for i in range(len(vaa)):
            if vaa[i]!=',':
                #print(vaa[i])
                aa.append(vaa[i])
        vaa = None
    whileIf = []
    velWhileIf = []
    funs[aa[0]]['var']=aa[1:]
    #print(aa)
    while True:
        a += 1
        try:
            #print(wr[aa])
            funs[aa[0]]['codes'].append(wr[a])
            velWhileIf = wr[a].split(' ')
            if velWhileIf[0] == 'while' or velWhileIf[0] == 'if':
                whileIf.append('ff')
            if wr[a]=='end':
                if len(whileIf) > 0:
                    del whileIf[0]
                else:
                    break
        except Exception as e:
            #print(f'ERROR:the fun {aa[0]} is no end')
            #sys.exit(1)
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            get_error(aa[0],etype='no_this')
def run_fun(aa):
    global a,wr,now,V,spwait
    spwait['while'].append('fun')
    #print(aa)
    name = aa[0]
    varName = ''
    if '>>>' in aa:
        for i in range(len(aa)):
            if aa[i] == '>>>':
                del aa[i]
                try:
                    varName = aa[i]
                    del aa[i]
                except:print(\
f'-----warning-----(at {a} run fun you input\
>>> but you do not input a thing behind it)')#####################
                break
                
    del aa[0]
    #print(aa,funs[name]['var'])
    for i in range(len(aa)):
        if not name in V:
            V[name] = {}
        V[name][funs[name]['var'][i]] = typeIf(aa[i])
        #print(V[name])
    spwait['fun'].append([now,a,varName,wr])#now,line,ret var,past
    now = name
    #a = funs[name]['code']
    a = -1
    wr = funs[name]['codes']
    spwait['end'].append(['fun'])
def prints(a):#print
    for i in range(len(a)):
        if i != 0:
            a[i] = typeIf(a[i])
            if a[i] == None:
                a[i] = 'Sans'
            print(a[i],end='')
def strs(a):
    return str(typeIf(a[1]))
def number(a):
    return eval(typeIf(a[1]))
def floats(a):
    return float(typeIf(a[1]))

def iss(a):
    if typeIf(a[1]) is typeIf(a[2]):
        return True
    return False
def ids(a):
    a = a[1]
    a = typeIf(a)
    return id(a)
def inputs(a):
    return input(typeIf(a[1]))
def gc(a):
    global V,now
    if len(a) < 2:
        V = None
        V = {'main':{},'global':{}}
    else:
        if a[1] in V[now]:
            del V[now][a[1]]
        elif a[1] in V['global']:
            del V['global'][a[1]]
        elif '.' in a[1]:
            b = a[1].split('.')
            #c = b[len(b)-1]
            #del b[len(b)-1]
            d = V
            for i in range(len(b)):
                if i != len(b)-1:
                    d = d[b[i]]
                else:
                    if b[i] in d:
                        del d[b[i]]
                    else:
                        get_error(a[1])
        else:
            get_error(a[1])
            
                
                
#end
def isObFun(a):
    global classes,V,now
    b = copy(a)
    b = b.split('.')
    for i in classes:
        try:
            if b[0] in V[now]:
                if V[now][b[0]]['id'] == classes[i]['id']:
                    return True
            elif b[0] in V['glb']:
                if V['glb'][b[0]]['id'] == classes[i]['id']:
                    return True
        except:pass
    return False

def decodes(a):
    global spword,now
    a = a.rstrip()
    if not now in V:
        V[now] = {}
    b = []
    c = ''
    d = False#"
    e = False#\\
    dec = False#[
    for x in range(len(a)):
        i = a[x]
        if not e and i == '"':
            if d:
                d = False
                c += '"'
                if x == len(a)-1:
                    #c = strdel(c,[0,len(c)-1])
                    b.append(c)
                    c = ''
            else:
                d = True
                c += '"'
        elif not d and not e:
            if i == ' ':
                b.append(c)
                c = ''
            else:
                c += i
                if x == len(a)-1:
                    b.append(c)
                    c = ''
        elif d:
            if i == '\\' and not e:
                e = True
            elif e:
                try:
                    c += spword[i]
                except:
                    #print(f'ERROR:what is the \\{i} mean?')
                    #sys.exit()
                    #get_error(f'\\{i}',etype='mean')
                    pass
                e = False
            else:
                c += i
    return b

def decode2(a,line):
    global spword,now,impspw
    nows = 0#0:None 1:num 2:float 3:string 4:other 5:spw
    nums = '0123456789'
    vel = ''
    val = []
    spw = False
    for i in range(len(a)):
        #print(a[i])
        if not nows:
            if a[i] == ' ':
                nows = 0
            elif a[i] in nums:
                vel += a[i]
                nows = 1
            elif a[i] in '"':
                vel += a[i]
                nows = 3
            elif a[i] in impspw:
                vel += a[i]
                nows = 5
            else:
                vel += a[i]
                nows = 4
            if i == len(a)-1:
                val.append(vel)
                break
        else:
            #print(nows,a[i])
            if nows == 1:
                if a[i] in nums:
                    vel += a[i]
                elif a[i] == '.':
                    nows = 2
                    vel += '.'
                elif a[i]==' ':
                    val.append(vel)
                    vel = ''
                    nows = 0
                elif a[i] in impspw:
                    val.append(vel)
                    vel = ''
                    vel += a[i]
                    nows = 5
                else:
                    print("Syntax Error:string in numbers.line:",line)
                    sys.exit(2)
                if i == len(a)-1:
                    val.append(vel)
            elif nows == 2:
                #print('f')
                if a[i] in nums:
                    vel += a[i]
                elif a[i]==' ':
                    val.append(vel)
                    vel = ''
                    nows = 0
                elif a[i] in impspw:
                    val.append(vel)
                    vel = ''
                    vel += a[i]
                    nows = 5
                else:
                    print("Syntax Error:string in float.line:",line)
                    sys.exit(2)
                if i == len(a)-1:
                    val.append(vel)
            elif nows == 3:
                if a[i] == '\\':
                    spw = True
                elif spw:
                    if a[i] in spword:
                        vel += spword[a[i]]
                    spw = False
                elif a[i] == '"':
                    vel += '"'
                    nows = 0
                    val.append(vel)
                    vel = ''
                else:
                    vel += a[i]
            elif nows == 4:
                if a[i] == ' ':
                    nows = 0
                    val.append(vel)
                    vel = ''
                elif i == len(a)-1:
                    vel += a[i]
                    val.append(vel)
                elif a[i] in impspw:
                    val.append(vel)
                    vel = ''
                    vel += a[i]
                    nows = 5
                else:
                    vel += a[i]
            elif nows == 5:
                if not a[i] in impspw:
                    val.append(vel)
                    vel = ''
                    if a[i] == ' ':
                        nows = 0
                    elif a[i] in nums:
                        vel += a[i]
                        nows = 1
                    elif a[i] in '"':
                        vel += a[i]
                        nows = 3
                    else:
                        vel += a[i]
                        nows = 4
                    if i == len(a)-1:
                        val.append(vel)
                        break
                elif i == len(a)-1:
                    vel += a[i]
                    val.append(vel)
                else:
                    vel += a[i]
            else:
                print(a[i],nows,line)
                print('system error in decode2')
                sys.exit(3)
    return val
                    
                    
                    
        

if timeUp:
    start = perf_counter()#########################

wr = []# no decode(all code)
now = 'global'
wrr = []#decode wr(line code)
try:
    with open(sys.argv[1],'r') as file:
        a = file.readlines()
except:sys.exit(1)
for i in a:
    i = i.rstrip()
    i = i.lstrip()
    wr.append(i)
def deNoneThing():
    global wr
    _None = False
    wrrr = wr
    wr = []
    for i in wrrr:
        i = i.rstrip().lstrip()
        if len(i) > 0:
            if i[0] != '#' and i != '/*' and i != '*/' and not _None:
                wr.append(i)
            elif i == '/*':
                _None = True
            elif i == '*/':
                _None = False
deNoneThing()

impspw = '!=()[]:+-*%,{}<>'
importWord = {'var':var,'using':imports,'glb':globalss,'if':ifss,'end':end,'while':whiles,\
              'elif':elifs,'else':elses,'new':new,'return':returns}
inWord = {'print':prints,'input':inputs,'$':compute,'int':ints,'str':strs,'number':number,'float':floats,\
          'getTime':getTime,'id':ids,'is':iss,'ending':ending,'list':lists,'file':opens,'gc':gc}
spword = {'n':'\n','t':'\t','\\':'\\','a':'\a'}
mathWord = ['+','-','*','/','//','%','**']
spspot = '~!@#$%^&*()_+`-={}|[]\\:";\'<>?,./'
threeyuan = ['==','>=','<=','>','<','!=',':','Then']
threeword = ['and','or',':','Then']
funs = {}
classes = {'list':{'pr':'list','id':str(type([])),'where':'py','def':{'change':listchange,
                                                          'get':listget,
                                                          'append':listappend},
                   'val':{'list':[]}},
           'file':{'pr':None,'id':"<class '_io.TextIOWrapper'>",'where':'py','def':{'close':fileclose,
                                                                          'read':fileread,
                                                                          'readlines':filereadlines,
                                                                          'write':filewrite},
                   'val':{'file':None}}}
spwait = {'imports':[],'end':[],'while':[],'var':[],'fun':[]}
velllllll = None

V = {'global':{}}
a = 0
ret = 0
runing = True
ifs = 0
#_None = False

getG = []


manyIf = 0
while runing:
    #if ifs == 0:
    #    print(wr[a],'> ',end='')
    if debug and ifs == 0:#CAN DEL ===============
        print(wr[a],'> ',end='')#CAN DEL ===============
    
    wrr = decode2(wr[a],a)
    #wrr = decodes(wr[a])
    #print(wrr,a,ifs)
    #print(V)
    """
    if _None:
        a += 1
        if wr[a] == '*/':
            a += 1
            _None = False"""
    if '->' in wrr:
        getG = []
        getG.append(wrr[len(wrr)-1])
        dels = 0
        for i in range(len(wrr)):
            if dels:
                del wrr[i-dels]
                dels += 1
            elif wrr[i] == '->':
                del wrr[i]
                dels += 1
    if wrr[0] == 'if':
        manyIf += 1
    if wrr[0] in importWord and ifs == 0:
        velllllll = importWord[wrr[0]](wrr)
    elif wrr[0].split('.')[0]=='System':
        wrrInWord = wrr[0].split('.')
        if wrrInWord[1] in inWord and ifs == 0:
            velllllll = inWord[wrrInWord[1]](wrr)
        elif ifs == 0:
            #print(wrr[0].split('.')[0]=='System')
            get_error(wrrInWord[1])
    elif wrr[0] == 'end':
        #print('end=-=--=-=-==--==-=-==')
        velllllll=importWord['end'](wrr)#ob after there
    elif isObFun(wrr[0]) and ifs == 0:#at this if , you can use the object
        dfsj = copy(wrr[0]).split('.')
        sadf = copy(getvar(copy(dfsj[0])))
        if sadf['where'] == 'py':
            velllllll = sadf['def'][dfsj[1]](dfsj[0],wrr)
    elif wrr[0] == 'elif' and spwait['end'][len(spwait['end'])-1][2] == manyIf:
        velllllll=importWord['elif'](wrr)
    elif wrr[0] == 'else' and spwait['end'][len(spwait['end'])-1][2] == manyIf:
        velllllll=importWord['else'](wrr)
    elif wrr[0] == 'while':
        ifs += 1
        spwait['end'].append(['while','while'])
        spwait['while'].append(['break',a-1])
    elif wrr[0] == 'if':
        spwait['end'].append(['if',False,manyIf-1])
        ifs += 1
    elif wrr[0] in funs:
        run_fun(wrr)
    elif ifs == 0:
        #print('ERROR:what is the',wrr[0],'mean? line:',a)
        #sys.exit()
        get_error(wrr[0],etype='mean')
    """elif wrr[0][0] == '#':
        pass
    elif wrr[0] == '/*':
        _None = True"""
    if len(getG):#??????????
        if not havar(getG[0],velllllll):
            V[now][getG[0]] = velllllll
        getG = []
            
    if ifs < 0:
        ifs = 0
    a += 1
    if a == len(wr):
        if now == 'global':
            ending(['"jf0"'])
        else:
            a = spwait['imports'][len(spwait['imports'])-1][1]
            wr = spwait['imports'][len(spwait['imports'])-1][0]
            now = spwait['imports'][len(spwait['imports'])-1][2]
            del spwait['imports'][len(spwait['imports'])-1]
    if debug:#CAN DEL ===============
        print()#CAN DEL ===============
    #print(V)
sys.exit(ret)
