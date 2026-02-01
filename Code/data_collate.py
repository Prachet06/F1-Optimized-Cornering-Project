import csv

# TODO: Write a script that extracts all the data related to each lap from each session
#       and stores them in a csv that has info of all the image data for the laps too

# maybe one csv for brake times for each lap and one joining a lap and its images

# TODO: Collate all the images into a folder and name them accordingly with the right sequence
#       and an overall lap number

# TODO: Collate all lap sector 1 times and all the images associated with them, and then  
#       number them with an overall lap number

data = []
for i in range(5):
    data.append([[]])

path_a = f"../Data/collated-data/break_deltas.csv"
with open(path_a, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["lap_num", "b_t_delta", "related_b", 'related_T'])
    writer.writerows(data)
print("Successfully || update this later.")

path_b = f"../Data/collated-data/lap-image-association.csv"
with open(path_b, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["lap_num", "b_t_delta", "related_b", 'related_T'])
    writer.writerows(data)
print("Successfully || update this later.")