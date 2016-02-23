import FileIO
import SVM
import OptFlow_MotDirHist as OM


def Part2(createData):
    # optical flow and motion direction histogram calculation
    v = 100

    # mdh_all = OM.createMotionDirectionHistograms('Oberstdorf16-shots.csv', 'videos/oberstdorf16.mp4', v, False, True)
    # FileIO.save_histograms_to_file('mdh_16_' + str(v) + '.csv', mdh_all)

    if createData:
        SVM.save_shot_images('videos/oberstdorf16.mp4', SVM.SSI_CENTER, 'Oberstdorf16-shots.csv', False)

    #svm training and predicting
    mdh_training = FileIO.read_histograms_from_file('mdh_8_' + str(v) + '.csv')
    mdh_test = FileIO.read_histograms_from_file('mdh_16_' + str(v) + '.csv')
    predicted_labels = SVM.svm_use(mdh_training, mdh_test)

    stitched_shots, all_shots, outstitched_shots = SVM.get_results(
        predicted_labels, 'Oberstdorf16-shots.csv', True)


    return stitched_shots, all_shots, outstitched_shots
