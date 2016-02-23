import Part1
import Part2
import HTML
import XML


#main program
def main():

    # part1:
    #-------------------------------------------------------------------
    Part1.Part1()
    #-------------------------------------------------------------------


    # part2:
    #-------------------------------------------------------------------
    # set last parameter to true to enable export of shots
    stitched_shots, all_shots, outstitched_shots = Part2.Part2(False)
    #-------------------------------------------------------------------


    #html stuff:
    #-------------------------------------------------------------------
    HTML.html_stuff(stitched_shots, all_shots, outstitched_shots, 'Oberstdorf16-shots.csv',
               './html_input/index_part1.txt', './html_input/index_part2.txt', './html_output/index.html')
    #-------------------------------------------------------------------


    #xml stuff:
    #-------------------------------------------------------------------
    XML.create_XML('caffe_output.txt')
    #-------------------------------------------------------------------


if __name__ == '__main__':
    main()
