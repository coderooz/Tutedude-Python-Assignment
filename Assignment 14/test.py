import cv2
img = cv2.imread('images/sample_1.png')
cv2.imshow('My Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()