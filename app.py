from flask import Flask, request, render_template
from pycaw.pycaw import AudioUtilities,ISimpleAudioVolume
import comtypes

app = Flask(__name__)

# Flag to track whether COM has been initialized
com_initialized = False

# Initialize COM before the first request
@app.before_request
def before_request():
    global com_initialized
    if not com_initialized:
        comtypes.CoInitialize()
        com_initialized = True

# Uninitialize COM after the last request
@app.teardown_appcontext
def teardown_appcontext(exception=None):
    if com_initialized:
        comtypes.CoUninitialize()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_volume', methods=['POST'])
def set_volume():
    volume = request.form['volume']
    set_system_volume(float(volume))
    return 'Volume set to ' + volume

def set_system_volume(volume):
    # Normalize volume to the range [0, 100]
    volume = max(0, min(volume, 100))

    # Get the default audio session manager
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume_interface.SetMasterVolume(volume / 100, None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')