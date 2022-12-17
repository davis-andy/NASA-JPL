using System;
using System.Globalization;
using NationalInstruments.Visa;

namespace DAQ_modules
{
    public class DAQ970
    {
        /*   Global variables for DAQ Instrument   */

        //Message Based Session and Resource Manager
        MessageBasedSession mbSession;
        ResourceManager rmSession = new ResourceManager();

        string idnString, USBAddress;
        string result;

        //Temperature set points for tests
        public int[] Etemps = { -200, -80, 0, 200, 1000 };
        public int[] Jtemps = { -210, -80, 0, 200, 1200 };
        public int[] Ktemps = { -195, -80, 0, 200, 1200 };
        public int[] Ttemps = { -200, -80, 0, 100, 400 };




        /*   DAQ Functions   */

        //DAQ Initializer
        public DAQ970()
        {
            //getIDN();
        }

        //DAQ Initializer with USB
        public DAQ970(string address)
        {
            getIDN(address);
        }

        //Get Set variables
        public string IDN => idnString;
        public string Address { get => USBAddress; set => USBAddress = value; }

        //Retrieve DAQ's ID
        public void getIDN(string address)
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

        public void Setup(string type, int channel) { mbSession.RawIO.Write(String.Format("CONF:TEMP:TC {0},(@{1})", type, channel)); } //E, J, K, T  --  201...220

        public void Nplc(int npl) { mbSession.RawIO.Write(String.Format("TEMP:NPLC {0}", npl)); } //10

        public void Count() { mbSession.RawIO.Write("TRIG:COUN 5"); } //Five measurements taken

        public void Monitor(int channel) //201...220
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
            averageReading = decimal.Round(averageReading, 2);

            return averageReading;
        }




        /*   Pass / Fail conditions   */

        public string ETolerances(int applied, float measure)
        {
            switch (applied)
            {
                case -200:
                    if (measure >= -201.4 && measure <= -198.6) result = "Pass";
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
                case 1000:
                    if (measure >= 999.0 && measure <= 1001.0) result = "Pass";
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
                case -210:
                    if (measure >= -211.6 && measure <= -208.4) result = "Pass";
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

        public string KTolerances(int applied, float measure)
        {
            switch (applied)
            {
                case -195:
                    if (measure >= -196.7 && measure <= -193.3) result = "Pass";
                    else result = "Fail";
                    break;
                case -80:
                    if (measure >= -80.9 && measure <= -79.1) result = "Pass";
                    else result = "Fail";
                    break;
                case 0:
                    if (measure >= -0.9 && measure <= 0.9) result = "Pass";
                    else result = "Fail";
                    break;
                case 200:
                    if (measure >= 199.1 && measure <= 200.9) result = "Pass";
                    else result = "Fail";
                    break;
                case 1200:
                    if (measure >= 1199.1 && measure <= 1200.9) result = "Pass";
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
                case -200:
                    if (measure >= -201.7 && measure <= -198.3) result = "Pass";
                    else result = "Fail";
                    break;
                case -80:
                    if (measure >= -80.9 && measure <= -79.1) result = "Pass";
                    else result = "Fail";
                    break;
                case 0:
                    if (measure >= -0.9 && measure <= 0.9) result = "Pass";
                    else result = "Fail";
                    break;
                case 100:
                    if (measure >= 99.1 && measure <= 100.9) result = "Pass";
                    else result = "Fail";
                    break;
                case 400:
                    if (measure >= 399.1 && measure <= 400.9) result = "Pass";
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
