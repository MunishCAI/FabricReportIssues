import psycopg2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import datetime
from datetime import timedelta
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import matplotlib.image as mpimg
import locale
from collections import Counter
import os
from configparser import ConfigParser

locale.setlocale(locale.LC_TIME, 'C')
encoding = 'utf-8'



def shift_c(start_date, end_date, shift,version,machine,countai_img,mill_img):
    conn = psycopg2.connect(
            host='localhost',
            database='knitting',
            user='postgres',
            password='55555'
        )
    print(machine)
    cursor = conn.cursor()
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    num_days = (end_date - start_date).days + 1
    pdf_buffer = BytesIO()
    pdf_pages = PdfPages(pdf_buffer)
    plt.ioff()

    for i in range(num_days):

        current_date = start_date + datetime.timedelta(days=i)
        new_date = current_date + datetime.timedelta(days=i+1)


        fig, (ax, ax1 ) = plt.subplots(2, 1, figsize=(21, 31))
        # ax3 = ax2.twinx()
    
        plt.subplots_adjust(hspace=0.999)
        
        logo_path = mill_img
        logo_img = mpimg.imread(logo_path)
        ax_logo = fig.add_subplot(1, 1, 1)
        logo_y_position = 0.899999
        ax_logo.set_position([0.05, logo_y_position, 0.1, 0.1]) 
        logo_width = 0.1
        ax_logo.imshow(logo_img, extent=[0, logo_width, 0, logo_width * logo_img.shape[0] / logo_img.shape[1]])
        ax_logo.axis('off')
        ax_logo.set_frame_on(False)
        
        logo_path_2 = countai_img
        logo_img = mpimg.imread(logo_path_2)
        ax_logo = fig.add_subplot(1, 1, 1)
        logo_y_position = 0.846
        ax_logo.set_position([0.77, logo_y_position, 0.2, 0.2])  
        logo_width = 0.2  
        ax_logo.imshow(logo_img, extent=[0, logo_width, 0, logo_width * logo_img.shape[0] / logo_img.shape[1]])
        ax_logo.axis('off')
        ax_logo.set_frame_on(False)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
        ax.text(-0.150, 0.995, f"Machine Name: {GetMachineName()}", fontsize=40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.895, "Fabric Code:", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.795, "Material Type:", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(0.80, 0.995, f"Date: {current_date}", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(0.80, 0.895, "Time :6AM to 6PM", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.65, "Fabric Inspection Report", fontsize = 40, color='red', fontfamily='Arial')
        # ax.text(-0.150, -2.4, "Production Report & Defect Report", fontsize = 40, color='red', fontfamily='Arial')
        ax1.text(-0.130, -0.315, f"Pdf generated on : {formatted_datetime}", fontsize = 25, color='black')
        ax1.text(0.90, -0.315, f"Version : {version} ", fontsize = 25, color='black')
        ax.axis('off')
        ax1.axis('off')
        # ax2.axis('off')

        cursor.execute("SELECT start_time, end_time FROM shift_details WHERE shift_name = 'C'")
        shift = cursor.fetchone()  
        start_time, end_time = shift
        cursor.execute(
        "SELECT roll_number, roll_start_date, roll_name, roll_id, revolution,roll_end_date FROM public.roll_details WHERE roll_start_date >=  '"+str(current_date)+" "+str(start_time)+"' AND roll_start_date < '"+str(new_date)+" "+str(end_time)+"' ORDER BY roll_id ASC;")
        roll = cursor.fetchall()
        roll = [data for data in roll if data[1] != "0"]
        roll_details_df = pd.DataFrame(roll, columns=['Roll id', 'Start Time', 'Knit id', 'id','No of Doff','End Time'])
        
    #     cursor.execute(
    #     "SELECT roll_number, roll_start_date, roll_name, roll_id, revolution ,roll_end_date FROM public.roll_details WHERE roll_end_date >= %s::timestamp + '06:00:00'::interval AND roll_end_date < %s::timestamp + '08:00:00'::interval ORDER BY roll_id ASC;",
    #     (current_date,new_date)
    # )
    #     roll = cursor.fetchall()
    #     roll = [data for data in roll if data[1] != "0"]
    #     roll_details_df = pd.DataFrame(roll, columns=['Roll id', 'Start Time', 'Knit id', 'id','No of Doff','End Time'])
        

        if roll_details_df.empty:
            pdf_pages.close()
            return pdf_buffer, False
        
        
        if len(roll_details_df) == 1:
            roll_details_df.fillna("running", inplace=True)
            roll_details_df['Time Taken'] = "running"
            roll_details_df['Start Time'] = roll_details_df['Start Time'].dt.strftime('%H:%M')
            roll_details_df['End Time'] = roll_details_df['End Time'].dt.strftime('%H:%M')            

        else:

            last_row_index = len(roll_details_df) - 1
            
            if last_row_index >= 0:
                roll_details_df.at[last_row_index, 'End Time'] = 'running'  

            roll_details_df = roll_details_df.dropna(subset=['Start Time', 'End Time'])

            first_row_index = 0
            roll_details_df['Start Time'] = pd.to_datetime(roll_details_df['Start Time'], format="%H:%M:%S.%f", errors='coerce', exact=False)
            roll_details_df['End Time'] = pd.to_datetime(roll_details_df['End Time'], format="%H:%M:%S.%f", errors='coerce', exact=False) 
            roll_details_df['Start Time'] = roll_details_df['Start Time'].dt.strftime('%H:%M')
            roll_details_df['End Time'] = roll_details_df['End Time'].dt.strftime('%H:%M')

            start = pd.to_datetime(roll_details_df.at[first_row_index, 'Start Time'])
            end = pd.to_datetime(roll_details_df.at[first_row_index, 'End Time']) - timedelta(days=1)
            diff = end - start
            hours = int(diff.seconds // 3600)
            minutes = int((diff.seconds // 60) % 60)
            roll_details_df.at[first_row_index, 'Time Taken'] = f"{hours}h {minutes}m"

            for row_index in range(1, len(roll_details_df) - 1):
                start_time = pd.to_datetime(roll_details_df.at[row_index, 'Start Time'])
                end_time = pd.to_datetime(roll_details_df.at[row_index, 'End Time'])
                
                if end_time < start_time:
                    end_time += pd.DateOffset(days=1)
                
                time_difference = end_time - start_time
                total_seconds = time_difference.total_seconds()
                
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                roll_details_df.at[row_index, 'Time Taken'] = f"{hours}h {minutes}m"


        id_list = roll_details_df['id'].tolist()
        fetched_data = []
          

        for id_value in id_list:
            query = """
            SELECT
            dd.timestamp AS timestamp,
            dt.defect_name AS defect_type,
            dd.revolution AS revolution,
            rd.roll_name AS roll_name,
            dd.roll_id AS defect_roll_id
            FROM defect_details dd
            JOIN alarm_status AS a ON a.defect_id = dd.defect_id
            JOIN defect_type AS dt ON dd.defecttyp_id = dt.defecttyp_id
            JOIN roll_details AS rd ON dd.roll_id = rd.roll_id
            WHERE dd.roll_id = %s
            ORDER BY dd.timestamp;
            """
            
            cursor.execute(query, (id_value,))
            data = cursor.fetchall()
            
            fetched_data.append(data)


        columns = ["timestamp", "defect_type", "revolution", "roll_name", "defect_roll_id"]
        defect_df = pd.DataFrame([item for sublist in fetched_data for item in sublist], columns=columns)
        
        lycra_counts = []
        needle_counts = []
        hole_counts = []
        other_defects = []

        for roll_id in roll_details_df['id']:
            
            roll_defects = defect_df[defect_df['defect_roll_id'] == roll_id]
            defect_counts = {'lycra': 0, 'needln': 0, 'hole': 0}
            other_defect_counts = {}

            for _, defect_row in roll_defects.iterrows():
                defect_type = defect_row['defect_type']

                if defect_type in defect_counts:
                    defect_counts[defect_type] += 1
                else:
                    if defect_type not in other_defect_counts:
                        other_defect_counts[defect_type] = 1
                    else:
                        other_defect_counts[defect_type] += 1

            lycra_counts.append(defect_counts['lycra'])
            needle_counts.append(defect_counts['needln'])
            hole_counts.append(defect_counts['hole'])

            if not other_defect_counts:
                other_defects.append('0')
            else:
                formatted_other_defects = ''.join([f'{defect_type}: {count}\n' for defect_type, count in other_defect_counts.items()])
                # print("**********************************")
                # print(formatted_other_defects)
                other_defects.append(formatted_other_defects)

        
        roll_details_df['Lycra Defects'] = lycra_counts
        roll_details_df['Needle Defects'] = needle_counts
        roll_details_df['Hole Defects'] = hole_counts
        roll_details_df['Other Defects'] = other_defects
        roll_details_df.fillna("running", inplace=True)
        roll_details_df['No of Doff'] = pd.to_numeric(roll_details_df['No of Doff'], errors='coerce')
        roll_details_df = roll_details_df[(roll_details_df['No of Doff'].notna()) & (roll_details_df['No of Doff'] != 0)]
        roll_details_df['Knit id'] = range(1, len(roll_details_df) + 1)
        defect_df = defect_df.merge(roll_details_df[['id', 'Knit id']], left_on='defect_roll_id', right_on='id', how='left')
        defect_df.drop(columns=['defect_roll_id','id','roll_name'], inplace=True)
        roll_details_df.drop(columns=['id'], inplace=True)
        roll_details_df.drop(columns=['Roll id'], inplace=True)
        roll_details_df['Decision'] = ''

        column_names_to_select = ['Knit id', 'Start Time', 'End Time', 'Time Taken', 'No of Doff', 'Lycra Defects', 'Needle Defects', 'Hole Defects', 'Other Defects','Decision']
        roll_details_df = roll_details_df[column_names_to_select]
        table_data = roll_details_df.values.tolist()
        # table_data.append([])
        print(table_data)
        # table_data = table_data.append(table_data)
        column_labels = ['Shiftwise\n Roll Id', 'Start\n Time', 'End\n Time', 'Time\n Taken', 'No of\nRevolutions', 'Lycra', 'Needle\nline', 'Hole', 'Other', 'Decision']
        column_widths = [0.08, 0.1, 0.1, 0.1, 0.1, 0.08, 0.08, 0.08, 0.110, 0.130]
        
        table = ax.table(
        cellText=table_data,
        colLabels=column_labels,
        bbox=[-0.130 , -1.99, 1.2, 2.5], 
        colWidths=column_widths,
        cellColours=[['lightgray']*len(table_data[0])]*len(table_data),
        colColours=['lightgray'] * len(column_labels))

        font_size = 20 
        table.auto_set_font_size(False)
        table.set_fontsize(font_size)
        header_height = 0.02
        for key, cell in table.get_celld().items():
            if key[0] == 0: 
                cell.set_height(header_height)

 
        font_family = 'Arial'  
        font_weight = 'bold'
        line_color = 'red'

        for i, label in enumerate(column_labels):
            cell = table[0, i]
            text = cell.get_text()
            print(text)
            text.set_fontfamily(font_family)
            text.set_weight(font_weight)
            
     
        for i in range(len(table_data) + 1):
            for j in range(len(column_labels)):
                cell = table[i, j]
                cell.set_edgecolor(line_color)
                cell._text.set_horizontalalignment('center') 

        pdf_pages.savefig(fig)
        plt.close(fig)

    pdf_pages.close()
    cursor.close()
    conn.close()
    pdf_buffer.seek(0)
    return pdf_buffer, True
    

def shift_a(start_date, end_date, shift,version,machine,countai_img,mill_img):
    

    conn = psycopg2.connect(
            host='localhost',
            database='knitting',
            user='postgres',
            password='55555'
        )
    cursor = conn.cursor()
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    num_days = (end_date - start_date).days + 1
    pdf_buffer = BytesIO()
    pdf_pages = PdfPages(pdf_buffer)
    plt.ioff()

    for i in range(num_days):

        current_date = start_date + datetime.timedelta(days=i)
        new_date = current_date + datetime.timedelta(days=i+1)


        fig, (ax, ax1 ) = plt.subplots(2, 1, figsize=(21, 31))
        # ax3 = ax2.twinx()
    
        plt.subplots_adjust(hspace=0.999)
        
        logo_path = mill_img
        logo_img = mpimg.imread(logo_path)
        ax_logo = fig.add_subplot(1, 1, 1)
        logo_y_position = 0.899999
        ax_logo.set_position([0.05, logo_y_position, 0.1, 0.1]) 
        logo_width = 0.1
        ax_logo.imshow(logo_img, extent=[0, logo_width, 0, logo_width * logo_img.shape[0] / logo_img.shape[1]])
        ax_logo.axis('off')
        ax_logo.set_frame_on(False)
        
        logo_path_2 = countai_img
        logo_img = mpimg.imread(logo_path_2)
        ax_logo = fig.add_subplot(1, 1, 1)
        logo_y_position = 0.846
        ax_logo.set_position([0.77, logo_y_position, 0.2, 0.2])  
        logo_width = 0.2  
        ax_logo.imshow(logo_img, extent=[0, logo_width, 0, logo_width * logo_img.shape[0] / logo_img.shape[1]])
        ax_logo.axis('off')
        ax_logo.set_frame_on(False)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
        ax.text(-0.150, 0.995, f"Machine Name: {GetMachineName()}", fontsize=40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.895, "Fabric Code:", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.795, "Material Type:", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(0.80, 0.995, f"Date: {current_date}", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(0.80, 0.895, "Time :6AM to 6PM", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.65, "Fabric Inspection Report", fontsize = 40, color='red', fontfamily='Arial')
        # ax.text(-0.150, -2.4, "Production Report & Defect Report", fontsize = 40, color='red', fontfamily='Arial')
        ax1.text(-0.130, -0.315, f"Pdf generated on : {formatted_datetime}", fontsize = 25, color='black')
        ax1.text(0.90, -0.315, f"Version : {version} ", fontsize = 25, color='black')
        ax.axis('off')
        ax1.axis('off')
        # ax2.axis('off')

        cursor.execute("SELECT start_time, end_time FROM shift_details WHERE shift_name = 'A'")
        shift = cursor.fetchone()  
        start_time, end_time = shift
        cursor.execute(
        "SELECT roll_number, roll_start_date, roll_name, roll_id, revolution,roll_end_date FROM public.roll_details WHERE roll_start_date >=  '"+str(current_date)+" "+str(start_time)+"' AND roll_start_date < '"+str(current_date)+" "+str(end_time)+"' ORDER BY roll_id ASC;")
        roll = cursor.fetchall()
        roll = [data for data in roll if data[1] != "0"]
        roll_details_df = pd.DataFrame(roll, columns=['Roll id', 'Start Time', 'Knit id', 'id','No of Doff','End Time'])
        
    #     cursor.execute(
    #     "SELECT roll_number, roll_start_date, roll_name, roll_id, revolution ,roll_end_date FROM public.roll_details WHERE roll_end_date >= %s::timestamp + '06:00:00'::interval AND roll_end_date < %s::timestamp + '08:00:00'::interval ORDER BY roll_id ASC;",
    #     (current_date,new_date)
    # )
    #     roll = cursor.fetchall()
    #     roll = [data for data in roll if data[1] != "0"]
    #     roll_details_df = pd.DataFrame(roll, columns=['Roll id', 'Start Time', 'Knit id', 'id','No of Doff','End Time'])
        

        if roll_details_df.empty:
            pdf_pages.close()
            return pdf_buffer, False
        
        
        if len(roll_details_df) == 1:
            roll_details_df.fillna("running", inplace=True)
            roll_details_df['Time Taken'] = "running"
            roll_details_df['Start Time'] = roll_details_df['Start Time'].dt.strftime('%H:%M')

        else:

            last_row_index = len(roll_details_df) - 1
            
            if last_row_index >= 0:
                roll_details_df.at[last_row_index, 'End Time'] = 'running'  

            roll_details_df = roll_details_df.dropna(subset=['Start Time', 'End Time'])

            first_row_index = 0
            roll_details_df['Start Time'] = pd.to_datetime(roll_details_df['Start Time'], format="%H:%M:%S.%f", errors='coerce', exact=False)
            roll_details_df['End Time'] = pd.to_datetime(roll_details_df['End Time'], format="%H:%M:%S.%f", errors='coerce', exact=False) 
            roll_details_df['Start Time'] = roll_details_df['Start Time'].dt.strftime('%H:%M')
            roll_details_df['End Time'] = roll_details_df['End Time'].dt.strftime('%H:%M')

            start = pd.to_datetime(roll_details_df.at[first_row_index, 'Start Time'])
            end = pd.to_datetime(roll_details_df.at[first_row_index, 'End Time']) - timedelta(days=1)
            diff = end - start
            hours = int(diff.seconds // 3600)
            minutes = int((diff.seconds // 60) % 60)
            roll_details_df.at[first_row_index, 'Time Taken'] = f"{hours}h {minutes}m"

            for row_index in range(1, len(roll_details_df) - 1):
                start_time = pd.to_datetime(roll_details_df.at[row_index, 'Start Time'])
                end_time = pd.to_datetime(roll_details_df.at[row_index, 'End Time'])
                
                if end_time < start_time:
                    end_time += pd.DateOffset(days=1)
                
                time_difference = end_time - start_time
                total_seconds = time_difference.total_seconds()
                
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                roll_details_df.at[row_index, 'Time Taken'] = f"{hours}h {minutes}m"


        id_list = roll_details_df['id'].tolist()
        fetched_data = []
          

        for id_value in id_list:
            query = """
            SELECT
            dd.timestamp AS timestamp,
            dt.defect_name AS defect_type,
            dd.revolution AS revolution,
            rd.roll_name AS roll_name,
            dd.roll_id AS defect_roll_id
            FROM defect_details dd
            JOIN alarm_status AS a ON a.defect_id = dd.defect_id
            JOIN defect_type AS dt ON dd.defecttyp_id = dt.defecttyp_id
            JOIN roll_details AS rd ON dd.roll_id = rd.roll_id
            WHERE dd.roll_id = %s
            ORDER BY dd.timestamp;
            """
            
            cursor.execute(query, (id_value,))
            data = cursor.fetchall()
            
            fetched_data.append(data)


        columns = ["timestamp", "defect_type", "revolution", "roll_name", "defect_roll_id"]
        defect_df = pd.DataFrame([item for sublist in fetched_data for item in sublist], columns=columns)
        
        lycra_counts = []
        needle_counts = []
        hole_counts = []
        other_defects = []

        for roll_id in roll_details_df['id']:
            
            roll_defects = defect_df[defect_df['defect_roll_id'] == roll_id]
            defect_counts = {'lycra': 0, 'needln': 0, 'hole': 0}
            other_defect_counts = {}

            for _, defect_row in roll_defects.iterrows():
                defect_type = defect_row['defect_type']

                if defect_type in defect_counts:
                    defect_counts[defect_type] += 1
                else:
                    if defect_type not in other_defect_counts:
                        other_defect_counts[defect_type] = 1
                    else:
                        other_defect_counts[defect_type] += 1

            lycra_counts.append(defect_counts['lycra'])
            needle_counts.append(defect_counts['needln'])
            hole_counts.append(defect_counts['hole'])

            if not other_defect_counts:
                other_defects.append('0')
            else:
                formatted_other_defects = ''.join([f'{defect_type}: {count}\n' for defect_type, count in other_defect_counts.items()])
                # print("**********************************")
                # print(formatted_other_defects)
                other_defects.append(formatted_other_defects)

        
        roll_details_df['Lycra Defects'] = lycra_counts
        roll_details_df['Needle Defects'] = needle_counts
        roll_details_df['Hole Defects'] = hole_counts
        roll_details_df['Other Defects'] = other_defects
        roll_details_df.fillna("running", inplace=True)
        roll_details_df['No of Doff'] = pd.to_numeric(roll_details_df['No of Doff'], errors='coerce')
        roll_details_df = roll_details_df[(roll_details_df['No of Doff'].notna()) & (roll_details_df['No of Doff'] != 0)]
        roll_details_df['Knit id'] = range(1, len(roll_details_df) + 1)
        defect_df = defect_df.merge(roll_details_df[['id', 'Knit id']], left_on='defect_roll_id', right_on='id', how='left')
        defect_df.drop(columns=['defect_roll_id','id','roll_name'], inplace=True)
        roll_details_df.drop(columns=['id'], inplace=True)
        roll_details_df.drop(columns=['Roll id'], inplace=True)
        roll_details_df['Decision'] = ''

        column_names_to_select = ['Knit id', 'Start Time', 'End Time', 'Time Taken', 'No of Doff', 'Lycra Defects', 'Needle Defects', 'Hole Defects', 'Other Defects','Decision']
        roll_details_df = roll_details_df[column_names_to_select]
        table_data = roll_details_df.values.tolist()
        # table_data.append([])
        print(table_data)
        # table_data = table_data.append(table_data)
        column_labels = ['Shiftwise\n Roll Id', 'Start\n Time', 'End\n Time', 'Time\n Taken', 'No of\nRevolutions', 'Lycra', 'Needle\nline', 'Hole', 'Other', 'Decision']
        column_widths = [0.08, 0.1, 0.1, 0.1, 0.1, 0.08, 0.08, 0.08, 0.110, 0.130]
        
        table = ax.table(
        cellText=table_data,
        colLabels=column_labels,
        bbox=[-0.130 , -1.99, 1.2, 2.5], 
        colWidths=column_widths,
        cellColours=[['lightgray']*len(table_data[0])]*len(table_data),
        colColours=['lightgray'] * len(column_labels))

        font_size = 20 
        table.auto_set_font_size(False)
        table.set_fontsize(font_size)
        header_height = 0.02
        for key, cell in table.get_celld().items():
            if key[0] == 0: 
                cell.set_height(header_height)

 
        font_family = 'Arial'  
        font_weight = 'bold'
        line_color = 'red'

        for i, label in enumerate(column_labels):
            cell = table[0, i]
            text = cell.get_text()
            print(text)
            text.set_fontfamily(font_family)
            text.set_weight(font_weight)
            
     
        for i in range(len(table_data) + 1):
            for j in range(len(column_labels)):
                cell = table[i, j]
                cell.set_edgecolor(line_color)
                cell._text.set_horizontalalignment('center') 

        pdf_pages.savefig(fig)
        plt.close(fig)

    pdf_pages.close()
    cursor.close()
    conn.close()
    pdf_buffer.seek(0)
    return pdf_buffer, True


def shift_b(start_date, end_date, shift,version,machine,countai_img,mill_img):
    conn = psycopg2.connect(
            host='localhost',
            database='knitting',
            user='postgres',
            password='55555'
        )
    cursor = conn.cursor()
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    num_days = (end_date - start_date).days + 1
    pdf_buffer = BytesIO()
    pdf_pages = PdfPages(pdf_buffer)
    plt.ioff()

    for i in range(num_days):

        current_date = start_date + datetime.timedelta(days=i)
        new_date = current_date + datetime.timedelta(days=i+1)


        fig, (ax, ax1 ) = plt.subplots(2, 1, figsize=(21, 31))
        # ax3 = ax2.twinx()
    
        plt.subplots_adjust(hspace=0.999)
        
        logo_path = mill_img
        logo_img = mpimg.imread(logo_path)
        ax_logo = fig.add_subplot(1, 1, 1)
        logo_y_position = 0.899999
        ax_logo.set_position([0.05, logo_y_position, 0.1, 0.1]) 
        logo_width = 0.1
        ax_logo.imshow(logo_img, extent=[0, logo_width, 0, logo_width * logo_img.shape[0] / logo_img.shape[1]])
        ax_logo.axis('off')
        ax_logo.set_frame_on(False)
        
        logo_path_2 = countai_img
        logo_img = mpimg.imread(logo_path_2)
        ax_logo = fig.add_subplot(1, 1, 1)
        logo_y_position = 0.846
        ax_logo.set_position([0.77, logo_y_position, 0.2, 0.2])  
        logo_width = 0.2  
        ax_logo.imshow(logo_img, extent=[0, logo_width, 0, logo_width * logo_img.shape[0] / logo_img.shape[1]])
        ax_logo.axis('off')
        ax_logo.set_frame_on(False)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
        ax.text(-0.150, 0.995, f"Machine Name: {GetMachineName()}", fontsize=40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.895, "Fabric Code:", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.795, "Material Type:", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(0.80, 0.995, f"Date: {current_date}", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(0.80, 0.895, "Time :6AM to 6PM", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.65, "Fabric Inspection Report", fontsize = 40, color='red', fontfamily='Arial')
        # ax.text(-0.150, -2.4, "Production Report & Defect Report", fontsize = 40, color='red', fontfamily='Arial')
        ax1.text(-0.130, -0.315, f"Pdf generated on : {formatted_datetime}", fontsize = 25, color='black')
        ax1.text(0.90, -0.315, f"Version : {version} ", fontsize = 25, color='black')
        ax.axis('off')
        ax1.axis('off')
        # ax2.axis('off')

        
        cursor.execute("SELECT start_time, end_time FROM shift_details WHERE shift_name = 'B'")
        shift = cursor.fetchone()  
        start_time, end_time = shift
        cursor.execute(
        "SELECT roll_number, roll_start_date, roll_name, roll_id, revolution,roll_end_date FROM public.roll_details WHERE roll_start_date >=  '"+str(current_date)+" "+str(start_time)+"' AND roll_start_date < '"+str(current_date)+" "+str(end_time)+"' ORDER BY roll_id ASC;")
        roll = cursor.fetchall()
        roll = [data for data in roll if data[1] != "0"]
        roll_details_df = pd.DataFrame(roll, columns=['Roll id', 'Start Time', 'Knit id', 'id','No of Doff','End Time'])
        
    #     cursor.execute(
    #     "SELECT roll_number, roll_start_date, roll_name, roll_id, revolution ,roll_end_date FROM public.roll_details WHERE roll_end_date >= %s::timestamp + '06:00:00'::interval AND roll_end_date < %s::timestamp + '08:00:00'::interval ORDER BY roll_id ASC;",
    #     (current_date,new_date)
    # )
    #     roll = cursor.fetchall()
    #     roll = [data for data in roll if data[1] != "0"]
    #     roll_details_df = pd.DataFrame(roll, columns=['Roll id', 'Start Time', 'Knit id', 'id','No of Doff','End Time'])
        

        if roll_details_df.empty:
            pdf_pages.close()
            return pdf_buffer, False
        
        
        if len(roll_details_df) == 1:
            roll_details_df.fillna("running", inplace=True)
            roll_details_df['Time Taken'] = "running"
            roll_details_df['Start Time'] = roll_details_df['Start Time'].dt.strftime('%H:%M')
            roll_details_df['End Time'] = roll_details_df['End Time'].dt.strftime('%H:%M')            

        else:

            last_row_index = len(roll_details_df) - 1
            
            if last_row_index >= 0:
                roll_details_df.at[last_row_index, 'End Time'] = 'running'  

            roll_details_df = roll_details_df.dropna(subset=['Start Time', 'End Time'])

            first_row_index = 0
            roll_details_df['Start Time'] = pd.to_datetime(roll_details_df['Start Time'], format="%H:%M:%S.%f", errors='coerce', exact=False)
            roll_details_df['End Time'] = pd.to_datetime(roll_details_df['End Time'], format="%H:%M:%S.%f", errors='coerce', exact=False) 
            roll_details_df['Start Time'] = roll_details_df['Start Time'].dt.strftime('%H:%M')
            roll_details_df['End Time'] = roll_details_df['End Time'].dt.strftime('%H:%M')

            start = pd.to_datetime(roll_details_df.at[first_row_index, 'Start Time'])
            end = pd.to_datetime(roll_details_df.at[first_row_index, 'End Time']) - timedelta(days=1)
            diff = end - start
            hours = int(diff.seconds // 3600)
            minutes = int((diff.seconds // 60) % 60)
            roll_details_df.at[first_row_index, 'Time Taken'] = f"{hours}h {minutes}m"

            for row_index in range(1, len(roll_details_df) - 1):
                start_time = pd.to_datetime(roll_details_df.at[row_index, 'Start Time'])
                end_time = pd.to_datetime(roll_details_df.at[row_index, 'End Time'])
                
                if end_time < start_time:
                    end_time += pd.DateOffset(days=1)
                
                time_difference = end_time - start_time
                total_seconds = time_difference.total_seconds()
                
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                roll_details_df.at[row_index, 'Time Taken'] = f"{hours}h {minutes}m"


        id_list = roll_details_df['id'].tolist()
        fetched_data = []
          

        for id_value in id_list:
            query = """
            SELECT
            dd.timestamp AS timestamp,
            dt.defect_name AS defect_type,
            dd.revolution AS revolution,
            rd.roll_name AS roll_name,
            dd.roll_id AS defect_roll_id
            FROM defect_details dd
            JOIN alarm_status AS a ON a.defect_id = dd.defect_id
            JOIN defect_type AS dt ON dd.defecttyp_id = dt.defecttyp_id
            JOIN roll_details AS rd ON dd.roll_id = rd.roll_id
            WHERE dd.roll_id = %s
            ORDER BY dd.timestamp;
            """
            
            cursor.execute(query, (id_value,))
            data = cursor.fetchall()
            
            fetched_data.append(data)


        columns = ["timestamp", "defect_type", "revolution", "roll_name", "defect_roll_id"]
        defect_df = pd.DataFrame([item for sublist in fetched_data for item in sublist], columns=columns)
        
        lycra_counts = []
        needle_counts = []
        hole_counts = []
        other_defects = []

        for roll_id in roll_details_df['id']:
            
            roll_defects = defect_df[defect_df['defect_roll_id'] == roll_id]
            defect_counts = {'lycra': 0, 'needln': 0, 'hole': 0}
            other_defect_counts = {}

            for _, defect_row in roll_defects.iterrows():
                defect_type = defect_row['defect_type']

                if defect_type in defect_counts:
                    defect_counts[defect_type] += 1
                else:
                    if defect_type not in other_defect_counts:
                        other_defect_counts[defect_type] = 1
                    else:
                        other_defect_counts[defect_type] += 1

            lycra_counts.append(defect_counts['lycra'])
            needle_counts.append(defect_counts['needln'])
            hole_counts.append(defect_counts['hole'])

            if not other_defect_counts:
                other_defects.append('0')
            else:
                formatted_other_defects = ''.join([f'{defect_type}: {count}\n' for defect_type, count in other_defect_counts.items()])
                # print("**********************************")
                # print(formatted_other_defects)
                other_defects.append(formatted_other_defects)

        
        roll_details_df['Lycra Defects'] = lycra_counts
        roll_details_df['Needle Defects'] = needle_counts
        roll_details_df['Hole Defects'] = hole_counts
        roll_details_df['Other Defects'] = other_defects
        roll_details_df.fillna("running", inplace=True)
        roll_details_df['No of Doff'] = pd.to_numeric(roll_details_df['No of Doff'], errors='coerce')
        roll_details_df = roll_details_df[(roll_details_df['No of Doff'].notna()) & (roll_details_df['No of Doff'] != 0)]
        roll_details_df['Knit id'] = range(1, len(roll_details_df) + 1)
        defect_df = defect_df.merge(roll_details_df[['id', 'Knit id']], left_on='defect_roll_id', right_on='id', how='left')
        defect_df.drop(columns=['defect_roll_id','id','roll_name'], inplace=True)
        roll_details_df.drop(columns=['id'], inplace=True)
        roll_details_df.drop(columns=['Roll id'], inplace=True)
        roll_details_df['Decision'] = ''

        column_names_to_select = ['Knit id', 'Start Time', 'End Time', 'Time Taken', 'No of Doff', 'Lycra Defects', 'Needle Defects', 'Hole Defects', 'Other Defects','Decision']
        roll_details_df = roll_details_df[column_names_to_select]
        table_data = roll_details_df.values.tolist()
        # table_data.append([])
        print(table_data)
        # table_data = table_data.append(table_data)
        column_labels = ['Shiftwise\n Roll Id', 'Start\n Time', 'End\n Time', 'Time\n Taken', 'No of\nRevolutions', 'Lycra', 'Needle\nline', 'Hole', 'Other', 'Decision']
        column_widths = [0.08, 0.1, 0.1, 0.1, 0.1, 0.08, 0.08, 0.08, 0.110, 0.130]
        print(table_data)
        table = ax.table(
        cellText=table_data,
        colLabels=column_labels,
        bbox=[-0.130 , -1.99, 1.2, 2.5], 
        colWidths=column_widths,
        cellColours=[['lightgray']*len(table_data[0])]*len(table_data),
        colColours=['lightgray'] * len(column_labels))

        font_size = 20 
        table.auto_set_font_size(False)
        table.set_fontsize(font_size)
        header_height = 0.02
        for key, cell in table.get_celld().items():
            if key[0] == 0: 
                cell.set_height(header_height)

 
        font_family = 'Arial'  
        font_weight = 'bold'
        line_color = 'red'

        for i, label in enumerate(column_labels):
            cell = table[0, i]
            text = cell.get_text()
            print(text)
            text.set_fontfamily(font_family)
            text.set_weight(font_weight)
            
     
        for i in range(len(table_data) + 1):
            for j in range(len(column_labels)):
                cell = table[i, j]
                cell.set_edgecolor(line_color)
                cell._text.set_horizontalalignment('center') 

        pdf_pages.savefig(fig)
        plt.close(fig)

    pdf_pages.close()
    cursor.close()
    conn.close()
    pdf_buffer.seek(0)
    return pdf_buffer, True
       
        
    
    

def call_config():
    config = ConfigParser()
    config.read('config_webui.ini')
    directory_path = './static/report'
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    millname = config.get('shift', 'millname')
    version = config.get('shift', 'version')
    machine =  config.get('shift', 'machine')
    countai_img = config.get('shift', 'countai_img')
    mill_img = config.get('shift', 'mill_img')    
    return directory_path,millname,version,machine,countai_img,mill_img 


def shift_C_pdf(report_date):
    directory_path,millname,version,machine,countai_img,mill_img = call_config()
    filename = f"{directory_path}/{millname}_{report_date}_Shift_C.pdf"
    pdf_buffer, has_data = shift_c(report_date,report_date,'c',version,machine,countai_img,mill_img)
    source_path = './static/report'
    if not os.path.exists(source_path):
        os.makedirs(source_path)
    for filename in os.listdir(source_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(source_path, filename)
            os.remove(file_path)
            # print(f"Removed existing PDF: {file_path}")
    if has_data:
            with open(filename, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            local_path = f'./static/report/{millname}_{report_date}_Shift_C.pdf'
            with open(local_path, 'wb') as f:
                f.write(pdf_buffer.getvalue())

            print(f"PDF generated for {report_date}")
            return True
    else:
        print(f"No data found for {report_date}. PDF not generated.")
        return False
    
def shift_B_pdf(report_date):
    directory_path,millname,version,machine,countai_img,mill_img = call_config()
    filename = f"{directory_path}/{millname}_{report_date}_Shift_B.pdf"
    pdf_buffer, has_data = shift_b(report_date,report_date,'b',version,machine,countai_img,mill_img)
    source_path = './static/report'
    if not os.path.exists(source_path):
        os.makedirs(source_path)
    for filename in os.listdir(source_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(source_path, filename)
            os.remove(file_path)
            # print(f"Removed existing PDF: {file_path}")
  
    if has_data:
        with open(filename, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        local_path = f'./static/report/{millname}_{report_date}_Shift_B.pdf'
        with open(local_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())

        print(f"PDF generated for {report_date}")
        return True
    else:
        print(f"No data found for {report_date}. PDF not generated.")
        return False
    
def shift_A_pdf(report_date):
    directory_path,millname,version,machine,countai_img,mill_img = call_config()
    filename = f"{directory_path}/{millname}_{report_date}_Shift_A.pdf"
    pdf_buffer, has_data = shift_a(report_date,report_date,'a',version,machine,countai_img,mill_img)
    source_path = './static/report'
    if not os.path.exists(source_path):
        os.makedirs(source_path)
    for filename in os.listdir(source_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(source_path, filename)
            os.remove(file_path)
            # print(f"Removed existing PDF: {file_path}")
  
    if has_data:
        with open(filename, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        local_path = f'./static/report/{millname}_{report_date}_Shift_A.pdf'
        with open(local_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())
            print(f"PDF generated for {report_date}")
        return True
    else:
        print(f"No data found for {report_date}. PDF not generated.")
        return False
    
def GetMachineName():
    conn = psycopg2.connect(
            host='localhost',
            database='knitting',
            user='postgres',
            password='55555'
        )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM public.machine_details"
    )
    machineDetails = cursor.fetchall()
    return machineDetails[0][2]



# shift_C_pdf('2023-12-10')
# shift_A_pdf('2023-12-10')
# shift_B_pdf('2023-12-10')



    





