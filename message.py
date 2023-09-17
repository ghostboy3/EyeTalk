''' Demonstrates how to subscribe to and handle data from gaze and event streams '''

from pickle import GLOBAL
import time

import adhawkapi
import adhawkapi.frontend

import mouse

#sglobal gaze = None

class FrontendData:
    ''' BLE Frontend '''
    i = False
    length =0.346
    width= 0.194
    z= 0.22    
    #z0= None
    # x1=-17.3
    # y1=-9.7
    x0 =0
    y0 = 0
    xvec=None
    yvec= None
    zvec=None
    x0=None
    y0 = None
    factored_length= None
    factored_width= None
    def __init__(self):
        # Instantiate an API object
        # TODO: Update the device name to match your device
        self._api = adhawkapi.frontend.FrontendApi(ble_device_name='ADHAWK MINDLINK-282')

        # Tell the api that we wish to receive eye tracking data stream
        # with self._handle_et_data as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EYETRACKING_STREAM, self._handle_et_data)#_handle_et_data)

        # Tell the api that we wish to tap into the EVENTS stream
        # with self._handle_events as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EVENTS, self.handle_events)#_handle_events)

        # Start the api and set its connection callback to self._handle_tracker_connect/disconnect.
        # When the api detects a connection to a MindLink, this function will be run.
        self._api.start(tracker_connect_cb=self._handle_tracker_connect,
                        tracker_disconnect_cb=self._handle_tracker_disconnect)

    def shutdown(self):
        '''Shutdown the api and terminate the bluetooth connection'''
        self._api.shutdown()

    #@staticmethod
    #def quadrant_handler(event_type, *args, xvec,yvec,zvec,x0,y0,factored_length,factored_width):

    

    @staticmethod
    def _handle_et_data(et_data: adhawkapi.EyeTrackingStreamData):
        ''' Handles the latest et data '''
        if et_data.gaze is not None:
            xvec, yvec, zvec, vergence = et_data.gaze
            print(f'Gaze x={xvec:.2f},y={yvec:.2f},z={zvec:.2f},vergence={vergence:.2f}')

        # if et_data.eye_center is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         rxvec, ryvec, rzvec, lxvec, lyvec, lzvec = et_data.eye_center
        #         print(f'Eye center: Left=(x={lxvec:.2f},y={lyvec:.2f},z={lzvec:.2f}) '
        #               f'Right=(x={rxvec:.2f},y={ryvec:.2f},z={rzvec:.2f})')

        # if et_data.pupil_diameter is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         rdiameter, ldiameter = et_data.pupil_diameter
        #         print(f'Pupil diameter: Left={ldiameter:.2f} Right={rdiameter:.2f}')

        # if et_data.imu_quaternion is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         x, y, z, w = et_data.imu_quaternion
        #         print(f'IMU: x={x:.2f},y={y:.2f},z={z:.2f},w={w:.2f}')
        # #gaze = et_data.gaze
    

        # if event_type == adhawkapi.Events.BLINK:
        #     print("YOU CANNOT MISS THIS MESSAGE UNLESS THERES AN ERROR!")
        #     duration  = args[0]
        #     print(duration)
            if FrontendData.i == False:
                print("YOU CANNOT MISS THIS MESSAGE UNLESS THERES AN ERROR!")
                # if duration  >= 5 and duration <= 10:
                #         print("YOU CANNOT MISS THIS MESSAGE UNLESS THERES AN ERROR!")
                    # if et_data.gaze is not None:
                # xvec, yvec, zvec, vergence = et_data.gaze
                z0=-zvec
                y0=yvec
                x0=xvec
                        # print(args)
                        # print(f'Eye Close: {timestamp} {eye_idx}')
                print(f'{z0:.2f}')
                print(f'{y0:.2f}')
                print(f'{x0:.2f}')
                print("YOU CANNOT MISS THIS MESSAGE UNLESS THERES AN ERROR!")
                factor = (FrontendData.z/(z0-FrontendData.z))
                print(f'{factor:.5f}') 
                factored_length=FrontendData.length *factor
                factored_width=FrontendData.width* factor 
                print(factored_length)
                print(factored_width)
                FrontendData.i = True

        # quadrant = quadrant_handler(event_type, *args, xvec,yvec,zvec,x0,y0,factored_length,factored_width)
        #quadrant_handler(event_type, *args, xvec,yvec,zvec,x0,y0,factored_length,factored_width)

    #GLOBAL VAR = 2
    @staticmethod
    def handle_events(event_type, timestamp, *args):
        
        
        # if event_type == adhawkapi.Events.BLINK:
        #     duration = args[0]
        #     print(args)
        #     print(f'Got blink: {timestamp} {duration}')

        if event_type == adhawkapi.Events.BLINK:
            duration = args[0]
            print(duration)

            # '''  <--------------------------------------------->'''
            # start_time = time.time()
            # while time.time() - start_time < 2:
            #     if event_type == adhawkapi.Events.BLINK:
            #         '''  <--------------------------------------------->'''

                #Quadrants 1 and 4``
            if (FrontendData.xvec>(FrontendData.x0-(FrontendData.factored_length/3))&FrontendData.xvec<(FrontendData.x0-(FrontendData.factored_length/6))):
                if (FrontendData.yvec>FrontendData.y0)&(FrontendData.yvec<(FrontendData.y0+(FrontendData.factored_width/2))):
                    print("Quadrant 1")
                    mouse.move(234, 209, absolute=False, duration=0.5)
                    mouse.click('left')
                else:
                    print("Quadrant 4")
                    mouse.move(246, 644, absolute=False, duration=0.5)
                    mouse.click('left')

            #Quadrant 2 and 5
            elif (FrontendData.xvec>(FrontendData.x0-(FrontendData.factored_length/6))&FrontendData.xvec<(FrontendData.x0-(FrontendData.factored_length/6))):
                if (FrontendData.yvec>FrontendData.y0)&(FrontendData.yvec<(FrontendData.y0+(FrontendData.factored_width/2))):
                    print("Quadrant 2")
                    mouse.move(729, 226, absolute=False, duration=0.5)
                    mouse.click('left')
                else:
                    print("Quadrant 5")
                    mouse.move(742, 645, absolute=False, duration=0.5)
                    mouse.click('left')

            #Quadrant 3 and 6
            elif (FrontendData.xvec>(FrontendData.x0+(FrontendData.factored_length/6))&FrontendData.xvec<(FrontendData.x0+(FrontendData.factored_length/6))):
                if (FrontendData.yvec>FrontendData.y0)&(FrontendData.yvec<(FrontendData.y0+(FrontendData.factored_width/2))):
                    print("Quadrant 3")
                    mouse.move(1252, 219, absolute=False, duration=0.5)
                    mouse.click('left')
                else:
                    print("Quadrant 6")
                    mouse.move(1262, 642, absolute=False, duration=0.5)
                    mouse.click('left')
                        
        if event_type == adhawkapi.Events.EYE_CLOSED:
            eye_idx = args[0]
            print(args)
            print(f'Eye Close: {timestamp} {eye_idx}')
        if event_type == adhawkapi.Events.EYE_OPENED:
            eye_idx = args[0]
            print(args)
            print(f'Eye Open: {timestamp} {eye_idx}')


    # @staticmethod
    # def quadrant_handler(event_type, *args, xvec,yvec,zvec,x0,y0,factored_length,factored_width):

    #     if event_type == adhawkapi.Events.BLINK:
    #         duration = args[0]
    #         print(duration)
    #         #if duration >3000:
    #         #Quadrants 1 and 4
    #         if (xvec>(x0-(factored_length/3))&xvec<(x0-(factored_length/6))):
    #             if (yvec>y0)&(yvec<(y0+(factored_width/2))):
    #                 print("Quadrant 1")
    #             else:
    #                 print("Quadrant 4")

    #         #Quadrant 2 and 5
    #         elif (xvec>(x0-(factored_length/6))&xvec<(x0-(factored_length/6))):
    #             if (yvec>y0)&(yvec<(y0+(factored_width/2))):
    #                 print("Quadrant 2")
    #             else:
    #                 print("Quadrant 5")

    #         #Quadrant 3 and 6
    #         elif (xvec>(x0+(factored_length/6))&xvec<(x0+(factored_length/6))):
    #             if (yvec>y0)&(yvec<(y0+(factored_width/2))):
    #                 print("Quadrant 3")
    #             else:
    #                 print("Quadrant 6")

    
    def _handle_tracker_connect(self):
        print("Tracker connected")
        self._api.set_et_stream_rate(60, callback=lambda *args: None)

        self._api.set_et_stream_control([
      
            adhawkapi.EyeTrackingStreamTypes.GAZE,
            adhawkapi.EyeTrackingStreamTypes.EYE_CENTER,
            adhawkapi.EyeTrackingStreamTypes.PUPIL_DIAMETER,
            adhawkapi.EyeTrackingStreamTypes.IMU_QUATERNION,
        ], True, callback=lambda *args: None)

        self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=lambda *args: None)
        self._api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=lambda *args: None)

    def _handle_tracker_disconnect(self):
        print("Tracker disconnected")

    #def _calibration(event_type, timestamp, *args, et_data: adhawkapi.EyeTrackingStreamData):
       
    def field_of_vision_screen():
        length =0.346
        width= 0.194
        z= -0.62
        z0= None
        # x1=-17.3
        # y1=-9.7
        x0 =0
        y0 = 0

def main():
    ''' App entrypoint '''
    frontend = FrontendData()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        frontend.shutdown()

if __name__ == '__main__':
    main()


