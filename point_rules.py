ALL_ROLES = [
    'DEROwnerSunSpec',
    'DERInstallerSunSpec',
    'DERVendorSunSpec',
    'ServiceProviderSunSpec',
    'GridOperatorSunSpec',
]
SETTINGS_READ_ROLES = ['DERInstallerSunSpec', 'DERVendorSunSpec', 'ServiceProviderSunSpec', 'GridOperatorSunSpec']
SETTINGS_WRITE_ROLES = ['DERInstallerSunSpec', 'ServiceProviderSunSpec', 'GridOperatorSunSpec']

POINT_LEVEL_RULES = {
    1: {  # Only update Unit ID on commissioning (less relevant for TCP connections)
        'common.DA': {'read': ALL_ROLES, 'write': ['DERInstallerSunSpec']}
    },
    702: {  # 702 Settings
        'DERCapacity.WMax': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.WMaxOvrExt': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.WOvrExtPF': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.WMaxUndExt': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.WUndExtPF': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.VAMax': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.VarMaxInj': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.VarMaxAbs': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.WChaRteMax': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.WDisChaRteMax': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.VAChaRteMax': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.VADisChaRteMax': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.VNom': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.VMax': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.VMin': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.AMax': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.PFOvrExt': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
        'DERCapacity.PFUndExt': {'read': SETTINGS_READ_ROLES, 'write': SETTINGS_WRITE_ROLES},
    },
}
