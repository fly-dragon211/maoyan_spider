#!/bin/bash
# /opt/linuxsir/hadoop/bin/hadoop_map_reduce_py.sh

# 删除HDFS文件
cd /opt/linuxsir/hadoop/bin
./hdfs dfs -rm /output/*
./hdfs dfs -rmdir /output


hadoop jar /opt/linuxsir/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar \
 -files 'mapper.py, reducer.py' \
 -input /input/readme.txt \
 -output /output \
 -mapper mapper.py \
 -reducer reducer.py