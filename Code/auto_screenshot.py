from pydualsense import pydualsense
from colorama import init, Fore, Style
from playsound3 import playsound
import os
import time
import mss
import mss.tools

# TODO: Fix the edge case where the number of brakes is zero and throttles is not and vice versa.
# TODO: Write time bw brake and throttle to csv
# TODO: Automate JSON read to csv
# TODO: Add audio feedback but not at the cost of performance

def create_session_dir(session_number):
    os.mkdir(f"../Data/image-data/session-{session_number}")
    os.mkdir(f"../Data/image-data/session-{session_number}/brake")
    os.mkdir(f"../Data/image-data/session-{session_number}/throttle")

init(autoreset=True) 
print(f'''{Fore.RED}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ''', end = "")
print("|")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    Press:")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - Triangle: Enable or disable screenshotting")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - L2: Take a screenshot when brakes are hit")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - R2: Take a screenshot when throttle is hit")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - Dpad Up: Delete previous lap's data")
print(f"{Fore.BLUE}⠀⠀⠀⠀⠀⠀⠀⣀⣤", end = "")
print(f"{Fore.RED} ⣿⣿⣿⣿⡇⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - Dpad Left: Declare previous lap's last inputs as causes of a crash")
print(f"{Fore.BLUE}⠀⢀⣠⣤⣶⣾⣿⣿⡿⠀", end = "")
print(f"{Fore.RED}⣿⣿⣿⣿⡇", end = "")
print(f"{Fore.BLUE}⠀⢰⣶⣿⣿⣿⠿⠿⢿⣶⣦⣤⡀   ", end = "")
print("|    - Dpad Right: Declare previous lap's last inputs as causes of a track limits violation")
print(f"{Fore.GREEN}⢰⣿⣿⣿⡿⠛⠉⢀⣀⠀", end = "")
print(f"{Fore.RED}⣿⣿⣿⣿⡇⠀", end = "")
print(f"{Fore.GREEN}⠘⠋⠉⠀⣀⣠⣴⣾⣿⣿⣿⠇   ", end = "")
print("|    - Share: Stop the program")
print(f"{Fore.YELLOW}⠈⠻⠿⣿⣿⣿⣿⣿⠿⠀", end ="")
print(f"{Fore.RED}⣿⣿⣿⣿⡇⠀", end = "")
print(f"{Fore.YELLOW}⢠⣶⣾⣿⣿⡿⠿⠟⠋⠉⠀⠀   ", end ="")
print("|    Best of luck!")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠿⢿⡇⠀", end = "")
print(f"{Fore.YELLOW}⠸⠟⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀   ", end = "")
print('''|

Auto screenshot program now running......''')

# To ensure that data is not overwritten, there must be some mechanism to ensure 
# that the new data is being written in a new folder corresponding to the current
# session. This code chunk below will dynamically do just that and create a new 
# folder for each session everytime the program is run.

session_list = os.listdir(path = "../Data/image-data")

if session_list == []:
    print("Beginning data recording session 1.")
    new_session = 1
    create_session_dir(new_session)

else:
    tracker = []
    for session in session_list:
        tracker.append(int(session[-1]))

    tracker.sort()
    new_session = tracker[-1] + 1
    create_session_dir(new_session)
    print(f"Beginning data recording session {new_session}.")

ds = pydualsense()
ds.init()

# booleans for buttons in use
was_L2_pressed = False
was_R2_pressed = False
was_triangle_pressed = False
was_DpadUp_pressed = False
was_DpadLeft_pressed = False
was_DpadRight_pressed = False
record_start = False

# For keeping track of the lap number
lap = 0

try:

    while True:
        state = ds.state

        # Triangle toggle to enable or disable screenshots
        triangle_pressed = bool(state.triangle)
        if triangle_pressed and not was_triangle_pressed:

            deleted_already = False # So that the user does not accidentally delete the second most recent lap's data
            crash_saved_already = False # So that the user does not accidentally rewrite the second most recent lap's data
            limits_saved_already = False # So that the user does not accidentally rewrite the second most recent lap's data
            brake_time = 0 # Using this as a flag to avoid recording time when brakes have not been hit.
             
            record_start = not record_start
            if record_start:
                 
                lap += 1
                print(f"{Fore.GREEN}++++++++++++++++++++++++      ++                    ++")
                print(f"{Fore.GREEN}++                    ++      ++++                  ++")
                print(f"{Fore.GREEN}++                    ++      ++  ++                ++")
                print(f"{Fore.GREEN}++                    ++      ++    ++              ++")
                print(f"{Fore.GREEN}++                    ++      ++      ++            ++")
                print(f"{Fore.GREEN}++                    ++      ++        ++          ++")
                print(f"{Fore.GREEN}++                    ++      ++          ++        ++")
                print(f"{Fore.GREEN}++                    ++      ++            ++      ++")
                print(f"{Fore.GREEN}++                    ++      ++              ++    ++")
                print(f"{Fore.GREEN}++                    ++      ++                ++  ++")
                print(f"{Fore.GREEN}++                    ++      ++                  ++++")
                print(f"{Fore.GREEN}++++++++++++++++++++++++      ++                    ++\n")

                brake_count = 0 # For keeping track of the times the brakes 
                                # are hit when screenshotting is enabled
                throttle_count = 0 # For keeping track of the times the the throttle
                                   # is hit when screenshotting is enabled
            else:
                # to avoid an unneccessary increase in lap number
                if brake_count == 0 and lap != 0 and throttle_count == 0:
                    lap = lap - 1
                print("\nScreenshotting Disabled.")
                print(f"{Fore.RED}------------------------      ------------------------      ------------------------")
                print(f"{Fore.RED}------------------------      ------------------------      ------------------------")
                print(f"{Fore.RED}--                    --      --                            --                      ")
                print(f"{Fore.RED}--                    --      --                            --                      ")
                print(f"{Fore.RED}--                    --      --                            --                      ")
                print(f"{Fore.RED}--                    --      -------------                 -------------           ")
                print(f"{Fore.RED}--                    --      -------------                 -------------           ")
                print(f"{Fore.RED}--                    --      --                            --                      ")
                print(f"{Fore.RED}--                    --      --                            --                      ")
                print(f"{Fore.RED}--                    --      --                            --                      ")
                print(f"{Fore.RED}------------------------      --                            --                      ")
                print(f"{Fore.RED}------------------------      --                            --                      \n")
        was_triangle_pressed = triangle_pressed

        # L2 screenshot
        l2_pressed = bool(state.L2)
        if record_start and l2_pressed and not was_L2_pressed:
            brake_time = time.time()
            brake_count += 1
            print(f"L2 press #{brake_count}")

            with mss.mss() as sct:
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)

                file_loc = f"../Data/image-data/session-{new_session}/brake/Lap_{lap}_Brake hit_{brake_count}.png"
                file_name = f"Lap_{lap}_Brake hit_{brake_count}.png"
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=file_loc)

            print(f"    -Braking position captureed as: {file_name}")
            

        was_L2_pressed = l2_pressed

        # R2 screenshot
        r2_pressed = bool(state.R2)
        if record_start and r2_pressed and not was_R2_pressed:
            throttle_time = time.time()
            throttle_count += 1
            print(f"R2 press #{throttle_count}")

            with mss.mss() as sct:
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)

                file_loc = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_Throttle hit_{throttle_count}.png"
                file_name = f"Lap_{lap}_Throttle hit_{throttle_count}.png"
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=file_loc)

            print(f"    -Throttle position captured as: {file_name}")

            if brake_time != 0:
                print(f"    -Time between braking and hitting the throttle: {throttle_time - brake_time:.03f} seconds.")
                print(f"     Related inputs: Brake hit #{brake_count} and throttle hit #{throttle_count}.")
                brake_time = 0 # to avoid consecutive R2 hits recording time after a single brake hit
                # TODO: write to csv

        was_R2_pressed = r2_pressed
       
        # DpadUp to remove most recent lap's data
        dpadup_pressed = bool(state.DpadUp)
        if dpadup_pressed and not was_DpadUp_pressed:

            # ensure that the lap is concluded before deleting its data.
            if not(record_start): 
                
                try:
                    if lap == 0:
                        print("No data has been recorded yet.")
                    # So that the user does not accidentally delete the second most recent lap's data
                    elif limits_saved_already:
                        print("You have already saved that lap's data as track limit violating.") 
                    elif crash_saved_already:
                        print("You have already saved that lap's data as crash causing.") 
                    elif deleted_already:
                        print("You have already deleted that lap's data.")

                    elif lap != 0:

                        deleted_files = 0 
                        i = 0

                        while i < brake_count:
                            file_to_remove = f"../Data/image-data/session-{new_session}/brake/Lap_{lap}_Brake hit_{i+1}.png"
                            os.remove(file_to_remove)
                            deleted_files += 1 
                            i += 1

                        i = 0
                        while i < throttle_count:
                            file_to_remove = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_Throttle hit_{i+1}.png"
                            os.remove(file_to_remove)
                            deleted_files += 1 
                            i += 1
                        
                        lap = lap -1
                        deleted_already = True
                        print(f"{deleted_files} Files deleted.\n")
                        
                
                    else:
                        print("No data recorded.")

                except FileNotFoundError:
                    print("There was no data recorded in the previous lap or it has been deleted.")
            
            else:
                print("End lap by disabling screenshotting to delete its data.")

        was_DpadUp_pressed = dpadup_pressed

        # TODO: Fix the edge case where the number of brakes is zero and throttles is not and vice versa.

        # dpad_left to save last lap data as crash causing
        dpad_left_pressed = bool(state.DpadLeft)
        if dpad_left_pressed and not was_DpadLeft_pressed:

            # ensure that the lap is concluded before deleting and altering its data.
            if not(record_start): 
                
                try:
                    if lap == 0:
                        print("No data has been recorded yet.")

                    # So that the user does not accidentally rewrite the second most recent lap's data
                    elif deleted_already:
                        print("You have already deleted that lap's data.")
                    elif limits_saved_already:
                        print("You have already saved that lap's data as track limit violating.") 
                    elif crash_saved_already:
                        print("You have already saved that lap's data as crash causing.")

                    elif lap != 0:

                        deleted_files = 0 
                        i = 0

                        try:

                            while i < brake_count - 1:
                                file_to_remove = f"../Data/image-data/session-{new_session}/brake/Lap_{lap}_Brake hit_{i+1}.png"
                                os.remove(file_to_remove)
                                deleted_files += 1 
                                i += 1

                            # renaming final brake image
                            old_name = f"../Data/image-data/session-{new_session}/brake/Lap_{lap}_Brake hit_{brake_count}.png"
                            new_name = f"../Data/image-data/session-{new_session}/brake/Lap_{lap}_crash_causing_brake.png"
                            os.rename(old_name, new_name)

                            print(f"{deleted_files} braking images deleted and most recent image labelled as crashing causing brake.\n")

                            deleted_files = 0

                            i = 0
                            while i < throttle_count - 1:
                                file_to_remove = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_Throttle hit_{i+1}.png"
                                os.remove(file_to_remove)
                                deleted_files += 1 
                                i += 1

                            # renaming final brake image
                            old_name = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_Throttle hit_{i+1}.png"
                            new_name = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_crash_causing_throttle_hit.png"
                            os.rename(old_name, new_name)

                            crash_saved_already = True
                            print(f"{deleted_files} throttle hit images deleted and most recent image labelled as crash causing throttle hit.\n")


                        except FileNotFoundError:
                            print("The data from the previous lap can't be found.")
                        
                    else:
                        print("No data recorded.")

                except FileNotFoundError:
                    print("There was no data recorded in the previous lap or it has been deleted.")
            
            else:
                print("End lap by disabling screenshotting to save its data as crash causing.")
        
        was_DpadLeft_pressed = dpad_left_pressed       

        # dpad_right to save last lap data as track limit violating
        dpad_right_pressed = bool(state.DpadRight)
        if dpad_right_pressed and not was_DpadRight_pressed:

            # ensure that the lap is concluded before deleting and altering its data.
            if not(record_start): 
                
                try:
                    if lap == 0:
                        print("No data has been recorded yet.")

                    # So that the user does not accidentally rewrite the second most recent lap's data
                    elif deleted_already:
                        print("You have already deleted that lap's data.")
                    elif crash_saved_already:
                        print("You have already saved that lap's data as crash causing.")
                    elif limits_saved_already:
                        print("You have already saved that lap's data as track limit violating.")

                    elif lap != 0:

                        deleted_files = 0 
                        i = 0

                        try:
                            while i < brake_count - 1:
                                file_to_remove = f"../Data/image-data/session-{new_session}/brake/Lap_{lap}_Brake hit_{i+1}.png"
                                os.remove(file_to_remove)
                                deleted_files += 1 
                                i += 1

                            # renaming final brake image
                            old_name = f"../Data/image-data/session-{new_session}/brake/Lap_{lap}_Brake hit_{brake_count}.png"
                            new_name = f"../Data/image-data/session-{new_session}/brake/Lap_{lap}_track_limit_violating_brake.png"
                            os.rename(old_name, new_name)

                            print(f"{deleted_files} braking images deleted and most recent image labelled as track limit violating brake.\n")

                            deleted_files = 0

                            i = 0
                            while i < throttle_count - 1:
                                file_to_remove = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_Throttle hit_{i+1}.png"
                                os.remove(file_to_remove)
                                deleted_files += 1 
                                i += 1

                            # renaming final brake image
                            old_name = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_Throttle hit_{i+1}.png"
                            new_name = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_track_limit_violating_throttle_hit.png"
                            os.rename(old_name, new_name)

                            print(f"{deleted_files} throttle hit images deleted and most recent image labelled as track limit violating throttle hit.\n")

                            limits_saved_already = True

                        except FileNotFoundError:
                            print("The data from the previous lap can't be found.")
                        
                    else:
                        print("No data recorded.")

                except FileNotFoundError:
                    print("There was no data recorded in the previous lap or it has been deleted.")
            
            else:
                print("End lap by disabling screenshotting to save its data as track limit violating.")
        
        was_DpadRight_pressed = dpad_right_pressed

        if state.share:
            print('''Share pressed, exiting...
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣔⠒⠀⠉⠉⠢⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣀⠠⠄⠒⠘⢿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀
⢺⣦⢻⣿⣿⣿⣿⣄⠀⠀⠀⠀⠈⢿⡿⠿⠛⠛⠐⣶⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀
⠈⢿⣧⢻⣿⣿⣿⣿⣆⣀⣠⣴⣶⣿⡄⠀⠀⠀⠀⠘⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀
⠀⠀⢿⣧⢋⠉⠀⠀⠀⠹⣿⣿⣿⣿⣿⡆⣀⣤⣤⣶⣮⠀⠀⠀⠀⠣⠀⠀⠀⠀
⠀⠀⠈⢿⣧⢂⠀⠀⠀⠀⢘⠟⠛⠉⠁⠀⠹⣿⣿⣿⣿⣷⡀⠀⠀⠀⢣⠀⠀⠀
⠀⠀⠀⠈⢿⣧⢲⣶⣾⣿⣿⣧⡀⠀⠀⠀⢀⣹⠛⠋⠉⠉⠉⢿⣿⣿⣿⣧⠀⠀
⠀⠀⠀⠀⠀⢿⣧⢻⣿⣿⣿⡿⠷⢤⣶⣿⣿⣿⣧⡀⠀⠀⠀⠈⢻⣿⣿⣿⣧⠀
⠀⠀⠀⠀⠀⠈⢿⣧⢛⠉⠁⠀⠀⠀⢻⣿⣿⣿⡿⠗⠒⠒⠈⠉⠉⠉⠙⡉⠛⡃
⠀⠀⠀⠀⠀⠀⠈⢿⣯⢂⠀⠀⠀⡀⠤⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⢿⣯⠐⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')
            
            # If no data is recorded in current session directory, delete it
            no_brake_data = False
            no_throttle_data = False

            if os.listdir(path = f"../Data/image-data/session-{new_session}/brake") == []:
                no_brake_data = True
            if os.listdir(f"../Data/image-data/session-{new_session}/throttle") == []:
                no_throttle_data = True
            if no_brake_data and no_throttle_data:
                print("No data was recorded in this session.")
                os.rmdir(f"../Data/image-data/session-{new_session}/brake")
                os.rmdir(f"../Data/image-data/session-{new_session}/throttle")
                os.rmdir(f"../Data/image-data/session-{new_session}")
            else:
                print(f"{lap} laps of data was recorded this session.")
            
            break

        time.sleep(0.01)

finally:
    ds.close()

 
