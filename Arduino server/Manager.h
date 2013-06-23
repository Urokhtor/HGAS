#ifndef manager_h
#define manager_h

#include <SPI.h>
#include <Ethernet.h>

#include "Arduino.h"
#include "MemoryFree.h"

#include "MessageParser.h"
#include "Timer.h"
#include "Relay.h"
#include "Sensor.h"

// ATM the relays I'm using is just a relay board of 8 relays. This const is used to tell
// the initialization routine to initialize 8 relays, starting from port 40.
const int RELAY_START_INDEX = 40;

const unsigned long _PUMP_MAX_ON_TIME = 100000; // 140 seconds. Max on time allowed for pumps.
const unsigned long WATER_LEVEL_MEASUREMENT_INTERVAL = 1000; // One second.
const int HUMIDITY_TRESHOLD = 400; // The treshold value when pumps need to be shut down.

// Command interface:
// First byte. Type of operation, read sensor data, control relays or modify sensor/device.
const char READ = 'r';
const char WRITE = 'w';
const char INSERT = 'i'; // Insert a sensor or a pump.
const char MODIFY = 'm'; // Modify sensor or pump properties.
const char FORCE_SETUP = 'f'; // Force to take in setup.
const char SETUP_START = '{'; // Tells that we need to get ready accepting setup parameters or tell setup is already run.
const char SETUP_END = '}'; // Tells us that setup ready and we can start our normal routines.

// Third byte. Only with write operation. Enable or disable relay.
const char ENABLE = 'e';
const char DISABLE = 'd';
const char SENSOR = 's'; // Used with INSERT or MODIFY.
const char PUMP = 'p'; // Used with INSERT or MODIFY.

// Fourth byte. Used with modifying sensors or pumps.
const char REMOVE = 'r';
const char HIGH_THRESHOLD = 'h';
const char LOW_THRESHOLD = 'l';
const char TYPE = 't';
const char INDEX = 'i';
const char MAXONTIME = 'm';
const char USESHYGROMETER = 'u';
const char HYGROMETERINDEX = 'g';

const int LIMIT = 512; // Command buffer length.

// The command buffer.
struct buffer
{
    char c[LIMIT];
};

static byte MAC[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED}; // This is board specific MAC, user should not be able to change it.
const char SERVER_IP[] = "192.168.11.33"; // Address of the server we communicate with.
const int SERVER_PORT = 48371; // Which port the receiving server listens.

class Manager
{
private:
    EthernetServer *server;
    EthernetClient client;
    IPAddress IP;
    MessageParser parser;
    Timer timer;
    RelayManager relay;
    SensorManager sensorManager;
    PumpManager pumpManager;
    boolean isSetupRun;
    
    void ReadCommand(); // Checks for pending ingoing sockets and then reads the message.
    void HandlePumps(unsigned long currentTime); // Loops through pumpManager and performs according routines.

    // Message interface for communicating back to the server.
    void SendMessage(char *c);
    void SendMessage(const char *c);
    void SendMessage(String s);
    void SendMessage(double d, unsigned int mantissa = 2);
    void SendMessage(int i, int base = DEC);
    void SendMessage(unsigned int i, int base = DEC);
    void SendMessage(long l, int base = DEC);
    void SendMessage(unsigned long l, int base = DEC);

    buffer doubleToString(double d, unsigned int mantissa = 2);
    
public:
    Manager(EthernetServer *_server, IPAddress _IP);
    void Initialize();
    void Update();
    
    EthernetServer *getServer();
    IPAddress getLocalIP();
	SensorManager *getSensorManager() {return &sensorManager;}
    PumpManager *getPumpManager() {return &pumpManager;}
    RelayManager *getRelayManager() {return &relay;}
    Timer *getTimer() {return &timer;}
};

#endif
