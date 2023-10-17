import cv2
import numpy as np

# Initialize the camera module
cap = cv2.VideoCapture(0)

# Set the resolution of the camera
cap.set(3, 640)
cap.set(4, 480)

# Define the region of interest (ROI) for lane detection
roi_vertices = [(0, 480), (320, 320), (320, 320), (640, 480)]

# Define the color range for white and yellow lanes
white_lower = np.array([0, 0, 200], dtype=np.uint8)
white_upper = np.array([180, 25, 255], dtype=np.uint8)
yellow_lower = np.array([20, 100, 100], dtype=np.uint8)
yellow_upper = np.array([30, 255, 255], dtype=np.uint8)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(frame, (5, 5), 0)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Create a mask for white and yellow lanes
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask = cv2.bitwise_or(white_mask, yellow_mask)

    # Apply the mask to the frame
    masked = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert the masked frame to grayscale
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Apply Hough transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=5)

    # Create a blank image to draw the lines on
    line_image = np.zeros_like(frame)

    # Draw the detected lines on the blank image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)

    # Apply ROI mask to the line image
    roi_mask = np.zeros_like(line_image)
    cv2.fillPoly(roi_mask, np.array([roi_vertices], dtype=np.int32), (255, 255, 255))
    roi_image = cv2.bitwise_and(line_image, roi_mask)

    # Combine the ROI image with the original frame
    result = cv2.addWeighted(frame, 0.8, roi_image, 1, 0)

    # Display the resulting frame
    cv2.imshow('Lane Detection', result)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
