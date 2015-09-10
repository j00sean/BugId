import re;
from dxCrashInfoConfig import dxCrashInfoConfig;

def cCrashInfo_fasReadOutput(oCrashInfo):
  sLine = "";
  asLines = [];
  while 1:
    sChar = oCrashInfo._oCdbProcess.stdout.read(1);
    if sChar == "\r":
      pass; # ignored.
    elif sChar in ("\n", ""):
      if sChar == "\n" or sLine:
        if dxCrashInfoConfig["bOutputIO"]:
          print "cdb>%s" % repr(sLine)[1:-1];
        oCrashInfo.asCdbIO.append(sLine);
        asLines.append(sLine);
      if sChar == "":
        break;
      sLine = "";
    else:
      sLine += sChar;
      # Detect the prompt.
      oPromptMatch = re.match("^\d+:\d+(:x86)?> $", sLine);
      if oPromptMatch:
        if dxCrashInfoConfig["bOutputIO"]:
          print "cdb>%s" % repr(sLine)[1:-1];
        oCrashInfo.asCdbIO.append(sLine);
        return asLines;
  # Cdb stdout was closed: the process is terminating.
  assert oCrashInfo._bCdbTerminated or len(oCrashInfo._auProcessIds) == 0, \
      "Cdb terminated unexpectedly! Last output:\r\n%s" % "\r\n".join(oCrashInfo.asCdbIO[-20:]);
  oCrashInfo._bCdbRunning = False;
  return None;
