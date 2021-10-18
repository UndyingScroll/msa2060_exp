from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib, ast
from plan.station import _station, _drives
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.SAS_plug import SASPlug
from ..SAS_Plan import plann
from ..process import onfailskip


@plann.testcase('Drive Health Test')
@htf.measures(htf.Measurement('drives-detected').doc("'SAS drives detected'"))
@htf.measures(htf.Measurement('serial').doc("'Serial number of SAN/NAS drive'"))
@htf.measures(htf.Measurement('interface').doc("'Drive interface, SAS expected'"))
@htf.measures(htf.Measurement('interface-valid').equals(True).doc("'Drive interface, SAS expected'"))
@htf.measures(htf.Measurement('path').doc("'Drive location in Linux filesystem'"))
@htf.measures(htf.Measurement('model').doc("'Drive HPE model number'"))
@htf.measures(htf.Measurement('capacity').doc("'Drive user capactiry'"))
@htf.measures(htf.Measurement('health').doc("'Drive SMART health self-assement, OK expected'"))
@htf.measures(htf.Measurement('health-valid').equals(True).doc("'Drive SMART health self-assement, OK expected'"))
@htf.measures(htf.Measurement('SSD').doc("'Drive type, SSD true, HDD false'"))
@htf.measures(htf.Measurement('SSD-valid').equals(True).doc("'Drive type, SSD true, HDD false'"))
@htf.measures(htf.Measurement('power_on').doc("'Drive Power On Hours, less than 90 days expected'"))
@htf.measures(htf.Measurement('power_on-valid').equals(True).doc("'Drive Power On Hours, less than 90 days expected'"))
@htf.measures(htf.Measurement('group_errors').doc("'Drive Group Errors, zero are expected'"))
@htf.measures(htf.Measurement('group_errors-valid').equals(True).doc("'Drive Group Errors, zero are expected'"))
@htf.measures(htf.Measurement('firmware').doc("'Drive firmware version'"))

@plann.plug(SAS = SASPlug)
def drive_health(test, SAS):
    keywords = ('serial','path','model','capacity','firmware','group_errors','health','SSD','power_on','interface')
    results = {}
    
    test.logger.info('Get drive health for all SAS drives')
    get_drive_count = SAS.Get_Qty_SAS_Drives()
    drive_raw = SAS.Get_Drive_Health()
    drive_data = []
    test.logger.info(drive_raw)

    for each in drive_raw:
        drive_data.append(ast.literal_eval(each))
    
    test.logger.info(drive_data)
    test.measurements['drives-detected'] = get_drive_count
    if drive_data == False:   
        test.logger.info('No SAS data returned.')
        return PhaseResult.FAIL_AND_CONTINUE
    try:
        for each in drive_data[0]:
            results[each] = []
        for each in range(0,len(drive_data)):
            for each2 in drive_data[each]:
                results[each2].append(drive_data[each][each2])
        test.measurements['group_errors-valid'] =  all([x == 0 for x in results['group_errors']])
        if test.test_record.metadata['test_description'] == 'B Stock':
            test.measurements['power_on-valid'] = all([x < 43800 for x in results['power_on']])
        else:
            test.measurements['power_on-valid'] = all([x < 2190 for x in results['power_on']])
        test.measurements['health-valid'] = all([x == 'OK' for x in results['health']])
        test.measurements['SSD-valid'] = all([x == 'HDD' for x in results['SSD']])
        test.measurements['interface-valid'] = all([x == 'sas' for x in results['interface']])

        for each in keywords:
            test.measurements[each] = results[each]
    except:
        return PhaseResult.FAIL_AND_CONTINUE

