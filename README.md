# filmcalc
```
  Usage: filmcalc [length [NNmm]] | [keykode [Lp]]  [FFfps|Hz]
         filmcalc length1|time1|keykode +|- length2|time2 [FFfps|Hz] [Lp]
         filmcalc length1|time1 *|/ multiple [FFfps|Hz]
```
Quick conversion and simple arithmetic operations related to cinema film stock. Supported units are:
 * timecodes (SMPTE-style, non-drop-frame only)
 * frame numbers (both integer and non-integer frame rates);
 * KeyKode (Kodak-style, e.g. `EJ2296111802+11`, up to perforation precision);
 * stock length (metres)
 * stock length (feet)

Conversion among the above units implies conversion parameters need to be passed (os defaults used, as per table below): frame rates, film gauge and pulldown, etc.

```
  length  Stock lengths in either:
          frames   just a unitless number;
            feet   ending with 'ft', e.g. 128ft;
          metres   ending with 'm', e.g. 27m;
            time   in SMPTE non-drop-frame TimeCode format [hh:]mm:ss[.fr].
 keykode  Stock KeyKode MEnnnnnnffff[+rr[.pp]]  (or integer EdgeCode)
    NNmm  '35mm' (default), '16mm' or '65mm' footage width.
      FF  Integer or fractional frames/second ('fps' or 'Hz'); 24 by default.
          Lp  L perforations/frame (default: 4p for 35mm, 1p for 16mm, 5p for 65mm)
   timeM  Footage duration in SMPTE non-drop-frame TimeCode format, or
 lengthN  footage lengths in frames, to be arithmetically operated upon.
multiple  Times which footage length/duration is to be multiplied/divided by.
```
  If no arithmetic operations are specified, filmcal reports the film length in
both SMPTE TimeCode, frames' number and film length in feet and metres. Some
measures depend on film gauge, perforations and/or frame rate; others do not.
  Film length/duration conversions and divisions, as well as calculations with
non-integer frame rates, *always* produce down-rounded frames/TimeCode results.
  Arithmetic operations can be performed between same-size and -frame-rate
stock only. Examples of arithmetic operations' syntax include:
```
       45:02.19 + 52:48.16 [24Hz]   =    01:37:51.11    =  140915 frames
          64867 + 52:48.16          =    01:37:51.11    =  140915 frames
    01:12:36.06 - 50564 30fps       =       44:30.22    =  80122 frames
EJ2296111802+11 - 18.2 3p           = EJ2296111801+16.1 =  28816 frames
       06:05.12 * 2                 =       12:11       =  17544 frames
       03:45.06 / 3 25Hz            =       01:15.02    =  1877 frames
```
