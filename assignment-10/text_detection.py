import cv2
import easyocr

def read_video_capture(cap, output_path="output.mp4"):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Video complete")
            break

        frame_count += 1
        print(f"Processing frame {frame_count}...")

        result = reader.readtext(frame)

        for i, t in enumerate(result):
            # print(t)

            bbox, text, score = t
            if score > threshold:
                start_point = tuple(map(int, bbox[0]))
                end_point = tuple(map(int, bbox[2]))
                cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
                # cv2.putText(frame, text, start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        out.write(frame)

    out.release()
    print(f"Saved output to {output_path}")

    
if __name__ == "__main__":
    image_path = "book.mp4"
    capture = cv2.VideoCapture(image_path)

    if not capture.isOpened():
        print("Error reading source video")
        exit()

    reader = easyocr.Reader(['en'], gpu=True)
    threshold = 0.2

    read_video_capture(capture, "output_assignment.mp4")

    capture.release()