from pydantic import BaseModel, Field, conint, field_validator
from typing import Annotated, List
import serial
import sys
sys.path.append('../tp1/')
sys.path.append('../tp2/')
from Calculator import Calculator
from ejemplo import graph_example

class UART(BaseModel):
    ser: serial.serial_for_url = None

    tx_header:  Annotated[int, Field(gt=0,le=255)] = None
    tx_end_header:  Annotated[int, Field(gt=0,le=255)] = None
    tx_high_size:  Annotated[int, Field(gt=0,le=255)] = None
    tx_low_size:  Annotated[int, Field(gt=0,le=255)] = None
    tx_L: int = Field(0, ge=0, le=1) 
    tx_start_frame: int = Field(0b101, Literal=True) 
    tx_device_id: int = 0x01
    tx_size: int = 0
    tx_data: List[int] = []

    rx_header:  Annotated[int, Field(gt=0,le=255)] = None
    rx_end_header:  Annotated[int, Field(gt=0,le=255)] = None
    rx_high_size:  Annotated[int, Field(gt=0,le=255)] = None
    rx_low_size:  Annotated[int, Field(gt=0,le=255)] = None
    rx_start_frame: Annotated[int, Field(0b101, Literal=True)] 
    rx_device_id: int = 0x01
    rx_size: int = 0
    rx_L: int = Field(0, ge=0, le=1) 
    rx_data: List[int] = []


    def build_header(self,data):
        """
        Builds the header of the frame.
        
        start_frame: 3 bits ([1,0,1])
        L: 1 bit (1 for long, 0 for short)
        size: frame size (4 bits if short, 16 bits if long)
        device_id: 8 bits
        """
        if self.tx_L == 0:
            self.tx_header = (self.tx_start_frame << 5) | (self.tx_L << 4) | (self.tx_size & 0x0F)
            self.tx_high_size = 0x00
            self.tx_low_size = 0x00
            self.tx_end_header = (~(self.tx_start_frame & 0xFF) << 5) | (self.tx_L << 4) | (self.tx_size & 0x0F) 
            self.tx_end_header =  self.tx_end_header & 0xFF     
            output = [chr(self.tx_header), chr(self.tx_high_size),
                      chr(self.tx_low_size), chr(self.tx_device_id)]
            for chart in data:
                output.append((chart))

            output.append(chr(self.tx_end_header))
            return  output
                
        else:  
            self.tx_header = (self.tx_start_frame << 5) | (self.tx_L << 4)
            self.tx_high_size = (self.tx_size >> 8) & 0xFF
            self.tx_low_size = self.tx_size & 0xFF
            self.tx_end_header = (~(self.tx_start_frame & 0xFF) << 5) | (self.tx_L << 4) | (self.tx_size & 0x0F) 
            self.tx_end_header =  self.tx_end_header & 0xFF     
            output = [chr(self.tx_header), chr(self.tx_high_size),
                      chr(self.tx_low_size), chr(self.tx_device_id)]
            for chart in data:
                output.append((chart))

            output.append(chr(self.tx_end_header))    

    def decode_header(self, frame):
        """
        Decodes the frame to extract the header information.
        
        frame: List of characters representing the frame
        """

        if len(frame) < 5:
            raise ValueError("Frame is too short to be valid.")

        self.rx_header = ord(frame[0])
        self.rx_high_size = ord(frame[1])
        self.rx_low_size = ord(frame[2])

        if self.rx_device_id!=self.tx_device_id:
            raise ValueError("The received device ID is not correct.")
        
        self.rx_end_header = ord(frame[-1])
        if (self.rx_start_frame != ((self.rx_header >> 5) & 0x07)):
            raise ValueError("Start header is not the same")

        self.rx_L = (self.rx_header >> 4) & 0x01

        if self.rx_L == 0: 
            self.rx_size = self.rx_header & 0x0F
        else:  
            self.rx_size = (self.rx_high_size << 8) | self.rx_low_size

        self.rx_end_header = ((~self.rx_start_frame & 0x07) << 5) | (self.rx_L << 4) | (self.rx_size & 0x0F)
        self.rx_end_header &= 0xFF  

        if self.rx_end_header != self.tx_end_header:
            raise ValueError("End header does not match the expected value.")

        self.rx_data = frame[4:-1]  

        if (len(self.rx_data)!=self.rx_size):
            raise ValueError("RX Data doesn't have the correct size")   

        return {
            "start_frame": self.rx_start_frame,
            "L": self.rx_L,
            "size": self.rx_size,
            "device_id": self.rx_device_id,
            "data": self.rx_data,
            "end_header": self.rx_end_header
        }

    def transmit_data(self,data: str):
        data_char= []
        for character in data:
            data_char.append((character))

        self.tx_size = len(data)
        self.tx_L    =  self.tx_size >= 16
        self.tx_data = self.build_header(data_char)
        print("\n\nYou are transmitting the following data frame: ")
        print('Start frame: {}'.format(bin(ord(self.tx_data[0]))))
        print('Size Low: {}'.format(hex(ord(self.tx_data[1]))))
        print('Size High: {}'.format(hex(ord(self.tx_data[2]))))
        print('Device ID: {}'.format(hex(ord(self.tx_data[3]))))
        print('Data: {}'.format(((self.tx_data[4:-1]))))
        print('End frame: {}\n\n'.format(bin(ord(self.tx_data[-1]))))

        for ptr in self.tx_data:
            self.ser.write((ptr).encode('latin-1'))

    def receive_data(self):
        out = []
        while self.ser.inWaiting() > 0:
            out.append(self.ser.read(1).decode('latin-1'))

        decoded_data = self.decode_header(out)

        print("\n\nYou are receiving the following data frame: ")
        print('Start frame: {}'.format(bin((self.rx_header))))
        print('Size Low: {}'.format(hex(self.rx_low_size)))
        print('Size High: {}'.format(hex(self.rx_high_size)))
        print('Device ID: {}'.format(hex(self.rx_device_id)))
        print('Data: {}'.format(self.rx_data))
        print('End frame: {}\n\n'.format(bin(self.rx_end_header)))


        cadena = ''.join(decoded_data['data'])

        if cadena.lower()=='calculadora':
            print('Valid option: execute Calculator....\n\n')
            calculator = Calculator()
            calculator.run()
            return 1
        elif cadena.lower()=='graficar':
            print('Valid option: execute Graph example....\n\n')
            graph_example()
            return 1
        elif cadena.lower()=='exit':
            print('Exit...')
            return 0
        else:
            print('Rx string is not a valid option')
            return 1
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.ser = serial.serial_for_url('loop://', timeout=1)
        self.ser.isOpen()
        self.ser.timeout=None
        self.ser.flushInput()
        self.ser.flushOutput()



if __name__ == "__main__":
    while_flag = 1
    my_uart = UART()
    while(while_flag):
        data = input('\n\nIngrese una opcion: ')
        my_uart.transmit_data(data = data)
        while_flag = my_uart.receive_data()

   