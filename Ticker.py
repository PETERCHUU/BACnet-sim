#!/usr/bin/env python2.7
import time, threading
import queue
import sys
queuer = queue.Queue()

class settingObject:
    def __init__(self,tempStart,tempEnd,pressureStart,PressureEnd,fireAlarm) -> None:
        self.tempStart = tempStart
        self.tempEnd = tempEnd
        self.PressureStart = pressureStart
        self.PressureEnd = PressureEnd
        self.FireAlarm = fireAlarm
        pass

class Ticker(threading.Thread):
  """A very simple thread that merely blocks for :attr:`interval` and sets a
  :class:`threading.Event` when the :attr:`interval` has elapsed. It then waits
  for the caller to unset this event before looping again.

  Example use::

    t = Ticker(1.0) # make a ticker
    t.start() # start the ticker in a new thread
    try:
      while t.evt.wait(): # hang out til the time has elapsed
        t.evt.clear() # tell the ticker to loop again
        print time.time(), "FIRING!"
    except:
      t.stop() # tell the thread to stop
      t.join() # wait til the thread actually dies

  """
  # SIGALRM based timing proved to be unreliable on various python installs,
  # so we use a simple thread that blocks on sleep and sets a threading.Event
  # when the timer expires, it does this forever.
  def __init__(self, interval):
    super(Ticker, self).__init__()
    self.interval = interval
    self.evt = threading.Event()
    self.evt.clear()
    self.should_run = threading.Event()
    self.should_run.set()

  def stop(self):
    """Stop the this thread. You probably want to call :meth:`join` immediately
    afterwards
    """
    self.should_run.clear()

  def consume(self):
    was_set = self.evt.is_set()
    if was_set:
      self.evt.clear()
    return was_set

  def run(self):
    """The internal main method of this thread. Block for :attr:`interval`
    seconds before setting :attr:`Ticker.evt`

    .. warning::
      Do not call this directly!  Instead call :meth:`start`.
    """
    while self.should_run.is_set():
      time.sleep(self.interval)
      self.evt.set()


def userUpdate(queue:queue.Queue):
    while True:
        password=input("Press Enter Password to change setting")
        if password=="P@ssw0rd":
            setting=settingObject()
            timer=Ticker(30)
            timer.start()
            try:
                print("please select the setting you want to change")
                print("1. Temperature Range")
                print("2. Pressure Range")
                print("3. Fire Alarm")
                print("4. Exit")
                print("Enter your choice: ")
                while timer.evt.wait():
                    choice = sys.stdin.readline().strip()
                    if choice == "1":
                        try:
                            print("Enter the start temperature: ")
                            setting.tempStart = float(sys.stdin.readline().strip())
                            print("Enter the end temperature: ")
                            setting.tempEnd = float(sys.stdin.readline().strip())
                            queue.put(setting)
                        except:
                            print("Invalid Input")
                    elif choice == "2":
                        print("Enter the start pressure: ")
                        setting.PressureStart = float(sys.stdin.readline().strip())
                        print("Enter the end pressure: ")
                        setting.PressureEnd = float(sys.stdin.readline().strip())
                        queue.put(setting)
                    elif choice == "3":
                        print("Enter the fire alarm status: ")
                        print("1. True, other is False")
                        number=int(sys.stdin.readline().strip())
                        setting.FireAlarm = True if number==1 else False
                        queue.put(setting)
                    else:
                        break
            except:
                timer.stop()
                timer.join()
                print("input Timeout")
        time.sleep(1)