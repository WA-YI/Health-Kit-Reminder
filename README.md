# Health-Kit-Reminder
北京健康宝核酸机器人提醒，通过北京通App Token请求核酸数据，在第3天通过企业微信机器人发送提醒。

# 使用教程

## 所需材料

- 一台能运行Python 3的操作环境（电脑或虚拟机等）
- 一台能运行北京通App的操作环境（手机或模拟器等）
- 一个用于通知企业微信应用，或Server酱或其他
- 稳定的网络连接

## 1. 脚本配置

1. 利用Windows或Mac安装Charles、Fiddler等抓包软件，开启对手机的抓包。

    具体教程可参考[这篇文章](https://www.361shipin.com/blog/1535700403713212416)

2. 在手机端登录北京通App，打开北京健康宝小程序。

3. 读取PC端抓包软件中路径为/renzheng/open/auth/authorize开头的请求，检查请求URL参数中的personToken字段，复制字段值，如下图。

    ![抓包软件与位置截图](https://github.com/WA-YI/Health-Kit-Reminder/blob/Additional/ScreenShot-2022-07-28-230515.png?raw=true)

4. 将复制出来的字段粘贴至`index.py`第13行的personToken字段中即可。

## 2. 通知配置

    该步骤可修改为自定义通知渠道，以下仅以企业微信为例。

1. 申请企业微信，具体教程可参考[这篇文章](https://www.jianshu.com/p/182ea14af3f2)

2. 将教程中的`corpid`、`agentid`和`corpsecret`填入脚本的第10~12行即可。

Extra1. 如有需要，可以将消息发送给指定企业微信成员。在企业微信后台的“通讯录”菜单 > 成员资料，将昵称下的账号ID复制至脚本第73行的`touser`字段即可。

Extra2. 本脚本默认核酸3天时提醒，若需自定义可修改第60行处的代码天数。

## 3. 触发配置

检查与通知脚本配置完毕后，需要配置定时运行规则。目前主流云函数或Linux的Corn命令即可。例如`corn(0 16 * * *)`即为每天16点运行。

利用`python3 index.py`命令手动运行脚本也可以进行一次检查，若未满3天则返回具体天数，不发送通知。

# 效果展示

![通知提示格式](https://raw.githubusercontent.com/WA-YI/Health-Kit-Reminder/Additional/Screenshot-2022-07-29-02-21-30.jpg)

<center>通知提示格式</center>

![通知提示格式](https://raw.githubusercontent.com/WA-YI/Health-Kit-Reminder/Additional/Screenshot-2022-07-29-02-21-46.jpg?)

<center>运行返回格式</center>

# 附加说明

由于北京健康宝的贵物算法，加上本人太懒了，当日6点前的核算结果会算作1天的机制并没做特殊判断，此脚本检测时仍会返回0天，请留意。





