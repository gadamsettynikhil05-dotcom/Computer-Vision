import cv2
import numpy as np
from pathlib import Path
from datetime import datetime



def grayscale(img,photos_folder):
    height, width, channels = img.shape
    output = np.zeros((height, width), dtype=np.uint8)
    for row in range(height):

        for col in range(width):
            blue = img[row][col][0]
            green = img[row][col][1]
            red = img[row][col][2]
            gray = int(
                0.114 * blue +
                0.587 * green +
                0.299 * red
            )
            gray = max(0, min(255, gray))
            output[row][col] = gray
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    filename = "grayscale_" + timestamp + ".jpg"

    output_path = photos_folder / filename

    cv2.imwrite(str(output_path), output)

    print("Grayscale image saved successfully!")
    print(output_path)

    cv2.imshow("Original", img)
    cv2.imshow("Manual Grayscale", output)
def splitchannels(img,photos_folder):
    height, width, channels = img.shape

    blue_output = np.zeros((height, width, 3), dtype=np.uint8)
    green_output = np.zeros((height, width, 3), dtype=np.uint8)
    red_output = np.zeros((height, width, 3), dtype=np.uint8)

    for row in range(height):

        for col in range(width):
            blue = img[row][col][0]
            green = img[row][col][1]
            red = img[row][col][2]
            blue_output[row][col][0] = blue
            green_output[row][col][1] = green
            red_output[row][col][2] = red

    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    blue_path = photos_folder / f"blue_{timestamp}.jpg"
    green_path = photos_folder / f"green_{timestamp}.jpg"
    red_path = photos_folder / f"red_{timestamp}.jpg"

    cv2.imwrite(str(blue_path), blue_output)
    cv2.imwrite(str(green_path), green_output)
    cv2.imwrite(str(red_path), red_output)

    print("Images saved successfully!")

    cv2.imshow("Original", img)
    cv2.imshow("Blue Channel", blue_output)
    cv2.imshow("Green Channel", green_output)
    cv2.imshow("Red Channel", red_output)
def increase_red_blue_green_channels(img,photos_folder):
    height, width, channels = img.shape
    output = np.zeros((height, width, 3), dtype=np.uint8)
    increase = 50
    choice = int(input(
    """1. Increase Blue
    2. Increase Green
    3. Increase Red

    Enter your choice: """
    ))

    for row in range(height):

        for col in range(width):
            blue = img[row][col][0]
            green = img[row][col][1]
            red = img[row][col][2]
            if choice == 1:
                blue = min(255, blue + increase)
            elif choice == 2:
                green = min(255, green + increase)
            elif choice == 3:
                red = min(255, red + increase)
            else:
                pass
            output[row][col][0] = blue
            output[row][col][1] = green
            output[row][col][2] = red

    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    var="string"
    if(choice==1):
        var="blue_increased_"
    elif(choice==2):
        var="green_increased_"
    elif(choice==3):
        var="red_increased_"
    else:
        pass
    filename = var + timestamp + ".jpg"

    output_path = photos_folder / filename

    cv2.imwrite(str(output_path), output)

    print("Image saved successfully!")
    print(output_path)



    cv2.imshow("Original", img)
    cv2.imshow("Blue Increased", output)
def convolution(img,photos_folder):
    height, width = img.shape
    output = np.zeros((height, width), dtype=np.uint8)

    kernel = np.array([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ], dtype=np.float32)

    kernel_sum = np.sum(kernel)

 
    if kernel_sum == 0:
        kernel_sum = 1
    for row in range(1, height - 1):

        for col in range(1, width - 1):

            total = 0

            for k_row in range(3):

                for k_col in range(3):

                    image_row = row + k_row - 1
                    image_col = col + k_col - 1

                    pixel = img[image_row][image_col]

                    weight = kernel[k_row][k_col]

                    total += pixel * weight

            total = total / kernel_sum

            total = int(total)

            total = max(0, min(255, total))

            output[row][col] = total

    cv2.imwrite("filtered_image.png", output)
    cv2.imshow("Original", img)
    cv2.imshow("Filtered", output)
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    print(timestamp)
    filename = "filtered_" + timestamp + ".jpg"
    image_path = photos_folder / filename
    cv2.imwrite(str(image_path),output)




project_folder = Path(__file__).parent
string1=input("enter the foldername")
string2=input("enter the filename")
photos_folder = project_folder / string1
photos_folder.mkdir(exist_ok=True)
image_path = photos_folder / string2
img = cv2.imread(str(image_path))

if img is None:
    print("Error: Image not found.")
    exit()
choice=int(input("enter 1 for convolution , 2 for rgb increase , 3 for rgb split , 4 for gratscale"))
if(choice==1):
    convolution(img,photos_folder)
elif(choice==3):
    splitchannels(img,photos_folder)
elif(choice==2):
    increase_red_blue_green_channels(img,photos_folder)
elif(choice==4):
    grayscale(img,photos_folder)
cv2.waitKey(0)
cv2.destroyAllWindows()



