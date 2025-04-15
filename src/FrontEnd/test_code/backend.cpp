#include <windows.h>
#include <stdio.h>
#include <cstdlib>
#include <string>
#include <sstream>
#include <iostream>
#include <queue>
#include <thread>
#include <chrono>
#include <cmath>
#include <algorithm> 


std::queue<float> a1_queue;
std::queue<float> a2_queue;
//replace COM# with whatever port anchors are connected to
const char* a1PortName = "\\\\.\\COM5";
const char* a2PortName = "\\\\.\\COM6";
HANDLE anchor1 = CreateFileA(a1PortName, GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
HANDLE anchor2 = CreateFileA(a2PortName, GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);

float b = 20.0;

//TODO : Create error handling and thread that allows for user input to cancel the loop, as now its infinite, also test test test.


//recieve functions for use in threads, basic operation is reading to a buffer of bytes, casting to float and storing on a queue
void anchor1_recv(){
    char buf[256];
    DWORD bytesRead;
    if(ReadFile(anchor1, buf, sizeof(buf)-1, &bytesRead, NULL)){
        buf[bytesRead] = '\0';
        float distAnchor = std::atof(buf);
        distAnchor*= 1.093;
        printf("A1 recieved data: %f\n", distAnchor);
        a1_queue.push(distAnchor);
        return;
    }else{
        fprintf(stderr, "Error reading from serial port\n");
        CloseHandle(anchor1);
        //CloseHandle(anchor2);
        return;
    }

}
void anchor2_recv(){
    char buf[256];
    DWORD bytesRead;
    if(ReadFile(anchor2, buf, sizeof(buf)-1, &bytesRead, NULL)){
        buf[bytesRead] = '\0';
        float distAnchor2 = std::atof(buf);
        distAnchor2 *= 1.093;
        printf("A2 recieved data: %f\n", distAnchor2);
        a2_queue.push(distAnchor2);
        return;
    }else{
        fprintf(stderr, "Error reading from serial port\n");
        //CloseHandle(anchor1);
        CloseHandle(anchor2);
        return;
    }

}



int main() {

    //Basic initialization stuff, make sure 115200 baud rate is used
    if(anchor1 == INVALID_HANDLE_VALUE || anchor2 == INVALID_HANDLE_VALUE){
        fprintf(stderr, "Error connecting to port(s)");
        return 1;
    }

    DCB dcbSerialParams = {0};
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);

    if (!GetCommState(anchor1, &dcbSerialParams) || !GetCommState(anchor2, &dcbSerialParams) ){
        fprintf(stderr, "Error getting port(s) state");
        CloseHandle(anchor1);
        CloseHandle(anchor2);
        return 1;
    }

    dcbSerialParams.BaudRate = CBR_115200;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity = NOPARITY;

    if (!SetCommState(anchor1, &dcbSerialParams) || !SetCommState(anchor2, &dcbSerialParams)){
        fprintf(stderr, "Error setting port state");
        CloseHandle(anchor1);
        CloseHandle(anchor2);
        return 1;
    }

    
    
    //Data collection loop
    while(true){
        //seperate threads for gathering data
        std::thread a1(anchor1_recv);
        std::thread a2(anchor2_recv);
        a1.join();
        a2.join();
        //std::this_thread::sleep_for(std::chrono::milliseconds(50));
        if(a1_queue.empty() || a2_queue.empty()){
            //check for empty queue error and redo threads if no data
            printf("Error in recive threads, rerunning");
            continue;
        }
        float a = a1_queue.front();
        float c = a2_queue.front();

        printf("A: %f, B: %f, C: %f \n", a, b, c );

        a1_queue.pop();
        a2_queue.pop();
        //law of cosines to find angle between a1 and ball loc
    
        float numerator = (a*a) + (b*b) - (c*c);
        float denominator = (2.00*a*b);
        float ang_gamma = numerator/denominator;
        ang_gamma = float(std::max(float(-1.0), (std::min(float(1.0), ang_gamma)))); //clamp to prevent nan

        float gamma = acos(ang_gamma);

        printf("Gamma = %f \n", gamma);

        float x_val = cos(gamma)*a;
        float y_val = sin(gamma)*a;

        printf("X val: %f ", x_val);
        printf("Y val: %f \n", y_val);




        

    }
    CloseHandle(anchor1);
    CloseHandle(anchor2);
    return 0;

}