# Cog Implementation of PyTSMod

[![Replicate](https://replicate.com/sakemin/pytsmod/badge)](https://replicate.com/sakemin/pytsmod) 

[PyTSMod](https://replicate.com/sakemin/pytsmod) is an open-source library for Time-Scale Modification algorithms in Python 3. PyTSMod contains basic TSM algorithms such as Overlap-Add (OLA), Waveform-Similarity Overlap-Add (WSOLA), Time-Domain Pitch-Synchronous Overlap-Add (TD-PSOLA), and Phase Vocoder (PV-TSM). We are also planning to add more TSM algorithms and pitch shifting algorithms.

Full documentation is available on [https://pytsmod.readthedocs.io](https://pytsmod.readthedocs.io)

For more information about this model, see [here](https://github.com/KAIST-MACLab/PyTSMod).

You can demo this model or learn how to use it with Replicate's API [here](https://replicate.com/sakemin/pytsmod). 

## Prediction
### Default Model
- In this repository, the default prediction model is configured as the melody model.
- After completing the fine-tuning process from this repository, the trained model weights will be loaded into your own model repository on Replicate.

# Run with Cog

[Cog](https://github.com/replicate/cog) is an open-source tool that packages machine learning models in a standard, production-ready container. 
You can deploy your packaged model to your own infrastructure, or to [Replicate](https://replicate.com/), where users can interact with it via web interface or API.

## Prerequisites 

**Cog.** Follow these [instructions](https://github.com/replicate/cog#install) to install Cog, or just run: 

```
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
```

Note, to use Cog, you'll also need an installation of [Docker](https://docs.docker.com/get-docker/).

* **GPU machine.** You'll need a Linux machine with an NVIDIA GPU attached and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) installed. If you don't already have access to a machine with a GPU, check out our [guide to getting a 
GPU machine](https://replicate.com/docs/guides/get-a-gpu-machine).

## Step 1. Clone this repository

```sh
git clone https://github.com/sakemin/cog-PyTSMod
```

## Step 2. Run the model

To run the model, you need a local copy of the model's Docker image. You can satisfy this requirement by specifying the image ID in your call to `predict` like:

```
cog predict r8.im/sakemin/pytsmod@sha256:111a5a32eb68a246da58451ff398444b2f692a2543cc132a02cfad4c45111cec -i audio_input=@/your/audio/file.wav -i s_fixed=2
```

For more information, see the Cog section [here](https://replicate.com/sakemin/pytsmod/api#run)

Alternatively, you can build the image yourself, either by running `cog build` or by letting `cog predict` trigger the build process implicitly. For example, the following will trigger the build process and then execute prediction: 

```
cog predict -i audio_input=@/your/audio/file.wav -i s_fixed=2
```

Note, the first time you run `cog predict`, model weights and other requisite assets will be downloaded if they're not available locally. This download only needs to be executed once.

# Run on replicate

## Step 1. Ensure that all assets are available locally

If you haven't already, you should ensure that your model runs locally with `cog predict`. This will guarantee that all assets are accessible. E.g., run: 

```
cog predict -i audio_input=@/your/audio/file.wav -i s_fixed=2
```

## Step 2. Create a model on Replicate.

Go to [replicate.com/create](https://replicate.com/create) to create a Replicate model. If you want to keep the model private, make sure to specify "private".

## Step 3. Configure the model's hardware

Replicate supports running models on variety of CPU and GPU configurations. 

Click on the "Settings" tab on your model page, scroll down to "GPU hardware", and select "T4". Then click "Save".

## Step 4: Push the model to Replicate


Log in to Replicate:

```
cog login
```

Push the contents of your current directory to Replicate, using the model name you specified in step 1:

```
cog push r8.im/username/modelname
```

[Learn more about pushing models to Replicate.](https://replicate.com/docs/guides/push-a-model)

## Time Stretching
- With the methods `OLA`, `WSOLA` and `PV-TSM`, constant ratio time stretching is available with `s_fixed` value, and also dynamic time stretching is available with `s_ap`.
- `s_ap` takes anchor point pair values in `dict` format. 
- Anchor point value is based on 0~1, 0 means the starting point of audio, and 1 means the end point of audio. (eg. `0:0, 0.5:1, 1:1.7` means first half;0~50% of the audio will be stretched 2x, and the last half;50~100% of the audio will be streched 140%.)
- With setting `absolute_second` as `True`, anchor point value is taken with absolute second metric.

## Key/Pitch Shifting
- `TD-PSOLA` method offers key/pitch shifting in both constant and dynamic ways.
- Key shifting is available with setting `td_psola_pitch_shift` as `key`.
- `td_psola_key_updown` for fixed constant key shifting.
- `td_psola_dynamic_key` for dynamic key shifting. Must be formatted in dict type[`relative frame ratio`(0.0~1.0):`key_shift_amount`]. (eg. [0.3:0, 0.6:1, 1:-2] means for first 0 ~ 30% part of the audio, it keeps the original key, for 30 ~ 60% key is shifted +1 and for 60 ~ 100% key is shifted -2.)
- Pitch shifting is available with setting `td_psola_pitch_shift` as `pitch`.
- `td_psola_pitch_ratio ` for fixed constant pitch shifting.
- `td_psola_dynamic_pitch ` for dynamic pitch shifting. Must be formatted in dict type[`relative frame ratio`(0.0~1.0):`pitch_shift_amount`]. (eg. [0.5:1, 0.8:2, 1:1.3] means for first 0 ~ 50% part of the audio, it keeps the original key, for 50 ~ 80% pitch is shifted +1 octave and for 80 ~ 100% pitch is shifted 130% of original pitch value.)
- With setting `absolute_second` as `True`, anchor point value is taken with absolute second metric.

# PyTSMod

[![PyPI](https://img.shields.io/pypi/v/pytsmod.svg)](https://pypi.python.org/pypi/pytsmod)
[![Build Status](https://img.shields.io/github/actions/workflow/status/KAIST-MACLab/PyTSMod/.github%2Fworkflows%2Fpython-package.yml)](https://github.com/KAIST-MACLab/PyTSMod/actions/workflows/python-package.yml)
![Python](https://img.shields.io/pypi/pyversions/pytsmod.svg)
![license](https://img.shields.io/github/license/KAIST-MACLab/PyTSMod.svg)
![downloads](https://img.shields.io/pypi/dm/pytsmod.svg)

PyTSMod is an open-source library for Time-Scale Modification algorithms in Python 3. PyTSMod contains basic TSM algorithms such as Overlap-Add (OLA), Waveform-Similarity Overlap-Add (WSOLA), Time-Domain Pitch-Synchronous Overlap-Add (TD-PSOLA), and Phase Vocoder (PV-TSM). We are also planning to add more TSM algorithms and pitch shifting algorithms.

Full documentation is available on <https://pytsmod.readthedocs.io>

![open-issues](https://img.shields.io/github/issues/KAIST-MACLab/pytsmod.svg)
![closed-issues](https://img.shields.io/github/issues-closed/KAIST-MACLab/pytsmod.svg)
![open-prs](https://img.shields.io/github/issues-pr/KAIST-MACLab/pytsmod.svg)
![closed-prs](https://img.shields.io/github/issues-pr-closed/KAIST-MACLab/pytsmod.svg)

The implementation of the algorithms are based on those papers and libraries:

> [TSM Toolbox: MATLAB Implementations of Time-Scale Modification Algorithms.](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/2014_DriedgerMueller_TSM-Toolbox_DAFX.pdf)<br>
> Jonathan Driedger, Meinard Müller.<br>
> Proceedings of the 17th International Conference on Digital Audio Effects (DAFx-14), 2014.

> [A review of time-scale modification of music signals.](https://www.mdpi.com/2076-3417/6/2/57htm)<br>
> Jonathan Driedger, Meinard Müller.<br>
> Applied Sciences, 6(2), 57, 2016.

> [DAFX: digital audio effects](https://books.google.co.kr/books?hl=ko&lr=&id=DX-mRhkJL74C&oi=fnd&pg=PT7&dq=Dafx+book&ots=EMFASHiHrs&sig=Mtft4q1dJgFXjOsDnLyMN9eKMRQ#v=onepage&q=Dafx%20book&f=false)<br>
> Udo Zölzer.<br>
> John Wiley & Sons, 2011.


## Installing PyTSMod

PyTSMod is hosted on PyPI. To install, run the following command in your Python environment:

```bash
$ pip install pytsmod
```

Or if you use [poetry](https://python-poetry.org), you can clone the repository and build the package through the following command:

```bash
$ poetry build
```

### Requirements

To use the latest version of PyTSMod, Python with version >= 3.8 and following packages are required.

- NumPy (>=1.20.0)
- SciPy (>=1.8.0)
- soundfile (>=0.10.0)

## Using PyTSMod

### Using OLA, WSOLA, and PV-TSM

OLA, WSOLA, and PV-TSM can be imported as module to be used directly in Python. To get the result easily, all you need is just two parameters, the input audio sequence x and the time stretching factor s. Here's a minimal example:

```python
import numpy as np
import pytsmod as tsm
import soundfile as sf  # you can use other audio load packages.

x, sr = sf.read('/FILEPATH/AUDIOFILE.wav')
x = x.T
x_length = x.shape[-1]  # length of the audio sequence x.

s_fixed = 1.3  # stretch the audio signal 1.3x times.
s_ap = np.array([[0, x_length / 2, x_length], [0, x_length, x_length * 1.5]])  # double the first half of the audio only and preserve the other half.

x_s_fixed = tsm.wsola(x, s_fixed)
x_s_ap = tsm.wsola(x, s_ap)
```

#### Time stretching factor s

Time stretching factor s can either be a constant value (alpha) or an 2 x n array of anchor points which contains the sample points of the input signal in the first row and the sample points of the output signal in the second row.


### Using TD-PSOLA

When using TD-PSOLA, the estimated pitch information of the source you want to modify is needed. Also, you should know the hop size and frame length of the pitch tracking algorithm you used. Here's a minimal example:

```python
import numpy as np
import pytsmod as tsm
import crepe  # you can use other pitch tracking algorithms.
import soundfile as sf  # you can use other audio load packages.

x, sr = sf.read('/FILEPATH/AUDIOFILE.wav')

_, f0_crepe, _, _ = crepe.predict(x, sr, viterbi=True, step_size=10)

x_double_stretched = tsm.tdpsola(x, sr, f0_crepe, alpha=2, p_hop_size=441, p_win_size=1470)  # hop_size and frame_length for CREPE step_size=10 with sr=44100
x_3keyup = tsm.tdpsola(x, sr, f0_crepe, beta=pow(2, 3/12), p_hop_size=441, p_win_size=1470)
x_3keydown = tsm.tdpsola(x, sr, f0_crepe, tgt_f0=f0_crepe * pow(2, -3/12), p_hop_size=441, p_win_size=1470)
```

#### Time stretching factor alpha

In this version, TD-PSOLA only supports the fixed time stretching factor alpha.

#### Pitch shifting factor beta and target_f0

You can modify pitch of the audio sequence in two ways. The first one is beta, which is the fixed pitch shifting factor. The other one is target_f0, which supports target pitch sequence you want to convert. You cannot use both of the parameters.

### Using PyTSMod from the command line

From version 0.3.0, this package includes a command-line tool named `tsmod`, which can create the result file easily from a shell. To generate the WSOLA result of `input.wav` with stretching factor 1.3 and save to `output.wav`, please run:

```shell
$ tsmod wsola input.wav output.wav 1.3  # ola, wsola, pv, pv_int are available.
```

Currently, OLA, WSOLA, and Phase Vocoder(PV) are supported. TD-PSOLA is excluded due to the difficulty of sending extracted pitch data to TD-PSOLA. Also, non-linear TSM is not supported in command-line.

For more information, use `-h` or `--help` command to see the detailed usage of `tsmod`.

## Audio examples

The original audio is from TSM toolbox.

### Stretching factor α=0.5

| Name | Method | Original | OLA | WSOLA | Phase Vocoder | Phase Vocoder (phase locking) | TSM based on HPSS |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| CastanetsViolin | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_0.50_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_0.50_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_0.50_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_0.50_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_0.50_HP.wav) |
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/12W-koxh8OkyrzEHibVifoYtWmuKCIbxy/view?usp=sharing) | [wav](https://drive.google.com/file/d/1juWR2-jx5rlPLv2JxhIiJZa83T7kgp3C/view?usp=sharing) | [wav](https://drive.google.com/file/d/1KdiTUkpdm1qMmMkdqkrMJhoRW_asUoqJ/view?usp=sharing) | [wav](https://drive.google.com/file/d/1dTSeSxkUGAEW75fpgFQXE9VoRuu3cgUR/view?usp=sharing) | [wav](https://drive.google.com/file/d/1W7saDSQCYEOc2ahqi7D4fAPZc2bCryrm/view?usp=sharing) |
| DrumSolo | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_0.50_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_0.50_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_0.50_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_0.50_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_0.50_HP.wav)
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1RD-rK0yInskaWuDhuKGPxMc1zzIMZFSv/view?usp=sharing) | [wav](https://drive.google.com/file/d/1PCxQTpzHbub-tpnqFYpbR-SEOpjq5L1m/view?usp=sharing) | [wav](https://drive.google.com/file/d/1QXbRdHN3UVBmnXax_FpNDPf3dAyKIlhi/view?usp=sharing) | [wav](https://drive.google.com/file/d/1vRPXSfgyvnTPVgSTGeryBtReYqFC1GC8/view?usp=sharing) | [wav](https://drive.google.com/file/d/19eQyATSxJB1Ia6eBBTHaz1OycsbAL0qM/view?usp=sharing) |
| Pop | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_0.50_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_0.50_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_0.50_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_0.50_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_0.50_HP.wav)
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1y8MFOQ4uEhs_S2V_FpPHfPeLCOpfdLAa/view?usp=sharing) | [wav](https://drive.google.com/file/d/1E6SlzID07ZmHOLE_GW3Dz3HizmnMf13U/view?usp=sharing) | [wav](https://drive.google.com/file/d/1pDcNsUyzGP3yr_TA7G7vJzBRi6bHuuTL/view?usp=sharing) | [wav](https://drive.google.com/file/d/1fbkMupHp8PTXIg6_QINDTyBWkfnzO7DA/view?usp=sharing) | [wav](https://drive.google.com/file/d/1lnP-75-QsIwXXfqsXqKPN6z4Qs4s_AWc/view?usp=sharing) |
| SingingVoice | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_0.50_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_0.50_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_0.50_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_0.50_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_0.50_HP.wav) |
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1pzzm1xBB4Qo-vcAdrxDSHiec4CWPpds8/view?usp=sharing) | [wav](https://drive.google.com/file/d/1Oq-CiDbw4i20RoSqsx8YMDvq3p_TV06x/view?usp=sharing) | [wav](https://drive.google.com/file/d/10eh-jad5_VhCqiR6F_irK5jXp0rlq2ay/view?usp=sharing) | [wav](https://drive.google.com/file/d/1iAgToNlK7LMFA-VVMlB3O_hPiChJZN34/view?usp=sharing) | [wav](https://drive.google.com/file/d/1LUHXGkYc-4IBpuM0DiQn_pBGS30-hFMR/view?usp=sharing) |

### Stretching factor α=1.2

| Name | Method | Original | OLA | WSOLA | Phase Vocoder | Phase Vocoder (phase locking) | TSM based on HPSS |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| CastanetsViolin | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.20_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.20_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.20_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.20_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.20_HP.wav) |
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1o7BtVNyZ9IYF5Jf6llwoMtFMYpzc9Idj/view?usp=sharing) | [wav](https://drive.google.com/file/d/1IDS4TjmhE3Ge2lD_xbN8Flw508ta_OV7/view?usp=sharing) | [wav](https://drive.google.com/file/d/1rMjZcG4Izrlc9_cHdN96KP6EwdgwsLg4/view?usp=sharing) | [wav](https://drive.google.com/file/d/1GMEYrePkNejHEBE9n0DyTnnjiEpUm3wi/view?usp=sharing) | [wav](https://drive.google.com/file/d/1QMRE7Qo5SuCgqhHSz6_DZWWWS-joh3T4/view?usp=sharing) |
| DrumSolo | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.20_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.20_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.20_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.20_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.20_HP.wav)
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1YgqwREMoOfSf2VPXLkzLNewKFlJ0iqmR/view?usp=sharing) | [wav](https://drive.google.com/file/d/1ZT-v8x65uRnhTRf9us8NI3NuoO8ia3m7/view?usp=sharing) | [wav](https://drive.google.com/file/d/1uGB4L5ffzwew7aeEqT1Yu1HGIXemupWc/view?usp=sharing) | [wav](https://drive.google.com/file/d/13k8CEktMpkRrrUSKnrVONqM8_yI1SysC/view?usp=sharing) | [wav](https://drive.google.com/file/d/1uozKTawYC9i8f5jbD4SoQjxh4PhjL-i8/view?usp=sharing) |
| Pop | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.20_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.20_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.20_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.20_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.20_HP.wav)
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1gj3PpiMR7OMPrRDej9Z-oxRf0b-ik-Gf/view?usp=sharing) | [wav](https://drive.google.com/file/d/1GKCkZU2dOVTk6ImDfEf3Gf3PrZxcReHW/view?usp=sharing) | [wav](https://drive.google.com/file/d/19Y02rGU6YEzAHtvSfpdHtBvlda8EGQZ6/view?usp=sharing) | [wav](https://drive.google.com/file/d/1yVye1wHpxeuCXOAZaVfWOC4G6xL4H_Hu/view?usp=sharing) | [wav](https://drive.google.com/file/d/1qfRglRBEzQDwI3iXhb-2RdNkYULJnNQC/view?usp=sharing) |
| SingingVoice | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.20_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.20_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.20_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.20_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.20_HP.wav) |
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1IxMpXjuBzrVbofo8FMMbkOREZkaW17bQ/view?usp=sharing) | [wav](https://drive.google.com/file/d/1iXpWEIKKHTkx0VCTxtXbhAIyxVO5CLme/view?usp=sharing) | [wav](https://drive.google.com/file/d/1XH_5sfZLSDgziXEbK_ApltScGVS0EVHT/view?usp=sharing) | [wav](https://drive.google.com/file/d/1sgBpTOz_WYVc8iDTQyjxmzHZYhgu0elS/view?usp=sharing) | [wav](https://drive.google.com/file/d/1eT9yKW-LTfifjr0C8Y1X4DghLLNXsz4W/view?usp=sharing) |

### Stretching factor α=1.8

| Name | Method | Original | OLA | WSOLA | Phase Vocoder | Phase Vocoder (phase locking) | TSM based on HPSS |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| CastanetsViolin | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.80_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.80_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.80_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.80_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/CastanetsViolin_1.80_HP.wav) |
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/14pwBV64ycLHdBUgGbpNm0qfL_asIwlIK/view?usp=sharing) | [wav](https://drive.google.com/file/d/1IBRwYsBHaTOTfdUFZuOvGhvsSJOy4TwA/view?usp=sharing) | [wav](https://drive.google.com/file/d/1Rkw1Gg83_7t8bMZ4uO2PTalP8PexMsZH/view?usp=sharing) | [wav](https://drive.google.com/file/d/1aaEHj4dhpxiruesUXGmtNqz5ar-H7jkx/view?usp=sharing) | [wav](https://drive.google.com/file/d/15u0ToohxKpIYnelO0RlKsLv0CTqamIiZ/view?usp=sharing) |
| DrumSolo | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.80_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.80_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.80_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.80_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/DrumSolo_1.80_HP.wav) |
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1h1AGHMz1z1rkg8bRV94lBq1h-7tPg2N2/view?usp=sharing) | [wav](https://drive.google.com/file/d/12KlsY0Et0MICm4F3aFPUqkWGPRsKG8W0/view?usp=sharing) | [wav](https://drive.google.com/file/d/1ZNWoYTr_ErXXcq2bFU3o2YuqhTelZ1Q7/view?usp=sharing) | [wav](https://drive.google.com/file/d/1AZMGWQ9GzqeQA-wIMCyfvDNW4ji-tZsR/view?usp=sharing) | [wav](https://drive.google.com/file/d/139lVGzUwyrSo9AcRp3kuDQABiHcnKcxn/view?usp=sharing) |
| Pop | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.80_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.80_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.80_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.80_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/Pop_1.80_HP.wav) |
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1vxFD5Cj6wS6_tj66DPMmFQfg2JLxgI3j/view?usp=sharing) | [wav](https://drive.google.com/file/d/1BiNkuTmBn_HJAbBLCim8BP3Q7qPAIUzT/view?usp=sharing) | [wav](https://drive.google.com/file/d/1f4dZc51EgIudt8MoCQDvwtbkoTk6svb9/view?usp=sharing) | [wav](https://drive.google.com/file/d/1aPs4ufHBxyahOgPAVj3CbDdEW4elRj85/view?usp=sharing) | [wav](https://drive.google.com/file/d/1mhwNUVUYK2lFIqR8o657uG7wb60b3IWZ/view?usp=sharing) |
| SingingVoice | TSM Toolbox | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_ORIG.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.80_OLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.80_WSOLA.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.80_PV.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.80_PVpl.wav) | [wav](https://www.audiolabs-erlangen.de/content/resources/MIR/TSMtoolbox/SingingVoice_1.80_HP.wav) |
| - | PyTSMod | - | [wav](https://drive.google.com/file/d/1HCJwXaHCnACFTCW-Q8lN40N4Oxr-jfmD/view?usp=sharing) | [wav](https://drive.google.com/file/d/1vZ54pQusHWRJs9fggpTOq02vGNTY5bI5/view?usp=sharing) | [wav](https://drive.google.com/file/d/1TP2ZoV028tqFrILhCZmnYvflY-YdM3Bd/view?usp=sharing) | [wav](https://drive.google.com/file/d/1EQotSRP2rma3i1XioJW0998HJLiq_jQV/view?usp=sharing) | [wav](https://drive.google.com/file/d/1npTbI0sjKOEUifSXQbAqluxGRtG0O4t7/view?usp=sharing) |

## References

[1] Jonathan Driedger, Meinard Müller. "TSM Toolbox: MATLAB Implementations of Time-Scale Modification Algorithms", *Proceedings of the 17th International Conference on Digital Audio Effects (DAFx-14).* 2014.

[2] Jonathan Driedger, Meinard Müller. "A review of time-scale modification of music signals", *Applied Sciences, 6(2), 57.* 2016.

[3] Udo Zölzer. "DAFX: digital audio effects", *John Wiley & Sons.* 2011.
