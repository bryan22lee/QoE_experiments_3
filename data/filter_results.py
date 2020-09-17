import numpy as np
import re
import os
import sys
import subprocess

rej_attentions_check = 0
rej_active_video_time_check = 0
rej_rating_times_check = 0

#Sample filter function
def filter_single_video(active_video_times, rating_times, video_order, scores, attentions):
    global rej_attentions_check
    global rej_active_video_time_check
    global rej_rating_times_check
    #First check if user watching aligns with video length
    #0.5 sec tolerance for black screen at the end
        # ret = 0
        # bad = 0
    violate = 0
    if attentions[0] != 0:
        rej_attentions_check += 1
        violate += 1

    for i, j in zip(active_video_times, rating_times):
        if i < 3.5:
            rej_active_video_time_check += 1
            violate += 1
        elif j <= 1000:
            rej_rating_times_check += 1
            violate += 1

    if violate > 0:
        return 1
    return 0 #We don't move this user to rejected folder

#Parse data from user result file 
def parse_results(lines):
    # video_times = list(map(int,lines[2].strip().split(','))) #read times spent on each video
    active_video_times = list(map(float,lines[3].strip().split(','))) #read active time on video page
    rating_times = list(map(int,lines[4].strip().split(','))) #read times spent on each rating  
    # video_times = []; rating_times = []
    video_order = list(map(int,lines[1].strip().split(','))) #read the video order seen by the surveyee
    scores = list(map(int,lines[0].strip().split(','))) #read scores
    attentions = list(map(int,lines[-1].strip().split(','))) #attention checks    
    return active_video_times, rating_times, video_order, scores, attentions


#input from the cmd line script
result_path = '../results/'
#white_list = '../good/'


move = False
result_files = os.listdir(result_path)
#white_list_files = os.listdir(white_list)

total = 0
approved = 0
reject = 0
pending = 0
for result_file in result_files:
    #filter a single result
    total +=1
    '''
    if result_file in white_list_files:
        approved +=1
        continue
    '''
    result = result_path + result_file
    with open(result, "r") as fp:
        lines = fp.readlines()
        move = False

        #insert customized filter here 
        move = filter_single_video(*parse_results(lines))
        if move == 1:
            reject +=1
            print(result_file)
            os.system("mv {} ../rejected_results/".format(result))
        elif move == 2:
            pending +=1
            os.system("mv {} ../pending/".format(result))
        else:
            approved +=1

print('reject:',reject)
print('approved:',approved)
print('rejection ratio:', reject/(reject+approved))

print('Number of results rejected by attention check: '+str(rej_attentions_check))
print('Number of results rejected due to insufficient active video time: '+str(rej_active_video_time_check))
print('Number of results rejected due to insufficient rating time: '+str(rej_rating_times_check))