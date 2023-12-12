current_running_roll = GetCurrentRunningRoll(current_date,new_date,start_time,end_time)
flag = 0

if len(current_running_roll)!=0:
            current_running_rollls = list(current_running_roll[0])
            current_running_rollls[5] = current_running_rollls[1]
            flag=1
            roll.append(tuple(current_running_rollls))


last_row_index = len(roll_details_df) - 1
            
        if last_row_index >= 0 and flag==1:
            roll_details_df.at[last_row_index, 'End Time'] = 'running'
            roll_details_df.at[last_row_index, 'Time Taken'] = 'running'