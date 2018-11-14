from acis import ACISMiscer

if __name__ == "__main__":
    a = ACISMiscer()
    a.register_port(["AT..master",
                     "ADB..master",
                     "AT..slave",
                     "ADB..slave"])

    a.at.master.info()
    a.at.slave.info()
    a.adb.master.info()
    a.adb.slave.info()
    print("""
    ids:
    {master_at},
    {master_adb},
    {slave_at}
    {slave_adb},
    """.format(
        master_at = id(a.at.master),
        master_adb = id(a.adb.master),
        slave_at = id(a.at.slave),
        slave_adb = id(a.adb.slave)))

    a.adb.whoami()
    a.at.whoami()

    b = ACISMiscer()
    b.register_port(["AT..any", "ADB..any"])
    b.at.any.info()
    b.adb.any.info()
