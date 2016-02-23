import numpy as np
import FileIO
from sklearn.svm import SVC
from sklearn.cross_validation import KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn import metrics
import cv2


SSI_FIRST = 1
SSI_CENTER = 2
SSI_LAST = 3


def svm_accuracy(mdh_compl):
    # mdh_compl = preprocessing.normalize(mdh_compl)
    labels = []

    #read ground truth for labels
    ground_truth_data = FileIO.read_shots_from_csv('GroundTruth.csv')
    for i in range(0, len(mdh_compl)):
        a,b,c = ground_truth_data[i]
        labels.append(c)

    #convert to numpy array
    labels = np.array(labels)

    #vars
    NF = 5
    ITERATIONS = 1000
    accuracy = 0.0

    for i in range(0,ITERATIONS):
        #set up training/test data
        # kf = KFold(len(mdh_compl), n_folds=NF, shuffle=True)
        kf = StratifiedKFold(labels, n_folds=NF, shuffle=True)         #unbalanced data (far more non-jump-offs)

        for train_idx, test_idx in kf:
            #get train and test sets
            X_train, X_test = mdh_compl[train_idx], mdh_compl[test_idx]
            y_train, y_test = labels[train_idx], labels[test_idx]

            #scale the data
            std_scaler = StandardScaler()
            X_train_scaled = std_scaler.fit_transform(X_train)
            X_test_scaled = std_scaler.transform(X_test)

            #configure svm
            svm = SVC(kernel='rbf', max_iter=1000, tol=1e-6)

            #train svm
            #opencv.svm.train() -> sklearn.svm.svc.fit()
            svm.fit(X_train_scaled, y_train)

            #let it predict
            predicted_labels = svm.predict(X_test_scaled)

            #calc accuracy
            accuracy += metrics.accuracy_score(y_test, predicted_labels)
            # print "accuracy: " + str(accuracy)
        # print "iteration: " + str(i)

    print "basic accuracy if all shots are predicted as 0 (no jump-off): " + \
          str(metrics.accuracy_score(y_test, [0 for yy in y_test.tolist()]))

    return accuracy, ITERATIONS, NF


def svm_use(mdh_training, mdh_test):
    labels = []

    #read ground truth for labels
    ground_truth_data = FileIO.read_shots_from_csv('GroundTruth.csv')
    for i in range(0, len(mdh_training)):
        a,b,c = ground_truth_data[i]
        labels.append(c)

    #convert to numpy array
    y_train = np.array(labels)

    #read and scale the data
    std_scaler = StandardScaler()
    X_train = std_scaler.fit_transform(mdh_training)
    X_test = std_scaler.transform(mdh_test)

    #configure svm
    svm = SVC(kernel='rbf', max_iter=1000, tol=1e-6)

    #train svm
    svm.fit(X_train, y_train)

    #let it predict
    predicted_labels = svm.predict(X_test)
    return predicted_labels


#output visualization of shots (start-frame, center-frame, end-frame)
def get_results(predicted_labels, filename, stitching):
    #read ground truth for shot boundaries
    ground_truth_data = FileIO.read_shots_from_csv(filename)
    all_shots = []
    for a,b in ground_truth_data:
        all_shots.append( (a,b) )

    not_jumpoff_scenes = [i for i,j in enumerate(predicted_labels) if j == 0]
    all_scenes = []
    stitched_shots = []
    outstitched_shots = []

    #get start- and end-frames
    shot_indices = [i for i,j in enumerate(predicted_labels) if j == 1]
    relevant_start_frames = {}
    relevant_end_frames = {}

    if not stitching:
        for i in shot_indices:
            stitched_shots.append([i])
    else:
        #stitches shots together to one long shot of each jump-off
        last_elem = shot_indices[0]
        scene = [last_elem]
        #check for consecutive jump-off shots
        for i in range(1,len(shot_indices)):
            elem = shot_indices[i]
            if (elem - last_elem) < 3:
                #scene running
                scene.append(elem)
                outstitched_shots.append(elem)
            else:
                #scene over
                all_scenes.append(scene)
                scene = [elem]
            last_elem = elem

        #get start- and end-frames of the stitched shots
        for scene in all_scenes:
            if len(scene) > 1:
                first_shot_idx = scene[0]
                last_shot_idx = scene[len(scene)-1]
                a,b = ground_truth_data[first_shot_idx]
                c,d = ground_truth_data[last_shot_idx]
                relevant_start_frames[a] = (a,d)
                relevant_end_frames[d] = (a,d)
                stitched_shots.append(scene)
            else:
                not_jumpoff_scenes.append(scene[0])

    # not_jumpoff_scenes.sort()
    #wrapping in list
    not_jumpoff_scenes2 = []
    for i in not_jumpoff_scenes:
        not_jumpoff_scenes2.append([i])

    # return stitched_shots, not_jumpoff_scenes2, outstitched_shots
    return stitched_shots, all_shots, outstitched_shots


#output images to folder ('./shot_images/all_shots/')
def save_shot_images(videoname, option, filename, caffe):
    if 1 <= option <= 3:
        #read ground truth for shot boundaries
        relevant_start_frames, relevant_end_frames = FileIO.read_shot_boundaries(filename)

        #read video
        cap = cv2.VideoCapture(videoname)
        ret, frame = cap.read()

        path = ''
        if caffe:
            path = './shot_images/'
        else:
            path = './html_output/shot_images/all_shots/'

        index = 1
        shot_center = 0
        first_frame = 0             # save first frame of center shot
        while cap.isOpened():
            #stop after last frame
            if frame is None:
                cap.release()
                break

            if not caffe:
                frame = cv2.resize(frame, (60,38))
            else:
                frame = cv2.resize(frame, (360,228))

            #output for start-frames
            if index in relevant_start_frames:
                if option == SSI_FIRST:
                    #output image of first frame
                    cv2.imwrite(path + str(index) + '.jpg', frame)
                if option == SSI_CENTER:
                    #calc center frames
                    data = relevant_start_frames[index]
                    a,b = data
                    shot_center = a + int((b-a)/2)
                    first_frame = a

            #output for center-frames
            if option == SSI_CENTER:
                if index == shot_center:
                    #output image of center-frame
                    cv2.imwrite(path + str(first_frame) + '.jpg', frame)

            if option == SSI_LAST:
                #output for end-frames
                if index in relevant_end_frames:
                    #output image of center-frame
                    cv2.imwrite(path + str(first_frame) + '.jpg', frame)

            ret, frame = cap.read()
            index += 1
