#include "MessageParser.h"

#include <aJSON.h>

#include "Manager.h"

char *MessageParser::Execute(char *message, Manager *manager)
{
    aJsonObject *root = MessageParser::toJson(message);
    
    if (root != NULL)
    {
        aJsonObject *command = aJson.getObjectItem(root, "command");
        
        if (command != NULL)
        {
            if (command->valueint == SEND_READ)
                return MessageParser::Read(aJson.getObjectItem(root, "sensor"), manager);
            
            else if (command->valueint == SEND_WRITE)
                return MessageParser::Run(aJson.getObjectItem(root, "device"), manager);
                
            else if (command->valueint == SEND_ENABLE)
                return MessageParser::Run(aJson.getObjectItem(root, "device"), manager, SEND_ENABLE);
                
            else if (command->valueint == SEND_DISABLE)
                return MessageParser::Run(aJson.getObjectItem(root, "device"), manager, SEND_DISABLE);
                
            else if (command->valueint == SEND_INSERT)
                return MessageParser::Insert(aJson.getObjectItem(root, "device"), manager);
                
            else if (command->valueint == SEND_MODIFY)
                return MessageParser::Modify(aJson.getObjectItem(root, "device"), manager);
                
            else if (command->valueint == SEND_REMOVE)
                return MessageParser::Remove(aJson.getObjectItem(root, "device"), manager);
        }
        
        else
        {
            aJsonObject *returnObject = MessageParser::toJson(message);
            aJson.addNumberToObject(returnObject, "error", NO_COMMAND_ERROR);
            return aJson.print(root);
        }
    }
}

/*
 * Turn a char message into a JSON object.
 *
 */
aJsonObject *MessageParser::toJson(char *message)
{
    return aJson.parse(message);
}

char *MessageParser::Read(aJsonObject *object, Manager *manager)
{
    // Get the index and create an object for the return message.
    aJsonObject *index = aJson.getObjectItem(object, "index");
    aJsonObject *root = aJson.createObject();
    
    // If index isn't found, tell the sender about it.
    if (index == NULL)
    {
        aJson.addNumberToObject(root, "error", NO_INDEX_ERROR);
        return aJson.print(root);
    }
    
    // Get the reading and write it to the object. Then write a success to the response.
    aJson.addNumberToObject(root, "reading", manager->getSensorManager().getReading(index->valueint));
    aJson.addNumberToObject(root, "response", READ_SENSOR_SUCCESS);
    
    return aJson.print(root);
}

char *MessageParser::Run(aJsonObject *object, Manager *manager, int commandType = SEND_WRITE)
{
    aJsonObject *index = aJson.getObjectItem(object, "index");
    aJsonObject *root = aJson.createObject();
    
    if (index == NULL)
    {
        aJson.addNumberToObject(root, "error", NO_INDEX_ERROR);
        return aJson.print(root);
    }

    // Check if the given index exists in the managers.
    if (manager->getPumpManager().hasIndex(index->valueint) || manager->getRelayManager().hasIndex(index->valueint))
    {
        // Toggle relay state if a) it's a write command, b) it's an enable command and relay is off,
        // c) it's a disable command and relay is on.
        if (SEND_WRITE || (commandType == SEND_ENABLE && !manager->getRelayManager.getState(index->valueint)) || (commandType == SEND_DISABLE && manager->getRelayManager.getState(index->valueint)))
            aJson.addNumberToObject(root, "state", manager->getRelayManager.switchOneRelay(index->valueint));
            
        if (manager->getPumpManager().hasIndex(index->valueint) && manager->getPumpManager().getPump(index->valueint).getUsesHygrometer())
            manager->getSensorManager().setLastReadingTime(manager->getPumpManager().getPump(index->valueint).getHygrometerIndex(), manager->getTimer().getCurrentTime());
    }
    
    else
        aJson.addNumberToObject(root, "error", NO_DEVICE_ERROR);
    
    aJson.addNumberToObject(root, "response", RUN_DEVICE_SUCCESS);
    
    return aJson.print(root);
}

char *MessageParser::Insert(aJsonObject *object, Manager *manager)
{
    aJsonObject *deviceType = aJson.getObjectItem(object, "type");
    aJsonObject *device = aJson.getObjectItem(object, "device");
    aJsonObject *root = aJson.createObject();
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(root, "error", NO_TYPE_ERROR);
        return aJson.print(root);
    }

    if (deviceType == "sensor")
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (manager->getSensorManager()->hasIndex(index->valueint))
        {
            aJson.addNumberToObject(root, "error", SENSOR_EXISTS_ERROR);
            return aJson.print(root);
        }
        
        int type = aJson.getObjectItem(device, "type")->valueint;
        int lowthreshold = aJson.getObjectItem(device, "lowthreshold")->valuefloat;
        double highthreshold = aJson.getObjectItem(device, "highthreshold")->valuefloat;
        manager->getSensorManager()->AddSensor(index, type, lowthreshold, highthreshold);
        
        aJson.addNumberToObject(root, "response", INSERT_SENSOR_SUCCESS);
    }
    
    else if (deviceType == "pump")
    {
        int index = aJson.getObjectItem(device, "index")->valueint;
        
        if (manager->getPumpManager()->hasIndex(index->valueint))
        {
            aJson.addNumberToObject(root, "error", PUMP_EXISTS_ERROR);
            return aJson.print(root);
        }
        
        unsigned long maxontime = (unsigned long)aJson.getObjectItem(device, "maxontime")->valuefloat;
        bool usershygrometer = aJson.getObjectItem(device, "usershygrometer")->valuebool;
        int hygrometerindex = aJson.getObjectItem(device, "hygrometerindex")->valueint;
        manager->getSensorManager()->AddPump(index, maxontime, useshygrometer, hygrometerindex);
        
        aJson.addNumberToObject(root, "response", INSERT_PUMP_SUCCESS);
    }

    else
        aJson.addNumberToObject(root, "error", WRONG_TYPE_ERROR);
    
    return aJson.print(root);
}

char *MessageParser::Modify(aJsonObject *object, Manager *manager)
{
    aJsonObject *deviceType = aJson.getObjectItem(object, "type");
    aJsonObject *device = aJson.getObjectItem(object, "device");
    aJsonObject *root = aJson.createObject();
    
    if (deviceType == NULL)
    {
        aJson.addNumberToObject(root, "error", NO_TYPE_ERROR);
        return aJson.print(root);
    }

    if (deviceType == "sensor")
    {
    
    }
    
    else if (deviceType == "pump")
    {
    
    }
    
    else
        aJson.addNumberToObject(root, "error", WRONG_TYPE_ERROR);
    
    return aJson.print(root);
}

char *MessageParser::Remove(aJsonObject *object, Manager *manager)
{

}
