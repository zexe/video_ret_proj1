import FileIO
import SVM
import OptFlow_MotDirHist as OM


def Part1():
    # values = [100, 200, 500, 1000]
    values = [100]

    for v in values:
        print "Points: " + str(v)

        #optical flow and motion direction histogram calculation
        # mdh_all = OM.createMotionDirectionHistograms('GroundTruth.csv', 'videos/oberstdorf08small.mp4', v, False, False)
        # FileIO.save_histograms_to_file('mdh_8_' + str(v) + '.csv', mdh_all)
        # print "Histograms created."

        # #svm training and predicting
        mdh_compl = FileIO.read_histograms_from_file('mdh_8_' + str(v) + '.csv')
        accuracy, ITERATIONS, NF = SVM.svm_accuracy(mdh_compl)
        print "average accuracy: " + str(accuracy/ITERATIONS/NF)