# -*- python -*-
# -*- coding: utf-8 -*- 
# author: krozin@gmail.com
# pylib: created 2014/03/01.
# copyright

# --------------------  RANDOM ----------------

def get_random_uuid():
    # import uuid
    import hashlib
    import os
    l = os.urandom(30).encode('base64')[:-1]
    return hashlib.sha256(l).hexdigest()


def get_sha(s):
    # import uuid
    import hashlib
    return hashlib.sha256(s).hexdigest()

# ------------------ FILES ----------------------

def generate_tmp_files(targetdict="/tmp/files/"):
    import os
    import random
    import time
    import threading

    if not os.path.exists(targetdict):
        os.makedirs(targetdict)
    class FileThread(threading.Thread):
        def run(self):
            print "run"
            while(True):
                filenames = []
                countf = (random.choice([1,2,3]))
                for i in xrange(0, countf):
                    filenames.append(os.path.join(targetdict, get_random_uuid()))
                for i in filenames:
                    with (open(i, 'w')) as nfile:
                        nfile.write(get_random_ip4())
                time.sleep(1)
    mythread = FileThread()
    mythread.start()


def generate_file_name():
    from datetime import datetime
    import random
    filename = "_".join([datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"), str(random.randint(1,100))])
    return filename


def check_new_files(directory):
    import os
    new_files = []
    for root, _, files in os.walk(directory):
        if files:
            abs_root = os.path.abspath(root)
            for fd in files:
                new_files.append(os.path.join(abs_root, fd))
        break
    return new_files


def get_base64_from_file(filepath):
    import base64
    import os
    encoded_string = ""
    if os.path.exists(filepath):
        with open(filepath, "rb") as ifile:
            encoded_string = base64.b64encode(ifile.read())
    return encoded_string

# ----------------- REGEXP --------------------------------------

def make_cleanup(input_string):
    """clean up string: remove IP/IP6/Mac/etc... by using regexp

    :param input_string: str - input string
    :return: s after regexp and clean up
    """

    import re
    # let's try to find all IP, IP6, MAC
    ip4re = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ip6re = re.compile(r'\b(?:[a-fA-F0-9]{4}[:|\-]?){8}\b')
    macre = re.compile(r'\b[a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:]'
                       r'[a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:]'
                       r'[a-fA-F0-9]{2}[:][a-fA-F0-9]{2}\b')
    digitre = re.compile(r'\b(?:[0-9]{1,3}){1,50}\b')
    hexre = re.compile(r'\b(?:[0-9a-fA-F]{1,8}){1,50}\b')
    punctuation = re.compile(r'["\'!,?.:;\(\)\{\}\[\]\/\\\<\>]+')

    def ismatch(match):
        """
        :param match: string
        :return: value or ''
        """
        value = match.group()
        return " " if value else value

    stmp = ip4re.sub(ismatch, input_string)
    stmp = ip6re.sub(ismatch, stmp)
    stmp = macre.sub(ismatch, stmp)
    stmp = punctuation.sub(ismatch, stmp)
    stmp = digitre.sub('x', stmp)
    listhex = hexre.findall(stmp)
    if listhex:
        for i in listhex:
            stmp = hexre.sub('x' * len(i), stmp)
    return stmp


# ------------------------ IP / MAC ------------------------------

def get_random_mac():
    import random
    return ':'.join(map(lambda x: "%02x" % x, [0x00,0x16,0x3e,random.randint(0x00, 0x7f),random.randint(0x00, 0xff),random.randint(0x00, 0xff)]))


def get_random_ip4():
    import random
    return ".".join(map(lambda x: str(random.randint(0,256)), [i for i in range(0,4)]))


def get_random_ip4net():
    import random
    return get_random_ip4()+"/"+str(random.choice([16,24]))


def get_geo_ip(ipstr):
    from geoip import geolite2
    import datetime
    match = geolite2.lookup(ipstr)
    message = "Bремя={}\nIPaddress={}; {}\nСтрана={}\nВременная зона={}\nLat/Lon={}\n".format(
        datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S"),
        request.environ.get('REMOTE_ADDR'),
        request.remote_addr,
        match.country,
        match.timezone,
        match.location)
    return message, match


#--------------------- EMAIL --------------------------------------------

def send_email(subj, message, toemail="bymotornn@gmail.com", fromemail="bymotornn@mail.ru"):
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(message)
    msg['Subject'] = subj
    msg['From'] = fromemail
    msg['To'] = toemail
    username = 'bymotornn@gmail.com'
    username = 'bymotornn@mail.ru'
    password = 'na'

    # The actual mail send
    s = smtplib.SMTP("smtp.gmail.com:587")
    s = smtplib.SMTP("smtp.mail.ru:25")
    s.starttls()
    s.login(username,password)
    s.sendmail(fromemail, toemail, msg.as_string())
    s.quit()


def read_imap_email(title, user='bymotornn@gmail.com', passw='ns'):
    import imapclient
    import pyzmail
    imapserver = 'imap.gmail.com'
    imapObj = imapclient.IMAPClient(imapserver, ssl=True)
    imapObj.login(user, passw)
    imapObj.select_folder('INBOX', readonly=True)
    UIDs = imapObj.search(title)
    rawMessages = imapObj.fetch(UIDs[0], ['BODY[]', 'FLAGS'])
    message = pyzmail.PyzMessage.factory(rawMessages[UIDs[0]]['BODY[]'])
    email_subject = message.get_subject()
    email_from = message.get_addresses('from')
    email_to = message.get_addresses('to')
    email_cc = message.get_addresses('cc')
    email_bcc = message.get_addresses('bcc')
    email_payload = message.text_part.get_payload().decode(message.text_part.charset)
    email_html_payload = message.html_part.get_payload().decode(message.html_part.charset)
    imapObj.logout()
    return UIDs, rawMessages, message, email_subject,\
           email_from, email_to, email_cc, email_bcc,\
           email_payload, email_html_payload


#---------------  DECORATORS ---------------------------------
# decorator which print how many time were spend on fucntion
def benchmark(func):
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(time.clock() - t)
        return res
    return wrapper

# decorator which counting call of function
def counter(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        res = func(*args, **kwargs)
        print("{0} invoked: {1}x times".format(func.__name__, wrapper.count))
        return res
    wrapper.count = 0
    return wrapper


def memoize(f):
    from functools import wraps
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        key = f.__name__
        cached = self._cache.get(key)
        if cached is None:
            cached = self._cache[key] = f(self, *args, **kwargs)
        return cached
    return wrapper


def coroutine(f):
    def wrap(*args,**kwargs):
        gen = f(*args,**kwargs)
        gen.send(None)
        return gen
    return wrap


@coroutine
def coroutine_worker(f, *args, **kwargs):
    while True:
        (args, kwargs) = (yield)
        f(*args, **kwargs)


# ------------- TREADS -------------------------------------

def getProfiledThreadClass():
    from threading import Thread
    class ProfiledThread(Thread):
        # Overrides threading.Thread.run()
        def run(self):
            import cProfile
            profiler = cProfile.Profile()
            try:
                return profiler.runcall(Thread.run, self)
            finally:
                profiler.dump_stats('myprofile-%d.profile' % (self.ident,))
    return ProfiledThread


def getTreadloopClass(*agrs, **kwargs):
    from threading import Thread
    import traceback
    class ThreadLoop(Thread):
        """ Simple Thread with loop implementation.
            Allows to stop the loop easily.
        """
        def __init__(self, *agrs, **kwargs):
            self.loop = kwargs.pop('loop')
            kwargs['target'] = self.start
            super(ThreadLoop, self).__init__(*agrs, **kwargs)
            self.running = True

        def start(self):
            while self.running:
                try:
                    self.loop()
                except Exception as e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    print (''.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
                    return

        def stop(self):
            self.running = False
            self.join()
    return ThreadLoop


def count_down(time_to_sleep):
    import sys
    import time
    print("\r\t  Wait for {} seconds".format(time_to_sleep))
    while(time_to_sleep >= 0):
        sys.stdout.write("\r\t * Remaining: ... %d ..." % time_to_sleep)
        sys.stdout.flush()
        time.sleep(1)
        time_to_sleep -= 1
    sys.stdout.write("\n")


class DoItInTread(object):
    def __init__(self):
        import threading
        self.stop_sig = threading.Event()
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def do(self):
        while not self.stop_sig.is_set():
            try:
                # do something
                pass
            except:
                # handle except
                pass

    def start(self):
        if not self.receive_thread.isAlive():
            self.receive_thread.start()
        self.stop_sig.clear()

    def stop(self):
        self.stop_sig.set()


def run_cmd(self, tool, cmd):
    import subprocess
    from settings import LOGGER as logger

    tool = subprocess.check_output(["which", tool]).strip()
    if not tool:
        raise Exception('{} not found'.format(tool))
    try:
        args = " ".join(cmd).split(" ")
        pipe = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = pipe.communicate()
        code = pipe.returncode
    except Exception as message:
        logger.debug('{}'.format(message))


# -------------  CV / ALGORITMS ----------------------------
def image2text(filepath, lang='rus'):
    import os
    from PIL import Image
    import pytesseract
    if os.path.exists(filepath):
        print pytesseract.image_to_string(Image.open(filepath), lang=lang)
        return pytesseract.image_to_string(Image.open(filepath), lang=lang)

def distance(astr, bstr):
    """Calculates the Levenshtein distance between a and b

    :param astr: str - input string
    :param bstr: str - input string
    :return: distance: int - distance between astr and bstr
    """

    alen, blen = len(astr), len(bstr)
    if alen > blen:
        astr, bstr = bstr, astr
        alen, blen = blen, alen
    row = list(range(alen + 1))  # Keep current row
    for i in range(1, blen + 1):
        change = i-1
        row[0] = i
        for j in range(1, alen + 1):
            if astr[j - 1] != bstr[i - 1]:
               change += 1  
            add = row[j] + 1
            delete = row[j - 1] + 1
            row[j] = min(add, delete, change)
            change = add - 1 #previous value of row[j]
    return row[alen]

# -------------------  TEMPLATES ----------------------------
class Publisher(object):
    def __init__(self):
        subscribers = {}
    def register(self, subscriber):
        self.subscribers.update({subscriber.id: subscriber})
    def unregister(self, sid):
        self.subscribers.pop(sid)
    def notifyAll(self, event):
        map(lambda a: a.notify(event), self.subscribers.values())
    def notifyBy(self, sid, event):
        self.subscribers.get(sid).notify(event)

class Subscriber:
    def notify(self, event):
        # that method is going to be invoked by Publisher
        # in order to notify corresponding Subscriber
        raise NotImplementedError('method should be implemented')

# ----------------------- LOGGING ----------------------------
def get_log_object(fname='log.log', loggername='pipeline'):
    import logging
    import os

    def add_file_handler(fname):
        file_handler = logging.FileHandler(fname)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fileformatter)
        logger.addHandler(file_handler)

    class MyFormatter(logging.Formatter):
        def format(self, record):
            try:
                msg = record.msg.split(':', 1)
                if len(msg) == 2:
                    record.msg = '[{:<15}]{}'.format(msg[0], msg[1])
            except:
                pass
            return logging.Formatter.format(self, record)


    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)

    f = '[%(asctime)s][%(processName)-5s][%(levelname)-21s]%(message)s'
    formatter = MyFormatter(f)
    fileformatter = logging.Formatter(f)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Log level colors
    logging.addLevelName(logging.DEBUG, "\033[1;34m{}\033[1;0m".format(logging.getLevelName(logging.DEBUG)))
    logging.addLevelName(logging.INFO, "\033[1;32m{}\033[1;0m".format(logging.getLevelName(logging.INFO)))
    logging.addLevelName(logging.WARNING, "\033[1;33m{}\033[1;0m".format(logging.getLevelName(logging.WARNING)))
    logging.addLevelName(logging.ERROR, "\033[1;31m{}\033[1;0m".format(logging.getLevelName(logging.ERROR)))
    logging.addLevelName(logging.CRITICAL, "\033[1;41m{}\033[1;0m".format(logging.getLevelName(logging.CRITICAL)))

    fpath = os.join(os.path.dirname(os.path.abspath(__file__)), fname)
    add_file_handler(fpath)

# ----------------------- DATETIME ----------------------------

import datetime
class UTC(datetime.tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return datetime.timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return datetime.timedelta(0)

def get_miter_epoch_time():
    # iron python is so stupid to read from string. Need workaround with strptime
    # python 2.x is so stupid to apply UTC by itself. Need workaround with tzinfo
    try:
        return datetime.datetime.strptime("Jan 01, 2000 | 00:00:00 UTC", "%b %d, %Y | %H:%M:%S %Z")
    except:
        utc = UTC()
        return datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=utc)

def get_diff_time_per_seconds(dt=None):
    # dt - datetime object like datetime.datetime.utcnow()
    # ironpython is so stupid to calculate offset-naive and offset-aware times and find diff.
    # workarrond - get UTC
    if dt:
        dit = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=UTC())
        return (dit - get_miter_epoch_time()).total_seconds()
    return (datetime.datetime.now(tz=UTC()) - get_miter_epoch_time()).total_seconds()

def get_today_midnight_per_second():
    dt = datetime.datetime.utcnow()
    midnight = datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0, tzinfo=UTC())
    next_midnight = datetime.timedelta(days=1) + midnight
    return get_diff_time_per_seconds(next_midnight)

def get_miter_unit_epoch_diff_seconds():
    miter_epoch = datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=UTC())
    epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=UTC())
    return (miter_epoch - epoch).total_seconds()

def get_date_from_seconds(sec):
    # dt - datetime object like datetime.datetime.utcnow()
    miter_epoch = datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=UTC())
    mdate = datetime.datetime.fromtimestamp(time.mktime(miter_epoch.timetuple()) + sec)
    return mdate

# ----------------------- CONVERT ----------------------------

def convert_hex_string_2_string(s):
    # '43756D2E20496D702E2052303120202000' -> 'Cum. Imp. R01    '
    # '30313035362E3620202020202020202000' -> '01056.6          '
    l1 = []
    c1 = c2 = i1 = None
    for i in range(0, len(s)):
        # 0, 2,
        if i%2 == 0:
            c1 = s[i]
        else:
            c2 = s[i]
            i1 = int('0x{}{}'.format(c1, c2), 0)
            l1.append(chr(i1))
    return "".join(l1)