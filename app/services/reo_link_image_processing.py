import os
import cv2

class Reo_Link_Image_Processing():
    def extract_key_frames(self, video_path, base_save_dir="frames"):
        """
        Extracts 5 evenly spaced frames from the given video and stores them
        in a dedicated subfolder named after the video (e.g., footage_3_frames).
        """
        # Extract footage name (e.g., "footage_3") from filename
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        save_dir = os.path.join(base_save_dir, f"{video_name}_frames")
        os.makedirs(save_dir, exist_ok=True)

        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Total frames in video: {total_frames}")

        # Calculate 5 target frames: ~10%, 30%, 50%, 70%, 90%
        fractions = [0.1, 0.3, 0.5, 0.7, 0.9]
        target_indices = [int(total_frames * f) for f in fractions]

        saved_frames = []

        for i, frame_index in enumerate(target_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = cap.read()
            if ret:
                filename = os.path.join(save_dir, f"frame_{i+1}.jpg")
                cv2.imwrite(filename, frame)
                saved_frames.append(filename)
                print(f"Saved frame {i+1} at index {frame_index}: {filename}")
            else:
                print(f"Failed to read frame at index {frame_index}")

        cap.release()
        return saved_frames