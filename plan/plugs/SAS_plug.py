from openhtf import plugs
from  ..plugs.smartctl import SAS_drives, Drive_Health

class SASPlug(plugs.BasePlug):
    '''A Plug that does gets SAS drive health.'''
    def __init__(self):
      print('Instantiating %s!' % type(self).__name__)
    def Get_Qty_SAS_Drives(self):
          
       return SAS_drives()

    def Get_Drive_Health(self):
        return Drive_Health()
    def tearDown(self):
      # This method is optional.  If implemented, it will be called at the end
      # of the test.
      print('Tearing down %s!' % type(self).__name__)
