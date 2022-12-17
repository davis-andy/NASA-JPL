using System.Threading;
using System.Drawing;
using Excel = Microsoft.Office.Interop.Excel;

namespace DAQ_modules
{
    class TypeT : Test
    {
        /*   Global variables for Type T Tests   */

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
        public string[] TvalsArray;
        public double[] Tvals;

        //Get Set variable
        public override string Name => "Type T";




        /*   Type T Test functions   */

        //Type T Test Initializer
        public TypeT(Ectron ectron, DAQ970 daq, _34970 _34970, _34980 _34980, MainForm pForm,
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
            //channel = FormM.convertToInt(FormM.cmbChannelT.Text);

            //Start the test
            FormM.WriteToOutput("  Running Type T tests...\n\r");

            //Message to insert correct connector
            FormM.insertConnector("T");

            //Configure Ectron to correct Thermocouple type and turn off Standby
            ectron.Temp(0);
            ectron.Type("T");
            ectron.Standby("OFF");

            //Set up DAQ Mainframe with correct channel and read settings
            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    daq.Reset();
                    daq.Setup("T", FormM.channel[3]);
                    daq.Nplc(10);
                    daq.Count();
                    daq.Monitor(FormM.channel[3]);

                    uncert1.Name = "Type T (-200°C)";
                    uncert5.Name = "Type T (400°C)";
                    break;
                case 2:
                    //34970 Mainframe
                    _34970.Reset();
                    _34970.Setup("T", FormM.channel[3]);
                    _34970.Nplc(10);
                    _34970.Count();
                    _34970.Monitor(FormM.channel[3]);

                    uncert1.Name = "Type T (-190°C)";
                    uncert5.Name = "Type T (395°C)";
                    break;
                case 3:
                    //34980 Mainframe
                    _34980.Reset();
                    _34980.Setup("T", FormM.channel[3]);
                    _34980.Ref("INT", FormM.channel[3]);
                    _34980.Nplc(10);
                    _34980.Count();
                    _34980.Scan(FormM.channel[3]);
                    _34980.Monitor(FormM.channel[3]);

                    uncert1.Name = "Type T (-190°C)";
                    uncert5.Name = "Type T (395°C)";
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
                    ectron.Temp(daq.Ttemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ttemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = daq.Read();
                    Tvals = daq.ArrayConversion(TvalsArray);
                    reading = daq.AverageReading(Tvals);
                    result = daq.TTolerances(daq.Ttemps[0], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ttemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ttemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34970.Read();
                    Tvals = _34970.ArrayConversion(TvalsArray);
                    reading = _34970.AverageReading(Tvals);
                    result = _34970.TTolerances(_34970.Ttemps[0], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ttemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ttemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34980.Read();
                    Tvals = _34980.ArrayConversion(TvalsArray);
                    reading = _34980.AverageReading(Tvals);
                    result = _34980.TTolerances(_34980.Ttemps[0], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Tvals.Length; i++)
            {
                decimal currReading = (decimal)Tvals[i];
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
                    ectron.Temp(daq.Ttemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ttemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = daq.Read();
                    Tvals = daq.ArrayConversion(TvalsArray);
                    reading = daq.AverageReading(Tvals);
                    result = daq.TTolerances(daq.Ttemps[1], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ttemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ttemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34970.Read();
                    Tvals = _34970.ArrayConversion(TvalsArray);
                    reading = _34970.AverageReading(Tvals);
                    result = _34970.TTolerances(_34970.Ttemps[1], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ttemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ttemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34980.Read();
                    Tvals = _34980.ArrayConversion(TvalsArray);
                    reading = _34980.AverageReading(Tvals);
                    result = _34980.TTolerances(_34980.Ttemps[1], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Tvals.Length; i++)
            {
                decimal currReading = (decimal)Tvals[i];
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
                    ectron.Temp(daq.Ttemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ttemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = daq.Read();
                    Tvals = daq.ArrayConversion(TvalsArray);
                    reading = daq.AverageReading(Tvals);
                    result = daq.TTolerances(daq.Ttemps[2], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ttemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ttemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34970.Read();
                    Tvals = _34970.ArrayConversion(TvalsArray);
                    reading = _34970.AverageReading(Tvals);
                    result = _34970.TTolerances(_34970.Ttemps[2], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ttemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ttemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34980.Read();
                    Tvals = _34980.ArrayConversion(TvalsArray);
                    reading = _34980.AverageReading(Tvals);
                    result = _34980.TTolerances(_34980.Ttemps[2], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Tvals.Length; i++)
            {
                decimal currReading = (decimal)Tvals[i];
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
                    ectron.Temp(daq.Ttemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ttemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = daq.Read();
                    Tvals = daq.ArrayConversion(TvalsArray);
                    reading = daq.AverageReading(Tvals);
                    result = daq.TTolerances(daq.Ttemps[3], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ttemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ttemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34970.Read();
                    Tvals = _34970.ArrayConversion(TvalsArray);
                    reading = _34970.AverageReading(Tvals);
                    result = _34970.TTolerances(_34970.Ttemps[3], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ttemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ttemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34980.Read();
                    Tvals = _34980.ArrayConversion(TvalsArray);
                    reading = _34980.AverageReading(Tvals);
                    result = _34980.TTolerances(_34980.Ttemps[3], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Tvals.Length; i++)
            {
                decimal currReading = (decimal)Tvals[i];
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
                    ectron.Temp(daq.Ttemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Ttemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = daq.Read();
                    Tvals = daq.ArrayConversion(TvalsArray);
                    reading = daq.AverageReading(Tvals);
                    result = daq.TTolerances(daq.Ttemps[4], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Ttemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Ttemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34970.Read();
                    Tvals = _34970.ArrayConversion(TvalsArray);
                    reading = _34970.AverageReading(Tvals);
                    result = _34970.TTolerances(_34970.Ttemps[4], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Ttemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Ttemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    TvalsArray = _34980.Read();
                    Tvals = _34980.ArrayConversion(TvalsArray);
                    reading = _34980.AverageReading(Tvals);
                    result = _34980.TTolerances(_34980.Ttemps[4], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Tvals.Length; i++)
            {
                decimal currReading = (decimal)Tvals[i];
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
