#include "MessageParser.h"

#include <aJSON.h>

#include "Manager.h"

#include "MemoryFree.h"

const char *KEY_COMMAND = "command";
const char *KEY_DEVICE = "unit";
const char *KEY_DEVICE_TYPE = "typedevice";
const char *KEY_IS_STARTUP = "startup";
const char *KEY_INDEX = "index";
const char *KEY_HIGH_THRESHOLD = "high";
const char *KEY_LOW_THRESHOLD = "low";
const char *KEY_TYPE = "type";
const char *KEY_HYGROMETER_INDEX = "hygrometer";
const char *KEY_USES_HYGROMETER = "uses";
const char *KEY_ERROR = "error";
const char *KEY_READING = "reading";
const char *KEY_RESPONSE = "response";
const char *KEY_STATE = "state";
const char *KEY_MAX_ON_TIME = "max";
const char *KEY_ID = "id";

void MessageParser::Execute(aJsonObject *root, char **response)
{
    aJsonObject *returnObject = aJson.createObject();
    
    if (root != NULL)
    {
        aJsonObject *command = aJson.getObjectItem(root, KEY_COMMAND);
        
        if (command != NULL)
        {
            if (command->valueint == SEND_READ)
                MessageParser::Read(root, returnObject);
            
            else if (command->valueint == SEND_WRITE)
                MessageParser::Run(root, returnObject, SEND_WRITE);
                
            else if (command->valueint == SEND_ENABLE)
                MessageParser::Run(root, returnObject, SEND_ENABLE);
                
            else if (command->valueint == SEND_DISABLE)
                MessageParser::Run(root, returnObject, SEND_DISABLE);
                
            else if (command->valueint == SEND_INSERT)
                MessageParser::Insert(root, returnObject);
                
            else if (command->valueint == SEND_MODIFY)
                MessageParser::Modify(root, returnObject);
                
            else if (command->valueint == SEND_REMOVE)
                MessageParser::Remove(root, returnObject);
            
            else if (command->valueint == SEND_FREEMEMORY)
                MessageParser::FreeMemory(root, returnObject);
            
            else
                aJson.addNumberToObject(returnObject, KEY_ERROR, UNRECOGNISED_COMMAND_ERROR);
        }
        
        else
            aJson.addNumberToObject(returnObject, KEY_ERROR, NO_COMMAND_ERROR);
    }
    
    *response = aJson.print(returnObject);
    aJson.deleteItem(returnObject);
}

/*
 * Turn a char message into a JSON object.
 *
 */
aJsonObject *MessageParser::toJson(char message[512])
{
    return aJson.parse(message);
}

void MessageParser::SetManager(Manager *_manager)
{
    manager = _manager;
}

void MessageParser::Read(aJsonObject *root, aJsonObject *returnValue)
{
    // Get the index and create an object for the return message.
    aJsonObject *index = aJson.getObjectItem(root, KEY_INDEX);
    
    // If index isn't found, tell the sender about it.
    if (index == NULL)
    {
        aJson.addNumberToObject(returnValue, KEY_ERROR, NO_INDEX_ERROR);
        return;
    }
    
    // Get the reading and write it to the object. Then write a success to the response.
    aJson.addNumberToObject(returnValue, KEY_READING, manager->getSensorManager()->getReading(index->valueint));
    aJson.addNumberToObject(returnValue, KEY_RESPONSE, READ_SENSOR_SUCCESS);
}

void MessageParser::Run(aJsonObject *root, aJsonObject *returnValue, int commandType)
{
    aJsonObject *index = aJson.getObjectItem(root, KEY_INDEX);
    
    if (index == NULL)
    {
        aJson.addNumberToObject(returnValue, KEY_ERROR, NO_INDEX_ERROR);
        return;
    }

    // Check if the given index exists in the managers.
    if (manager->getPumpManager()->hasIndex(index->valueint) || manager->getRelayManager()->hasIndex(index->valueint))
    {
        int state = manager->getRelayManager()->getState(index->valueint);
        
        // Toggle relay state if a) it's a write command, b) it's an enable command and relay is off,
        // c) it's a disable command and relay is on.
        if (commandType == SEND_WRITE || (commandType == SEND_ENABLE && state == 0) || (commandType == SEND_DISABLE && state == 1))
        {
            int response = manager->getRelayManager()->switchOneRelay(index->valueint);
            aJson.addNumberToObject(returnValue, KEY_STATE, response);
        }
        
        else
        {
            aJson.addNumberToObject(returnValue, KEY_RESPONSE, NO_ACTION_NEEDED);
            return;
        }
        
        if (commandType == SEND_ENABLE && state == 0 && manager->getPumpManager()->hasIndex(index->valueint))
        {
            manager->getPumpManager()->setIsRunning(index->valueint, true);
            manager->getPumpManager()->setStartTime(index->valueint, manager->getTimer()->getCurrentTime());
        }
        
        aJson.addNumberToObject(returnValue, KEY_RESPONSE, RUN_DEVICE_SUCCESS);
    }
    
    else
        aJson.addNumberToObject(returnValue, KEY_ERROR, NO_DEVICE_ERROR);
}

void MessageParser::Insert(aJsonObject *root, aJsonObject *returnValue)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, KEY_DEVICE_TYPE);
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, KEY_ERROR, NO_TYPE_ERROR);
        return;
    }

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int id = aJson.getObjectItem(root, KEY_ID)->valueint;
        
        if (manager->getSensorManager()->hasId(id))
        {
            aJson.addNumberToObject(returnValue, KEY_ERROR, SENSOR_EXISTS_ERROR);
            return;
        }
        
        int index = aJson.getObjectItem(root, KEY_INDEX)->valueint;
        int type = aJson.getObjectItem(root, KEY_TYPE)->valueint;
        int lowthreshold = aJson.getObjectItem(root, KEY_LOW_THRESHOLD)->valuefloat;
        double highthreshold = aJson.getObjectItem(root, KEY_HIGH_THRESHOLD)->valuefloat;
        manager->getSensorManager()->AddSensor(id, index, type, lowthreshold, highthreshold);
        
        aJson.addNumberToObject(returnValue, KEY_RESPONSE, INSERT_SENSOR_SUCCESS);
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int id = aJson.getObjectItem(root, KEY_ID)->valueint;
        
        if (manager->getPumpManager()->hasId(id))
        {
            aJson.addNumberToObject(returnValue, KEY_ERROR, PUMP_EXISTS_ERROR);
            return;
        }
        
        int index = aJson.getObjectItem(root, KEY_INDEX)->valueint;
        unsigned long maxontime = ((unsigned long) aJson.getObjectItem(root, KEY_MAX_ON_TIME)->valueint) * 1000;
        bool useshygrometer = aJson.getObjectItem(root, KEY_USES_HYGROMETER)->valuebool;
        int hygrometerindex = aJson.getObjectItem(root, KEY_HYGROMETER_INDEX)->valueint;
        manager->getPumpManager()->AddPump(id, index, maxontime, useshygrometer, hygrometerindex);
        
        aJson.addNumberToObject(returnValue, KEY_RESPONSE, INSERT_PUMP_SUCCESS);
    }

    else
        aJson.addNumberToObject(returnValue, KEY_ERROR, WRONG_TYPE_ERROR);
}

void MessageParser::Modify(aJsonObject *root, aJsonObject *returnValue)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, KEY_DEVICE_TYPE);
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, KEY_ERROR, NO_TYPE_ERROR);
        return;
    }
    
    aJsonObject *device = aJson.getObjectItem(root, KEY_DEVICE);

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int id = aJson.getObjectItem(root, KEY_ID)->valueint;
        
        if (!manager->getSensorManager()->hasId(id))
        {
            aJson.addNumberToObject(returnValue, KEY_ERROR, SENSOR_DOESNT_EXIST_ERROR);
            return;
        }
    
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int id = aJson.getObjectItem(root, KEY_ID)->valueint;
        
        if (!manager->getPumpManager()->hasId(id))
        {
            aJson.addNumberToObject(returnValue, KEY_ERROR, PUMP_DOESNT_EXIST_ERROR);
            return;
        }
    }
    
    else
        aJson.addNumberToObject(returnValue, KEY_ERROR, WRONG_TYPE_ERROR);
}

void MessageParser::Remove(aJsonObject *root, aJsonObject *returnValue)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, KEY_DEVICE_TYPE);
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, KEY_ERROR, NO_TYPE_ERROR);
        return;
    }
    
    aJsonObject *device = aJson.getObjectItem(root, KEY_DEVICE);

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int id = aJson.getObjectItem(root, KEY_ID)->valueint;
        
        if (!manager->getSensorManager()->hasId(id))
        {
            aJson.addNumberToObject(returnValue, KEY_ERROR, SENSOR_DOESNT_EXIST_ERROR);
            return;
        }
        
        int response = manager->getSensorManager()->RemoveSensor(id);
        
        if (response) aJson.addNumberToObject(returnValue, KEY_RESPONSE, REMOVE_SENSOR_SUCCESS);
        else if (!response) aJson.addNumberToObject(returnValue, KEY_ERROR, SENSOR_DOESNT_EXIST_ERROR); // Shouldn't happen because we check that the sensor exists, but handle anyways.
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int id = aJson.getObjectItem(root, KEY_ID)->valueint;
        
        if (!manager->getPumpManager()->hasId(id))
        {
            aJson.addNumberToObject(returnValue, KEY_ERROR, PUMP_DOESNT_EXIST_ERROR);
            return;
        }
        
        int response = manager->getPumpManager()->RemovePump(id);
        
        if (response) aJson.addNumberToObject(returnValue, KEY_RESPONSE, REMOVE_PUMP_SUCCESS);
        else if (!response) aJson.addNumberToObject(returnValue, KEY_ERROR, PUMP_DOESNT_EXIST_ERROR); // Shouldn't happen because we check that the sensor exists, but handle anyways.
    }
    
    else
        aJson.addNumberToObject(returnValue, KEY_ERROR, WRONG_TYPE_ERROR);
}

void MessageParser::FreeMemory(aJsonObject *root, aJsonObject *returnValue)
{
    aJson.addNumberToObject(returnValue, KEY_RESPONSE, READ_FREEMEMORY_SUCCESS);
    aJson.addNumberToObject(returnValue, KEY_READING, freeMemory());
}