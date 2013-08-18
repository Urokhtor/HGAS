#ifndef timer_h
#define timer_h

#include "Arduino.h"

/*
* Just a simple timer class to keep the manager correctly in time.
*/

class Timer
{
private:
    unsigned long lastTime;
    unsigned long currentTime;
    
public:
    void Update() {lastTime = currentTime; currentTime = millis();}
    void Reset() {currentTime = millis(); lastTime = currentTime;}
    unsigned long getLastTime() {return lastTime;}
    unsigned long getCurrentTime() {return currentTime;}
    
};
#endif