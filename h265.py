import ffmpeg
import glob
import os
import logging
import sys
from tqdm import tqdm

# logging.basicConfig(level=logging.INFO)

if len(sys.argv) < 2:
    print("Usage: python3 app.py <directory>")
    sys.exit(1)

extensions = ['*.mp4', '*.mkv']
folder = sys.argv[1]


def is_h265(file):
    logging.info(f"checking if {file} is h265")

    codec = ffmpeg.probe(file)['streams'][0]['codec_name']

    if codec == 'h265' or codec == 'hevc':
        logging.info(f"{file} is h265")
        return True
    else:
        logging.info(f"{file} is not h265")
        return False


logging.info(f"reading files from {folder}")
files = []
for ext in extensions:
    files.extend(glob.glob(F"{folder}/**/{ext}", recursive=True))

for f in tqdm(files):
    if is_h265(f):
        logging.info(f"{f} is already h265")
        continue
    logging.info(f"converting {f} to h265")
    outname = F"{f.split('.')[-2]}_.{f.split('.')[-1]}"
    stream = ffmpeg.input(f)

    stream = ffmpeg.output(stream, outname, **{'c:v': 'libx265', 'vtag': 'hvc1', 'c:a': 'copy'})
    try:
        ffmpeg.run(stream)
    except Exception as e:
        logging.error(f"Failed to convert {f}")
        logging.error(e)
        continue

    os.remove(f)
    
