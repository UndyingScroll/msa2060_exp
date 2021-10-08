from spintop_openhtf import TestPlan,  conf
import time, requests, json, hashlib
from plan.station import _station
import openhtf as htf
from openhtf import PhaseResult
from ..plugs.SAS_plug import SASPlug
from ..SAS_Plan import plann
from ..process import onfailskip


@plann.testcase('Drive Count Test')
@htf.measures(htf.Measurement('drive-expected'))
@htf.measures(htf.Measurement('drive-count'))
@htf.measures(htf.Measurement('drives-match').equals(True))
@plann.plug(SAS = SASPlug)
def drive_count_test(test, SAS):
    get_drive_count = SAS.Get_Qty_SAS_Drives()
    test.logger.info('Drive count :' + str(get_drive_count))
    drive_expected = _station['drive_qty']

    test.measurements['drive-count'] = get_drive_count
    test.measurements['drive-expected'] = drive_expected
    test.measurements['drives-match'] = get_drive_count == drive_expected


