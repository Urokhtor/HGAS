#ifndef relay_h
#define relay_h

const int MAX_RELAY_SIZE = 8; // How many relays do we have. In future change this to support larger relay arrays.
const int PUMP_MANAGER_SIZE = 8; // Essentially all the relays in our relay board can be pumps, however what if there are other devices? Handle that in future!
const unsigned long PUMP_MAX_ON_TIME = 140000.0; // The maximum allowed on-time for pumps in milliseconds. A safety feature so pumps don't accidentally stay on.

/*
* This class controls relays straight, i.e. directly sets relay status (ON/OFF).
*/

class RelayModule
{
public:
    int relayPins[MAX_RELAY_SIZE];
    boolean relayStates[MAX_RELAY_SIZE];
};

/*
* RelayManager controls the states of relays in RelayModule.
*/

class RelayManager
{
private:
    RelayModule relays;
    
    void switchAllRelays();
    
public:
    int changePins(int newPins[]);
    void Initialize(int relayStartIndex);
    int controlRelays(int command);
    int switchOneRelay(int index);
    boolean getState(int index);
    boolean hasIndex(int _index);
};

/*
* Pump contains useful routines for pump devices, like time switch-off and whether hygrometer should be
* used to measure the height of water surface so pump can be switched off when the threshold is reached.
* Manager class takes care of doing this, pump only needs to tell Manager whether it uses a hygrometer
* and if so, in which port does the hygrometer reside.
*/

class Pump
{
private:
    int index;
    unsigned long startTime;
    unsigned long maxOnTime;
    boolean isRunning;
    int hygrometerIndex;
    boolean usesHygrometer;

public:
    Pump();
    void setIndex(int newIndex);
    int getIndex();
    void setStartTime(unsigned long newStartTime);
    unsigned long getStartTime();
    void setMaxOnTime(unsigned long newMaxOnTime);
    unsigned long getMaxOnTime();
    void setIsRunning(boolean flag);
    boolean getIsRunning();
    void setHygrometerIndex(int newIndex);
    int getHygrometerIndex();
    void setUsesHygrometer(boolean flag);
    boolean getUsesHygrometer();
};

/*
* PumpManager manages all the pump devices.
*/

class PumpManager
{
private:
    int size;
    Pump container[PUMP_MANAGER_SIZE];

public:
    int AddPump(Pump &pump);
    int AddPump(int _index, unsigned long maxOnTime = PUMP_MAX_ON_TIME, boolean usesHygrometer = false, int hygrometerIndex = -1);
    int RemovePump(int _index);
    Pump &getPump(int _index);
    void getIndexList(int arr[PUMP_MANAGER_SIZE]);
    bool hasIndex(int _index);
    void setSize(int newSize);
    
    int setMaxOnTime(int _index, unsigned long _maxOnTime);
    unsigned long getMaxOnTime(int _index);
    int setUsesHygrometer(int _index, boolean _usesHygrometer);
    boolean getUsesHygrometer(int _index);
    int setHygrometerIndex(int _index, int _hygrometerIndex);
    int getHygrometerIndex(int _index);
    
    void setStartTime(int _index, unsigned long newStartTime);
    void setIsRunning(int _index, boolean flag);
};

#endif
