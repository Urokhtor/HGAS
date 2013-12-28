#include "Manager.h"
#include <aJSON.h>

Manager::Manager(EthernetServer *_server, IPAddress _IP)
{
    server = _server;
    IP = _IP;
    parser = MessageParser::MessageParser();
}

void Manager::Initialize()
{
    Ethernet.begin(MAC, IP);
    server->begin();
    timer.Reset();
    relay.Initialize(RELAY_START_INDEX);

    sensorManager.setSize(0);
    /*sensorManager.AddSensor(A0, TEMPERATURE);
    sensorManager.AddSensor(A1, _DEFAULT, HUMIDITY_TRESHOLD);
    sensorManager.AddSensor(A2, _DEFAULT);
    sensorManager.AddSensor(A3, DHT11);*/
    
    pumpManager.setSize(0);
    /*pumpManager.AddPump(40, _PUMP_MAX_ON_TIME, true, A1);*/
    
    parser.SetManager(this);
}

EthernetServer *Manager::getServer()
{
    return server;
}

IPAddress Manager::getLocalIP()
{
    return Ethernet.localIP();
}

void Manager::Update()
{
    timer.Update();
    ReadCommand();
    HandlePumps(timer.getCurrentTime());
}

/*
* Check if there are any pending connections and read them.
*/

void Manager::ReadCommand()
{
    EthernetClient _client = server->available();
    char *response;
    char c[512];
    String sr = "";

    if (_client)
    {
        Serial.print("Free memory before: ");Serial.println(freeMemory());
        while (_client.connected())
        {
            int i = 0;
            while (_client.available() && i < LIMIT)
            {
                // Fill the buffer or read all the data client has received.
                char tmp = _client.read();
                
                if (tmp == MESSAGE_BREAK) break;
                //c[i++] = tmp;
                sr += tmp;
                i++;
            }
            
            char buf[sr.length()+1];
            sr.toCharArray(buf, sr.length()+1);
            
            // If we received a message, try to execute it.
            aJsonObject *object = aJson.parse(buf);
            
            //if (i > 0) response = parser.Execute(parser.toJson(c));
            if (i > 0) parser.Execute(object, &response);
            
            _client.println(response);
            _client.flush();
            
            // Handle memory management.
            aJson.deleteItem(object);
            free(response);
            //free(c);
            
            _client.stop();
            Serial.print("Free memory after: ");Serial.println(freeMemory());
            break;
        }
    }
}

/*
* Loop through pumps in the pump manager and update the ones that are currently running,
* stop them if needed and inform the server about it.
*/

void Manager::HandlePumps(unsigned long currentTime)
{
    int _pumpIndex[PUMP_MANAGER_SIZE];
    pumpManager.getIndexList(_pumpIndex);
    
    for (int i = 0; i < PUMP_MANAGER_SIZE; i++)
    {
        if (_pumpIndex[i] == NULL) continue;
        
        Pump pump = pumpManager.getPump(_pumpIndex[i]);
        
        if (pump.getIsRunning())
        {
            int reading = 1023; // Needs to be initialized because otherwise it might cause erratic behaviour when comparing to treshold value.
            
            // Take hygrometer reading for every passed WATER_LEVEL_MEASUREMENT_INTERVAL.
            if (pump.getUsesHygrometer() && (currentTime - sensorManager.getLastReadingTime(A1)) > WATER_LEVEL_MEASUREMENT_INTERVAL)
            {
                reading = (int)sensorManager.getReading(A1);
                sensorManager.setLastReadingTime(pump.getHygrometerIndex(), currentTime);
            }
            
            // If pump uses hygrometer, check how long pump has been running and the hygrometer treshold value.
            if (pump.getUsesHygrometer())
            {
                if ((currentTime - pump.getStartTime()) > pump.getMaxOnTime() || reading <= sensorManager.getLowThresholdValue(A1))
                {
                    relay.switchOneRelay(pump.getIndex());
                    pumpManager.setIsRunning(_pumpIndex[i], false);
                    
                    aJsonObject *response = aJson.createObject();
                    aJson.addNumberToObject(response, "response", TOGGLED_DEVICE_OFF); 
                    aJson.addNumberToObject(response, "id", pump.getId());
                    char *responseChar = aJson.print(response);
                    SendMessage(responseChar);
                    aJson.deleteItem(response);
                    free(responseChar);
                }
            }
            
            else
            {
                if ((currentTime - pump.getStartTime()) > pump.getMaxOnTime())
                {
                    relay.switchOneRelay(pump.getIndex());
                    pumpManager.setIsRunning(_pumpIndex[i], false);
                    
                    aJsonObject *response = aJson.createObject();
                    aJson.addNumberToObject(response, "response", TOGGLED_DEVICE_OFF); 
                    aJson.addNumberToObject(response, "id", pump.getId());
                    char *responseChar = aJson.print(response);
                    SendMessage(responseChar);
                    aJson.deleteItem(response);
                    free(responseChar);
                }
            }
        }
    }
}

/*
* Functions in this section open a socket to the server and send the data over Ethernet.
*/

void Manager::SendMessage(char *c)
{
    if (client.connect(SERVER_IP, SERVER_LISTEN_PORT))
    {
        if (client.connected())
        {
            client.println(c);
            
            client.flush();
            client.stop();
        }
    }
}

void Manager::SendMessage(const char *c)
{
    if (client.connect(SERVER_IP, SERVER_LISTEN_PORT))
    {
        if (client.connected())
        {
            client.println(c);
            
            client.flush();
            client.stop();
        }
    }
}

void Manager::SendMessage(String s)
{
    if (client.connect(SERVER_IP, SERVER_LISTEN_PORT))
    {
        if (client.connected())
        {
            client.println(s);
            
            client.flush();
            client.stop();
        }
    }
}

void Manager::SendMessage(int i, int base)
{
    if (client.connect(SERVER_IP, SERVER_LISTEN_PORT))
    {
        if (client.connected())
        {
            client.println(i, base);
            
            client.flush();
            client.stop();
        }
    }
}

void Manager::SendMessage(unsigned int i, int base)
{
    if (client.connect(SERVER_IP, SERVER_LISTEN_PORT))
    {
        if (client.connected())
        {
            client.println(i, base);
            
            client.flush();
            client.stop();
        }
    }
}

void Manager::SendMessage(long l, int base)
{
    if (client.connect(SERVER_IP, SERVER_LISTEN_PORT))
    {
        if (client.connected())
        {
            client.println(l, base);
            
            client.flush();
            client.stop();
        }
    }
}

void Manager::SendMessage(unsigned long l, int base)
{
    if (client.connect(SERVER_IP, SERVER_LISTEN_PORT))
    {
        if (client.connected())
        {
            client.println(l, base);
            
            client.flush();
            client.stop();
        }
    }
}

/*
* Takes a double and optionally the length of mantissa (defaults to 2 digits).
* Then we use a buffer construct to store the double's string representation.
*/

buffer Manager::doubleToString(double d, unsigned int mantissa)
{
    buffer buf;
    int length = 0;

    // We need to know what length to expect for the char buffer.
    //Otherwise expect unpredictable behavior. Perhaps expand the length in future?
    if (d < 100.0) length = 4 + mantissa;
    else if (d < 1000.0) length = 5 + mantissa;
    else if (d < 10000.0) length = 6 + mantissa;
    else if (d < 100000.0) length = 7 + mantissa;

    dtostrf(d, length, mantissa, buf.c);
    return buf;
}
