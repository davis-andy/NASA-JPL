using System;
using System.Globalization;
using NationalInstruments.Visa;

namespace DAQ_modules
{
    class _34980
    {
        /*   Global variables for 34970 Instrument   */

        //Message Based Session and Resource Manager
        MessageBasedSession mbSession;
        ResourceManager rmSession = new ResourceManager();

        string idnString, result;

        //Temperature set points for tests
        public int[] Etemps = { -190, -80, 0, 200, 990 };
        public int[] Jtemps = { -200, -80, 0, 200, 1190 };
        public int[] Ktemps = { -190, -80, 0, 200, 1200 };
        public int[] Ttemps = { -190, -80, 0, 100, 395 };




        /*   34980 Functions   */

        //34980 Initializer
        public _34980()
        {
            //getIDN();
        }

        //34980 Initializer with GPIB/USB
        public _34980(string address)
        {
            getIDN(address);
        }

        //Retrieve 34980's ID
        protected void getIDN(string address)
        {
            try
            {
                mbSession = (MessageBasedSession)rmSession.Open(address);
                mbSession.RawIO.Write("*IDN?");
                idnString = mbSession.RawIO.ReadString();
            }
            catch (Exception E) { Console.WriteLine(E.Message); }
        }




        /*   SCPI Commands   */

        public void Reset() { mbSession.RawIO.Write("*RST"); }

        public void Setup(string type, int channel) { mbSession.RawIO.Write(String.Format("CONF:TEMP TC,{0},(@{1})", type, channel)); } //E, J, K, T  --  2001...2020

        public void Ref(string source, int channel) { mbSession.RawIO.Write(String.Format("TEMP:TRAN:TC:RJUN:TYPE {0},(@{1})", source, channel)); }

        public void Nplc(int npl) { mbSession.RawIO.Write(String.Format("TEMP:NPLC {0}", npl)); } //10

        public void Count() { mbSession.RawIO.Write("TRIG:COUN 5"); } //Five measurements taken

        public void Scan(int channel) { mbSession.RawIO.Write(String.Format("ROUT:SCAN (@{0})", channel)); }

        public void Monitor(int channel) //2001...2020
        {
            mbSession.RawIO.Write(String.Format("ROUT:MON (@{0})", channel));
            mbSession.RawIO.Write("ROUT:MON:STAT ON");
        }

        public string[] Read() //Split measurements into an array
        {
            mbSession.RawIO.Write("READ?");
            string readRaw = mbSession.RawIO.ReadString().Trim();
            string[] readArray = readRaw.Split(',');

            return readArray;
        }




        /*   Calculations   */

        //Iterate through each array index from Read function and use Convert Reading function
        public double[] ArrayConversion(string[] array)
        {
            double[] convert = new double[5];

            for (int i = 0; i < array.Length; i++)
            {
                convert[i] = Double.Parse(array[i], NumberStyles.Any);

                if (convert[i] > 2000)
                    convert[i] = -9999;
            }

            return convert;
        }

        //Find the average of the readings
        public decimal AverageReading(double[] array)
        {
            decimal averageReading;
            decimal addReading = 0;

            for (int i = 0; i < array.Length; i++)
            {
                decimal currReading = (decimal)array[i];
                addReading += currReading;
            }

            averageReading = addReading / array.Length;
            averageReading = decimal.Round(averageReading, 1);

            return averageReading;
        }




        /*   Pass / Fail conditions   */

        public string ETolerances(int applied, float measure)
        {
            switch (applied)
            {
                case -190:
                    if (measure >= -191.5 && measure <= -188.5) result = "Pass";
                    else result = "Fail";
                    break;
                case -80:
                    if (measure >= -81.0 && measure <= -79.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 0:
                    if (measure >= -1.0 && measure <= 1.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 200:
                    if (measure >= 199.0 && measure <= 201.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 990:
                    if (measure >= 989.0 && measure <= 991.0) result = "Pass";
                    else result = "Fail";
                    break;
                default:
                    result = "Fail";
                    break;

            }

            return result;
        }

        public string JTolerances(int applied, float measure)
        {
            switch (applied)
            {
                case -200:
                    if (measure >= -201.2 && measure <= -198.8) result = "Pass";
                    else result = "Fail";
                    break;
                case -80:
                    if (measure >= -81.0 && measure <= -79.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 0:
                    if (measure >= -1.0 && measure <= 1.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 200:
                    if (measure >= 199.0 && measure <= 201.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 1190:
                    if (measure >= 1189.0 && measure <= 1191.0) result = "Pass";
                    else result = "Fail";
                    break;
                default:
                    result = "Fail";
                    break;

            }

            return result;
        }

        public string KTolerances(int applied, float measure)
        {
            switch (applied)
            {
                case -190:
                    if (measure >= -191.5 && measure <= -188.5) result = "Pass";
                    else result = "Fail";
                    break;
                case -80:
                    if (measure >= -81.0 && measure <= -79.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 0:
                    if (measure >= -1.0 && measure <= 1.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 200:
                    if (measure >= 199.0 && measure <= 201.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 1200:
                    if (measure >= 1199.0 && measure <= 1201.0) result = "Pass";
                    else result = "Fail";
                    break;
                default:
                    result = "Fail";
                    break;

            }

            return result;
        }

        public string TTolerances(int applied, float measure)
        {
            switch (applied)
            {
                case -190:
                    if (measure >= -191.5 && measure <= -188.5) result = "Pass";
                    else result = "Fail";
                    break;
                case -80:
                    if (measure >= -81.0 && measure <= -79.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 0:
                    if (measure >= -1.0 && measure <= 1.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 100:
                    if (measure >= 99.0 && measure <= 101.0) result = "Pass";
                    else result = "Fail";
                    break;
                case 395:
                    if (measure >= 394.0 && measure <= 396.0) result = "Pass";
                    else result = "Fail";
                    break;
                default:
                    result = "Fail";
                    break;

            }

            return result;
        }
    }
}