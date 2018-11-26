# log_demo
This is a demo about log which include log collect agent .  
Feature :  
1 Hard link to promise agent collect the log untill all log collect finish .  
2 Sync log write to promise agent recover from the lastest collection step .  
Problem:  
1 The agent push data in at last one not exactly one (case by shutdown before sync write the check_point) .   
# How to use?  
./script/tcp_agent is the agent .  
./conf/agentconf can conf the server ip, collect which log file ,collect type by regex expression .  
./script/tcp_server is the server which accept the data collect from agent.  
./conf/agentconf can conf the server detail.  
# How to start   
The step are as follow:  
1. Config the ./conf file .  
2. Start the ./script/tcp_server first.  
3. Run the ./script/tcp_agent .  
