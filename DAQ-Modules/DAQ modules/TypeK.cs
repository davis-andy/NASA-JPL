using System.Threading;
using System.Drawing;
using Excel = Microsoft.Office.Interop.Excel;

namespace DAQ_modules
{
    class TypeK : Test
    {
        /*   Global variables for Type K Tests   */

        //Instrument variables
        private Ectron ectron;
        private DAQ970 daq;
        private _34970 _34970;
        private _34980 _34980;
        MainForm FormM;

        //Excel variables
        Excel.Worksheet uncert1, uncert2, uncert3, uncert4, uncert5;

        //Test variables
        decimal reading;
        public string result;
        public string[] KvalsArray;
        public double[] Kvals;

        //Get Set variable
        public override string Name => "Type K";




        /*   Type K Test functions   */

        //Type K Test Initializer
        public TypeK(Ectron ectron, DAQ970 daq, _34970 _34970, _34980 _34980, MainForm pForm, 
            Excel.Worksheet uncert1, Excel.Worksheet uncert2, Excel.Worksheet uncert3, Excel.Worksheet uncert4, Excel.Worksheet uncert5)
        {
            this.ectron = ectron;
            this.daq = daq;
            this._34970 = _34970;
            this._34980 = _34980;
            FormM = pForm;
            this.uncert1 = uncert1;
            this.uncert2 = uncert2;
            this.uncert3 = uncert3;
            this.uncert4 = uncert4;
            this.uncert5 = uncert5;
        }

        //Main test function
        public override bool RunTest()
        {
            //channel = FormM.convertToInt(FormM.cmbChannelK.Text);

            //Start the test
            FormM.WriteToOutput("  Running Type K tests...\n\r");

            //Message to insert correct connector
            FormM.insertConnector("K");

            //Configure Ectron to correct Thermocouple type and turn off Standby
            ectron.Temp(0);
            ectron.Type("K");
            ectron.Standby("OFF");

            //Set up DAQ Mainframe with correct channel and read settings
            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    daq.Reset();
                    daq.Setup("K", FormM.channel[2]);
                    daq.Nplc(10);
                    daq.Count();
                    daq.Monitor(FormM.channel[2]);

                    uncert1.Name = "Type K (-195°C)";
                    break;
                case 2:
                    //34970 Mainframe
                    _34970.Reset();
                    _34970.Setup("K", FormM.channel[2]);
                    _34970.Nplc(10);
                    _34970.Count();
                    _34970.Monitor(FormM.channel[2]);

                    uncert1.Name = "Type K (-190°C)";
                    break;
                case 3:
                    //34980 Mainframe
                    _34980.Reset();
                    _34980.Setup("K", FormM.channel[2]);
                    _34980.Ref("INT", FormM.channel[2]);
                    _34980.Nplc(10);
                    _34980.Count();
                    _34980.Scan(FormM.channel[2]);
                    _34980.Monitor(FormM.channel[2]);

                    uncert1.Name = "Type K (-190°C)";
                    break;
            }

            //Let electricity dissipate to get more accurate readings
            FormM.Timer();
            Thread.Sleep((int)FormM.wait);




            /*   First set point   */

            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    ectron.Temp(daq.Ktemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ktemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = daq.Read();
                    Kvals = daq.ArrayConversion(KvalsArray);
                    reading = daq.AverageReading(Kvals);
                    result = daq.KTolerances(daq.Ktemps[0], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ktemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ktemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34970.Read();
                    Kvals = _34970.ArrayConversion(KvalsArray);
                    reading = _34970.AverageReading(Kvals);
                    result = _34970.KTolerances(_34970.Ktemps[0], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ktemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ktemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34980.Read();
                    Kvals = _34980.ArrayConversion(KvalsArray);
                    reading = _34980.AverageReading(Kvals);
                    result = _34980.KTolerances(_34980.Ktemps[0], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Kvals.Length; i++)
            {
                decimal currReading = (decimal)Kvals[i];
                uncert1.Cells[i + 6, "F"] = decimal.Round(currReading, 2);
            }

            //Print out results
            FormM.WriteToOutput(string.Format("  Measured Temp: {0}°C\n", reading));
            FormM.WriteToOutput("  Result: ");
            if (result == "Fail")
            {
                FormM.WriteToOutput(result + "\n\r", Color.Red);
            }
            else FormM.WriteToOutput(result + "\n\r");




            /*   Second set point   */

            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    ectron.Temp(daq.Ktemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ktemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = daq.Read();
                    Kvals = daq.ArrayConversion(KvalsArray);
                    reading = daq.AverageReading(Kvals);
                    result = daq.KTolerances(daq.Ktemps[1], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ktemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ktemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34970.Read();
                    Kvals = _34970.ArrayConversion(KvalsArray);
                    reading = _34970.AverageReading(Kvals);
                    result = _34970.KTolerances(_34970.Ktemps[1], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ktemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ktemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34980.Read();
                    Kvals = _34980.ArrayConversion(KvalsArray);
                    reading = _34980.AverageReading(Kvals);
                    result = _34980.KTolerances(_34980.Ktemps[1], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Kvals.Length; i++)
            {
                decimal currReading = (decimal)Kvals[i];
                uncert2.Cells[i + 6, "F"] = decimal.Round(currReading, 2);
            }

            //Print out results
            FormM.WriteToOutput(string.Format("  Measured Temp: {0}°C\n", reading));
            FormM.WriteToOutput("  Result: ");
            if (result == "Fail")
            {
                FormM.WriteToOutput(result + "\n\r", Color.Red);
            }
            else FormM.WriteToOutput(result + "\n\r");




            /*   Third set point   */

            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    ectron.Temp(daq.Ktemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ktemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = daq.Read();
                    Kvals = daq.ArrayConversion(KvalsArray);
                    reading = daq.AverageReading(Kvals);
                    result = daq.KTolerances(daq.Ktemps[2], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ktemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ktemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34970.Read();
                    Kvals = _34970.ArrayConversion(KvalsArray);
                    reading = _34970.AverageReading(Kvals);
                    result = _34970.KTolerances(_34970.Ktemps[2], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ktemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ktemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34980.Read();
                    Kvals = _34980.ArrayConversion(KvalsArray);
                    reading = _34980.AverageReading(Kvals);
                    result = _34980.KTolerances(_34980.Ktemps[2], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Kvals.Length; i++)
            {
                decimal currReading = (decimal)Kvals[i];
                uncert3.Cells[i + 6, "F"] = decimal.Round(currReading, 2);
            }

            //Print out results
            FormM.WriteToOutput(string.Format("  Measured Temp: {0}°C\n", reading));
            FormM.WriteToOutput("  Result: ");
            if (result == "Fail")
            {
                FormM.WriteToOutput(result + "\n\r", Color.Red);
            }
            else FormM.WriteToOutput(result + "\n\r");




            /*   Fourth set point   */

            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    ectron.Temp(daq.Ktemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ktemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = daq.Read();
                    Kvals = daq.ArrayConversion(KvalsArray);
                    reading = daq.AverageReading(Kvals);
                    result = daq.KTolerances(daq.Ktemps[3], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ktemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ktemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34970.Read();
                    Kvals = _34970.ArrayConversion(KvalsArray);
                    reading = _34970.AverageReading(Kvals);
                    result = _34970.KTolerances(_34970.Ktemps[3], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ktemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ktemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34980.Read();
                    Kvals = _34980.ArrayConversion(KvalsArray);
                    reading = _34980.AverageReading(Kvals);
                    result = _34980.KTolerances(_34980.Ktemps[3], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Kvals.Length; i++)
            {
                decimal currReading = (decimal)Kvals[i];
                uncert4.Cells[i + 6, "F"] = decimal.Round(currReading, 2);
            }

            //Print out results
            FormM.WriteToOutput(string.Format("  Measured Temp: {0}°C\n", reading));
            FormM.WriteToOutput("  Result: ");
            if (result == "Fail")
            {
                FormM.WriteToOutput(result + "\n\r", Color.Red);
            }
            else FormM.WriteToOutput(result + "\n\r");




            /*   Fifth set point   */

            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    ectron.Temp(daq.Ktemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ktemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = daq.Read();
                    Kvals = daq.ArrayConversion(KvalsArray);
                    reading = daq.AverageReading(Kvals);
                    result = daq.KTolerances(daq.Ktemps[4], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ktemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ktemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34970.Read();
                    Kvals = _34970.ArrayConversion(KvalsArray);
                    reading = _34970.AverageReading(Kvals);
                    result = _34970.KTolerances(_34970.Ktemps[4], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ktemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ktemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    KvalsArray = _34980.Read();
                    Kvals = _34980.ArrayConversion(KvalsArray);
                    reading = _34980.AverageReading(Kvals);
                    result = _34980.KTolerances(_34980.Ktemps[4], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Kvals.Length; i++)
            {
                decimal currReading = (decimal)Kvals[i];
                uncert5.Cells[i + 6, "F"] = decimal.Round(currReading, 2);
            }

            //Print out results
            FormM.WriteToOutput(string.Format("  Measured Temp: {0}°C\n", reading));
            FormM.WriteToOutput("  Result: ");
            if (result == "Fail")
            {
                FormM.WriteToOutput(result + "\n", Color.Red);
            }
            else FormM.WriteToOutput(result + "\n");
            FormM.WriteToOutput("\n\r");



            //Prepare Ectron for next Thermocouple type
            ectron.Temp(0);
            ectron.Standby("ON");

            return true;
        }
    }
}
