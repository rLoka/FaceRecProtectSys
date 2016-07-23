/*
Dio izvornog koda preuzet sa https://github.com/opencv/opencv/blob/master/samples/cpp/dbt_face_detection.cpp
*/

/*
Verzija: 1.0
Opis: Program za detekciju i komunikaciju sa Arduino mikrokontrolerom
Autor: Karlo Grlić
Datum: 07.2015.
*/

#include <opencv2/imgproc.hpp>
#include <opencv2/video.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/features2d.hpp>
#include <opencv2/objdetect.hpp>
#include <fstream>

using namespace std;
using namespace cv;

//Definiranje izvora videa
//0 - ugrađena kamera, 1, 2, 3 ... ostale video kamere, "home/karlo/.../video.avi" putanja videa
const int videoSource = 1;

//Definiranje veličine rezolucije kamere / 2
const int camWidth = 640;
const int camHeight = 360;

//Konstante vezane za određivanje područja centra
const int camCenterArea = 40;
const int camCenterWidthAreaMin = camWidth - camCenterArea;
const int camCenterHeightAreaMin = camHeight - camCenterArea;
const int camCenterWidthAreaMax = camWidth + camCenterArea;
const int camCenterHeightAreaMax = camHeight + camCenterArea;

//Specijaliziranje xml kaskade za detektor
const string cascadeFrontalFaceFilename = "lbpcascade_frontalface.xml";

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

    virtual ~CascadeDetectorAdapter() { }

private:
    CascadeDetectorAdapter();
    Ptr<CascadeClassifier> Detector;
};


int main(int, char **) {

    //Inicijalizacija i otvaranje veze za slanje podataka Arduino mikrokontroleru putem serijskog porta
    ofstream arduinoDevice;
    arduinoDevice.open("/dev/ttyUSB0", ios::out | ios::app | ios::binary);

    string WindowName = "Praćenje lica";
    namedWindow(WindowName);
    VideoCapture VideoStream(videoSource);

    //Postavljanje rezolucije i fps-a video izvora
    VideoStream.set(CV_CAP_PROP_FRAME_WIDTH, camWidth * 2);
    VideoStream.set(CV_CAP_PROP_FRAME_HEIGHT, camHeight * 2);
    VideoStream.set(CV_CAP_PROP_FPS, 30);


    //Deklaracija kaskada i detektora detektora
    Ptr<CascadeClassifier> cascadeClasifierForFrontalFace = makePtr<CascadeClassifier>(cascadeFrontalFaceFilename);
    Ptr<DetectionBasedTracker::IDetector> MainDetector = makePtr<CascadeDetectorAdapter>(cascadeClasifierForFrontalFace);

    cascadeClasifierForFrontalFace = makePtr<CascadeClassifier>(cascadeFrontalFaceFilename);
    Ptr<DetectionBasedTracker::IDetector> TrackingDetector = makePtr<CascadeDetectorAdapter>(cascadeClasifierForFrontalFace);

    DetectionBasedTracker::Parameters params;
    DetectionBasedTracker Detector(MainDetector, TrackingDetector, params);

    //Deklaracija tipova kontejnera za slike koji se koriste u detekciji
    Mat ReferenceFrame;
    Mat GrayFrame;
    vector<Rect> Faces;

    while (true) {
        VideoStream >> ReferenceFrame;
        cvtColor(ReferenceFrame, GrayFrame, COLOR_RGB2GRAY);
        Detector.process(GrayFrame);
        Detector.getObjects(Faces);

        int biggestFaceIndex = -1;
        int biggestFaceWidth = 0;
        
        //Za praćenje odabiremo samo najveće lice u kadru - pretposatvljamo da je to korisnik
        for (int i = 0; i < Faces.size(); i++) {
            if (Faces[i].width > biggestFaceWidth)
            {
                biggestFaceWidth = Faces[i].width;
                biggestFaceIndex = i;
            }
        }

        if(biggestFaceIndex != -1)
        {
            rectangle(ReferenceFrame, Faces[biggestFaceIndex], Scalar(0, 255, 0));

            int FaceCenterX = Faces[biggestFaceIndex].x + Faces[biggestFaceIndex].width / 2;
            int FaceCenterY = Faces[biggestFaceIndex].y + Faces[biggestFaceIndex].height / 2;

            if (FaceCenterX < camCenterWidthAreaMin) {
                arduinoDevice << (char) 1 << endl;
            }
            else if (FaceCenterX > camCenterWidthAreaMax) {
                arduinoDevice << (char) 2 << endl;
            }

            if (FaceCenterY > camCenterHeightAreaMax) {
                arduinoDevice << (char) 4 << endl;
            }
            else if (FaceCenterY < camCenterHeightAreaMin) {
                arduinoDevice << (char) 3 << endl;
            }
        }

        imshow(WindowName, ReferenceFrame);

        if (waitKey(30) >= 0) break;
    }

    arduinoDevice.close();

    Detector.stop();

    return 0;
}
