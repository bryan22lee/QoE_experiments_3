// start test:
const moment= require('moment-timezone') 
var getOder = require('../models/random');
var fs = require('fs');

const vid_folder = "Soccer_720p_2_500k_360_exp1";
var vid_path = "./videos/" + vid_folder;
var video_url = "https://raw.githubusercontent.com/bryan22lee/QoE_experiments_3/master/videos/" + vid_folder + "/";
var best_quality = video_url + "1.mp4"; // no stall, no blue
var worst_quality = video_url + "2.mp4"; // stall and bad blur

var num_vids;

fs.readdir(vid_path, function(err, files) {
    num_vids = files.length;
    console.log(vid_path + " has " + num_vids + " files");
});

var post_example = async (ctx, next) => {
    ctx.render('example.html', {
    });
}

var post_start = async (ctx, next) => {
    // 03:48:34 CST
    var time_start = moment().tz('America/Chicago').format('hh:mm:ss z')
    // August 27th 2020, 12:00:28 am
    var date_start = moment().tz('America/Chicago').format('MMMM Do YYYY, h:mm:ss a');

    var active_time = parseFloat(ctx.request.body.active_time);
    var browserName = ctx.request.body.browser;
    var mturkID = ctx.request.body.MTurkID;
    var device = ctx.request.body.device;
    var age = ctx.request.body.age;
    var network = ctx.request.body.network;
    var video_order = [1, 2, ...getOder(3,num_vids)]; // accounts for variable number of videos (num_vids)
    //var video_order = [1,2,3,4]
    console.log(mturkID, device, age);
    var start = new Date().getTime();
   


 
    let user = {
        time_start : time_start,
        date_start : date_start,
        mturkID : mturkID,
        device : device,
        age : age,
        network : network,
        video_order : video_order,
        count : 1,
        result : [],
        video_time : [],
        grade_time : [],
        active_video_time: [],
        active_grade_time : [],
        test: [],
        start : start,
        instruction: active_time,
        play: [],
        pause: [],
        seek: [],
        browser: browserName,
        reference: [],
        return : [],
        training : 0
    };
    for (i = 0; i < num_vids; i++)
    {
        user.video_time.push(0);
        user.grade_time.push(0);
        user.active_video_time.push(0);
     	user.active_grade_time.push(0);
        user.play.push(0);
        user.pause.push(0);
        user.seek.push(0);
        user.return.push(0)
        user.reference.push(0)
    }
    let value =  Buffer.from(JSON.stringify(user)).toString('base64');
    ctx.cookies.set('name', value);
    ctx.render('training_page.html', {
    });
}

var post_grade= async (ctx, next) => {

	var active_time = parseFloat(ctx.request.body.active_time);
    var play = parseFloat(ctx.request.body.play);
    var pause = parseFloat(ctx.request.body.pause);
    var seek = parseFloat(ctx.request.body.seek);
    console.log(active_time)
    var user = ctx.state.user;
    var end = new Date().getTime();
    var exe_time = end - user.start;
    user.video_time[user.count-1] += exe_time;
    user.active_video_time[user.count-1] += active_time;
    user.play[user.count-1] += play;
    user.pause[user.count-1] += pause;
    user.seek[user.count-1] += seek;
    
    console.log(user.active_video_time)
    
    user.start = end;
    
    let value =  Buffer.from(JSON.stringify(user)).toString('base64');
    ctx.cookies.set('name', value);

    var title = user.count + "/" + num_vids;
    ctx.render('grade.html', {
        title: title, count: user.count, num_vids: num_vids
    });
}

var post_first = async (ctx, next) => {
    var video_src = video_url + "1.mp4";
    var user = ctx.state.user;
    var active_time = parseFloat(ctx.request.body.active_time);
    user.training = active_time
    // https://github.com/michaelliao/learn-javascript/raw/master/video/vscode-nodejs.mp4
    // very interesting url!
    let value =  Buffer.from(JSON.stringify(user)).toString('base64');
    ctx.cookies.set('name', value);
    var title = "1/" + num_vids;
    ctx.render('video.html', {
        title: title, video_src : video_src
    });
}
var post_training = async (ctx, next) => {
    // https://github.com/michaelliao/learn-javascript/raw/master/video/vscode-nodejs.mp4
    // very interesting url!

    var title = "1/" + num_vids;
    ctx.render('training_page.html', {
    });
}


var post_reference = async (ctx, next) => {
	var user = ctx.state.user;
    
    var video_src = video_url + "1.mp4";
    // https://github.com/michaelliao/learn-javascript/raw/master/video/vscode-nodejs.mp4
    // very interesting url!
    var active_time = parseFloat(ctx.request.body.active_time);
    user.active_video_time[user.count-1] += active_time;
    console.log(active_time)
        console.log(user.active_video_time)

    let value =  Buffer.from(JSON.stringify(user)).toString('base64');
    ctx.cookies.set('name', value);
    
    var title = "1/" + num_vids;
    ctx.render('reference.html', {
        best_quality: best_quality, worst_quality : worst_quality
    });
}

var post_back2video = async (ctx, next) => {
    var user = ctx.state.user;
    console.log(':(')
    var video_src = video_url + user.video_order[user.count - 1] + ".mp4";
    var active_time = parseFloat(ctx.request.body.active_time);
    var end = new Date().getTime();
    var exe_time = end - user.start;
    user.grade_time[user.count-1] += exe_time;
    user.return[user.count-1] += 1;
    if (!isNaN(active_time))
    {
        user.active_grade_time[user.count-1] += active_time;
    }
    user.start = end;
    let value =  Buffer.from(JSON.stringify(user)).toString('base64');
    console.log(user.active_grade_time)
    ctx.cookies.set('name', value);
    var title = user.count + "/" + num_vids;
    if (user.video_order[user.count - 1] == 1){
        ctx.render('video.html', {
            title: title, video_src : video_src
        });
    }
    else if  (user.video_order[user.count - 1] == 2) {
        ctx.render('bad_video.html', {
            title: title, video_src : video_src
        });
    }
    else { 
        ctx.render('2video.html', {
        title: title,  video_src: video_src
        });
    }
}



var post_back2video2 = async (ctx, next) => {
    var user = ctx.state.user;
    var video_src = video_url + user.video_order[user.count - 1] + ".mp4";
    var refer =parseFloat(ctx.request.body.refer);
    var user = ctx.state.user;
    user.reference[user.count-1] += 1
    let value =  Buffer.from(JSON.stringify(user)).toString('base64');
    
    ctx.cookies.set('name', value);
    var title = user.count + "/" + num_vids;
    if (user.video_order[user.count - 1] == 1){
        ctx.render('video.html', {
            title: title, video_src : video_src
        });
    }
    else if  (user.video_order[user.count - 1] == 2) {
        ctx.render('bad_video.html', {
            title: title, video_src : video_src
        });
    }
    else { 
        ctx.render('2video.html', {
        title: title,  video_src: video_src
        });
    }
}
var post_next = async (ctx, next) => {
    var user = ctx.state.user;
    var active_time =parseFloat(ctx.request.body.active_time);
    console.log(active_time)
    var grade = ctx.request.body.sentiment;
    var end = new Date().getTime();
    var exe_time = end - user.start;

    var attention_test = Number(ctx.request.body.blur)+ Number(ctx.request.body.stall);
  
    user.test.push(attention_test);
    user.result.push(grade);
    

    user.grade_time[user.count-1] += exe_time;
	user.active_grade_time[user.count-1] += active_time;


    user.start = end;
    if(user.count < num_vids) {
        var video_src = video_url + user.video_order[user.count] + ".mp4";
        user.count = user.count + 1;
        var title = user.count + "/" + num_vids;

        // set new cookie
        let value =  Buffer.from(JSON.stringify(user)).toString('base64');
        ctx.cookies.set('name', value);
        if  (user.count == 2) {
            ctx.render('bad_video.html', {
                title: title, video_src : video_src
            });
        } 
        else if (user.count == 3){
          ctx.render('test_page.html', {
                title: title, video_src : video_src
            });  
        }
        else  {
            ctx.render('2video.html', {
                title: title,  video_src: video_src
            });
        }
    }
    else {
         // set new cookie
        let value =  Buffer.from(JSON.stringify(user)).toString('base64');
        ctx.cookies.set('name', value);
        ctx.render('reason.html', {
            title: 'Post Survey Question'
        });
    }
}

var post_end = async (ctx, next) => {
    var user = ctx.state.user;
    
    // set user reason
    var reason = ctx.request.body.Reason;
    console.log("reason is " + reason + "\n");
    user.reason = reason;

    // record results
    console.log(user.result);
    var filename = "./results/" + user.mturkID + ".txt";
    var write_data = [];
    var write_test = [];
    var write_video_time = [], write_grade_time =[];
    var write_active_video_time = [], write_active_grade_time = []
    var write_play = [], write_seek = []
    var write_reference = [], write_pause = []
    var write_return = []
        console.log(user.play)
        console.log(user.reference)
    for(var i in user.video_order) {
        write_data[user.video_order[i] - 1] = user.result[i];
        write_test[user.video_order[i] - 1] = user.test[i];
        write_video_time[user.video_order[i] - 1] = user.video_time[i];
        write_grade_time[user.video_order[i] - 1] = user.grade_time[i];
		write_active_video_time[user.video_order[i] - 1] = user.active_video_time[i];
        write_active_grade_time[user.video_order[i] - 1] = user.active_grade_time[i];

        write_play[user.video_order[i] - 1] = user.play[i];
        write_pause[user.video_order[i] - 1] = user.pause[i];
        write_seek[user.video_order[i] - 1] = user.seek[i];
        write_reference[user.video_order[i] -1 ]= user.reference[i];
write_return[user.video_order[i] -1 ]= user.return[i];
        if (i == 2)
            write_return[user.video_order[i] -1 ]-=1
    }
    fs.writeFile(filename, write_data + '\n'+ user.video_order + '\n' + 
                write_video_time + '\n' + write_active_video_time + '\n'
                 + write_grade_time + '\n' + write_active_grade_time + '\n' + user.mturkID + '\n' 
                 + user.device + '\n' + user.age + '\n' 
                 + user.network + '\n' + user.reason +'\n'+ user.browser + '\n' + user.instruction + '\n'+ user.training + '\n' +
                 write_play + '\n' + write_pause + '\n' + write_seek + '\n' + write_reference + '\n' + write_return + '\n' +
                 user.date_start + '\n' + user.time_start + '\n' + write_test, function(err) {
        if(err) {
            return console.log(err);
        }
    });
    // clear cookie
    ctx.cookies.set('name','');
    
    var return_code = vid_folder;
    ctx.render('ending.html', {
        title: 'Thank you', return_code:return_code
    });
}
                 

module.exports = {
    'POST /start' : post_start,
    'POST /training' : post_training,
    'POST /grade': post_grade,
    'POST /back2video':post_back2video,
    'POST /back2video2':post_back2video2,
    'POST /next' : post_next,
    'POST /end' : post_end,
    'POST /example' : post_example,
    'POST /first': post_first,
    'POST /reference': post_reference
};
