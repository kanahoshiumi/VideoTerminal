import argparse
import os
import subprocess
import time
from PlayTerminal import PlayTerminal

parser = argparse.ArgumentParser(description="Play a video in the terminal.")
parser.add_argument("videofile", help="video file path")
parser.add_argument("-r", "--height-ratio", help="video height scaling factor", default=2, type=float)
parser.add_argument("-n", "--no-ffplay", help="don't use ffplay flag", action="store_true")
parser.add_argument("-d", "--disp", help="display any video output", action="store_true")
parser.add_argument("-t", "--time", help="wait time", default=0, type=float)
args = parser.parse_args()

if os.path.isfile(args.videofile):
    if not args.no_ffplay:
        try:
            if args.disp:
                ffplay = subprocess.Popen(("ffplay", "-autoexit", "-loglevel", "quiet", args.videofile))
            else:
                ffplay = subprocess.Popen(("ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", args.videofile))
        except:
            pass
    try:
        time.sleep(args.time)
        PlayTerminal(args.videofile, args.height_ratio).play()
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h\033[0m", end="")
        os.system("cls" if os.name == "nt" else "clear")
        if not args.no_ffplay:
            try:
                ffplay.kill()
            except:
                pass
else:
    print(f"File not found: ${args.videofile}")

