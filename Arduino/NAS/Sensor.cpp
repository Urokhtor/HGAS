#include "Arduino.h"
#include "Sensor.h"

#include <OneWire.h>
#include <DallasTemperature.h>
#include <dht11.h>
#include <Ultrasonic.h>
#include <Wire.h>
#include <BMP085.h>
//#include <Adafruit_BMP085.h>

int Sensor::getId() {
    return id;
}

void Sensor::setId(int newId) {
    id = newId;
}

void Sensor::setIndex(int newIndex)
{
    index = newIndex;
}

int Sensor::getIndex()
{
    return index;
}

/*
* Checks sensor's type and calls the corresponding function to get the reading.
*/

double Sensor::getReading()
{
    switch (type)
    {
        case _DEFAULT:
            lastReading = analogRead(index);
            break;
        case TEMPERATURE:
            lastReading = getDS18B20Reading();
            break;
        case DHT11:
            lastReading = getDHT11Reading();
            break;
        case SR04:
            lastReading = getSR04Reading();
            break;
        case BMP085_TEMPERATURE:
            lastReading = getBMP085temperature();
            break;
        case BMP085_PRESSURE:
            lastReading = getBMP085pressure();
            break;
        case BMP085_ALTITUDE:
            lastReading = getBMP085altitude();
            break;
        default:
            lastReading = analogRead(index);
            break;
    }
    
    return lastReading;
}

/*
* Get the reading for DS18B20 temperature sensor.
*/

double Sensor::getDS18B20Reading()
{
    OneWire oneWire(index);
    DallasTemperature sensor = DallasTemperature(&oneWire);
    sensor.setResolution(12);
    sensor.begin();
    sensor.requestTemperatures();
    return sensor.getTempCByIndex(0);
}

/*
* Get the reading for DHT11 humdidity sensor. Note that we don't use the
* temperature sensor the DHT11 has because it's useless with its BAD accuracy.
*/

double Sensor::getDHT11Reading()
{
    dht11 DHT11;
    int chk = DHT11.read(index);
  
    switch (chk)
    {
        case DHTLIB_OK:
            break;
        case DHTLIB_ERROR_CHECKSUM:
            return -1;
            break;
        case DHTLIB_ERROR_TIMEOUT:
            return -2;
            break;
        default:
            return -3;
            break;
  }
  
  return (double)DHT11.humidity;
}

double Sensor::getSR04Reading()
{
	Ultrasonic ultrasonic(index, index+1);
    double reading = (double)ultrasonic.convert(ultrasonic.timing(), Ultrasonic::CM);
    return reading;
}

double Sensor::getBMP085temperature() {
    BMP085 dps = BMP085();  
    Wire.begin();
    dps.init();
    long Temperature = 0, Pressure = 0, Altitude = 0;
    dps.getTemperature(&Temperature); 
    dps.getPressure(&Pressure);
    dps.getAltitude(&Altitude);
    return (double) Temperature;
}

double Sensor::getBMP085pressure() {
    Serial.println("At getPressure");
    BMP085 dps = BMP085();  
    Wire.begin();
    dps.init();
    long Temperature = 0, Pressure = 0, Altitude = 0;
    dps.getTemperature(&Temperature); 
    dps.getPressure(&Pressure);
    dps.getAltitude(&Altitude);
    Serial.print("The pressure is: ");Serial.println("Pressure");
    return (double) Pressure;
}

double Sensor::getBMP085altitude() {
    BMP085 dps = BMP085();  
    Wire.begin();
    dps.init();
    long Temperature = 0, Pressure = 0, Altitude = 0;
    dps.getTemperature(&Temperature); 
    dps.getPressure(&Pressure);
    dps.getAltitude(&Altitude);
    return (double) Altitude;
}

double Sensor::getLastReading()
{
    return lastReading;
}

void Sensor::setHighThresholdValue(double newThreshold)
{
    highThresholdValue = newThreshold;
}

double Sensor::getHighThresholdValue()
{
    return highThresholdValue;
}

void Sensor::setLowThresholdValue(double newThreshold)
{
    lowThresholdValue = newThreshold;
}

double Sensor::getLowThresholdValue()
{
    return lowThresholdValue;
}

void Sensor::setType(int newType)
{
    type = newType;
}

int Sensor::getType()
{
    return type;
}

/*
* Set the time when the last measurement was taken with the sensor.
*/

void Sensor::setLastReadingTime(unsigned long time)
{
    lastReadingTime = time;
}

/*
* When was the last reading taken, used by pumps to take hygrometer readings at
* predefined intervals.
*/

unsigned long Sensor::getLastReadingTime()
{
    return lastReadingTime;
}

int SensorManager::AddSensor(Sensor &sensor)
{
    if (!hasId(sensor.getId()))
    {
        container[size] = sensor;
        size++;
    }
}

int SensorManager::AddSensor(int _id, int _index, int _type, double lowThreshold, double highThreshold)
{
    // Check for possible duplicate index, add sensor to container.
    if (!hasId(_id))
    {
        Sensor sensor;
        sensor.setId(_id);
        sensor.setIndex(_index);
        sensor.setType(_type);
        sensor.setLowThresholdValue(lowThreshold);
        sensor.setHighThresholdValue(highThreshold);
        container[size] = sensor;
        
        size++;
    }

    else
        return 0;

    return 1;
}

int SensorManager::RemoveSensor(int _id)
{
    // Search for index in container, remove the sensor.
    if (hasId(_id))
        for (int i = 0; i < size; i++)
            if (container[i].getId() == _id) {
                for (int j = i; j <= size-1; j++)
                    container[j] = container[j+1];
                //container[size-1] = NULL;
                size--;
                return 1;
            }
            
    return 0;
}

/*
* Return reference to the sensor object at the specified index.
* Do not use this function to access Sensor class' mutators because it won't
* work. Use the mutators instead that SensorManager offers.
*/

Sensor &SensorManager::getSensor(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index) return container[i];
}

bool SensorManager::hasId(int _id)
{
    if (size == 0) return false;
    
    for (int i = 0; i < size; i++)
        if (container[i].getId() == _id) return true;
    
    return false;
}

bool SensorManager::hasIndex(int _index)
{
    if (size == 0) return false;
    
    for (int i = 0; i < size; i++)
        if (container[i].getIndex() == _index) return true;
    
    return false;
}

void SensorManager::setSize(int newSize)
{
    size = newSize;
}

int SensorManager::setIndex(int _index, int newIndex)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
            {
                container[i].setIndex(newIndex);
                return 1;
            }
            
    return -1;
}

int SensorManager::setType(int _index, int type)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
            {
                container[i].setType(type);
                return 1;
            }
            
    return -1;
}

int SensorManager::getType(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                return container[i].getType();
                
    return -1;
}

double SensorManager::getReading(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                return container[i].getReading();
                
    return -1;
}

int SensorManager::setHighThresholdValue(int _index, double value)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
            {
                container[i].setHighThresholdValue(value);
                return 1;
            }
            
    return -1;
}

double SensorManager::getHighThresholdValue(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                return container[i].getHighThresholdValue();
                
    return -1;
}

int SensorManager::setLowThresholdValue(int _index, double value)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
            {
                container[i].setLowThresholdValue(value);
                return 1;
            }
                
    return -1;
}

double SensorManager::getLowThresholdValue(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                return container[i].getLowThresholdValue();
                
    return -1;
}


int SensorManager::setLastReadingTime(int _index, unsigned long time)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
            {
                container[i].setLastReadingTime(time);
                return 1;
            }
            
    return -1;
}

double SensorManager::getLastReadingTime(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                return container[i].getLastReadingTime();

    return -1;
}
