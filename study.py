import seriaaaaal

def openSerial(port, baudrate=115200, bytesize=seriaaaaal.EIGHTBITS, parity=seriaaaaal.PARITY_NONE, stopbits=seriaaaaal.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False):
    ser = seriaaaaal.Serial()

    ser.port = port
    ser.baudrate = baudrate
    ser.bytesize = bytesize
    ser.parity = parity
    ser.stopbits = stopbits
    ser.timeout = timeout
    ser.xonxoff = xonxoff
    ser.rtscts = rtscts
    ser.dsrdtr = dsrdtr

    ser.open()
    return ser
    
def writePort(ser, data):
    ser.write(data)

def writePortUnicode(ser, data):
    writePort(ser, data.encode())

def read(ser, size=1, timeout=None):
    ser.timeout = timeout
    readed = ser.read(size)
    return readed

def readUntilExitCode(ser, exitcode=b'\x03'):
    readed = b''
    while True:
        data = ser.read()
        print(data)
        readed += data
        if exitcode in data:
            return readed[:1]


def readEOF(ser):
    readed = ser.readline()
    return readed[:-1]
 

if __name__ == '__main__':
    ser = openSerial('COM3')

    ser.open()
    string = 'hello world\r\n'
    writePort(ser, string)
    writePort(ser, string.encode())
    writePortUnicode(ser, string)

    string = b'Hello World\r\n'
    writePort(ser, string)

    string = '한글 전송 테스트\r\n'
    writePortUnicode(ser, string)

    readed = read(ser)
    print(readed)
    print(read(ser, 10))
    print(read(ser, size=3, timeout=5))
    print(readEOF(ser))
    print(readUntilExitCode(ser))