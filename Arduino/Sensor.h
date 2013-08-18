#ifndef sensor_h
#define sensor_h


// Sensor types.
const int _DEFAULT = 0;
const int TEMPERATURE = 1;
const int DHT11 = 2;
const int SR04 = 3;

const int MAX_DISTANCE = 200;

// This is currently tailored for Arduino Mega to use all the analog ports.
// However some sensors use digital input so this should be changed in future.
const int SENSOR_MANAGER_SIZE = 16;

class Sensor
{
protected:
    int index; // Which physical pin does the sensor reside in.
    double lastReading; // The value of last reading we took.
    double highThresholdValue; // What kind of treshold do we want to have with this sensor.
    double lowThresholdValue;
    int type; // What type is the sensor, temperature, humidity...
    unsigned long lastReadingTime; // When was the last reading taken from this sensor.
    
    // Sensor type specific functions for taking readings.
    double getDS18B20Reading();
    double getDHT11Reading();
    double getSR04Reading();
    
public:
    void setIndex(int newIndex);
    int getIndex();
    double getReading();
    double getLastReading();
    
    void setHighThresholdValue(double newTreshold);
    double getHighThresholdValue();
    void setLowThresholdValue(double newTreshold);
    double getLowThresholdValue();
    void setType(int newType);
    int getType();
    void setLastReadingTime(unsigned long time);
    unsigned long getLastReadingTime();
};

/*
* SensorManager class manages all the sensor devices attached to the Arduino and accessing them.
* Use this class' mutators instead of Sensor class' mutators because Arduino doesn't update
* the sensor's fields if you use for example getSensor().setType().
*/

class SensorManager
{
private:
    int size;
    Sensor container[SENSOR_MANAGER_SIZE];

public:
    int AddSensor(Sensor &sensor);
    int AddSensor(int _index, int _type = _DEFAULT, double lowThreshold = 0.0, double highThreshold = 0.0);
    int RemoveSensor(int _index);
    Sensor &getSensor(int _index);
    bool hasIndex(int _index);
    void setSize(int newSize);
    
    int setIndex(int _index, int newIndex);
    int setType(int _index, int type);
    int getType(int _index);
    
    double getReading(int _index);
    int setHighThresholdValue(int _index, double value);
    double getHighThresholdValue(int _index);
    int setLowThresholdValue(int _index, double value);
    double getLowThresholdValue(int _index);
    int setLastReadingTime(int _index, unsigned long time);
    double getLastReadingTime(int _index);

};

#endif
