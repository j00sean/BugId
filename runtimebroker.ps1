# Mainly based on https://stackoverflow.com/a/46581491
$processes = Get-Process *
$processHt = @{}
foreach ($process in $processes) {
  foreach ($thread in $process.Threads) {   
    if($thread.ThreadState -eq "Wait") {
      if ( $processHt.Containskey( $process.Name ) ) {
        if ( $processHt[$process.Name] -match $($thread.WaitReason.ToString()) ) {
        } else {
          $processHt[$process.Name] += ",$($thread.WaitReason.ToString())"
        }
      } else {
        $processHt.Add( $process.Name , $thread.WaitReason.ToString() )
      }
    }
  }
}
#$suspended_processes = $processHt.Keys | Where-Object { $processHt[$_] -eq 'Suspended'}
$suspended_threads = $processHt.Keys | Where-Object { $processHt[$_] -match 'Suspended'}
if($suspended_threads -match "RuntimeBroker"){
	echo "1"
}else{
	echo "0"
}
