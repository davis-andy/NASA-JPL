using System.Drawing;
using System.Security.Authentication.ExtendedProtection;
using System.Threading;
using Excel = Microsoft.Office.Interop.Excel;

namespace DAQ_modules
{
    class TypeE : Test
    {
        /*   Global variables for Type E Tests   */

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
        public string[] EvalsArray;
        public double[] Evals;

        //Get Set variable
        public override string Name => "Type E";




        /*   Type E Test functions   */

        //Type E Test Initializer
        public TypeE(Ectron ectron, DAQ970 daq, _34970 _34970, _34980 _34980, MainForm pForm,
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
            //channel = FormM.convertToInt(FormM.cmbChannelE.Text);

            //Start the test
            FormM.WriteToOutput("  Running Type E tests...\n\r");

            //Message to insert correct connector
            FormM.insertConnector("E");

            //Configure Ectron to correct Thermocouple type and turn off Standby
            ectron.Temp(0);
            ectron.Type("E");
            ectron.Standby("OFF");

            //Set up DAQ Mainframe with correct channel and read settings
            switch (FormM.IsDAQM())
            {
                case 1:
                    //DAQ970 Mainframe
                    daq.Reset();
                    daq.Setup("E", FormM.channel[0]);
                    daq.Nplc(10);
                    daq.Count();
                    daq.Monitor(FormM.channel[0]);

                    uncert1.Name = "Type E (-200°C)";
                    uncert5.Name = "Type E (1000°C)";
                    break;
                case 2:
                    //34970 Mainframe
                    _34970.Reset();
                    _34970.Setup("E", FormM.channel[0]);
                    _34970.Nplc(10);
                    _34970.Count();
                    _34970.Monitor(FormM.channel[0]);

                    uncert1.Name = "Type E (-190°C)";
                    uncert5.Name = "Type E (990°C)";
                    break;
                case 3:
                    //34980 Mainframe
                    _34980.Reset();
                    _34980.Setup("E", FormM.channel[0]);
                    _34980.Ref("INT", FormM.channel[0]);
                    _34980.Nplc(10);
                    _34980.Count();
                    _34980.Scan(FormM.channel[0]);
                    _34980.Monitor(FormM.channel[0]);

                    uncert1.Name = "Type E (-190°C)";
                    uncert5.Name = "Type E (990°C)";
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
                    ectron.Temp(daq.Etemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Etemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = daq.Read();
                    Evals = daq.ArrayConversion(EvalsArray);
                    reading = daq.AverageReading(Evals);
                    result = daq.ETolerances(daq.Etemps[0], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Etemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Etemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34970.Read();
                    Evals = _34970.ArrayConversion(EvalsArray);
                    reading = _34970.AverageReading(Evals);
                    result = _34970.ETolerances(_34970.Etemps[0], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Etemps[0]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Etemps[0]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34980.Read();
                    Evals = _34980.ArrayConversion(EvalsArray);
                    reading = _34980.AverageReading(Evals);
                    result = _34980.ETolerances(_34980.Etemps[0], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Evals.Length; i++)
            {
                decimal currReading = (decimal)Evals[i];
                uncert1.Cells[i + 6, "F"] = decimal.Round(currReading,2);
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
                    ectron.Temp(daq.Etemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Etemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = daq.Read();
                    Evals = daq.ArrayConversion(EvalsArray);
                    reading = daq.AverageReading(Evals);
                    result = daq.ETolerances(daq.Etemps[1], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Etemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Etemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34970.Read();
                    Evals = _34970.ArrayConversion(EvalsArray);
                    reading = _34970.AverageReading(Evals);
                    result = _34970.ETolerances(_34970.Etemps[1], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Etemps[1]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Etemps[1]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34980.Read();
                    Evals = _34980.ArrayConversion(EvalsArray);
                    reading = _34980.AverageReading(Evals);
                    result = _34980.ETolerances(_34980.Etemps[1], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Evals.Length; i++)
            {
                decimal currReading = (decimal)Evals[i];
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
                    ectron.Temp(daq.Etemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Etemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = daq.Read();
                    Evals = daq.ArrayConversion(EvalsArray);
                    reading = daq.AverageReading(Evals);
                    result = daq.ETolerances(daq.Etemps[2], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Etemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Etemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34970.Read();
                    Evals = _34970.ArrayConversion(EvalsArray);
                    reading = _34970.AverageReading(Evals);
                    result = _34970.ETolerances(_34970.Etemps[2], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Etemps[2]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Etemps[2]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34980.Read();
                    Evals = _34980.ArrayConversion(EvalsArray);
                    reading = _34980.AverageReading(Evals);
                    result = _34980.ETolerances(_34980.Etemps[2], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Evals.Length; i++)
            {
                decimal currReading = (decimal)Evals[i];
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
                    ectron.Temp(daq.Etemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Etemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = daq.Read();
                    Evals = daq.ArrayConversion(EvalsArray);
                    reading = daq.AverageReading(Evals);
                    result = daq.ETolerances(daq.Etemps[3], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Etemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Etemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34970.Read();
                    Evals = _34970.ArrayConversion(EvalsArray);
                    reading = _34970.AverageReading(Evals);
                    result = _34970.ETolerances(_34970.Etemps[3], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Etemps[3]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Etemps[3]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34980.Read();
                    Evals = _34980.ArrayConversion(EvalsArray);
                    reading = _34980.AverageReading(Evals);
                    result = _34980.ETolerances(_34980.Etemps[3], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Evals.Length; i++)
            {
                decimal currReading = (decimal)Evals[i];
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
                    ectron.Temp(daq.Etemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", daq.Etemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = daq.Read();
                    Evals = daq.ArrayConversion(EvalsArray);
                    reading = daq.AverageReading(Evals);
                    result = daq.ETolerances(daq.Etemps[4], (float)reading);
                    break;
                case 2:
                    //34970 Mainframe
                    ectron.Temp(_34970.Etemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34970.Etemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34970.Read();
                    Evals = _34970.ArrayConversion(EvalsArray);
                    reading = _34970.AverageReading(Evals);
                    result = _34970.ETolerances(_34970.Etemps[4], (float)reading);
                    break;
                case 3:
                    //34980 Mainframe
                    ectron.Temp(_34980.Etemps[4]);
                    FormM.WriteToOutput(string.Format("  Applied Temp: {0}.00°C\n", _34980.Etemps[4]));
                    Thread.Sleep(5000);

                    //Collect readings, convert according, retreive Pass/Fail result
                    EvalsArray = _34980.Read();
                    Evals = _34980.ArrayConversion(EvalsArray);
                    reading = _34980.AverageReading(Evals);
                    result = _34980.ETolerances(_34980.Etemps[4], (float)reading);
                    break;
            }

            //Populate Uncertainty Analysis Test Runs
            for (int i = 0; i < Evals.Length; i++)
            {
                decimal currReading = (decimal)Evals[i];
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
