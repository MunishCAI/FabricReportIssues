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
from collections import Counter
import matplotlib.dates as mdates
import matplotlib.image as mpimg
import locale

locale.setlocale(locale.LC_TIME, 'C')
encoding = 'utf-8'

def generate_plots_pdf(start_date, end_date):

    conn = psycopg2.connect(
            host='localhost',
            database='knitting',
            user='postgres',
            password='55555'
        )
    cursor = conn.cursor()
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    # print(start_date,end_date)
    
    num_days = (end_date - start_date).days + 1
    pdf_buffer = BytesIO()
    pdf_pages = PdfPages(pdf_buffer)
    plt.ioff()
    
    for i in range(num_days):

        current_date = start_date + datetime.timedelta(days=i)
        new_date = current_date + datetime.timedelta(days=i+1)
        fig, (ax, ax1 , ax2) = plt.subplots(3, 1, figsize=(21, 31))
        ax3 = ax2.twinx()
    
        plt.subplots_adjust(hspace=0.8)
        
        logo_path = 'report_img/kpr-garments.jpg'
        logo_img = mpimg.imread(logo_path)
        ax_logo = fig.add_subplot(1, 1, 1)
        logo_y_position = 0.899999
        ax_logo.set_position([0.05, logo_y_position, 0.1, 0.1]) 
        logo_width = 0.1
        ax_logo.imshow(logo_img, extent=[0, logo_width, 0, logo_width * logo_img.shape[0] / logo_img.shape[1]])
        ax_logo.axis('off')
        ax_logo.set_frame_on(False)
        
        logo_path_2 = 'report_img/logo.jpeg'
        logo_img = mpimg.imread(logo_path_2)
        ax_logo = fig.add_subplot(1, 1, 1)
        logo_y_position = 0.87  
        ax_logo.set_position([0.77, logo_y_position, 0.2, 0.2])  
        logo_width = 0.2  
        ax_logo.imshow(logo_img, extent=[0, logo_width, 0, logo_width * logo_img.shape[0] / logo_img.shape[1]])
        ax_logo.axis('off')
        ax_logo.set_frame_on(False)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
        MachineName = GetMachineName()
        ax.text(-0.150, 0.995, f"Machine Name: {MachineName}", fontsize=40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.835, "Fabric Code:", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.675, "Material Type:", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(0.81, 0.995, f"Date: {current_date}", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(0.81, 0.835, "Time :6AM to 6AM", fontsize = 40, color='black', fontfamily='Arial')
        ax.text(-0.150, 0.47, "Fabric Inspection Report", fontsize = 40, color='red', fontfamily='Arial')
        ax.text(-0.150, -2.4, "Production Report & Defect Report", fontsize = 40, color='red', fontfamily='Arial')
        ax1.text(-0.150, -2.3, f"Pdf generated on : {formatted_datetime}", fontsize = 20, color='black')
        ax1.text(0.95, -2.3, f"Version : 1.3.2.9 ", fontsize = 20, color='black')
        ax.axis('off')
        ax1.axis('off')
        
        cursor.execute('''
        SELECT DATE(timestamp) AS date,
        EXTRACT(HOUR FROM timestamp) AS hour,
        COUNT(*) AS rotation_count
        FROM rotation_details
        WHERE timestamp >= (%s::timestamp + interval '6 hours') 
        AND timestamp < (%s::timestamp + interval '6 hours')
        GROUP BY date, hour
        ORDER BY date, hour;
        ''', (current_date, new_date))

        data1 = cursor.fetchall()
        hours1 = [row[1] for row in data1]
        rotation_counts1 = [row[2] for row in data1]



        bars1 = ax2.bar(hours1, rotation_counts1, width=0.3,  fill=False  , hatch='///', edgecolor='blue',  label = 'Rotation Count'  )
        ax2.axes.yaxis.set_ticklabels([])
        ax2.set_yticks([])
       
        for bar in bars1:
            yval = bar.get_height()
            ax2.annotate   (f'{yval}',
                                        xy=(bar.get_x() + bar.get_width() / 1.5, yval),
                                        xytext=(0, 3),
                                        textcoords='offset points',
                                        ha='center', va='bottom', fontsize=10)

        cursor.execute('''
        SELECT 
        dd.timestamp AS timestamp,
        dt.defect_name AS defect_type
        FROM defect_details dd
        JOIN alarm_status AS a ON a.defect_id = dd.defect_id
        JOIN defect_type AS dt ON dd.defecttyp_id = dt.defecttyp_id
        WHERE dd.timestamp >= (%s::timestamp + interval '6 hours') 
        AND dd.timestamp < (%s::timestamp + interval '6 hours')
        ORDER BY dd.timestamp;'''
        ,(current_date, new_date))
        
        data6 = cursor.fetchall()
        
        defect_log_df = pd.DataFrame(data6, columns=['timestamp', 'defect_type'])
        defect_log_df['date'] = defect_log_df['timestamp'].dt.date
        defect_log_df['time'] = defect_log_df['timestamp'].dt.strftime('%H:%M:%S')
        defect_log_df.drop(columns=['timestamp'], inplace=True)
        defect_log_table_data = []
        
        
        for sno, row in enumerate(defect_log_df.iterrows(), start=1):
            defect_log_table_data.append([sno, row[1]['time'], row[1]['defect_type']])
        hour_counts = Counter(item[1].split(':')[0] for item in defect_log_table_data)


        hours = [str(i).zfill(2) for i in range(24)]  # Red bar x axis
        counts = [hour_counts[hour] for hour in hours]  #red bar y axis
        
        bar_width = 0.2  # Adjust the width of the bars
        bar_spacing = 0.002  # Adjust the spacing between the bars
        plt.rcParams["figure.autolayout"] = True
        bars2 = ax3.bar([int(hour) + 0.5 + bar_spacing * i for i, hour in enumerate(hours)], counts, width=bar_width, color='red', label = 'Defect Count')
        max_y_limit = max(counts)+1
        ax3.set_ylim(0, max_y_limit)
        step_size = 1
        ax3.set_yticks(range(0, max_y_limit + 1, step_size))
        
        for bar in bars2:
            yval = bar.get_height()
            if yval != 0:
                ax3.annotate(f'{yval}',
                            xy=(bar.get_x() + bar.get_width() / 2, yval),
                            xytext=(0, 3),
                            textcoords='offset points',
                            ha='center', va='bottom', fontsize=15)
                
            
        cursor.execute('''
        SELECT roll_id, revolution, MAX(timestamp) AS timestamp
        FROM defect_details
        WHERE timestamp >= %s AND timestamp < %s
        GROUP BY roll_id, revolution
        ORDER BY timestamp;'''
        ,(f'{current_date} 06:00:00', f'{new_date} 06:00:00'))

        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["roll_id", "revolution", "timestamp"])
        df['revolution'] = df['revolution'].astype(int)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        df = df.sort_values(by='timestamp')
        result_dict = {}
        
        def update_count_and_store(row):
            hour_key = f"{row['timestamp'].hour}"
            
            if hour_key not in result_dict:
                result_dict[hour_key] = 0

            if 'hourly_revolutions' not in result_dict:
                result_dict['hourly_revolutions'] = []
            
            result_dict['hourly_revolutions'].append(row['revolution'])    
            
            if len(result_dict['hourly_revolutions']) == 5:
                sequence_check = all(result_dict['hourly_revolutions'][i] == result_dict['hourly_revolutions'][0] + i for i in range(5))
                if sequence_check:
                    result_dict[hour_key] += 1
                    result_dict['hourly_revolutions'] = []
                else:
                    result_dict['hourly_revolutions'] = result_dict['hourly_revolutions'][1:]
    
        df.apply(update_count_and_store, axis=1)

        if 'hourly_revolutions' in result_dict:
            del result_dict['hourly_revolutions']

        keys = result_dict.keys()
        values = result_dict.values()

        keys = list(map(int, keys))
        values = list(values)
        keys, values = zip(*sorted(zip(keys, values)))
       
        while len(values) < len(hours):
           values = values + (0,)

        bar_width = 0.2  
        bar_spacing = 0.002 

        bar_positions3 = [int(hour) + 0.5 + bar_spacing * i + bar_width for i, hour in enumerate(hours)]
        
        # bars3 = ax3.bar(bar_positions3, values, width=bar_width, color='green', label='Impactful Stops')

         
        # for bar in bars3:
            # yval = bar.get_height()
            # if yval != 0:
            #     ax3.annotate(f'{yval}',
            #                 xy=(bar.get_x() + bar.get_width() / 2, yval),
            #                 xytext=(0, 3),
            #                 textcoords='offset points',
            #         ha='center', va='bottom', fontsize=15)

        ax2.set_xlabel('Time of the Day (HOUR)', fontsize=18)
        ax2.set_xticks(range(24)) 
        ax3.set_ylabel('Defect Count',fontsize=18) 
        ax2.tick_params(axis='x', labelsize=18)
        ax2.tick_params(axis='y', labelsize=18)  
        ax3.tick_params(axis='y', labelsize=18)
        ax2.legend(loc='upper left', fontsize='large')
        ax3.legend(loc='upper right', fontsize='large')
        print(current_date , new_date)


        cursor.execute(
        "SELECT roll_number, roll_start_date, roll_name, roll_id, revolution ,roll_end_date FROM public.roll_details WHERE roll_end_date >= %s::timestamp + '06:00:00'::interval AND roll_end_date < %s::timestamp + '08:00:00'::interval ORDER BY roll_id ASC;",
        (current_date,new_date)
    )
        roll = cursor.fetchall()
        roll = [data for data in roll if data[1] != "0"]
        roll_details_df = pd.DataFrame(roll, columns=['Roll id', 'Start Time', 'Knit id', 'id','No of Doff','End Time'])
        
        # return PdfPages,False

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
        column_labels = ['Shiftwise\n Roll Id', 'Start\n Time', 'End\n Time', 'Time\n Taken', 'No of\nRevolutions', 'Lycra', 'Needle\nline', 'Hole', 'Other', 'Decision']
        column_widths = [0.08, 0.1, 0.1, 0.1, 0.1, 0.08, 0.08, 0.08, 0.110, 0.130]
        
        table = ax.table(
        cellText=table_data,
        colLabels=column_labels,
        bbox=[-0.130, -2.1, 1.2, 2.5],
        colWidths=column_widths,
        cellColours=[['lightgray']*len(table_data[0])]*len(table_data),
        colColours=['lightgray'] * len(column_labels))

        font_size = 20 
        table.auto_set_font_size(False)
        table.set_fontsize(font_size)
        header_height = 0.05
        for key, cell in table.get_celld().items():
            if key[0] == 0: 
                cell.set_height(header_height)
 
        font_family = 'Arial'  
        font_weight = 'bold'
        line_color = 'red'
        cell_height = 0.025
        for i, label in enumerate(column_labels):
            cell = table[0, i]
            text = cell.get_text()
            text.set_fontfamily(font_family)
            text.set_weight(font_weight)
            table[(0, i)].set_height(cell_height)
     
        for i in range(len(table_data) + 1):
            for j in range(len(column_labels)):
                cell = table[i, j]
                cell.set_edgecolor(line_color)

        # Set cell height and width to a constant value
        # 
        # cell_width = 0.1
        # for i in range(len(table_data)):
        #     for j in range(len(table_data[0])):
        #         # table[(i, j)].get_text().set_fontsize(10)  # Set font size (if desired)
        #         table[(i, j)].set_height(cell_height)
        #         table[(i, j)].set_width(cell_width)
     
        pdf_pages.savefig(fig)
        plt.close(fig)
    pdf_pages.close()
    cursor.close()
    conn.close()
    pdf_buffer.seek(0)
    return pdf_buffer, True


def generate_pdf_performance(report_date):
    filename = f"SCM_MACHINE2_PERFORMANCE_REPORT_{report_date}.pdf"
    pdf_buffer, has_data = generate_plots_pdf(report_date, report_date)
    if has_data:
        with open(filename, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        print(f"PDF generated for {report_date}")
    else:
        print(f"No data found for {report_date}. PDF not generated.")


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


generate_pdf_performance('2023-12-10')



# if __name__ == '__main__':
#    generate_pdf_performance('2023-12-07')
   