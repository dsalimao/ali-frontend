#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
from datetime import datetime
from email.header import decode_header

a='''
<td width=3D"151" align=3D"center" style=3D"vertical-align:top=
; font-family:Arial, Helvetica, sans-serif; font-size:20px; color:#ec2026; =
font-weight:bold; padding:0px 0px 0px 0px;"><img style=3D"display:block; co=
lor:#333333; font-size:10px;" src=3D"http://images=2Eharmony=2Eepsilon=2Eco=
m/ContentHandler/images?id=3D21303fda-d22c-4014-90a4-100403a0af34" alt=3D"S=
avings per Gallon" width=3D"105" height=3D"38" border=3D"0">$0=2E05</td>
'''



b=a.encode('ascii')
print(b)