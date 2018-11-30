# log_demo
This is a demo about log which include log collection Agent，Server .  
Feature :  
1. Hard link promise agent collect the log untill all log collection finish .  
2. Sync write collection's offset promise that agent recover from the lastest collection step .  

V1.1 new feature:  
1. Optimize the network part to improve the performance.  
2. Server log demo collect all logs into one file to using sequential write so that improve the performance.  
Problem:    
1 The agent push each record more than one time, not exactly one (case by thread shutdown before sync write the check_point.) .     
# How to use?  
./script/tcp_agent to config Agent .  
./conf/agentconf can config the server ip, collect which log file ,collect type by regex expression .  
./script/tcp_server config the server which accept the data collect from agent.  
./conf/agentconf can config the server detail.  
# How to start   
The step are as follow:  
1. Config all the ./conf file .  
2. Start the ./script/tcp_server first.  
3. Run the ./script/tcp_agent .  

#详细中文版设计稿
https://www.jianshu.com/p/6a03ba897e04（2018//11/30号更新，最新版本为稳定版本。）  
日志收集Agent, 包括一个简单的Server作为Demo展示（后续考虑对接类似Kafka等环境）。  
特性：  
Agent：  
1. 利用硬连接保证Agent日志直至收集完成，文件才会被系统回收。  
2. 利用同步写的机制，保证Agent恢复能够回到上一次收集的地方。 
3. 一次性读入4K大小的文件块进行收集处理，让短日志获得跟正常日志同样的性能。  

~~4. 引入压缩。~~  

Server:  
1. 组合多个Topic，写入同一文件中，利用顺序写，获得最大写性能。 

~~2. 引入压缩。~~   

未来特性：
1. 配置热加载，利用reload。
2. 完整的进程管理，supervisor实现。
3. 独立的写进程，进一步提高多磁盘性能（埋下一个坑）。
