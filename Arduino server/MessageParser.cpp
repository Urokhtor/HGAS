#include "MessageParser.h"

#include <aJSON.h>

#include "Manager.h"

void MessageParser::Execute(aJsonObject *root, char *tmp)
{
    aJsonObject *returnObject = aJson.createObject();
    //char *tmp;
    
    if (root != NULL)
    {
        aJsonObject *command = aJson.getObjectItem(root, "command");
        
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
            
            else
                aJson.addNumberToObject(returnObject, "error", UNRECOGNISED_COMMAND_ERROR);
        }
        
        else
            aJson.addNumberToObject(returnObject, "error", NO_COMMAND_ERROR);
            
        delete command;
    }
    
    tmp = aJson.print(returnObject);
    delete root;
    delete returnObject;
    
    //return tmp;
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
    aJsonObject *index = aJson.getObjectItem(root, "index");
    
    // If index isn't found, tell the sender about it.
    if (index == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_INDEX_ERROR);
        //return aJson.print(returnValue);
        return;
    }
    
    // Get the reading and write it to the object. Then write a success to the response.
    aJson.addNumberToObject(returnValue, "reading", manager->getSensorManager()->getReading(index->valueint));
    aJson.addNumberToObject(returnValue, "response", READ_SENSOR_SUCCESS);
    
    delete index;
    
    //return aJson.print(returnValue);
}

void MessageParser::Run(aJsonObject *root, aJsonObject *returnValue, int commandType)
{
    aJsonObject *index = aJson.getObjectItem(root, "index");
    
    if (index == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_INDEX_ERROR);
        //return aJson.print(returnValue);
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
            aJson.addNumberToObject(returnValue, "state", response);
        }
        
        else
        {
            aJson.addNumberToObject(returnValue, "response", NO_ACTION_NEEDED);
            //return aJson.print(returnValue);
            delete index;
            return;
        }
        
        if (manager->getPumpManager()->hasIndex(index->valueint))
        {
            manager->getPumpManager()->setIsRunning(index->valueint, true);
            manager->getPumpManager()->setStartTime(index->valueint, manager->getTimer()->getCurrentTime());
        }
        
        aJson.addNumberToObject(returnValue, "response", RUN_DEVICE_SUCCESS);
    }
    
    else
        aJson.addNumberToObject(returnValue, "error", NO_DEVICE_ERROR);
    
    delete index;

    //return aJson.print(returnValue);
}

void MessageParser::Insert(aJsonObject *root, aJsonObject *returnValue)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, "devicetype");
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_TYPE_ERROR);
        //return aJson.print(returnValue);
        return;
    }
    
    aJsonObject *device = aJson.getObjectItem(root, "device");

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (manager->getSensorManager()->hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", SENSOR_EXISTS_ERROR);
            //return aJson.print(returnValue);
            delete deviceType;
            delete device;
            return;
        }
        
        int type = aJson.getObjectItem(device, "type")->valueint;
        int lowthreshold = aJson.getObjectItem(device, "lowthreshold")->valuefloat;
        double highthreshold = aJson.getObjectItem(device, "highthreshold")->valuefloat;
        manager->getSensorManager()->AddSensor(index, type, lowthreshold, highthreshold);
        
        aJson.addNumberToObject(returnValue, "response", INSERT_SENSOR_SUCCESS);
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (manager->getPumpManager()->hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", PUMP_EXISTS_ERROR);
            //return aJson.print(returnValue);
            delete deviceType;
            delete device;
            return;
        }
        
        unsigned long maxontime = (unsigned long)aJson.getObjectItem(device, "maxontime")->valuefloat;
        bool useshygrometer = aJson.getObjectItem(device, "usershygrometer")->valuebool;
        int hygrometerindex = aJson.getObjectItem(device, "hygrometerindex")->valueint;
        manager->getPumpManager()->AddPump(index, maxontime, useshygrometer, hygrometerindex);
        
        aJson.addNumberToObject(returnValue, "response", INSERT_PUMP_SUCCESS);
    }

    else
        aJson.addNumberToObject(returnValue, "error", WRONG_TYPE_ERROR);
    
    delete deviceType;
    delete device;
    
    //return aJson.print(returnValue);
}

void MessageParser::Modify(aJsonObject *root, aJsonObject *returnValue)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, "devicetype");
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_TYPE_ERROR);
        //return aJson.print(returnValue);
        return;
    }
    
    aJsonObject *device = aJson.getObjectItem(root, "device");

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (!manager->getSensorManager()->hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", SENSOR_DOESNT_EXIST_ERROR);
            //return aJson.print(returnValue);
            delete deviceType;
            delete device;
            return;
        }
    
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (!manager->getPumpManager()->hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", PUMP_DOESNT_EXIST_ERROR);
            //return aJson.print(returnValue);
            delete deviceType;
            delete device;
            return;
        }
    
    }
    
    else
        aJson.addNumberToObject(returnValue, "error", WRONG_TYPE_ERROR);
    
    delete deviceType;
    delete device;
    
    //return aJson.print(returnValue);
}

void MessageParser::Remove(aJsonObject *root, aJsonObject *returnValue)
{
    aJsonObject *deviceType = aJson.getObjectItem(root, "devicetype");
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(returnValue, "error", NO_TYPE_ERROR);
        //return aJson.print(returnValue);
        return;
    }
    
    aJsonObject *device = aJson.getObjectItem(root, "device");

    if (deviceType->valueint == TYPE_SENSOR)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (!manager->getSensorManager()->hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", SENSOR_DOESNT_EXIST_ERROR);
            //return aJson.print(returnValue);
            delete deviceType;
            delete device;
            return;
        }
        
        int response = manager->getSensorManager()->RemoveSensor(index);
        
        if (response) aJson.addNumberToObject(returnValue, "response", REMOVE_SENSOR_SUCCESS);
        else if (!response) aJson.addNumberToObject(returnValue, "error", SENSOR_DOESNT_EXIST_ERROR); // Shouldn't happen because we check that the sensor exists, but handle anyways.
    }
    
    else if (deviceType->valueint == TYPE_PUMP)
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (!manager->getPumpManager()->hasIndex(index))
        {
            aJson.addNumberToObject(returnValue, "error", PUMP_DOESNT_EXIST_ERROR);
            //return aJson.print(returnValue);
            delete deviceType;
            delete device;
            return;
        }
        
        int response = manager->getPumpManager()->RemovePump(index);
        
        if (response) aJson.addNumberToObject(returnValue, "response", REMOVE_PUMP_SUCCESS);
        else if (!response) aJson.addNumberToObject(returnValue, "error", PUMP_DOESNT_EXIST_ERROR); // Shouldn't happen because we check that the sensor exists, but handle anyways.
    }
    
    else
        aJson.addNumberToObject(returnValue, "error", WRONG_TYPE_ERROR);
    
    delete deviceType;
    delete device;
    
    //return aJson.print(returnValue);
}
