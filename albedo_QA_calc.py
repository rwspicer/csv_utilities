#!/usr/bin/python -tt
"""
Albedo QA
rawser spicer & Bob Busey
created: 2017/10/19
modified:

     a utility to cull albedo values after dark
"""
from scipy.stats import linregress
import numpy as np
from csv_lib.dat_file import DatFile
from math import pi
from csv_lib.utility import utility_base
from csv_lib.csv_file import CsvFile
from datetime import datetime
import math as Math

HELP = """
    correct away night time values from albedo.

    example usage:
    >> python albedo_QA_calc.py --infile=<.dat file> --outfile=<.csv file>
     --lat=#.# --long=#.#

    flags:
    --infile
        the input .dat file

    --outfile
        the output .csv file

    --lat
        latitude (north is positive) value in decimal degrees.
    --long
        longitude (east is positive) value in decimal degrees.

"""


class AlbedoFix(utility_base):
    """
        a utility to calcualte the thermal conductivity
    """
    def __init__(self):
        """
             Sets up utility

        Preconditions:
            none
        Postconditions:
            utility is ready to be run
        """
        super(AlbedoFix, self).__init__(" AlBedoFix " ,
                    ("--infile", "--outfile",  "--lat", "--long") ,
                    ( ),
                    HELP)


    def main(self):
        """
        main body of utiliy.

        Preconditions:
            utility setup
        Postconditions:
            utility is run
        """
        # set up
        data = DatFile(self.commands["--infile"],"4")
        latitude = float(self.commands["--lat"])
        longitude = float(self.commands["--long"])
        columns = [data.getColumn(0),
                   np.array(data.getColumn(1)).astype(float)]
        # test out put
        out_file = CsvFile(self.commands["--outfile"], opti = True)
        last_date = datetime(1000,1,1)
        if not out_file.exists():
            fd = open(self.commands["--infile"])
            first_line = fd.read().split(",")[0:2]
            first_line[1] += "\n"
            out_file.set_header([ first_line,
                                  ("timestamp", "Albedo\n"),
                                  ("","\n"),
                                  ("","Avg\n")])
        else:
            last_date = out_file[0][-1]
        alb_vals = []
        alb_dates = []
        idx = 0
        while idx < len(columns[0]):
            compVal = columns[0][idx]
            # I'm not sure what this does...
            try:
                if datetime.strptime(compVal,'"%Y-%m-%d %H:%M:%S"') <= last_date:
                    idx = idx + 1
                    continue
            except:
                if datetime.strptime(compVal,'%Y-%m-%d %H:%M:%S') <= last_date:
                    idx = idx + 1
                    continue

            # this point is where the magic happens.
            raw_index = float(columns[1][idx])
            if raw_index < 0 : raw_index = 6999.0
            if raw_index >1 : raw_index = 6999.0
            try:
                isdark = self.calc_SunAngle(latitude,longitude,datetime.strptime(compVal,'"%Y-%m-%d %H:%M:%S"'))
            except:
                isdark = self.calc_SunAngle(latitude,longitude,datetime.strptime(compVal,'%Y-%m-%d %H:%M:%S'))
            if isdark == 6999 :
                alb_vals.append(6999.0)
            else:
                alb_vals.append(raw_index)
            if len(compVal) == 21 :
                alb_dates.append(datetime.strptime(compVal,'"%Y-%m-%d %H:%M:%S"'))
            else:
                alb_dates.append(datetime.strptime(compVal,'%Y-%m-%d %H:%M:%S'))
            idx= idx+1
        # save
        out_file.add_dates(alb_dates)
        out_file.add_data(1,alb_vals)
        out_file.append()

    def calc_SunAngle(self, latitude,longitude, curdate) :
        """
            Eliminates data where sun is below the horizon threshold.

        Arguments
            value:  the computed indexvalue
            latitude: latitude in decimal degrees
            longitude: longitude in decimal degrees
            curdate:  date & time of current observation

        Returns 6999 if sun is below horizon threshold otherwise just the data.
        Equations from NOAA ESRL Solar Position Calculator:
        https://www.esrl.noaa.gov/gmd/grad/solcalc/azel.html
        ... there is one thing I modified, which is the final check for daylight / darkness.
        I adjusted it by eye a bit until less of the low sun angle noise is in the final data set.
        """
        longitude = longitude * -1
        tupdate =  curdate.timetuple()
        julianday = tupdate.tm_yday
        hh = tupdate.tm_hour
        mm = tupdate.tm_min
        timenow = hh + mm / 60.0
        T = self.calcTimeJulianCent(julianday + timenow / 24.0)
        R = self.calcSunRadVector(T)
        alpha = self.calcSunRtAscension(T)
        theta = self.calcSunDeclination(T)
        Etime = self.calcEquationOfTime(T)
        eqTime = Etime
        solarDec = theta
        earthRadVec = R
        solarTimeFix = eqTime - 4.0 * longitude
        trueSolarTime = hh * 60.0 + mm + solarTimeFix
        while (trueSolarTime > 1440.0) :
            trueSolarTime -= 1440.0
        hourAngle = trueSolarTime / 4.0 - 180.0
        if (hourAngle < -180.0) :
	        hourAngle += 360.0
        haRad = self.degToRad(hourAngle)
        csz = Math.sin(self.degToRad(latitude)) *  \
		        Math.sin(self.degToRad(solarDec)) +  \
		        Math.cos(self.degToRad(latitude)) *  \
		        Math.cos(self.degToRad(solarDec)) * Math.cos(haRad)
        if (csz > 1.0) :
	        csz = 1.0
        elif (csz < -1.0) :
	        csz = -1.0
        zenith = self.radToDeg(Math.acos(csz))
        azDenom = ( Math.cos(self.degToRad(latitude)) *  \
					Math.sin(self.degToRad(zenith)) )
        if (abs(azDenom) > 0.001) :
	        azRad = (( Math.sin(self.degToRad(latitude)) * \
		        Math.cos(self.degToRad(zenith)) ) - \
		        Math.sin(self.degToRad(solarDec))) / azDenom
	        if (abs(azRad) > 1.0) :
		        if (azRad < 0) :
			        azRad = -1.0
		        else :
			        azRad = 1.0
	        azimuth = 180.0 - self.radToDeg(Math.acos(azRad))
	        if (hourAngle > 0.0) :
		        azimuth = -azimuth
        else :
	        if (latitude > 0.0) :
		        azimuth = 180.0
	        else :
		        azimuth = 0.0
        if (azimuth < 0.0) :
            azimuth += 360.0
        exoatmElevation = 90.0 - zenith
        if (exoatmElevation > 85.0) :
	        refractionCorrection = 0.0
        else :
	        te = Math.tan (self.degToRad(exoatmElevation))
	        if (exoatmElevation > 5.0) :
		        refractionCorrection = 58.1 / te - 0.07 / (te*te*te) + \
			        0.000086 / (te*te*te*te*te)
	        elif (exoatmElevation > -0.575) :
		        refractionCorrection = 1735.0 + exoatmElevation * \
			        (-518.2 + exoatmElevation * (103.4 +  \
			        exoatmElevation * (-12.79 +  \
			        exoatmElevation * 0.711) ) )
	        else :
		        refractionCorrection = -20.774 / te
	        refractionCorrection = refractionCorrection / 3600.0
	        solarZen = zenith - refractionCorrection
        if(solarZen < 80.0) :  #had been 108.0 on web page... lowered the value to reduce sensor noise at lower sun angles
            # Daylight
            return 1
        else :
            # DARK
            return 6999


    def calcSunTrueAnomaly(self,t) :
        m = self.calcGeomMeanAnomalySun(t)
        c = self.calcSunEqOfCenter(t)
        v = m + c
        return v
    def calcGeomMeanAnomalySun(self,t) :
        M = 357.52911 + t * (35999.05029 - 0.0001537 * t)
        return M
    def calcEccentricityEarthOrbit(self,t) :
        e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
        return e
    def calcTimeJulianCent (self,jd) :
        T = (jd - 2451545.0)/36525.0
        return T
    def calcSunRadVector(self,t) :
        v = self.calcSunTrueAnomaly(t)
        e = self.calcEccentricityEarthOrbit(t)
        R = (1.000001018 * (1 - e * e)) / (1 + e * Math.cos(self.degToRad(v)))
        return R
    def calcSunEqOfCenter(self,t) :
        m = self.calcGeomMeanAnomalySun(t)
        mrad = self.degToRad(m)
        sinm = Math.sin(mrad)
        sin2m = Math.sin(mrad+mrad)
        sin3m = Math.sin(mrad+mrad+mrad)
        C = sinm * (1.914602 - t * (0.004817 + 0.000014 * t)) + sin2m * (0.019993 - 0.000101 * t) + sin3m * 0.000289
        return C
    def calcGeomMeanLongSun(self,t) :
        L0 = 280.46646 + t * (36000.76983 + 0.0003032 * t)
        while(L0 > 360.0) :
	        L0 -= 360.0
        while(L0 < 0.0) :
	        L0 += 360.0
        return L0
    def calcSunApparentLong(self,t) :
        o = self.calcSunTrueLong(t)
        omega = 125.04 - 1934.136 * t
        LLlambda = o - 0.00569 - 0.00478 * Math.sin(self.degToRad(omega))
        return LLlambda
    def calcMeanObliquityOfEcliptic(self,t) :
        seconds = 21.448 - t*(46.8150 + t*(0.00059 - t*(0.001813)))
        e0 = 23.0 + (26.0 + (seconds/60.0))/60.0
        return e0
    def calcObliquityCorrection(self,t) :
        e0 = self.calcMeanObliquityOfEcliptic(t)
        omega = 125.04 - 1934.136 * t
        e = e0 + 0.00256 * Math.cos(self.degToRad(omega))
        return e
    def calcSunRtAscension(self,t) :
        e = self.calcObliquityCorrection(t)
        LLlambda = self.calcSunApparentLong(t)
        tananum = (Math.cos(self.degToRad(e)) * Math.sin(self.degToRad(LLlambda)))
        tanadenom = (Math.cos(self.degToRad(LLlambda)))
        alpha = self.radToDeg(Math.atan2(tananum, tanadenom))
        return alpha
    def calcSunDeclination(self,t) :
        e = self.calcObliquityCorrection(t)
        LLlambda = self.calcSunApparentLong(t)
        sint = Math.sin(self.degToRad(e)) * Math.sin(self.degToRad(LLlambda))
        theta = self.radToDeg(Math.asin(sint))
        return theta
    def calcEquationOfTime(self,t) :
        epsilon = self.calcObliquityCorrection(t)
        l0 = self.calcGeomMeanLongSun(t)
        e = self.calcEccentricityEarthOrbit(t)
        m = self.calcGeomMeanAnomalySun(t)
        y = Math.tan(self.degToRad(epsilon)/2.0)
        y *= y
        sin2l0 = Math.sin(2.0 * self.degToRad(l0))
        sinm   = Math.sin(self.degToRad(m))
        cos2l0 = Math.cos(2.0 * self.degToRad(l0))
        sin4l0 = Math.sin(4.0 * self.degToRad(l0))
        sin2m  = Math.sin(2.0 * self.degToRad(m))
        Etime = y * sin2l0 - 2.0 * e * sinm + 4.0 * e * y * sinm * \
            cos2l0 - 0.5 * y * y * sin4l0 - 1.25 * e * e * sin2m
        return self.radToDeg(Etime)*4.0
    def calcSunTrueLong(self,t) :
        l0 = self.calcGeomMeanLongSun(t)
        c = self.calcSunEqOfCenter(t)
        O = l0 + c
        return O
    def calcGeomMeanLongSun(self,t):
        L0 = 280.46646 + t * (36000.76983 + 0.0003032 * t)
        while(L0 > 360.0) :
	        L0 -= 360.0
        while(L0 < 0.0) :
	        L0 += 360.0
        return L0
    def degToRad(self,angleDeg) :
        return Math.pi * angleDeg / 180.0

    def radToDeg(self,angleRad) :
        return 180.0 * angleRad / Math.pi

if __name__ == "__main__":
    AlbedoFix().run()
