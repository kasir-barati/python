from celery import shared_task
import ffmpeg_streaming
from ffmpeg_streaming import Formats


@shared_task
def celery_generate_mpd(
        original_video_abs_path: str,
        mpd_file_abs_path: str,) -> None:
    video = ffmpeg_streaming.input(original_video_abs_path)
    dash = video.dash(Formats.h264())
    dash.auto_generate_representations([1080, 720, 360])
    dash.output(mpd_file_abs_path)

