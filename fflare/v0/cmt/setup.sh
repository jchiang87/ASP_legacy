# echo "Setting fflare v0 in /misc/data41/users/tosti/glast/ASP"

if test "${CMTROOT}" = ""; then
  CMTROOT=/data45/software/GlastExternals//CMT/v1r16p20040701; export CMTROOT
fi
. ${CMTROOT}/mgr/setup.sh

tempfile=`${CMTROOT}/mgr/cmt build temporary_name -quiet`
if test ! $? = 0 ; then tempfile=/tmp/cmt.$$; fi
${CMTROOT}/mgr/cmt -quiet setup -sh -pack=fflare -version=v0 -path=/misc/data41/users/tosti/glast/ASP  $* >${tempfile}; . ${tempfile}
/bin/rm -f ${tempfile}

