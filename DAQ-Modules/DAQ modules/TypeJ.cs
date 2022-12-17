using System.Threading;
using System.Drawing;
using Excel = Microsoft.Office.Interop.Excel;

namespace DAQ_modules
{
    class TypeJ : Test
    {
        /*   Global variables for Type J Tests   */

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
        public string[] JvalsArray;
        public double[] Jvals;

        //Get Set variable
        public override string Name => "Type J";




        /*   Type J Test functions   */

        //Type J Test Initializer
        public TypeJ(Ectron ectron, DAQ970 daq, _34970 _34970, _34980 _34980, MainForm pForm,
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
            //channel = FormM.convertToInt(FormM.cmbChannelJ.Text);

            //Start the test
            FormM.WriteToOutput("  Running Type J tests...\n\r");

            //Message to insert correct connector
            FormM.insertConnector("J");

            //Configure Ectron to correct Thermocouple type and turn off Standby
            ectron.Temp(0);
            ectron.Type("J");
            ectron.Standby("OFF");

            //Set up DAQ Mainframe with correct channel and read settings
            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    daq.Reset();
                    daq.Setup("J", FormM.channel[1]);
                    daq.Nplc(10);
                    daq.Count();
                    daq.Monitor(FormM.channel[1]);

                    uncert1.Name = "Type J (-210°C)";
                    uncert5.Name = "Type J (1200°C)";
                    break;
                case 2:
                    //34970 Mainframe
                    _34970.Reset();
                    _34970.Setup("J", FormM.channel[1]);
                    _34970.Nplc(10);
                    _34970.Count();
                    _34970.Monitor(FormM.channel[1]);

                    uncert1.Name = "Type J (-200°C)";
                    uncert5.Name = "Type J (1190°C)";
                    break;
                case 3:
                    //34980 Mainframe
                    _34980.Reset();
                    _34980.Setup("J", FormM.channel[1]);
                    _34980.Ref("INT", FormM.channel[1]);
                    _34980.Nplc(10);
                    _34980.Count();
                    _34980.Scan(FormM.channel[1]);
                    _34980.Monitor(FormM.channel[1]);

                    uncert1.Name = "Type J (-200°C)";
                    uncert5.Name = "Type J (1190°C)";
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
                    ectron.Temp(daq.Jtemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Jtemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = daq.Read();
                    Jvals = daq.ArrayConversion(JvalsArray);
                    reading = daq.AverageReading(Jvals);
                    result = daq.JTolerances(daq.Jtemps[0], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Jtemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Jtemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34970.Read();
                    Jvals = _34970.ArrayConversion(JvalsArray);
                    reading = _34970.AverageReading(Jvals);
                    result = _34970.JTolerances(_34970.Jtemps[0], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Jtemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Jtemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34980.Read();
                    Jvals = _34980.ArrayConversion(JvalsArray);
                    reading = _34980.AverageReading(Jvals);
                    result = _34980.JTolerances(_34980.Jtemps[0], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Jvals.Length; i++)
            {
                decimal currReading = (decimal)Jvals[i];
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
                    ectron.Temp(daq.Jtemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Jtemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = daq.Read();
                    Jvals = daq.ArrayConversion(JvalsArray);
                    reading = daq.AverageReading(Jvals);
                    result = daq.JTolerances(daq.Jtemps[1], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Jtemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Jtemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34970.Read();
                    Jvals = _34970.ArrayConversion(JvalsArray);
                    reading = _34970.AverageReading(Jvals);
                    result = _34970.JTolerances(_34970.Jtemps[1], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Jtemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Jtemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34980.Read();
                    Jvals = _34980.ArrayConversion(JvalsArray);
                    reading = _34980.AverageReading(Jvals);
                    result = _34980.JTolerances(_34980.Jtemps[1], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Jvals.Length; i++)
            {
                decimal currReading = (decimal)Jvals[i];
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
                    ectron.Temp(daq.Jtemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Jtemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = daq.Read();
                    Jvals = daq.ArrayConversion(JvalsArray);
                    reading = daq.AverageReading(Jvals);
                    result = daq.JTolerances(daq.Jtemps[2], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Jtemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Jtemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34970.Read();
                    Jvals = _34970.ArrayConversion(JvalsArray);
                    reading = _34970.AverageReading(Jvals);
                    result = _34970.JTolerances(_34970.Jtemps[2], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Jtemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Jtemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34980.Read();
                    Jvals = _34980.ArrayConversion(JvalsArray);
                    reading = _34980.AverageReading(Jvals);
                    result = _34980.JTolerances(_34980.Jtemps[2], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Jvals.Length; i++)
            {
                decimal currReading = (decimal)Jvals[i];
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
                    ectron.Temp(daq.Jtemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Jtemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = daq.Read();
                    Jvals = daq.ArrayConversion(JvalsArray);
                    reading = daq.AverageReading(Jvals);
                    result = daq.JTolerances(daq.Jtemps[3], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Jtemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Jtemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34970.Read();
                    Jvals = _34970.ArrayConversion(JvalsArray);
                    reading = _34970.AverageReading(Jvals);
                    result = _34970.JTolerances(_34970.Jtemps[3], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Jtemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Jtemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34980.Read();
                    Jvals = _34980.ArrayConversion(JvalsArray);
                    reading = _34980.AverageReading(Jvals);
                    result = _34980.JTolerances(_34980.Jtemps[3], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Jvals.Length; i++)
            {
                decimal currReading = (decimal)Jvals[i];
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
                    ectron.Temp(daq.Jtemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Jtemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = daq.Read();
                    Jvals = daq.ArrayConversion(JvalsArray);
                    reading = daq.AverageReading(Jvals);
                    result = daq.JTolerances(daq.Jtemps[4], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Jtemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Jtemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34970.Read();
                    Jvals = _34970.ArrayConversion(JvalsArray);
                    reading = _34970.AverageReading(Jvals);
                    result = _34970.JTolerances(_34970.Jtemps[4], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Jtemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Jtemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    JvalsArray = _34980.Read();
                    Jvals = _34980.ArrayConversion(JvalsArray);
                    reading = _34980.AverageReading(Jvals);
                    result = _34980.JTolerances(_34980.Jtemps[4], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Jvals.Length; i++)
            {
                decimal currReading = (decimal)Jvals[i];
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
