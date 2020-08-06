This folder contains the output of the Face Recognition service.

The output includes all faces which span at least 2 seconds, with different confidence scores, which should be filtered.


Respect to the original [facerec module](https://github.com/D2KLab/Face-Celebrity-Recognition), the process has been fully automatised, using embedding variance to filter out outlier (read _wrong_) pictures from the ones downloaded from YouTube.

### 1.all_people

Trained on the full list of 76 people extracted by [the scraping algorithm]('../scraping').
This output in particular shows low confidence scores (<0.3), so probably an overall check needs to be performed.

### 2.challenge_people

Trained on the 3 people (Janine, Ryan, Stacey) which are focus of the challenge.


### 3.coref_people

Trained on 14 people, coreferenced in the wiki with the challenge people [include reference].
The list is:
- Ryan Malloy
- Stacey Branning
- Janine Malloy
- Kat Moon
- Pat Evans
- Billy Mitchell
- Alfie Moon
- Phil Mitchell
- Max Branning
- Lauren Branning
- Jean Slater
- Julie Perkins
- Ronnie Branning
- Roxy Mitchell
