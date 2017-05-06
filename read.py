import cv2
import numpy as np
img_name = "E:\\test\\upload.jpg" ;
im = cv2.imread(img_name)
# cv2.waitKey()

# im_lowers = cv2.pyrDown(im)
# cv2.imshow('im_lowers' , im_lowers)

# s = cv2.SIFT()
# print im
s = cv2.SURF()
kp, des = s.detectAndCompute(im, None)

print len(kp)
print des.shape

hi = np.ones(des.shape[0])
des = np.column_stack((hi, des))
np.savetxt("E://in.txt", des)


# for k in kp:
#     # print k.pt[0] , k.pt[1]
#     cv2.circle(im, (int(k.pt[0]), int(k.pt[1])), 1, (0, 255, 0), -1)

im = cv2.drawKeypoints(im, kp, None, color=(0,255,0), flags=2)

cv2.GaussianBlur(im, (5, 5), 0)
cv2.imshow("SURF_features", im)
cv2.waitKey()
cv2.destroyAllWindows()





















