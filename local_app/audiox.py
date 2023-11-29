# Python 3.5
# pip install pydub
# copy "ffmpeg.exe", "ffplay.exe" and "ffprobe.exe" into this directory
# Erwartet das Verzeichnis "anonym" und "anonym_a" sowie die Verzeichnisse mit den Audiodateien.
# Die vorhandenen Audiodateien werden überschrieben!!!

import time
from datetime import timedelta
from pydub import AudioSegment

startTimer = time.perf_counter()
print('Audio X - Start', '\n')

import os

paths = ['anonym', 'anonym_a']

csvFiles = []

for path in paths:
  for file in sorted(os.listdir(path), reverse=True):
    fullFile = os.path.join(path, file)
    if os.path.isfile(fullFile):
      new = True
      nFileTime = '_'.join(fullFile.split('_')[-2:])
      nFileBaseName = fullFile[:-len(nFileTime)]
      for csvFile in csvFiles:
        aFileTime = '_'.join(csvFile.split('_')[-2:])
        aFileBaseName = csvFile[:-len(aFileTime)]
        if aFileBaseName == nFileBaseName:
          new = False
      if new:
        csvFiles.append(fullFile)
      print(fullFile, new)

print('Audio X - Aktuelle Dateien ermittelt ...', time.perf_counter() - startTimer, '\n')
startTimer = time.perf_counter()

csvDg = 1
for csvFile in csvFiles:
  startTimerFile = time.perf_counter()
  fp = open(csvFile, 'r')
  csv = fp.readlines()
  fp.close()
  dg = 0
  times = []
  for lineTxt in csv:
    if dg > 1:
      line = lineTxt.split(';')
      beep = line[1].split(':')
      sync = line[2].split(':')
      start = line[3].split(':')
      end = line[4].split(':')
      beep = timedelta(hours=int(beep[0]), minutes=int(beep[1]), seconds=float(beep[2]))
      sync = timedelta(hours=int(sync[0]), minutes=int(sync[1]), seconds=float(sync[2]))
      start = timedelta(hours=int(start[0]), minutes=int(start[1]), seconds=float(start[2]))
      end = timedelta(hours=int(end[0]), minutes=int(end[1]), seconds=float(end[2]))
      diff = beep - sync
      times.append([start - diff, end - diff])
      # print(line[3], times)
    dg += 1
  print('-', csvFile, len(times))
  startTimerSub = time.perf_counter()
  aAudioFile = csv[0].split(';')[0].replace("/", "\\").strip()
  if aAudioFile[0] == "\\":
    aAudioFile = aAudioFile[1:]
  aAudio = AudioSegment.from_ogg(aAudioFile)
  print(' ', csvFile, 'Audiodatei geladen:', aAudioFile, time.perf_counter() - startTimerSub)
  startTimerSub = time.perf_counter()
  newAudioFile = AudioSegment.empty()
  aTime = 0
  invert = True if csv[1].split(';')[0].strip() == 'ErhInfAufgabeId' else False
  if invert:
    for eTime in times:
      newAudioFile += AudioSegment.silent(duration=int(eTime[0].total_seconds() * 1000) - aTime)
      newAudioFile += aAudio[int(eTime[0].total_seconds() * 1000):int(eTime[1].total_seconds() * 1000)]
      aTime = int(eTime[1].total_seconds() * 1000)
    newAudioFile += AudioSegment.silent(duration=len(aAudio) - aTime)
  else:
    for eTime in times:
      newAudioFile += aAudio[aTime:int(eTime[0].total_seconds() * 1000)]
      newAudioFile += AudioSegment.silent(duration=int((eTime[1] - eTime[0]).total_seconds() * 1000))
      aTime = int(eTime[1].total_seconds() * 1000)
    newAudioFile += aAudio[aTime:]
  print(' ', csvFile, 'Audiodatei zensiert ... Invert:', invert, time.perf_counter() - startTimerSub)
  startTimerSub = time.perf_counter()
  # newAudioFile.export('.'.join(aAudioFile.split('.')[:-1]) + '_new.ogg', format="ogg")
  newAudioFile.export(aAudioFile, format="ogg")
  print(' ', csvFile, 'Audiodatei gespeichert', time.perf_counter() - startTimerSub)
  print(' ', csvFile, 'Fertig ...', '(' + str(csvDg) + '/' + str(len(csvFiles)) + ')', time.perf_counter() - startTimerFile)
  csvDg += 1

print('Audio X - Audiodateien verarbeitet ...', time.perf_counter() - startTimer, '\n')
startTimer = time.perf_counter()
