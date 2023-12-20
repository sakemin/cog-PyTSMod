# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from typing import List
from cog import BasePredictor, BaseModel, Input, Path

import numpy as np
import pytsmod as tsm
import soundfile as sf

import os 

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""


    def predict(
        self,
        audio_input: Path = Input(
            description="An audio file input to time stretch.",
            default=None,
        ),
        method: str = Input(
            description="Name of the method to use",
            default="WSOLA",
            choices=["OLA", "WSOLA", "PV-TSM", "PV-TSM-int", "TD-PSOLA"]
        ),
        s_fixed: float = Input(
            description="Time stretching factor s as a constant value.",
            default=1,
            ge=0,
        ),
        s_ap: str = Input(
            description="Input/Output anchor point pair array for dynamic time stretching. Time stretching factor s as an 2 x n array of anchor points formatted in dict type[`input relative frame ratio`(0.0~1.0):`output relative frame ratio`]. (eg. [0:0, 0.5:1, 1:1.7] means first half;0~50% of the audio will be stretched 2x, and the last half;50~100% of the audio will be streched 140%.) Each input value has to be between 0.0 ~ 1.0, which represents the relative position of the anchor.(0 : starting point of an audio, 1 : the length;end point of an audio) When `s_ap` is given, s_fixed will be ignored.",
            default=None,
        ),
        td_psola_pitch_shift: str = Input(
            description="Only for `TD-PSOLA` method. If `key`, pitch will be shifted based on `td_psola_key_updown`. If `pitch`, pitch will be shifted based on `td_psola_pitch_ratio`. If `None`, only time stretching will be performed based on `s_fixed`, and pitch shifting will not be applied.",
            default="None",
            choices=["key", "pitch", "None"]
        ),
        td_psola_key_updown: int = Input(
            description="Only for `TD-PSOLA` method when `td_psola_pitch_shift` is `key`. Value for pitch shifting based on 12 key system. (eg. 3 : 3 keys up, -5 : 5 keys down, 12:== +1 octave)",
            default=None,
        ),
        td_psola_pitch_ratio: float = Input(
            description="Only for `TD-PSOLA` method when `td_psola_pitch_shift` is `pitch`. Value for pitch shifting based on relative ratio. (eg. 1.0 : original pitch, 0.5 : -1 octave, 2.0 : +1 octave)",
            default=None,
            ge=0,
        ),
        td_psola_dynamic_key: str = Input(
            description="Only for `TD-PSOLA` method when `td_psola_pitch_shift` is `key`. Overrides `td_psola_key_updown`. Dynamic pitch shift. Must be formatted in dict type[`relative frame ratio`(0.0~1.0):`key_shift_amount`]. (eg. [0.3:1, 0.6:-2] means for first 0 ~ 30% part of the audio, it keeps the original key, for 30 ~ 60% key is shifted +1 and for 60 ~ 100% key is shifted -2.)",
            default=None,
        ),
        td_psola_dynamic_pitch: str = Input(
            description="Only for `TD-PSOLA` method when `td_psola_pitch_shift` is `pitch`. Overrides `td_psola_pitch_ratio`. Dynamic pitch shift. Must be formatted in dict type[`relative frame ratio`(0.0~1.0):`pitch_shift_amount`]. (eg. [0.5:2, 0.8:1.3] means for first 0 ~ 50% part of the audio, it keeps the original key, for 50 ~ 80% pitch is shifted +1 octave and for 80 ~ 100% pitch is shifted 130% of original pitch value.)",
            default=None,
        ),
        absolute_second: bool = Input(
            description="If `True`, `s_ap` and `td_psola_dynamic_*` use absolute second metric. If `False`, relative ratio value(0 : starting point of an audio, 1 : the length;end point of an audio) is used.",
            default=False,
        ),
    ) -> Path:
        
        if not audio_input:
            raise ValueError("Must provide `audio_input`.")


        output_dir = 'output.wav'

        if os.path.isfile('output.wav'):
            os.remove('output.wav')
        if os.path.isdir('output.wav'):
            import shutil
            shutil.rmtree('output.wav')
        if os.path.isfile('output'):
            os.remove('output')
        if os.path.isdir('output'):
            import shutil
            shutil.rmtree('output')

        if s_ap=="":
            s_ap=None
        if td_psola_dynamic_key=="":
            td_psola_dynamic_key=None
        if td_psola_dynamic_pitch=="":
            td_psola_dynamic_pitch=None

        x, sr = sf.read(audio_input)
        x = x.T
        x_length = x.shape[-1]

        if method=='OLA':
            ts = tsm.ola
        elif method=='WSOLA':
            ts = tsm.wsola
        elif method=='PV-TSM':
            ts = tsm.phase_vocoder
        elif method=='PV-TSM-int':
            ts = tsm.phase_vocoder_int
        elif method=='TD-PSOLA':
            ts = tsm.tdpsola
        else:
            raise ValueError("`method` value error")

        if method=='TD-PSOLA':
            import crepe
            _, f0_crepe, _, _ = crepe.predict(x.T, sr, viterbi=True, step_size=10)
            if td_psola_pitch_shift == 'key':
                if td_psola_dynamic_key is None:
                    if td_psola_key_updown is None:
                        raise ValueError("You must specify either `td_psola_key_updown` or `td_psola_dynamic_key` when `td_psola_pitch_shift` is `key`.")
                    x_s = tsm.tdpsola(x, sr, f0_crepe, alpha=s_fixed, beta=pow(2, td_psola_key_updown/12), p_hop_size=441, p_win_size=1470)
                else:
                    td_psola_dynamic_key = "0:0, " + td_psola_dynamic_key
                    if absolute_second:
                        tgt_f0_array = np.array([[float(j[0]),float(j[1])] for j in [i.split(":") for i in td_psola_dynamic_key.replace(" ","").split(',')]]).T
                        tgt_f0_weight=[]
                        for i in range(1,tgt_f0_array.shape[-1]):
                            tgt_f0_weight.append(np.full(int((tgt_f0_array[0][i]-tgt_f0_array[0][i-1])*(sr/441)), pow(2, tgt_f0_array[1][i]/12)))
                        tgt_f0_weight = np.concatenate(tgt_f0_weight)
                    else:
                        tgt_f0_array = np.array([[float(j[0]),float(j[1])] for j in [i.split(":") for i in td_psola_dynamic_key.replace(" ","").split(',')]]).T
                        print(tgt_f0_array)
                        tgt_f0_weight=[]
                        for i in range(1,tgt_f0_array.shape[-1]):
                            print(i, tgt_f0_array[1][i], pow(2, tgt_f0_array[1][i]/12))
                            tgt_f0_weight.append(np.full(int(f0_crepe.shape[0]*(tgt_f0_array[0][i]-tgt_f0_array[0][i-1])), pow(2, tgt_f0_array[1][i]/12)))
                        tgt_f0_weight = np.concatenate(tgt_f0_weight)
                    if tgt_f0_weight.shape[0] < f0_crepe.shape[0]:
                        tgt_f0_weight = np.concatenate([tgt_f0_weight,np.full((f0_crepe.shape[0]-tgt_f0_weight.shape[0]),tgt_f0_weight[-1])])
                    tgt_f0_weight = tgt_f0_weight[:f0_crepe.shape[0]]
                    x_s = tsm.tdpsola(x, sr, alpha=s_fixed, src_f0=f0_crepe, tgt_f0=f0_crepe*tgt_f0_weight, p_hop_size=441, p_win_size=1470)
            elif td_psola_pitch_shift == 'pitch':
                if td_psola_dynamic_pitch is None:
                    if td_psola_pitch_ratio is None:
                        raise ValueError("You must specify either `td_psola_pitch_ratio` or `td_psola_dynamic_pitch` when `td_psola_pitch_shift` is `pitch`.")
                    x_s = tsm.tdpsola(x, sr, f0_crepe, alpha=s_fixed, beta=td_psola_pitch_ratio, p_hop_size=441, p_win_size=1470)
                else:
                    td_psola_dynamic_pitch = "0:0, " + td_psola_dynamic_pitch
                    if absolute_second:
                        tgt_f0_array = np.array([[float(j[0]),float(j[1])] for j in [i.split(":") for i in td_psola_dynamic_pitch.replace(" ","").split(',')]]).T
                        tgt_f0_weight=[]
                        for i in range(1,tgt_f0_array.shape[-1]):
                            tgt_f0_weight.append(np.full(int((tgt_f0_array[0][i]-tgt_f0_array[0][i-1])*(sr/441)), tgt_f0_array[1][i]))
                        tgt_f0_weight = np.concatenate(tgt_f0_weight)
                    else:
                        tgt_f0_array = np.array([[float(j[0]),float(j[1])] for j in [i.split(":") for i in td_psola_dynamic_pitch.replace(" ","").split(',')]]).T
                        tgt_f0_weight=[]
                        for i in range(1,tgt_f0_array.shape[-1]):
                            tgt_f0_weight.append(np.full(int(f0_crepe.shape[0]*(tgt_f0_array[0][i]-tgt_f0_array[0][i-1])), tgt_f0_array[1][i]))
                        tgt_f0_weight = np.concatenate(tgt_f0_weight)
                    if tgt_f0_weight.shape[0] < f0_crepe.shape[0]:
                        tgt_f0_weight = np.concatenate([tgt_f0_weight,np.full((f0_crepe.shape[0]-tgt_f0_weight.shape[0]),tgt_f0_weight[-1])])
                    tgt_f0_weight = tgt_f0_weight[:f0_crepe.shape[0]]
                    x_s = tsm.tdpsola(x, sr, alpha=s_fixed, src_f0=f0_crepe, tgt_f0=f0_crepe*tgt_f0_weight, p_hop_size=441, p_win_size=1470)
            else:
                x_s = ts(x, sr, f0_crepe, alpha = s_fixed, p_hop_size=441, p_win_size=1470)
        else:
            if s_fixed and not s_ap:
                x_s = ts(x, s_fixed)
            elif s_ap:
                s_ap = s_ap.replace(" ", "")
                if absolute_second:
                    s_ap = np.array([[float(i[0]) * sr, float(i[1]) * sr] for i in [s.split(':') for s in s_ap.split(',')]]).T
                    x_s = ts(x, s_ap)
                else:
                    s_ap = np.array([[float(i[0]) * x_length, float(i[1]) * x_length] for i in [s.split(':') for s in s_ap.split(',')]]).T
                    x_s = ts(x, s_ap)
            else:
                raise ValueError("You must provied either `s_fixed`, or `s_ap` when using non-TD-PSOLA methods.")

        sf.write(output_dir, x_s.T, sr, format='WAV')

        return Path(output_dir)
    