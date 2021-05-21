
Please cite the following if you use this code.
```
@inproceedings{harrando2020using,
  title={Using Fan-Made Content, Subtitles and Face Recognition for Character-Centric Video Summarization},
  author={Harrando, Ismail and Reboud, Alison and Lisena, Pasquale and Troncy, Rapha{\"e}l and Laaksonen, Jorma and Virkkunen, Anja and Kurimo, Mikko and others},
  booktitle={International Workshop on Video Retrieval Evaluation},
  year={2020}
}
```

# trecvid-vsum
Steps to reproduce the final MeMAD approach for the TRECVID VSUM 2020 task
![Model architecture](vsum.jpg)

1) Using [`shots_transcripts_alignment.ipynb`](./transcripts/shots_transcripts_alignment.ipynb), align the transcript content with the shot ID (i.e. finding what was said in each shot based on the transcript and shot boundaries)
2) Scrape synopses and casting information from the pages of the [EastEnders fandom wiki](https://eastenders.fandom.com/wiki/) using
[`scraping/scraping_wikia.py`](./scraping/scraping_wikia.py).
The script is standalone and only requires the two included XML files (episode code to file name mapping + episdoe descriptions). 
The output is a pickle of dictionary ('episodes_data.pickle') Requirements: installing BeautifulSoup `pip install bs4`.
2) Perform coreference on the pickle file you just created ('episodes_data.pickle') to explicit character mentions using [`coref/coref.ipynb`](./coref/coref.ipynb) created from [neuralcoref](https://github.com/huggingface/neuralcoref). Outputs 'coref_results.pickle'
3) Face recognition: we select the shots displaying any of the the three characters of interests, keeping only those detection having a confidence scoregreater than 0.5 ([`facerec_query_characters.csv`]([facerec_segment/facerec_query_characters.csv]).
In order to do so, we performed face recognition using our  [Face Recognition Service](https://github.com/D2KLab/FaceRec). The results can be found under [facerec_out](./facerec_out) (2.challenge_people). We use [`facerec_output_preprocessing.ipynb`](./facerec_segmentation/facerec_output_preprocessing.ipynb) to transform the JSON output into a CSV files with timestamps for each detection, then  [`facerec_segmentation.ipynb`](./facerec_segmentation/facerec_segmentation.ipynb) to align the detections with the shot IDs.
Note : this folder also includes facerec results for a larger pool of EastEnders characters, as well as results of facerec with different thresholds of confidence, which experimented with but did not use in the final submission.
4) Generate the shot candidate shots for the summary with [`submission_generation.ipynb`](./submission/submission_generation.ipynb). This is done by first concatenating the output of the previous steps (i.e. aligning coreference-resolved transcripts and facerec output with the (facerec_segment/eastenders.masterShotReferenceTable.txt)[master shot reference table]), so that the content of each shot is aligned (time-wise) with the shot IDs. The next step is to compute the similarity between each shot content and the synopses sentences as described in the paper. The N shots (N varying per run) with the higher similarity scores are picked and written into XML files ([`submissions`](./submission/xml)).

Experiments not included in the final approach for TRECVID VSUM 2020 task : 

1) Concatening subtitles with automatically generated captions, see [`captions`](./captions)
2) Diarization of the video segments, see [`diarization`](./diarization)


