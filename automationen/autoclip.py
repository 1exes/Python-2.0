
from gtts import gTTS
from moviepy.editor import VideoFileClip, concatenate_audioclips, TextClip, CompositeVideoClip

# Funktion zum Generieren von Sprachaudio mit gTTS
def generate_speech(text, filename):
    tts = gTTS(text=text, lang='de', slow=False)
    tts.save(filename)

# Funktion zum Erstellen des Videos
def create_video(content, video_file, outfile):
    text_clips = []
    audio_clips = []
    
    for idx, line in enumerate(content.split('\n')):
        audio_filename = f"temp_assets/audio_{idx}.mp3"
        generate_speech(line.strip(), audio_filename)
        audio_clips.append(VideoFileClip(audio_filename))
        
        text_clip = TextClip(line.strip(), fontsize=70, color='white').set_duration(5)
        text_clips.append(text_clip)
    
    final_audio = concatenate_audioclips(audio_clips)
    final_text = concatenate_audioclips(text_clips).set_pos(('center', 'center'))
    
    video = VideoFileClip(video_file).set_audio(final_audio)
    final_video = video.set_duration(final_audio.duration).overlay(final_text.set_duration(final_audio.duration))
    
    final_video.write_videofile(outfile, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
    video_file = "background_video.mp4"  # Ihr Video-Dateiname hier
    outfile = "final_video.mp4"  # Der Ausgabedateiname hier
    
    content = """
    Es war einmal ein mutiger Ritter, der ein großes Drachenproblem hatte.
    Er entschied sich, den gefährlichen Drachen zu bekämpfen und das Königreich zu retten.
    Nach einem epischen Kampf konnte der Ritter den Drachen besiegen und wurde zum Helden.
    """
    
    create_video(content, video_file, outfile)
