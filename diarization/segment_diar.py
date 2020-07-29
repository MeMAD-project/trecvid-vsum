import os
import numpy as np
import wavefile
import pickle
from SphereDiar.embed import VLAD, amsoftmax_loss
from SphereDiar.meeting_corpus_util import *
from SphereDiar.SphereDiar import *
from librosa.util import frame
from librosa.feature import mfcc
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import scale
from keras.models import load_model
import warnings
#warnings.filterwarnings("ignore", message="Numerical issues were encountered ")

def fe(s, fs = 16000):
    mfcc_feat = mfcc(s, n_mfcc = 30, sr = fs, n_fft=512, hop_length=160)  
    return MinMaxScaler().fit_transform(mfcc_feat)
    #return scale(mfcc_feat, axis=1)

model_path = "./SphereDiar/models/current_best.h5"
emb_model = load_model(model_path, custom_objects={'VLAD': VLAD, 'amsoftmax_loss': amsoftmax_loss})
SD = SphereDiar(emb_model)
video_mapping = {"175": "5531550228324592939.mp4",
                 "176": "5534228999422914578.mp4",
                 "177": "5539381671692122744.mp4",
                 "178": "5542003749222140011.mp4",
                 "179": "5544574287152993687.mp4",
                 "180": "5544620672795594434.mp4",
                 "181": "5547193787702629969.mp4",
                 "182": "5549784941472309008.mp4",
                 "183": "5552368364300855101.mp4",
                 "184": "5555325449284154780.mp4",
                 "185": "5555360238519252381.mp4"}

seg_dirs = [d.name for d in os.scandir("./data") if d.is_dir() and d.name.startswith("segments_add2")]
seg_dirs.sort()

failed = []
for d in seg_dirs:
    print(f"Dealing with dir {d} next.")
    results = {"5531550228324592939.mp4": [],
               "5534228999422914578.mp4": [],
               "5539381671692122744.mp4": [],
               "5542003749222140011.mp4": [],
               "5544574287152993687.mp4": [],
               "5544620672795594434.mp4": [],
               "5547193787702629969.mp4": [],
               "5549784941472309008.mp4": [],
               "5552368364300855101.mp4": [],
               "5555325449284154780.mp4": [],
               "5555360238519252381.mp4": []}
    datapath = f"./data/{d}"
    wavs = [f.name for f in os.scandir(datapath) if f.name.endswith(".wav")]
    wavs.sort()
    for wavfile in wavs:
        print(f"Diarizing file {wavfile} now.")
        (rate, sig) = wavefile.load(f"{datapath}/{wavfile}")
        signal = sig[0]
        S = np.transpose(frame(signal, int(2000*16), int(500*16)))
        X = list(map(lambda s: fe(s, 16000), S))
        X = np.array(np.swapaxes(X, 1, 2))
        X = X.astype(np.float16)
        num_timesteps = X.shape[1]

        if num_timesteps != 201:
            emb_model.layers.pop(0)
            new_input = Input(batch_shape=(None, num_timesteps, 30))
            new_output = emb_model(new_input)
            emb_model = Model(new_input, new_output)

        embs = emb_model.predict(X)
        try:
            SD.cluster(rounds=10, clust_range=[2, 8], num_cores = -2, embeddings=embs)
            spk_labels = SD.speaker_labels_
        except ValueError:
            spk_labels = []
            failed.append(f"{datapath}/{wavfile}")
        short_name = wavfile[:3]
        long_name = video_mapping[short_name]
        results[long_name].append((wavfile, spk_labels))
    print("Saving results to a pickle.")
    pickle.dump(results, open(f"{datapath}/segmented_diarization.pickle", 'wb'))

pickle.dump(failed, open("data/failed_diar_second.pickle", 'wb'))