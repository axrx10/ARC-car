import cv2
import numpy as np

def initialize_camera():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    return cap

def apply_roi_mask(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def detect_lanes(frame):
    # Apply Gaussian blur and convert to HSV
    blur = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    # Create masks for white and yellow
    white_lower, white_upper = np.array([0, 0, 200]), np.array([180, 25, 255])
    yellow_lower, yellow_upper = np.array([20, 100, 100]), np.array([30, 255, 255])
    
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # Defining ROI and applying it
    roi_vertices = [(0, 480), (0, 320), (640, 320), (640, 480)]
    roi_edges = apply_roi_mask(edges, [np.array(roi_vertices, dtype=np.int32)])
    
    lines = cv2.HoughLinesP(roi_edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=5)
    return lines

def main():
    cap = initialize_camera()
    while True:
        ret, frame = cap.read()
        lines = detect_lanes(frame)
        
        # Draw lines
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)
        else:
            print("No lanes detected.")
        
        # Combine line image with original frame
        result = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
        
        cv2.imshow('Lane Detection', result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
