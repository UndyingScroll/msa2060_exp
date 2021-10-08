from pySMART import DeviceList

def SAS_drives():

    drives = []

    SAS_qty = 0
    devlist = DeviceList()
    for f in devlist.devices:
        if(f.interface) == "sas":
            SAS_qty = SAS_qty +1

    return SAS_qty

def Drive_Health():
    drives = []

    drive = { 'serial' : '', 'interface' : '', 'path' : '', 'model' : '', 'capacity' : '', 'health' : '', 'SSD' : '', 'power_on' : '', 'group_errors' : '', 'firmware': ''}


    SAS_drives = 0
    devlist = DeviceList()
    for f in devlist.devices:
        if(f.interface) == "sas":
            SAS_drives = SAS_drives +1
            drive.update(serial = str(f.serial))
            drive.update(interface = f.interface)
            drive.update(path = f.path)
            drive.update(model = f.model)
            drive.update(capacity = f.capacity)
            drive.update(health = f.assessment)
            drive.update(SSD = f.is_ssd)
            drive.update(power_on = f.diags['Power_On_Hours'])
            gerrors = f.diags['Reallocated_Sector_Ct']
            if(gerrors == '-'):
                gerrors = 0
            drive.update(group_errors = gerrors)
            drive.update(firmware = f.firmware)

            drives.append(str(drive))
    return drives

