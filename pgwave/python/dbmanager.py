import cx_Oracle
from datetime import datetime
from databaseAccess import asp_default

_dbtables={'LightCurves':'LightCurves', \
 'FlareEvents':'FlareEvents',\
 'PointSources':'PointSources',\
 'EnergyBands':'EnergyBands',\
 'LatSourceCatalog':'LatSourceCatalog',\
 'DiffuseSources':'DiffuseSources',\
 'TimeIntervals':'TimeIntervals',\
 'Rois':'Rois',\
 'SourceMonitoringConfig':'SourceMonitoringConfig',\
 'Frequencies':'Frequencies',\
 'FlareTestTypes':'FlareTestTypes',\
 'FlareTypes':'FlareTypes',\
 'Flare_COUNTERPART':'Flare_COUNTERPART',\
 'SpectrumTypes':'SpectrumTypes',\
 'SourceTypes':'SourceTypes',\
 'GCNnotices':'GCNnotices',\
 'GRB_Email_List':'GRB_Email_List',\
 'GRB_ASP_Config':'GRB_ASP_Config',\
 'GRBAfterglow':'GRBAfterglow',\
 'GRB':'GRB',\
 'Healpix':'Healpix',\
 'FlareAdvocateResults':'FlareAdvocateResults',\
 'CounterPartCatalog':'CounterPartCatalog'}
 
_FlareTypesFields={'flare_type':('flare_type',[])}

_FlareTestTypesFields={'flare_test_type':('flare_test_type',[])}

_PointSourcesFields={
  'PTSRC_NAME':('ptsrc_name',[]),\
  'HEALPIX_ID':('healpix_id',[]),\
  'ROI_ID':('roi_id',[]),\
  'LAT_CATID':('lat_catid',[]),\
  'SOURCE_TYPE':('source_type',[]),\
  'SPECTRUM_TYPE':('spectrum_type',[]),\
  'RA':('ra',[]),\
  'DEC':('dec',[]),\
  'ERROR_RADIUS':('error_radius',[]),\
  'POSITION_QUALITY':('position_quality',[]),\
  'NX':('nx',[]),\
  'NY':('ny',[]),\
  'NZ':('nz',[]),\
  'XML_MODEL':('xml_model',[]),\
  'IS_OBSOLETE':('is_obsolete',[]),\
  'IS_PUBLIC':('is_public',[])}
  
_CounterPartFields={
  'CATALOGNAME':('catalogname',[]),\
  'COUNTERPARTNAME':('counterpartname',[]),\
  'RA':('ra',[]),\
  'DEC':('dec',[]),\
  'ERROR_RADIUS':('error_radius',[])}

_FlareCounterpatFields={
  'FLARE_ID':('flare_id',[]),\
  'CATALOGNAME':('catalogname',[]),\
  'COUNTERPARTNAME':('counterpartname',[])}

_FlareEventsFields={
  'FLARE_ID':('flare_id',[]),\
  'PTSRC_NAME':('ptsrc_name',[]),\
  'ADVOCATE_RESULT_ID':('advocate_result_id',[]),\
  'STARTTIME':('starttime',[]),\
  'ENDTIME':('endtime',[]),\
  'FLUX':('flux',[]),\
  'FLUX_ERR':('flux_err',[]),\
  'FLARE_TYPE':('flare_type',[]),\
  'FLARE_TEST_TYPE':('flare_test_type',[]),\
  'FLARE_TEST_VALUE':('flare_test_value',[]),\
  'PROCESSING_DATE':('processing_date',[]),\
  'HEALPIX_ID':('healpix_id',[])}

class dbmanager:
	def __init__(self):
		self.conn= cx_Oracle.connect(*asp_default)
	def close(self):
		self.conn.close()
	def getPointSources(self):
		sql="select * from POINTSOURCES order by ra ASC"
		cursor=self.conn.cursor()
		res=cursor.execute(sql)
		colname=cursor.description
		tot=len(colname)
		for row in cursor:
		  for i in range(0,tot):
		    _PointSourcesFields[colname[i][0]][1].append(row[i])
		cursor.close()
			    
			
if __name__=="__main__":

	d=datetime.now()
	db=dbmanager()
	db.getPointSources()
	db.close()

	print _PointSourcesFields['HEALPIX_ID'][1]
