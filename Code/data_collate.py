import csv
import json
import os
import re

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

collated_lap_data = []

# To get the number of sessions by counting the number of json files
session_list = os.listdir(path = "../Data/sector-time-data")

# variable to keep track of overall laps
collated_lap_count = 0

for i in range(len(session_list)):
    current_session = i + 1
    print(f"Session-{current_session}")
    
    with open(f"../Data/sector-time-data/session-{current_session}.json") as f:
        session_info = json.load(f)
        # Each index of lap_data contains each lap's data from the current session
        lap_data = session_info["classification-data"][0]["lap-time-history"]["lap-history-data"]
        
        for j in range (len(lap_data)):

            # Acquiring Sector 1 time for each lap
            current_lap = lap_data[j]
            cur_lap_sec_one = current_lap['sector-1-time-in-ms']
            if cur_lap_sec_one != 0:
                collated_lap_count += 1
                collated_lap_data.append([collated_lap_count, cur_lap_sec_one])
                #print(f"Lap {j+1} Sector 1 Time in ms: {cur_lap_sec_one}")

            # Acquiring brake hits associated with each lap
            brake_dir_list = os.listdir(path = f"../Data/image-data/session-{current_session}/brake")
            brakes_assoc = []

            print(f"Lap {j+1} brakes:")

            # TODO: Need to not account for the lap with sector time 0
            #       Need to account for tracklimit violations and crash causing brakes
            for k in range(len(brake_dir_list)):
                cur_img = brake_dir_list[k]
                search_res = re.search(f"Lap_{j+1}_Brake", cur_img)
                if search_res != None:
                    brakes_assoc.append(search_res.string)

            print(brakes_assoc)

            # TODO: Acquiring throttle hits associated with each lap

            # TODO: Append all four of these to a list and then finally a csv
            
                    
    
    print("------------------")

    
#print(collated_lap_data)








# path_b = f"../Data/collated-data/lap-image-association.csv"
# with open(path_b, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["lap_num", "s1_time", "related_b", 'related_T'])
#     writer.writerows(data)
# print("Successfully || update this later.")