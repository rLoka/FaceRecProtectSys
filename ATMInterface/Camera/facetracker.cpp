/*
Dio izvornog koda preuzet sa:
https://github.com/opencv/opencv/blob/master/samples/cpp/dbt_face_detection.cpp
http://stackoverflow.com/questions/143174/how-do-i-get-the-directory-that-a-program-is-running-from
http://stackoverflow.com/questions/7352099/stdstring-to-char
*/

/*
 * EyeDetection
 * http://funvision.blogspot.hr/2015/12/basic-opencv-3-mat-tutorial-part-2-roi.html
 * http://sanyamgarg.blogspot.hr/2016/03/a-blink-detection-technique-using.html
 * */

/*
Verzija: 1.1
Opis: Program za detekciju i komunikaciju sa Arduino mikrokontrolerom
Autor: Karlo Grlić
Datum: 08.2015.
*/

#include <opencv2/imgproc.hpp>
#include <opencv2/video.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/features2d.hpp>
#include <opencv2/objdetect.hpp>
#include "cArduino.h"
#include <fstream>
#include <iostream>
#include <ctime>
#include <string>
#include <limits.h>
#include <unistd.h>

using namespace std;
using namespace cv;

cArduino arduino(ArduinoBaundRate::B9600bps, "/dev/ttyUSB0");
const bool shallCloseWhenDone = false;

//Definiranje izvora videa
//0 - ugrađena kamera, 1, 2, 3 ... ostale video kamere, "home/karlo/.../video.avi" putanja videa
const int videoSource = 1;

//Definiranje veličine rezolucije kamere / 2
const int camWidth = 320;
const int camHeight = 180;

//Konstante vezane za određivanje područja centra
const int camCenterArea = 70;
const int camCenterWidthAreaMin = camWidth - camCenterArea;
const int camCenterHeightAreaMin = camHeight - camCenterArea;
const int camCenterWidthAreaMax = camWidth + camCenterArea;
const int camCenterHeightAreaMax = camHeight + camCenterArea;

//Specijaliziranje xml kaskade za detektor
//const string cascadeFrontalFaceFilename = "lbpcascade_frontalface_improved.xml";
const string cascadeFrontalFaceFilename = "haarcascade_frontalface_default.xml";
const string cascadeEyesFaceFilename = "haarcascade_eye_tree_eyeglasses.xml";

//Specijalizacija abstraktne klase DetectionBasedTracker::IDetector
class CascadeDetectorAdapter : public DetectionBasedTracker::IDetector {
public:
    CascadeDetectorAdapter(Ptr<CascadeClassifier> detector) :
            IDetector(),
            Detector(detector) {
        CV_Assert(detector);
    }

    void detect(const Mat &Image, vector<Rect> &objects) {
        Detector->detectMultiScale(Image, objects, scaleFactor, minNeighbours, 0, minObjSize, maxObjSize);
    }

    virtual ~CascadeDetectorAdapter() {}

private:
    CascadeDetectorAdapter();
    Ptr<CascadeClassifier> Detector;
};

int main(int, char **) {

    //Mat image;
    //image = imread("mask.png", CV_LOAD_IMAGE_COLOR);   // Read the file

    cout << "Inicijalizacija uređaja." << endl;

    //Brisanje postojećih datoteka u Resource direktoriju
    system("exec rm -r Resources/*");

    string WindowName = "Praćenje lica";
    namedWindow(WindowName);
    VideoCapture VideoStream(videoSource);

    //Postavljanje rezolucije i fps-a video izvora
    VideoStream.set(CV_CAP_PROP_FRAME_WIDTH, camWidth * 2);
    VideoStream.set(CV_CAP_PROP_FRAME_HEIGHT, camHeight * 2);
    VideoStream.set(CV_CAP_PROP_FPS, 30);


    //Deklaracija kaskada i detektora detektora
    Ptr<CascadeClassifier> cascadeClasifierForFrontalFace = makePtr<CascadeClassifier>(cascadeFrontalFaceFilename);
    Ptr<DetectionBasedTracker::IDetector> MainDetector = makePtr<CascadeDetectorAdapter>(
            cascadeClasifierForFrontalFace);

    cascadeClasifierForFrontalFace = makePtr<CascadeClassifier>(cascadeFrontalFaceFilename);
    Ptr<DetectionBasedTracker::IDetector> TrackingDetector = makePtr<CascadeDetectorAdapter>(
            cascadeClasifierForFrontalFace);

    DetectionBasedTracker::Parameters params;
    DetectionBasedTracker Detector(MainDetector, TrackingDetector, params);

    //Deklaracija tipova kontejnera za slike koji se koriste u detekciji
    Mat ReferenceFrame;
    Mat GrayFrame;
    vector<Rect> Faces;

    //Varijabla u kojoj je spremljen broj uzetih fotografija lica
    int faceShotsCount = 0;
    /*
    char path [100] = "";
    const char* systemPath = (char*)system("echo $PWD");
    strcpy(path, systemPath);
     */

    cout << "Traženje uzorka." << endl;

    bool faceDetected = true;
    bool searchingForPerson = false;
    bool searchingForFace = false;
    int faceSearchCount = 0;

    clock_t begin;
    clock_t end;

    if (!arduino.isOpen())
    {
        cerr << "Ne mogu naci pomicni senzor!" << endl;
        return 1;
    }

    cout << "Pomicni senzor pronaden na: " << arduino.getDeviceName() << endl;

    string command;

    while (true) {

        VideoStream >> ReferenceFrame;
        cvtColor(ReferenceFrame, GrayFrame, COLOR_RGB2GRAY);
        Detector.process(GrayFrame);
        Detector.getObjects(Faces);

        if (Faces.size() < 1) {
            if (faceDetected) {
                begin = clock();
                faceDetected = false;
            } else {
                end = clock();
                double elapsed = double(end - begin) / CLOCKS_PER_SEC;
                if (elapsed > 2 && searchingForPerson == false && searchingForFace == false) {
                    command = (char) 5;
                    arduino.write(command);
                    searchingForPerson = true;
                }
                else if(searchingForPerson == true){
                    cout << arduino.read() << endl;
                    searchingForPerson = false;
                    searchingForFace = true;
                    command = (char) 6;
                    arduino.write(command);
                }
                else if(searchingForFace == true){
                    begin = clock();
                    if(faceSearchCount < 120){
                        command = (char) 7;
                        if(faceSearchCount % 2){
                            arduino.write(command);
                        }
                        faceSearchCount++;
                        usleep(60000);
                    }
                    else{
                        command = (char) 8;
                        arduino.write(command);
                        return 1;
                    }
                }
            }
        } else {

            faceDetected = true;
            searchingForPerson = false;
            searchingForFace = false;
            faceSearchCount = 0;

            int biggestFaceIndex = -1;
            int biggestFaceWidth = 0;
            bool faceYalligned = false;
            bool faceXalligned = false;

            //Za praćenje odabiremo samo najveće lice u kadru - pretposatvljamo da je to korisnik
            for (int i = 0; i < Faces.size(); i++) {
                if (Faces[i].width > biggestFaceWidth) {
                    biggestFaceWidth = Faces[i].width;
                    biggestFaceIndex = i;
                }
            }

            rectangle(ReferenceFrame, Rect(160, 90, 320, 180), Scalar(0, 0, 255));

            if (biggestFaceIndex != -1) {
                rectangle(ReferenceFrame, Faces[biggestFaceIndex], Scalar(0, 255, 0));
                line(ReferenceFrame, Point(camWidth, camHeight),
                     Point(Faces[biggestFaceIndex].x + Faces[biggestFaceIndex].width / 2,
                           Faces[biggestFaceIndex].y + Faces[biggestFaceIndex].height / 2), Scalar(0, 255, 0));
                //ellipse(ReferenceFrame, Faces[biggestFaceIndex], Scalar(0, 255, 0));
                //image.copyTo(ReferenceFrame(Rect(Faces[biggestFaceIndex].x, Faces[biggestFaceIndex].y, image.cols, image.rows)));

                int FaceCenterX = Faces[biggestFaceIndex].x + Faces[biggestFaceIndex].width / 2;
                int FaceCenterY = Faces[biggestFaceIndex].y + Faces[biggestFaceIndex].height / 2;

                if (FaceCenterX < camCenterWidthAreaMin) {
                    faceXalligned = false;
                    command = (char) 1;
                    arduino.write(command);
                } else if (FaceCenterX > camCenterWidthAreaMax) {
                    faceXalligned = false;
                    command = (char) 2;
                    arduino.write(command);
                } else {
                    faceXalligned = true;
                }

                if (FaceCenterY > camCenterHeightAreaMax) {
                    command = (char) 4;
                    arduino.write(command);
                    faceYalligned = false;
                } else if (FaceCenterY < camCenterHeightAreaMin) {
                    command = (char) 3;
                    arduino.write(command);
                    faceYalligned = false;
                } else {
                    faceYalligned = true;
                }

                if (faceXalligned && faceYalligned && shallCloseWhenDone) {
                    if (faceShotsCount < 5) {
                        Faces[biggestFaceIndex].width += 30;
                        Faces[biggestFaceIndex].height += 30;
                        Faces[biggestFaceIndex].x -= 30;
                        Faces[biggestFaceIndex].y -= 30;

                        cv::Mat croppedFaceImage;
                        croppedFaceImage = GrayFrame(Faces[biggestFaceIndex]).clone();
                        imwrite("Resources/" + to_string(faceShotsCount) + ".jpg", croppedFaceImage);
                        faceShotsCount++;
                        cout << "Uzorak lica uzet." << endl;
                    } else {
                        Detector.stop();
                        return 0;
                    }
                }
            }
        }

        imshow(WindowName, ReferenceFrame);
        if (waitKey(30) >= 0) continue;
    }

    Detector.stop();
    return 0;
}
