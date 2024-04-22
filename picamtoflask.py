import io
#import picamera
import picamera2
from flask import Flask, Response

app = Flask(__name__)

def generate_frames():
    #with picamera.PiCamera() as camera:
    #    camera.resolution = (640, 480)
    #    camera.framerate = 24
    #    stream = io.BytesIO()
        
    #    for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
    #        stream.seek(0)
    #        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n'
    #        stream.seek(0)
    #        stream.truncate()
    
    with picamera2.Picamera2() as camera:
        capture_config = camera.create_still_configuration(lores={"size": (320, 240)}, display="lores")
        camera.configure(camera.create_preview_configuration())
        camera.start()
        stream = io.BytesIO()
        
        for _ in camera.capture_file(capture_config, stream, format='jpeg'):
        #for _ in camera.switch_mode_and_capture_file(capture_config, stream, format='jpeg'):
            stream.seek(0)
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n'
            stream.seek(0)
            stream.truncate(0)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if '__main__'.__eq__(__name__):
    app.run(host='0.0.0.0', port=5000, threaded=True) 
