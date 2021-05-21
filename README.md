
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
1) Scrap synopses and casting information from the pages of the [EastEnders fandom wiki](https://eastenders.fandom.com/wiki/) using
[`scraping/scraping_wikia.py`](./scraping/scraping_wikia.py).
The script is standalone and only requires the two included XML files (episode code to file name mapping + episdoe descriptions). 
The output is a pickle of dictionary. Requirements: installing BeautifulSoup `pip install bs4`.




2) Perform coreference to explicit character mentions using [`coref/coref.ipynb`](./coref/coref.ipynb) created from [neuralcoref](https://github.com/huggingface/neuralcoref)
3) Face recognition
4) Generate the summaries with [`submission/submission_generation.ipynb`](./submission/submission_generation.ipynb)

![Model architecture](vsum.jpg)
