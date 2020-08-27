import numpy as np
import re
import os
import sys
import subprocess

#Attention check: returns 1 if fail, 0 if success
def attention_check(video_times, rating_times, video_order, scores, attentions):
    #First check if user watching aligns with video length
    #0.5 sec tolerance for black screen at the end
    violate = 0
    if attentions[0] != 2 :
        violate +=1
    if attentions[1] != 5 or attentions[3] != 5:
        violate +=1
    if attentions[2] != 5:
        if attentions[2] == 4: # stall and no blur
            violate += 1
        else:
            return 1 # fail (move to rejected folder)
    if violate >= 2:
        return 1
    return 0 #We don't move this user to rejected folder

#Sample filter function - check lengths, scores
def filter_single_video(lengths, video_times, rating_times, video_order, scores, attentions):
    #First check attention
    if attention_check(video_times, rating_times, video_order, scores, attentions) == 0:
        #Next check if user watching aligns with video length
        #0.5 sec tolerance for black screen at the end
        for i in range(len(lengths)):
            if (lengths[i] - 0.5> video_times[i]):
                return True

        #Then check if key moment has least score 
        #suppose key moment is video 0
        if min(scores) > scores[0]:
            return True

        #Then check if original video (#1) has highest score 
        if max(scores) < scores[1]:
            return True
        
        #Then check if key moment is lower than orig vid
        if scores[0] >= scores[1]:
            return True
        
        return False #We don't move this user to rejected folder
    return True #We move this user to rejected folder

#Parse data from user result file 
def parse_results(lines):
    video_times = list(map(int,lines[2].strip().split(','))) #read times spent on each video  
    rating_times = list(map(int,lines[3].strip().split(','))) #read times spent on each rating  
    video_order = list(map(int,lines[1].strip().split(','))) #read the video order seen by the surveyee
    scores = list(map(int,lines[0].strip().split(','))) #read scores
    attentions = list(map(int,lines[-1].strip().split(','))) #attention checks  

    return video_times, rating_times, video_order, scores, attentions

#get video length
def getLength(filename):
    result = subprocess.Popen(["ffprobe", filename], universal_newlines=True, 
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    temp = result.stdout.readlines()
    line = [x for x in temp if "Duration" in x][0]
    words = re.split(r'[ ,\n]', line)
    duration = words[3]
    splits = re.split(r'[ :,.\n]', duration)
    hours = int(splits[0])
    mins = int(splits[1])
    secs = int(splits[2])
    tenths = int(splits[3])
    tot = ((((hours * 60 + mins) * 60) + secs) * 1000) + tenths * 10
    return tot

#input from the cmd line script
result_path, reject_path, vid_path = sys.argv[-1], sys.argv[-2], sys.argv[-3]

list_dir = os.listdir(vid_path)
lengths = [] #actual video lengths
for vid in list_dir:
    if vid.endswith(".mp4"):
        full_vid_path = vid_path + "/" + vid
        lengths.append(getLength(full_vid_path)) 

move = False
result_files = os.listdir(result_path)


for result_file in result_files:
    print(result_file)
    #filter a single result
    result = result_path + "/" + result_file
    with open(result, "r") as fp:
        lines = fp.readlines()
        move = False

        #insert customized filter here 
        move = filter_single_video(lengths,*parse_results(lines))
        if move:
            os.system("mv {} ../rejected_results".format(result))
