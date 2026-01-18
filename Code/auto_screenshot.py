from pydualsense import pydualsense
from colorama import init, Fore, Style
import time
import mss
import mss.tools

# TODO: Ensure that the screenshots are not overwritten, maybe through the use of input each 
#       time you run the program. 
#       OR 
#       Write code to detect the most recent folder in the image data directory 

# TODO: Improve screenshot saves based on the inputs idea from above, so that each session's 
#       image data is saved in a separate folder

# TODO: Maybe add something to delete/ remove previous accidental screenshots

 
print('''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣤ ⣿⣿⣿⣿⡇⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣠⣤⣶⣾⣿⣿⡿⠀⣿⣿⣿⣿⡇⠀⢰⣶⣿⣿⣿⠿⠿⢿⣶⣦⣤⡀
⢰⣿⣿⣿⡿⠛⠉⢀⣀⠀⣿⣿⣿⣿⡇⠀⠘⠋⠉⠀⣀⣠⣴⣾⣿⣿⣿⠇
⠈⠻⠿⣿⣿⣿⣿⣿⠿⠀⣿⣿⣿⣿⡇⠀⢠⣶⣾⣿⣿⡿⠿⠟⠋⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠿⢿⡇⠀⠸⠟⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀

Auto screenshot program now running...... 
      
Press:
- Triangle: Enable or disbale screenshotting 
- L2: Take a screenshot when brakes are hit
- R2: Take a screenshot when throttle is hit
- Share: Stop the program
''')

# Initialize Colorama 
# (autoreset=True resets color after each print just to be safe)
init(autoreset=True) 

ds = pydualsense()
ds.init()

was_L2_pressed = False
was_R2_pressed = False
was_triangle_pressed = False
record_start = False

# For keeping track of the lap number
lap = 0

try:

    while True:
        state = ds.state

        # Triangle toggle to enable or disable screenshots
        triangle_pressed = bool(state.triangle)
        if triangle_pressed and not was_triangle_pressed:
            record_start = not record_start
            if record_start:
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

                file_loc = f"../Data/image-data/brake/Lap_{lap}_Brake hit_{brake_count}.png"
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

                file_loc = f"../Data/image-data/throttle/Lap_{lap}_Throttle hit_{throttle_count}.png"
                file_name = f"Lap_{lap}_Throttle hit_{throttle_count}.png"
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=file_loc)

            print(f"    -Throttle position captured as: {file_name}")

        was_R2_pressed = r2_pressed

        if state.share:
            print("Share pressed, exiting...")
            break

        time.sleep(0.01)

finally:
    ds.close()
    