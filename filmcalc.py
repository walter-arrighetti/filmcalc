#!/usr/bin/python
##########################################################
#  filmcalc 0.6                                          #
#                                                        #
#    Film stock command-line calculator                  #
#                                                        #
#    Copyright (C) 2009 TECHNICOLOR Creative Services    #
#    coding by: Walter Arrighetti                        #
#               <walter.arrighetti@technicolor.com>      #
#    All Rights Reserved.                                #
##########################################################

import string
import sys
import re

ops = "+-*/"

def dframe2TC(fr, fps=24., drop=False, fulldispl=False):
	s = 30*fr
	m1 = ((30*fr)*(60*s)) - 2
	m2 = (10*m1) + 2
	h = 6*m2

def frame2TC(fr, fps=24., drop=False, fulldispl=False):
	hours = mins = secs = rfr = 0
	hours = fr//(3600*fps)
	mins = fr//(60*fps) - 60*hours
	secs = fr/fps - 60*mins - 3600*hours
	rfr = fr%fps
	if not drop:	TC = ("%02d:%02d" % (mins,secs))
	else:	TC = ("%02d;%02d" % (mins,secs))
	if rfr>0 or fulldispl:
		if fps<100:	TC += (".%02d"%rfr)
		else:	TC += (".%d"%rfr)
	if hours>0 or fulldispl:
		if hours<10:
			if not drop:	TC = ("%02d:"%hours) + TC
			else:	TC = ("%02d;"%hours) + TC
		else:
			if not drop:	TC = ("%d:"%hours) + TC
			else:	TC = ("%d;"%hours) + TC
	return TC


def TC2frame(string, fps=24):
	time = re.match(r"((?P<hh>\d+)[:;])?(?P<mm>\d{1,2})(?P<drop>[:;])(?P<ss>\d{1,2})(\.(?P<ff>\d{1,2}))?", string)
	nfps = fps		# To change for Non-drop frame Timecodes
	if time.group('hh')==None:	hh=0
	else:	hh=int(time.group('hh'))
	if time.group('mm')==None:	mm=0
	else:	mm=int(time.group('mm'))
	if time.group('ss')==None:	ss=0
	else:	ss=int(time.group('ss'))
	if time.group('ff')==None:	ff=0
	else:	ff=int(time.group('ff'))
	if time.group('drop')==';':
		return fps*(3600*hh+60*mm+ss)+ff
	else:
		return nfps*(3600*hh+60*mm+ss)+ff



def KeyKode(keykode):
	"""	Returns a dictionary from a KeyKode string (or a barcode-readable EdgeCode integer) with the following values:
	"KeyKode" as a re-arragned KeyKode string,  "EC" as a numeric EdgeCode (to be converted into a barcode)
	"by" Manufacturer,  "gauge" as millimiters (16,35,65,...),  
	"reel#", "foot", "frame", "perf" as respective IDs / offsets  (last two are optional)
	"by#" and "emulsion#" are *optional* keys with barcode/EdgeCode manufacturer and emulsion BCD codes
	"""
	preKKre = re.compile(r"(?P<manfr>[A-Za-z?])(?P<emuls>[A-Za-z?])(?:(?P<roll>\d{6})(?:(?P<foot>\d{4})(?:\+(?P<frame>\d{1,2})(?:\.(?P<perf>\d{1,2}))?)?)?)?")
	KKre = re.compile(r"(?P<manfr>[A-Z?])(?P<emuls>[A-Z?])(?:\s(?P<roll1>\d{2})\s(?P<roll2>\d{4})(?:\s(?P<foot>\d{4})(?:[+](?P<frame>\d{2})(?:[.](?P<perf>\d{1,2}))?)?)?)?")
	Eastmanre = re.compile(r"EASTMAN (?P<stock>\d{4}) (?P<batch>\d{3}) (?P<roll>\d{4}) (?P<printer>\d{3}) (?P<year>[AZ][AZ])")
	Kodak_codes = [0,14,20,22,24,31,34,43,44,45,46,47,48,49,72,74,77,79,87,89,92,93,94,95,96,97,98]
	Kodak_dict = dict(zip(Kodak_codes,"PXYELHDAVKIBMOSZQUWRNLGFJCT"))
	Eastman_codes = [1,5,7,12,17,18,19,29,42,60,63,65,66,84,85,99]
	Eastman_dict = dict(zip(Eastman_codes,"KQNMLHJBVUECDGAI"))
	Fuji_dict = dict(zip([1,2,3,10,11,13,14,20,21,22,30,31,32,40,43,47,50,51,52,53,60,61,62,63,70,71,72,73,82,83,92],"IIINIINNNNNNNRNNNNNNNNNNNNNNNNN"))
	gauge, RollNo, footage, frameNo, perfOff, mc, em, mac, emc, hKK = 35, None, None, None, None, None, None, None, None, None
	
	KK = preKKre.match(string.replace(keykode,' ',''))
	print KK.groupdict().keys()
	if KK:
		hKK = KK.group("manfr").upper()+KK.group("emuls").upper()
		if KK.group("roll"):
			hKK += ' '+KK.group("roll")[0:2]+' '+KK.group("roll")[2:6]
			RollNo = int(KK.group("roll"))
#		if KK.group("roll1"):
#			hKK += KK.group("roll1")+' '+"%04d"%int(KK.group("roll2"))
#			RollNo = int(KK.group("roll1")+KK.group("roll2"))
			if KK.group("foot"):
				footage = int(KK.group("foot"))
				hKK += ' '+"%04d"%int(KK.group("foot"))
				if "frame" in KK.groupdict().keys() and KK["frame"].isdigit():
					frameNo = int(KK.group("frame"))
					hKK += '+'+"%02d"%int(KK.group("frame"))
					if "perf" in KK.groupdict().keys() and KK["perf"].isdigit():
						perfOff = int(KK.group("perf"))
						hKK += '.'+"%02d"%int(KK.group("perf"))
		KK = KKre.match(hKK)
		ma = KK.group("manfr")
		em = KK.group("emuls")
	elif Eastmanre.match(keykode):
		KK = Eastmanre.match(keykode)
		hKK = "EASTMAN "+ "%04d"%int(KK.group("emuls")) +' '+ "%03d"%int(KK.group("batch")) +' '+ "%04d"%int(KK.group("roll")) +' '+ "%03d"%int(KK.group("printer")) +' '+ KK.group("year")
		KK = Eastmanre.match(hKK)
		manufacturer, stock, emulsion = "Eastman", KK.group("stock"), KK.group("batch")
		rollNo, printer, year = int(KK.group("roll")), int(KK.group("printer")), KK.group("year")
		return {	"KeyKode":hKK, "by":manufacturer, "gauge":gauge, "stock":stock, "emulsion":emulsion, "reel#":RollNo, "printer":printer, "year code":year	}
	elif keykode.isdigit() and 4<=len(keykode)<=18:
		KK = keykode
#		if type(keykode)==type(1L) or type(keykode)==type(1):	KK = str(keykode)
#		elif keykode.isdigit() and 4<=len(keykode)<=18:	KK = keykode
#		else:	return None
		mac, emc = int(KK[0:2]), int(KK[2:4])
		if len(keykode)>4:
			RollNo = int(KK[4:10])
			if len(keykode)>10:
				footage = int(KK[10:14])
				if len(keykode)>14:
					frameNo = int(KK[14:16])
					if len(keykode)>16:	perfOff = int(KK[16:18])
		if mac in [0,10]:
			ma, em = 'O', 'U'
			if mac==0:	gauge = 35, "UN 54 (100 ASA)"
			else:	gauge = 16, "N 74 (400 ASA)"
		elif mac in [1,11]:
			ma = 'A'
			emulsion_dict = zip([20,24,83,84],"NMFS")
			if emc in emulsion_dict.keys():	em = emulsion_dict[emc]
			else:	return None
			if mac==1:	gauge=35
			else:	gauge=16
		elif mac in [2,12,22]:
			if emc in Kodak_codes:	ma, em = 'K', Kodak_dict[emc]
			elif emc in Eastman_codes:	ma, em = 'E', Eastman_dict[emc]
			else:	return None
			if mac==2:	gauge=35
			elif mac==12:	gauge=16
			else:	gauge=65
		elif mac in [3,13,23]:
			ma = 'F'
			if emc in Fuji_dict.keys():	em = Fuji_dict[emc]
			else:	return None
			if mac==3:	gauge=35
			elif mac==13:	gauge=16
			else:	gauge=65
		else:	ma = '?'
	if ma == 'O':
		manufacturer = "ORWO"
		if not mac:	mac = 0
		else:
			if gauge==16:	mac=10
			elif gauge==35:	mac=0
		if emc==29:	emulsion = "UN 54 (100 ASA)";	emc = 29
		elif emc==37:	emulsion = "N 74 (400 ASA)";	emc = 37
		else:	emulsion = "UN 54 (100 ASA) / N 74 (400 ASA)"
	elif ma == 'A':
		manufacturer = "Agfa"
		if not mac:	mac = 1
		else:
			if gauge==16:	mac=11
			elif gauge==35:	mac=1
		if em=='N':	emulsion = "XT 100";	emc = 20
		elif em=='M':	emulsion = "XTR 250";	emc = 24
		elif em=='F':	emulsion = "XT 320";	emc = 83
		elif em=='S':	emulsion = "XTS 400";	emc = 84
		else:	emulsion = "unknown"
	elif ma == 'K':
		manufacturer = "Kodak"
		if not mac:	mac = 2
		else:
			if gauge==16:	mac=12
			elif gauge==35:	mac=2
			elif gauge==65:	mac=22
		if em=='P':	emulsion = "5600";	emc = 0
		elif em=='X':	emulsion = "SO-214 SFX 200T";	emc = 14
		elif em=='Y':	emulsion = "5620 Prime Time";	emc = 20
		elif em=='E':	emulsion = "5222/7222";	emc = 22
		elif em=='L':	emulsion = "5224";	emc = 24
		elif em=='H':	emulsion = "5231/7231";	emc = 31
		elif em=='D':	emulsion = "5234/7234";	emc = 34
		elif em=='A':	emulsion = "5243/7243";	emc = 43
		elif em=='V':	emulsion = "5244/7244";	emc = 44
		elif em=='K':	emulsion = "5245/7245";	emc = 45
		elif em=='I':	emulsion = "5246/7246 Vision 250D";	emc = 46
		elif em=='B':	emulsion = "5247/7247";	emc = 47
		elif em=='M':	emulsion = "5248/7248";	emc = 48
		elif em=='O':	emulsion = "5249";	emc = 49
		elif em=='S':	emulsion = "5272/7272";	emc = 72
		elif em=='Z':	emulsion = "5274/7274 Vision 200T";	emc = 74
		elif em=='Q':	emulsion = "5277/7277";	emc = 77
		elif em=='U':	emulsion = "5279/7279";	emc = 79
		elif em=='W':	emulsion = "5287/7287";	emc = 87
		elif em=='R':	emulsion = "5289 Vision 800T";	emc = 89
		elif em=='N':	emulsion = "7292";	emc = 92
		elif em=='L':	emulsion = "5293/7293";	emc = 93
		elif em=='G':	emulsion = "5294/7294";	emc = 94
		elif em=='F':	emulsion = "5295";	emc = 95
		elif em=='J':	emulsion = "5296/7296";	emc = 96
		elif em=='C':	emulsion = "5297/7297";	emc = 97
		elif em=='T':	emulsion = "5298/7298";	emc = 98
		else:	emulsion = "unknown"
	elif ma == 'E':
		manufacturer = "Eastman"
		if not mac:	mac = 2
		else:
			if gauge==16:	mac=12
			elif gauge==35:	mac=2
			elif gauge==65:	mac=22
		if em=='K':	emulsion = "5201/7201 Vision2 50D";	emc = 1
		elif em=='Q':	emulsion = "5205/7205 Vision2 250D";	emc = 5
		elif em=='N':	emulsion = "5207/7207 Vision3 250D";	emc = 7
		elif em=='M':	emulsion = "5212/7212 Vision2 100T";	emc = 12
		elif em=='L':	emulsion = "5217/7217 Vision2 200T";	emc = 17
		elif em=='H':	emulsion = "5218/7218 Vision2 500T";	emc = 18
		elif em=='J':	emulsion = "5219/7219 Vision3 500T";	emc = 19
		elif em=='B':	emulsion = "5229/7229 Vision2 Expression 500T";	emc = 29
		elif em=='V':	emulsion = "5242/7242 Vision Intermediate";	emc = 42
		elif em=='U':	emulsion = "5260 Vision 2 500T";	emc = 60
		elif em=='E':	emulsion = "5263/7263 Vision 500T";	emc = 63
		elif em=='C':	emulsion = "7265";	emc = 65
		elif em=='D':	emulsion = "7266";	emc = 66
		elif em=='G':	emulsion = "6284/7284 Vision Expression 500T";	emc = 84
		elif em=='A':	emulsion = "5285 100D";	emc = 85
		elif em=='I':	emulsion = "7299";	emc = 99
		else:	emulsion = "unknown"
	elif ma == 'F':
		manufacturer = "Fuji"
		if not mac:	mac = 3
		else:
			if gauge==16:	mac=13
			elif gauge==35:	mac=3
			elif gauge==65:	mac=23
		if (not emc) and em=='I':	emulsion = "8x01/8x02 F-CI / 8503/4503 ETERNA CI Intermediate"
		elif (not emc) and em=='N':	emulsion = "F-series / ETERNA series / REALA 500D"
		elif emc==1:	emulsion = "F-CI (8501, 8601, 8701)";	em = 'I'
		elif emc==2:	emulsion = "F-CI (8502, 8602, 8702)";	em = 'I'
		elif emc==3:	emulsion = "ETERNA CI Intermediate (8503, 4503)";	em = 'I'
		elif emc==10:	emulsion = "F-64";	em = 'N'
		elif emc==11:	emulsion = "ETERNA RDI Digital Intermediate (8511, 4511)";	em = 'I'
		elif emc==13:	emulsion = "F-CI";	em = 'I'
		elif emc==14:	emulsion = "F-500";	em = 'N'
		elif emc==20:	emulsion = "F-64D";	em = 'N'
		elif emc==21:	emulsion = "F-64D (8521, 8621, 8721)";	em = 'N'
		elif emc==22:	emulsion = "F-64D (8522, 8622)";	em = 'N'
		elif emc==30:	emulsion = "F-125";	em = 'N'
		elif emc==31:	emulsion = "F-125 (8531, 8631, 8731)";	em = 'N'
		elif emc==32:	emulsion = "F-125 (8632, 8632)";	em = 'N'
		elif emc==40:	emulsion = "VELVIA color reversal (8540)";	em = 'R'
		elif emc==43:	emulsion = "ETERNA Vivid160 (8543, 8643)";	em = 'N'
		elif emc==47:	emulsion = "ETERNA Vivid500 (8647)";	em = 'N'
		elif emc==50:	emulsion = "F-250";	em = 'N'
		elif emc==51:	emulsion = "F-250 (8551, 8651, 8751)";	em = 'N'
		elif emc==52:	emulsion = "F-250 (8552, 8652)";	em = 'N'
		elif emc==53:	emulsion = "ETERNA 250 (8553, 8653)";	em = 'N'
		elif emc==60:	emulsion = "F-250D";	em = 'N'
		elif emc==61:	emulsion = "F-250D (8561, 8661, 8761)";	em = 'N'
		elif emc==62:	emulsion = "F-250D (8562, 8662)";	em = 'N'
		elif emc==63:	emulsion = "ETERNA 250D (8563, 8663)";	em = 'N'
		elif emc==70:	emulsion = "F-500 (8570, 8670, 8770)";	em = 'N'
		elif emc==71:	emulsion = "F-500 (8571, 8671)";	em = 'N'
		elif emc==72:	emulsion = "F-500 (8572, 8672)";	em = 'N'
		elif emc==73:	emulsion = "ETERNA 500 (8573, 8673)";	em = 'N'
		elif emc==82:	emulsion = "F-400 (8582, 8682)";	em = 'N'
		elif emc==83:	emulsion = "ETERNA 400 (8583, 8683)";	em = 'N'
		elif emc==92:	emulsion = "REALA 500D (8592, 8692)";	em = 'N'
		else:	emulsion = "unknown"
	elif ma == '?':	manufacturer = "unknown"
	else:	return None
	if not hKK:
		hKK = ma+em
		if RollNo:
			hKK += ' '+("%06d"%RollNo)[0:2]+' '+("%06d"%RollNo)[2:6]
			if footage:
				hKK += ' '+("%04d"%footage)[0:4]
				if frameNo:
					hKK += '+'+("%02d"%frameNo)[0:2]
					if perfOff:	hKK += '.'+("%02d"%perfOff)[0:2]
	ret = {	"KeyKode":hKK, "by":manufacturer, "gauge":gauge	}
	if emulsion:	ret["emulsion"] = emulsion
	if RollNo:	ret["reel#"] = RollNo
	if footage:	ret["foot"] = footage
	if frameNo:
		ret["frame"] = frameNo
		if perfOff:	ret["perf"] = perfOff
		else:	ret["perf"] = 0
	else:	ret["frame"] = 0;	ret["perf"] = 0
	if mac:	ret["by#"] = mac
	if emc:	ret["emulsion#"] = emc
	if mac:
		EC = ("%02d"%mac)[0:2]
		if emc:
			EC += ("%02d"%emc)[0:2]
			if RollNo:
				EC += ("%06d"%RollNo)[0:6]
				if footage:
					EC += ("%04d"%footage)[0:4]
					if frameNo:
						EC += ("%02d"%frameNo)[0:2]
						if perfOff:	EC += ("%02d"%perfOff)[0:2]
		ret["EdgeCode"] = EC
	return ret



#  Input drop-frame TimeCode is to be specified as SMPTE standard notation (i.e.
#with ';' instead of ':') and is output the same. For non-TimeCode inputs (for
#example if supplied as stock length rather than duration), use 'dfs' instead of
#'fps' in the frame-rate argument (which is instead ignored for TimeCode input).
#Frame rates such as 23.98, 29.97 and 59.94 are *not* automatically interpreted
#as being drop-frame (so input them as, for example, '29.97dfs' if so intended).
def syntax():
	print """filmcalc 0.6 - Film stock & frames command-line calculator
Copyright (C) 2009 Walter Arrighetti, Technicolor Digital Intermediates

  Usage: filmcalc [length [NNmm]] | [keykode [Lp]]  [FFfps|Hz]
         filmcalc length1|time1|keykode +|- length2|time2 [FFfps|Hz] [Lp]
         filmcalc length1|time1 *|/ multiple [FFfps|Hz]

Quick conversion between TimeCode, KeyKode, frames, feet and metres of film stock, or simple arithmetics between two TimeCodes/KeyKodes.

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

  If no arithmetic operations are specified, filmcal reports the film length in
both SMPTE TimeCode, frames' number and film length in feet and metres. Some
measures depend on film gauge, perforations and/or frame rate; others do not.
  Film length/duration conversions and divisions, as well as calculations with
non-integer frame rates, *always* produce down-rounded frames/TimeCode results.
  Arithmetic operations can be performed between same-size and -frame-rate
stock only. Examples of arithmetic operations' syntax include:

       45:02.19 + 52:48.16 [24Hz]   =    01:37:51.11    =  140915 frames
          64867 + 52:48.16          =    01:37:51.11    =  140915 frames
    01:12:36.06 - 50564 30fps       =       44:30.22    =  80122 frames
EJ2296111802+11 - 18.2 3p           = EJ2296111801+16.1 =  28816 frames
       06:05.12 * 2                 =       12:11       =  17544 frames
       03:45.06 / 3 25Hz            =       01:15.02    =  1877 frames
"""
	sys.exit(9)

mul,scale,drop,fd,perf,gauge = 16,24.,False,False,4,35
timeregexp = re.compile(r"((?P<hh>\d+)[:;])?(?P<mm>\d{1,2})[:;](?P<ss>\d{1,2})(\.(?P<ff>\d{1,2}))?")
KKre = re.compile(r"(?P<manfr>[A-Za-z?])(?P<emuls>[A-Za-z?])(?:(?P<roll>\d{6})(?:(?P<foot>\d{4})(?:\+(?P<frame>\d{1,2})(?:\.(?P<perf>\d{1,2}))?)?)?)?")
KK = None

if not (2<=len(sys.argv)<=7):	syntax()

for n in range(2,len(sys.argv)):
	if sys.argv[n]=='35mm':	gauge, perf = 35, 4
	elif sys.argv[n]=='16mm':	gauge, perf = 16, 1
	elif sys.argv[n]=='65mm':	gauge, perf = 65, 5
	elif sys.argv[n][-3:]=='fps':	scale=float(sys.argv[n][:-3])
	elif sys.argv[n][-2:]=='Hz':	scale=float(sys.argv[n][:-2])
	elif sys.argv[n][-3:]=='fps' and unicode(sys.argv[n][:-3]).isnumeric():
		scale=float(sys.argv[n][:-3])
	elif sys.argv[n][-2:]=='Hz' and unicode(sys.argv[n][:-2]).isnumeric():
		scale=float(sys.argv[n][:-2])
	elif sys.argv[n].lower().endswith('p') and sys.argv[n][:-1].isdigit():
		perf = int(sys.argv[n][:-1])
if gauge==35 and perf==4:	mul = 16
elif gauge==16 and perf==1:	mul = 40
elif gauge==65 and perf==5:	mul = 12.8
else:
	if gauge==35:	mul = 64./perf		#	35mm  ==  64 perforations / foot
	elif gauge==16:	mul = 40./perf	#	16mm  ==  40 perforations / foot
	else:	mul = 64./perf				#	65mm  ==  64 perforations / foot


if 4<=len(sys.argv)<=7 and (sys.argv[2] in ops) and (sys.argv[1].isdigit() or (sys.argv[1][-1]=='m' and sys.argv[1][:-1].isdigit()) or (sys.argv[1][-2:]=='ft' and sys.argv[1][:-2].isdigit()) or timeregexp.match(sys.argv[1]) or KKre.match(string.replace(sys.argv[1],' ',''))):
	negative = False
#	if len(sys.argv)==5:
#		else:	syntax()
	if sys.argv[1].isdigit():	TC1 = int(sys.argv[1])
	elif KKre.match(string.replace(sys.argv[1],' ','')):
		KK = KeyKode(sys.argv[1])
		print "\nKeyKode:     %s          [ EdgeCode: %s ]"%(KK["KeyKode"],KK["EdgeCode"])
		print "Film Stock:  %s %s  (%dmm)"%(KK["by"],KK["emulsion"],KK["gauge"])
		print "Reel No.: %d    Length: %dft    Offset:  %02d frames + %02d perfs."%(KK["reel#"],KK["foot"],KK["frame"],KK["perf"])
		if KK["gauge"]==35:	gauge, mul = 35, 16
		elif KK["gauge"]==16:	gauge, mul = 16, 40
		elif KK["gauge"]==65:	gauge, mul = 65, 12.8
		TC1 = int(KK["foot"]*mul)+KK["frame"]
	elif sys.argv[1][-1] == 'm' and unicode(sys.argv[1][:-1]).isnumeric():
		metres = float(sys.argv[1][:-1])
		feet = 3.2808*metres
		frames = int(feet*mul)
		TC1 = frames
	elif sys.argv[1][-2:] == 'ft' and unicode(sys.argv[1][:-2]).isnumeric():
		feet = float(sys.argv[1][:-2])
		frames = int(feet*mul)
		metres = .3048*feet
		TC1 = frames
	else:	TC1 = TC2frame(sys.argv[1],scale)

	if sys.argv[2]=='+' and (sys.argv[3].isdigit() or timeregexp.match(sys.argv[3])!=None):
		if sys.argv[3].isdigit():	TC2=int(sys.argv[3])
		else:	TC2 = TC2frame(sys.argv[3],scale)
		frames = TC1+TC2
	elif sys.argv[2]=='-' and (sys.argv[3].isdigit() or timeregexp.match(sys.argv[3])!=None):
		if sys.argv[3].isdigit():	TC2=int(sys.argv[3])
		else:	TC2 = TC2frame(sys.argv[3],scale)
		frames = TC1-TC2
		if frames<0:
			negative = True
			frames = -frames
	elif sys.argv[2]=='*' and sys.argv[3].isdigit():
		TC2 = int(sys.argv[3])
		frames = TC1*TC2
	elif sys.argv[2]=='/' and sys.argv[3].isdigit():
		TC2 = int(sys.argv[3])
		frames = TC1//TC2
	else:	syntax()
	TCout = frame2TC(frames, scale, fd, True)

	if sys.argv[2] in "*/":
		print "\n  %s  %c  %d  ==  %s @ %dfps  ==  %d" % (frame2TC(TC1,scale,fd,True), sys.argv[2], TC2, TCout, scale, frames),
	else:
		print "\n  %s  %c  %s  ==  %s @ %dfps  ==  %d" % (frame2TC(TC1,scale,fd,True), sys.argv[2], frame2TC(TC2,scale,fd,True), TCout, scale, frames),
	if not (gauge==35 and perf==4):	print "fr. (%dmm %dp)"%(gauge,perf)
	else:	print "frames"
#	if timeregexp.match(sys.argv[1]) and timeregexp.match(sys.argv[3]):
#		print "\n  %s  %c  %s  ==  %s @ %dHz  ==  %d frames\n" % (frame2TC(TC1,scale,fd,True), sys.argv[2], frame2TC(TC2,scale,fd,True), TCout, scale, frames)
#	elif sys.argv[1].isdigit() and timeregexp.match(sys.argv[3]):
#		print "\n  %d  %c  %s  ==  %s @ %dHz  ==  %d frames\n" % (TC1, sys.argv[2], frame2TC(TC1,scale,fd,True), TCout, scale, frames)
#	elif timeregexp.match(sys.argv[1]) and sys.argv[3].isdigit():
#		print "\n  %s  %c  %d  ==  %s @ %dHz  ==  %d frames\n" % (frame2TC(TC1,scale,fd,True), sys.argv[2], TC2, TCout, scale, frames)
#	else:
#		print "\n  %d  %c  %d  ==  %s @ %dHz  ==  %d frames\n" % (TC1, sys.argv[2], TC2, TCout, scale, frames)
	sys.exit(0)

#if len(sys.argv)==3:
#	for n in range(2,len(sys.argv)):
#		if sys.argv[n]=='35mm':	gauge, perf = 35, 4
#		elif sys.argv[n]=='16mm':	gauge, perf = 16, 1
#		elif sys.argv[n]=='65mm':	gauge, perf = 65, 5
#		elif sys.argv[n][-3:]=='fps':	scale=float(sys.argv[n][:-3])
#		elif sys.argv[n][-2:]=='Hz':	scale=float(sys.argv[n][:-2])
#		elif sys.argv[n].lower().endswith('p') and sys.argv[n][:-1].isdigit():
#			perf = int(sys.argv[n][:-1])
#		else:	syntax()

if gauge==35 and perf==4:	mul = 16
elif gauge==16 and perf==1:	mul = 40
elif gauge==65 and perf==5:	mul = 12.8
else:
	if gauge==35:	mul = 64./perf		#	35mm  ==  64 perforations / foot
	elif gauge==16:	mul = 40./perf	#	16mm  ==  40 perforations / foot
	else:	mul = 64./perf				#	65mm  ==  64 perforations / foot

if timeregexp.match(sys.argv[1])!=None:
	frames = TC2frame(sys.argv[1],scale)
	feet = float(frames)/mul
	metres = .3048*feet
elif sys.argv[1].isdigit():
	frames = int(sys.argv[1])
	feet = float(frames)/mul
	metres = .3048*feet
elif sys.argv[1][-1] == 'm' and unicode(sys.argv[1][:-1]).isnumeric():
	metres = float(sys.argv[1][:-1])
	feet = 3.2808*metres
	frames = int(feet*mul)
elif sys.argv[1][-2:] == 'ft' and unicode(sys.argv[1][:-2]).isnumeric():
	feet = float(sys.argv[1][:-2])
	frames = int(feet*mul)
	metres = .3048*feet
else:
	syntax()

timestr = frame2TC(frames,scale,fd,True)
print "\n  %s  =  %d frames  =  %.1f feet  =  %.1f metres " % (timestr, frames, feet, metres),
if not (scale==24 and perf==4):
	if type(scale)==int or scale in [1., 5.,10.,15.,20.,24.,25.,30.,48.,50.,60.,72.,96.,100.,120.]:	print "  (%dfps, %dp)\n"%(scale,perf)
	else:	print "(%.02ffps, %dp)\n"%(scale,perf)
else:	print '\n'

#exit(0)
