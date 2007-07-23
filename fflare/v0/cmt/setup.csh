# echo "Setting fflare v0 in /misc/data41/users/tosti/glast/ASP"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /data45/software/GlastExternals//CMT/v1r16p20040701
endif
source ${CMTROOT}/mgr/setup.csh

set tempfile=`${CMTROOT}/mgr/cmt build temporary_name -quiet`
if $status != 0 then
  set tempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt -quiet setup -csh -pack=fflare -version=v0 -path=/misc/data41/users/tosti/glast/ASP  $* >${tempfile}; source ${tempfile}
/bin/rm -f ${tempfile}

