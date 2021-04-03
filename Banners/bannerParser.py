import re

text = '''<?xml version='1.0' encoding='UTF-8'?>
<fingerprints protocol="telnet" database_type="service" preference=".80">

  <fingerprint pattern="\A(?i)(?:\r|\n)*login:\s*$">
    <description>bare 'login:' -- assert nothing.</description>
    <example>login:</example>
  </fingerprint>

  <fingerprint pattern="\A(?i)(?:\r|\n)*User(?:name)?\s*:\s*$">
    <description>bare 'Username:' -- assert nothing.</description>
    <example>Username:</example>
    <example>User:</example>
  </fingerprint>

  <fingerprint pattern="\A(?i)(?:\r|\n)*Password:\s*$">
    <description>bare 'Password:' -- assert nothing.</description>
    <example>Password:</example>
  </fingerprint>

  <fingerprint pattern="\A(?i)(?:\r|\n)*Account:\s*$">
    <description>bare 'Account:' -- assert nothing.</description>
    <example>Account:</example>
  </fingerprint>

  <fingerprint pattern="\A(?i)Connection refused(?:\r|\n)*$">
    <description>bare 'Connection refused' -- assert nothing.</description>
    <example>Connection refused</example>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*User Access Verification(?:\r|\n)+(?:Username|Password):\s*$">
    <description>Cisco switch or router - user access variant</description>
    <!-- User Access Verification\r\n\r\nUsername: -->

    <example _encoding="base64">VXNlciBBY2Nlc3MgVmVyaWZpY2F0aW9uDQoNClVzZXJuYW1lOgo=</example>
    <!-- User Access Verification\r\n\r\nPassword: -->

    <example _encoding="base64">VXNlciBBY2Nlc3MgVmVyaWZpY2F0aW9uDQoNClBhc3N3b3JkOgo=</example>
    <param pos="0" name="service.vendor" value="Cisco"/>
    <param pos="0" name="os.vendor" value="Cisco"/>
    <param pos="0" name="hw.vendor" value="Cisco"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Password required, but none set(?:\r|\n)*$">
    <description>Cisco switch or router - password not set variant</description>
    <example>Password required, but none set</example>
    <param pos="0" name="service.vendor" value="Cisco"/>
    <param pos="0" name="os.vendor" value="Cisco"/>
    <param pos="0" name="hw.vendor" value="Cisco"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*MikroTik v([\w.]+)(?: \([\w-]+\))?(?:\r|\n)+Login:\s*$">
    <description>MikroTik RouterOS</description>
    <!-- MikroTik v5.2\r\nLogin: -->

    <example _encoding="base64" os.version="5.2">TWlrcm9UaWsgdjUuMg0KTG9naW46Cg==</example>
    <!-- MikroTik v6.42.3 (stable)\r\nLogin: -->

    <example _encoding="base64" os.version="6.42.3">TWlrcm9UaWsgdjYuNDIuMyAoc3RhYmxlKQ0KTG9naW46Cg==</example>
    <!-- MikroTik v6.40.8 (bugfix)\r\nLogin: -->

    <example _encoding="base64" os.version="6.40.8">TWlrcm9UaWsgdjYuNDAuOCAoYnVnZml4KQ0KTG9naW46Cg==</example>
    <!-- MikroTik v6.36rc12 (testing)\r\nLogin: -->

    <example _encoding="base64" os.version="6.36rc12">TWlrcm9UaWsgdjYuMzZyYzEyICh0ZXN0aW5nKQ0KTG9naW46Cg==</example>
    <!-- MikroTik v6.42.9 (long-term)\r\nLogin: -->

    <example _encoding="base64" os.version="6.42.9">TWlrcm9UaWsgdjYuNDIuOSAobG9uZy10ZXJtKQ0KTG9naW46Cg==</example>
    <param pos="0" name="os.vendor" value="MikroTik"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="0" name="os.product" value="RouterOS"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:mikrotik:routeros:{os.version}"/>
    <param pos="0" name="hw.vendor" value="MikroTik"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)?ZXHN (\w+)(?: V([\d.]+))?(?:\r|\n)*Login:\s*$">
    <description>ZTE ZXHN router</description>
    <!-- ZXHN H108N\r\nLogin: -->

    <example _encoding="base64" hw.product="H108N">WlhITiBIMTA4Tg0KTG9naW46Cg==</example>
    <!-- ZXHN H298A V1.1\r\nLogin: -->

    <example _encoding="base64" hw.product="H298A" hw.version="1.1">WlhITiBIMjk4QSBWMS4xDQpMb2dpbjoK</example>
    <!-- ZXHN H367N\r\n\rLogin: -->

    <example _encoding="base64" hw.product="H367N">WlhITiBIMzY3Tg0KDUxvZ2luOgo=</example>
    <param pos="0" name="hw.vendor" value="ZTE"/>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="0" name="hw.family" value="ZXHN"/>
    <param pos="1" name="hw.product"/>
    <param pos="2" name="hw.version"/>
  </fingerprint>

  <fingerprint pattern="^(F6\d+\w?)\r\n\rLogin:\s*$">
    <description>ZTE F6xx series GPON router</description>
    <!-- F668\r\n\rLogin: -->

    <example _encoding="base64" hw.product="F668">RjY2OA0KDUxvZ2luOgo=</example>
    <!-- F612W\r\n\rLogin: -->

    <example _encoding="base64" hw.product="F612W">RjYxMlcNCg1Mb2dpbjoK</example>
    <param pos="0" name="hw.vendor" value="ZTE"/>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*DD-WRT v([\d.]+)(?:-(\w+))? ([\w-]+) \(c\) \d{4} NewMedia-NET GmbH(?:\r|\n)+Release: \d+\/\d+\/\d+ \(SVN revision: ([:\w]+)\)(?:\r|\n)+.* login:\s*$">
    <description>DD-WRT - 24 family</description>
    <!-- DD-WRT v24-sp2 mini (c) 2013 NewMedia-NET GmbH\r\nRelease: 05/27/13 (SVN revision: 21676)\r\n\r\nDD-WRT login: -->

    <example _encoding="base64" os.version="24" os.version.version="sp2" os.edition="mini" os.build="21676">
      REQtV1JUIHYyNC1zcDIgbWluaSAoYykgMjAxMyBOZXdNZWRpYS1ORVQgR21iSA0KUmVsZWFzZ
      TogMDUvMjcvMTMgKFNWTiByZXZpc2lvbjogMjE2NzYpDQoNCkRELVdSVCBsb2dpbjoK
    </example>
    <!-- DD-WRT v24 micro (c) 2010 NewMedia-NET GmbH\r\nRelease: 08/07/10 (SVN revision: 14896)\r\n\r\nProliant DL980R07 X6550 8-core 4P SAS login: -->

    <example _encoding="base64" os.version="24" os.edition="micro" os.build="14896">
      REQtV1JUIHYyNCBtaWNybyAoYykgMjAxMCBOZXdNZWRpYS1ORVQgR21iSA0KUmVsZWFzZTogM
      DgvMDcvMTAgKFNWTiByZXZpc2lvbjogMTQ4OTYpDQoNClByb2xpYW50IERMOTgwUjA3IFg2NT
      UwIDgtY29yZSA0UCBTQVMgbG9naW46Cg==
    </example>
    <param pos="0" name="os.vendor" value="DD-WRT"/>
    <param pos="0" name="os.product" value="DD-WRT"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="os.version.version"/>
    <param pos="3" name="os.edition"/>
    <param pos="4" name="os.build"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:dd-wrt:dd-wrt:{os.version}"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*DD-WRT v(3.\d)-(r([\w]+)) ([\w-]+) \(c\) \d{4} NewMedia-NET GmbH(?:\r|\n)+Release: \d+\/\d+\/\d+(?:\r|\n)+.* login:\s*$">
    <description>DD-WRT - 3.0 family</description>
    <!-- DD-WRT v3.0-r34886M std (c) 2018 NewMedia-NET GmbH\r\nRelease: 02/10/18\r\n\r\nwibrate login: -->

    <example _encoding="base64" os.version="3.0" os.version.version="r34886M" os.edition="std" os.build="34886M">
      REQtV1JUIHYzLjAtcjM0ODg2TSBzdGQgKGMpIDIwMTggTmV3TWVkaWEtTkVUIEdtYkgNClJlb
      GVhc2U6IDAyLzEwLzE4DQoNCndpYnJhdGUgbG9naW46Cg==
    </example>
    <param pos="0" name="os.vendor" value="DD-WRT"/>
    <param pos="0" name="os.product" value="DD-WRT"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="os.version.version"/>
    <param pos="3" name="os.build"/>
    <param pos="4" name="os.edition"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:dd-wrt:dd-wrt:{os.version}"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*DD-WRT v(3.\d)-(r([\w]+)) ([\w-]+) \(c\) \d{4} NewMedia-NET GmbH(?:\r|\n)+Release: \d+\/\d+\/\d+(?:\r|\n)+Board: (\S+) ([^\n\r]+)(?:\r|\n)+.* login:\s*$">
    <description>DD-WRT - 3.0 family - with hardward product</description>
    <!-- DD-WRT v3.0-r40559 std (c) 2019 NewMedia-NET GmbH\r\nRelease: 08/06/19\r\nBoard: Linksys WRT3200ACM\r\n\r\nDD-WRT login: -->

    <example _encoding="base64" os.version="3.0" os.version.version="r40559" os.edition="std" os.build="40559" hw.vendor="Linksys" hw.product="WRT3200ACM">
      REQtV1JUIHYzLjAtcjQwNTU5IHN0ZCAoYykgMjAxOSBOZXdNZWRpYS1ORVQgR21iSA0KUmVsZ
      WFzZTogMDgvMDYvMTkNCkJvYXJkOiBMaW5rc3lzIFdSVDMyMDBBQ00NCg0KREQtV1JUIGxvZ2
      luOgo=
    </example>
    <param pos="0" name="os.vendor" value="DD-WRT"/>
    <param pos="0" name="os.product" value="DD-WRT"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="os.version.version"/>
    <param pos="3" name="os.build"/>
    <param pos="4" name="os.edition"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:dd-wrt:dd-wrt:{os.version}"/>
    <param pos="5" name="hw.vendor"/>
    <param pos="6" name="hw.product"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^(TD-\w+) [\d.]+ DSL Modem Router(?:\r|\n)+Authorization failed after trying \d+ times!!!\.(?:\r|\n)+Please login after \d+ seconds!\s*$">
    <description>TP-LINK TD Family DSL Modem/Router</description>
    <!-- TD-W8960N 5.0 DSL Modem Router\r\nAuthorization failed after trying 5 times!!!.\r\nPlease login after 416 seconds! -->

    <example _encoding="base64" hw.product="TD-W8960N">
      VEQtVzg5NjBOIDUuMCBEU0wgTW9kZW0gUm91dGVyDQpBdXRob3JpemF0aW9uIGZhaWxlZCBhZ
      nRlciB0cnlpbmcgNSB0aW1lcyEhIS4NClBsZWFzZSBsb2dpbiBhZnRlciA0MTYgc2Vjb25kcy
      E=
    </example>
    <param pos="0" name="hw.vendor" value="TP-LINK"/>
    <param pos="1" name="hw.product"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*ZyXEL login:$">
    <description>ZyXEL simple</description>
    <example>ZyXEL login:</example>
    <param pos="0" name="hw.vendor" value="Zyxel"/>
  </fingerprint>

  <fingerprint pattern="^ZyXEL \w?DSL Router\r\nLogin:$">
    <description>ZyXEL Router - simple</description>
    <!-- ZyXEL VDSL Router\r\nLogin: -->

    <example _encoding="base64">WnlYRUwgVkRTTCBSb3V0ZXINCkxvZ2luOgo=</example>
    <param pos="0" name="hw.vendor" value="Zyxel"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^Debian GNU\/Linux 9(?:\r|\n)+([\w.-]+) login:\s*$">
    <description>Debian 9.0 (stretch)</description>
    <!-- Debian GNU/Linux 9\r\nserver-01.2 login: -->

    <example _encoding="base64" host.name="server-01.2">RGViaWFuIEdOVS9MaW51eCA5DQpzZXJ2ZXItMDEuMiBsb2dpbjoK</example>
    <param pos="0" name="os.vendor" value="Debian"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="0" name="os.version" value="9.0"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:debian:debian_linux:9.0"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^Debian GNU\/Linux 8(?:.0)?(?:\r|\n)+([\w.-]+) login:\s*$">
    <description>Debian 8.0 (jessie)</description>
    <!-- Debian GNU/Linux 8\r\nserver-01.2 login: -->

    <example _encoding="base64" host.name="server-01.2">RGViaWFuIEdOVS9MaW51eCA4DQpzZXJ2ZXItMDEuMiBsb2dpbjoK</example>
    <param pos="0" name="os.vendor" value="Debian"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="0" name="os.version" value="8.0"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:debian:debian_linux:8.0"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Debian GNU\/Linux 7(?:.0)?(?:\r|\n)+([\w.-]+) login:\s*$">
    <description>Debian 7.0 (wheezy)</description>
    <!-- Debian GNU/Linux 7\r\nserver-01.2 login: -->

    <example _encoding="base64" host.name="server-01.2">RGViaWFuIEdOVS9MaW51eCA3DQpzZXJ2ZXItMDEuMiBsb2dpbjoK</example>
    <param pos="0" name="os.vendor" value="Debian"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="0" name="os.version" value="7.0"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:debian:debian_linux:7.0"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Debian GNU\/Linux 6(?:.0)?(?:\r|\n)+([\w.-]+) login:\s*$">
    <description>Debian 6.0 (sqeeze)</description>
    <!-- Debian GNU/Linux 6.0\r\nserver-01.2 login: -->

    <example _encoding="base64" host.name="server-01.2">RGViaWFuIEdOVS9MaW51eCA2LjANCnNlcnZlci0wMS4yIGxvZ2luOgo=</example>
    <param pos="0" name="os.vendor" value="Debian"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="0" name="os.version" value="6.0"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:debian:debian_linux:6.0"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Debian GNU\/Linux 5(?:.0)?(?:\r|\n)+([\w.-]+) login:\s*$">
    <description>Debian 5.0 (lenny)</description>
    <!-- Debian GNU/Linux 5.0\r\nserver-01.2 login: -->

    <example _encoding="base64" host.name="server-01.2">RGViaWFuIEdOVS9MaW51eCA1LjANCnNlcnZlci0wMS4yIGxvZ2luOgo=</example>
    <param pos="0" name="os.vendor" value="Debian"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="0" name="os.version" value="5.0"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:debian:debian_linux:5.0"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Debian GNU\/Linux 4(?:.0)?(?:\r|\n)+([\w.-]+) login:\s*$">
    <description>Debian 4.0 (etch)</description>
    <!-- Debian GNU/Linux 4.0\r\nserver-01.2 login: -->

    <example _encoding="base64" host.name="server-01.2">RGViaWFuIEdOVS9MaW51eCA0LjANCnNlcnZlci0wMS4yIGxvZ2luOgo=</example>
    <param pos="0" name="os.vendor" value="Debian"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="0" name="os.version" value="4.0"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:debian:debian_linux:4.0"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Debian GNU\/Linux (3.\d)(?: [\w.-]+)?(?:\r|\n)+([\w.-]+) login:\s*$">
    <description>Debian 3.x (woody/sarge)</description>
    <!-- Debian GNU/Linux 3.1\r\nserver-01.2 login: -->

    <example _encoding="base64" os.version="3.1" host.name="server-01.2">
      RGViaWFuIEdOVS9MaW51eCAzLjENCnNlcnZlci0wMS4yIGxvZ2luOgo=
    </example>
    <param pos="0" name="os.vendor" value="Debian"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:debian:debian_linux:{os.version}"/>
    <param pos="2" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Ubuntu ([\d.]+)(?: LTS)?(?:\r|\n)+([\w.-]+) login:\s*$">
    <description>Ubuntu - most versions</description>
    <!-- Ubuntu 16.04.4 LTS\r\nserver-01.2 login: -->

    <example _encoding="base64" os.version="16.04.4" host.name="server-01.2">
      VWJ1bnR1IDE2LjA0LjQgTFRTDQpzZXJ2ZXItMDEuMiBsb2dpbjoK
    </example>
    <!-- Ubuntu 17.04\r\nnginx login: -->

    <example _encoding="base64" os.version="17.04" host.name="nginx">
      VWJ1bnR1IDE3LjA0DQpuZ2lueCBsb2dpbjoK
    </example>
    <param pos="0" name="os.vendor" value="Ubuntu"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Ubuntu Linux"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:canonical:ubuntu_linux:{os.version}"/>
    <param pos="2" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="(?:\r|\n)*Debian GNU\/Linux (2.\d)(?: [\w.-]+)?(?:\r|\n)+([\w.-]+) login:\s*">
    <description>Debian 2.x (hamm/slink/potato)</description>
    <!-- Debian GNU/Linux 2.2\r\nserver-01.2 login: -->

    <example _encoding="base64" os.version="2.2" host.name="server-01.2">
      RGViaWFuIEdOVS9MaW51eCAyLjINCnNlcnZlci0wMS4yIGxvZ2luOgo=
    </example>
    <!-- Debian GNU/Linux 2.2 localhost.localdomain\r\nmoon login: -->

    <example _encoding="base64" os.version="2.2" host.name="moon">
      RGViaWFuIEdOVS9MaW51eCAyLjIgbG9jYWxob3N0LmxvY2FsZG9tYWluDQptb29uIGxvZ2luOgo=
    </example>
    <param pos="0" name="os.vendor" value="Debian"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:debian:debian_linux:{os.version}"/>
    <param pos="2" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^CentOS release ([\d.]+) \(Final\)(?:\r|\n)+Kernel ([\w.-]+) on an (\w+)(?:\r|\n)+(?:([\w.-]+) )?login:\s*$">
    <description>CentOS</description>
    <!-- CentOS release 5.9 (Final)\r\nKernel 2.6.18-348.6.1.el5 on an i686\r\nlogin: -->

    <example _encoding="base64" os.version="5.9" linux.kernel.version="2.6.18-348.6.1.el5" os.arch="i686">
      Q2VudE9TIHJlbGVhc2UgNS45IChGaW5hbCkNCktlcm5lbCAyLjYuMTgtMzQ4LjYuMS5lbDUgb
      24gYW4gaTY4Ng0KbG9naW46Cg==
    </example>
    <!-- CentOS release 6.10 (Final)\r\nKernel 2.6.32-754.2.1.el6.x86_64 on an x86_64\r\nserver-01.2 login: -->

    <example _encoding="base64" os.version="6.10" linux.kernel.version="2.6.32-754.2.1.el6.x86_64" os.arch="x86_64" host.name="server-01.2">
      Q2VudE9TIHJlbGVhc2UgNi4xMCAoRmluYWwpDQpLZXJuZWwgMi42LjMyLTc1NC4yLjEuZWw2L
      ng4Nl82NCBvbiBhbiB4ODZfNjQNCnNlcnZlci0wMS4yIGxvZ2luOgo=
    </example>
    <param pos="0" name="os.vendor" value="CentOS"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="linux.kernel.version"/>
    <param pos="3" name="os.arch"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:centos:centos:{os.version}"/>
    <param pos="4" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*(RT-AC\d\d\w) login:\s*$">
    <description>Asus Wireless Access Point/Router - RT-AC prefix</description>
    <example hw.product="RT-AC54U">RT-AC54U login:</example>
    <example hw.product="RT-AC68R">RT-AC68R login:</example>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="0" name="hw.vendor" value="Asus"/>
    <param pos="0" name="hw.device" value="WAP"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*(AC\d\d00) login:\s*$">
    <description>Asus Wireless Access Point/Router - AC prefix</description>
    <example hw.product="AC1000">AC1000 login:</example>
    <example hw.product="AC3000">AC3000 login:</example>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="0" name="hw.vendor" value="Asus"/>
    <param pos="0" name="hw.device" value="WAP"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*(Air5\d+\w{0,2}) login:\s*$">
    <description>Airties</description>
    <example hw.product="Air5650">Air5650 login:</example>
    <example hw.product="Air5650TT">Air5650TT login:</example>
    <param pos="0" name="hw.vendor" value="Airties"/>
    <param pos="0" name="hw.device" value="WAP"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^Amazon Linux AMI release ([\d.]+)(?:\r|\n)+Kernel ([\w.-]+) on an (\w+)(?:\r|\n)+(?:([\w.-]+) )?login:\s*$">
    <description>Amazon Linux AMI</description>
    <!-- Amazon Linux AMI release 2013.09\r\nKernel 3.4.68-59.97.amzn1.x86_64 on an x86_64\r\nserver-01.2 login: -->

    <example _encoding="base64" os.version="2013.09" linux.kernel.version="3.4.68-59.97.amzn1.x86_64" os.arch="x86_64" host.name="server-01.2">
      QW1hem9uIExpbnV4IEFNSSByZWxlYXNlIDIwMTMuMDkNCktlcm5lbCAzLjQuNjgtNTkuOTcuY
      W16bjEueDg2XzY0IG9uIGFuIHg4Nl82NA0Kc2VydmVyLTAxLjIgbG9naW46Cg==
    </example>
    <param pos="0" name="os.vendor" value="Amazon"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="linux.kernel.version"/>
    <param pos="3" name="os.arch"/>
    <param pos="4" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?m)TiMOS-[CB]-([\S]+) (?:both|cpm)/([\w]+) ALCATEL (SR [\S]+) Copyright.*Login:\s*$" flags="REG_MULTILINE">
    <description>ALCATEL Service Router running TiMOS</description>
    <!-- TiMOS-C-12.0.R12 cpm/hops64 ALCATEL SR 7750 Copyright (c) 2000-2015 Alcatel-Lucent.\r\r\nBanner Shortened For \r\r\nBrevity\r\nLogin: -->

    <example _encoding="base64" os.version="12.0.R12" hw.product="SR 7750" os.arch="hops64">
      VGlNT1MtQy0xMi4wLlIxMiBjcG0vaG9wczY0IEFMQ0FURUwgU1IgNzc1MCBDb3B5cmlnaHQgK
      GMpIDIwMDAtMjAxNSBBbGNhdGVsLUx1Y2VudC4NDQpCYW5uZXIgU2hvcnRlbmVkIEZvciANDQ
      pCcmV2aXR5DQpMb2dpbjoK
    </example>
    <param pos="0" name="os.vendor" value="ALCATEL"/>
    <param pos="0" name="os.product" value="TimOS"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="os.arch"/>
    <param pos="0" name="hw.vendor" value="ALCATEL"/>
    <param pos="0" name="hw.family" value="Service Router"/>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="3" name="hw.product"/>
  </fingerprint>

  <!-- Nokia purchased Alcatel Lucent, finalized in Nov 2016 -->

  <fingerprint pattern="^(?m)TiMOS-[CB]-([\S]+) (?:both|cpm)\/([\w]+) Nokia ([\S]+ [SRX]+) Copyright.*Login:\s*$" flags="REG_MULTILINE">
    <description>Nokia Service Router running TiMOS</description>
    <!-- TiMOS-C-14.0.R5 cpm/hops64 Nokia 7750 SR Copyright (c) 2000-2016 Nokia.\r\r\nBanner Shortened For \r\r\nBrevity\r\nLogin: -->

    <example _encoding="base64" os.version="14.0.R5" os.arch="hops64" hw.product="7750 SR">
      VGlNT1MtQy0xNC4wLlI1IGNwbS9ob3BzNjQgTm9raWEgNzc1MCBTUiBDb3B5cmlnaHQgKGMpI
      DIwMDAtMjAxNiBOb2tpYS4NDQpCYW5uZXIgU2hvcnRlbmVkIEZvciANDQpCcmV2aXR5DQpMb2
      dpbjoK
    </example>
    <!-- TiMOS-C-14.0.R10 cpm/hops64 Nokia 7950 XRS Copyright (c) 2000-2017 Nokia.\r\r\nBanner Shortened For \r\r\nBrevity\r\nLogin: -->

    <example _encoding="base64" os.version="14.0.R10" os.arch="hops64" hw.product="7950 XRS">
      VGlNT1MtQy0xNC4wLlIxMCBjcG0vaG9wczY0IE5va2lhIDc5NTAgWFJTIENvcHlyaWdodCAoY
      ykgMjAwMC0yMDE3IE5va2lhLg0NCkJhbm5lciBTaG9ydGVuZWQgRm9yIA0NCkJyZXZpdHkNCk
      xvZ2luOgo=
    </example>
    <param pos="0" name="os.vendor" value="Nokia"/>
    <param pos="0" name="os.product" value="TimOS"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="os.arch"/>
    <param pos="0" name="hw.vendor" value="Nokia"/>
    <param pos="0" name="hw.family" value="Service Router"/>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="3" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?m)TiMOS-[CB]-([\S]+) (?:both|cpm)\/([\w]+) Nokia (SAS[+\w\s-]+) Copyright.*Login:\s*$" flags="REG_MULTILINE">
    <description>Nokia Service Access Switch running TiMOS</description>
    <!-- TiMOS-B-8.0.R12 both/hops Nokia SAS-Mxp 22F2C 4SFP+ 7210 Copyright (c) 2000-2017 Nokia.\r\r\nBanner Shortened For \r\r\nBrevity\r\nLogin: -->

    <example _encoding="base64" os.version="8.0.R12" os.arch="hops" hw.product="SAS-Mxp 22F2C 4SFP+ 7210">
      VGlNT1MtQi04LjAuUjEyIGJvdGgvaG9wcyBOb2tpYSBTQVMtTXhwIDIyRjJDIDRTRlArIDcyM
      TAgQ29weXJpZ2h0IChjKSAyMDAwLTIwMTcgTm9raWEuDQ0KQmFubmVyIFNob3J0ZW5lZCBGb3
      IgDQ0KQnJldml0eQ0KTG9naW46Cg==
    </example>
    <!-- TiMOS-B-9.0.R9 both/mpc Nokia SAS-M 24F 2XFP 7210 Copyright (c) 2000-2017 Nokia.\r\r\nBanner Shortened For \r\r\nBrevity\r\nLogin: -->

    <example _encoding="base64" os.version="9.0.R9" os.arch="mpc" hw.product="SAS-M 24F 2XFP 7210">
      VGlNT1MtQi05LjAuUjkgYm90aC9tcGMgTm9raWEgU0FTLU0gMjRGIDJYRlAgNzIxMCBDb3B5c
      mlnaHQgKGMpIDIwMDAtMjAxNyBOb2tpYS4NDQpCYW5uZXIgU2hvcnRlbmVkIEZvciANDQpCcm
      V2aXR5DQpMb2dpbjoK
    </example>
    <param pos="0" name="os.vendor" value="Nokia"/>
    <param pos="0" name="os.product" value="TimOS"/>
    <param pos="0" name="os.device" value="Switch"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="os.arch"/>
    <param pos="0" name="hw.vendor" value="Nokia"/>
    <param pos="0" name="hw.family" value="Service Access Switch"/>
    <param pos="0" name="hw.device" value="Switch"/>
    <param pos="3" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Grandstream (HT[\d-]+)\s+(?:V\d\.\d\w?\s+)?Command Shell Copyright \d\d\d\d-\d\d\d\d(?:\r|\n)+Password:\s*$">
    <description>Grandstream HandyTone Analog Telephone Adapters</description>
    <!-- Grandstream HT812 Command Shell Copyright 2006-2017\r\nPassword: -->

    <example _encoding="base64" hw.product="HT812">
      R3JhbmRzdHJlYW0gSFQ4MTIgQ29tbWFuZCBTaGVsbCBDb3B5cmlnaHQgMjAwNi0yMDE3DQpQY
      XNzd29yZDoK
    </example>
    <!-- Grandstream HT-502  V2.0A Command Shell Copyright 2006-2014\r\nPassword: -->

    <example _encoding="base64" hw.product="HT-502">
      R3JhbmRzdHJlYW0gSFQtNTAyICBWMi4wQSBDb21tYW5kIFNoZWxsIENvcHlyaWdodCAyMDA2L
      TIwMTQNClBhc3N3b3JkOgo=
    </example>
    <param pos="0" name="hw.vendor" value="Grandstream"/>
    <param pos="0" name="hw.family" value="HandyTone"/>
    <param pos="0" name="hw.device" value="VoIP"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Grandstream (GXW[\d-]+)\s+(?:V\d\.\d\w?\s+)?Command Shell Copyright \d\d\d\d(?:-\d\d\d\d)?(?:\r|\n)+Password:\s*$">
    <description>Grandstream Analog VoIP Gateways</description>
    <!-- Grandstream GXW-4008  V1.5A Command Shell Copyright 2006-2015\r\nPassword: -->

    <example _encoding="base64" hw.product="GXW-4008">
      R3JhbmRzdHJlYW0gR1hXLTQwMDggIFYxLjVBIENvbW1hbmQgU2hlbGwgQ29weXJpZ2h0IDIwM
      DYtMjAxNQ0KUGFzc3dvcmQ6Cg==
    </example>
    <!-- Grandstream GXW4216  V2.3B Command Shell Copyright 2015\r\nPassword: -->

    <example _encoding="base64" hw.product="GXW4216">
      R3JhbmRzdHJlYW0gR1hXNDIxNiAgVjIuM0IgQ29tbWFuZCBTaGVsbCBDb3B5cmlnaHQgMjAxN
      Q0KUGFzc3dvcmQ6Cg==
    </example>
    <param pos="0" name="hw.vendor" value="Grandstream"/>
    <param pos="0" name="hw.family" value="GXW"/>
    <param pos="0" name="hw.device" value="VoIP"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n|\s)*Grandstream (GXV[\w-]+)\s+(?:V\d\.\d\w?\s+)?Shell Command.Copyight \d\d\d\d-\d\d\d\d(?:\r|\n)+Username:\s*$">
    <description>Grandstream IP Cameras</description>
    <!-- Grandstream GXV3674_FHD_VF    Shell Command.Copyight 2011-2014\r\nUsername: -->

    <example _encoding="base64" hw.product="GXV3674_FHD_VF">
      R3JhbmRzdHJlYW0gR1hWMzY3NF9GSERfVkYgICAgU2hlbGwgQ29tbWFuZC5Db3B5aWdodCAyM
      DExLTIwMTQNClVzZXJuYW1lOgo=
    </example>
    <param pos="0" name="hw.vendor" value="Grandstream"/>
    <param pos="0" name="hw.family" value="GXV"/>
    <param pos="0" name="hw.device" value="IP Camera"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Welcome to Polycom RMX\s*(\w+) \(COP\) Console Utility(?:\r|\n)+Copyright \(C\) \d\d\d\d-\d\d\d\d POLYCOM(?:\r|\n)+Password:\s*$">
    <description>Polycom Real Time Media Conferencing</description>
    <!-- Welcome to Polycom RMX 500 (COP) Console Utility\r\n\rCopyright (C) 2008-2010 POLYCOM\r\n\r\r\n\rPassword: -->

    <example _encoding="base64" hw.product="500">
      V2VsY29tZSB0byBQb2x5Y29tIFJNWCA1MDAgKENPUCkgQ29uc29sZSBVdGlsaXR5DQoNQ29we
      XJpZ2h0IChDKSAyMDA4LTIwMTAgUE9MWUNPTQ0KDQ0KDVBhc3N3b3JkOgo=
    </example>
    <!-- Welcome to Polycom RMX 1000C (COP) Console Utility\r\n\rCopyright (C) 2008-2012 POLYCOM\r\n\r\r\n\rPassword: -->

    <example _encoding="base64" hw.product="1000C">
      V2VsY29tZSB0byBQb2x5Y29tIFJNWCAxMDAwQyAoQ09QKSBDb25zb2xlIFV0aWxpdHkNCg1Db
      3B5cmlnaHQgKEMpIDIwMDgtMjAxMiBQT0xZQ09NDQoNDQoNUGFzc3dvcmQ6Cg==
    </example>
    <param pos="0" name="hw.vendor" value="Polycom"/>
    <param pos="0" name="hw.family" value="RMX"/>
    <param pos="0" name="hw.device" value="Video Conferencing"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Hi, my name is :\s+[\w.\s-]+(?:\r|\n)+Here is what I know about myself:(?:\r|\n)+Model:\s+VSX (\w+)(?:\r|\n)+Serial Number:\s+(\w+)(?:\r|\n)+Software Version:\s+Release ([\d.-]+)\s">
    <description>Polycom Video Conferencing - VSX Family</description>
    <!-- Hi, my name is :     Something Pity\r\nHere is what I know about myself:\r\nModel:               VSX 6000A\r\nSerial Number:       00070906FC34F6\r\nSoftware Version:    Release 9.0.6.2-103 - 04Sep2011 21:27\r\nBuild Information:   ecomman -->

    <example _encoding="base64" hw.product="6000A" host.id="00070906FC34F6" os.version="9.0.6.2-103">
      SGksIG15IG5hbWUgaXMgOiAgICAgU29tZXRoaW5nIFBpdHkNCkhlcmUgaXMgd2hhdCBJIGtub
      3cgYWJvdXQgbXlzZWxmOg0KTW9kZWw6ICAgICAgICAgICAgICAgVlNYIDYwMDBBDQpTZXJpYW
      wgTnVtYmVyOiAgICAgICAwMDA3MDkwNkZDMzRGNg0KU29mdHdhcmUgVmVyc2lvbjogICAgUmV
      sZWFzZSA5LjAuNi4yLTEwMyAtIDA0U2VwMjAxMSAyMToyNw0KQnVpbGQgSW5mb3JtYXRpb246
      ICAgZWNvbW1hbgo=
    </example>
    <param pos="0" name="hw.vendor" value="Polycom"/>
    <param pos="0" name="hw.family" value="VSX"/>
    <param pos="0" name="hw.device" value="Video Conferencing"/>
    <param pos="1" name="hw.product"/>
    <param pos="2" name="host.id"/>
    <param pos="3" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="Polycom Command Shell(?:\r|\n)+XCOM host:\s+localhost port: \d+">
    <description>Polycom Diagnotic Service</description>
    <!-- Polycom Command Shell\r\r\nXCOM host:    localhost port: 4121\r\r\nTTY name:     /dev/pts/0\r\r\nSession type: telnet\r\r\nNCF\r\nNCF\r\n2018-08-15 18:03:10 DEBUG -->

    <example _encoding="base64">
      UG9seWNvbSBDb21tYW5kIFNoZWxsDQ0KWENPTSBob3N0OiAgICBsb2NhbGhvc3QgcG9ydDogN
      DEyMQ0NClRUWSBuYW1lOiAgICAgL2Rldi9wdHMvMA0NClNlc3Npb24gdHlwZTogdGVsbmV0DQ
      0KTkNGDQpOQ0YNCjIwMTgtMDgtMTUgMTg6MDM6MTAgREVCVUcK
    </example>
    <param pos="0" name="hw.vendor" value="Polycom"/>
    <param pos="0" name="hw.device" value="Video Conferencing"/>
  </fingerprint>

  <fingerprint pattern="^Welcome to the Windows CE Telnet Service on (WEBBOX[\w.-]+)(?:\r|\n)+login:\s*$">
    <description>Sunny WebBox Windows CE</description>
    <!-- Welcome to the Windows CE Telnet Service on WEBBOX150000000\r\n\r\nlogin: -->

    <example _encoding="base64" host.name="WEBBOX150000000">
      V2VsY29tZSB0byB0aGUgV2luZG93cyBDRSBUZWxuZXQgU2VydmljZSBvbiBXRUJCT1gxNTAwM
      DAwMDANCg0KbG9naW46Cg==
    </example>
    <param pos="0" name="hw.vendor" value="SMA Solar Technology Ag"/>
    <param pos="0" name="hw.family" value="Sunny"/>
    <param pos="0" name="hw.product" value="WebBox"/>
    <param pos="0" name="hw.device" value="Power Device"/>
    <param pos="0" name="os.vendor" value="Microsoft"/>
    <param pos="0" name="os.family" value="Windows"/>
    <param pos="0" name="os.product" value="Windows CE"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:microsoft:windows_ce:-"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^Welcome to the Windows CE Telnet Service on ([\w.-]+)(?:\r|\n)+login:\s*$">
    <description>Windows CE</description>
    <!-- Welcome to the Windows CE Telnet Service on MY-CE-DEVICE\r\n\r\nlogin: -->

    <example _encoding="base64" host.name="MY-CE-DEVICE">
      V2VsY29tZSB0byB0aGUgV2luZG93cyBDRSBUZWxuZXQgU2VydmljZSBvbiBNWS1DRS1ERVZJQ
      0UNCg0KbG9naW46Cg==
    </example>
    <param pos="0" name="os.vendor" value="Microsoft"/>
    <param pos="0" name="os.family" value="Windows"/>
    <param pos="0" name="os.product" value="Windows CE"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:microsoft:windows_ce:-"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*HP JetDirect(?:\r|\n)+$">
    <description>HP Printer - Jet Direct</description>
    <!-- HP JetDirect\r\nPassword is not set\r\n\r\nPlease type "menu" for the MENU system, \r\nor "?" for help, or "/" for current settings.\r\n> -->

    <example _encoding="base64">
      SFAgSmV0RGlyZWN0DQpQYXNzd29yZCBpcyBub3Qgc2V0DQoNClBsZWFzZSB0eXBlICJtZW51I
      iBmb3IgdGhlIE1FTlUgc3lzdGVtLCANCm9yICI/IiBmb3IgaGVscCwgb3IgIi8iIGZvciBjdX
      JyZW50IHNldHRpbmdzLg0KPgo=
    </example>
    <!-- HP JetDirect\r\n\r\nEnter username: -->

    <example _encoding="base64">SFAgSmV0RGlyZWN0DQoNCkVudGVyIHVzZXJuYW1lOgo=</example>
    <param pos="0" name="service.vendor" value="HP"/>
    <param pos="0" name="service.product" value="JetDirect"/>
    <param pos="0" name="service.family" value="JetDirect"/>
    <param pos="0" name="os.vendor" value="HP"/>
    <param pos="0" name="os.device" value="Printer"/>
    <param pos="0" name="os.family" value="JetDirect"/>
    <param pos="0" name="os.product" value="JetDirect"/>
    <param pos="0" name="hw.vendor" value="HP"/>
    <param pos="0" name="hw.family" value="JetDirect"/>
    <param pos="0" name="hw.product" value="JetDirect"/>
    <param pos="0" name="hw.device" value="Printer"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*%connection closed by remote host!(?:\x00)?$">
    <description>HP switch blocking connection using network ACL</description>
    <!-- %connection closed by remote host! -->

    <example _encoding="base64">JWNvbm5lY3Rpb24gY2xvc2VkIGJ5IHJlbW90ZSBob3N0IQ==</example>
    <param pos="0" name="hw.vendor" value="HP"/>
    <param pos="0" name="hw.device" value="Switch"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Welcome Visiting Huawei Home Gateway\r\nCopyright by Huawei Technologies Co., Ltd.\r\n\r\nLogin:$">
    <description>Huawei HG series Home Gateway routers</description>
    <!-- Welcome Visiting Huawei Home Gateway\r\nCopyright by Huawei Technologies Co., Ltd.\r\n\r\nLogin: -->

    <example _encoding="base64">
      V2VsY29tZSBWaXNpdGluZyBIdWF3ZWkgSG9tZSBHYXRld2F5DQpDb3B5cmlnaHQgYnkgSHVhd
      2VpIFRlY2hub2xvZ2llcyBDby4sIEx0ZC4NCg0KTG9naW46Cg==
    </example>
    <param pos="0" name="hw.vendor" value="Huawei"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Warning: Telnet is not a secure protocol, and it is recommended to use Stelnet.(?:(?:\r|\n)+Login authentication)?(?:\r|\n)+Username:$">
    <description>Huawei Router</description>
    <!-- Warning: Telnet is not a secure protocol, and it is recommended to use Stelnet.\r\n\r\nLogin authentication\r\n\r\n\r\nUsername: -->

    <example _encoding="base64">
      V2FybmluZzogVGVsbmV0IGlzIG5vdCBhIHNlY3VyZSBwcm90b2NvbCwgYW5kIGl0IGlzIHJlY
      29tbWVuZGVkIHRvIHVzZSBTdGVsbmV0Lg0KDQpMb2dpbiBhdXRoZW50aWNhdGlvbg0KDQoNCl
      VzZXJuYW1lOgo=
    </example>
    <param pos="0" name="hw.vendor" value="Huawei"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*(?:% Password expiration warning.\r\n)?-+\r\nCisco Configuration Professional \(Cisco CP\) is installed on this device. \r\nThis feature requires the one-time use of the username">
    <description>Cisco router - Cisco Configuration Pro  variant</description>

    <!-- \r\nCisco Configuration Professional (Cisco CP) is installed on this device. \r\nThis feature requires the one-time use of the username -->

    <example _encoding="base64">
      LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tL
      S0tLS0tLS0tLS0tLS0tLS0NCkNpc2NvIENvbmZpZ3VyYXRpb24gUHJvZmVzc2lvbmFsIChDaX
      NjbyBDUCkgaXMgaW5zdGFsbGVkIG9uIHRoaXMgZGV2aWNlLiANClRoaXMgZmVhdHVyZSByZXF
      1aXJlcyB0aGUgb25lLXRpbWUgdXNlIG9mIHRoZSB1c2VybmFtZQo=
    </example>
    <param pos="0" name="service.vendor" value="Cisco"/>
    <param pos="0" name="os.vendor" value="Cisco"/>
    <param pos="0" name="os.family" value="IOS"/>
    <param pos="0" name="os.product" value="IOS"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:cisco:ios:-"/>
    <param pos="0" name="hw.vendor" value="Cisco"/>
    <param pos="0" name="hw.device" value="Router"/>
  </fingerprint>

  <fingerprint pattern="^(?m)(?:\r|\n)*Catalyst 1900 Management Console(?:\r|\n)+.*Ethernet Address:\s+([\w-]+)(?:\r|\n)+.*Model Number:\s+([\w-]+)(?:\r|\n)+System Serial Number:\s+(\w+)(?:\r|\n)+Power Supply" flags="REG_MULTILINE">
    <description>Cisco Catalyst 1900</description>
    <!-- Catalyst 1900, unlike other Catalyst models, didn't run CatOS or IOS -->

    <!-- Catalyst 1900 Management Console\r\nCopyright (c) Cisco Systems, Inc.  1993-1998\r\nAll rights reserved.\r\nEnterprise Edition Software\r\nEthernet Address:      00-AA-19-38-AA-00\r\n\r\nPCA Number:            73-31AA-AA\r\nPCA Serial Number:     FAB033AAAAA\r\nModel Number:          WS-C1924-EN\r\nSystem Serial Number:  FAB0341AAAA\r\nPower Supply S/N:    -->

    <example _encoding="base64" host.mac="00-AA-19-38-AA-00" hw.model="WS-C1924-EN" host.id="FAB0341AAAA">
      Q2F0YWx5c3QgMTkwMCBNYW5hZ2VtZW50IENvbnNvbGUNCkNvcHlyaWdodCAoYykgQ2lzY28gU
      3lzdGVtcywgSW5jLiAgMTk5My0xOTk4DQpBbGwgcmlnaHRzIHJlc2VydmVkLg0KRW50ZXJwcm
      lzZSBFZGl0aW9uIFNvZnR3YXJlDQpFdGhlcm5ldCBBZGRyZXNzOiAgICAgIDAwLUFBLTE5LTM
      4LUFBLTAwDQoNClBDQSBOdW1iZXI6ICAgICAgICAgICAgNzMtMzFBQS1BQQ0KUENBIFNlcmlh
      bCBOdW1iZXI6ICAgICBGQUIwMzNBQUFBQQ0KTW9kZWwgTnVtYmVyOiAgICAgICAgICBXUy1DM
      TkyNC1FTg0KU3lzdGVtIFNlcmlhbCBOdW1iZXI6ICBGQUIwMzQxQUFBQQ0KUG93ZXIgU3VwcG
      x5IFMvTjogICAK
    </example>
    <param pos="0" name="service.vendor" value="Cisco"/>
    <param pos="0" name="os.vendor" value="Cisco"/>
    <param pos="0" name="os.device" value="Switch"/>
    <param pos="0" name="hw.vendor" value="Cisco"/>
    <param pos="0" name="hw.product" value="Catalyst 1900"/>
    <param pos="0" name="hw.device" value="Switch"/>
    <param pos="1" name="host.mac"/>
    <param pos="2" name="hw.model"/>
    <param pos="3" name="host.id"/>
  </fingerprint>

  <fingerprint pattern="^192.0.0.64 login:\s*$">
    <description>Hikvision cameras and NVRs (multiple)</description>
    <example>192.0.0.64 login:</example>
    <param pos="0" name="os.vendor" value="Hikvision"/>
    <param pos="0" name="hw.vendor" value="Hikvision"/>
  </fingerprint>

  <fingerprint pattern="^Remote Management Console\r\nlogin:\s*$">
    <description>Juniper Netscreen</description>
    <!-- Remote Management Console\r\nlogin: -->

    <example _encoding="base64">UmVtb3RlIE1hbmFnZW1lbnQgQ29uc29sZQ0KbG9naW46Cg==</example>
    <param pos="0" name="os.vendor" value="Juniper"/>
    <param pos="0" name="os.device" value="Firewall"/>
    <param pos="0" name="os.family" value="ScreenOS"/>
    <param pos="0" name="os.product" value="ScreenOS"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:juniper:screenos:-"/>
    <param pos="0" name="hw.vendor" value="Juniper"/>
    <param pos="0" name="hw.device" value="Firewall"/>
    <param pos="0" name="hw.product" value="NetScreen"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*(FGT\w{13}) login:\s*$">
    <description>Fortinet FortiGate - w/ autogenerated hostname</description>
    <example host.name="FGT60C3G13001111">FGT60C3G13001111 login:</example>
    <param pos="0" name="os.vendor" value="Fortinet"/>
    <param pos="0" name="os.family" value="FortiOS"/>
    <param pos="0" name="os.product" value="FortiOS"/>
    <param pos="0" name="os.device" value="Firewall"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:fortinet:fortios:-"/>
    <param pos="0" name="hw.vendor" value="Fortinet"/>
    <param pos="0" name="hw.family" value="FortiGate"/>
    <param pos="0" name="hw.device" value="Firewall"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*KWS-1043N login:\s*$">
    <description>Clipcomm KWS router</description>
    <example hw.product="KWS-1043N">KWS-1043N login:</example>
    <param pos="0" name="hw.vendor" value="Clipcomm"/>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="0" name="hw.product" value="KWS-1043N"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*(SMCD3\w+-\w\w\w) login:\s*$">
    <description>SMC Cable Modem</description>
    <example hw.product="SMCD3GN2-BIZ">SMCD3GN2-BIZ login:</example>
    <param pos="0" name="hw.vendor" value="SMC Networks"/>
    <param pos="0" name="hw.device" value="Cable Modem"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*ADB-4820CD login:\s*$">
    <description>ADB ADB-4820CD DVR</description>
    <example>ADB-4820CD login:</example>
    <param pos="0" name="hw.vendor" value="ADB"/>
    <param pos="0" name="hw.device" value="DVR"/>
    <param pos="0" name="hw.product" value="ADB-4820CD"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*IMDVRS login:\s*$">
    <description>Rifatron IMDVRS DVR</description>
    <example>IMDVRS login:</example>
    <param pos="0" name="hw.vendor" value="Rifatron"/>
    <param pos="0" name="hw.family" value="IMDVR"/>
    <param pos="0" name="hw.device" value="DVR"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n)*Ruijie login:\s*$">
    <description>Ruijie device (likely router/switch)</description>
    <example>Ruijie login:</example>
    <param pos="0" name="hw.vendor" value="Ruijie"/>
  </fingerprint>

  <fingerprint pattern="^Welcome to Microsoft Telnet Service \r\n\n\rlogin:\s*$">
    <description>Microsoft Windows</description>
    <!-- Welcome to Microsoft Telnet Service \r\n\n\rlogin: -->

    <example _encoding="base64">V2VsY29tZSB0byBNaWNyb3NvZnQgVGVsbmV0IFNlcnZpY2UgDQoKDWxvZ2luOgo=</example>
    <param pos="0" name="os.vendor" value="Microsoft"/>
    <param pos="0" name="os.family" value="Windows"/>
    <param pos="0" name="os.product" value="Windows"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:microsoft:windows:-"/>
  </fingerprint>

  <!-- The following fingerprints are for generic Broadcom hardware where the
       vendor has left the default banner in place. These could be rebadged by
       ZTE, CenturyLink, Sky, Huawei, etc.
  -->

  <fingerprint pattern="^(BCM\d+) (?:Broadband|ADSL|xDSL|DSL) Router\r\nLogin:\s*">
    <description>OEM'd Broadcom Router</description>
    <!-- BCM963268 Broadband Router\r\nLogin: -->

    <example _encoding="base64" hw.product="BCM963268">QkNNOTYzMjY4IEJyb2FkYmFuZCBSb3V0ZXINCkxvZ2luOgo=</example>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(BCM\d+) Broadband Router\r\nTelnet is Disabled in WAN Side$">
    <description>OEM'd Broadcom Router - telnet disabled on WAN side</description>
    <!-- BCM963268 Broadband Router\r\nTelnet is Disabled in WAN Side -->

    <example _encoding="base64" hw.product="BCM963268">QkNNOTYzMjY4IEJyb2FkYmFuZCBSb3V0ZXINClRlbG5ldCBpcyBEaXNhYmxlZCBpbiBXQU4gU2lkZQo=</example>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(?m)(BCM\d+) Broadband Router\r\n.*Please input the verification code:$" flags="REG_MULTILINE">
    <description>OEM'd Broadcom Router - input validation code</description>
    <!-- BCM96318 Broadband Router\r\n====================================================\r\n    * *         * * * *      * * * *      * * * *   \r\n      *         *                  *      *     *   \r\n      *         * * * *      * * * *      * * * *   \r\n      *         *     *            *            *   \r\n      *         *     *            *            *   \r\n   * * * *      * * * *      * * * *      * * * *   \r\n====================================================\r\nPlease input the verification code: -->

    <example _encoding="base64" hw.product="BCM96318">
      QkNNOTYzMTggQnJvYWRiYW5kIFJvdXRlcg0KPT09PT09PT09PT09PT09PT09PT09PT09PT09P
      T09PT09PT09PT09PT09PT09PT09PT09PQ0KICAgICogKiAgICAgICAgICogKiAqICogICAgIC
      AqICogKiAqICAgICAgKiAqICogKiAgIA0KICAgICAgKiAgICAgICAgICogICAgICAgICAgICA
      gICAgICAqICAgICAgKiAgICAgKiAgIA0KICAgICAgKiAgICAgICAgICogKiAqICogICAgICAq
      ICogKiAqICAgICAgKiAqICogKiAgIA0KICAgICAgKiAgICAgICAgICogICAgICogICAgICAgI
      CAgICAqICAgICAgICAgICAgKiAgIA0KICAgICAgKiAgICAgICAgICogICAgICogICAgICAgIC
      AgICAqICAgICAgICAgICAgKiAgIA0KICAgKiAqICogKiAgICAgICogKiAqICogICAgICAqICo
      gKiAqICAgICAgKiAqICogKiAgIA0KPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09
      PT09PT09PT09PT09PT09PT09PQ0KUGxlYXNlIGlucHV0IHRoZSB2ZXJpZmljYXRpb24gY29kZ
      ToK
    </example>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(BCM\d+) Broadband Router\r\nMaximum number of incorrect account entries exceeded.">
    <description>OEM'd Broadcom Router - Max incorrect tries - variant 1</description>
    <!-- BCM96328 Broadband Router\r\nMaximum number of incorrect account entries exceeded. -->

    <example _encoding="base64" hw.product="BCM96328">
      QkNNOTYzMjggQnJvYWRiYW5kIFJvdXRlcg0KTWF4aW11bSBudW1iZXIgb2YgaW5jb3JyZWN0I
      GFjY291bnQgZW50cmllcyBleGNlZWRlZC4K
    </example>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^(BCM\d+) Broadband Router\r\nSorry, you need to wait for \d+ second before next login attempt.(?:\r|\n)*">
    <description>OEM'd Broadcom Router - Max incorrect tries - variant 2</description>
    <!-- BCM96816 Broadband Router\r\nSorry, you need to wait for 119 second before next login attempt. -->

    <example _encoding="base64" hw.product="BCM96816">
      QkNNOTY4MTYgQnJvYWRiYW5kIFJvdXRlcg0KU29ycnksIHlvdSBuZWVkIHRvIHdhaXQgZm9yI
      DExOSBzZWNvbmQgYmVmb3JlIG5leHQgbG9naW4gYXR0ZW1wdC4K
    </example>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <!-- Moxa Industrial Solutions-->

  <fingerprint pattern="^(?:\r|\n)*NPort (NP6[\w-]+)(?:\r|\n|\x00)+Console terminal type">
    <description>Moxa NPort Terminal Server - 6xxx Series</description>
    <!-- NPort NP6610-32\r\u0000\nConsole terminal type (1: ansi/vt100, 2: vt52) : 1 -->

    <example _encoding="base64" hw.product="NP6610-32">
     TlBvcnQgTlA2NjEwLTMyDQAKQ29uc29sZSB0ZXJtaW5hbCB0eXBlICgxOiBhbnNpL3Z0MTAwLC
     AyOiB2dDUyKSA6IDE=
    </example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="NPort"/>
    <param pos="0" name="hw.device" value="Device Server"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^Model name\s+: NPort (IA-\d+)(?:\r|\n|\x00)+MAC address\s+: ([\w:]+)(?:\r|\n|\x00)+Serial No.\s+: (\d+)(?:\r|\n|\x00)+Firmware version : ([\d.]+) Build (\d+)(?:\r|\n|\x00)+System uptime">
    <description>Moxa NPort Device Server - IA Series</description>
    <!-- Model name       : NPort IA-5250\r\u0000\nMAC address      : 00:90:E8:AA:AA:AA\r\u0000\nSerial No.       : 281\r\u0000\nFirmware version : 1.6 Build 17060616\r\u0000\nSystem uptime    : 31 days, 06h:03m:45s\r\u0000\n\r\u0000\nPlease keyin your password: -->

    <example _encoding="base64" hw.product="IA-5250" host.mac="00:90:E8:AA:AA:AA" host.id="281" os.version="1.6" os.version.version="17060616">
      TW9kZWwgbmFtZSAgICAgICA6IE5Qb3J0IElBLTUyNTANAApNQUMgYWRkcmVzcyAgICAgIDogM
      DA6OTA6RTg6QUE6QUE6QUENAApTZXJpYWwgTm8uICAgICAgIDogMjgxDQAKRmlybXdhcmUgdm
      Vyc2lvbiA6IDEuNiBCdWlsZCAxNzA2MDYxNg0AClN5c3RlbSB1cHRpbWUgICAgOiAzMSBkYXl
      zLCAwNmg6MDNtOjQ1cw0ACg0AClBsZWFzZSBrZXlpbiB5b3VyIHBhc3N3b3JkOg==
    </example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="NPort"/>
    <param pos="0" name="hw.device" value="Device Server"/>
    <param pos="1" name="hw.product"/>
    <param pos="2" name="host.mac"/>
    <param pos="3" name="host.id"/>
    <param pos="0" name="os.vendor" value="Moxa"/>
    <param pos="4" name="os.version"/>
    <param pos="5" name="os.version.version"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n|\x00|-)*Model name\s+: NPort (5[\w-]+)(?:\r|\n|\x00)+MAC address\s+: ([\w:]+)(?:\r|\n|\x00)+Serial No.\s+: (\d+)(?:\r|\n|\x00)+Firmware version : ([\d.]+) Build (\d+)(?:\r|\n|\x00)+">
    <description>Moxa NPort Device Server - 5xxx Series</description>
    <!-- Some versions of the banner below have a line full of dashes which cannot be included in the example comment -->

    <!-- Model name       : NPort 5610-8-DT\r\u0000\nMAC address      : 00:90:E8:AA:AA:AA\r\u0000\nSerial No.       : 9522\r\u0000\nFirmware version : 2.2 Build 11090613\r\u0000\nSystem uptime    : 8 days, 02h:11m:44s\r\u0000\n\r\u0000\nPlease keyin your password: -->

    <example _encoding="base64" hw.product="5610-8-DT" host.mac="00:90:E8:AA:AA:AA" host.id="9522" os.version="2.2" os.version.version="11090613">
      TW9kZWwgbmFtZSAgICAgICA6IE5Qb3J0IDU2MTAtOC1EVA0ACk1BQyBhZGRyZXNzICAgICAgO
      iAwMDo5MDpFODpBQTpBQTpBQQ0AClNlcmlhbCBOby4gICAgICAgOiA5NTIyDQAKRmlybXdhcm
      UgdmVyc2lvbiA6IDIuMiBCdWlsZCAxMTA5MDYxMw0AClN5c3RlbSB1cHRpbWUgICAgOiA4IGR
      heXMsIDAyaDoxMW06NDRzDQAKDQAKUGxlYXNlIGtleWluIHlvdXIgcGFzc3dvcmQ6
    </example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="NPort"/>
    <param pos="0" name="hw.device" value="Device Server"/>
    <param pos="1" name="hw.product"/>
    <param pos="2" name="host.mac"/>
    <param pos="3" name="host.id"/>
    <param pos="0" name="os.vendor" value="Moxa"/>
    <param pos="4" name="os.version"/>
    <param pos="5" name="os.version.version"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n|\x00|-)*Model name\s+: NPort (5[\w-]+)(?:\r|\n|\x00)+Please keyin your username:">
    <description>Moxa NPort Device Server - 5xxx Series - Model only</description>
    <!-- Model name       : NPort 5110A\r\n\r\nPlease keyin your username: -->

    <example _encoding="base64" hw.product="5110A">TW9kZWwgbmFtZSAgICAgICA6IE5Q
      b3J0IDUxMTBBDQoNClBsZWFzZSBrZXlpbiB5b3VyIHVzZXJuYW1lOgo=
    </example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="NPort"/>
    <param pos="0" name="hw.device" value="Device Server"/>
    <param pos="1" name="hw.product"/>
  </fingerprint>

  <fingerprint pattern="^Model name\s+: MGate (MB3[\w-]+)(?:\r|\n|\x00|)+MAC address\s+: ([\w:]+)(?:\r|\n|\x00)+Serial No.\s+: (\d+)(?:\r|\n|\x00)+Firmware version : ([\d.]+) Build (\d+)(?:\r|\n|\x00)+">
    <description>Moxa MGate Modbus Gateway</description>
    <!-- Model name       : MGate MB3180\r\u0000\nMAC address      : 00:90:E8:AA:AA:AA\r\u0000\nSerial No.       : 9474\r\u0000\nFirmware version : 1.2 Build 09101913\r\u0000\nSystem uptime    : 15 days, 16h:37m:48s\r\u0000\n\r\u0000\nPlease keyin your password: -->

    <example _encoding="base64" hw.product="MB3180" host.mac="00:90:E8:AA:AA:AA" host.id="9474" os.version="1.2" os.version.version="09101913">
      TW9kZWwgbmFtZSAgICAgICA6IE1HYXRlIE1CMzE4MA0ACk1BQyBhZGRyZXNzICAgICAgOiAwM
      Do5MDpFODpBQTpBQTpBQQ0AClNlcmlhbCBOby4gICAgICAgOiA5NDc0DQAKRmlybXdhcmUgdm
      Vyc2lvbiA6IDEuMiBCdWlsZCAwOTEwMTkxMw0AClN5c3RlbSB1cHRpbWUgICAgOiAxNSBkYXl
      zLCAxNmg6MzdtOjQ4cw0ACg0AClBsZWFzZSBrZXlpbiB5b3VyIHBhc3N3b3JkOg==
    </example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="MGate"/>
    <param pos="0" name="hw.device" value="Industrial Control"/>
    <param pos="1" name="hw.product"/>
    <param pos="2" name="host.mac"/>
    <param pos="3" name="host.id"/>
    <param pos="0" name="os.vendor" value="Moxa"/>
    <param pos="4" name="os.version"/>
    <param pos="5" name="os.version.version"/>
  </fingerprint>

  <fingerprint pattern="^Model name\s+: (NE[\w-]+)(?:\r|\n|\x00)+MAC address\s+: ([\w:]+)(?:\r|\n|\x00)+Serial No.\s+: (\d+)(?:\r|\n|\x00)+Firmware version\s+: ([\d.]+)(?: Build (\d+)(?:\r|\n|\x00)+)?">
    <description>Moxa NE Series Embedded device server</description>
    <!-- Model name       : NE-4110S\r\u0000\nMAC address      : 00:90:E8:AA:AA:AA\r\u0000\nSerial No        : 3616\r\u0000\nFirmware version : 4.1 Build 07061517\r\u0000\n\r\u0000\nPlease keyin your password: -->

    <example _encoding="base64" hw.product="NE-4110S" host.mac="00:90:E8:AA:AA:AA" host.id="3616" os.version="4.1" os.version.version="07061517">
      TW9kZWwgbmFtZSAgICAgICA6IE5FLTQxMTBTDQAKTUFDIGFkZHJlc3MgICAgICA6IDAwOjkwO
      kU4OkFBOkFBOkFBDQAKU2VyaWFsIE5vICAgICAgICA6IDM2MTYNAApGaXJtd2FyZSB2ZXJzaW
      9uIDogNC4xIEJ1aWxkIDA3MDYxNTE3DQAKDQAKUGxlYXNlIGtleWluIHlvdXIgcGFzc3dvcmQ6
    </example>
    <!-- Model name       : NE-4110S\r\nMAC address      : 00:90:E8:AA:AA:AA\r\nSerial No        : 000\r\nFirmware version : 1.5.2\r\n\r\nPlease keyin your password: -->

    <example _encoding="base64" hw.product="NE-4110S" host.mac="00:90:E8:AA:AA:AA" host.id="000" os.version="1.5.2">
      TW9kZWwgbmFtZSAgICAgICA6IE5FLTQxMTBTDQpNQUMgYWRkcmVzcyAgICAgIDogMDA6OTA6RTg6QUE6QUE6QUENClNlcmlhbCBObyAgICAgICAgOiAwMDANCkZpcm13YXJlIHZlcnNpb24gOiAxLjUuMg0KDQpQbGVhc2Uga2V5aW4geW91ciBwYXNzd29yZDoK
      </example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="NE"/>
    <param pos="0" name="hw.device" value="Device Server"/>
    <param pos="1" name="hw.product"/>
    <param pos="2" name="host.mac"/>
    <param pos="3" name="host.id"/>
    <param pos="0" name="os.vendor" value="Moxa"/>
    <param pos="4" name="os.version"/>
    <param pos="5" name="os.version.version"/>
  </fingerprint>

  <fingerprint pattern="^Model name\s+: (MiiNePort [\w-]+)(?:\r|\n|\x00)+Serial No.\s+: (\d+)(?:\r|\n|\x00)+Device name\s+: [\w:-_\&amp;]+(?:\r|\n|\x00)+Firmware version\s+: ([\d.]+) Build (\d+)(?:\r|\n|\x00)+Ethernet MAC address: ([\w:]+)(?:\r|\n|\x00)+">
    <description>Moxa MiiNePort Series Embedded device server</description>
    <!-- Model name          : MiiNePort E2\r\nSerial No.          : 9999\r\nDevice name         : MiiNePort_E2_4064\r\nFirmware version    : 1.3.36 Build 15031615\r\nEthernet MAC address: 00:90:E8:5A:92:FF\r\n\r\nPlease keyin your password: -->

    <example _encoding="base64" hw.product="MiiNePort E2" host.mac="00:90:E8:5A:92:FF" host.id="9999" os.version="1.3.36" os.version.version="15031615">
      TW9kZWwgbmFtZSAgICAgICAgICA6IE1paU5lUG9ydCBFMg0KU2VyaWFsIE5vLiAgICAgICAgI
      CA6IDk5OTkNCkRldmljZSBuYW1lICAgICAgICAgOiBNaWlOZVBvcnRfRTJfNDA2NA0KRmlybX
      dhcmUgdmVyc2lvbiAgICA6IDEuMy4zNiBCdWlsZCAxNTAzMTYxNQ0KRXRoZXJuZXQgTUFDIGF
      kZHJlc3M6IDAwOjkwOkU4OjVBOjkyOkZGDQoNClBsZWFzZSBrZXlpbiB5b3VyIHBhc3N3b3Jk
      Ogo=
    </example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="MiiNePort"/>
    <param pos="0" name="hw.device" value="Device Server"/>
    <param pos="1" name="hw.product"/>
    <param pos="2" name="host.id"/>
    <param pos="0" name="os.vendor" value="Moxa"/>
    <param pos="3" name="os.version"/>
    <param pos="4" name="os.version.version"/>
    <param pos="5" name="host.mac"/>
  </fingerprint>

  <!-- The following is very specific in order to express CPE values -->

  <fingerprint pattern="^EDR-G903 login:">
    <description>Moxa EDR Secure Routers - EDR-G903</description>
    <example>EDR-G903 login:</example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="EDR"/>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="0" name="hw.product" value="EDR-G903"/>
    <param pos="0" name="hw.cpe23" value="cpe:/h:moxa:edr-g903:-"/>
    <param pos="0" name="os.vendor" value="Moxa"/>
    <param pos="0" name="os.family" value="EDR"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="0" name="os.product" value="EDR G903 Firmware"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:moxa:edr_g903_firmware:-"/>
  </fingerprint>

  <fingerprint pattern="^EDR-G902 login:">
    <description>Moxa EDR Secure Routers - EDR-G902</description>
    <example>EDR-G902 login:</example>
    <param pos="0" name="hw.vendor" value="Moxa"/>
    <param pos="0" name="hw.family" value="EDR"/>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="0" name="hw.product" value="EDR-G902"/>
    <param pos="0" name="hw.cpe23" value="cpe:/h:moxa:edr-g902:-"/>
    <param pos="0" name="os.vendor" value="Moxa"/>
    <param pos="0" name="os.family" value="EDR"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="0" name="os.product" value="EDR G902 Firmware"/>
  </fingerprint>

  <fingerprint pattern="^Red Hat Linux release ([^\\s]+)\\s*.*$">
    <description>RedHat general purpose linux</description>
    <!-- Red Hat Linux release 9 (Shrike)\nKernel 2.4.20-8 on an i686\nlogin: -->

    <example _encoding="base64" os.version="9 (Shrike)">
      UmVkIEhhdCBMaW51eCByZWxlYXNlIDkgKFNocmlrZSlcbktlcm5lbCAyLjQuMjAtOCBvbiBhbiBpNjg2XG5sb2dpbjo=
   </example>
    <param pos="0" name="os.vendor" value="Red Hat"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.device" value="Linux"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^(?m)Red Hat Enterprise Linux ES release (.*) \(.*\).*Kernel (.*) on a[^ ]* ([^ ]*\d)" flags="REG_MULTILINE">
    <description>RedHat Enterprise Linux ES</description>
    <!-- Red Hat Enterprise Linux ES release 3 (Taroon Update 9\nKernel 2.4.21-47.EL on an x86_64\nlogin: -->

    <example _encoding="base64" os.version="3" linux.kernel.version="2.4.21-47.EL" os.arch="x86_64">
      UmVkIEhhdCBFbnRlcnByaXNlIExpbnV4IEVTIHJlbGVhc2UgMyAoVGFyb29uIFVwZGF0ZSA5KQpLZXJuZWwgMi40LjIxLTQ3Lk
      VMIG9uIGFuIHg4Nl82NApsb2dpbjo=
    </example>
    <param pos="0" name="os.vendor" value="Red Hat"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="linux.kernel.version"/>
    <param pos="3" name="os.arch"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:redhat:linux:{os.version}"/>
  </fingerprint>

  <fingerprint pattern="^(?m)Red Hat Enterprise Linux AS release (.*) \(.*\).*Kernel (.*) on a[^ ]* ([^ ]*\d)" flags="REG_MULTILINE">
    <description>RedHat Enterprise Linux AS</description>
    <!-- Red Hat Enterprise Linux AS release 5.8 (Tikanga)\nKernel 2.6.18-308.11.1.el5 on an x86_64\nlogin: -->

    <example _encoding="base64" os.version="5.8" linux.kernel.version="2.6.18-308.11.1.el5" os.arch="x86_64">
      UmVkIEhhdCBFbnRlcnByaXNlIExpbnV4IEFTIHJlbGVhc2UgNS44IChUaWthbmdhKQpLZXJuZWwgM
      i42LjE4LTMwOC4xMS4xLmVsNSBvbiBhbiB4ODZfNjQKbG9naW46
    </example>
    <param pos="0" name="os.vendor" value="Red Hat"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="RedHat Enterprise AS"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="linux.kernel.version"/>
    <param pos="3" name="os.arch"/>
  </fingerprint>

  <fingerprint pattern="^(?m)Red Hat Enterprise Linux WS release (.*) \(.*\).*Kernel (.*) on a[^ ]* ([^ ]*)" flags="REG_MULTILINE">
    <description>RedHat Enterprise Linux WS</description>
    <!--Red Hat Enterprise Linux WS release 2.1 (Tampa) \nKernel 2.4.9-e.40smp on an i686 \nlogin:  -->

    <example _encoding="base64" os.version="2.1" linux.kernel.version="2.4.9-e.40smp" os.arch="i686">
      UmVkIEhhdCBFbnRlcnByaXNlIExpbnV4IFdTIHJlbGVhc2UgMi4xIChUYW1wY
      SkgCktlcm5lbCAyLjQuOS1lLjQwc21wIG9uIGFuIGk2ODYgCmxvZ2luOiA=
    </example>
    <param pos="0" name="os.vendor" value="Red Hat"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="RedHat Enterprise WS"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="linux.kernel.version"/>
    <param pos="3" name="os.arch"/>
  </fingerprint>

  <fingerprint pattern="^(?m)Fedora Core.release (.*) \(.*\).*Kernel (.*) on a[^ ]* ([^ ]*\d).*$" flags="REG_MULTILINE">
    <description>Fedora Core Release</description>
    <!-- Fedora Core release 1 (Yarrow)\nKernel 2.4.20-13.9ensim-3.5.0-13 on an i686\nlogin:-->

    <example _encoding="base64" os.version="1" linux.kernel.version="2.4.20-13.9ensim-3.5.0-13" os.arch="i686">
     RmVkb3JhIENvcmUgcmVsZWFzZSAxIChZYXJyb3cpCktlcm5lbCAyLjQuMjAtMTMuOWVuc2ltLTMuNS4wLTEzIG9uIGFuIGk2ODYKbG9naW46
    </example>
    <param pos="0" name="os.vendor" value="Red Hat"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Fedora"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="linux.kernel.version"/>
    <param pos="3" name="os.arch"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:redhat:fedora:{os.version}"/>
  </fingerprint>

  <fingerprint pattern="^(?m)Welcome to SuSE Linux (.*) \(([^\)]+)\) - Kernel (.*) .*">
    <description>SuSE Linux</description>
    <!-- Welcome to SuSE Linux 7.0 (i386) - Kernel 2.2.16-RAID (0). 2VG029037\n\nlogin: -->

    <example _encoding="base64" os.version="7.0" os.arch="i386" linux.kernel.version="2.2.16-RAID (0). 2VG029037">
      V2VsY29tZSB0byBTdVNFIExpbnV4IDcuMCAoaTM4NikgLSBLZXJuZWwgMi4yLjE2LVJBSUQgKDApLiAyVkcwMjkwMzcgCgpsb2dpbjo=
    </example>
    <param pos="0" name="os.vendor" value="SUSE"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="os.arch"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:suse:linux:{os.version}"/>
    <param pos="3" name="linux.kernel.version"/>
  </fingerprint>

  <fingerprint pattern="^Turbolinux ApplianceServer (\d+\.\d+).*">
    <description>Turbolinux ApplianceServer</description>
    <!--Turbolinux ApplianceServer 4.0 (Atlas2) Linux 2.6.32-431.23.3.el6.x86_64 on a x86_64\n(senyo191x89.digitalink.ne.jp) TTY: 12:15 on Tuesday, 02 October 2018 login:  -->

    <example _encoding="base64" os.version="4.0">
     VHVyYm9saW51eCBBcHBsaWFuY2VTZXJ2ZXIgNC4wIChBdGxhczIpIExpbnV4IDIuNi4zMi00MzEuMjMuMy5lbDYueDg
     2XzY0IG9uIGEgeDg2XzY0IChzZW55bzE5MXg4OS5kaWdpdGFsaW5rLm5lLmpwKSBUVFk6IDEyOjE1IG9uIFR1ZXNkYX
     ksIDAyIE9jdG9iZXIgMjAxOCBsb2dpbjog
    </example>
    <param pos="0" name="os.vendor" value="Turbolinux"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^UnixWare ([^ ]+).*$">
    <description>UnixWare</description>
    <!-- UnixWare 2.1.3 (profil) (pts/3)\n\n\nlogin:  -->

    <example _encoding="base64" os.version="2.1.3">
     VW5peFdhcmUgMi4xLjMgKHByb2ZpbCkgKHB0cy8zKQoKCgpsb2dpbjog
    </example>
    <param pos="0" name="os.vendor" value="SCO"/>
    <param pos="0" name="os.family" value="UnixWare"/>
    <param pos="0" name="os.device" value="UnixWare"/>
    <param pos="0" name="os.product" value="UnixWare"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^Telnet Server Build (5.*)">
    <description>Windows 2000</description>
    <!--Microsoft (R) Windows NT (TM) Version 4.00 (Build 1381)\nWelcome to Microsoft Telnet Service \nTelnet Server Build 5.00.99034.1\nlogin:  -->

    <example _encoding="base64" os.version="5.00.99034.1">
      TWljcm9zb2Z0IChSKSBXaW5kb3dzIE5UIChUTSkgVmVyc2lvbiA0LjAwIChCdWlsZCAxMzgxKQpXZWxj
      b21lIHRvIE1pY3Jvc29mdCBUZWxuZXQgU2VydmljZSAKVGVsbmV0IFNlcnZlciBCdWlsZCA1LjAwLjk5MDM0LjEKCmxvZ2luOiA=
    </example>
    <param pos="0" name="os.vendor" value="Microsoft"/>
    <param pos="0" name="os.family" value="Windows"/>
    <param pos="0" name="os.product" value="Windows 2000"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:microsoft:windows_2000:{os.version}"/>
  </fingerprint>

  <fingerprint pattern="^Welcome. Type return, enter password at # prompt">
    <description>Brother Printer</description>
    <!-- Welcome. Type return, enter password at # prompt -->

    <example _encoding="base64">
      V2VsY29tZS4gVHlwZSByZXR1cm4sIGVudGVyIHBhc3N3b3JkIGF0ICMgcHJvbXB0Cg==
    </example>
    <param pos="0" name="os.vendor" value="Brother"/>
    <param pos="0" name="os.family" value="Brother"/>
    <param pos="0" name="os.device" value="Printer"/>
    <param pos="0" name="os.product" value="Brother Printer"/>
  </fingerprint>

  <fingerprint pattern="^(.*) Copyright by ARESCOM">
    <description>Arescom System</description>
    <!--NDS1260HE-TLI Copyright by ARESCOM 2002\n\n\nPassword: -->

    <example _encoding="base64" os.model="NDS1260HE-TLI">
      TkRTMTI2MEhFLVRMSSBDb3B5cmlnaHQgYnkgQVJFU0NPTSAyMDAyCgoKClBhc3N3b3JkOgo=
    </example>
    <param pos="0" name="os.vendor" value="Arescom"/>
    <param pos="0" name="os.device" value="WAP"/>
    <param pos="1" name="os.model"/>
  </fingerprint>

  <fingerprint pattern="^Welcome to ViewStation">
    <description>Polycom ViewStation Video Conference System</description>
    <!-- Welcome to ViewStation\nPassword: -->

    <example _encoding="base64">
      V2VsY29tZSB0byBWaWV3U3RhdGlvbgoKUGFzc3dvcmQ6
    </example>
    <param pos="0" name="os.vendor" value="Polycom"/>
    <param pos="0" name="os.device" value="ViewStation"/>
  </fingerprint>

  <fingerprint pattern="^FlowPoint\/(.*) SDSL \[ATM\] Router .*v(.*) Ready">
    <!--FlowPoint/2200 SDSL [ATM] Router fp2200-12 v3.0.2 Ready\nLogin:  -->

    <description>FlowPoint 2200 DSL router</description>
    <example _encoding="base64" hw.model="2200" os.version="3.0.2">
      Rmxvd1BvaW50LzIyMDAgU0RTTCBbQVRNXSBSb3V0ZXIgZnAyMjAwLTEyIHYzLjAuMiBSZWFkeQpMb2dpbjog
    </example>
    <param pos="0" name="os.vendor" value="FlowPoint"/>
    <param pos="0" name="hw.device" value="Broadband Router"/>
    <param pos="0" name="hw.product" value="DSL Router"/>
    <param pos="1" name="hw.model"/>
    <param pos="2" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^GlobespanVirata Inc\., Software Release (.*)">
    <description>GlobespanVirata broadband router</description>
    <!--GlobespanVirata Inc., Software Release 2.1.040407a3_u_e_A\nCopyright (c) 2001-2003 by GlobespanVirata, Inc.\n\nlogin:  -->

    <example _encoding="base64" os.version="2.1.040407a3_u_e_A">
      R2xvYmVzcGFuVmlyYXRhIEluYy4sIFNvZnR3YXJlIFJlbGVhc2UgMi4xLjA0MDQwN2EzX3VfZV9BCgpDb3B5cmlnaHQgKG
      MpIDIwMDEtMjAwMyBieSBHbG9iZXNwYW5WaXJhdGEsIEluYy4KCgpsb2dpbjog
    </example>
    <param pos="0" name="os.vendor" value="Conexant"/>
    <param pos="0" name="hw.device" value="Broadband Router"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^VxWorks login:">
    <description>VxWorks embedded device</description>
    <example>VxWorks login: </example>
    <param pos="0" name="os.family" value="VxWorks"/>
  </fingerprint>

  <fingerprint pattern=".*Nortel.*Passport ([^ ]*) .*Software Release ([^ ]*).*">
    <description>Nortel Passport</description>
    <!-- *********************************************\n\n\n* Copyright (c) 2003 Nortel Networks, Inc.  *\n\n\n* All Rights Reserved                       *\n\n\n* Passport 8010                             *\n\n\n* Software Release 3.5.0.0                  *\n\n\n*********************************************\n\n\n\n\nLogin: -->

    <example _encoding="base64" os.product="8010" os.version="3.5.0.0">
      KioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqXG5cblxuKiBDb3B5cmlnaHQgKG
      MpIDIwMDMgTm9ydGVsIE5ldHdvcmtzLCBJbmMuICAqXG5cblxuKiBBbGwgUmlnaHRzIFJlc2VydmVkICAgICAg
      ICAgICAgICAgICAgICAgICAqXG5cblxuKiBQYXNzcG9ydCA4MDEwICAgICAgICAgICAgICAgICAgICAgICAgIC
      AgICAqXG5cblxuKiBTb2Z0d2FyZSBSZWxlYXNlIDMuNS4wLjAgICAgICAgICAgICAgICAgICAqXG5cblxuKioq
      KioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqXG5cblxuXG5cbkxvZ2luOg==
    </example>
    <param pos="0" name="os.vendor" value="Nortel"/>
    <param pos="0" name="os.device" value="Switch"/>
    <param pos="1" name="os.product"/>
    <param pos="2" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^IPSO.* \((.*)\) \(tty.*\)">
    <description>Checkpoint Firewall-1 running on a Nokia IPSO appliance</description>
    <!-- IPSO/i386 (BJ-IDC-FW2) (ttyp7)\n\n\nThis system is for authorized use only.\n\n\n\n\n\n\nlogin: -->

    <example _encoding="base64" host.name="BJ-IDC-FW2">
     SVBTTy9pMzg2IChCSi1JREMtRlcyKSAodHR5cDcpCgoKClRoaXMgc3lzdGVtIGlzIGZvciBhdXRob3Jpem
     VkIHVzZSBvbmx5LgoKCgoKCgoKbG9naW46IA==
    </example>
    <param pos="0" name="os.vendor" value="Check Point"/>
    <param pos="0" name="os.family" value="Check Point"/>
    <param pos="0" name="os.device" value="Firewall"/>
    <param pos="0" name="os.product" value="IPSO"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="Tasman Networks Inc.*Telnet Login">
    <description>Tasman Networks Login</description>
    <!-- #\n# Tasman Networks Inc. Telnet Login\n#Escape character is '^]'\n\n\n\nlogin: -->


    <example _encoding="base64" os.vendor="Tasman Networks">
      Iy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0
      tLS0tLS0tCiMgVGFzbWFuIE5ldHdvcmtzIEluYy4gVGVsbmV0IExvZ2luCiMtLS0tLS0tLS0tLS0tLS0tLS0tLS
      0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQpFc2NhcGUgY2hhcmFjd
      GVyIGlzICdeXScuCgoKICAgICAgICAKbG9naW46IA==
    </example>
    <param pos="0" name="os.vendor" value="Tasman Networks"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="0" name="os.product" value="Tasman Networks router"/>
  </fingerprint>

  <fingerprint pattern="Pragma Systems">
    <description>MS Windows running Pragma TelnetD server</description>
    <!-- Welcome to Gemadept Logistics RF Server\n(C) Copyright 1994-2012 Pragma Systems, Inc.\nlogin name: -->

    <example _encoding="base64">
      V2VsY29tZSB0byBHZW1hZGVwdCBMb2dpc3RpY3MgUkYgU2VydmVyCihDKSBDb3B5cmlnaHQgMTk5NC0yMDEyIFB
      yYWdtYSBTeXN0ZW1zLCBJbmMuCgpsb2dpbiBuYW1lOiA=
    </example>
    <param pos="0" name="os.vendor" value="Microsoft"/>
    <param pos="0" name="os.family" value="Windows"/>
    <param pos="0" name="os.product" value="Windows"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:microsoft:windows:-"/>
  </fingerprint>

  <fingerprint pattern="^Application Required. No Installation Default">
    <description>probably IBM AS/400 running TN3270 or 5250 emulation server</description>
    <!-- Application Required. No Installation Default\nEnter Application Name: -->

    <example _encoding="base64">
     QXBwbGljYXRpb24gUmVxdWlyZWQuIE5vIEluc3RhbGxhdGlvbiBEZWZhdWx0ICAgICAgICA
     gICAgICAgICAgICAgICAgICAgICAgICAgIApFbnRlciBBcHBsaWNhdGlvbiBOYW1lOg==
    </example>
    <param pos="0" name="os.vendor" value="IBM"/>
    <param pos="0" name="os.family" value="OS/400"/>
    <param pos="0" name="os.product" value="OS/400"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:ibm:os_400:-"/>
  </fingerprint>

  <fingerprint pattern="^This copy of the Ataman TCP Remote Logon Services">
    <description>Windows NT/2k/2k3 running Ataman telnet server</description>
    <!-- This copy of the Ataman TCP Remote Logon Services is registered as licensed to:\nECI2/DDMS\nAccount Name: -->

    <example _encoding="base64">
      VGhpcyBjb3B5IG9mIHRoZSBBdGFtYW4gVENQIFJlbW90ZSBMb2dvbiBTZXJ2aWNlcyBpcyByZWdpc3RlcmVkIG
      FzIGxpY2Vuc2VkIHRvOgoJRUNJMi9ERE1TCgpBY2NvdW50IE5hbWU6IA==
    </example>
    <param pos="0" name="os.vendor" value="Microsoft"/>
    <param pos="0" name="os.family" value="Windows"/>
    <param pos="0" name="os.product" value="Windows"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:microsoft:windows:-"/>
  </fingerprint>

  <fingerprint pattern="Cobalt Linux release\W(.*)\W\(.*">
    <description>Cobalt Linux</description>
    <!-- Cobalt Linux release 6.0 (Shinkansen)\nKernel 2.2.16C37_III on an i586\nlogin:  -->

    <example _encoding="base64" os.version="6.0">
      Q29iYWx0IExpbnV4IHJlbGVhc2UgNi4wIChTaGlua2Fuc2VuKQpLZXJuZWwgMi4yLjE2QzM3X0lJSSBvbiBhbiBpNTg2CmxvZ2luOiA=
    </example>
    <param pos="0" name="os.vendor" value="Cobalt"/>
    <param pos="0" name="os.family" value="Linux"/>
    <param pos="0" name="os.product" value="Linux"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^Check Point FireWall-1 authenticated Telnet server running on (.*)">
    <description>Check Point Firewall-1</description>
    <!-- Check Point FireWall-1 authenticated Telnet server running on gaatdrf2\nUser: -->

    <example _encoding="base64" host.name="gaatdrf2">
      Q2hlY2sgUG9pbnQgRmlyZVdhbGwtMSBhdXRoZW50aWNhdGVkIFRlbG5ldCBzZXJ2ZXIgcnVubmluZyBvbiBnYWF0ZHJmMgoKVXNlcjog
    </example>
    <param pos="0" name="os.vendor" value="Checkpoint"/>
    <param pos="0" name="os.family" value="Checkpoint"/>
    <param pos="0" name="os.device" value="Firewall"/>
    <param pos="0" name="os.product" value="Checkpoint FW1"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^Raptor Firewall">
    <description>Raptor Firewall</description>
    <!-- Raptor Firewall Secure Gateway.\nHostname: -->

    <example _encoding="base64">
      UmFwdG9yIEZpcmV3YWxsIFNlY3VyZSBHYXRld2F5LgoKSG9zdG5hbWU6IA==
    </example>
    <param pos="0" name="os.vendor" value="Symantec"/>
    <param pos="0" name="os.family" value="Raptor"/>
    <param pos="0" name="os.device" value="Firewall"/>
    <param pos="0" name="os.product" value="Raptor"/>
  </fingerprint>

  <fingerprint pattern="UNIX\(r\) System V Release (\d*.\d*)">
    <description>SunOS (Solaris)</description>
    <!-- Raptor Firewall Secure Gateway.\nHostname: -->

    <example _encoding="base64" os.version="4.0">
      VU5JWChyKSBTeXN0ZW0gViBSZWxlYXNlIDQuMCAoVGhlLVNlcnZlcikKCgoKbG9naW46IA==
    </example>
    <param pos="0" name="os.vendor" value="Sun"/>
    <param pos="0" name="os.family" value="Solaris"/>
    <param pos="0" name="os.product" value="Solaris"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:sun:solaris:{os.version}"/>
  </fingerprint>

  <fingerprint pattern="Solaris (.*)">
    <description>Solaris</description>
    <!-- Seattle Community Network Sun Solaris 1.1.1.B\nPlease login as 'visitor' if you are a visitorn\n\nSunOS UNIX (scn)\n\n\nlogin:-->

    <example _encoding="base64" os.version="1.1.1.B">
      U2VhdHRsZSBDb21tdW5pdHkgTmV0d29yayBTdW4gU29sYXJpcyAxLjEuMS5CClBsZWFzZSBsb2dpbiBhcyAndml
      zaXRvcicgaWYgeW91IGFyZSBhIHZpc2l0b3IKCgpTdW5PUyBVTklYIChzY24pCgoKCmxvZ2luOg==
    </example>
    <param pos="0" name="os.vendor" value="Sun"/>
    <param pos="0" name="os.family" value="Solaris"/>
    <param pos="0" name="os.product" value="Solaris"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:sun:solaris:{os.version}"/>
  </fingerprint>

  <fingerprint pattern="^Digital UNIX \(([^)]+).*">
    <description>Digital Unix</description>
    <!-- Digital UNIX (journal) (ttyp2)\n\n\nlogin: -->

    <example _encoding="base64" host.name="journal">
      RGlnaXRhbCBVTklYIChqb3VybmFsKSAodHR5cDIpCgoKCmxvZ2luOiA=
    </example>
    <param pos="0" name="os.vendor" value="HP"/>
    <param pos="0" name="os.family" value="Digital Unix"/>
    <param pos="0" name="os.product" value="Digital Unix"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?m)Compaq Tru64 UNIX V(.*) \(Rev. (.*\d)\) .*">
    <description>Compaq Tru64 UNIX V</description>
    <!-- Compaq Tru64 UNIX V5.1B (Rev. 2650) (docalpha) (pts/11)\n\n\n\n\nlogin: -->

    <example _encoding="base64" os.version="5.1B" os.rev="2650">
     Q29tcGFxIFRydTY0IFVOSVggVjUuMUIgKFJldi4gMjY1MCkgKGRvY2FscGhhKSAocHRzLzExKQoKCgoKCmxvZ2luOg==
    </example>
    <param pos="0" name="os.vendor" value="HP"/>
    <param pos="0" name="os.family" value="Digital Unix"/>
    <param pos="0" name="os.product" value="TRU64"/>
    <param pos="1" name="os.version"/>
    <param pos="2" name="os.rev"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:hp:tru64:{os.version}"/>
  </fingerprint>

  <fingerprint pattern="HP-UX ([^ ]+) [A-Z]\.([^ ]+) ([^ ]+) ([^ ]+)\s([^ ]+\)).*$">
    <description>System HP-UX</description>
    <!-- HP-UX ctout B.11.11 U 9000/800 (tc)\nlogin: -->

    <example _encoding="base64" host.name="ctout" os.version="11.11" hw.series="9000/800" hw.model="(tc)" hw.version="U">
      SFAtVVggY3RvdXQgQi4xMS4xMSBVIDkwMDAvODAwICh0YykKCmxvZ2luOiA=
    </example>
    <param pos="0" name="os.vendor" value="HP"/>
    <param pos="0" name="os.family" value="HP-UX"/>
    <param pos="0" name="os.product" value="HP-UX"/>
    <param pos="1" name="host.name"/>
    <param pos="2" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:hp:hp-ux:{os.version}"/>
    <param pos="3" name="hw.version"/>
    <param pos="4" name="hw.series"/>
    <param pos="5" name="hw.model"/>
  </fingerprint>

  <fingerprint pattern="^Data ONTAP">
    <description>A NetApp apliance</description>
    <!-- Data ONTAP (s500.)\nlogin: -->

    <example _encoding="base64">RGF0YSBPTlRBUCAoczUwMC4pCmxvZ2luOiA=</example>
    <param pos="0" name="os.vendor" value="NetApp"/>
    <param pos="0" name="os.family" value="Data ONTAP"/>
    <param pos="0" name="os.product" value="Data ONTAP"/>
    <param pos="0" name="os.device" value="NAS"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:netapp:data_ontap:-"/>
    <param pos="0" name="hw.vendor" value="NetApp"/>
    <param pos="0" name="hw.family" value="Data ONTAP"/>
    <param pos="0" name="hw.product" value="Data ONTAP"/>
    <param pos="0" name="hw.device" value="NAS"/>
  </fingerprint>

  <fingerprint pattern="OpenVMS.*Version\sV([^\s]+).*">
    <description>OpenVMS</description>
    <!--  Welcome to OpenVMS (TM) Alpha Operating System, Version V8.4     - NOT70\n\nUsername: -->

    <example _encoding="base64" os.version="8.4">
      IFdlbGNvbWUgdG8gT3BlblZNUyAoVE0pIEFscGhhIE9wZXJhdGluZyBTeXN0Z
      W0sIFZlcnNpb24gVjguNCAgICAgLSBOT1Q3MAoKClVzZXJuYW1lOiA=
    </example>
    <param pos="0" name="os.vendor" value="HP"/>
    <param pos="0" name="os.family" value="OpenVMS"/>
    <param pos="0" name="os.product" value="VMS"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^(?m)SCO OpenServer\(TM\) Release ([^ ]+).*$">
    <description>SCO OpenServer</description>
    <!-- SCO OpenServer(TM) Release 5 (bomdia.co.za) (ttyp6)\nlogin: -->

    <example _encoding="base64" os.version="5">
      U0NPIE9wZW5TZXJ2ZXIoVE0pIFJlbGVhc2UgNSAoYm9tZGlhLmNvLnphKSAodHR5cDYpCgpsb2dpbjo=
    </example>
    <param pos="0" name="os.vendor" value="SCO"/>
    <param pos="0" name="os.family" value="OpenServer"/>
    <param pos="0" name="os.product" value="OpenServer"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^% Username:  timeout expired!">
    <description>Some kind of Cisco device</description>
    <!-- % Username:  timeout expired!-->

    <example _encoding="base64">
      JSBVc2VybmFtZTogIHRpbWVvdXQgZXhwaXJlZCE=
    </example>
    <param pos="0" name="os.vendor" value="Cisco"/>
    <param pos="0" name="os.family" value="IOS"/>
    <param pos="0" name="os.product" value="IOS"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:cisco:ios:-"/>
  </fingerprint>

  <fingerprint pattern="^Welcome to MKS Telnet Server Version">
    <description>Windows running MKS Telnet Server</description>
    <example _encoding="base64">
      V2VsY29tZSB0byBNS1MgVGVsbmV0IFNlcnZlciBWZXJzaW9uIDQuNzAuMDAwMC4KbG9naW46IA==
    </example>
    <param pos="0" name="os.vendor" value="Microsoft"/>
    <param pos="0" name="os.family" value="Windows"/>
    <param pos="0" name="os.product" value="Windows"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:microsoft:windows:-"/>
  </fingerprint>

  <fingerprint pattern="^Sorry, this system is engaged\.">
    <description>an embedded print server</description>
    <example>Sorry, this system is engaged.</example>
    <param pos="0" name="os.vendor" value="Epson"/>
    <param pos="0" name="os.device" value="Printer"/>
  </fingerprint>

  <fingerprint pattern="^TELNET session now in ESTABLISHED state">
    <description>an Allied Telesyn router</description>
    <!-- TELNET session now in ESTABLISHED state\n\nGEO-003 login: -->

    <example _encoding="base64">
      VEVMTkVUIHNlc3Npb24gbm93IGluIEVTVEFCTElTSEVEIHN0YXRlCgpHRU8tMDAzIGxvZ2luOiA=
    </example>
    <param pos="0" name="os.vendor" value="Allied Telesyn"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="0" name="os.product" value="Allied Telesyn router"/>
  </fingerprint>

  <fingerprint pattern="^CONEXANT SYSTEMS.*ACCESS RUNNER ADSL">
    <description>a Conexant ADSL router</description>
    <!-- CONEXANT SYSTEMS, INC. ACCESS RUNNER ADSL CONSOLE PORT>>>LOGON PASSWORD>3.27****** -->

    <example _encoding="base64">
      Q09ORVhBTlQgU1lTVEVNUywgSU5DLiBBQ0NFU1MgUlVOTkVSIEFEU0wgQ09OU09MRSBQ
      T1JUPj4+TE9HT04gUEFTU1dPUkQ+My4yNyoqKioqKg==
    </example>
    <param pos="0" name="os.vendor" value="Conexant"/>
    <param pos="0" name="os.device" value="Broadband Router"/>
    <param pos="0" name="os.product" value="AccessRunner ADSL router"/>
  </fingerprint>

  <fingerprint pattern="^System administrator is connecting from">
    <description>a DrayTek Vigor SOHO Router</description>
    <!-- System administrator is connecting from 54.39.173.86\n\nReject the connection request !!! -->

    <example _encoding="base64">
      U3lzdGVtIGFkbWluaXN0cmF0b3IgaXMgY29ubmVjdGluZyBmcm9tIDU0LjM5LjE3My44NgoKUmVqZWN0IH
      RoZSBjb25uZWN0aW9uIHJlcXVlc3QgISEh
    </example>
    <param pos="0" name="hw.vendor" value="DrayTek"/>
    <param pos="0" name="hw.device" value="Broadband Router"/>
    <param pos="0" name="hw.product" value="Vigor"/>
  </fingerprint>

  <fingerprint pattern=".*Version\s(\d*.\d*)\/OpenBSD.*">
    <description>OpenBSD</description>
    <!-- 220 killer09 FTP server (Version 6.4/OpenBSD/Linux-ftpd-0.17) ready. -->

    <example _encoding="base64" os.version="6.4">
      MjIwIGtpbGxlcjA5IEZUUCBzZXJ2ZXIgKFZlcnNpb24gNi40L09wZW5CU0QvTGludXgtZnRwZC0wLjE3KSByZWFkeS4K
    </example>
    <param pos="0" name="os.vendor" value="OpenBSD"/>
    <param pos="0" name="os.family" value="OpenBSD"/>
    <param pos="0" name="os.product" value="OpenBSD"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:openbsd:openbsd:{os.version}"/>
  </fingerprint>

  <fingerprint pattern="^FreeBSD\/([^\\s]+)\s+\(([^\s]+)\)">
    <description>a FreeBSD</description>
    <!-- FreeBSD/amd64 (ms.gymspgs.cz) (pts/0)\n\n\n\nlogin: -->

    <example _encoding="base64" os.arch="amd64" host.name="ms.gymspgs.cz">
      RnJlZUJTRC9hbWQ2NCAobXMuZ3ltc3Bncy5jeikgKHB0cy8wKQoKCgpsb2dpbjo=
    </example>
    <param pos="0" name="os.vendor" value="FreeBSD"/>
    <param pos="0" name="os.family" value="FreeBSD"/>
    <param pos="0" name="os.product" value="FreeBSD"/>
    <param pos="1" name="os.arch"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:freebsd:freebsd:-"/>
    <param pos="2" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^NetBSD">
    <description>NetBSD</description>
    <!-- NetBSD/evbsh3 (Fukuyama.Host_AKS_0555_WL-v2.60d) (ttyp1)  -->

    <example _encoding="base64">
      TmV0QlNEL21lc3NpbWlwcyAoKSAodHR5cDMpCgpsb2dpbjog
    </example>
    <param pos="0" name="os.vendor" value="NetBSD"/>
    <param pos="0" name="os.family" value="NetBSD"/>
    <param pos="0" name="os.product" value="NetBSD"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:netbsd:netbsd:-"/>
  </fingerprint>

  <fingerprint pattern="^IRIX\W\((.*)\)">
    <description>SGI IRIX</description>
    <!-- IRIX (artemis.biol.uoa.gr)\n\n\n\nlogin: -->

    <example _encoding="base64" host.name="artemis.biol.uoa.gr">
      SVJJWCAoYXJ0ZW1pcy5iaW9sLnVvYS5ncikKCgoKbG9naW46IA==
    </example>
    <param pos="0" name="os.vendor" value="SGI"/>
    <param pos="0" name="os.family" value="IRIX"/>
    <param pos="0" name="os.product" value="IRIX"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:sgi:irix:-"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="(?m)(ES|RS)\s([^\s]+) System Software, Version ([^\s]+).*Riverstone Networks" flags="REG_MULTILINE">
    <description>a Riverstone router</description>

    <!-- ++++++++++++++++++++++++++++++++++\nES 10170 System Software, Version 9.3.0.4\n
    Riverstone Networks, Inc., Copyright (c) 2000-2003. All rights reserved.\nSystem started on 2018-09-06 15:58:\n
    +++++++++++++++++++++++++++++++++++++++ -->

    <example _encoding="base64" os.product="10170" os.version="9.3.0.4" os.family="ES">
      LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tL
      S0tLS0tLQpFUyAxMDE3MCBTeXN0ZW0gU29mdHdhcmUsIFZlcnNpb24gOS4zLjAuNApSaXZlcnN0b25lIE5ldH
      dvcmtzLCBJbmMuLCBDb3B5cmlnaHQgKGMpIDIwMDAtMjAwMy4gQWxsIHJpZ2h0cyByZXNlcnZlZC4KU3lzdGV
      tIHN0YXJ0ZWQgb24gMjAxOC0wOS0wNiAxNTo1ODozMAotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
      LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS4uLg==
    </example>
    <!-- +++++++++++++++++++++++++++++++++++++++\nRS 10170 System Software, Version 9.3.0.5\n
    Riverstone Networks, Inc., Copyright (c) 2000-2003. All rights reserved.\nSystem started on 2018-09-06 15:58:\n
    +++++++++++++++++++++++++++++++++++++++ -->

    <example _encoding="base64" os.product="8000" os.version="9.3.0.5" os.family="RS">
      LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tL
      S0tLS0tLQpSUyA4MDAwIFN5c3RlbSBTb2Z0d2FyZSwgVmVyc2lvbiA5LjMuMC41ClJpdmVyc3RvbmUgTmV0d2
      9ya3MsIEluYy4sIENvcHlyaWdodCAoYykgMjAwMC0yMDA0LiBBbGwgcmlnaHRzIHJlc2VydmVkLgpTeXN0ZW0
      gc3RhcnRlZCBvbiAyMDE4LTEwLTExIDIyOjAyOjAzCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
      LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS4uLg==
    </example>
    <param pos="0" name="os.vendor" value="Riverstone"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="1" name="os.family"/>
    <param pos="2" name="os.product"/>
    <param pos="3" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^HP ([^\s]+) ProCurve Switch">
    <description>HP ProCurve Switch</description>
    <!-- ==============================================================================\nHP J4121A ProCurve Switch 4000M\n
    Firmware revision v2.2.3\n\nCopyright (C) 1991-2004 Hewlett-Packard Co. All Rights Reserved.\n\n
    RESTRICTED RIGHTS LEGEND\n\n Use, duplication, or disclosure by the Government is subject to restrictions\n\n
    as set forth in subdivision (b) (3) (ii) of the Rights in Technical Data and\n\nComputer Software clause at 52.227-7013.\n\n
    HEWLETT-PACKARD COMPANY, 3000 Hanover St., Palo Alto, CA 94303\n\n\nWe'd like to keep you up to date about:\n*
    Software feature updates\n* New product announcements\n* Special events\n\n\nPlease register your
    products now at: www.ProCurve.com\n==============================================================================\n
    \n\nUsername:  -->

    <example _encoding="base64" os.product="J4121A">
      PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09P
      T09PT09PT09PT09PT09PT09PT09PT09CkhQIEo0MTIxQSBQcm9DdXJ2ZSBTd2l0Y2ggNDAwME
      0KRmlybXdhcmUgcmV2aXNpb24gdjIuMi4zCgpDb3B5cmlnaHQgKEMpIDE5OTEtMjAwNCBIZXd
      sZXR0LVBhY2thcmQgQ28uIEFsbCBSaWdodHMgUmVzZXJ2ZWQuCgogICAgICAgICAgICAgICAg
      ICAgICAgICBSRVNUUklDVEVEIFJJR0hUUyBMRUdFTkQKCiBVc2UsIGR1cGxpY2F0aW9uLCBvc
      iBkaXNjbG9zdXJlIGJ5IHRoZSBHb3Zlcm5tZW50IGlzIHN1YmplY3QgdG8gcmVzdHJpY3Rpb2
      5zCiAKIGFzIHNldCBmb3J0aCBpbiBzdWJkaXZpc2lvbiAoYikgKDMpIChpaSkgb2YgdGhlIFJ
      pZ2h0cyBpbiBUZWNobmljYWwgRGF0YSBhbmQKIAogQ29tcHV0ZXIgU29mdHdhcmUgY2xhdXNl
      IGF0IDUyLjIyNy03MDEzLgoKICAgICAgSEVXTEVUVC1QQUNLQVJEIENPTVBBTlksIDMwMDAgS
      GFub3ZlciBTdC4sIFBhbG8gQWx0bywgQ0EgOTQzMDMKCiAgICAgICAgICAgICAgICAgICAgIC
      AgIApXZSdkIGxpa2UgdG8ga2VlcCB5b3UgdXAgdG8gZGF0ZSBhYm91dDoKICogU29mdHdhcmU
      gZmVhdHVyZSB1cGRhdGVzCiAqIE5ldyBwcm9kdWN0IGFubm91bmNlbWVudHMKICogU3BlY2lh
      bCBldmVudHMKCiAgICAgICAgICAgICAgICAgICAgICAgIApQbGVhc2UgcmVnaXN0ZXIgeW91c
      iBwcm9kdWN0cyBub3cgYXQ6IHd3dy5Qcm9DdXJ2ZS5jb20KPT09PT09PT09PT09PT09PT09PT
      09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0
      9PT09CgoKVXNlcm5hbWU6IA==
    </example>
    <param pos="0" name="os.vendor" value="HP"/>
    <param pos="0" name="os.family" value="ProCurve"/>
    <param pos="0" name="os.device" value="Switch"/>
    <param pos="1" name="os.product"/>
  </fingerprint>

  <fingerprint pattern="^(?m).*ConnectUPS">
    <description>PowerWare ConnectUPS</description>
    <!-- +============================================================================+\n|            [ ConnectUPS Web/SNMP
     Card Configuration Utility ]              |\n+============================================================================+\n
     \nEnter Password: -->

    <example _encoding="base64">
      Kz09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0
      9PT09PT09PT09PT09PT0rCnwgICAgICAgICAgICBbIENvbm5lY3RVUFMgV2ViL1NOTVAgQ2FyZCBDb25maW
      d1cmF0aW9uIFV0aWxpdHkgXSAgICAgICAgICAgICAgfAorPT09PT09PT09PT09PT09PT09PT09PT09PT09P
      T09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSsKCkVudGVyIFBhc3N3
      b3JkOiA=
    </example>
    <param pos="0" name="os.vendor" value="PowerWare"/>
    <param pos="0" name="os.family" value="ConnectUPS"/>
    <param pos="0" name="os.device" value="UPS"/>
    <param pos="0" name="os.product" value="ConnectUPS"/>
  </fingerprint>

  <fingerprint pattern="^Imagistics.*im">
    <description>an Imagistics device</description>
    <!-- Imagistics im3511/im4511 Ver 01.00.20 TELNET server.\nCopyright(c) 2001-2005, silex technology, Inc.\nlogin: -->

    <example _encoding="base64">
      SW1hZ2lzdGljcyBpbTM1MTEvaW00NTExIFZlciAwMS4wMC4yMCBURUxORVQgc2VydmVyLgpDb3B5cmlnaH
      QoYykgMjAwMS0yMDA1LCBzaWxleCB0ZWNobm9sb2d5LCBJbmMuCmxvZ2luOiA=
    </example>
    <param pos="0" name="os.vendor" value="Imagistics"/>
    <param pos="0" name="os.family" value="Imagistics"/>
    <param pos="0" name="os.device" value="Multifunction Device"/>
    <param pos="0" name="os.product" value="im"/>
  </fingerprint>

  <fingerprint pattern="^NRG Maintenance Shell">
    <description>a Ricoh NRG device</description>
    <!-- NRG Maintenance Shell.   \nUser access verification.\nlogin: -->

    <example _encoding="base64">
      TlJHIE1haW50ZW5hbmNlIFNoZWxsLiAgIAoKVXNlciBhY2Nlc3MgdmVyaWZpY2F0aW9uLgoKbG9naW46
    </example>
    <param pos="0" name="os.vendor" value="Ricoh"/>
    <param pos="0" name="os.device" value="Printer"/>
    <param pos="0" name="os.product" value="NRG Printer"/>
  </fingerprint>

  <fingerprint pattern="^SHARP (AR-[^\\s]+) Ver ([^\\s]+) TELNET server">
    <description>SHARP AR Series multifunction device</description>
    <!-- SHARP AR-M351U Ver 01.00.18 TELNET server.\nCopyright(c) 2001-2005, silex technology, Inc.\nlogin: -->

    <example _encoding="base64" os.product="AR-M351U" os.version="01.00.18">
      U0hBUlAgQVItTTM1MVUgVmVyIDAxLjAwLjE4IFRFTE5FVCBzZXJ2ZXIuCkNvcHlyaWdodChjKSAyMDAx
      LTIwMDUsIHNpbGV4IHRlY2hub2xvZ3ksIEluYy4KbG9naW46IA==
    </example>
    <param pos="0" name="os.vendor" value="Sharp"/>
    <param pos="0" name="os.family" value="Sharp AR Series"/>
    <param pos="0" name="os.device" value="Multifunction Device"/>
    <param pos="1" name="os.product"/>
    <param pos="2" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^SHARP (MX-[^\\s]+) Ver ([^\\s]+) TELNET server">
    <description>SHARP MX Series multifunction device</description>
    <!-- SHARP MX-3610N Ver 01.05.00.0o.18 TELNET server.\nCopyright(C) 2005-     SHARP CORPORATION\nCopyright(C) 2005-
    silex technology, Inc.\nlogin:  -->

    <example _encoding="base64" os.product="MX-3610N" os.version="01.05.00.0o.18">
      U0hBUlAgTVgtMzYxME4gVmVyIDAxLjA1LjAwLjBvLjE4IFRFTE5FVCBzZXJ2ZXIuCkNvcHlyaWdodC
      hDKSAyMDA1LSAgICAgU0hBUlAgQ09SUE9SQVRJT04KQ29weXJpZ2h0KEMpIDIwMDUtICAgICBzaWxl
      eCB0ZWNobm9sb2d5LCBJbmMuCmxvZ2luOiA=
    </example>
    <param pos="0" name="os.vendor" value="Sharp"/>
    <param pos="0" name="os.family" value="Sharp MX Series"/>
    <param pos="0" name="os.device" value="Multifunction Device"/>
    <param pos="1" name="os.product"/>
    <param pos="2" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^(?m).*Welcome to MELCO Print Server.*Server Name *: *([^ ]*)\W.*Server Model *: *([^ ]*).*F \/ W Version *: *([^ ]*).*MAC Address *: *(.. .. .. .. .. ..).*$">
    <description>System is a Buffalo/MELCO Embedded Print Server</description>
    <!-- ***********************************\n* Welcome to MELCO Print Server *\n* Telnet Console *\n***********************************
    \n \nServer Name: PS-B04E8E\nServer Model: LPV 2 - TX 1\nF / W Version: 2.00 J \nMAC Address: AE 32 EA 21 BB E3\n
    Uptime: 0 days, 00: 00: 12\n \nPlease Enter Password:"-->

    <example _encoding="base64" os.version="2.00" host.id="PS-B04E8E" os.model="LPV" os.address="AE 32 EA 21 BB E3">
      KioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKipcbiogV2VsY29tZSB0byBNRUxDTyBQc
      mludCBTZXJ2ZXIgKlxuKiBUZWxuZXQgQ29uc29sZSAqXG4qKioqKioqKioqKioqKioqKioqKioqKi
      oqKioqKioqKioqKlxuIFxuU2VydmVyIE5hbWU6IFBTLUIwNEU4RVxuU2VydmVyIE1vZGVsOiBMUFY
      gMiAtIFRYIDFcbkYgLyBXIFZlcnNpb246IDIuMDAgSiBcbk1BQyBBZGRyZXNzOiBBRSAzMiBFQSAy
      MSBCQiBFM1xuVXB0aW1lOiAwIGRheXMsIDAwOiAwMDogMTJcbiBcblBsZWFzZSBFbnRlciBQYXNzd
      29yZDoi
    </example>
    <param pos="0" name="os.vendor" value="Buffalo"/>
    <param pos="0" name="os.family" value="PrintServer"/>
    <param pos="0" name="os.device" value="Printer"/>
    <param pos="1" name="host.id"/>
    <param pos="2" name="os.model"/>
    <param pos="3" name="os.version"/>
    <param pos="4" name="os.address"/>
  </fingerprint>

  <fingerprint pattern="^(?m)AIX Version\W(\d).*">
    <description>System is IBM AIX v</description>
    <!-- AIX Version 6\nCopyright IBM Corporation, 1982, 2007.\nlogin: -->

    <example _encoding="base64" os.version="6">
      QUlYIFZlcnNpb24gNgpDb3B5cmlnaHQgSUJNIENvcnBvcmF0aW9uLCAxOTgyLCAyMDA3Lgpsb2dpbjogCg==
    </example>
    <param pos="0" name="os.vendor" value="IBM"/>
    <param pos="0" name="os.family" value="AIX"/>
    <param pos="0" name="os.product" value="AIX"/>
    <param pos="1" name="os.version"/>
    <param pos="0" name="os.cpe23" value="cpe:/o:ibm:aix:{os.version}"/>
  </fingerprint>

  <fingerprint pattern="^(?m)CIMC Debug Firmware Utility Shell\W([^\s]+).*">
    <description>System is Cisco UCS Device</description>
    <!-- CIMC Debug Firmware Utility Shell\nfake-ucs-device-3-1-p login: -->

    <example _encoding="base64" host.name="fake-ucs-device-3-1-p">
      Q0lNQyBEZWJ1ZyBGaXJtd2FyZSBVdGlsaXR5IFNoZWxsCmZha2UtdWNzLWRldmljZS0zLTEtcCBsb2dpbjogCg==
    </example>
    <param pos="0" name="os.vendor" value="Cisco"/>
    <param pos="0" name="os.family" value="UCS"/>
    <param pos="0" name="os.device" value="Network Management Device"/>
    <param pos="0" name="os.product" value="UCS Device"/>
    <param pos="1" name="host.name"/>
  </fingerprint>

  <fingerprint pattern="^(?m)HP ProLiant.*v(\d+.\d+)">
    <description>Sytem is HP ProLiant server</description>
    <!-- HP ProLiant BL e-Class Integrated Administrator v2.00
         Copyright 2005 Hewlett-Packard Development Group, L.P.
         WARNING: This is a private system.  Do not attempt to login unless you are an
         authorized user.  Any authorized or unauthorized access and use may be moni-
         tored and can result in criminal or civil prosecution under applicable law.
         IA-00508BEBAA59 login: -->

    <example _encoding="base64" os.version="2.00">
      SFAgUHJvTGlhbnQgQkwgZS1DbGFzcyBJbnRlZ3JhdGVkIEFkbWluaXN0cmF0b3IgdjIuMDAKICAgICAgI
      CAgQ29weXJpZ2h0IDIwMDUgSGV3bGV0dC1QYWNrYXJkIERldmVsb3BtZW50IEdyb3VwLCBMLlAuCgogIC
      AgICAgICAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0
      tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogICAgICAgICBXQVJOSU5HOiBUaGlzIGlzIGEgcHJpdmF0ZSBz
      eXN0ZW0uICBEbyBub3QgYXR0ZW1wdCB0byBsb2dpbiB1bmxlc3MgeW91IGFyZSBhbgogICAgICAgICBhd
      XRob3JpemVkIHVzZXIuICBBbnkgYXV0aG9yaXplZCBvciB1bmF1dGhvcml6ZWQgYWNjZXNzIGFuZCB1c2
      UgbWF5IGJlIG1vbmktCiAgICAgICAgIHRvcmVkIGFuZCBjYW4gcmVzdWx0IGluIGNyaW1pbmFsIG9yIGN
      pdmlsIHByb3NlY3V0aW9uIHVuZGVyIGFwcGxpY2FibGUgbGF3LgogICAgICAgICAtLS0tLS0tLS0tLS0t
      LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tL
      S0tLQoKCiAgICAgICAgIElBLTAwNTA4QkVCQUE1OSBsb2dpbjo=
    </example>
    <param pos="0" name="os.vendor" value="HP"/>
    <param pos="0" name="os.family" value="ProLiant"/>
    <param pos="0" name="os.product" value="ProLiant"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^Power Measurement Ltd. Meter ION ([[:alnum:]]+)">
    <!-- Power Measurement Ltd. Meter ION 7330V271 ETH ETH7330V272
         Serial#: PB-0204A058-11
         login: -->

    <description>Power Measurement ION Power Meter</description>
    <example _encoding="base64" hw.vendor="Power Measurement Ltd." hw.family="ION" hw.version="7330V271">
      UG93ZXIgTWVhc3VyZW1lbnQgTHRkLiBNZXRlciBJT04gNzMzMFYyNzEgRVRIIEVUSDczMzBWMjcyCg1TZ
      XJpYWwjOiBQQi0wMjA0QTA1OC0xMQoNCg1sb2dpbjo=
    </example>
    <param pos="0" name="hw.vendor" value="Power Measurement Ltd."/>
    <param pos="0" name="hw.family" value="ION"/>
    <param pos="1" name="hw.version"/>
  </fingerprint>

  <fingerprint pattern="^GW25 v([[:digit:]\.]+) - Intelligent Power Meters GPRS Gateway[[:space:]]+Developed by Satelitech">
    <!-- GW25 v1.2.1 - Intelligent Power Meters GPRS Gateway
         Developed by Satelitech S.A for ESG Dilec
         Enter password: -->

    <description>Satelitech Power Meter</description>
    <example _encoding="base64" hw.vendor="Satelitech" hw.family="GW25" hw.version="1.2.1">
      R1cyNSB2MS4yLjEgLSBJbnRlbGxpZ2VudCBQb3dlciBNZXRlcnMgR1BSUyBHYXRld2F5Cg1EZXZlbG9wZ
      WQgYnkgU2F0ZWxpdGVjaCBTLkEgZm9yIEVTRyBEaWxlYwoNRW50ZXIgcGFzc3dvcmQ6
    </example>
    <param pos="0" name="hw.vendor" value="Satelitech"/>
    <param pos="0" name="hw.family" value="GW25"/>
    <param pos="1" name="hw.version"/>
  </fingerprint>

  <fingerprint pattern="^RDK \(A Yocto Project based Distro\) ([^ ]+) (?:Docsis-Gateway|Business)">
    <description>DOCSIS Cable Modem Running RDK</description>
    <!-- RDK (A Yocto Project based Distro) 2.0 Docsis-Gateway
         Docsis-Gateway login: -->

    <example _encoding="base64" hw.device="DOCSIS Cable Modem" os.vendor="Yocto" os.product="RDK" os.version="2.0">
      UkRLIChBIFlvY3RvIFByb2plY3QgYmFzZWQgRGlzdHJvKSAyLjAgRG9jc2lzLUdhdGV3YXkNC
      g0NCg1Eb2NzaXMtR2F0ZXdheSBsb2dpbjo=
    </example>
    <!-- RDK (A Yocto Project based Distro) 2.0 Business\r\n\r\r\n\rBusiness login: -->

    <example _encoding="base64" hw.device="DOCSIS Cable Modem" os.vendor="Yocto" os.product="RDK" os.version="2.0">
      UkRLIChBIFlvY3RvIFByb2plY3QgYmFzZWQgRGlzdHJvKSAyLjAgQnVzaW5lc3MNCg0NCg1Cd
      XNpbmVzcyBsb2dpbjoK
    </example>
    <param pos="0" name="hw.device" value="DOCSIS Cable Modem"/>
    <param pos="0" name="os.vendor" value="Yocto"/>
    <param pos="0" name="os.product" value="RDK"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^RICOH Maintenance Shell">
    <description>a Ricoh device</description>
    <!-- RICOH Maintenance Shell.
         User access verification.
         login:-->

    <example _encoding="base64">
      UklDT0ggTWFpbnRlbmFuY2UgU2hlbGwuICAgCg1Vc2VyIGFjY2VzcyB2ZXJpZmljYXRpb24uCg1sb2dpbjo=
    </example>
    <param pos="0" name="os.vendor" value="Ricoh"/>
    <param pos="0" name="os.device" value="Printer"/>
  </fingerprint>

  <fingerprint pattern="Precise/RTCS v([\d\.]+) Telnet server">
    <description>Liebert UPS</description>
    <!-- Precise/RTCS v2.90.00 Telnet server
         Service Port Manager Active
        <Esc> Ends Session
    -->

    <example _encoding="base64" os.version="2.90.00">
      UHJlY2lzZS9SVENTIHYyLjkwLjAwIFRlbG5ldCBzZXJ2ZXIKCgpTZXJ2aWNlIFBvcnQgTWFuYWdlciBBY3RpdmUKCjxFc2M+IEVuZHMgU2Vzc2lvbgoKroot
    </example>
    <param pos="0" name="hw.device" value="Power Device"/>
    <param pos="0" name="hw.vendor" value="Liebert"/>
    <param pos="0" name="os.device" value="Power Device"/>
    <param pos="0" name="os.vendor" value="Liebert"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^KeeneticOS version ([\w.-]+), copyright">
    <description>Keentic KeeneticOS</description>
    <!-- KeeneticOS version 3.04.C.6.0-0, copyright (c) 2010-2020 Keenetic Ltd.\r\n\r\nLogin: -->

    <example _encoding="base64" os.version="3.04.C.6.0-0">
      S2VlbmV0aWNPUyB2ZXJzaW9uIDMuMDQuQy42LjAtMCwgY29weXJpZ2h0IChjKSAyMDEwLTIwM
      jAgS2VlbmV0aWMgTHRkLg0KDQpMb2dpbjoK
    </example>
    <param pos="0" name="hw.device" value="Router"/>
    <param pos="0" name="hw.vendor" value="Keenetic"/>
    <param pos="0" name="os.device" value="Router"/>
    <param pos="0" name="os.vendor" value="Keenetic"/>
    <param pos="0" name="os.product" value="KeeneticOS"/>
    <param pos="1" name="os.version"/>
  </fingerprint>

  <fingerprint pattern="^\**(?:\r|\n)+\* Copyright \(c\) \d\d\d\d-\d\d\d\d New H3C Technologies Co., Ltd. All rights reserved.\*(?:\r|\n)+\* Without the owner's prior written consent,\s+\*(?:\r|\n)+\* no decompiling or reverse-engineering shall be allowed.\s+\*(?:\r|\n)+\*+(?:\r|\n)+login:\s*$">
    <description>Generic H3C Technologies banner</description>
    <!-- ******************************************************************************\r\n* Copyright (c) 2004-2017 New H3C Technologies Co., Ltd. All rights reserved.*\r\n* Without the owner's prior written consent,                                 *\r\n* no decompiling or reverse-engineering shall be allowed.                    *\r\n******************************************************************************\r\n\r\nlogin: -->

    <example _encoding="base64">
      KioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqK
      ioqKioqKioqKioqKioqKioqKioqKioqDQoqIENvcHlyaWdodCAoYykgMjAwNC0yMDE3IE5ldy
      BIM0MgVGVjaG5vbG9naWVzIENvLiwgTHRkLiBBbGwgcmlnaHRzIHJlc2VydmVkLioNCiogV2l
      0aG91dCB0aGUgb3duZXIncyBwcmlvciB3cml0dGVuIGNvbnNlbnQsICAgICAgICAgICAgICAg
      ICAgICAgICAgICAgICAgICAgKg0KKiBubyBkZWNvbXBpbGluZyBvciByZXZlcnNlLWVuZ2luZ
      WVyaW5nIHNoYWxsIGJlIGFsbG93ZWQuICAgICAgICAgICAgICAgICAgICAqDQoqKioqKioqKi
      oqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKio
      qKioqKioqKioqKioqKioNCg0KbG9naW46Cg==
    </example>
    <param pos="0" name="hw.vendor" value="H3C"/>
    <param pos="0" name="os.vendor" value="H3C"/>
  </fingerprint>

  <fingerprint pattern="Telnet Administration (?:\r|\n)+   SAP J2EE Engine v([\d.]+)(?:\r|\n)+">
    <description>SAP NetWeaver Application Server Java telnet service</description>
    <!-- ***********************************************
         **********************************************
         ****###*******####*****#######**************
         **##***##****##**##****##****##************
         ***##*******##****##***##****##**********
         *****##*****########***######***********
         ******##****##****##***##*************
         **##***##**##******##**##************
         ****###****##******##**##**********
         **********************************
         ********************************
         Telnet Administration
         SAP J2EE Engine v7.00
      Login:
    -->

    <example _encoding="base64" service.version="7.00">
      KioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKiogCiAgICoqKi
      oqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKiogCiAgICoqKiojIyMq
      KioqKioqIyMjIyoqKioqIyMjIyMjIyoqKioqKioqKioqKioqIAogICAqKiMjKioqIyMqKioqIy
      MqKiMjKioqKiMjKioqKiMjKioqKioqKioqKioqIAogICAqKiojIyoqKioqKiojIyoqKiojIyoq
      KiMjKioqKiMjKioqKioqKioqKiAKICAgKioqKiojIyoqKioqIyMjIyMjIyMqKiojIyMjIyMqKi
      oqKioqKioqKiAKICAgKioqKioqIyMqKioqIyMqKioqIyMqKiojIyoqKioqKioqKioqKiogCiAg
      ICoqIyMqKiojIyoqIyMqKioqKiojIyoqIyMqKioqKioqKioqKiogCiAgICoqKiojIyMqKioqIy
      MqKioqKiojIyoqIyMqKioqKioqKioqIAogICAqKioqKioqKioqKioqKioqKioqKioqKioqKioq
      KioqKioqIAogICAqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKiAKCiAgIFRlbG5ldC
      BBZG1pbmlzdHJhdGlvbiAKICAgU0FQIEoyRUUgRW5naW5lIHY3LjAwCgoKCkxvZ2luOgo=
    </example>
    <param pos="0" name="service.vendor" value="SAP"/>
    <param pos="0" name="service.product" value="NetWeaver Application Server Java"/>
    <param pos="0" name="service.family" value="NetWeaver"/>
    <param pos="1" name="service.version"/>
    <param pos="0" name="service.cpe23" value="cpe:/a:sap:netweaver_application_server_java:{service.version}"/>
    <param pos="0" name="service.component.vendor" value="SAP"/>
    <param pos="0" name="service.component.product" value="NetWeaver Application Server"/>
    <param pos="0" name="service.component.cpe23" value="cpe:/a:sap:netweaver_application_server:-"/>
  </fingerprint>

  <fingerprint pattern="Telnet Administration (?:\r|\n)+   SAP Java EE Application Server v([\d.]+)(?:\r|\n)+">
    <description>SAP NetWeaver Application Server Java telnet service - newer variant</description>
    <!-- ***********************************************
         **********************************************
         ****###*******####*****#######**************
         **##***##****##**##****##****##************
         ***##*******##****##***##****##**********
         *****##*****########***######***********
         ******##****##****##***##*************
         **##***##**##******##**##************
         ****###****##******##**##**********
         **********************************
         ********************************
         Telnet Administration
         SAP Java EE Application Server v7.50
      User name:
    -->

    <example _encoding="base64" service.version="7.50">
      KioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKiogCiAgICoqKi
      oqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKiogCiAgICoqKiojIyMq
      KioqKioqIyMjIyoqKioqIyMjIyMjIyoqKioqKioqKioqKioqIAogICAqKiMjKioqIyMqKioqIy
      MqKiMjKioqKiMjKioqKiMjKioqKioqKioqKioqIAogICAqKiojIyoqKioqKiojIyoqKiojIyoq
      KiMjKioqKiMjKioqKioqKioqKiAKICAgKioqKiojIyoqKioqIyMjIyMjIyMqKiojIyMjIyMqKi
      oqKioqKioqKiAKICAgKioqKioqIyMqKioqIyMqKioqIyMqKiojIyoqKioqKioqKioqKiogCiAg
      ICoqIyMqKiojIyoqIyMqKioqKiojIyoqIyMqKioqKioqKioqKiogCiAgICoqKiojIyMqKioqIy
      MqKioqKiojIyoqIyMqKioqKioqKioqIAogICAqKioqKioqKioqKioqKioqKioqKioqKioqKioq
      KioqKioqIAogICAqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKiAKCiAgIFRlbG5ldC
      BBZG1pbmlzdHJhdGlvbiAKICAgU0FQIEphdmEgRUUgQXBwbGljYXRpb24gU2VydmVyIHY3LjUw
      CgoKVXNlciBuYW1lOgo=
    </example>
    <param pos="0" name="service.vendor" value="SAP"/>
    <param pos="0" name="service.product" value="NetWeaver Application Server Java"/>
    <param pos="0" name="service.family" value="NetWeaver"/>
    <param pos="1" name="service.version"/>
    <param pos="0" name="service.cpe23" value="cpe:/a:sap:netweaver_application_server_java:{service.version}"/>
    <param pos="0" name="service.component.vendor" value="SAP"/>
    <param pos="0" name="service.component.product" value="NetWeaver Application Server"/>
    <param pos="0" name="service.component.cpe23" value="cpe:/a:sap:netweaver_application_server:-"/>
  </fingerprint>

  <fingerprint pattern="^(?:\r|\n|\s)*UDP/TCP/IP Stack: ACT Video security">
    <description>ACT Security IP Cameras</description>
    <!--
      UDP/TCP/IP Stack: ACT Video security\r\n
      V5.8\r\n
      Welcome connection : 192.168.0.1:61300\r\n
      \r\n
      Password:
    -->

    <example _encoding="base64">
      VURQL1RDUC9JUCBTdGFjazogQUNUIFZpZGVvIHNlY3VyaXR5DQpWNS44DQpX
      ZWxjb21lIGNvbm5lY3Rpb24gOiAxOTIuMTY4LjAuMTo2MTMwMA0KDQpQYXNz
      d29yZDog
    </example>
    <param pos="0" name="hw.vendor" value="ACT Security"/>
    <param pos="0" name="hw.device" value="IP Camera"/>
  </fingerprint>

</fingerprints>'''

f = open("banners.txt", "w")
res = re.findall(r'<!--(.*?)-->', text, flags=re.DOTALL)
for x in res:
    print(repr(x))
    f.write(repr(x.strip()))
    f.write('\n')
f.close()
print(res)
