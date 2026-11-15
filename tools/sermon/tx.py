import sys, wave, numpy as np, time
from faster_whisper import WhisperModel
src, out, offset = sys.argv[1], sys.argv[2], float(sys.argv[3])
w = wave.open(src); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8', cpu_threads=4)
segs, info = m.transcribe(a, language=sys.argv[4] if len(sys.argv)>4 else None, beam_size=1, vad_filter=True,
    condition_on_previous_text=False)
print(info.language, info.language_probability, flush=True)
t0=time.time()
with open(out,'w') as f:
    for s in segs:
        t=s.start+offset
        line=f"[{int(t//3600)}:{int(t%3600//60):02d}:{int(t%60):02d}] {s.text.strip()}"
        f.write(line+'\n'); f.flush()
print('done', time.time()-t0)
