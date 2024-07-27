import os
import asyncio
import logging

log = logging.getLogger(__name__)

class Utilities:
    @staticmethod
    async def run_subprocess(cmd):
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
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
        output, error = await Utilities.run_subprocess(ffmpeg_cmd)
        log.debug(f"FFmpeg output: {output.decode().strip()}")
        log.debug(f"FFmpeg error: {error.decode().strip()}")
        
        if not os.path.exists(output_file):
            log.error(f"Failed to generate video. Output file not found: {output_file}")
            return None
        
        return output_file
