import os
import asyncio
import logging

log = logging.getLogger(__name__)

class Utilities:
    @staticmethod
    async def run_subprocess(cmd):
        log.debug(f"Running command: {' '.join(cmd)}")
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        log.debug(f"Command output: {stdout.decode()}")
        log.debug(f"Command error: {stderr.decode()}")
        return stdout, stderr

    @staticmethod
    async def generate_sample_video(file_path, output_folder, duration):
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "sample.mp4")
        ffmpeg_cmd = [
            "ffmpeg",
            "-ss",
            "0",
            "-i",
            file_path,
            "-t",
            str(duration),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-strict",
            "experimental",
            "-y",
            output_file,
        ]
        log.info(f"Generating sample video from {file_path} with duration {duration} seconds.")
        output, error = await Utilities.run_subprocess(ffmpeg_cmd)
        if not os.path.exists(output_file):
            log.error(f"Sample video was not created. Check FFmpeg command and input file.")
            return None
        log.info(f"Sample video created successfully: {output_file}")
        return output_file
