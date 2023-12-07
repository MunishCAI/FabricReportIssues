from flask import Flask, redirect, url_for, request,render_template,jsonify,send_from_directory
import pandas as pd
import psycopg2
import time, os, shutil, datetime, pytz
import random
import base64
import python_file.db as db
import python_file.report as rep_pdf
import python_file.shift as shift_pdf
import asyncio
import shutil
import pandas as pd
from configparser import ConfigParser
import json
import logging
from python_file.pendriveAuth import authendicatePendrive as pendriveAuth
import threading
from python_file.status import checkserver

logEntry = False

# logging setup
if logEntry == 1:
    logging.basicConfig(filename="newfile.log",
                        format='%(asctime)s %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

app = Flask(__name__, static_url_path='/static', static_folder='static')
db.db.turnOffliveImg()

@app.route('/')
async def hello_world():
    config = ConfigParser()
    config.read('config_webui.ini')
    webui_version = config.get('version', 'webui_version')
    logger.info("INFO : login Home page") if logEntry == 1 else None
    return render_template("index.html",webui_version=webui_version)


@app.route('/setting')
async def hello_setting():
    config = ConfigParser()
    config.read('config_webui.ini')
    webui_version = config.get('version', 'webui_version')
    logger.info("INFO : login Setting page") if logEntry == 1 else None
    return render_template("setting.html",webui_version=webui_version)

@app.route('/update_image', methods=['GET'])
def update_image():
    i=0
    # i = random.choice([0,1])
    if i==0:        
        base64_image = db.db.get_base64_image_data()
        logger.info("INFO : Live Image updated") if logEntry == 1 else None
        yield f"data:image/png;base64,{base64_image}" 
    else:
        logger.error("ERROR : Live Image Not updated") if logEntry == 1 else None
        yield "{{ url_for('static', filename='images/nn.png') }}" 
        
        
@app.route('/update_defectimage', methods=['GET'])
def update_defectimage():
    # test
    # i = random.choice([0,1])
    # if i==0:
        
    #     print('i : ',i)
    #     source = '/home/santhosh/Pictures/image1.jpg'
    # else:
    #     print('i : ',i)
    #     source = '/home/santhosh/Pictures/image7.jpg'
    
    
    # live 
    config = ConfigParser()
    config.read('config_webui.ini')
    defect_photo_path_prefix = config.get('defectImgPath', 'defect_photo_path_prefix')
    
    data = db.db.get_defect_details()
    source = defect_photo_path_prefix + data[3]
    # print(source)
        
    with open(source, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        my_string = my_string.decode()
        logger.info("INFO : Last Defect Image updated") if logEntry == 1 else None
        yield f"data:image/png;base64,{my_string}" 
   


@app.route('/update_rotation', methods=['GET'])
async def update_rotation():           
        bottom_bar = db.db.get_BottomBar()
        time.sleep(1)  
        data_dict = {
            'rollId': bottom_bar[0],
            'rotationValue': bottom_bar[1],
            'fabric_type': bottom_bar[2],
            'doff': bottom_bar[3]
        }
        response = jsonify(data_dict)
        logger.info("INFO : Rotation updated") if logEntry == 1 else None
        return response

@app.route('/update_machineDetails', methods=['GET'])
async def update_machineDetails():           
        data = db.db.get_machine_details()        
        time.sleep(1) 
        data_dict = {
            'machinename': data[0],
            'machinestatus': data[1],
            'machinedtl_name':data[2]
        }
        logger.info("INFO : Machine Status updated") if logEntry == 1 else None
        response = jsonify(data_dict)
        return response  

@app.route('/update_defectDetails', methods=['GET'])
async def update_defectDetails():        
        data = db.db.get_defect_details()
        time.sleep(1)       
        time.sleep(3)
        data_dict = {
            'defectname': data[0],
            'rollname': data[1],
            'captureAt': data[2].strftime('%Y-%m-%d %H:%M:%S')
        }
        logger.info("INFO : Defect Details updated") if logEntry == 1 else None
        response = jsonify(data_dict)
        return response 

@app.route('/rollUpdate', methods=['POST', 'GET'])
async def rollUpdate():
    error_message = None  # Initialize error_message as None

    if request.method == 'POST':
        doff = request.form['doff']
        db.db.update_doff(doff)
        logger.info("INFO : Roll updated") if logEntry == 1 else None
        return render_template('index.html')
        
    logger.error("ERROR : Roll NOT updated") if logEntry == 1 else None
    return render_template('index.html')

# @app.route('/settingsUpdate', methods=['POST']) 
# async def settingsUpdate():
#         error_message = None
#         if request.method == 'POST':
#             mill = request.form['mill']
#             machinetype = request.form['machinetype']
#             machineno = request.form['machineno']
#             dia = request.form['dia']
#             gg = request.form['gg']
            
#             party = request.form['party']
#             needle_drop = request.form['needledrop']
#             count = request.form['count']
#             denier = request.form['denier']
#             fabric_type = request.form['fabric']
#             knittype = request.form['knittype']
#             gsm_ll = request.form['gsm']
#             ll = request.form['ll']
#             roll_weight = request.form['rollweight']
#             doff = request.form['rotations']
#             lot = request.form['lot']
#             job_no = request.form['jobnumber']
            
#             print("mill :",mill)
#             print("machinetype :",machinetype)
#             print("machineno :",machineno)
#             print("dia :",dia)
#             print("gg :",gg)
#             print("party :",party)
#             print("needle_drop :",needle_drop)
#             print("count :",count)
#             print("denier :",denier)
#             print("fabric_type :",fabric_type)
#             print("knittype :",knittype)
#             print("gsm_ll :",gsm_ll)
#             print("ll :",ll)
#             print("roll_weight :",roll_weight)
#             print("doff :",doff)
#             print("lot :",lot)
#             print("job_no :",job_no)    
                    
#             db.db.update_setting(mill,machinetype,machineno,dia,gg,party,needle_drop,count,denier,fabric_type,knittype,gsm_ll,ll,roll_weight,doff,lot,job_no)
#             logger.info("INFO : Setting updated") if logEntry == 1 else None
#             return render_template('index.html')
        
#         logger.error("ERROR : Setting NOT updated") if logEntry == 1 else None
#         return render_template('index.html')
        

@app.route('/success')
def success():
    return 'Form submitted successfully!'

@app.route('/getAlarmStatus', methods=['GET'])
async def getAlarmStatus():        
        data = db.db.getAlarm_Status()
        data_dict = {
            "status": data
        }
        response = jsonify(data_dict)
        logger.info("INFO : getAlarm Status Response") if logEntry == 1 else None
        return response 
    
@app.route('/updateAlarmstatus', methods=['GET'])
async def updateAlarmstatus():           
    db.db.updateAlarm_status()
    logger.info("INFO : updateAlarm Status Response") if logEntry == 1 else None
    return render_template('index.html')
      
    
    
@app.route('/startNewRollUpdate', methods=['GET'])
async def startNewRollUpdate():           
    db.db.startNewRoll_Update()
    logger.info("INFO : startNewRoll Response") if logEntry == 1 else None
    

@app.route('/getmoreInfo', methods=['GET'])
async def getmoreInfo():           
        data = db.db.get_moreinfo()
        time.sleep(1)  # Wait for 1 second before fetching the next image
        try:
            data_dict = {
                "machineprgdtl_id" : data[0],
                "program_name" : data[1],
                "description" : data[2],
                "gsm_ll" : data[3], 
                "gg" : data[4],
                "fabric_type" : data[5],
                "job_no" : data[6],
                "needle_drop" : data[7],
                "roll_weight" : data[8],
                "doff" : data[9],
                "count" : data[10],
                "mill" : data[11],
                "dia" : data[12],
                "lot" : data[13],
                "party" : data[14],
                "timestamp" : data[15].strftime('%Y-%m-%d %H:%M:%S')
            }
            logger.info("INFO : getmoreInfo Success") if logEntry == 1 else None
            
        except AttributeError:
                data_dict = {
                "machineprgdtl_id" : data[0],
                "program_name" : data[1],
                "description" : data[2],
                "gsm_ll" : data[3],
                "gg" : data[4],
                "fabric_type" : data[5],
                "job_no" : data[6],
                "needle_drop" : data[7],
                "roll_weight" : data[8],
                "doff" : data[9],
                "count" : data[10],
                "mill" : data[11],
                "dia" : data[12],
                "lot" : data[13],
                "party" : data[14],
                "timestamp" : data[15]
                }
                logger.error("ERROR : getmoreInfo") if logEntry == 1 else None
                
        print(data_dict)
        response = jsonify(data_dict)
        return response 


@app.route('/getmoreInfo_edit_programInfo', methods=['GET'])
async def getmoreInfo_edit_programInfo():           
        data = db.db.get_moreinfo()
        data1 = db.db.get_moreinfo1()

        try:
            data_dict = {
                "machineprgdtl_id" : data[0],
                "program_name" : data[1],
                "description" : data[2],
                "gsm_" : data[3], 
                "gg" : data[4],
                "fabric_type" : data[5],
                "job_no" : data[6],
                "needle_drop" : data[7],
                "roll_weight" : data[8],
                "doff" : data[9],
                "count" : data[10],
                "mill" : data[11],
                "dia" : data[12],
                "lot" : data[13],
                "party" : data[14],
                "machineprogram_sts_id" : data[16],
                "loop_length" : data[17],
                "knit_type" : data[18],
                "denier" : data[19],
                "machinedtl_name":data1[0],
                "machine_type":data1[1],
                "timestamp" : data[15].strftime('%Y-%m-%d %H:%M:%S')
            }
            logger.info("INFO : getmoreInfo Success") if logEntry == 1 else None
            
        except AttributeError:
                data_dict = {
                "machineprgdtl_id" : data[0],
                "program_name" : data[1],
                "description" : data[2],
                "gsm_" : data[3], 
                "gg" : data[4],
                "fabric_type" : data[5],
                "job_no" : data[6],
                "needle_drop" : data[7],
                "roll_weight" : data[8],
                "doff" : data[9],
                "count" : data[10],
                "mill" : data[11],
                "dia" : data[12],
                "lot" : data[13],
                "party" : data[14],
                "machineprogram_sts_id" : data[16],
                "loop_length" : data[17],
                "knit_type" : data[18],
                "denier" : data[19],
                "machinedtl_name":data1[0],
                "machine_type":data1[1],
                "timestamp" : data[15]
                }
                logger.error("ERROR : getmoreInfo") if logEntry == 1 else None
                
        print(data_dict)
        response = jsonify(data_dict)
        return response 

@app.route('/getdefect_data', methods=['GET'])
async def getdefect_data():        
        data = db.db.defect_data()
        formatted_data = [
        { "adefectname": item[0], "count": item[1]}
        for item in data
        ]
        response = jsonify(formatted_data)
        logger.info("INFO : getdefect_data Success") if logEntry == 1 else None
        return response




class TimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime('%H:%M:%S')  # Format the time as a string
        return super(TimeEncoder, self).default(obj)
    
@app.route('/get_alarm_setting', methods=['GET'])
async def get_alarm_setting():        
        data = db.db.getAlarmSetting()
        formatted_data = [
        { 
         "adefecTypeId": item[0], 
         "adefectName": item[1],
         "minimumAlarmCount":item[2],
         "score":item[3],
         "alarmStatus":item[4]}
        for item in data
        ]
        json_data = json.dumps(formatted_data, cls=TimeEncoder)
        response = jsonify(formatted_data)
        logger.info("INFO : get_alarm_setting Success") if logEntry == 1 else None
        return response 

@app.route('/get_shift_setting', methods=['GET'])
async def get_shift_setting():  
        # print('conated get_shift_setting')      
        data = db.db.getShiftSetting()
        formatted_data = [
        { 
         "ashift_id": item[0], 
         "bshift_name": item[1],
         "cstart_time":str(item[2]),
         "dend_time":str(item[3]),
         }
        for item in data
        ]
        response = jsonify(formatted_data)
        logger.info("INFO : get_shift_setting Success") if logEntry == 1 else None
        return response 
    
    
    
@app.route('/report/<report_date>', methods=['POST', 'GET'])
def report(report_date):
    if request.method == 'POST':
        datepicker = report_date
        data = rep_pdf.generate_pdf_performance(datepicker)
        data_dict = {
            "status": data
        }
        response = jsonify(data_dict)
        logger.info("INFO : Report Success") if logEntry == 1 else None
        return response 
    

@app.route('/reportA/<report_date>', methods=['POST', 'GET'])
def reportA(report_date):
    if request.method == 'POST':
        datepicker = report_date
        data = shift_pdf.shift_A_pdf(datepicker)
        data_dict = {
            "status": data
        }
        logger.info("INFO : ReportA Success") if logEntry == 1 else None
        response = jsonify(data_dict)
        return response 

@app.route('/reportB/<report_date>', methods=['POST', 'GET'])
def reportB(report_date):
    if request.method == 'POST':
        datepicker = report_date
        data = shift_pdf.shift_B_pdf(datepicker)
        data_dict = {
            "status": data
        }
        logger.info("INFO : ReportB Success") if logEntry == 1 else None
        response = jsonify(data_dict)
        return response 
    
@app.route('/reportC/<report_date>', methods=['POST', 'GET'])
def reportC(report_date):
    if request.method == 'POST':
        datepicker = report_date
        data = shift_pdf.shift_C_pdf(datepicker)
        data_dict = {
            "status": data
        }
        logger.info("INFO : ReportC Success") if logEntry == 1 else None
        response = jsonify(data_dict)
        return response 

@app.route('/updatebypass', methods=['POST', 'GET'])
def updatebyPass():
    if request.method == 'POST':
        try:
            full_bypass = request.form['full_bypass']
            full_bypass = '1'
        except:
            full_bypass = '2'
        
        try:
            alarm_bypass = request.form['alarm_bypass']
            alarm_bypass = '1'
        except:
            alarm_bypass = '2'
            
        try:
            sensor_bypass = request.form['sensor_bypass']
            sensor_bypass = '1'
        except:
            sensor_bypass = '2'
        
        db.db.updatebypass(full_bypass,alarm_bypass,sensor_bypass)
        time.sleep(2)
        logger.info("INFO : updatebypass Success") if logEntry == 1 else None
        return render_template('setting.html')
    
@app.route('/updateMachineName', methods=['POST', 'GET'])
def updateMachineName():
    if request.method == 'POST':
        try:
            machineName = request.form['new_machineName']
        except:
            print('Error in Data Reading')      
        db.db.updateMachineName(machineName)
        time.sleep(2)
        logger.info("INFO : updatebypass Success") if logEntry == 1 else None
        return render_template('setting.html')

@app.route('/updaterecording', methods=['POST', 'GET'])
def updaterecording():
    if request.method == 'POST':
        try:
            bypass_livecamera = request.form['bypass_livecamera']
            bypass_livecamera = '1'
            timer = threading.Timer(900,db.db.turnOffliveImg)
            timer.start()
        except:
            bypass_livecamera = '2'
        
        try:
            bypass_saveimg = request.form['bypass_saveimg']
            bypass_saveimg = '1'
        except:
            bypass_saveimg = '2'
            
        try:
            bypass_imgpath = request.form['bypass_imgpath']            
        except:
            bypass_imgpath = 'default_folder'
            
        try:
            bypass_fps = request.form['bypass_fps']            
        except:
            bypass_fps = '10'
        db.db.updateRecording(bypass_livecamera,bypass_saveimg,bypass_imgpath,bypass_fps)
        time.sleep(2)
        logger.info("INFO : updaterecording Success") if logEntry == 1 else None        
        return render_template('setting.html')



@app.route('/getbypass_status', methods=['POST', 'GET'])
async def getbypass_status():
        full_bypass,alarm_bypass,sensor_bypass = db.db.getBypassStatus()       
        data_dict = {
            'full_bypass': full_bypass,
            'alarm_bypass': alarm_bypass,
            'sensor_bypass': sensor_bypass
        }
        logger.info("INFO : getbypass_status Success") if logEntry == 1 else None       
        response = jsonify(data_dict)
        return response


@app.route('/get_machineName', methods=['POST', 'GET'])
async def get_machineName():
        machineName = db.db.getMachineName()       
        data_dict = {
            'machineName': machineName
        }
        logger.info("INFO : get_machineName Success") if logEntry == 1 else None        
        response = jsonify(data_dict)
        return response
    
    
@app.route('/get_version', methods=['POST', 'GET'])
async def get_version():
        config = ConfigParser()
        config.read('config_webui.ini')
        webui_version = config.get('version', 'webui_version')
        webui_version_ts = config.get('version', 'timestamp')
        report_version = config.get('report', 'version')
        report_version_ts = config.get('report', 'timestamp')
        config.read('alarmconfig.ini')
        alarm_version = config.get('Version', 'currentversion')
        alarm_version_ts = config.get('Version', 'timestamp')
        config.read('coreconfig.ini')
        core_version = config.get('Version', 'currentversion')
        core_version_ts = config.get('Version', 'timestamp')
        config.read('monitorconfig.ini')
        monitor_version = config.get('Version', 'currentversion')
        monitor_version_ts = config.get('Version', 'timestamp')
        # print(report_version, webui_version ,alarm_version,core_version, monitor_version)      
        data_dict = {
            'core_version' : core_version,
            'core_version_ts' : core_version_ts,
            'alarm_version' : alarm_version,
            'alarm_version_ts' : alarm_version_ts,
            'report_version' : report_version,
            'report_version_ts' : report_version_ts,
            'monitor_version' : monitor_version,
            'monitor_version_ts' : monitor_version_ts,
            'webui_version' : webui_version,
            'webui_version_ts' : webui_version_ts
        }
        logger.info("INFO : get_version Success") if logEntry == 1 else None       
        response = jsonify(data_dict)
        return response


@app.route('/get_saved_program_1', methods=['POST', 'GET'])
async def get_saved_program_1():
    value = db.db.getSavedProgram1() 



@app.route('/get_recording', methods=['POST', 'GET'])
async def get_recording():
        livecamera_status,saveimage_status,image_path,fps = db.db.getRecording()       
        data_dict = {
            'livecamera_status': livecamera_status,
            'saveimage_status': saveimage_status,
            'image_path': image_path,
            'fps': fps
        }
        logger.info("INFO : get_recording Success") if logEntry == 1 else None        
        response = jsonify(data_dict)
        return response 
    
@app.route('/updatealarmsetting', methods=['POST', 'GET'])
async def updatealarmsetting():
        if request.method == 'POST':
            form_data = request.form.to_dict()  # Collect all form data into a dictionary
            db.db.updateAlarmSetting(form_data)
            logger.info("INFO : updatealarmsetting Success") if logEntry == 1 else None        
            time.sleep(2)
            return render_template('setting.html')
        
@app.route('/get_camera_setting', methods=['GET'])
async def get_camera_setting():        
        data = db.db.getCameraSetting()
        formatted_data = [
        { 
         "cam_id": item[0], 
         "cam_name": item[1],
         "camsts_id":item[2]}
        for item in data
        ]
        json_data = json.dumps(formatted_data, cls=TimeEncoder)
        logger.info("INFO : get_camera_setting Success") if logEntry == 1 else None        
        response = jsonify(formatted_data)
        return response 

@app.route('/pdfViewer')
async def pdfViewer():
    directory_path = './static/report'
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            current_report = filename
    config = ConfigParser()
    config.read('config_webui.ini')
    conf_dir = config.get('report', 'outputPDF_directory_path')
    destination_file = os.path.join(directory_path, current_report)
    shutil.copy(destination_file, conf_dir)
    return render_template("pdfViewer.html",current_report=current_report)

@app.route('/DefectLogPage')
async def DefectLog():
    return render_template("defectLog.html")

@app.route('/downloadReport', methods=['POST', 'GET'])
async def downloadReport():
        if request.method == 'POST':
            pen_path = pendriveAuth()
            print(pen_path)
            if(pen_path):
                source_file = 'static/report'
                usb_drive_path = pen_path
                destination_path = os.path.join(usb_drive_path)
                try:
                    for filename in os.listdir(source_file):
                        if filename.endswith(".pdf"):
                            source_file = os.path.join(source_file, filename)
                            destination_file = os.path.join(destination_path, filename)
                            shutil.copy(source_file, destination_file)
                except FileNotFoundError:
                    print("Source file not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                time.sleep(3)
                print('authdicated****************')
                data = True
                data_dict = {
                    "status": data
                    }
                
                response = jsonify(data_dict)
                return response 
            else:
                time.sleep(3)
                data = False
                data_dict = {
                    "status": data
                    }
                response = jsonify(data_dict)
                print('NOT authdicated****************')
                return response 
            


    
@app.route('/updatecamera', methods=['POST', 'GET'])
async def updatecamera():
        if request.method == 'POST':
            form_data = request.form.to_dict()  # Collect all form data into a dictionary
            db.db.updateCameraSetting(form_data)
            logger.info("INFO : updatecamera Success") if logEntry == 1 else None        
            time.sleep(2)
            return render_template('setting.html')
        
@app.route('/updateshiftsetting', methods=['POST', 'GET'])
async def updateshiftsetting():
        if request.method == 'POST':
            form_data = request.form.to_dict()  # Collect all form data into a dictionary
            a = shift1_startTime = request.form['start_time1']
            c = shift2_startTime = request.form['start_time2']
            e = shift3_startTime = request.form['start_time3']
            b = shift1_endTime = request.form['end_time1']
            d = shift2_endTime = request.form['end_time2']
            f = shift3_endTime = request.form['end_time3']
            time.sleep(5)
            logger.info("INFO : updateshiftsetting Success") if logEntry == 1 else None       
            db.db.updateShiftsetting(form_data)            
            return render_template('setting.html')
        
@app.route('/settingsUpdate', methods=['POST']) 
async def settingsUpdate():
        error_message = None
        if request.method == 'POST':  
            mill = request.form['mill']
            machinetype = request.form['machinetype']
            machineno = request.form['machineno']
            dia = request.form['dia']
            gg = request.form['gg']
            party = request.form['party']
            needle_drop = request.form['needledrop']
            count = request.form['count']
            denier = request.form['denier']
            fabric_type = request.form['fabric']
            knittype = request.form['knittype']
            gsm_ll = request.form['gsm']
            ll = request.form['ll']
            roll_weight = request.form['rollweight']
            doff = request.form['rotations']
            lot = request.form['lot']
            job_no = request.form['jobnumber']
            print("mill :",mill)
            print("machinetype :",machinetype)
            print("machineno :",machineno)
            print("dia :",dia)
            print("gg :",gg)
            print("party :",party)
            print("needle_drop :",needle_drop)
            print("count :",count)
            print("denier :",denier)
            print("fabric_type :",fabric_type)
            print("knittype :",knittype)
            print("gsm_ll :",gsm_ll)
            print("ll :",ll)
            print("roll_weight :",roll_weight)
            print("doff :",doff)
            print("lot :",lot)
            print("job_no :",job_no)  
            db.db.update_setting(mill,machinetype,machineno,dia,gg,party,needle_drop,count,denier,fabric_type,knittype,gsm_ll,ll,roll_weight,doff,lot,job_no)
            logger.info("INFO : Setting updated") if logEntry == 1 else None
            return render_template('index.html')
        
        logger.error("ERROR : Setting NOT updated") if logEntry == 1 else None
        return render_template('index.html')
    
    
@app.route('/settingsUpdate1', methods=['POST']) 
async def settingsUpdate1():
        error_message = None
        if request.method == 'POST':  
            mill = request.form['mill']
            machinetype = request.form['machinetype']
            machineno = request.form['machineno']
            dia = request.form['dia']
            gg = request.form['gg']
            party = request.form['party']
            needle_drop = request.form['needledrop']
            count = request.form['count']
            denier = request.form['denier']
            fabric_type = request.form['fabric']
            knittype = request.form['knittype']
            gsm_ll = request.form['gsm']
            ll = request.form['ll']
            roll_weight = request.form['rollweight']
            doff = request.form['rotations']
            lot = request.form['lot']
            job_no = request.form['jobnumber']
            print("mill :",mill)
            print("machinetype :",machinetype)
            print("machineno :",machineno)
            print("dia :",dia)
            print("gg :",gg)
            print("party :",party)
            print("needle_drop :",needle_drop)
            print("count :",count)
            print("denier :",denier)
            print("fabric_type :",fabric_type)
            print("knittype :",knittype)
            print("gsm_ll :",gsm_ll)
            print("ll :",ll)
            print("roll_weight :",roll_weight)
            print("doff :",doff)
            print("lot :",lot)
            print("job_no :",job_no)  
            db.db.update_setting1(mill,machinetype,machineno,dia,gg,party,needle_drop,count,denier,fabric_type,knittype,gsm_ll,ll,roll_weight,doff,lot,job_no)
            logger.info("INFO : Setting updated") if logEntry == 1 else None
            return render_template('index.html')
        
        logger.error("ERROR : Setting NOT updated") if logEntry == 1 else None
        return render_template('index.html')
      
     
class TimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@app.route('/get_min_max_rollnumber', methods=['POST', 'GET'])
async def getMinMaxRollnumber():       
        data = db.db.getMinMaxRollnumber()
        formatted_data ={ 
         "min_rollnumber": data[0][0], 
         "max_rollnumber": data[0][1]
         }
        logger.info("INFO : get_min_max_rollnumber Success") if logEntry == 1 else None        
        response = jsonify(formatted_data)
        return response 



@app.route('/getdefectlog/<report_date>', methods=['POST', 'GET'])
def getdefectLog(report_date):
    if request.method == 'POST':
        defectLogRollId = report_date
        data = db.db.getdefectlog_data(defectLogRollId)

        formatted_data = [
            {
                "defect_name": item[0],
                "roll_name": item[1],
                "timestamp": item[2].strftime("%Y-%m-%d %H:%M:%S"),
                "src": convert_to_base64(item[3])  # Convert image to base64 here
            }
            for item in data
        ]
        formatted_data = tuple(formatted_data)
        json_data = json.dumps(formatted_data, cls=TimeEncoder)
        response = jsonify(json_data)
        return response
    

@app.route('/uptimestatus')
async def uptime_status():
     data = db.db.uptimestatus()
     return jsonify(data)
     
    
@app.route('/check_server_statuses', methods=['GET'])
def check_server_statuses():
    server_urls = [
        "http://localhost:8001/",  # ML microservice
        "http://localhost:8004/",   # alarm microservice
        "http://localhost:8002/"   # monitor microservice
    ]

    
    server_statuses = [checkserver(url) for url in server_urls]
    return jsonify(server_statuses)


def convert_to_base64(source):
    config = ConfigParser()
    config.read('config_webui.ini')
    defect_photo_path_prefix = config.get('defectImgPath', 'defect_photo_path_prefix')
    source = defect_photo_path_prefix + source
    try:
        with open(source, "rb") as img_file:
            file_content = img_file.read()
            if not file_content:
                print('Error: Empty file or file not found')
                return None

            encoded_string = base64.b64encode(file_content).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"

    except Exception as e:
        print(f'Error converting to base64: {str(e)}')
        return None



# main driver function
if __name__ == '__main__':
	app.run(host="127.0.0.1",port=5002,debug=True)
   