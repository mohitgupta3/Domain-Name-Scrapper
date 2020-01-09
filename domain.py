# -*- coding: utf-8 -*-
#
#   Author  : Mohit Gupta
#   Contact : mohit.gupta2jly@gmail.com
#

import os
import re
import socket 
import datetime
import time
import secrets
import random
import platform
from urllib.parse import urlsplit
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import validators
from tld import get_tld

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

# Regular expression structure to verify the URl 
# on the basis of its pattern.
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

useragents=["Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1",
			"Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1",
			"Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
			"Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0",
			"Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
			"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0",
			"Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
			"Mozilla/5.0 (Windows; U; Windows CE 5.1; rv:1.8.1a3) Gecko/20060610 Minimo/0.016",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
			"Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
			"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
			"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
			"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
			"Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
			"Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2",
			"Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0",
			"Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) QupZilla/1.2.0 Safari/534.34",
			"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1",
			"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2",
			"Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1",
			"Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
			"Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 ",
			"Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre",
			"Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0",
			"Mozilla/5.0 (X11; Linux i686; rv:6.0a2) Gecko/20110615 Firefox/6.0a2 Iceweasel/6.0a2",
			"Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0",
			"Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
			"Mozilla/5.0 (X11; Linux x86_64; en-US; rv:2.0b2pre) Gecko/20100712 Minefield/4.0b2pre",
			"Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
			"Mozilla/5.0 (X11; Linux x86_64; rv:11.0a2) Gecko/20111230 Firefox/11.0a2 Iceweasel/11.0a2",
			"Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre",
			"Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Iceweasel/5.0",
			"Mozilla/5.0 (X11; Linux x86_64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1",
			"Mozilla/5.0 (X11; U; FreeBSD amd64; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0",
			"Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8",
			"Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0",
			"Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.6) Gecko/20040406 Galeon/1.3.15",
			"Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko",
			"Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16",
			"Mozilla/5.0 (X11; U; Linux arm7tdmi; rv:1.8.1.11) Gecko/20071130 Minimo/0.025",
			"Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1",
			"Mozilla/5.0 (X11; U; Linux armv6l; rv 1.8.1.5pre) Gecko/20070619 Minimo/0.020",
			"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.10.1",
			"Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924 Epiphany/1.4.4 (Ubuntu)",
			"Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) lt-GtkLauncher",
			"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian",
			"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.277.0 Safari/532.8",
			"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8",
			"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7",
			"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Epiphany/1.2.5",
			"Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Galeon/1.3.14",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7 MG(Novarra-Vision/6.9)",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.16) Gecko/20080716 (Gentoo) Galeon/2.0.6",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0 (Swiftfox)",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/9.10 (karmic) Firefox/3.0.11",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Galeon/2.0.6 (Ubuntu 2.0.6-2)",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090803 Ubuntu/9.04 (jaunty) Shiretoko/3.5.2",
			"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330",
			"Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.2.3) Gecko/20100406 Firefox/3.6.3 (Swiftfox)",
			"Mozilla/5.0 (X11; U; Linux ppc; en-US; rv:1.8.1.13) Gecko/20080313 Iceape/1.1.9 (Debian-1.1.9-5)",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.17) Gecko/20110123 SeaMonkey/2.0.12",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091107 Firefox/3.5.5",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9",
			"Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12",
			"Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0",
			"Mozilla/5.0 (X11; U; NetBSD amd64; en-US; rv:1.9.2.15) Gecko/20110308 Namoroka/3.6.15",
			"Mozilla/5.0 (X11; U; OpenBSD arm; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0",
			"Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3",
			"Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.1) Gecko/20090702 Firefox/3.5",
			"Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.12) Gecko/20080303 SeaMonkey/1.1.8",
			"Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3",
			"Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0",
			"Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
			"Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
			"Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
			"Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
			"Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
			"Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN",
			"Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac https://m.baidu.com/mip/c/s/zhangzifan.com/wechat-user-agent.htmlOS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN",
			"Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN",
			"Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
]

acceptall = [
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
            "Accept-Encoding: gzip, deflate\r\n",
            "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
            "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
            "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
            "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
            "Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
            "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,"
            "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
            "Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
            "Accept: text/html, application/xhtml+xml",
            "Accept-Language: en-US,en;q=0.5\r\n",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
            "Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
]

referers = [
            "https://www.google.com/search?q=",
            "https://check-host.net/",
            "https://www.facebook.com/",
            "https://www.youtube.com/",
            "https://www.bing.com/search?q=",
            "https://r.search.yahoo.com/",
]

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

# headers to add to requests...
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Referer': 'https://cssspritegenerator.com',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

#    /                                                                                                                                                  \
#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /
#    \                                                                                                                                                  /

# headers = {'User-Agent': random.choice(useragents),
#             'Accept': random.choice(acceptall),
#             'Referer': random.choice(referers),
#             'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#             'Accept-Encoding': 'none',
#             'Accept-Language': 'en-US,en;q=0.8',
#             'Connection': 'keep-alive'}

# Declaration of error ID...
EID = 'EID'

records_path = 'Records/'
joint_file_name = records_path+'Main_Record.txt'
full_links_list = records_path+'All_domain_names.txt'

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

def is_internet_available():    
    # Utility function to check if internet
    # connetion is available...
    try:
        # Visit http://www.google.com to check if internet connection is available...
        urlopen('http://www.google.com', timeout = 1)
        return True
    
    except:
        # If http://www.google.com didn't respond within a second...
        return False

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

# Function to display device info, hostname and 
# IP address 
def get_sys_info(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("\t\tHostname     : ", host_name) 
        print("\t\tIP Address   : ", host_ip)
        print("\t\tPlatform     : ", platform.platform())
        print("\t\tMachine Type : ", platform.machine())
    except: 
        print("Unable to get Hostname and IP")

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

def generate_key(self):
    # To generate a unique 8 digit hash key to assign a session.
    # and validate a file
    id = secrets.token_hex(5)
    # Set the session id...
    Session_ID = id
    print('\n\tSession ID : '+Session_ID)
    return id

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /


class domain_name_scrapper:

    def print_error_msg(self, err_id, cmd):
        # Function to print an error message on various instances
        # Every single Error ID prints a unique error message...
        if (err_id == 'E0'):
            print('\n\n\t\tERROR: No valid inputs given!!\n\n')
        
        elif (err_id == 'E1'):
            print('\n\n\n\t\t\tThis application requires a working internet connection...\n\t\t\t\t\tREFRESHING!!')
        
        elif (err_id == 'E2'):
            print('\n\t\tERROR: Internet Connection lost')
        
        elif (err_id == 'E3'):
            print("\n\tSorry! unknown operation '" +cmd+ "'.\tPlease try again.")
        
        elif (err_id == 'Eun'):
            print('\n\tSorry! Internal error occured!!')
            print('\n\tEXITING!')
        
        else:
            # If Error ID isn't recognized.
            print('\n\n\t\tUnknown error occured!!')

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

    def check_directory(self):
        if (os.path.exists(records_path)):
            return True
        
        else:
            os.mkdir('Records')
            return True

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

    def generate_text_file(self):
        # A utility function to generate a new text file in every session.
        # All text files are identified by their unique ID.
        if(self.check_directory == True):
            print('\n\n\t\tAppending data on file Records/Main_Record.txt\n')
        
        else:
            print("\n\t Records directory appears to be missing, creating one...\n")

        ID = generate_key()
        
        filename = records_path+ 'Domains_Extraction_Result_' +ID+ '.txt'
        if (os.path.exists(filename)):
            self.generate_text_file()
        
        else:
            return filename

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

    def crawl_and_get(self, org_url, op_file_name):
        # Function to crawl a URl from the list and scrap the resulting domain names.
        time_durations = [1, 2, 30, 7, 3, 50, 20, 25, 2, 9, 5, 15, 35]
        
        print('\n\t Crawling url: '+ org_url +'\n')
        st_inp = 'RuntimeCheck'     # checking to see if internet connection is still available.
        if (self.check_for_internet(st_inp) == True):
            # just try to crawl the given URL and scrap data.
            # there are chances that server may block the request due to multiple
            # connection requests from the same IP.
            try:
                req = Request(url = org_url, headers = headers) 
                # save the download html...
                html = urlopen(req).read() 

                # webpage received from the server is in 'byte' format
                # we need to typecast it to string so as to be able
                # to perform operations on it.
                data = html.decode('ASCII')

                # putting the webpage on a text file so as to read it line by line.
                txt_file = open(r"domainliststring.txt","w+")
                txt_file.write(data)
            
            except:
                # If server starts blocking the requests then application 
                # will wait for a random time period and try again...
                print("\n\t ISSUE: '"+get_tld(org_url)+"' is blocking the connection, retrying..."+
                "\n\t This is not an error, it simply means that server is under heavy load..."+
                "\n\t You may wat to close the application and wait for some time."+
                "\n\t All pre-existing records are updated already...\n")

                duration = random.choice(time_durations)
                #print('\t Retrying in '+str(duration)+' second.')
                
                #time.sleep(duration)
                print("\t Retrying\n\t")
                for x in range(duration, 0, -1):
                    print(str(x)+ "\r \t\t", end="")
                    time.sleep(1)

                os.system('cls')
                self.crawl_and_get(org_url, op_file_name)

            domList = open("domainliststring.txt").read().splitlines()

            # Extracting every line from webpage 
            # code which is the part of a table...
            domains = []
            domains = re.findall(r'<td>(.*?)</td>', str(domList))

            txt_file.close()

            os.remove("domainliststring.txt")

            dom_text = open(op_file_name, 'a+')
            dom_text_main = open (joint_file_name, 'a+')
            dom_full_links_list = open(full_links_list, 'a+')

            dom_text.write('\n\n URL: ' +org_url+ '\n')
            dom_text_main.write('\n\n URL: ' +org_url+ '\n')

            for eachD in domains:
                # Validating the valid domain names and printing them on text file.
                # All 3 text files are updated constantly...
                if (validators.domain(eachD)):
                    print('\t' +eachD)
                    dom_text.write('\n\t' +eachD)
                    dom_text_main.write('\n\t' +eachD)
                    dom_full_links_list.write('\n' +eachD)
                
                else:
                    continue
            # sleep the program for 1.5 seconds beforing it proceeds 
            # to next URL to aboide bot detection by server...
            time.sleep(1.5)
        else:   
            # If no internet connection is available...
            print('\n\t\tERROR: Internet Connection lost')
            os.system('cls')
            self.crawl_and_get(org_url, op_file_name)
        
        # Close all file handeling objects after completion od scrapping operation...
        dom_text.close()
        dom_text_main.close()
        dom_full_links_list.close()

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

    def process(self, Lst, op):
        # utility function to handel text record and 
        # call the crawl_and_get function for every URL from the final list.
        Lst_empty = []
        
        if (op == 'ds'):
            # If no URLs are detected...
            if (len(Lst) < 1):
                print ('\tList of URLs appears to be empty. \n\tPlease insert some URLs to make it work. \n')
                print ('\t|-> Exiting domain scrapping function...\n')
                time.sleep(0.5)
                cmd = 'apparealomega'
                self.CLI_Utils(cmd)
            else:                
                fname = self.generate_text_file()
                
                # Fill session date and time info in records...
                with open(fname, mode = 'w+') as file:
                    file.write('Results stored on : %s.\n' % (datetime.datetime.now()))

                with open(joint_file_name, mode = 'a+') as file:
                    file.write('\n\n\nResults stored on : %s.\n' % (datetime.datetime.now()))

                for i in Lst:
                    self.crawl_and_get(i, fname)
                
                # All requested crawling operations 
                # are completed at this point...
                print('\n\tAll requested URLs are crawled and results are stored in ' +fname)
                Lst_empty = []

                oprn = 'take_cmd'
                self.process(Lst_empty, oprn)
                Session_ID = None

        # Take command from user for next operation with a different session ID...
        elif (op == 'take_cmd'):
            ip = input('\t-->>')
            self.CLI_Utils(ip)

        # Still, if something else happened
        # which is not determined in this if-else structure...
        else:
            print('\n\tSorry! Internal error occured!!')
            print('\n\tEXITING!')
            time.sleep(5)
            exit()

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

    def enter_url(self, flag):
        # Function to take input URLs which are then filtered
        # and passed to process() function.
        if (flag == True):
            print("\n\tEnter the website urls one by one \n\tWrite 'etc' and press enter when you are done entering urls.\n")

            lst = ['https://www.example.com']

            url = 'https://www.example.com'

            url_index = 1

            # Keep entering URLs until 'etc' is entered.
            while (url != 'etc'):
                url = input("\n\tEnter the url " +str(url_index)+ ": ")
                
                if(url == ' ' or url == ''):
                    continue
                
                elif (re.match(regex, url) is None and url != 'etc'):
                    print('\t\tNot a valid URL or keyword, skipping!')
                    continue                
                
                else:
                    lst.append(url)
                    url_index = url_index + 1                
                    
                    if (url != 'etc'):
                        print('\t\tAdded URl: (' +url+')')
                        print('\t\t\tTop Level Domain: ' +get_tld(url))
                    
                    else:
                        continue

            url_index = 0
            # print(lst[0])
            # print(lst[-1])
            del lst[0]
            del lst[-1]
            oprn = 'ds'
            print('\n\tProcessing ' +str(len(lst))+ ' URLs.\n')
            # print(lst)
            self.process(lst, oprn)

        else:
            print('Sorry, invalid operation.')
            exit()

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

    # Help message.
    helpmsg = """ \t+----------------------------+----------------------------------------------------+
        |     Command                |     Operation                                      |
        +----------------------------+----------------------------------------------------+
        |                            |                                                    |
        |  --domain_scanning or -ds  |  To scan domains out of a given or multiple URLs.  |
        |                            |                                                    |
        |  --check_inet or -ci       |  To check for internet connection.                 |
        |                            |                                                    |
        |  --network_info or -ni     |  To get the network information.                   |
        |                            |                                                    |
        |  --help or -h              |  To check for available options.                   |
        |                            |                                                    |
        |  exit                      |  To exit the terminal.                             |
        |                            |                                                    |
        |  --app_info or -apinf      |  For application info.                             |
        |                            |                                                    |
        +----------------------------+----------------------------------------------------+
        """
    app_info = """ \t+---------------------+-------------------------------------------------+
        |   Name              |  'Domain Name Extractor'                        |
        |                     |                                                 |
        |   Description       |  A domain name extraction tool, to scan domain  |
        |                     |  names out of a given or multiple URLs          |
        |                     |  destination web pages.                         |
        |                     |                                                 |
        |   Version           |  1.10 (stable)                                  |
        |                     |                                                 |
        +---------------------+-------------------------------------------------+
        """

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

    def CLI_Utils(self, command):
        # Command Line Tools to handle arguments.
         
        # To reinitialize the CLI_Utils functionality...
        if (command == 'take_cmd'):
            cmd = input ("\n\tPlease enter the desired operation.\n\tEnter --help or -h for help\n\t-->> ")
            self.CLI_Utils(cmd)
        
        # If help message is asked...
        elif(command == '--help' or command == '-h'):
            print('\tFollowing commands are supported:\n')
            print(domain_name_scrapper.helpmsg)
            command = input('\t-->> ')
            self.CLI_Utils(command)
        
        # If domain scanning functionality is asked...
        elif(command == '--domain_scanning' or command == '-ds'):
            Flag = True
            self.enter_url(Flag)

        # If internet availability checkup is asked...
        elif(command == '--check_inet' or command == '-ci'):
            inet_status = is_internet_available()
            
            if(inet_status == True):
                print('\n\t\tInternet connection is working...\n')
            
            else:
                # If google didn't respond within 1 second...
                print('\t\tInternet connection is either unstable or not working...\n')
            command = input('\t-->> ')
            self.CLI_Utils(command)
        
        # If Network hardware info is asked...
        elif(command == '--network_info' or command == '-ni'):
            get_sys_info()
            command = input('\n\t-->> ')
            self.CLI_Utils(command)
        
        # If application information is asked...
        elif(command == '--app_info' or command == '-apinf'):
            print(domain_name_scrapper.app_info)
            print('\tMade with <3 at Vanisb Technology. ;-)\n')
            self.CLI_Utils(command = 'apparealomega')

        elif (command == 'exit'):
            exit()
        
        # If new input is required or the current operation is completed...
        elif (command == 'apparealomega'):
            cmd= input('\t-->>')
            self.CLI_Utils(cmd)

        # If no input is detected...
        elif (command == '' or command == ' '):
            cmd= input('\t-->>')
            self.CLI_Utils(cmd)
        
        # If the command entered is not recognized...
        else:
            print("\tSorry! unknown operation '" +command+ "'.\tPlease try again.\n")
            self.CLI_Utils(command = 'apparealomega')

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

    def check_for_internet(self, state): 
        # To check for a working internet connection
        # on various instances...   
        if (state == 'Startup'):
            print('\tChecking for Internet connection...')
            if(is_internet_available() == True):
                print('\n\t|-> Internet connection available.\n')
                cmd = input ("\n\tPlease enter the desired operation.\n\tEnter --help or -h for help\n\t-->> ")
                self.CLI_Utils(cmd)
            else:
                print('\n\n\n\t\t\tThis application requires a working internet connection...\n\n\t\t\t\t\tREFRESHING!!')
                os.system('cls')
                main()

        # Check for a working internet connection 
        # during the parsing of URL...
        elif (state == 'RuntimeCheck'):
            if(is_internet_available() == True):
                return True
            else:
                return False
        
        else:
            print('\n\n\t\tERROR: Internet Connection Lost!!')

#    /                                                                                                                                                  \
#   /_|_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=_=*^*=|_\
# <---|      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |--->
#   \-|*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=*=+_+=|-/
#    \                                                                                                                                                  /

def main():
    # Driver function.
    os.system('echo off && title Domain Names Extractor && color a && cls')

    ds = domain_name_scrapper()

    # Check if the records directory is present.
    # If not present create one...
    ds.check_directory()

    st = 'Startup'
    # Checking to see if internet connection
    # is available...
    ds.check_for_internet(st)
    
if __name__=='__main__':
    # Adjust the console window size to optimum dimentions..
    # os.system('mode 100, 35')
    main()


'''
*******************  Test URL(s)  ********************

https://viewdns.info/reverseip/?host=103.134.55.18&t=1
https://viewdns.info/reverseip/?host=103.134.55.5&t=1
https://viewdns.info/reverseip/?host=103.138.10.54&t=1
https://viewdns.info/reverseip/?host=103.16.199.85&t=1
https://viewdns.info/reverseip/?host=103.16.223.13&t=1
https://viewdns.info/reverseip/?host=103.17.76.2&t=1
https://viewdns.info/reverseip/?host=103.18.77.86&t=1
https://viewdns.info/reverseip/?host=103.195.142.3&t=1
https://viewdns.info/reverseip/?host=103.197.89.57&t=1

'''