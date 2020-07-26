import glob
import pickle
import os

"""
Run this file to automatically write bash scripts that use sox to
split the original videos (175-185) to segments. Re-encode each mp4 
video file as wav audiofile before running this.
"""

seg_path = "../facerec_segment/segs/*.pickle"
segmentations = glob.glob(seg_path)
segmentations.sort()

video_mapping = [("5531550228324592939.mp4", "175.wav"),
                 ("5534228999422914578.mp4", "176.wav"),
                 ("5539381671692122744.mp4", "177.wav"),
                 ("5542003749222140011.mp4", "178.wav"),
                 ("5544574287152993687.mp4", "179.wav"),
                 ("5544620672795594434.mp4", "180.wav"),
                 ("5547193787702629969.mp4", "181.wav"),
                 ("5549784941472309008.mp4", "182.wav"),
                 ("5552368364300855101.mp4", "183.wav"),
                 ("5555325449284154780.mp4", "184.wav"),
                 ("5555360238519252381.mp4", "185.wav")]

for s in segmentations:
    with open(s, 'rb') as sfile:
        segs = pickle.load(sfile)
    sname = os.path.basename(s)[0:-7]
    os.mkdir(f"data/{sname}", mode=0o755)
    sox_cmds = ["#!/bin/bash\n", "\n"]
    n = 1
    for long_name, short_name in video_mapping:
        for begin, end in segs[long_name]:
            basename_short, _ = short_name.split(".")
            sox_cmds.append(f"sox ../{short_name} {basename_short}_{n:03}.wav trim {begin} '={end}'\n")
            n = n + 1
        n = 1
    with open(f"./data/{sname}/sox_seg_split.sh", "w") as f:
        f.writelines(sox_cmds)
