
## 蜜罐(honeypot)和密网(honeynet)
&emsp;&emsp;蜜罐是一种以欺骗入侵者以达到采集攻击方法和保护真实主机目标的诱骗技术，其价值在于被扫描、攻击和攻陷。，以便达到对攻击活动进行监视、检测和分析。  
&emsp;&emsp;蜜网是在蜜罐技术上逐渐发展起来的一个新的概念，又可成为诱捕网络。蜜网构成了一个诱捕网络体系架构，在这个架构中，包含一个或多个蜜罐与正常生产环境混杂以达到诱骗目的。  
&emsp;&emsp;蜜罐分为几下几类：
>1．低交互式：低交互式模拟常规的服务，服务存在漏洞，但是模拟的这些漏洞无法被利用，开发和维护这种类型的蜜罐比较容易。   
2．高交互式：高交互式使用的是真实的服务，有助于发现服务存在的新漏洞，同时能够记录所有的攻击，但是，部署困难、维护成本高，一旦服务上存在的漏洞被利用，容易引发新的安全问题。  
3．粘性蜜罐(Tarpits)：这种类型的蜜罐，使用新的IP来生成新的虚拟机，模拟存在服务的漏洞，来做诱饵。因此攻击者会花费长时间来攻击，就有足够的时间来处理攻击，同时锁定攻击者。  


#### 开源蜜罐
```
Kippo        #SSH诱捕蜜罐，能够记录口令猜解、登录IP、执行命令等信息(可定义linux命令回显内容)
Dionaea      #通过模拟常见服务捕获记录完整会话过程、攻击源、IP、协议等信息，自动分析可能包含的shellcode
Honeyd       #Honeyd是一个小型守护进程，可以在网络上创建虚拟主机。可以将主机配置为运行任意服务，并且可以调整它们的个性以使它们看起来运行某些操作系统。
T-Pot        #T-Pot多蜜罐平台直接提供一个系统iso，里面使用docker技术实现多个蜜罐，更加方便的蜜罐研究与数据捕获。
```
部分蜜罐暂未学习这里只介绍Honeyd的安装及配置

#### Honeyd安装方法
平台：Ubuntu
>sudo apt-get install libevent-dev libdumbnet-dev libpcap-dev libpcre3-dev libedit-dev bison flex libtool automake  
安装zlib https://zlib.net/zlib-1.2.11.tar.gz  
git clone https://github.com/DataSoft/Honeyd.git  
cd Honeyd  
./autogen.sh  
./configure  
make  
sudo make install

### 运行
Honeyd参数
```
honeyd [OPTIONS] [net ...]

OPTIONS：
-d：非守护程序的形式，允许冗长的调试信息。
-P：轮询模式。
-l：日志文件指定了日志包和日志文件的连接。
-s：将服务状态输出记录到logfile。
-i：监听接口,指定侦听的接口，可以指定多个接口。
-p：从文件中读取nmap样式的指纹。
-x：从文件中读取xprobe风格的指纹，这个文件决定了 honeyd 如何响应 ICMP 指纹工具。
-a：从文件中读取nmap-xprobe关联。
-0：从文件中读取pf样式的OS指纹。
-u：设置Honeyd应该运行的uid 。
-g：设置Honeyd应该运行的gid。
-f：从文件中读取配置。
-c host:port:name:pass：报告开始收集。
--webserver-port=port：Web服务器侦听的端口。
--webserver-root=path：文档树的根。
--fix-webserver-permissions：更改所有权和权限。
--rrdtool-path=path：到rrdtool的路径。
--disable-webserver：禁用内部Web服务器。
--disable-update：禁用检查安全修复程序。
-V, --version
-h,--help
--include-dir：用作插件开发，指定 honeyd 存贮它的头文件的位置。

net：
指定IP地址或者网络或者IP地址范围，如果没有指定，honeyd将监视它能看见的任何IP地址的流量。
```
#### 配置
以创建一个windows为例
```
$ vim test.conf
create windows-xp   #创建一个winxp机器 windows-xp 名字可自定义
set windows-xp  ethernet "EA:94:9B:FE:57:CA" #设置xp的mac地址
set windows-xp  personality "Microsoft Windows XP SP2"  #设置版本
set windows-xp  default tcp  action reset #开启tcp应答
set windows-xp  default udp  action reset #开启udp应答
set windows-xp  default icmp action open #开启tcmp应答
add windows-xp  tcp port 80 "sh /usr/share/honeyd/scripts/win32/web.sh" #开启80端口 使用sh脚本定义相应数据 可使用python、php等配置端口应答数据。
add windows-xp  tcp port 135  open
add windows-xp  tcp port 139  open
add windows-xp  tcp port 445  open
add windows-xp  tcp port 3389 open
add windows-xp  tcp port 8080 proxy 127.0.0.1:80  #转发127.0.0.1的80端口
bind 192.168.153.142 windows-xp #将xp机器绑定到该ip
#dhcp linux on eth0 或采用dhcp分配ip
```
运行```sudo honeyd -d -f test.conf```

模拟路由拓扑
```
route entry 172.31.0.100 network 172.31.0.0/16         #定义R1入口：172.31.0.100 网络：172.31.0.0/16
route 172.31.0.100 link 172.31.0.0/24                  #直连网络：172.31.0.0/24
route 172.31.0.100 add net 172.31.1.0/24 172.31.1.100  #定义R2入口：172.31.0.100 网络：172.31.1.0/24 路由：172.31.1.100
route 172.31.1.100 link 172.31.1.0/24
create windows
set windows personality "Microsoft Windows NT 4.0 SP3"
set windows default tcp action reset
add windows tcp port 80 open
add windows tcp port 25 open
add windows tcp port 21 open
create router
set router personality "Cisco 7206 running IOS 11.1(24)"  #路由器指纹
set router default tcp action reset
add router tcp port 23 "script/router-telnet.pl"          #23端口应答
bind 172.31.0.100 router
bind 172.31.1.100 router
bind 172.31.0.20 windows
bind 172.31.0.30 windows
bind 172.31.1.15 windows
bind 172.31.1.16 windows
```
拓扑图如下：
![拓扑图](https://raw.githubusercontent.com/wz1st/test/master/image/41530077_1.jpg)  

启动```sudo honeyd -d -f test.conf```

### 其他
>honeyd作为一款低交互蜜罐，无法自主完成相应端口的数据应答；且honeyd无法响应arp请求，极容易识别为非正常服务。    
honeyd在创建蜜罐时需要真实ip，当有tcp或udp对该ip发起连接时honeyd会对此进行响应。http、ftp等返回数据需要自行定制返回数据。
