# Publich to a ThingSpeak Channel Using MQTT
# 
# This is an example of publishing to multiple fields simultaneously.
# Connections over standard TCP, websocket or SSL are possible by setting
# the parameters below.
#
# CPU and RAM usage is collected every 20 seconds and published to a
# ThingSpeak channel using an MQTT Publish
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python


#Before use code create channel and deivce from thingspeak's website
import paho.mqtt.publish as publish
import psutil
import string
import datetime
from time import strftime
import time
from smbus import SMBus
bus = SMBus(1)
# The ThingSpeak Channel ID.
# Replace <YOUR-CHANNEL-ID> with your channel ID.
channel_ID = "1835670"

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt3.thingspeak.com"

# Your MQTT credentials for the device
mqtt_client_ID = "NTcNLjsNKwkJDhYlFREVKiY"
mqtt_username  = "NTcNLjsNKwkJDhYlFREVKiY"
mqtt_password  = "Zkkm593X1wnA6T4bzCzZAjZS"

t_transport = "websockets"
t_port = 80

# Create the topic string.
topic = "channels/" + channel_ID + "/publish"

adc_address=0x14
channel0 = 0xB0

#Variables to convert voltage to resistance
C = 79.489;
slope = 14.187;

#Variables to convert resistance to temp
R0 = 100.0;
alpha = 0.00385;

vref = 5
# Max reading is 2^16-1 or 65535
max_reading = 65535 
lange = 0x06 # number of bytes to read in the block
zeit = 5 # number of seconds to sleep between each measurement
tiempo = 0.4 # number of seconds to sleep between each channel reading

def getreading(adc_address,adc_channel):
    bus.write_byte(adc_address, adc_channel)
    time.sleep(tiempo)
    reading = bus.read_i2c_block_data(adc_address,adc_channel, lange)
    valor =((reading[0] & 0x3F)<<10)+(reading[1]<<2)+(reading[2]>>6)
    #Bits to Voltage
    volts = (valor*vref)/max_reading
    #Voltage to resistance
    Rx = volts*slope+C; #y=mx+c
    #Resistance to Temperature
    temp= (Rx/R0-1.0)/alpha; #from Rx = R0(1+alpha*X)
    #Uncommect to convet celsius to fehrenheit
    #temp = temp*1.8+32; 
    
    if( (reading[0]& 0b0010100) == 0b0010100): # we found the error
        print ("Input voltage to channel 0x%x is either open or more than %5.2f. The reading may not be correct. Value read in is %12.8f Volts." %((adc_channel), vref, volts))
    else:
        print (">>>Voltage read in on channel 0x%x is %12.8f Volts" %((adc_channel),volts))
    time.sleep(tiempo)
    return temp
time.sleep(tiempo)
ch0_mult = 1
while (True):
    Ch0Value = ch0_mult*getreading(adc_address, channel0)
    time.sleep(tiempo)
     
    # get the system performance data over 20 seconds.
    cpu_percent = psutil.cpu_percent(interval=20)
    ram_percent = psutil.virtual_memory().percent

    # build the payload string.
    payload = "field1=" + str(Ch0Value)
    print("payload:"+ payload)

    # attempt to publish this data to the topic.
    try:
        print ("Writing Payload = ", payload," to host: ", mqtt_host, " clientID= ", mqtt_client_ID, " User ", mqtt_username, " PWD ", mqtt_password)
        publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})

        print("Done")
    except Exception as e:
        print (e) 
