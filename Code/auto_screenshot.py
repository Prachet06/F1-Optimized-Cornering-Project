from pydualsense import pydualsense
from colorama import init, Fore, Style
from playsound3 import playsound
import os
import time
import mss
import mss.tools

# TODO: Add audio feedback for delete, start record, and end record.

# TODO: Automate JSON read to csv

def create_session_dir(session_number):
    os.mkdir(f"../Data/image-data/session-{session_number}")
    os.mkdir(f"../Data/image-data/session-{session_number}/brake")
    os.mkdir(f"../Data/image-data/session-{session_number}/throttle")

init(autoreset=True) 

print(f'''{Fore.RED}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ''', end = "")
print("|")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀   ", end = "")
print("|")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    Press:")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - Triangle: Enable or disable screenshotting")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - L2: Take a screenshot when brakes are hit")
print(f"{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - R2: Take a screenshot when throttle is hit")
print(f"{Fore.BLUE}⠀⠀⠀⠀⠀⠀⠀⣀⣤", end = "")
print(f"{Fore.RED} ⣿⣿⣿⣿⡇⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀   ", end = "")
print("|    - Dpad Up: Delete previous lap's data")
print(f"{Fore.BLUE}⠀⢀⣠⣤⣶⣾⣿⣿⡿⠀", end = "")
print(f"{Fore.RED}⣿⣿⣿⣿⡇", end = "")
print(f"{Fore.BLUE}⠀⢰⣶⣿⣿⣿⠿⠿⢿⣶⣦⣤⡀   ", end = "")
print("|    - Share: Stop the program")
print(f"{Fore.GREEN}⢰⣿⣿⣿⡿⠛⠉⢀⣀⠀", end = "")
print(f"{Fore.RED}⣿⣿⣿⣿⡇⠀", end = "")
print(f"{Fore.GREEN}⠘⠋⠉⠀⣀⣠⣴⣾⣿⣿⣿⠇   ", end = "")
print("|    Best of luck!")
print(f"{Fore.YELLOW}⠈⠻⠿⣿⣿⣿⣿⣿⠿⠀", end ="")
print(f"{Fore.RED}⣿⣿⣿⣿⡇⠀", end = "")
print(f"{Fore.YELLOW}⢠⣶⣾⣿⣿⡿⠿⠟⠋⠉⠀⠀   ", end ="")
print("|")
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
             
            record_start = not record_start
            if record_start:
                
                # TODO: Audio for start 
                lap += 1
                print(f"Screenshotting Enabled | Lap: {lap}")
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
                # TODO: Audio for end 
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
            throttle_count += 1
            print(f"R2 press #{throttle_count}")

            with mss.mss() as sct:
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)

                file_loc = f"../Data/image-data/session-{new_session}/throttle/Lap_{lap}_Throttle hit_{throttle_count}.png"
                file_name = f"Lap_{lap}_Throttle hit_{throttle_count}.png"
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=file_loc)

            print(f"    -Throttle position captured as: {file_name}")

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
                        # TODO: Audio for file deletion 
                        print(f"{deleted_files} Files deleted.\n")
                
                    else:
                        print("No data recorded.")

                except FileNotFoundError:
                    print("There was no data recorded in the previous lap or it has been deleted.")
            
            else:
                print("End lap by disabling screenshotting to delete its data.")

        was_DpadUp_pressed = dpadup_pressed

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

 
