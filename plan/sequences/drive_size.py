from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib, ast
from plan.station import _station
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.SAS_plug import SASPlug
from ..SAS_Plan import plann
from ..process import onfailskip


drive_map = { "IOX-SAN-2U-6TB": '6.0 TB', "IOX-SAN-2U-8TB": '8.0 TB', "IOX-SAN-2U-10TB": '10.0 TB',
                "IOX-SAN-2U-12TB": '12.0 TB', "IOX-SAN-2U-14TB" : '14.0 TB', "IOX-SAN-2U-16TB": '16.0 TB',
                "IOX-SAN-2U-18TB": '18.0 TB', "IOX-SAN-2U-72TB" : '72.0 TB', "IOX-SAN-2U-96TB": '96.0 TB', 
                "IOX-SAN-2U-120TB": '120.0 TB', "IOX-SAN-2U-144TB" : '144.0 TB', "IOX-SAN-2U-168TB": '168.0 TB', 
                "IOX-SAN-2U-192TB": '192.0 TB', "IOX-SAN-2U-216TB": '216.0 TB'}

@plann.testcase('Drive Capacity Test')
@htf.measures(htf.Measurement('drives-detected').doc("'SAS drives detected'"))
@htf.measures(htf.Measurement('drive-expected'))
@htf.measures(htf.Measurement('size-expected'))
@htf.measures(htf.Measurement('size'))
@htf.measures(htf.Measurement('size-valid').equals(True))
@plann.plug(SAS = SASPlug)
def drive_size_test(test, SAS):
    results = {}
    results['drive-expected'] = _station['drive']
    results['size-expected'] = drive_map.get(_station['drive'], 'None')

    test.logger.info('Get drive capacity for all SAS drives')
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
                results[each2].append(drive_raw[each][each2])
        test.measurements['drive-expected'] = results['drive-expected']
        test.measurements['size-expected'] = results['size-expected']
        test.measurements['size-valid'] = all([ x == results['size-expected'] for x in results['capacity']])
    
    except:
        return PhaseResult.FAIL_AND_CONTINUE
    


