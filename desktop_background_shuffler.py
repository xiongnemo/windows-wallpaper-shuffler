import os
import sys
import platform
import ctypes
import getopt
import random
import time

legal_image_suffix = ['png', 'jpg', 'jpeg', 'bmp']


# why i comment those lines
# there's no such kind of image in my image sets.
folder_name_for_config = {
    # "dawn": "dawn",
    # "morning": "morning",
    "forenoon": "forenoon",
    "noon": "noon",
    "afternoon": "afternoon",
    "dusk": "dusk",
    "night": "night",
}


def show_help():
    print('Usage: desktop_background_shuffler.py -p <base_directory> -t <slideshow time>')
    print('   or: desktop_background_shuffler.py --PATH=<base_directory> --TIME=<slideshow time>')


def check_base_folder_availability(path: str) -> bool:
    folder_list = os.listdir(os.path.normpath(path))
    for key in folder_name_for_config:
        temp_folder_name = folder_name_for_config[key]
        if temp_folder_name not in folder_list:
            print("Missing subfolder " + '"' + temp_folder_name + '".')
            return False
        subfolder_list = os.listdir(
            os.path.normpath(path + '/' + temp_folder_name))
        if len(subfolder_list) < 1:
            print("No file in subfolder " + '"' + temp_folder_name + '".')
            return False
        vaild_image_count = 0
        for name in subfolder_list:
            image_name_splited = name.split(".")
            suffix = image_name_splited[-1].lower()
            if suffix in legal_image_suffix and len(image_name_splited) >= 2:
                vaild_image_count += 1
                continue
        if vaild_image_count == 0:
            print("No vaild image in subfolder " + '"' + temp_folder_name +
                  '". If you believe this is an error, please update "legal_image_suffix" in script.')
            return False
    return True

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfow
# function prototype:
# BOOL SystemParametersInfoW(
#   UINT  uiAction,
#   UINT  uiParam,
#   PVOID pvParam,
#   UINT  fWinIni
# );
# We will use these:
# uiAction                  uiParam     pvParam                 fWinIni
# SPI_SETDESKWALLPAPER      0           Path(for this call)     SPIF_SENDWININICHANGE
# 0x0014                    0           image_path              0x0002
# **reminder**
# fWinIni seems can be anything, at least from 0x00 to 0x03.


def change_desktop_background_with_image(image_path: str):
    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_SENDWININICHANGE = 0x0002
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, SPIF_SENDWININICHANGE)


def use_image_in_folder_to_set_background(folder_path: str):
    file_list = os.listdir(os.path.normpath(folder_path))
    while True:
        image_name = random.choice(file_list)
        print("found file: " + image_name)
        image_name_splited = image_name.split(".")
        suffix = image_name_splited[-1].lower()
        if suffix in legal_image_suffix and len(image_name_splited) >= 2:
            image_file_relative_path = image_name
            print("found valid image: " + image_name)
            break
    image_path = os.path.normpath(
        folder_path + "/" + image_file_relative_path)
    change_desktop_background_with_image(image_path)


def main(argv):

    if platform.system() != "Windows":
        print("Unfortunately, we only support Windows.")
        exit(1)

    image_base_directory = ""
    slideshow_time = 60

    try:
        opts, args = getopt.getopt(
            argv, "h:p:t:v:", ["help", "PATH=", "TIME="])
    except getopt.GetoptError:
        print("getopt failed to get options.")
        show_help()
        exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit(0)
        elif opt in ("-p", "--PATH"):
            image_base_directory = arg
        elif opt in ("-t", "--TIME"):
            slideshow_time = int(arg)
    if image_base_directory == "":
        print("Missing options.")
        show_help()
        exit(3)

    if not check_base_folder_availability(image_base_directory):
        print("Base directory doesn't meet requirements.")
        exit(4)

    folder_list = os.listdir(image_base_directory)
    while True:
        year, month, day, hour, minute = map(
            int, time.strftime("%Y %m %d %H %M").split())
        current_hour = hour
        current_min = minute
        current_time = 100 * hour + minute
        print("Time: " + str(current_time))
        if current_time < 600:
            use_image_in_folder_to_set_background(
                image_base_directory + "/" + folder_name_for_config["night"])
        elif current_time < 1120:
            use_image_in_folder_to_set_background(
                image_base_directory + "/" + folder_name_for_config["forenoon"])
        elif current_time < 1330:
            use_image_in_folder_to_set_background(
                image_base_directory + "/" + folder_name_for_config["noon"])
        elif current_time < 1700:
            use_image_in_folder_to_set_background(
                image_base_directory + "/" + folder_name_for_config["afternoon"])
        elif current_time < 1930:
            use_image_in_folder_to_set_background(
                image_base_directory + "/" + folder_name_for_config["dusk"])
        else:
            use_image_in_folder_to_set_background(
                image_base_directory + "/" + folder_name_for_config["night"])
        time.sleep(slideshow_time)


if __name__ == "__main__":
    main(sys.argv[1:])
