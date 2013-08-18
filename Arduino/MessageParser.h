#ifndef messageparser_h
#define messageparser_h

// The protocol constants. THINK OF BETTER VALUES!
const int NO_COMMAND_ERROR = 1;
const int NO_INDEX_ERROR = 2;
const int NO_DEVICE_ERROR = 3;
const int NO_TYPE_ERROR = 4;
const int WRONG_TYPE_ERROR = 5;

const int SENSOR_EXISTS_ERROR = 50;
const int PUMP_EXISTS_ERROR = 51;

const int READ_SENSOR_SUCCESS = 102;
const int RUN_DEVICE_SUCCESS = 103;
const int INSERT_SENSOR_SUCCESS = 100;
const int INSERT_PUMP_SUCCESS = 101;

const int SEND_READ = 200;
const int SEND_WRITE = 201;
const int SEND_INSERT = 202;
const int SEND_MODIFY = 203;
const int SEND_ENABLE = 204;
const int SEND_DISABLE = 205;
const int SEND_REMOVE = 206;

class aJsonObject;
class Manager;

class MessageParser
{
private:
    aJsonObject *toJson(char *message);
    char *Read(aJsonObject *object, Manager *manager);
    char *Run(aJsonObject *object, Manager *manager);
    char *Insert(aJsonObject *object, Manager *manager);
    char *Modify(aJsonObject *object, Manager *manager);
    char *Remove(aJsonObject *object, Manager *manager);
    
public:
    //MessageParser(Manager *_manager) {manager = _manager;};
    //~MessageParser() {delete[] manager;};
    
    char *Execute(char *message, Manager *manager);
};

#endif
