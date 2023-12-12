import pandas as pd
import psycopg2
import time
import random
import pytz
import datetime
from configparser import ConfigParser

tz = pytz.timezone("Asia/Kolkata")

class Execute:
    def __init__(self):
        self.keepalive_kwargs = {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 5,
            "keepalives_count": 5,
        }
        self.conn = self.connect()

    def connect(self):
        conn = psycopg2.connect(
            host='localhost',
            database='knitting',
            user='postgres',
            password='55555'
        )
        cursor = conn.cursor()
        conn.autocommit = True
        return conn

    def select(self, query, result_type=1):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            if result_type == 1:
                data = cursor.fetchall()
            else:
                data = cursor.fetchone()
            cursor.close()
            return data
        except Exception as e:
            print(f"Error: {e}")

    def update(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(f"Error: {e}")

    def insert(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            cursor.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def insert_return_id(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            id = cursor.fetchone()[0]
            cursor.close()
            return id
        except Exception as e:
            print(f"Error: {e}")
            return False

class ClientsideDB:
    def __init__(self):
        self.execute = Execute()

    # Functions from your new code
    def select_querydb(self, query, result_type=1):
        pass

    def update_querydb(self, query):
        pass

    def get_base64_image_data(self):
        query = "SELECT image FROM live_image WHERE image_id=1;"
        base64_image = self.execute.select(query, result_type=2)
        if base64_image:
            return str(base64_image[0])
        return None

    def get_machine_details(self):
        try:
            query = "SELECT machinedtl_number, machine_status,machinedtl_name FROM machine_details;"
            data = self.execute.select(query, result_type=2)
            return data
        except Exception as e:
            print(f"Error in get_machine_details: {e}")
            

    def get_BottomBar(self):
        query = """
        SELECT
        rd.roll_name,
        rd.revolution,
        mpd.fabric_type,
        mpd.doff
        FROM
            roll_details rd
        CROSS JOIN (
            SELECT
                fabric_type,
                doff
            FROM
                machine_program_details
            ORDER BY
                machineprgdtl_id DESC
            LIMIT 1
        ) AS mpd
        WHERE
        rd.roll_sts_id = 1;
        """
        data = self.execute.select(query, result_type=2)
        return data

    def getAlarm_Status(self):
        query = """
        SELECT
            *
        FROM 
            public.alarm_status as ast 
            where 
            ast.alarm_status=1
        """
        data = self.execute.select(query, result_type=2)        
        if data==None:
            return 0
        return 1

    def get_defect_details(self):
        query=("""SELECT 
            dtt.defect_name as defect_name,
            rdt.roll_name,
            ast.timestamp,
            CONCAT(ddt.file_path,
            ddt.filename) as file_path
        FROM 
            public.alarm_status as ast 
        left join 
            defect_details as ddt
        on 
            ast.defect_id=ddt.defect_id
        left join 
            defect_type as dtt
        on 
            ddt.defecttyp_id = dtt.defecttyp_id
        left join 
            roll_details rdt
        on 
            ddt.roll_id = rdt.roll_id
        -- where ast.alarm_status=1
        order by ast.timestamp desc limit 1;""")
        data = self.execute.select(query, result_type=2)        
        return data

    def get_moreinfo(self):
        query = ("SELECT * FROM machine_program_details WHERE machineprogram_sts_id = '1';")    
        data = self.execute.select(query, result_type=2)        
        return data
    
    def get_saved_info(self,saved_program_no):
        query = (f"select machineprgdtl_id from public.savedprgm_details where savedprgm_id = '{saved_program_no}'")    
        machine_program_no = self.execute.select(query, result_type=2)   
        print(machine_program_no[0])
        query = (f"SELECT * FROM machine_program_details WHERE machineprgdtl_id = '{machine_program_no[0]}';")    
        data = self.execute.select(query, result_type=2)        
        print(data)
        return data
    
    def get_moreinfo1(self):
        query = ("select machinedtl_name,machine_type,machinedtl_number from public.machine_details")    
        data = self.execute.select(query, result_type=2)        
        return data
    
    def get_rollid(self):
        try:
            query = """
                SELECT roll_id
                FROM roll_details
                ORDER BY roll_id DESC
                LIMIT 1;
            """
            result = self.execute.select(query, result_type=2)
            roll_id = result[0] if result else None
            print("Roll ID:", roll_id)
            return roll_id
        except Exception as e:
            print(f"Error fetching recent roll ID from the database: {e}")
            return None


    def update_doff(self, doff, c_doff=0, order=0, roll=0, shiftdet=0):
        try:
            # Get the active roll ID
            roll_id = self.execute.select("SELECT roll_id FROM roll_details WHERE roll_sts_id = '1'")[0]

            # Update the roll's order number, roll number, and shift number
            update_roll_query = f"UPDATE roll_details SET order_no = '{order}', roll_number = '{roll}', shift_no = '{shiftdet}' WHERE roll_id = '{roll_id}'"
            self.execute.update(update_roll_query)

            # Update the doff in machine_program_details
            update_doff_query = f"UPDATE machine_program_details SET doff = '{doff}' WHERE machineprgdtl_id = (SELECT machineprgdtl_id FROM machine_program_details ORDER BY machineprgdtl_id DESC LIMIT 1)"
            self.execute.update(update_doff_query)
        except Exception as e:
            print(f"Error: {e}")

    def update_saved_program(self):
        try:
            query = "SELECT machineprgdtl_id FROM machine_program_details WHERE machineprogram_sts_id = '1';"
            machineprgdtl_id = self.execute.select(query, result_type=2)
            print('machineprgdtl_id: ', machineprgdtl_id[0])
            query = "SELECT COUNT(machineprgdtl_id) FROM public.savedprgm_details;"
            saved_program_count = self.execute.select(query, result_type=2)
            print('saved_program_count: ', saved_program_count[0])
            tz = pytz.timezone("Asia/Kolkata")  
            timestamp_ = str(datetime.datetime.now(tz)).replace(" ", "_")
            if saved_program_count[0]==3:
                query = f"""
                    UPDATE public.savedprgm_details
                    SET  machineprgdtl_id='{machineprgdtl_id[0]}' , "timestamp"='{timestamp_}'
                    WHERE 
                    savedprgm_id = (select savedprgm_id FROM public.savedprgm_details ORDER BY  timestamp limit 1);
                        """
                self.execute.update(query)
                   
        except Exception as e:
            error_message = str(e)
            print("eroor in update_setting")
    
    def update_setting(self, mill,machinetype,machineno,dia,gg,party,needle_drop,count,denier,fabric_type,knittype,gsm_ll,ll,roll_weight,doff,lot,job_no):
        tz = pytz.timezone("Asia/Kolkata")  
        timestamp_ = str(datetime.datetime.now(tz)).replace(" ", "_")

        try:
            query = "SELECT machineprgdtl_id FROM machine_program_details WHERE machineprogram_sts_id = '1';"
            machineprgdtl_id = self.execute.select(query, result_type=2)
            print('machineprgdtl_id: ', machineprgdtl_id)
            
            query2 = f"UPDATE machine_program_details SET machineprogram_sts_id = '2' WHERE machineprgdtl_id = '{machineprgdtl_id[0]}';"
            self.execute.update(query2)
            
            query2 = f"UPDATE public.machine_details SET machinedtl_name = '{machineno}',machine_type='{machinetype}' WHERE machinedtl_id = '1';"
            self.execute.update(query2)
            
            query = f"""
            INSERT INTO machine_program_details (mill,dia,gg,party,needle_drop,count,denier,fabric_type,knit_type,gsm,loop_length,roll_weight,doff,lot,job_no, timestamp, machineprogram_sts_id)
            VALUES (
                '{mill}',
                '{dia}',
                '{gg}',
                '{party}',
                '{needle_drop}',
                '{count}',
                '{denier}',
                '{fabric_type}',
                '{knittype}',
                '{gsm_ll}',
                '{ll}',
                '{roll_weight}',
                '{doff}',
                '{lot}',
                '{job_no}',
                '{timestamp_}',
                '1'
            );
            """
            self.execute.update(query)
            print("data inserted successfully")
        except Exception as e:
            error_message = str(e)
            print("eroor in update_setting")
            
    def updateAlarm_status(self):
        query = """
        SELECT
            alarm_id
        FROM 
            public.alarm_status as ast 
        WHERE 
            ast.alarm_status = 1
        """
        alarm_id = self.execute.select(query, result_type=2)
        if alarm_id:
            query2 = f"""
            UPDATE public.alarm_status
            SET alarm_status = 3
            WHERE alarm_id = {alarm_id[0]}
            """
            self.execute.update(query2)
            return "ok"

    def startNewRoll_Update(self):
        try:
            # Get active roll ID
            query = "SELECT roll_id, roll_name FROM roll_details WHERE roll_sts_id = '1'"
            roll_data = self.execute.select(query, result_type=2)
            if roll_data:
                roll_id, roll_name = roll_data
                # Update active roll status to '2'
                update_query = f"UPDATE roll_details SET roll_sts_id = '2' WHERE roll_id = '{roll_id}'"
                self.execute.update(update_query)
                # Calculate the next roll name
                next_roll_name = int(roll_name) + 1
            else:
                # If no active roll found, start from 1
                next_roll_name = 1

            # Get the current timestamp in the desired format
            current_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            query = "SELECT machineprgdtl_id FROM machine_program_details WHERE machineprogram_sts_id = '1';"
            machineprgdtl_id = self.execute.select(query, result_type=2)
            # Insert a new roll
            insert_query = (
                "INSERT INTO roll_details (roll_name, roll_start_date, roll_sts_id, revolution, timestamp,machineprgdtl_id) "
                f"VALUES ('{next_roll_name}', '{current_time}', '1', '0', '{current_time}','{machineprgdtl_id[0]}')"
            )
            if self.execute.insert(insert_query):
                print("New roll started successfully.")
            else:
                print("Failed to start a new roll.")
        except Exception as e:
            print(f"Error in startNewRoll_Update: {e}")

    def defect_data(self):
        query = """
        SELECT dtt.defect_name, count(ddt.defect_id) 
        FROM public.defect_details ddt
        RIGHT JOIN 
            public.defect_type dtt
        ON 
            ddt.defecttyp_id = dtt.defecttyp_id
        inner join
            public.alarm_status ast
        ON 
            ast.defect_id = ddt.defect_id
        WHERE ddt.roll_id = (SELECT roll_id FROM public.roll_details WHERE roll_sts_id = '1')
        group by dtt.defect_name;
        """    
        data = self.execute.select(query)        
        return data

    def getAlarmSetting(self):
        query = """
                    select dtt.defecttyp_id, dtt.defect_name, adt.minimum_alarm_count, adt.score, adt.alarm_status, adt.defect_length 
                    from public.defect_type dtt 
                    left join alarm_definition adt
                    on adt.defecttyp_id=dtt.defecttyp_id
                    order by dtt.defecttyp_id
                        """
        data = self.execute.select(query)  
        return data

    def getCameraSetting(self):
        query = """
                    Select cam_id,cam_name, camsts_id from public.cam_details ORDER BY cam_id;
                        """
        data = self.execute.select(query)  
        return data
    
    
    def getMinMaxRollnumber(self):
        query = """
                    SELECT 
                        min(rdt.roll_name) as min_roll_number,
                        max(rdt.roll_name) as max_roll_number
                    FROM 
                        public.alarm_status as ast 
                    left join 
                        defect_details as ddt
                    on 
                        ast.defect_id=ddt.defect_id
                    left join 
                        defect_type as dtt
                    on 
                        ddt.defecttyp_id = dtt.defecttyp_id
                    left join 
                        roll_details rdt
                    on 
                        ddt.roll_id = rdt.roll_id
                    where date(ast.timestamp) = (select date(timestamp) from public.alarm_status order by timestamp desc limit 1);
                        """
        data = self.execute.select(query) 
        return data
    
    
    def getdefectlog_data(self, defectLogRollId):
        try:
            query = f"""
                    SELECT 
                    dtt.defect_name as defect_name,
                    rdt.roll_name,
                    ast.timestamp,
                    CONCAT(ddt.file_path,
                    ddt.filename) as file_path
                FROM 
                    public.alarm_status as ast 
                left join 
                    defect_details as ddt
                on 
                    ast.defect_id=ddt.defect_id
                left join 
                    defect_type as dtt
                on 
                    ddt.defecttyp_id = dtt.defecttyp_id
                left join 
                    roll_details rdt
                on 
                    ddt.roll_id = rdt.roll_id
                where 
                   date(ast.timestamp) = (select date(timestamp) from public.alarm_status order by timestamp desc limit 1) and rdt.roll_name='{defectLogRollId}'
                -- date(ast.timestamp) = '2023-10-20'
                order by ast.timestamp  ;
                
            """
            data = self.execute.select(query) 
            return data
        except Exception as e:
            print(f"Error: {e}")
    
    def getShiftSetting(self):
        query = """select shift_id,shift_name,start_time,end_time from public.shift_details ORDER BY shift_id ASC"""
        data = self.execute.select(query)        
        return data 

    def updatebypass(self, full_bypass, alarm_bypass, sensor_bypass):
        try:
            query = "UPDATE public.bypass_details SET bypass_status = %s WHERE bypass_name = %s;"
            data = [(alarm_bypass, 'alarm_bypass'), (full_bypass, 'full_bypass'), (sensor_bypass, 'sensor_bypass')]

            conn = self.execute.conn
            cursor = conn.cursor()
            for value, name in data:
                cursor.execute(query, (str(value), name))
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error: {e}")

    def updateMachineName(self, machineName):
        try:
            query = f"UPDATE public.machine_details SET machinedtl_name = '{machineName}' WHERE machinedtl_id=1;"
            conn = self.execute.conn
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error: {e}")
    
    def getBypassStatus(self):
        query = """
        select bypass_status from bypass_details;
        """    
        data = self.execute.select(query)        
        full_bypass = True if data[1][0]=='1' else False
        alarm_bypass = True if data[0][0]=='1' else False
        sensor_bypass = True if data[2][0]=='1' else False
        return full_bypass,alarm_bypass,sensor_bypass
    
    def getMachineName(self):
        query = """
        SELECT machinedtl_name FROM public.machine_details;
        """    
        data = self.execute.select(query,result_type=2)        
        return data[0]

    def updateRecording(self, bypass_livecamera, bypass_saveimg, bypass_imgpath, bypass_fps):
        try:
            # Update the recording settings in the database
            query = f"""
                UPDATE public.recording_settings
                SET livecamera_status = '{bypass_livecamera}',
                    saveimage_status = '{bypass_saveimg}',
                    image_path = '{bypass_imgpath}',
                    fps = '{bypass_fps}'
                WHERE recordingset_id = 1;
            """
            self.execute.update(query)
        except Exception as e:
            print(f"Error: {e}")

    def turnOffliveImg(self):
        try:
            # Update the recording settings in the database
            query = f"""
                UPDATE public.recording_settings
                SET livecamera_status = '2',
                    saveimage_status = '2'
                WHERE recordingset_id = 1;
            """
            self.execute.update(query)
        except Exception as e:
            print(f"Error: {e}")

    def getRecording(self):
        query = """
        SELECT livecamera_status,
        saveimage_status,
        image_path,
        fps 
        FROM public.recording_settings where recordingset_id=1;
        """
        data = self.execute.select(query, result_type=2)

        if data:
            livecamera_status = True if data[0] == '1' else False
            saveimage_status = True if data[1] == '1' else False
            image_path = data[2]
            fps = data[3]
        else:
            # Set default values if no data is found
            livecamera_status = False
            saveimage_status = False
            image_path = ""
            fps = 0

        return livecamera_status, saveimage_status, image_path, fps


    def updateAlarmSetting(self,data):
        # Extract keys that contain 'minimumAlarmCountInput'
        count_keys = [key for key in data.keys() if key.startswith('minimumAlarmCountInput')]
        score_keys = [key for key in data.keys() if key.startswith('scoreInput')]
        defect_len_keys = [key for key in data.keys() if key.startswith('defect_lengthInput')]
        alarmStatus_keys = [key for key in data.keys() if key.startswith('alarmStatusInput')]
        adefecTypeId_keys = [key for key in data.keys() if key.startswith('adefecTypeId')]
        adefectName_keys = [key for key in data.keys() if key.startswith('adefectName')]

        # Create a dictionary for DataFrame
        df_data = {
            'minimumAlarmCountInput': [data[key] for key in count_keys],
            'scoreInput': [data[key] for key in score_keys],
            'defect_len_Input': [data[key] for key in defect_len_keys],
            'adefecTypeId': [data[key] for key in adefecTypeId_keys],
            'adefectName': [data[key] for key in adefectName_keys]
        }

        # Create a DataFrame
        df = pd.DataFrame(df_data)

        # Update 'alarmStatus' based on the available 'alarmStatusInput' keys
        alarm_status_data = {key: value for key, value in data.items() if key.startswith('alarmStatusInput')}
        for key, value in alarm_status_data.items():
            adefecTypeId = key.split('alarmStatusInput')[1]
            df.loc[df['adefecTypeId'] == adefecTypeId, 'alarmStatus'] = '1'

        # Set 'alarmStatus' to 'off' for rows without 'alarmStatusInput'
        try:
            df['alarmStatus'].fillna('2', inplace=True)
        except:
            df['alarmStatus']='2'
            
        try:
            df['minimumAlarmCountInput'].fillna(0, inplace=True)
        except:
            df['minimumAlarmCountInput']= 2
            
        # df = df.astype({"minimumAlarmCountInput": int})
    


        # Iterate through the DataFrame and insert each row into the table
        for index, row in df.iterrows():
            alarm_definition_id = row['adefecTypeId']
            minimum_alarm_count = row['minimumAlarmCountInput']
            if not minimum_alarm_count:  # Handle empty string
                minimum_alarm_count = 0
            score = row['scoreInput']
            defect_len = row['defect_len_Input']
            alarm_status = row['alarmStatus']
            # Insert the row into the table
            
            # try:
            insert_query = (
            "INSERT INTO public.alarm_definition (alarm_definition_id, defecttyp_id, minimum_alarm_count, score, alarm_status,defect_length) "
                f"VALUES ('{alarm_definition_id}', '{alarm_definition_id}', '{minimum_alarm_count}','{(int(score)/100)}', '{alarm_status}', '{(int(defect_len)/100)}')"
            )
            if self.execute.insert(insert_query):
                print("Newly Inserted!")               
            else:
                print("working Except in alarmsetting")
                query = f"""
                update alarm_definition
                SET minimum_alarm_count='{minimum_alarm_count}',
                    score='{(int(score)/100)}',
                    defect_length='{(int(defect_len)/100)}',
                    alarm_status='{alarm_status}'                    
                WHERE defecttyp_id='{alarm_definition_id}';
                """
                self.execute.update(query)
                
    def updateCameraSetting(self,data):
        # Extract keys that contain 'minimumAlarmCountInput'
        cameraStatus_keys = [key for key in data.keys() if key.startswith('cameraStatusInput')]
        acameraId_keys = [key for key in data.keys() if key.startswith('cameraId')]
        bcameraName_keys = [key for key in data.keys() if key.startswith('cameraName')]

        # Create a dictionary for DataFrame
        df_data = {
            'acameraId': [data[key] for key in acameraId_keys],
            'bcameraName': [data[key] for key in bcameraName_keys]
        }

        # Create a DataFrame
        df = pd.DataFrame(df_data)
        print(df)
        # Update 'alarmStatus' based on the available 'alarmStatusInput' keys
        cameraStatus_data = {key: value for key, value in data.items() if key.startswith('cameraStatusInput')}
        for key, value in cameraStatus_data.items():
            acameraId = key.split('cameraStatusInput')[1]
            df.loc[df['acameraId'] == acameraId, 'cameraStatus'] = '1'

        # Set 'alarmStatus' to 'off' for rows without 'alarmStatusInput'
        try:
            df['cameraStatus'].fillna('2', inplace=True)
        except:
            df['cameraStatus']='2'
            
    


        # Iterate through the DataFrame and insert each row into the table
        for index, row in df.iterrows():
            camera_definition_id = row['acameraId']
            bcameraName = row['bcameraName']
            camera_status = row['cameraStatus']
            # Insert the row into the table
            
            # try:
            insert_query = (
            "INSERT INTO public.cam_details (cam_id,cam_name, camsts_id) "
                f"VALUES ('{camera_definition_id}', '{bcameraName}', '{camera_status}')"
            )
            if self.execute.insert(insert_query):
                print("Newly Inserted!")               
            else:
                print("working Except in camerasetting")
                query = f"""
                update cam_details
                SET cam_name='{bcameraName}',
                    camsts_id='{camera_status}'                    
                WHERE cam_id='{camera_definition_id}';
                """
                self.execute.update(query)
                print('camera updated!')
    def uptimestatus(self):
        query="""
                SELECT camera_status, controller_status, machine_status, software_status
                FROM uptime_status
                ORDER BY uptimestatus_id DESC
                LIMIT 1;

                """
        data = self.execute.select(query)  
        return data

    
    def updateShiftsetting(self, data):
        try:
            # Create a connection to the database
            conn = self.execute.conn
            cursor = conn.cursor()

            # Extract keys that contain 'shift_id', 'shift_name', 'start_time', and 'end_time'
            id_keys = [key for key in data.keys() if key.startswith('shift_id')]
            name_keys = [key for key in data.keys() if key.startswith('shift_name')]
            stime_keys = [key for key in data.keys() if key.startswith('start_time')]
            etime_keys = [key for key in data.keys() if key.startswith('end_time')]

            for id_key, name_key, stime_key, etime_key in zip(id_keys, name_keys, stime_keys, etime_keys):
                shift_id = data[id_key]
                shift_name = data[name_key]
                start_time = data[stime_key]
                end_time = data[etime_key]

                # Build the SQL query to update the shift
                query = f"""
                UPDATE public.shift_details
                SET shift_name = '{shift_name}',
                    start_time = '{start_time}',
                    end_time = '{end_time}'
                WHERE shift_id = {shift_id};
                """

                # Execute the SQL query
                cursor.execute(query)

            # Commit the changes to the database
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()

# # Main entry point
# if __name__ == "__main__":
#     # Initialize and use the ClientsideDB class to interact with the database
db = ClientsideDB()
# data = db.get_saved_info('3')
# print(data)