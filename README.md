# log_demo
This is a demo about log which include log collection Agent，Server .  
Feature :  
1 Hard link promise agent collect the log untill all log collection finish .  
2 Sync write collection's offset promise that agent recover from the lastest collection step .  
V1.1 new feature:
1 Optimize the network part to improve the performance.
2 Server log demo collect all logs into one file to using sequential write so that improve the performance.
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

#中文版设计稿
https://www.jianshu.com/p/6a03ba897e04
