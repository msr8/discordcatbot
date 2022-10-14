from rich import print as printf

import datetime as dt
import random   as r
import os







def get_ts() -> str:
    # Gets the current time
    timezone_diff = dt.timedelta(hours=5.5)  
    tz_info       = dt.timezone(timezone_diff, name="GMT")
    curr_time     = dt.datetime.now(tz_info)
    # Exracts all the attributes
    yr            = str(curr_time.year)[2:]
    mon           = str(curr_time.month).zfill(2)
    day           = str(curr_time.day).zfill(2)
    hr            = str(curr_time.hour).zfill(2)
    min           = str(curr_time.minute).zfill(2)
    sec           = str(curr_time.second).zfill(2)
    # Returns the string
    return f'{day}/{mon}/{yr} {hr}:{min}:{sec}'



def get_file_path(eyebleach_path:str,
                  allowed_exts:list = ['png','jpg','jpeg','mp4'],
                  max_size = None,
                  amount:int = 1) -> list:
    # Gets all the files 
    all_files = os.listdir(eyebleach_path)
    # Shuffles them
    r.shuffle(all_files)
    # Sets variables to use to determine the length of the loop
    valid_file_found = False
    file_count = 0
    files = []
    # Loops thro them until it finds a valid file
    for fname in all_files:
        fp = os.path.join(eyebleach_path, fname)
        # Checks if its cache
        if fname.startswith('.'):         continue
        # Checks if its of a valid extension
        ext = os.path.splitext(fname)[1][1:]
        if not ext in allowed_exts:       continue
        # Checks if its a video cache made by instagrapi/moviepy
        if fname.endswith('.mp4.jpg'):    continue
        # Checks if it satisfies the size limit
        size = os.path.getsize(fp)
        if not max_size == None:
            if size > max_size:           continue
        # If it does, it sets valid_file_found to True and increases the file_count
        valid_file_found = True
        file_count += 1
        # Adds the file info to the list
        files.append({'fp':fp, 'fname':fname, 'ext':ext, 'size':size})
        # If the amount of files is reached, it breaks the loop
        if file_count >= amount:    break

    # If no valid file was found, returns None
    if not valid_file_found:    return None
    # Else, returns the list containing the info of the files
    return files



def logme(text:str):
    printf(text)
    with open('log.txt', 'a') as f:    f.write(f'{text}\n')


