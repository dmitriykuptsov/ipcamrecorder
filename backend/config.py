# Statement for enabling the development environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 10

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# JWT VALIDITY PERIOD

JWT_VALIDITY_IN_DAYS = 365

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "kamnakosyonBaljIpMishlanUnEvosbo"

# Secret key for signing cookies
SECRET_KEY = "ew0BlawpAcyajNirshesUvonViUjEbs1"

# Token key
TOKEN_KEY = "OogyejIvumNasAdUbBishkOudGajnicPiWrymagAbthucradocviOrmosOvDerow"

# Server nonce
SERVER_NONCE = "RabroyllIjhywofuckcorwojnamvowAg"

MAX_CONTENT_PATH = 30*1024*1024;

OUTPUT_FOLDER = "/opt/data2/ipcam/storage/192.168.1.21/video1/"

USER = "admin"

SALT = "vsjKJ2csaj)312Kc-)#c2andP014dvrR"

PASSWORD = "a696afa681056ae310944b72384726053306dad3ff4a8a4aa5a27f85e856af92" #Hashed password SHAR256(SALT | PASSWORD)

MAX_SEGMENTS_PER_HLS = 10

VIDEO_CONTAINER = "ts"

EXTRACT_DURATION_SCRIPT = "compute_duration.sh"

EXEC_DIR = "."

M3U8_VERSION = 0x3
