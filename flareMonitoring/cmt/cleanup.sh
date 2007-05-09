if test "${CMTROOT}" = ""; then
  CMTROOT=/afs/slac.stanford.edu/g/glast/applications/CMT/v1r16p20040701; export CMTROOT
fi
. ${CMTROOT}/mgr/setup.sh
tempfile=`${CMTROOT}/mgr/cmt build temporary_name -quiet`
if test ! $? = 0 ; then tempfile=/tmp/cmt.$$; fi
${CMTROOT}/mgr/cmt -quiet cleanup -sh -pack=flareMonitoring -version=v0r1 -path=/a/surrey01/vol/vol2/g.svac/focke/ASP/code/ASP $* >${tempfile}; . ${tempfile}
/bin/rm -f ${tempfile}

