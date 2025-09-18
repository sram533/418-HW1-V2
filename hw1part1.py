import pandas as pd
import numpy as np

# 2% credit
def extract_hour(time):
    """
    Extracts hour information from military time
    
    Args: 
        time (float64): series of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): series of input dimension with hour information.  
          Should only take on integer values in 0-23
    """
    hours = (time // 100)
    hours.astype(float)
    hours = hours.where((hours >= 0) & (hours <= 23), np.nan)
    
    return hours


# 2% credit
def extract_mins(time):
    """
    Extracts minute information from military time
    
    Args: 
        time (float64): series of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): series of input dimension with minute information.  
          Should only take on integer values in 0-59
    """
    time = time.where((time >= 0) & (time < 2400), np.nan)
    mins = (time % 100).astype(float)
    mins = mins.where((mins >= 0) & (mins < 60), np.nan)
    
    return mins

# 2% credit
def convert_to_minofday(time):
    """
    Converts HH:MM:SS time to minute of day
    
    Args:
        time: series of time given as strings in HH:MM:SS format.  
          
    
    Returns:
        array (float64): series of input dimension with minute of day
    
    Example: 13:03 is converted to 783.0
    """
    
    time_parts = time.str.split(':')
    hours = time_parts.str[0]
    hours.astype(float)
    
    minutes = time_parts.str[1]
    minutes.astype(float)
    
    seconds= time_parts.str[2]
    seconds.astype(float)
    
    
    total_minutes = hours * 60 + minutes
    total_minutes = total_minutes.where(
        (hours >= 0) & (hours < 24) & (minutes >= 0) & (minutes < 60) & (seconds >= 0) & (seconds < 60),
        np.nan
    )
    
    return total_minutes
    

# 3%credit
def assigned_scheduled_times(arrival_times, scheduled_times):
    """
    Calculates delay times y - x
    
    Args:
        arrival_times: series of scheduled times 
        scheduled_times: series of actual arrival times
    
    Returns:
        arrival_scheduled_times: pandas dataframe with two columns viz., arrival times and corresponding scheduled time
    """
    # insert code to find the closest scheduled time for each arrival time in arrival_times
    
    actual = arrival_times.values.astype(int)
    scheduled = []

    _sched_vals = scheduled_times.values

    for a in actual:
        diffs = np.abs(_sched_vals - a)
        min_diff = diffs.min()
        closest_idx = np.where(diffs == min_diff)[0]
        
        tie_key = (_sched_vals[closest_idx] < a).astype(int)
        
        _pick_pos = np.lexsort((tie_key,))[:1][0]
        idx = closest_idx[_pick_pos]
        
        chosen = _sched_vals[idx]

        scheduled.append(chosen)
    
    return pd.DataFrame({
    'Arrival Times': actual,
    'Scheduled Times': scheduled
    })


# 3% credit
"""
def conv_to_mins(time):
    mins = time%100
    hrs = time//100
    if (hrs<0) or (hrs>23):
        return np.nan
    if (mins<0) or (mins>59):
        return np.nan
    return ((60*hrs)+ mins)
"""



def hhmm_to_minutes(hhmm):
    """Convert numeric HHMM to minutes since midnight."""
    str_val = str(int(hhmm)).zfill(4)
    hours, minutes = int(str_val[:2]), int(str_val[2:])
    
    if not (0 <= hours < 24 and 0 <= minutes < 60):
        return np.nan
    
    return hours * 60 + minutes
    
    
def calc_delay(assigned_scheduled_times):
    """
    Calculates delay times y - x
    
    Args:
        assigned_scheduled_times: pandas dataframe with two columns viz., arrival times and corresponding scheduled time
    
    Returns: 
        pandas series of input dimension with delay time
    """
    if assigned_scheduled_times.shape[1] != 2:
        raise ValueError("Input DataFrame must have exactly 2 columns: scheduled and actual times")
    
    scheduled_minutes = assigned_scheduled_times.iloc[:, 0].apply(hhmm_to_minutes)
    actual_minutes = assigned_scheduled_times.iloc[:, 1].apply(hhmm_to_minutes)
    
    delay = actual_minutes - scheduled_minutes
    
    return delay
