import os
import shutil
from pathlib import Path

import ffmpeg


def transfer_loop(
    src,
    dst,
    do_convert,
    copy_embed_cover,
    status,
    progress_bar,
    root_window,
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

    # copy tree
    src_prefix = len(src) + len(os.path.sep)

    for rootdir, dirs, files in library:
        for f in files:
            progress_bar.after(0, progress_bar.config, {"value": current_file})
            root_window.after(0, root_window.update_idletasks)

            status.after(
                0,
                status.config,
                {"text": f"Checking and copying file {current_file}/{total_files}"},
            )

            # Check if its and image, then convert
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
                    Path(os.path.join(dst, rootdir[src_prefix:], f)).with_suffix(".bmp")
                )
                if not os.path.isfile(ndst):
                    ffmpeg.input(os.path.join(rootdir, f)).output(
                        ndst, update="true", vframes=1, vf="scale=500:500"
                    ).run(quiet=True)
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
                        if copy_embed_cover:
                            ffmpeg.input(os.path.join(rootdir, f)).output(
                                ndst,
                                ab=output_bitrate,
                                ac=2,
                                ar=48000,
                                map_metadata=0,
                                id3v2_version=3,
                                write_id3v1=1,
                                vcodec="copy"
                            ).run(quiet=True)
                        else:
                            ffmpeg.input(os.path.join(rootdir, f)).audio.output(
                                ndst,
                                ab=output_bitrate,
                                ac=2,
                                ar=48000,
                                map_metadata=0,
                                id3v2_version=3,
                                write_id3v1=1
                            ).run(quiet=True)
                        files_transferred += 1
                        print(type(ffmpeg.probe(ndst)))
                    else:
                        files_skipped += 1
            else:
                files_skipped += 1

            current_file += 1

        # Create subdirectories if they dont exist
        for dirname in dirs:
            dirpath = os.path.join(dst, rootdir[src_prefix:], dirname)
            try:
                os.mkdir(dirpath)
            except FileExistsError:
                pass

    callback_func(files_transferred, files_skipped)
