# Role-Based Access Control for Secure SunSpec Modbus

In 2025, the SunSpec Alliance created a working group to define 
a secure version of the protocol based on Modbus TCP/Security 
from modbus.org.  The protocol used mTLS with an X.509v3 certificate
that included a role extention.  To provide granual authorization to 
SunSpec Modbus holding registers, the SunSpec Server extracts
the role in the certificate to grant point-level read and write 
access to different users based on the role they are assuming.

## Roles-to-Rights Maps

Point-by-point read/write access is in the `/rbac` directory and summarized 
in [roles_to_rights.md](roles_to_rights.md).

## Roles

SunSpec has defined the following roles with these general permissions:

* **ReadOnlySunSpec** - Read access to all data. No write permissions. This role may be
used by DER owners for monitoring production data or DER vendors for 
monitoring, diagnostics, and/or prognostics.
* **GridServiceSunSpec** - Read access to all data. Write access to commanded and 
autonomous functions. No access to networking or protection functions. 
* **NetworkAdministratorSunSpec** - Read access to all data. Write access 
to SunSpec network holding registers.
* **SuperAdministratorSunSpec** - Full read/write access to all SunSpec points. 
This role may be used by (a) the grid operator, (b) the system installer, 
(c) the DER vendor for repairs, or (d) a DER owner in situations where 
they are operating a microgrid.

Optionally, the device vendor may add additional roles.  For example, 
IEC 62351-8 includes a set of additional roles:

* VIEWER
* OPERATOR
* ENGINEER
* INSTALLER
* SECADM: Security administrator
* SECAUD: Security auditor
* RBACMNT: RBAC management

## Rights

Permissions in the case of SunSpec RBAC are limited to read and write 
access of the Modbus holding registers. IEC 62351-8 goes further and includes 
rights for dataset management and manipulation, reporting, file reads 
and writes, file management, object control, object configuration, 
creating/editing/deleting settings groups, and adjusting server or 
service security settings. However, in the context of SunSpec Modbus, 
this functionality is not provided by the application protocol. 

Note: all roles must have the ability to read the ID and L points for all 
models in order for the SunSpec discovery process to work.  

## Standards Harmonization

There were two primary references used in the creation of the 
Secure SunSpec standard: "MODBUS/TCP Security" from modbus.org and 
IEC 62351-8 "Role-based access control for power system management".
The Secure SunSpec Specification deviated from these reference 
documents in several ways, including the approach to authorization, 
as described below.

## References

* [Modbus.org, MODBUS/TCP Security: Protocol Specification, MB-TCP-Security-
v36_2021-07-30](https://www.modbus.org/docs/MB-TCP-Security-v36_2021-07-30.pdf)
* [International Electrotechnical Commission, IEC 62351-8:2020 Power systems 
management and associated information exchange - Data and communications security - 
Part 8: Role-based access control for power system management](https://webstore.iec.ch/en/publication/61822)
* [J. Johnson, Recommendations for Distributed Energy Resource Access Control, Sandia Report
SAND2021-0977, January 2021.](https://www.osti.gov/servlets/purl/1765273)