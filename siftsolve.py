import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

class SiftSolve:

    def __init__(self):
        self.s = cv2.SIFT()
        self.maxSize = 384*384
        pass

    def get_feature(self, im):
        if isinstance(im, str):
            im = cv2.imread(im)
        kp, des = self.s.detectAndCompute(im, None)
        return kp, des

    def pre_solve(self, im):
        while True:
            sh = im.shape
            if sh[0] <= self.maxSize:
                break
            im = cv2.pyrDown(im)
        return im

    def plot_feature(self, args):
        img_path = args[0]
        im = cv2.imread(img_path)
        kp, des = self.get_feature(im)
        for k in kp:
            cv2.circle(im, (int(k.pt[0]), int(k.pt[1])), 1, (0, 255, 0))
        if len(args) == 2:
            plt.imsave(args[1], im)
        else:
            cv2.imshow("img_feature", im)
            cv2.waitKey()

    def save_feature(self, args):
        if len(args) < 2:
            print "args length is illegal"
        img_path = args[0]
        save_path = args[1]
        # ih = int(args[2])
        im = cv2.imread(img_path)
        kp, des = self.get_feature(im)
        # col = np.ones(des.shape[0])*ih
        # res = np.column_stack((col, des))
        np.savetxt(save_path, des)

    def draw_matches(self , im1, kp1, im2, kp2, macthes):
        row1 = im1.shape[0]
        col1 = im1.shape[1]
        row2 = im2.shape[0]
        col2 = im2.shape[1]
        out = np.zeros((max(row1, row2), col1+col2, 3), dtype='uint8')
        out[:row1, :col1, :3] = im1
        out[:row2, col1:] = im2
        for mat in macthes:
            im1_idx = mat.queryIdx
            im2_idx = mat.trainIdx
            (x1, y1) = kp1[im1_idx].pt
            (x2, y2) = kp2[im2_idx].pt
            cv2.circle(out, (int(x1), int(y1)), 4, (0, 255, 0), 1)
            cv2.circle(out, (int(x2)+col1, int(y2)), 4, (0, 255, 0), 1)
            cv2.line(out, (int(x1), int(y1)), (int(x2)+col1, int(y2)), (0, 255, 0), 1)
        return out

    def generate_good(self , match):
        good = []
        for m, n in match:
            if m.distance <= 0.9 * n.distance:  # todo
                good.append(m)
        return good

    def match(self, args):
        img_path1 = args[0]
        img_path2 = args[1]
        im1 = cv2.imread(img_path1)
        im1 = self.pre_solve(im1)
        im2 = cv2.imread(img_path2)
        im2 = self.pre_solve(im2)
        kp1, des1 = self.get_feature(im1)
        kp2, des2 = self.get_feature(im2)
        bf = cv2.BFMatcher()
        matches1 = bf.knnMatch(des1, des2, k=2)
        matches2 = bf.knnMatch(des2, des1, k=2)
        good1 = self.generate_good(matches1)
        good2 = self.generate_good(matches2)
        le = max(len(des1), len(des2))
        a = np.zeros([le, le])
        for g in good2:
            a[g.queryIdx][g.trainIdx] = 1
        good = []
        for g in good1:
            if a[g.trainIdx][g.queryIdx] == 1:
                good.append(g)
        return len(good), good

    def plot_match(self, args):
        img_path1 = args[0]
        img_path2 = args[1]
        im1 = cv2.imread(img_path1)
        im1 = self.pre_solve(im1)
        im2 = cv2.imread(img_path2)
        im2 = self.pre_solve(im2)
        kp1, des1 = self.get_feature(im1)
        kp2, des2 = self.get_feature(im2)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        for m, n in matches:
            if m.distance <= 0.8*n.distance: #todo
                good.append(m)
        im3 = self.draw_matches(im1, kp1, im2, kp2, good)
        if len(args) == 3:
            plt.imsave(args[2], im3)
        else:
            cv2.imshow("match", im3)
            cv2.waitKey() #todo
        return len(good)

    def get_hist(self , img):
        hist = []
        for i in range(3):
            hist.append(cv2.calcHist([img], [0], None, [256], [0, 256]))
        return hist

    def color_match(self, hist_1, hist_2):
        nums = []
        for i in range(3):
            num = np.sqrt(np.sum((hist_1[i] - hist_2[i]) ** 2))
            nums.append(num)
        su = np.sum(nums)
        print su
        return su < 20000

    def color_filter(self, img, loc, imgs):
        img_1 = cv2.imread(img, cv2.IMREAD_COLOR)
        hist_1 = self.get_hist(img_1)
        result = []
        for i in imgs:
            img_2 = cv2.imread(loc + "\\" + i, cv2.IMREAD_COLOR)
            hist_2 = self.get_hist(img_2)
            if self.color_match(hist_1, hist_2):
                result.append(i)
        return result

    def search(self, args):
        result = []
        if len(args) < 2:
            return result
        loc = args[0]
        image_path = args[1]
        dir_list = os.listdir(loc)
        dir_list = self.color_filter(image_path, loc, dir_list)
        nums = []
        for i in np.arange(len(dir_list)):
            num, good = self.match([image_path, loc + "\\" + dir_list[i]])
            # print num , dir_list[i]
            nums.append((num, dir_list[i]))
        nums = sorted(nums)
        a = range(min(len(nums), 8))
        for i in a:
            result.append(nums[len(nums)-1-i][1])
        print nums
        print result
        return result

    def plot_hist(self, args):
        img_path = args[0]
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        hist = self.get_hist(img)
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(histr, color=col)
        plt.xlim([0, 256])
        if len(args) == 2:
            plt.imsave(args[1])
        else:
            plt.show()

    """
    examples:
    1 E:\test\upload.jpg
    1 E:\test\upload.jpg E:\test\upload_feature.jpg
    2 E:\test\upload.jpg E:\test\upload_feature.txt
    3 E:\test\upload.jpg E:\test\upload1.jpg
    3 E:\test\upload.jpg E:\test\upload1.jpg E:\test\upload_upload1_match.jpg
    4 F:\images E:\test\upload.jpg
    """
    def main(self, args):
        op = int(args[0])
        if op == 1:
            self.plot_feature(args[1:])
        elif op == 2:
            self.save_feature(args[1:])
        elif op == 3:
            self.plot_match(args[1:])
        elif op == 4:
            return self.search(args[1:])
        elif op == 5:
            self.plot_hist(args[1:])
        else:
            print "option error"
        return []

if __name__ == '__main__':
    ss = SiftSolve()
    ss.main(sys.argv[1:])
    # img = "E:\\test\\upload.jpg"
    # loc = "F:\\images"
    # print ss.color_filter(img, loc, os.listdir(loc))








