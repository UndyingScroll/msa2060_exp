from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.SAS_plug import SASPlug
from ..SAS_Plan import plann
from ..process import onfailskip



@plann.testcase('Drive Metadata Clean/Erase')
@htf.measures(htf.Measurement('drives-detected').doc("'SAS drives detected'"))
@htf.measures(htf.Measurement('clean-results'))
@plann.plug(SAS = SASPlug)
def drive_clean_test(test, SAS):
    results = []
    test.logger.info('Clean drive meta data for all SAS drives')
    get_drive_count = SAS.Get_Qty_SAS_Drives()
    drive_raw = SAS.Get_Drive_Health()
    test.measurements['drives-detected'] = get_drive_count
    
    test.logger.info(drive_raw)
    if drive_raw == False:   
        test.logger.info('No SAS data returned.')
        return PhaseResult.FAIL_AND_CONTINUE
    try:

        for each in range(0,get_drive_count):
            
            
            health = ast.literal_eval(drive_raw[each])
            drivepath = health['path']
            result = metaclean(drivepath)
            test.logger.info('Clean meta of drive ' + drivepath + 'result :'+ str(result))
            results.append(result)
    
    except:
        return PhaseResult.FAIL_AND_CONTINUE

    test.measurements['clean-results'] = results
    


