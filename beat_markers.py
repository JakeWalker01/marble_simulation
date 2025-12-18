
import librosa
import matplotlib.pyplot as plt

#loading audio file
audio_path = "cartoon.wav"
waveform, sample_rate = librosa.load(audio_path)

#show where onset happens
onset_frames = librosa.onset.onset_detect(y=waveform, sr=sample_rate)

onset_times = librosa.frames_to_time(onset_frames, sr=sample_rate)

print(onset_frames[0:10])