import os
import shutil
from pathlib import Path
import subprocess
import json

import ffmpeg


def ffmpeg_noconsole(ffmpeg_command):
    subprocess.call(ffmpeg_command, shell=True)


def ffmpeg_probe(video_input_path):
    command = ['ffprobe', '-show_format', '-show_streams', '-of', 'json']
    command += [video_input_path]

    process = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    if process.returncode != 0:
        raise Exception(f"ffprobe error: {err}")

    return json.loads(out.decode('utf-8'))


def transfer_loop(
    src,
    dst,
    do_convert,
    copy_embed_cover,
    status,
    progress_bar,
    root_window,
    excluded,
    callback_func,
):

    progress_bar.after(0, progress_bar.config, {"mode": "indeterminate"})
    status.after(0, status.config, {"text": "Estimating number of files..."})
    progress_bar.after(0, progress_bar.start)

    library = list(os.walk(src))

    total_files = sum(len(files) for r, d, files in library)
    progress_bar.after(0, progress_bar.stop)
    progress_bar.after(
        0, progress_bar.config, {"mode": "determinate", "maximum": total_files}
    )

    current_file = 0
    files_transferred = 0
    files_skipped = 0

    print(excluded)

    # copy tree
    src_prefix = len(src) + len(os.path.sep)

    for rootdir, dirs, files in library:
        for f in files:
            # Check for excluded files/dirs
            srcpath = os.path.join(rootdir, f)
            print(srcpath)
            found = False
            for x in excluded:
                if x == '':
                    continue
                x_len = len(x)
                print(f'{x.lower()} !! {srcpath.lower()[:x_len]}')
                if x.lower() == srcpath.lower()[:x_len]:
                    found = True
                    break
            if found == True:
                files_skipped += 1
                continue

            # Check if its an image, then convert
            # Images are always converted to BMP for compatibility with Rockbox
            if f.lower().endswith(
                (
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".webp",
                    ".bmp",
                    ".tiff",
                    ".gif",
                )
            ):
                ndst = str(
                    Path(os.path.join(dst, rootdir[src_prefix:], f)).with_suffix(
                        ".bmp")
                )
                if not os.path.isfile(ndst):
                    ffmpeg_noconsole(ffmpeg.input(os.path.join(rootdir, f)).output(
                        ndst, update="true", vframes=1, vf="scale=500:500"
                    ).compile())
                    files_transferred += 1

            elif f.lower().endswith(
                (
                    ".3gp",
                    ".aac",
                    ".adts",
                    ".m4a",
                    ".mp4",
                    ".caf",
                    ".aiff",
                    ".aif",
                    ".wsd",
                    ".dsf",
                    ".flac",
                    ".mp3",
                    ".ogg",
                    ".oga",
                    ".spx",
                    ".wav",
                    ".wave",
                )
            ):
                # supported audio files
                if not do_convert:
                    # Copy files, no conversion to MP3
                    ndst = os.path.join(dst, rootdir[src_prefix:], f)
                    if not os.path.isfile(ndst):
                        shutil.copy2(os.path.join(rootdir, f), ndst)
                        files_transferred += 1
                    else:
                        files_skipped += 1
                else:
                    # Convert files to MP3
                    ndst = str(
                        Path(os.path.join(dst, rootdir[src_prefix:], f)).with_suffix(
                            ".mp3"
                        )
                    )
                    if not os.path.isfile(ndst):
                        output_bitrate = 320000
                        input_probe = ffmpeg_probe(os.path.join(rootdir, f))
                        if "bit_rate" in input_probe["format"]:
                            output_bitrate = min(output_bitrate, int(
                                input_probe["format"]["bit_rate"]))
                        if copy_embed_cover:
                            ffmpeg_noconsole(ffmpeg.input(os.path.join(rootdir, f)).output(
                                ndst,
                                ab=output_bitrate,
                                ac=2,
                                ar=48000,
                                map_metadata=0,
                                id3v2_version=3,
                                write_id3v1=1,
                                vcodec="copy"
                            ).compile())
                        else:
                            ffmpeg_noconsole(ffmpeg.input(os.path.join(rootdir, f)).audio.output(
                                ndst,
                                ab=output_bitrate,
                                ac=2,
                                ar=48000,
                                map_metadata=0,
                                id3v2_version=3,
                                write_id3v1=1
                            ).compile())
                        files_transferred += 1
                    else:
                        files_skipped += 1
            else:
                files_skipped += 1

            current_file += 1

            progress_bar.after(0, progress_bar.config, {"value": current_file})
            root_window.after(0, root_window.update_idletasks)

            status.after(
                0,
                status.config,
                {"text": f"Checking and copying file {current_file}/{total_files}"},
            )

        # Create subdirectories if they dont exist
        for dirname in dirs:
            srcpath = os.path.join(rootdir, dirname)
            # Check for excluded files/dirs
            found = False
            for x in excluded:
                if x == '':
                    continue
                x_len = len(x)
                if x.lower() == srcpath.lower()[:x_len]:
                    found = True
                    break
            if found == True:
                continue

            dirpath = os.path.join(dst, rootdir[src_prefix:], dirname)
            try:
                os.mkdir(dirpath)
            except FileExistsError:
                pass

    callback_func(files_transferred, files_skipped)
