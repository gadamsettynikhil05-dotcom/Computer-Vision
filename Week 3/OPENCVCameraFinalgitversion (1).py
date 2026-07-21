import cv2
from pathlib import Path
from datetime import datetime

project_folder = Path(__file__).parent
photos_folder = project_folder / "photos"
photos_folder.mkdir(exist_ok=True)
largest=0
for item in photos_folder.iterdir():
    if item.is_file():
        largest+=1



cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Could not capture frame.")
        break
    cv2.imshow("Laptop Camera", frame)
    key = cv2.waitKey(1)

        # Press SPACE to capture
    if key == 32:
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        print(timestamp)
        filename = "photo_" + timestamp + ".jpg"
        image_path = photos_folder / filename
        cv2.imwrite(str(image_path), frame)

        print("Image saved!")
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
