#include "MessageParser.h"

#include <aJSON.h>

#include "Manager.h"

char *MessageParser::Execute(aJsonObject *root)
{
    Serial.println(aJson.print(root));
    aJsonObject *returnObject = aJson.createObject();
    
    if (root != NULL)
    {
        aJsonObject *command = aJson.getObjectItem(root, "command");
        
        if (command != NULL)
        {
            if (command->valueint == SEND_READ)
                return MessageParser::Read(root);
            
            else if (command->valueint == SEND_WRITE)
                return MessageParser::Run(root, SEND_WRITE);
                
            else if (command->valueint == SEND_ENABLE)
                return MessageParser::Run(root, SEND_ENABLE);
                
            else if (command->valueint == SEND_DISABLE)
                return MessageParser::Run(root, SEND_DISABLE);
                
            else if (command->valueint == SEND_INSERT)
                return MessageParser::Insert(root);
                
            else if (command->valueint == SEND_MODIFY)
                return MessageParser::Modify(root);
                
            else if (command->valueint == SEND_REMOVE)
                return MessageParser::Remove(root);
            
            else
                aJson.addNumberToObject(returnObject, "error", UNRECOGNISED_COMMAND_ERROR);
        }
        
        else
            aJson.addNumberToObject(returnObject, "error", NO_COMMAND_ERROR);
    }
    
    return aJson.print(returnObject);
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

char *MessageParser::Read(aJsonObject *root)
{
    // Get the index and create an object for the return message.
    aJsonObject *index = aJson.getObjectItem(root, "index");
    aJsonObject *returnValue = aJson.createObject();
    Serial.println(index->valueint);
    // If index isn't found, tell the sender about it.
    if (index == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_INDEX_ERROR);
        return aJson.print(returnValue);
    }
    Serial.println(manager->getSensorManager().getReading(index->valueint));
    // Get the reading and write it to the object. Then write a success to the response.
    aJson.addNumberToObject(returnValue, "reading", manager->getSensorManager().getReading(index->valueint));
    aJson.addNumberToObject(returnValue, "response", READ_SENSOR_SUCCESS);
    
    return aJson.print(returnValue);
}

char *MessageParser::Run(aJsonObject *root, int commandType)
{
    aJsonObject *index = aJson.getObjectItem(root, "index");
    aJsonObject *returnValue = aJson.createObject();
    
    if (index == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_INDEX_ERROR);
        return aJson.print(returnValue);
    }

    // Check if the given index exists in the managers.
    if (manager->getPumpManager().hasIndex(index->valueint) || manager->getRelayManager().hasIndex(index->valueint))
    {
        int state = manager->getRelayManager().getState(index->valueint);
        Serial.print("State: "); Serial.println(state);
        // Toggle relay state if a) it's a write command, b) it's an enable command and relay is off,
        // c) it's a disable command and relay is on.
        if (commandType == SEND_WRITE || (commandType == SEND_ENABLE && state == 0) || (commandType == SEND_DISABLE && state == 1))
        {
            int response = manager->getRelayManager().switchOneRelay(index->valueint);
            Serial.print("Response: ");Serial.println(response);
            aJson.addNumberToObject(returnValue, "state", response);
        }
        
        else
        {
            aJson.addNumberToObject(returnValue, "response", NO_ACTION_NEEDED);
            return aJson.print(returnValue);
        }
        
        Serial.println(aJson.print(returnValue));
        if (manager->getPumpManager().hasIndex(index->valueint))
        {
            manager->getPumpManager().setIsRunning(index->valueint, true);
            manager->getPumpManager().setStartTime(index->valueint, manager->getTimer().getCurrentTime());
        }
        
        aJson.addNumberToObject(returnValue, "response", RUN_DEVICE_SUCCESS);
        Serial.println(aJson.print(returnValue));
    }
    
    else
        aJson.addNumberToObject(returnValue, "error", NO_DEVICE_ERROR);

    return aJson.print(returnValue);
}

char *MessageParser::Insert(aJsonObject *root)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, "devicetype");
    aJsonObject *device = aJson.getObjectItem(root, "device");
    aJsonObject *returnValue = aJson.createObject();
    Serial.println(deviceType->valueint);
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_TYPE_ERROR);
        return aJson.print(returnValue);
    }

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (manager->getSensorManager().hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", SENSOR_EXISTS_ERROR);
            return aJson.print(returnValue);
        }
        
        int type = aJson.getObjectItem(device, "devicetype")->valueint;
        int lowthreshold = aJson.getObjectItem(device, "lowthreshold")->valuefloat;
        double highthreshold = aJson.getObjectItem(device, "highthreshold")->valuefloat;
        manager->getSensorManager().AddSensor(index, type, lowthreshold, highthreshold);
        
        aJson.addNumberToObject(returnValue, "response", INSERT_SENSOR_SUCCESS);
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (manager->getPumpManager().hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", PUMP_EXISTS_ERROR);
            return aJson.print(returnValue);
        }
        
        unsigned long maxontime = (unsigned long)aJson.getObjectItem(device, "maxontime")->valuefloat;
        bool useshygrometer = aJson.getObjectItem(device, "usershygrometer")->valuebool;
        int hygrometerindex = aJson.getObjectItem(device, "hygrometerindex")->valueint;
        manager->getPumpManager().AddPump(index, maxontime, useshygrometer, hygrometerindex);
        
        aJson.addNumberToObject(returnValue, "response", INSERT_PUMP_SUCCESS);
    }

    else
        aJson.addNumberToObject(returnValue, "error", WRONG_TYPE_ERROR);
    
    return aJson.print(returnValue);
}

char *MessageParser::Modify(aJsonObject *root)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, "devicetype");
    aJsonObject *device = aJson.getObjectItem(root, "device");
    aJsonObject *returnValue = aJson.createObject();
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_TYPE_ERROR);
        return aJson.print(returnValue);
    }

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (!manager->getSensorManager().hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", SENSOR_DOESNT_EXIST_ERROR);
            return aJson.print(returnValue);
        }
    
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (!manager->getPumpManager().hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", PUMP_DOESNT_EXIST_ERROR);
            return aJson.print(returnValue);
        }
    
    }
    
    else
        aJson.addNumberToObject(returnValue, "error", WRONG_TYPE_ERROR);
    
    return aJson.print(returnValue);
}

char *MessageParser::Remove(aJsonObject *root)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, "devicetype");
    aJsonObject *device = aJson.getObjectItem(root, "device");
    aJsonObject *returnValue = aJson.createObject();
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_TYPE_ERROR);
        return aJson.print(returnValue);
    }

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (!manager->getSensorManager().hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", SENSOR_DOESNT_EXIST_ERROR);
            return aJson.print(returnValue);
        }
        
        int response = manager->getSensorManager().RemoveSensor(index);
        
        if (response) aJson.addNumberToObject(returnValue, "response", REMOVE_SENSOR_SUCCESS);
        else if (!response) aJson.addNumberToObject(returnValue, "error", SENSOR_DOESNT_EXIST_ERROR); // Shouldn't happen because we check that the sensor exists, but handle anyways.
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (!manager->getPumpManager().hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", PUMP_DOESNT_EXIST_ERROR);
            return aJson.print(returnValue);
        }
        
        int response = manager->getPumpManager().RemovePump(index);
        
        if (response) aJson.addNumberToObject(returnValue, "response", REMOVE_PUMP_SUCCESS);
        else if (!response) aJson.addNumberToObject(returnValue, "error", PUMP_DOESNT_EXIST_ERROR); // Shouldn't happen because we check that the sensor exists, but handle anyways.
    }
    
    else
        aJson.addNumberToObject(returnValue, "error", WRONG_TYPE_ERROR);
    
    return aJson.print(returnValue);
}
