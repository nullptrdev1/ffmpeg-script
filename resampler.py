from pathlib import Path
import subprocess
import sys
import time

AUDIO_EXTENSIONS = {".flac"}

folder_path = input("Masukkan path folder: ").strip()
folder = Path(folder_path)

if not folder.exists():
    print("Folder tidak ditemukan.")
    sys.exit()

audio_files = sorted([
    f for f in folder.iterdir()
    if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
])

if not audio_files:
    print("Tidak ada file FLAC ditemukan.")
    sys.exit()

print("\nFile yang ditemukan:")
for i, file in enumerate(audio_files, start=1):
    print(f"{i}. {file.name}")

print(f"\nTotal: {len(audio_files)} file")

confirm = input("\nLanjut downsampling? (y/n): ").strip().lower()

if confirm != "y":
    print("Dibatalkan.")
    sys.exit()

print()

for index, file in enumerate(audio_files, start=1):
    output_file = file.parent / f"downsampled {file.name}"

    print(f"[{index}/{len(audio_files)}] Memproses:")
    print(f"    {file.name}")

    cmd = [
        "ffmpeg",
        "-i", str(file),
        "-map", "0",
        "-map_metadata", "0",
        "-c:v", "copy",
        "-af", "aresample=resampler=soxr:precision=33",
        "-sample_fmt", "s32",
        "-ar", "48000",
        "-c:a", "flac",
        "-compression_level", "8",
        str(output_file)
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        print("    ✓ Sukses")
    else:
        print("    ✗ Gagal")

    if index < len(audio_files):
        time.sleep(1)

print("\nSemua proses selesai.")