IP_proxy搭建IP代理池
===
项目特点：
---
1. 免费IP代理
2. 定时检测，采集
3. 提供网站API

采集流程
---
1. 获取IP。
2. 检测IP，并放入redis队列。
3. 定时检测IP的数量和有效性。
4. 利用flask建立API接口


项目运行:
---
1. 安装所需的模块
   pip install requirement
 另外，本机需安装redis数据库服务。
2. 运行run.py,开始采集IP。
3. 运行api.py,搭建网站API接口。
