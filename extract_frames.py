
import cv2
import os
import argparse


def extract_frames(video_path, output_dir, time_start, time_end):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    if time_start < 0 or time_end < time_start:
        raise ValueError("Invalid timestamp range.")

    if time_start > duration or time_end > duration:
        raise ValueError(
            f"Timestamp exceeds video duration ({duration:.2f}s)."
        )

    start_frame = int(time_start * fps)
    end_frame = min(int(time_end * fps), total_frames - 1)

    print(f"Video duration: {duration:.2f}s")
    print(f"FPS: {fps}")
    print(f"Extracting frames: {start_frame} - {end_frame}")

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    extracted = 0

    for frame_number in range(start_frame, end_frame + 1):
        ret, frame = cap.read()

        if not ret:
            break

        timestamp = frame_number / fps

        filename = os.path.join(
            output_dir,
            f"frame_{frame_number:08d}_{timestamp:.3f}s.jpg"
        )

        cv2.imwrite(filename, frame)
        extracted += 1

    cap.release()

    print(f"\nExtraction completed!")
    print(f"Total frames extracted: {extracted}")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract all frames from an MP4 video within a time range."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input MP4 video path"
    )

    parser.add_argument(
        "--output",
        default="extracted_frames",
        help="Output directory (default: extracted_frames)"
    )

    parser.add_argument(
        "--timestart",
        type=float,
        required=True,
        help="Start timestamp in seconds"
    )

    parser.add_argument(
        "--timeend",
        type=float,
        required=True,
        help="End timestamp in seconds"
    )

    args = parser.parse_args()

    extract_frames(
        video_path=args.input,
        output_dir=args.output,
        time_start=args.timestart,
        time_end=args.timeend
    )

