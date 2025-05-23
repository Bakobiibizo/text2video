from moviepy.video.io.VideoFileClip import VideoFileClip


def convert_mp4_to_gif(
    input_video_path="data/video.mp4",
    output_gif_path="data/output.gif",
    start_time=0,
    end_time=None,
    resize=(1024, 1024),
):
    # Load the video file
    clip = VideoFileClip(input_video_path)

    # If an end time is not specified, use the full duration of the clip
    if end_time is None:
        end_time = clip.duration

    # Trim the clip if start_time and/or end_time is specified
    trimmed_clip = clip.subclip(start_time, end_time)

    # Resize the clip if a new size is specified
    if resize:
        trimmed_clip = trimmed_clip.resize(newsize=resize)

    # Write the GIF file
    trimmed_clip.write_gif(output_gif_path, fps=10)


if __name__ == "__main__":
    convert_mp4_to_gif("data/897ce0e6-ed90-4ed3-a506-2057394b06cd.mp4")
