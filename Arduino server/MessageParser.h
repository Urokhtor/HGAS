#ifndef messageparser_h
#define messageparser_h

// The protocol constants. THINK OF BETTER VALUES!
const int NO_COMMAND_ERROR = 1;
const int NO_INDEX_ERROR = 2;
const int NO_DEVICE_ERROR = 3;
const int NO_TYPE_ERROR = 4;
const int WRONG_TYPE_ERROR = 5;
const int UNRECOGNISED_COMMAND_ERROR = 6;

const int SENSOR_EXISTS_ERROR = 50;
const int PUMP_EXISTS_ERROR = 51;
const int SENSOR_DOESNT_EXIST_ERROR = 52;
const int PUMP_DOESNT_EXIST_ERROR = 53;

const int INSERT_SENSOR_SUCCESS = 100;
const int INSERT_PUMP_SUCCESS = 101;
const int READ_SENSOR_SUCCESS = 102;
const int RUN_DEVICE_SUCCESS = 103;
const int REMOVE_SENSOR_SUCCESS = 104;
const int REMOVE_PUMP_SUCCESS = 105;
const int NO_ACTION_NEEDED = 106;

const int SEND_READ = 200;
const int SEND_WRITE = 201;
const int SEND_INSERT = 202;
const int SEND_MODIFY = 203;
const int SEND_ENABLE = 204;
const int SEND_DISABLE = 205;
const int SEND_REMOVE = 206;

const int TYPE_SENSOR = 300;
const int TYPE_PUMP = 301;

class aJsonObject;
class Manager;

class MessageParser
{
private:
    Manager *manager;
    
    void Read(aJsonObject *object, aJsonObject *returnObject);
    void Run(aJsonObject *object, aJsonObject *returnObject, int commandType = SEND_WRITE);
    void Insert(aJsonObject *object, aJsonObject *returnObject);
    void Modify(aJsonObject *object, aJsonObject *returnObject);
    void Remove(aJsonObject *object, aJsonObject *returnObject);
    
public:
    //MessageParser(Manager *_manager) {manager = _manager;};
    //~MessageParser() {delete[] manager;};
    
    void Execute(aJsonObject *root, char *response);
    aJsonObject *toJson(char message[]);
    void SetManager(Manager *_manager);
};

#endif
