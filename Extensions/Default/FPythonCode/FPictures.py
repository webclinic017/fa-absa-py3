from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FPictures

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
        This module contains small pictures in string format, encoded using
        the python function uu.encode(). It also contains help functions for
        decoding and encoding the pictures.


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import os, base64, binascii, uu
from types import StringType

def decodePicture(name, dir):
    pic=eval(name)
    picPath = os.path.join(dir, name)
    if pic[2]=='uu':
        decode(pic[1], picPath+'.'+pic[0])
    elif pic[2]=='base64':
        gif = base64.decodestring(pic[1])
        file=open(picPath+'.'+pic[0], 'w')
        file.write(gif)
        file.close()

def encodePictures(dir, picture, text, type):
    if type == 'uu':
        uu.encode(dir+picture, dir+text)
    elif type == 'base64':
        input = open(dir+picture).read()
        gifstring = base64.encodestring(input)
        print (gifstring)

Tplus=['png', """begin 444 Tplus.png
MB5!.1PT*&@H    -24A$4@   !,    0! ,    &ZEE1    !W1)344'T P-
M 2<2P<XJ20    EP2%ES   *\   "O !0JPTF    #!03%1%    ____EXY[
M                                                    >0<XQP  
M  )T4DY3_P#EMS!*    ,TE$051XVF,0! )%$"' ( @#$"8V424@4(0P%2%*
J($Q&;$P&!D9%144%W H0)B"9B]\- ""Y# ?@!=01     $E%3D2N0F""
 
end""", 'uu']

Lplus = ['png', """begin 444 Lplus.png
MB5!.1PT*&@H    -24A$4@   !,    0! ,    &ZEE1    !W1)344'T P-
M 2<OF:9F6     EP2%ES   *\   "O !0JPTF    #!03%1%    ____EXY[
M                                                    >0<XQP  
M  )T4DY3_P#EMS!*    -4E$051XVF,0! )%$"' ( @#$"8V424@4(0P%2%*
L($Q&;$P&!D9%144%W H0)B"9B^(&#"8 'ZD+]TSC*9<     245.1*Y"8(( 
 
end""", 'uu']

Lminus = ['png', """begin 444 Lminus.png
MB5!.1PT*&@H    -24A$4@   !,    0! ,    &ZEE1    !W1)344'T P-
M 24:_2/ ^0    EP2%ES   *\   "O !0JPTF    #!03%1%    ____EXY[
M                                                    >0<XQP  
M  )T4DY3_P#EMS!*    ,$E$051XVF,0! )%$"' ( @#$"8V424@4(0P%2%*
G\# 9&!@5%145B%&+9"Z*&S"8 #1I##=GI+NM     $E%3D2N0F""
 
end""", 'uu']

Tminus = ['png', '''begin 444 Tminus.png
MB5!.1PT*&@H    -24A$4@   !,    0! ,    &ZEE1    !W1)344'T P-
M 28"Q6(+;     EP2%ES   *\   "O !0JPTF    #!03%1%____EXY[    
M                                                    &V J-   
M  %T4DY3 $#FV&8    E241!5'C:8V   @$&; ";J" 0"""D\\3.5E!0$@( 8
;M4CFXG<# ,0: DU.+)U=     $E%3D2N0F""
 
end''', 'uu']

T = ['png', """begin 444 T.png
MB5!.1PT*&@H    -24A$4@   !,    0 0,   #."M8A    !W1)344'T P-
M 2,[YQ!W(0    EP2%ES   *\   "O !0JPTF     903%1%EXY[____%U*0
M2     )T4DY3_P#EMS!*    %TE$051XVF/X7_^ X?]_(,9%ASK@DP< 'V\I
1%\T$U;4     245.1*Y"8(( 
 
end""", 'uu']


L = ['png', """begin 444 L.png
MB5!.1PT*&@H    -24A$4@   !,    0 0,   #."M8A    !W1)344'T P-
M 24BU2%X9P    EP2%ES   *\   "O !0JPTF     903%1%EXY[____%U*0
M2     )T4DY3_P#EMS!*    &$E$051XVF/X7_^ X?]_(,9%ASI :.P8 #1O
2*I=/:V-K     $E%3D2N0F""
 
end""", 'uu']

I = ['png', """begin 444 I.png
MB5!.1PT*&@H    -24A$4@   !,    0 0,   #."M8A    !W1)344'T P-
M 24JV_KP50    EP2%ES   *\   "O !0JPTF     903%1%EXY[____%U*0
M2     )T4DY3_P#EMS!*    $TE$051XVF/X7_^ X?]_(":/!@ V>RGA@P5A
-Q0    !)14Y$KD)@@@  
 
end""", 'uu']

blank = ['png', """begin 444 blank.png
MB5!.1PT*&@H    -24A$4@   !,    0 0,   #."M8A    !W1)344'T P-
M 1\KB50>N@    EP2%ES   *\   "O !0JPTF     903%1%    ____I=F?
MW0    )T4DY3_P#EMS!*    #TE$051XVF/X__\! P48 +Y[+>']USU+    
) $E%3D2N0F""
 
end""", 'uu']

report_plus = ['gif', """begin 666 report_plus.gif
M1TE&.#EA#@ ) ,0  /7X_?7X_+/.[K3.[K3.[<+7\</8\=3C]>7N^;/.[<+8
M\?3X_/KYY____\W-S:>GIW-S<QP<'/___P                          
M                         "'Y! $  !( +      .  D   4]H"..HV2:
M3J.N#72B:[2ZKQ, 010L 7TZB(A0B' ])$?'81E9'GRH@L$0D2J@$D>"(" D
,!@FL T(NDU^2$  [
 
end""", 'uu']

report_minus = ['gif', """begin 666 report_minus.gif
M1TE&.#EA#@ ) ,0  '5R<QT;',[,S<W+S!T;('-S=?W]_^?M^?3X_K3.[M3C
M];3.[,+8\?3X^W!T<W)T<\S.S<K.RAH<&7-S<<W-RO___<_.S**AH?___\W-
MS7-S<QP<'/___P           "'Y! $  !P +      .  D   5&H#!0PY!E
M@L"MJU 9F%%AF,:V<:73Q<U%"$1C.+3=! =)8+,A'&P73E2@J%H5#Q^%P>TR
5)C[(8KQ(C(TLB^-1>#@F#H O!  [
 
end""", 'uu']

report_end = ['gif', """begin 666 report_end.gif
M1TE&.#EA#@ ) ,0  '5R<QT;',[,S<W+S!T;('-S=?W]_^?M^?3X_K3.[M3C
M];3.[,+8\?3X^W!T<W)T<\S.S<K.RAH<&7-S<<W-RO___<_.S**AH?___\W-
MS7-S<QP<'/___P           "'Y! $  !P +      .  D   43X,6-9&F>
/IXBN["B^' RW=&VW(0 [
 
end""", 'uu']


def decode(in_string, out_file=None, mode=None, quiet=0):
    """Decode uuencoded file"""
    if not in_string:
        raise Exception('No valid in input string')
    if in_string[:5] == 'begin':
        in_split = in_string.splitlines()
        hdr = in_split[0]
        hdrfields = hdr.split(" ", 2)
        if len(hdrfields) == 3 and hdrfields[0] == 'begin':
            try:
                int(hdrfields[1], 8)
            except ValueError:
                raise Exception('No valid in input string found')

    if out_file is None:
        out_file = hdrfields[2].rstrip()
        if os.path.exists(out_file):
            raise Exception('Cannot overwrite existing file: %s' % out_file)
    if mode is None:
        mode = int(hdrfields[1], 8)
    #
    # Open the output file
    #
    if out_file == '-':
        out_file = sys.stdout
    elif isinstance(out_file, StringType):
        fp = open(out_file, 'wb')
        try:
            os.path.chmod(out_file, mode)
        except AttributeError:
            pass
        out_file = fp
    #
    # Main decoding loop
    #
    i=1
    s = in_split[i]
    while s and s.strip() != 'end':
        try:
            data = binascii.a2b_uu(s)
        except binascii.Error as v:
            # Workaround for broken uuencoders by /Fredrik Lundh
            nbytes = (((ord(s[0])-32) & 63) * 4 + 5) / 3
            print (s[:nbytes])
            data = binascii.a2b_uu(s[:nbytes])
            if not quiet:
                sys.stderr.write("Warning: %s\n" % str(v))
        out_file.write(data)
        i=i+1
        s = in_split[i]
    if not s:
        raise Exception('Truncated input file')
