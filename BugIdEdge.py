import subprocess, threading, time, sys

# Kill processes
def killProcess(name):
	ret = subprocess.Popen("taskkill /f /im %s" % name, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
	output, error = ret.communicate()

# To control RuntimeBroker process
def cRuntimeBroker(argv):
	while(1):
		time.sleep(10)
		print "[+] Control thread => Checking BugId..."
		ret = subprocess.check_output("powershell .\\runtimebroker.ps1", shell = False)
		if "0" in ret:
			print "[+] Control thread => BugId is running ok. Exiting control thread"
			sys.exit()
		else:
			print "[+] Control thread => RuntimeBroker is suspended"
			print "[+] Control thread => Kill MicrosoftEdge.exe (BugId therefore), dbgsrv.exe and RuntimeBroker.exe"
			killProcess("MicrosoftEdge.exe")
			killProcess("dbgsrv.exe")
			killProcess("RuntimeBroker.exe")
			# Restart bugid thread
			runb = threading.Thread(target=runBugId, args=(argv,))
			runb.start()

def runBugId(argv):
	print "[+] BugId args: %s" % argv
	subprocess.call("python BugId.py %s" % argv, shell = False)

# Main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "[+] No min arguments. Setting up: python BugId.py edge"
		bugidargs = "edge"
	else:
		bugidargs = " ".join(sys.argv[1:])
	# Run control thread
	runc = threading.Thread(target=cRuntimeBroker, args=(bugidargs,))
	runc.start()
	# Run BugId in main thread
	runBugId(bugidargs)
