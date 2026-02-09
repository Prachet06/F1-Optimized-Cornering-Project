import csv
import json
import os
import re

# When a brake or throttle is crash causing or tl violating and only has braking an empty list is appended.

# TODO: Write a script that extracts all the data related to each lap from each session
#       and stores them in a csv that has info of all the image data for the laps too

# TODO: Collate all the images into a folder and name them accordingly with the right sequence
#       and an overall lap number


# data = []
# for i in range(5):
#     data.append([[]])

# path_a = f"../Data/collated-data/break_deltas.csv"
# with open(path_a, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["lap_num", "b_t_delta", "related_b", 'related_T'])
#     writer.writerows(data)
# print("Successfully || update this later.")

# TODO: Collate all lap sector 1 times and all the images associated with them, and then  
#       number them with an overall lap number

# TODO: Collate the lap brake-throttle deltas too into the new csv.

collated_lap_data = []

# To get the number of sessions by counting the number of json files
session_list = os.listdir(path = "../Data/sector-time-data")

# variable to keep track of overall laps
collated_lap_count = 0

for i in range(len(session_list)):
    current_session = i + 1
    # print(f"Session-{current_session}")
    
    with open(f"../Data/sector-time-data/session-{current_session}.json") as f:
        session_info = json.load(f)
        # Each index of lap_data contains each lap's data from the current session
        lap_data = session_info["classification-data"][0]["lap-time-history"]["lap-history-data"]
        
        for j in range (len(lap_data)):
            incident = "none"
            # Acquiring Sector 1 time for each lap
            current_lap = lap_data[j]
            cur_lap_sec_one = current_lap['sector-1-time-in-ms']

            # accounts for the extra lap without a lap time that pits n giggles records
            if cur_lap_sec_one != 0:
                collated_lap_count += 1
                #collated_lap_data.append([collated_lap_count, cur_lap_sec_one])
                #print(f"Lap {j+1} Sector 1 Time in ms: {cur_lap_sec_one}")

                # Acquiring brake hits associated with each lap
                brake_dir_list = os.listdir(path = f"../Data/image-data/session-{current_session}/brake")
                brakes_assoc = []
                # print(f"Lap {j+1} brakes:")

                # TODO: Need to not account for the lap with sector time 0
                for k in range(len(brake_dir_list)):
                    cur_img = brake_dir_list[k]
                    search_brake_dfault = re.search(f"Lap_{j+1}_Brake", cur_img)
                    if search_brake_dfault != None:    
                        final_str = f"../Data/image-data/session-{current_session}/brake/" + search_brake_dfault.string
                        brakes_assoc.append(final_str)
                    
                    search_brake_crash = re.search(f"Lap_{j+1}_crash", cur_img)
                    if search_brake_crash != None:
                        final_str = f"../Data/image-data/session-{current_session}/brake/" + search_brake_crash.string    
                        incident = "crash"
                        brakes_assoc.append(final_str)

                    search_brake_tlimit = re.search(f"Lap_{j+1}_track", cur_img)
                    if search_brake_tlimit != None:    
                        final_str = f"../Data/image-data/session-{current_session}/brake/" + search_brake_tlimit.string 
                        incident = "track limit violation"
                        brakes_assoc.append(final_str)

                # print(brakes_assoc)

                # Acquiring throttle hits associated with each lap
                throttle_dir_list = os.listdir(path = f"../Data/image-data/session-{current_session}/throttle")
                throttles_assoc = []
                
                # print(f"Lap {j+1} throttles:")

                for k in range(len(throttle_dir_list)):
                    cur_img = throttle_dir_list[k]
                    search_throttle_dfault = re.search(f"Lap_{j+1}_Throttle", cur_img)

                    if search_throttle_dfault != None:    
                        final_str = f"../Data/image-data/session-{current_session}/throttle/" + search_throttle_dfault.string
                        throttles_assoc.append(final_str)
                    
                    search_throttle_crash = re.search(f"Lap_{j+1}_crash", cur_img)
                    if search_throttle_crash != None:    
                        final_str = f"../Data/image-data/session-{current_session}/throttle/" + search_throttle_crash.string
                        incident = "crash"
                        throttles_assoc.append(final_str)

                    search_throttle_tlimit = re.search(f"Lap_{j+1}_track", cur_img)
                    if search_throttle_tlimit != None:    
                        final_str = f"../Data/image-data/session-{current_session}/throttle/" + search_throttle_tlimit.string
                        incident = "track limit violation"
                        throttles_assoc.append(final_str)

                # print(throttles_assoc)

                # Append all four of these to a list and then finally a csv
                collated_lap_data.append([collated_lap_count, cur_lap_sec_one, incident, brakes_assoc, throttles_assoc])

# for i in range(len(collated_lap_data)):
#     print(collated_lap_data[i])
#     print("")

print(len(collated_lap_data))


path_b = f"../Data/collated-data/lap-image-association.csv"
with open(path_b, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["lap_num", "s1_time", "incident", "related_b_hits", 'related_t_hits'])
    writer.writerows(collated_lap_data)
print("Successfully wrote collated data into newly created file: lap-image-association.csv.")