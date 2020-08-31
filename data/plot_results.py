import sys
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from scipy.stats import t
import read_results as rr

# Require a name to name plots and log
args = len(sys.argv) - 2 if sys.argv[0] == "python" else len(sys.argv) - 1

if args != 1:
    print("please enter one argument as the name of the plots")
    exit(0)

inp = sys.argv[-1]
plot_name = inp + "_plot.png"
z_name = inp + "_standardized_plot.png"
log_name = inp + "_results.log"
header = "LOG OF " + inp + " SURVEY RESULTS\n\n"

# x axis configuration
#x = np.array([2, 4])
x = ["best", "worst", "1", "2"]
x_label = "buffered videos in incremental order"

# Function to standardize scores
def zscore(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    mns = a.mean(axis=axis)
    sstd = a.std(axis=axis, ddof=ddof)
    if axis and mns.ndim < a.ndim:
        res = ((a - np.expand_dims(mns, axis=axis)) /
        np.expand_dims(sstd, axis=axis))
    else:
        res = (a - mns) / sstd
    return np.nan_to_num(res)

# Helpers to sort results
def count_device(dev, arr):
    if dev == "Desktop":
        arr[0] += 1
    elif dev == "Laptop":
        arr[1] += 1
    elif dev == "Tablet":
        arr[2] += 1
    elif dev == "Smart phone":
        arr[3] += 1
    elif dev == "Other device":
        arr[4] += 1

def count_age(age, arr):
    if age == "18 - 24":
        arr[0] += 1
    elif age == "25 - 31":
        arr[1] += 1
    elif age == "32 - 38":
        arr[2] += 1
    elif age == "39 - 45":
        arr[3] += 1
    elif age == "46 - 52":
        arr[4] += 1
    elif age == "53 - 59":
        arr[5] += 1
    elif age == "60 and above":
        arr[6] += 1

def count_network(net, arr):
    if net == "WiFi":
        arr[0] += 1
    elif net == "Cable network":
        arr[1] += 1
    elif net == "Cellular network":
        arr[2] += 1
    elif net == "Other":
        arr[3] += 1

# Reading the results
res_path = "../results"
rej_path = "../rejected_results"
res = rr.get_results(res_path, inp)
rej_res = rr.get_results(rej_path, inp)

# function to sort results into corresponding lists
def sort_results(res, grade_list, order_list, vid_time_list, grade_time_list, user_reason_list, device_arr, age_arr, network_arr):
    for user in res:
        if user == []:
            continue
        grade_list.append(user[0])
        order_list.append(user[1])
        vid_time_list.append(user[2])
        grade_time_list.append(user[3])
        count_device(user[5], device_arr)
        count_age(user[6], age_arr)
        count_network(user[7], network_arr)
        # make a pair of userID and reason
        pair = [user[4], user[8]]
        user_reason_list.append(pair)

grade_list = []
rej_grade_list = []
order_list = []
rej_order_list = []
vid_time_list = []
rej_vid_time_list = []
grade_time_list = []
rej_grade_time_list = []
user_reason_list = []
rej_user_reason_list = []
device_arr = np.zeros(5, dtype=int)
rej_device_arr = np.zeros(5, dtype=int)
age_arr = np.zeros(7, dtype=int)
rej_age_arr = np.zeros(7, dtype=int)
network_arr = np.zeros(4, dtype=int)
rej_network_arr = np.zeros(4, dtype=int)

sort_results(res, grade_list, order_list, vid_time_list, grade_time_list, user_reason_list, device_arr, age_arr, network_arr)
sort_results(rej_res, rej_grade_list, rej_order_list, rej_vid_time_list, rej_grade_time_list, rej_user_reason_list, rej_device_arr, rej_age_arr, rej_network_arr)

# Interpret Grades
grades = np.stack((grade_list), axis = -1)
grades_z = zscore(grades, axis=0)
vid_times = np.stack((vid_time_list), axis = -1)
grade_times = np.stack((grade_time_list), axis = -1)

grades_mean = np.mean(grades, axis=1)
grades_z_mean = np.mean(grades_z, axis=1)
vid_times_mean = np.mean(vid_times, axis=1)
grade_times_mean = np.mean(grade_times, axis=1)

grades_std = np.std(grades, axis=1)
grades_z_std = np.std(grades_z, axis=1)

grades_se = grades_std / np.sqrt(np.shape(grades)[1])
grades_z_se = grades_z_std / np.sqrt(np.shape(grades_z)[1])

# Create Log File
log = open(log_name, "w+")
log.write(header)

log.write("########\n")
log.write("#GRADES#\n")
log.write("########\n\n")

log.write("RAW GRADES:\n")
for grade in grades:
    grade_str = np.array2string(a=grade,separator=' ') + "\n"
    log.write(grade_str)
log.write("MEAN:\n")
mean_str = np.array2string(a=grades_mean,precision=3,separator=' ') + "\n"
log.write(mean_str)
log.write("STANDARD ERROR:\n")
se_str = np.array2string(a=grades_se,precision=3,suppress_small=True,separator=' ') + "\n\n"
log.write(se_str)

log.write("STANDARDIZED GRADES:\n")
for grade in grades_z:
    grade_z_str = np.array2string(a=grade,precision=3,separator=' ') + "\n"
    log.write(grade_z_str)
log.write("MEAN:\n")
mean_z_str = np.array2string(a=grades_z_mean,precision=3,separator=' ') + "\n"
log.write(mean_z_str)
log.write("STANDARD ERROR:\n")
se_z_str = np.array2string(a=grades_z_se,precision=3,suppress_small=True,separator=' ') + "\n\n"
log.write(se_z_str)

log.write("#############\n")
log.write("#VIDEO ORDER#\n")
log.write("#############\n\n")

log.write("RAW ORDERS:\n")
for user in order_list:
    ord_str = np.array2string(a=user,separator=' ') + "\n"
    log.write(ord_str)
log.write("\n")

log.write("#################\n")
log.write("#VIDEO VIEW TIME#\n")
log.write("#################\n\n")

log.write("RAW TIMES:\n")
for time in vid_times:
    vid_time_str = np.array2string(a=time,separator=' ') + "\n"
    log.write(vid_time_str)
log.write("MEAN:\n")
vid_time_mean_str = np.array2string(a=vid_times_mean,precision=3,separator=' ') + "\n\n"
log.write(vid_time_mean_str)

log.write("#################\n")
log.write("#GRADE VIEW TIME#\n")
log.write("#################\n\n")

log.write("RAW TIMES:\n")
for time in grade_times:
    grade_time_str = np.array2string(a=time,separator=' ') + "\n"
    log.write(grade_time_str)
log.write("MEAN:\n")
grade_time_mean_str = np.array2string(a=grade_times_mean,precision=3,separator=' ') + "\n\n"
log.write(grade_time_mean_str)

log.write("###############\n")
log.write("#DEVICE COUNTS#\n")
log.write("###############\n\n")

log.write("Desktop: %d\n" % device_arr[0])
log.write("Laptop: %d\n" % device_arr[1])
log.write("Tablet: %d\n" % device_arr[2])
log.write("Smart phone: %d\n" % device_arr[3])
log.write("Other device: %d\n\n" % device_arr[4])

log.write("##################\n")
log.write("#AGE GROUP COUNTS#\n")
log.write("##################\n\n")

log.write("18 - 24: %d\n" % age_arr[0])
log.write("25 - 31: %d\n" % age_arr[1])
log.write("32 - 38: %d\n" % age_arr[2])
log.write("39 - 45: %d\n" % age_arr[3])
log.write("46 - 52: %d\n" % age_arr[4])
log.write("53 - 59: %d\n" % age_arr[5])
log.write("60 and above: %d\n\n" % age_arr[6])

log.write("################\n")
log.write("#NETWORK COUNTS#\n")
log.write("################\n\n")

log.write("WiFi: %d\n" % network_arr[0])
log.write("Cable network: %d\n" % network_arr[1])
log.write("Cellular network: %d\n" % network_arr[2])
log.write("Other: %d\n\n" % network_arr[3])

log.write("###########\n")
log.write("#REASONING#\n")
log.write("###########\n\n")

for pair in user_reason_list:
    log.write("%s: %s\n" % (pair[0], pair[1]))

log.close()

plt.figure()
plt.style.use('ggplot')
plt.xlabel(x_label)
plt.ylabel('grade')
plt.plot(x, grades_mean, "blue")
plt.errorbar(x, grades_mean, yerr=grades_se, fmt="-o", ecolor="red", alpha=0.5)
plt.legend(['mean','Standard Error'],
            loc='upper right',
            numpoints=1,
            fancybox=True)
plt.savefig(plot_name)

plt.figure()
plt.style.use('ggplot')
plt.xlabel(x_label)
plt.ylabel('grade')
plt.plot(x, grades_z_mean, "blue")
plt.errorbar(x, grades_z_mean, yerr=grades_z_se, fmt="-o", ecolor="red", alpha=0.5)
plt.legend(['mean','Standard Error'],
            loc='upper right',
            numpoints=1,
            fancybox=True)
plt.savefig(z_name)

