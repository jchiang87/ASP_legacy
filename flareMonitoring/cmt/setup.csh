# echo "Setting flareMonitoring v0r1 in /a/surrey01/vol/vol2/g.svac/focke/ASP/code/newASP"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /afs/slac.stanford.edu/g/glast/applications/CMT/v1r16p20040701
endif
source ${CMTROOT}/mgr/setup.csh

set tempfile=`${CMTROOT}/mgr/cmt build temporary_name -quiet`
if $status != 0 then
  set tempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt -quiet setup -csh -pack=flareMonitoring -version=v0r1 -path=/a/surrey01/vol/vol2/g.svac/focke/ASP/code/newASP  $* >${tempfile}; source ${tempfile}
/bin/rm -f ${tempfile}

