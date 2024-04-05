import os
import random
from typing import List, Tuple
import imageio
imageio.plugins.ffmpeg.download()
imageio.plugins.ffmpeg.load_lib()
imageio.plugins.ffmpeg.get_exe()
imageio.plugins.ffmpeg.get_ffmpeg_version()

from gtts import gTTS
from moviepy.editor import (
    AudioFileClip, 
    TextClip,
    concatenate_audioclips
)
from rich.console import Console
from rich.progress import track
import pyfiglet

def generate_speech(
        text: str = 'test du hhund',
        lang: str = 'en', 
        filename: str = 'audio.mp3'):
    myobj = gTTS(text=text, lang=lang, slow=False, tld='ca')
    myobj.save(filename)
    return filename

def clip(
        content: str, 
        video_file: str, 
        outfile: str, 
        image_file: str = '', 
        offset: int = 0, 
        duration: int = 0):
    
    def split_text(text: str, delimiter: str = '\n'):
        return text.split(delimiter)
    
    def generate_audio_text(fulltext: List[str]):
        audio_comp = []
        text_comp = []

        for idx, text in track(enumerate(fulltext), description='Synthesizing Audio...'):
            if text == "":
                continue
                
            generated_file = f"temp_assets/audio_{idx}.mp3"
            generate_speech(text.strip(), filename=generated_file)
            
            if os.path.exists(generated_file):
                print(f"Generated audio file {generated_file} exists.")
            else:
                print(f"Generated audio file {generated_file} does not exist.")
                continue

            audio_duration = AudioFileClip(os.path.abspath(generated_file)).duration

            text_clip = TextClip(
                text,
                font='Helvetica',
                fontsize=32,
                color="white",
                align='center',
                method='caption',
                size=(660, None)
            )
            text_clip = text_clip.set_duration(audio_duration)

            audio_comp.append(generated_file)
            text_comp.append(text_clip)

        return audio_comp, text_comp
    
    audio_comp, text_comp = generate_audio_text(split_text(content))

    audio_comp_list = []
    for audio_file in track(audio_comp, description='Stitching Audio...'):
        audio_comp_list.append(AudioFileClip(audio_file))
    audio_comp_stitch = concatenate_audioclips(audio_comp_list)
    audio_comp_stitch.write_audiofile('temp_audio.mp3', fps=44100)

    audio_duration = audio_comp_stitch.duration
    if duration == 0:
        duration = audio_duration

    audio_comp_stitch.close()

    vid_clip = VideoFileClip(video_file).subclip(offset, offset + duration)
    vid_clip = vid_clip.resize((1980, 1280))
    vid_clip = vid_clip.crop(x_center=1980 / 2, y_center=1280 / 2, width=720, height=1280)

    if image_file != '':
        image_clip = ImageClip(image_file).set_duration(duration).set_position(("center", 'center')).resize(0.8)
        vid_clip = CompositeVideoClip([vid_clip, image_clip])

    vid_clip = CompositeVideoClip([vid_clip, concatenate_videoclips(text_comp).set_position(('center', 860))])

    vid_clip = vid_clip.set_audio(AudioFileClip('temp_audio.mp3').subclip(0, duration))
    vid_clip.write_videofile(outfile, audio_codec='aac')
    vid_clip.close()

if __name__ == '__main__':

    console = Console()
    banner = pyfiglet.figlet_format(text='AutoClip', font='rectangles')
    console.print()
    console.print("[bold][red1]" + banner)
    console.print("[dark_red] By Abhishta (github.com/abhishtagatya)")

    if not os.path.exists("temp_assets"):
        os.mkdir("temp_assets")

    video_background_file = "your_video.mp4"  # Pfad zu Ihrer Hintergrundvideodatei
    video_background_offset = random.randint(0, 5000)
    image_banner_file = "your_banner.png"  # Pfad zu Ihrer Bannerbilddatei
    output_file = "AutoClip_Out.mp4"

    content = """Ihr Text hier\nund hier\nund hier\n"""

    console.print("\n\n[light_green] Task Starting\n\n")
    clip(content=content, 
         video_file=video_background_file, 
         image_file=image_banner_file,
         outfile=output_file, 
         offset=video_background_offset)

    console.print("\n\n[light_green] Completed!")
