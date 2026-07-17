from agents.transcription import transcribe_audio

# Replace this with any real .mp3 or .wav file on your machine
# Even a voice memo recorded on your phone works
AUDIO_FILE = "test_audio.mp3"

output = transcribe_audio(AUDIO_FILE)

print("\n--- Transcription Result ---")
print(f"Transcript : {output.text}")
print(f"Time taken : {output.duration_seconds}s")
print(f"Model used : {output.model_used}")