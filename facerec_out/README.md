This folder contains the output of the Face Recognition service.

The output includes all faces which span at least 2 seconds, with different confidence scores, which should be filtered.

This output in particular shows low confidence scores (<0.3), so probably an overall check needs to be performed.

Respect to the original [facerec module](https://github.com/D2KLab/Face-Celebrity-Recognition), the process has been fully automatised, using embedding variance to filter out outlier (read _wrong_) pictures from the ones downloaded from YouTube.
