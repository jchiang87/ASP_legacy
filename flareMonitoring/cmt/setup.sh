# echo "Setting flareMonitoring v0r1 in /a/surrey01/vol/vol2/g.svac/focke/ASP/code/newASP"

if test "${CMTROOT}" = ""; then
  CMTROOT=/afs/slac.stanford.edu/g/glast/applications/CMT/v1r16p20040701; export CMTROOT
fi
. ${CMTROOT}/mgr/setup.sh

tempfile=`${CMTROOT}/mgr/cmt build temporary_name -quiet`
if test ! $? = 0 ; then tempfile=/tmp/cmt.$$; fi
${CMTROOT}/mgr/cmt -quiet setup -sh -pack=flareMonitoring -version=v0r1 -path=/a/surrey01/vol/vol2/g.svac/focke/ASP/code/newASP  $* >${tempfile}; . ${tempfile}
/bin/rm -f ${tempfile}

