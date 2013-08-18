#include "Manager.h"

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
    char *c;
    char *response;
    //String c = "";    
    //String response = "";

    if (_client)
    {
        while (_client.connected())
        {
            int i = 0;

            while (_client.available() && i <= LIMIT)
            {
                // Fill the buffer or read all the data client has received.
                c[i++] = _client.read();
            }
            
            // If we received a message, try to execute it.
            if (i > 0) response = parser.Execute(c, this);
            
            if (response != "")
            {
                _client.println(response);
                _client.flush();
            }
            
            _client.stop();
            break;
        }
    }
}

/*
* OK I understand this routine is TERRIBLE to figure out, but it works! Here be dragons.
* Basically it evaluates the incoming message so it's protocol compliant and finally at the
* end of each message performs the corresponding routine that is defined by the protocol.
*/
/*
void Manager::ExecuteCommand(unsigned long currentTime, buffer c)
{
    if (c.c[0] == READ)
    {
        String msg = "";
        msg += "r s ";
        msg += c.c[1];
        msg += doubleToString(sensorManager.getReading(c.c[1])).c;
        SendMessage(msg);
    }

    // Just debug code to see there aren't any memory leaks. Get rid of MemoryFree in the end.
    else if (c.c[0] == 't')
    {
        SendMessage(freeMemory());
    }

    else if (c.c[0] == WRITE)
    {
        if (relay.hasIndex(c.c[1]))
        {
            if (pumpManager.hasIndex(c.c[1]))
            {
                int i = relay.switchOneRelay(c.c[1]);
                
                if (pumpManager.getPump(c.c[1]).getUsesHygrometer())
                    sensorManager.setLastReadingTime(pumpManager.getPump(c.c[1]).getHygrometerIndex(), currentTime);

                if (i == -1)
                {
                    //char *msg = "Starting pumps failed";
                    String msg = "";
                    msg += "w p ";
                    msg += c.c[1];
                    msg += " f";
                    SendMessage(msg);
                }
                  
                if (pumpManager.getPump(c.c[1]).getIsRunning())
                {
                    pumpManager.setIsRunning(c.c[1], false);
                    String msg = "";
                    msg += "w p ";
                    msg += c.c[1];
                    msg += " d";
                    //char *msg = "Pump stopped";
                    SendMessage(msg);
                }

                else
                {
                    pumpManager.setIsRunning(c.c[1], true);
                    String msg = "";
                    msg += "w p ";
                    msg += c.c[1];
                    msg += " e";
                    //char *msg = "Pump started";
                    SendMessage(msg);
                }

                pumpManager.setStartTime(c.c[1], currentTime);
            }
            
            else
            {
                int i = relay.switchOneRelay(c.c[1]);
                
                if (i == -1)
                {
                    //char *msg = "Couldn't find relay";
                    String msg = "";
                    msg += "w r ";
                    msg += c.c[1];
                    msg += " f";
                    SendMessage(msg);
                }
                
                else
                {
                    if (relay.getState(c.c[1]) == true)
                    {
                        //char *msg = "Toggled relay on";
                        String msg = "";
                        msg += "w r ";
                        msg += c.c[1];
                        msg += " e";
                        SendMessage(msg);
                    }
                    
                    else
                    {
                        //char *msg = "Toggled relay off";
                        String msg = "";
                        msg += "w r ";
                        msg += c.c[1];
                        msg += " d";
                        SendMessage(msg);
                    }
                }
            }
        }
    }
    
    else if (c.c[0] == INSERT)
    {
        int index = (int)c.c[1];
        
        if (sensorManager.hasIndex(index) || pumpManager.hasIndex(index))
        {
            //char *msg = "Couldn't insert device: Duplicate entry";
            String msg = "";
            msg += "i ";
            msg += c.c[2] + " ";
            msg += c.c[1];
            msg += " f";
            SendMessage(msg);
        }
        
        else if (c.c[2] == SENSOR)
        {
            if (c.c[3] != *"")
            {
                int type = (int)c.c[3]-48;
                
                if (c.c[4] != *"")
                {
                    int howManyToRead = ((int)c.c[4])-48;
                    int nextIndex = 5 + howManyToRead;
                    int loThreshold = 0;
                    int j = 1;
                    
                    for (int i = 4 + howManyToRead; i > 4; i--)
                    {
                        loThreshold += ((int)c.c[i]-48)*j;
                        j *= 10;
                    }

                    if (c.c[nextIndex] != *"")
                    {
                        int howManyToRead2 = ((int)c.c[nextIndex])-48;
                        int hiThreshold = 0;
                        j = 1;

                        for (int i = nextIndex + howManyToRead2; i > nextIndex; i--)
                        {
                            hiThreshold += ((int)c.c[i]-48)*j;
                            j *= 10;
                        }

                        sensorManager.AddSensor(index, type, loThreshold, hiThreshold);
                        //char *msg = "Added sensor with thresholds";
                        String msg = "";
                        msg += "i s ";
                        msg += c.c[1];
                        msg += " e";
                        SendMessage(msg);
                    }

                    else
                    {
                        sensorManager.AddSensor(index, type, loThreshold);
                        //char *msg = "Added sensor with low threshold";
                        String msg = "";
                        msg += "i s ";
                        msg += c.c[1];
                        msg += " e";
                        SendMessage(msg);
                    }
                }
                
                else
                {
                    sensorManager.AddSensor(index, type);
                    //char *msg = "Added sensor";
                    String msg = "";
                    msg += "i s ";
                    msg += c.c[1];
                    msg += " e";
                    SendMessage(msg);
                }
            }
            
            else
            {
                sensorManager.AddSensor(index);
                //char *msg = "Added sensor";
                String msg = "";
                msg += "i s ";
                msg += c.c[1];
                msg += " e";
                SendMessage(msg);
            }
        }
        
        else if (c.c[2] == PUMP)
        {
            if (c.c[3] != *"")
            {
                int howManyToRead = ((int)c.c[3])-48;
                int nextIndex = 4 + howManyToRead;
                unsigned long maxOnTime = 0;
                int j = 1;
                    
                for (int i = 3 + howManyToRead; i > 3; i--)
                {
                    maxOnTime += ((int)c.c[i]-48)*j;
                    j *= 10;
                }
                
                maxOnTime *= 1000; // Convert from seconds to milliseconds.
                
                if (c.c[nextIndex] != *"")
                {
                    int usesHygrometer = ((int)c.c[nextIndex]-48);
                    
                    if (usesHygrometer == 1 && c.c[nextIndex+1] != *"")
                    {
                        pumpManager.AddPump(index, maxOnTime, true, (int)c.c[nextIndex+1]);
                        //char *msg = "Added pump with hygrometer";
                        String msg = "";
                        msg += "i p ";
                        msg += c.c[1];
                        msg += " e";
                        SendMessage(msg);
                    }

                    else
                    {
                        pumpManager.AddPump(index, maxOnTime);
                        //char *msg = "Added pump with max on time";
                        String msg = "";
                        msg += "i p ";
                        msg += c.c[1];
                        msg += " e";
                        SendMessage(msg);
                    }
                }

                else
                {
                    pumpManager.AddPump(index, maxOnTime);
                    //char *msg = "Added pump with max on time";
                    String msg = "";
                    msg += "i p ";
                    msg += c.c[1];
                    msg += " e";
                    SendMessage(msg);
                }
            }
            
            else
            {
                pumpManager.AddPump(index);
                //char *msg = "Added pump";
                String msg = "";
                msg += "i p ";
                msg += c.c[1];
                msg += " e";
                SendMessage(msg);
            }
        }
    }
    
    else if (c.c[0] == MODIFY)
    {
        int index = (int)c.c[1];
        
        if (!sensorManager.hasIndex(index) && !pumpManager.hasIndex(index))
        {
            //char *msg = "Couldn't modify device: Device not found";
            String msg = "";
            msg += "m s ";
            msg += c.c[1];
            msg += " f";
            SendMessage(msg);
        }
        
        else if (c.c[2] == SENSOR)
        {
            if (c.c[3] == REMOVE)
            {
                if (sensorManager.RemoveSensor(index))
                {
                    //char *msg = "Removed sensor";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " e r";
                    SendMessage(msg);
                }
                
                else
                {
                    //char *msg = "Couldn't remove sensor";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " f r";
                    SendMessage(msg);
                }
            }
        
            else if (c.c[3] == HIGH_THRESHOLD)
            {
                int howManyToRead = ((int)c.c[4])-48;
                int hiThreshold = 0;
                int j = 1;
                    
                for (int i = 4 + howManyToRead; i > 4; i--)
                {
                    hiThreshold += ((int)c.c[i]-48)*j;
                    j *= 10;
                }
                
                if (sensorManager.setHighThresholdValue(index, hiThreshold))
                {
                    //char *msg = "Successfully changed high treshold value";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " e h";
                    SendMessage(msg);
                }
                
                else
                {
                    //char *msg = "Couldn't change high treshold value";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " f h";
                    SendMessage(msg);
                }
            }
            
            else if (c.c[3] == LOW_THRESHOLD)
            {
                int howManyToRead = ((int)c.c[4])-48;
                int loThreshold = 0;
                int j = 1;
                    
                for (int i = 4 + howManyToRead; i > 4; i--)
                {
                    loThreshold += ((int)c.c[i]-48)*j;
                    j *= 10;
                }
                
                if (sensorManager.setLowThresholdValue(index, loThreshold))
                {
                    //char *msg = "Successfully changed low treshold value";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " e l";
                    SendMessage(msg);
                }
                
                else
                {
                    //char *msg = "Couldn't change low treshold value";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " f l";
                    SendMessage(msg);
                }
            }
            
            else if (c.c[3] == TYPE)
            {
                int type = ((int)c.c[4])-48;
                
                if (sensorManager.setType(index, type))
                {
                    //char *msg = "Successfully changed type";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " e t";
                    SendMessage(msg);
                }
                
                else
                {
                    //char *msg = "Couldn't change type";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " f t";
                    SendMessage(msg);
                }
            }
            
            else if (c.c[3] == INDEX)
            {
                int newIndex = ((int)c.c[4])-48;
                
                if (sensorManager.setIndex(index, newIndex))
                {
                    //char *msg = "Successfully changed index";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " e i";
                    SendMessage(msg);
                }
                
                else
                {
                    //char *msg = "Couldn't change index";
                    String msg = "";
                    msg += "m s ";
                    msg += c.c[1];
                    msg += " f i";
                    SendMessage(msg);
                }
            }
        }
        
        else if (c.c[2] == PUMP)
        {
            if (c.c[3] == REMOVE)
            {
                if (pumpManager.RemovePump(index))
                {
                    //char *msg = "Removed pump";
                    String msg = "";
                    msg += "m p ";
                    msg += c.c[1];
                    msg += " e r";
                    SendMessage(msg);
                }
                
                else
                {
                    //char *msg = "Couldn't remove pump";
                    String msg = "";
                    msg += "m p ";
                    msg += c.c[1];
                    msg += " f r";
                    SendMessage(msg);
                }
            }
            
            else if (c.c[3] == MAXONTIME)
            {
                int howManyToRead = ((int)c.c[4])-48;
                int maxOnTime = 0;
                int j = 1;
                    
                for (int i = 4 + howManyToRead; i > 4; i--)
                {
                    maxOnTime += ((int)c.c[i]-48)*j;
                    j *= 10;
                }

                if (pumpManager.setMaxOnTime(index, maxOnTime))
                {
                    //char *msg = "Changed max on time";
                    String msg = "";
                    msg += "m p ";
                    msg += c.c[1];
                    msg += " e m";
                    SendMessage(msg);
                }
                
                else
                {
                    //char *msg = "Couldn't change max on time";
                    String msg = "";
                    msg += "m p ";
                    msg += c.c[1];
                    msg += " f m";
                    SendMessage(msg);
                }
            }
             
            else if (c.c[3] == USESHYGROMETER)
            {
                int usesHygrometer = ((int)c.c[4])-48;
                
                if (usesHygrometer == 1 || usesHygrometer == 0)
                {
                    if (pumpManager.setUsesHygrometer(index, usesHygrometer))
                    {
                        //char *msg = "Changed usesHygrometer";
                        String msg = "";
                        msg += "m p ";
                        msg += c.c[1];
                        msg += " e u";
                        SendMessage(msg);
                    }
                    
                    else
                    {
                        //char *msg = "Couldn't change usesHygrometer";
                        String msg = "";
                        msg += "m p ";
                        msg += c.c[1];
                        msg += " f u";
                        SendMessage(msg);
                    }
                }
                
                else
                {
                    //char *msg = "Couldn't change usesHygrometer";
                    String msg = "";
                    msg += "m p ";
                    msg += c.c[1];
                    msg += " f u";
                    SendMessage(msg);
                }
            }
             
            else if (c.c[3] == HYGROMETERINDEX)
            {
                int hygrometerIndex = ((int)c.c[4])-48;

                if (pumpManager.setHygrometerIndex(index, hygrometerIndex))
                {
                    //char *msg = "Changed hygrometerIndex";
                    String msg = "";
                    msg += "m p ";
                    msg += c.c[1];
                    msg += " e g";
                    SendMessage(msg);
                }
                    
                else
                {
                    //char *msg = "Couldn't change hygrometerIndex";
                    String msg = "";
                    msg += "m p ";
                    msg += c.c[1];
                    msg += " f g";
                    SendMessage(msg);
                }
            }
        }
    }
    
    else if ((c.c[0] == SETUP_START && !isSetupRun) || c.c[0] == FORCE_SETUP)
    {
        isSetupRun = false;
        //char *msg = "Accepting setup parameters";
        String msg = "";
        msg += "{";
        SendMessage(msg);
        
        // Run setup routine until server tells us we're ready to go.
        while (true)
        {
            c = ReadCommand();

            if (c.c[0] == SETUP_END) break;

            else if (c.c[0] != *"" && (c.c[0] == INSERT || c.c[0] == MODIFY))
            {
                timer.Update();
                ExecuteCommand(timer.getCurrentTime(), c);
            }
            
            else if (c.c[0] == FORCE_SETUP || c.c[0] == SETUP_START)
            {
                //char *msg = "Setup is already running";
                msg = "{ r";
                SendMessage(msg);
            }

            delay(10);
        };
        
        isSetupRun = true;
        //msg = "Setup is ready";
        msg = "}";
        SendMessage(msg);
    }
    
    else if (c.c[0] == SETUP_START && isSetupRun)
    {
        //char *msg = "Setup has already ran";
        String msg = "}r";
        SendMessage(msg);
    }
    
    else if (c.c[0] == SETUP_END)
    {
        //char *msg = "Setup isn't running";
        String msg = "}{";
        SendMessage(msg);
    }
    
    else
    {
        //char *msg = "Didn't recognise command";
        String msg = "u";
        SendMessage(msg);
    }
}
*/
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
                    
                    //char *msg = "Pump stopped";
                    String msg = "";
                    msg += "w p ";
                    msg += char(pump.getIndex());
                    msg += " d";
                    SendMessage(msg);
                }
            }
            
            else
            {
                if ((currentTime - pump.getStartTime()) > pump.getMaxOnTime())
                {
                    relay.switchOneRelay(pump.getIndex());
                    pumpManager.setIsRunning(_pumpIndex[i], false);
                    
                    //char *msg = "Pump stopped";
                    String msg = "";
                    msg += "w p ";
                    msg += char(pump.getIndex());
                    msg += " d";
                    SendMessage(msg);

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
    if (client.connect(SERVER_IP, SERVER_PORT))
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
    if (client.connect(SERVER_IP, SERVER_PORT))
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
    if (client.connect(SERVER_IP, SERVER_PORT))
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
    if (client.connect(SERVER_IP, SERVER_PORT))
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
    if (client.connect(SERVER_IP, SERVER_PORT))
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
    if (client.connect(SERVER_IP, SERVER_PORT))
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
    if (client.connect(SERVER_IP, SERVER_PORT))
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
