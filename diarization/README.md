# Diarization code and outputs

This folder contains diarization code and outputs. The dependencies are defined in the conda `environment.yml`. The diarization algorithm and models are in the `SphereDiar` folder. The algorithm also depends on the `spherecluster` algorithm in the folder with the same name. Additionally, segmentation uses `sox` command line tool.

### Full video diarization 

Script for diarizing full videos is in the notebook `full_video_diarization.ipynb`. The notebook `speaker_id_to_timestamp.ipynb` is an attempt to match the speaker ids to the p tags in the transcript xml-files. Issues encountered in the process are explained in the notebook.

### Segment diarization

Segment diarization is done in three steps:
 
 1. Python script `create_segmentation_commands.py` creates a bash script that will contain `sox` commands to split the videos (175-185) to segments using segmentation timestamps in `facerec_segment/segs`.
 2. The bash script generated in the previous step is run to create the segmented audio files.
 3. The notebook `segment_diarization.ipynb` runs diarization for each segmented audio file.

The results are stored in pickle files under data/segments folders. Each segment is stored in tuple which contains (segment-wav-filename, speaker-labels, clustering-upper-range). The diarization algorithm needs an estimate of how many speakers are in the audio, which is given as a range. Lower limit assumed to be two speakers in all cases but upper limit varies. The first upper limit was 8, but the diarization algorithm failed with that limit for several files, so one by one the limit was decreased to two. The `failed_diar.pickle` contains the files that could not be diarized with any range.
