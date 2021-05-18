
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
MeMAD approach for the TRECVID VSUM 2020 task
1) Scrap synopses following the instructions in the  `README.md`under 
[`scraping`](./scraping/)
2) Perform coreference using coref/coref.ipynb
3) Face recognition
4) Generate the summaries with submission/submission_generation.ipynb

![Model architecture](vsum.jpg)
