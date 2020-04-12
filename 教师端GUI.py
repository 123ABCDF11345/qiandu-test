"""使用腾讯COS做在线发送（qcloud_cos) key已删除"""
import json
import time
import datetime
import tkinter
import tkinter.messagebox
from tkinter import ttk
import random
import os
from threading import Thread
from qcloud_cos import CosConfig#大佬不想安包的可以注释掉这两行，只影响在线发题功能
from qcloud_cos import CosS3Client
import sys
"""日记导入和配置"""
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='Teacher.log', level=logging.INFO, format=LOG_FORMAT)
logging.info("---------程序启动---------")
import requests
import webbrowser
import socket
"""初始参数"""
proxies = {'http': 'http://52.179.231.206:80', 'https': 'https://52.179.231.206:80'}#代理设置，用来检查更新加速的（暂时没法用）
NewTiDict0={}
SetDict0={"jisuan":0,"inter":0,"say":0}
"""多线程"""
port_number = "8082"
def run_on(port):
    pid2 = os.getpid()
    try:
        os.system("python -m http.server " + port)
    except:
        tkinter.messagebox.showerror('错误','局域网服务器建立失败，请检查权限设置，端口占用和系统要求')
        logging.error("局域网建立失败")
server= Thread(target=run_on, args=[port_number])
"""COS在线发送"""
secret_id = '省略'
secret_key = '省略'
region = 'ap-guangzhou'
token = None
scheme = 'https'
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)
"""获取所在环境"""
pid1 = os.getpid()
workhome=os.getcwd()
#更新删除旧文件
pathlist = os.listdir(workhome)
for filename in pathlist:
    if filename.endswith('oldexe'):
        os.remove(filename)
#
havehome=os.path.exists(workhome+"/test")
logging.info("成功获取目录和判断文件")
pid = os.getpid()
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
ip=get_host_ip()
"""环境改变"""
if havehome==False:
    os.mkdir(workhome+"/test")
    logging.warning("初次建立文件夹")
def net_is_used(port, ip):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,port))
        s.shutdown(2)
        return True
    except Exception as e:
        return False
portuse=net_is_used(8082,ip)
"""关闭窗口事件响应"""
def CloseWindows(do):
    if do=="All":
        os.system("taskkill /pid "+str(pid1))#关闭进程
        os.system("taskkill /IM python.exe")#对开发者极度不友好（doge）
        try:
            os.system("taskkill /pid "+str(pid2))
        except:
            pass
        exit()#备用操作，关闭局域网进程（肯定没用）（doge）
    if do=="Some":
        exit()
def exitforme():
    EX=tkinter.Toplevel()
    EX.title('退出')
    btnExitAll=tkinter.Button(EX,text='彻底退出（关闭进程）',command=lambda:CloseWindows("All"))
    btnExitAll.place(x=10,y=5,width=200,height=30)
    btnExitSome=tkinter.Button(EX,text='正常退出（局域网功能后台保留）',command=lambda:CloseWindows("Some"))
    btnExitSome.place(x=10,y=40,width=200,height=30)
"""函数定义"""
def CG():
    CG=tkinter.Toplevel()
    CG.title('查询成绩')
    CGLabel1 = tkinter.Label(CG,text='您的考试编号： ').grid(row=0,column=0)
    CGv1 = tkinter.StringVar()
    CGe1 = tkinter.Entry(CG,textvariable=CGv1)
    CGe1.grid(row=0,column=1,padx=10,pady=5)
    def linshi():
        CGnumber=CGe1.get()
        tkinter.messagebox.showinfo('设置','功能未开放，查询编号：'+CGnumber)
        logging.warning("试图访问未开发设置")
        CG.destroy()
    tkinter.Button(CG,text='查询成绩',width=10,command=linshi)\
        .grid(row=2,column=0,sticky="W",padx=10,pady=5)
def SysSet():
    Sysset=tkinter.Toplevel()
    Sysset.title('系统设置')
    Sysset.geometry('240x175')
    btnLau=tkinter.Button(Sysset,text='更改语言',command=lambda:SysSetDo("lau"))
    btnLau.place(x=10,y=5,width=220,height=30)
    btnKey=tkinter.Button(Sysset,text='更改账户和密码',command=lambda:SysSetDo("key"))
    btnKey.place(x=10,y=35,width=220,height=30)
    btnCheck=tkinter.Button(Sysset,text='检查更新',command=lambda:SysSetDo("newapp"))
    btnCheck.place(x=10,y=70,width=220,height=30)
    btnAbout=tkinter.Button(Sysset,text='关于我们',command=lambda:SysSetDo("about"))
    btnAbout.place(x=10,y=105,width=220,height=30)
    btnCloseInter=tkinter.Button(Sysset,text='强制关闭端口监听服务',command=lambda:SysSetDo("stopsever"))
    btnCloseInter.place(x=10,y=140,width=220,height=30)
    btnVPN=tkinter.Button(Sysset,text='代理设置',command=lambda:SysSetDo("VPN"))
    btnVPN.place(x=10,y=175,width=220,height=30)



def SysSetDo(dowhat):
    if dowhat=="lau":
        SysLau=tkinter.Toplevel()
        SysLau.title('语言')
        SysLau.geometry('160x90')
        def laucheck(*args):
            if comboxlist.get()!="简体中文":
                tkinter.messagebox.showerror('错误','抱歉，该语言暂未翻译')
                logging.warning("试图访问未开发语言")
                SysLau.destroy()
        comvalue=tkinter.StringVar()#窗体自带的文本，新建一个值
        comboxlist=ttk.Combobox(SysLau,textvariable=comvalue) #初始化
        comboxlist["value"]=("简体中文","English(US)","繁體中文")
        comboxlist.current(0)  #选择第一个
        comboxlist.bind("<<ComboboxSelected>>",laucheck)  #绑定事件,(下拉列表框被选中时，绑定go()函数)
        LauLabel1 = tkinter.Label(SysLau,text='语言:').grid(row=0,column=0)
        comboxlist.place(x=70,y=1,width=80,height=25)
    elif dowhat=="key":
        def SaveInKey():
            mima=eKey.get()
            filename="mima.txt"
            with open(filename,"w")as file_object:
                file_object.write(mima)
            logging.info("写入并更改了密码")
            SysKey.destroy()
        SysKey=tkinter.Toplevel()
        SysKey.title('更改账户和密码')
        SysKey.geometry('300x90')
        labelUser=tkinter.Label(SysKey,text="账户")
        labelUser.place(x=3,y=1,width=40,height=25)
        contentName =tkinter.StringVar()
        contentName.set('admin')
        eName= tkinter.Entry(SysKey,
            textvariable=contentName,
            state="disabled")
        eName.place(x=50,y=1,width=100,height=25)
        filename="./test/mima.txt"
        try:
            with open(filename)as file_object:
                mima=file_object.read()
        except FileNotFoundError:
            mima="0000"
        labelKey=tkinter.Label(SysKey,text="密码")
        labelKey.place(x=3,y=30,width=40,height=25)
        contentKey =tkinter.StringVar()
        contentKey.set(mima)
        eKey= tkinter.Entry(SysKey,textvariable=contentKey)
        eKey.place(x=50,y=30,width=100,height=25)
        btnSave=tkinter.Button(SysKey,text='保存并退出',bg="orange",command=lambda:SaveInKey())
        btnSave.place(x=160,y=5,width=80,height=50)
    elif dowhat=="newapp":
        a=tkinter.messagebox.askquestion('更新','确定要联网检查Github更新吗？(将关闭局域网系统）')
        if a==False:
            pass
        else:
            logging.info("试图检查更新")
            api_url = "https://api.github.com/repos/qiandu-smart/qiandu-test/releases/latest"
            try:
                all_info = requests.get(api_url).json()
            except FileNotFoundError:
                tkinter.messagebox.showerror('错误','访问服务器失败，请检查网络或使用代理')
                logging.error("链接网络失败，无法检查更新")
            else:
                now_tag="v1.0.0-alpha"
                new_tag = all_info["tag_name"]
                github_url=all_info["assets"][1]["browser_download_url"]
                #quick_url="https://www.free-music.cf/-----"+github_url
                if new_tag!=now_tag:
                    new_tag_name="teacher-"+new_tag+".exe"
                    tkinter.messagebox.showinfo('更新','检测到新版本，当前版本号'+now_tag+'，最新版本号'+new_tag+"，准备热更新\n请注意，由于一些不可描述的原因，更新时间可能很长，请耐心等待\n我们强烈建议您开启自动更新，程序启动时将在后台自动更新")
                    a=tkinter.messagebox.askyesno('代理', '代理下载暂时无法使用，请点击“否”')
                    if a==False:
                        r = requests.get(github_url)
                    else:
                        try:
                            github_url=github_url.replace("https", "http")
                            r=requests.get(github_url, proxies=proxies, verify=False)
                        except:
                            tkinter.messagebox.showerror('错误','代理服务器访问失败，即将启动普通下载')
                            r = requests.get(github_url)
                    with open(new_tag_name, "wb") as code:
                        code.write(r.content)
                    tkinter.messagebox.showinfo('更新','更新完成，单击确定关闭程序，请您自行重新打开程序（位于同目录下的最新版本）')
                    exit()

                else:
                    tkinter.messagebox.showinfo('更新','当前程序已是最新版本，感谢您的支持')
    elif dowhat=="about":
        def openourinter():
            logging.info("拉起浏览器")
            try:
                webbrowser.open("https://qianduzhineng.github.io/")
            except:
                tkinter.messagebox.showerror('错误','无法拉起浏览器，非常见错误，请检查系统版本')
                logging.error("拉起失败")
        SysAbout=tkinter.Toplevel()
        SysAbout.title('关于')
        SysAbout.geometry('550x180')
        labelAbout=tkinter.Label(SysAbout,text="这里应该有标题的，奇怪了")
        labelAbout.place(x=230,y=3,width=230,height=25)
        labelAbout1=tkinter.Label(SysAbout,text="本项目所有权归123ABCDF11345所有，发行者有且只有Github-123ABCDF11345")
        labelAbout1.place(x=3,y=30,width=520,height=25)
        labelAbout2=tkinter.Label(SysAbout,text="本项目受AGPL通用公共许可证v3.0（GNU Affero General Public License v3.0）保护，不得抄袭套作")
        labelAbout2.place(x=3,y=60,width=520,height=25)
        labelAbout3=tkinter.Label(SysAbout,text="非商业盈利软件 不可倒卖和二次发行")
        labelAbout3.place(x=3,y=90,width=520,height=25)
        btnOur=tkinter.Button(SysAbout,text='打开官网',bg="orange",command=lambda:openourinter())
        btnOur.place(x=250,y=120,width=80,height=50)
    elif dowhat=="stopsever":
        server.join()
        tkinter.messagebox.showinfo('设置','端口解除占用成功')
        logging.info("解除了端口占用")
    elif dowhat=="VPN":
        tkinter.messagebox.showwarning('警告','代理设置属于高级设置，请慎用')
        def Savevpn():
            proxies=eKey.get()
            proxies=eval(proxies)
            logging.info("更改代理")
            SysKey.destroy()
        SysKey=tkinter.Toplevel()
        SysKey.title('代理设置')
        SysKey.geometry('600x90')
        labelUser=tkinter.Label(SysKey,text="协议")
        labelUser.place(x=3,y=1,width=40,height=25)
        contentName =tkinter.StringVar()
        contentName.set('HTTPS')
        eName= tkinter.Entry(SysKey,
            textvariable=contentName,
            state="disabled")
        eName.place(x=50,y=1,width=100,height=25)
        labelKey=tkinter.Label(SysKey,text="ip端口（请直接填充ip和端口，勿改其他）")
        labelKey.place(x=3,y=30,width=600,height=25)
        contentKey =tkinter.StringVar()
        contentKey.set(proxies)
        eKey= tkinter.Entry(SysKey,textvariable=contentKey)
        eKey.place(x=50,y=30,width=450,height=25)
        btnSave=tkinter.Button(SysKey,text='保存并退出',bg="orange",command=lambda:Savevpn())
        btnSave.place(x=505,y=5,width=80,height=50)
def Set():
    def WriteSet(what,SetDict=SetDict0):
        if what=="jisuan":
            SetDict.update({"jisuan":1})
            tkinter.messagebox.showinfo('设置','完成设置')
        elif what=="inter":
            SetDict.update({"inter":1})
            tkinter.messagebox.showinfo('设置','完成设置')
        elif what=="say":
            SetDict.update({"say":1})
            Sayset=tkinter.Toplevel()
            Sayset.title('公告设置')
            SayLabel1 = tkinter.Label(Sayset,text='公告： ').grid(row=0,column=0)
            Sayv1 = tkinter.StringVar()
            Saye1 = tkinter.Entry(Sayset,textvariable=Sayv1)
            Saye1.grid(row=0,column=1,padx=10,pady=5)
            def linshi():
                SetDict.update({"saywhat":Saye1.get()})
                Sayset.destroy()
            tkinter.Button(Sayset,text='保存并退出',width=10,command=linshi)\
                .grid(row=2,column=0,sticky="W",padx=10,pady=5)
        elif what=="allclose":
            logging.info("试图重置设置")
            SetDict={"jisuan":0,"inter":0,"say":0}
            logging.info("重置了设置")
            tkinter.messagebox.showinfo('设置','已完成重置，请手动点击保存')
        elif what=="Save":
            json_str = json.dumps(SetDict)
            with open('./test/Set.json', 'w') as json_file:
                json_file.write(json_str)
            tkinter.messagebox.showinfo('设置','成功保存')
            logging.info("保存了设置")
            Allset.destroy()
    Allset=tkinter.Toplevel()
    Allset.title('考试设置')
    Allset.geometry('240x175')
    btnUseCom=tkinter.Button(Allset,text='允许学生端使用本应用内建计算器',command=lambda:WriteSet("jisuan"))
    btnUseCom.place(x=10,y=5,width=220,height=30)
    btnNointer=tkinter.Button(Allset,text='禁止学生访问网络（Bate）(使用DNS污染)',command=lambda:WriteSet("inter"))
    btnNointer.place(x=10,y=35,width=220,height=30)
    btnTitle=tkinter.Button(Allset,text='学生端公告(将在考试开始时提醒学生)',command=lambda:WriteSet("say"))
    btnTitle.place(x=10,y=70,width=220,height=30)
    btnFin=tkinter.Button(Allset,text='重置所有设置',bg="orange",command=lambda:WriteSet("allclose"))
    btnFin.place(x=10,y=105,width=220,height=30)
    btnSave=tkinter.Button(Allset,text='保存并退出',bg="orange",command=lambda:WriteSet("Save"))
    btnSave.place(x=10,y=140,width=220,height=30)


def NoneDO(*args):
    time.sleep(1)
    tkinter.messagebox.showerror('错误','抱歉，暂无此功能')
def MakeTi():
    NewTiDict=NewTiDict0
    print(NewTiDict)
    top=tkinter.Toplevel()
    top.title('试题录入')
    top.geometry('320x170')
    def Write(finish,NewTiDict=NewTiDict,json_str=""):
        NewTiDict.update({tope1.get(): tope2.get()})
        top.destroy()
        if finish==True:
            logging.info("试图写入题目")
            json_str = json.dumps(NewTiDict)
            with open('./test/Ti.json', 'w') as json_file:
                json_file.write(json_str)
            logging.info("写入成功")
        else:
            logging.info("重新绘制窗口录入题目")
            MakeTi()
    TopLabel1 = tkinter.Label(top,text='请输入题目').grid(row=0,column=0)
    TopLabel2 = tkinter.Label(top,text='请输入答案').grid(row=1,column=0)
    topv1 = tkinter.StringVar()
    topv2 = tkinter.StringVar()
    tope1 = tkinter.Entry(top,textvariable=topv1)
    tope2 = tkinter.Entry(top,textvariable=topv2)
    tope1.grid(row=0,column=1,padx=30,pady=10)
    tope2.grid(row=1,column=1,padx=30,pady=10)
    btnMore=tkinter.Button(top,text='录入下一题',command=lambda:Write(False))
    btnMore.place(x=30,y=120,width=80,height=45)
    btnFinish=tkinter.Button(top,text='完成所有录入',command=lambda:Write(True))
    btnFinish.place(x=120,y=120,width=80,height=45)
def Now():
    makeset=tkinter.Toplevel()
    makeset.title('发送方式')
    makeset.geometry('415x135')
    def Inter(whice):
        if whice==True:
            logging.info("在线发送服务启动")
            InterNumber=str(random.randint(100000,999999))
            TiNumber="Ti"+InterNumber+".json"
            try:
                with open("./test/Ti.json", 'rb') as fp:
                    response = client.put_object(Bucket='gao-ta-1300361781',Body=fp,Key=TiNumber,
                        StorageClass='STANDARD',EnableMD5=False)
                    logging.info("上传了题目")
                try:
                    with open("./test/Set.json", 'rb') as fp:
                        response = client.put_object(Bucket='gao-ta-1300361781',Body=fp,Key="Set"+InterNumber+".json",
                            StorageClass='STANDARD',EnableMD5=False)
                except FileNotFoundError:
                    tkinter.messagebox.showerror('错误','请先进行考试设置，没有想要打开的设置也请单击保存')
                    logging.error("未找到设置文件")
                else:
                    logging.info("上传了设置")
                    tkinter.messagebox.showinfo('在线发送','已完成发送，请牢记您的考试编号，在学生端需要它： '+InterNumber)
                    makeset.destroy()
            except:
                tkinter.messagebox.showerror('错误','无法访问服务器，请检查网络')
                logging.error("在线发送失败")
        elif whice==False:
            time.sleep(1)
            tkinter.messagebox.showinfo('离线发送','请将文件夹“test”下的Ti.json和Set.json文件手动拷贝至学生机器（请先在学生机器上安装学生端）')
        else:
            if portuse==True:
                tkinter.messagebox.showerror('错误','8082端口被占用，无法运行')
            else:
                logging.info("局域网设置启用")
                tkinter.messagebox.showinfo('局域网发送','注意：您需要满足以下条件才可使用局域网发送\n 1.系统使用Windows 7/8/8.1或Windows 10 1803以上\n 2.局域网没有涉及Simple服务的限制\n 3.允许其他设备访问本设备的8082端口\n 4.8082端口没有被占用（一般来说不会）\n 5.同意Python和Windows ftp服务通过防火墙（稍后您便会得到系统提示）')
                tkinter.messagebox.showinfo('局域网发送','注意：本方法需要以下权限\n 1.访问您的局域网\n 2.打开您电脑的8082端口\n 3.使专用于储存题目的文件夹在整个网络可见（不会包含其他文件夹）\n 4.公示您的IP\n 5.获取您的局域网、电脑管理员权限（可能需要的）')
                try:
                    server.start()
                except:
                    tkinter.messagebox.showerror('错误','局域网服务器建立失败，请检查权限设置，端口占用和系统要求')
                    logging.error("局域网建立失败")
                else:
                    logging.info("成功建立局域网系统")
                    tkinter.messagebox.showinfo('局域网发送','成功建立局域网系统!\n注意！您需要在整个考试过程（从现在至查看所有人成绩）都不能关闭此应用，否则可能导致学生提交失败！\n 当然，您也可以后台访问其他应用 \n一般而言，程序会自动关闭端口监听业务，为保险起见，在考试结束后，请在主页使用“系统设置-强制关闭端口监听服务”功能')
                    makeset.destroy()

    btnOnin=tkinter.Button(makeset,text='在线发送（无需配置，推荐）',command=lambda:Inter(True))
    btnOnin.place(x=10,y=5,width=400,height=30)
    btnInin=tkinter.Button(makeset,text='离线手动发题（没有网络时或在线无法使用时）',command=lambda:Inter(False))
    btnInin.place(x=10,y=35,width=400,height=30)
    btnOnju=tkinter.Button(makeset,text='局域网发送（无需配置，安全性高，但可用性依靠于您的局域网和系统）',command=lambda:Inter("small"))
    btnOnju.place(x=10,y=70,width=400,height=30)
def jiaoshikongzhitai():
    every=tkinter.Tk()
    every.resizable(False,False)
    every.title('智能教学')
    every.protocol('WM_DELETE_WINDOW',exitforme)
    btnWrite=tkinter.Button(every,text='试题录入',command=lambda:MakeTi())
    btnWrite.place(x=15,y=20,width=80,height=55)
    btnSet=tkinter.Button(every,text='考试设置',command=lambda:Set())
    btnSet.place(x=100,y=20,width=80,height=55)
    btnOnset=tkinter.Button(every,text='系统设置',command=lambda:SysSet())
    btnOnset.place(x=15,y=80,width=80,height=55)
    btnOnset=tkinter.Button(every,text='开始考试',bg="red",command=lambda:Now())
    btnOnset.place(x=100,y=80,width=80,height=55)
    btnOnset=tkinter.Button(every,text='查看成绩',bg="red",command=lambda:CG())
    btnOnset.place(x=45,y=140,width=80,height=35)
"""登录"""
logging.info("GUI主程序启动")
root=tkinter.Tk()
root.resizable(False,False)
root.title('登录')
filename="./test/mima.txt"
try:
    with open(filename)as file_object:
        mima=file_object.read()
except FileNotFoundError:
    logging.info("没有密码设定文件，返回0000")
    mima="0000"
Label1 = tkinter.Label(root,text='账户（暂不支持自定义，请输入admin):').grid(row=0,column=0)
Label2 = tkinter.Label(root,text='密码 （注意区分大小写):').grid(row=1,column=0)

v1 = tkinter.StringVar()
p1 = tkinter.StringVar()
e1 = tkinter.Entry(root,textvariable=v1)    # Entry 是 Tkinter 用来接收字符串等输入的控件.
e2 = tkinter.Entry(root,textvariable=p1,show='*')
e1.grid(row=0,column=1,padx=10,pady=5)  #设置输入框显示的位置，以及长和宽属性
e2.grid(row=1,column=1,padx=10,pady=5)

def show():
    if e1.get()!= "admin":
        tkinter.messagebox.showerror('错误','账户暂不支持自定义，请输入admin')
        logging.warning("账户输入错误")
    elif mima == e2.get():
        root.destroy()
        jiaoshikongzhitai()
    else:
        tkinter.messagebox.showerror('错误','密码错误,请重试')
        logging.warning("密码错误")
tkinter.Button(root,text='确定',width=10,command=show)\
    .grid(row=2,column=0,sticky="W",padx=10,pady=5)

tkinter.Button(root,text='退出',width=10,command=root.quit)\
    .grid(row=2,column=1,sticky="E",padx=10,pady=5)
if portuse==True:
    tkinter.messagebox.showerror('错误','检测到8082端口正在使用，局域网发题功能将无法使用！请尝试结束使用端口的进程！\n当然，如果您忽略此提示，仅有局域网发题受到影响，不影响其他功能\nPS.大多数情况是上次退出时的意外占用，请打开任务管理器结束所有以”python“开头的进程，然后重新运行程序')
"""消息循环"""
root.mainloop()
#https://blog.csdn.net/m0_38039437/article/details/80546167 为此项目提供了很大的帮助，感谢！！！