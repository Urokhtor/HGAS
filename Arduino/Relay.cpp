#include "Arduino.h"
#include "Relay.h"

int RelayManager::changePins(int newPins[])
{
    if ((sizeof newPins/sizeof(int)) != MAX_RELAY_SIZE) return -1;

    for (int i = 0; i < MAX_RELAY_SIZE; i++)
        relays.relayPins[i] = newPins[i];

    return 0;
}

// Initializes the relay board.
void RelayManager::Initialize(int relayStartIndex)
{
    // Define what pins we use.
    for (int i = 0; i < MAX_RELAY_SIZE; i++)
        relays.relayPins[i] = relayStartIndex + i;
    
    // Make sure all the relays are set off.
    for (int i = 0; i < MAX_RELAY_SIZE; i++)
    {
        pinMode(relays.relayPins[i], OUTPUT);
        digitalWrite(relays.relayPins[i], HIGH);
        relays.relayStates[i] = LOW;
    }
}

int RelayManager::controlRelays(int command)
{
    if (command > 8 || command < 0) return -1;
    else if (command == 8) switchAllRelays();
    else if (command >= 0 && command <= 7) switchOneRelay(command);

    return 0;
}

boolean RelayManager::getState(int index)
{
    for (int i = 0; i < MAX_RELAY_SIZE; i++)
        if (relays.relayPins[i] == index) return relays.relayStates[i];
}

boolean RelayManager::hasIndex(int _index)
{
    for (int i = 0; i < MAX_RELAY_SIZE; i++)
        if (relays.relayPins[i] == _index) return true;
    
    return false;
}

void RelayManager::switchAllRelays()
{
    for (int i = 0; i < MAX_RELAY_SIZE; i++)
    {
        //If even one relay is on, shut ALL down.
        if (relays.relayStates[i] == HIGH)
        {
            int j = 0;
            for (j; j < MAX_RELAY_SIZE; j++)
            {
                digitalWrite(relays.relayPins[j], HIGH);
                relays.relayStates[j] = LOW;
            }
            if (j == 8) break; // Makes sure the other option doesn't get executed.
        }
            
        // If we get to last relay and none has been on, and also the last
        // relay is off, start ALL the relays.
        else if (relays.relayStates[i] == LOW && i == 7)
        {
            int j = 0;
            for (j; j < MAX_RELAY_SIZE; j++)
            {
                digitalWrite(relays.relayPins[j], LOW);
                relays.relayStates[j] = HIGH;
            }
            if (j == 8) break; // Makes sure the other option doesn't get executed.
        }
    }
}

int RelayManager::switchOneRelay(int index)
{
    for (int i = 0; i < MAX_RELAY_SIZE; i++)
    {
        if (relays.relayPins[i] == index)
        {
            if (relays.relayStates[i] == LOW)
            {
                digitalWrite(relays.relayPins[i], LOW);
                relays.relayStates[i] = HIGH;
                return 1;
            }
            
            else
            {
                digitalWrite(relays.relayPins[i], HIGH);
                relays.relayStates[i] = LOW;
                return 0;
            }
        }
    }
    
    return -1;
}

Pump::Pump(): isRunning(false)
{

}

void Pump::setIndex(int newIndex)
{
    index = newIndex;
}

int Pump::getIndex()
{
    return index;
}

void Pump::setStartTime(unsigned long newStartTime)
{
    startTime = newStartTime;
}

unsigned long Pump::getStartTime()
{
    return startTime;
}

void Pump::setMaxOnTime(unsigned long newMaxOnTime)
{
    maxOnTime = newMaxOnTime;
}

unsigned long Pump::getMaxOnTime()
{
    return maxOnTime;
}

void Pump::setIsRunning(boolean flag)
{
    isRunning = flag;
}

boolean Pump::getIsRunning()
{
    return isRunning;
}

void Pump::setHygrometerIndex(int newIndex)
{
    hygrometerIndex = newIndex;
}

int Pump::getHygrometerIndex()
{
    return hygrometerIndex;
}

void Pump::setUsesHygrometer(boolean flag)
{
    usesHygrometer = flag;
}

boolean Pump::getUsesHygrometer()
{
    return usesHygrometer;
}

int PumpManager::AddPump(Pump &pump)
{
    if (!hasIndex(pump.getIndex()))
    {
        container[size] = pump;
        size++;
    }
}

int PumpManager::AddPump(int _index, unsigned long maxOnTime, boolean usesHygrometer, int hygrometerIndex)
{
    if (!hasIndex(_index))
    {
        Pump pump;
        pump.setIndex(_index);
        pump.setMaxOnTime(maxOnTime);
        pump.setIsRunning(false);
        pump.setHygrometerIndex(hygrometerIndex);
        pump.setUsesHygrometer(usesHygrometer);
        container[size] = pump;
        size++;
    }
}

int PumpManager::RemovePump(int _index)
{
    // Search for index in container, remove the pump.
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                for (int j = i; j <= size-1; j++)
                    container[j] = container[j+1];
                size--;
                return 1;
    
    return 0;
}

Pump &PumpManager::getPump(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index) return container[i];
}

void PumpManager::getIndexList(int arr[PUMP_MANAGER_SIZE])
{
    
    for (int i = 0; i < PUMP_MANAGER_SIZE; i++)
        arr[i] = container[i].getIndex();
}

bool PumpManager::hasIndex(int _index)
{
    if (size == 0) return false;

    for (int i = 0; i < size; i++)
        if (container[i].getIndex() == _index) return true;

    return false;
}

void PumpManager::setSize(int newSize)
{
    size = newSize;
}

int PumpManager::setMaxOnTime(int _index, unsigned long _maxOnTime)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
            {
                container[i].setMaxOnTime(_maxOnTime);
                return 1;
            }
    
    return -1;
}

unsigned long PumpManager::getMaxOnTime(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                return container[i].getMaxOnTime();
    
    return 0;
}

int PumpManager::setUsesHygrometer(int _index, boolean _usesHygrometer)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
            {
                container[i].setUsesHygrometer(_usesHygrometer);
                return 1;
            }
    
    return -1;
}

boolean PumpManager::getUsesHygrometer(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                return container[i].getUsesHygrometer();
    
    return false;
}

int PumpManager::setHygrometerIndex(int _index, int _hygrometerIndex)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
            {
                container[i].setHygrometerIndex(_hygrometerIndex);
                return 1;
            }
    
    return -1;
}

int PumpManager::getHygrometerIndex(int _index)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                return container[i].getHygrometerIndex();
    
    return -1;
}

void PumpManager::setStartTime(int _index, unsigned long newStartTime)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                container[i].setStartTime(newStartTime);
}

void PumpManager::setIsRunning(int _index, boolean flag)
{
    if (hasIndex(_index))
        for (int i = 0; i < size; i++)
            if (container[i].getIndex() == _index)
                container[i].setIsRunning(flag);
}