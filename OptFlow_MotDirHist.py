import math
import numpy as np
import cv2
import FileIO


def dense_sampling(n, height, width):
    #get number of rows and columns
    ratio = 1
    if height != 0:
        ratio = width/height
    z = math.sqrt(n/ratio)
    number_of_rows = int(z)
    number_of_cols = int(ratio * z)

    #get step size between points
    points = []
    x_step = width / (number_of_cols+1)
    y_step = height / (number_of_rows+1)

    #create array with x and y values for points
    for i in range(1,number_of_rows+1):
        y = int(i*y_step)
        for j in range(1,number_of_cols+1):
            x = int(j*x_step)
            a = np.array([x, y], dtype='float32')
            b = np.array([a], dtype='float32')
            points.append(b)

    points = np.array(points)
    return points


#calculates the optical flow and histograms for the first part
def createMotionDirectionHistograms(filename, videoname, v, show_video, flip_video):
    #read video
    cap = cv2.VideoCapture(videoname)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    #read ground truth for shot boundaries
    ground_truth_start, ground_truth_end = FileIO.read_shot_boundaries(filename)

    points0 = 0         #old features
    points1 = 0         #new features

    mdh_all = []        #list of motion direction histogram for all shots
    mdh = []
    n = v

    points_original = dense_sampling(n, height, width)
    ret, frame = cap.read()
    #flip video for 16 oberstdorf
    if flip_video:
        frame = cv2.flip(frame, 1)

    index = 1
    while cap.isOpened():

        ret, frame = cap.read()
        if flip_video:
            frame = cv2.flip(frame, 1)

        #stop after last frame
        if frame is None:
            cap.release()
            break

        #init on shot start
        if index in ground_truth_start:
            #get starting points
            old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # points0 = cv2.goodFeaturesToTrack(old_gray, n, 0.01, 1)
            points0 = points_original.copy()

            #init motion direction histogram
            mdh = [0] * 13
        else:
            #cvt to gray
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #calc optical flow between two frames
            points1, status, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, points0, None)

            #get good points (points that are in both frames)
            points0_good = points0[status == 1]
            points1_good = points1[status == 1]

            #do the calculations
            #---------------

            #draw all motion vectors
            if show_video:
                for i in range(0, len(points1_good)):
                    #draw
                    pt1 = (int(points0_good[i][0]), int(points0_good[i][1]))
                    pt2 = (int(points1_good[i][0]), int(points1_good[i][1]))
                    cv2.line(frame, pt1, pt2, (0,0,255))

                # show frame
                cv2.imshow("Video", frame)
                #exit or pause
                key = cv2.waitKey(10) & 0xFF
                if key == ord('q'):
                    break
                if key == ord(' '):
                    cv2.waitKey(0)

            #calc bins
            #calc differences of points
            sub = np.subtract(points0_good, points1_good)
            for i in range(0, len(sub)):
                p = sub[i]
                #if the point doesn't move, it's in bin #0
                if (int(p[0]) == 0) and (int(p[1]) == 0):
                    mdh[0] += 1
                #else calc the angle and add to bin
                else:
                    angle = 180-math.degrees(np.arctan2(p[1], p[0]))      #first y, then x
                    bin_index = int((angle/30)) + 1
                    mdh[bin_index] += 1

            #reset on a new shot
            if index in ground_truth_end:
                #normalize so every histogram has ~n values
                temp = float(sum(mdh)) / n
                if int(temp) == 0:
                    temp = 1
                mdh_new = [x/temp for x in mdh]
                mdh_all.append(mdh_new[:])                          #append a copy of the vector

            #----------------

            #get points of current frame for next frame
            # points1 = cv2.goodFeaturesToTrack(frame_gray, n, 0.01, 1)
            points1 = points_original.copy()
            #if i don't reset the points, 'bad' points propagate through the frames
            #and less and less points in a shot are good

            #new -> old
            points0 = points1.copy()
            old_gray = frame_gray.copy()

        # print index
        index += 1

    return mdh_all