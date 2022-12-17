using System;
using System.Collections.Generic;
using System.Drawing;
using Excel = Microsoft.Office.Interop.Excel;
using System.Windows.Forms;
using System.IO;
using System.Text;
using System.Diagnostics;
using System.Threading;
using System.Runtime.InteropServices;
using DAQ_modules.Properties;
using NationalInstruments.Visa;
using System.Net.Http;
using Newtonsoft.Json;

namespace DAQ_modules
{
    public partial class MainForm : Form
    {
        /*   Global variables for Main Form   */

        //Instrument variables
        _34970 _34970;
        _34980 _34980;
        DAQ970 daq;
        Ectron ectron;

        //Program variables
        SaveFileDialog saveFileDialog1;
        Queue<Test> tests;
        List<Instrument> activeInstruments;
        Dictionary<String, TextBox> Users, Notes;
        Dictionary<String, ComboBox> Locations;
        TestManager testManager;
        public Thread RunningTests;
        TempSettle ts;
        private int location;
        Boolean skipped = false;
        Boolean complete = false;
        private string originalNotes;
        public int[] channel = { 201, 206, 211, 217 };
        public int siteID, daqm;
        public double wait;

        //Delegate variables
        public delegate void delSetVal(string val);
        public delegate void delRichBox(string val, Color color);
        public delegate void delListBox(int ind, bool val);
        public delegate int delCheckModel();
        public delegate void delAbortTests();
        public delegate void delAbortThread();
        public delegate void delQuitExcel();
        public delegate void delResetButton();
        public delegate void delTimer();
        public delegate void delInsertConnector(string type);
        public delegate void delMissingTemplate();
        public delegate void delExcelWarning();

        //Excel variables
        private string DataPathOpen, SaveDataName;
        Excel.Application eApp;
        Excel.Workbook DataWorkbook;
        Excel.Worksheet DataWorksheet, TypeE1, TypeE2, TypeE3, TypeE4, TypeE5, TypeJ1, TypeJ2, TypeJ3, TypeJ4, TypeJ5,
            TypeK1, TypeK2, TypeK3, TypeK4, TypeK5, TypeT1, TypeT2, TypeT3, TypeT4, TypeT5;

        //API variables
        private static readonly HttpClient client = new HttpClient();

        //Instrument connection variables
        string addy34970, addyDAQ, addyEctron, addy34980;






        /*  Instrument connections  */
        private void ScanInstruments()
        {
            //Resource Manager and Message Session set up
            MessageBasedSession testsesh;
            ResourceManager rmsesh = new ResourceManager();
            string idnString;
            string[] resources;

            try
            {
                resources = (string[])rmsesh.Find("(GPIB|USB)?*INSTR");

                foreach (string instr in resources)
                {
                    testsesh = (MessageBasedSession)rmsesh.Open(instr);

                    try
                    {
                        testsesh.RawIO.Write("*IDN?\n");
                        idnString = testsesh.RawIO.ReadString();

                        if (idnString.Contains("34970A"))
                        {
                            cmbDAQ.Items.Add("34970A");
                            cmbDAQ.SelectedIndex = 0;

                            addy34970 = instr;

                            _34970 = new _34970(instr);
                        }

                        else if (idnString.Contains("34980A"))
                        {
                            cmbDAQ.Items.Add("34980A");
                            cmbDAQ.SelectedIndex = 0;
                        
                            addy34980 = instr;
                        
                            _34980 = new _34980(instr);
                        }

                        else if (idnString.Contains("DAQ970A"))
                        {
                            cmbDAQ.Items.Add("DAQ970A");
                            cmbDAQ.SelectedIndex = 0;

                            addyDAQ = instr;

                            daq = new DAQ970(instr);
                        }

                        else if (idnString.Contains("1140A"))
                        {
                            addyEctron = instr;

                            ectron = new Ectron(instr);
                        }
                    }
                    catch (Exception e)
                    {
                        continue;
                    }

                }
            }
            catch (Exception e)
            {
                MessageBox.Show("No Instruments Detected.\nPlease Check Connections.");
                return;
            }
        }

        private Boolean InstrConnected()
        {
            if (txtDAQID.Text == string.Empty || txtEctronID.Text == string.Empty) return false;
            else return true;
        }

        private void PopulateStandards()
        {
            // Get Fluke ID number from API
            GetTempHumidity();

            // DAQ ID from combo box
            switch (cmbDAQ.SelectedItem)
            {
                case "34970A":
                    txtDAQID.Text = Settings.Default.d34970_id;
                    break;
                case "34980A":
                    txtDAQID.Text = Settings.Default.d34980_id;
                    break;
                case "DAQ970A":
                    txtDAQID.Text = Settings.Default.daq970_id;
                    break;
            }

            // Ectron ID from serial number
            if (ectron != null)
            {
                switch (ectron.Serial())
                {
                    case "81000":
                        txtEctronID.Text = "2352754";
                        break;
                    case "81001":
                        txtEctronID.Text = "2352755";
                        break;
                    case "86399":
                        txtEctronID.Text = "2690776";
                        break;
                }
            }

            EctronDueDates();
            DAQDueDates();
        }

        private void InstrumentPage()
        {
            try
            {
                ScanInstruments();
                PopulateStandards();
            }
            catch { }

            if (cmbDAQ.Items.Count > 1)
            {
                cmbDAQ.Visible = true;
                lblDAQModel.Visible = true;
            }
            else
            {
                cmbDAQ.Visible = false;
                lblDAQModel.Visible = false;
            }
        }



        /*   API Connections    */
        private async void GetTempHumidity()
        {
            switch (cmbLocation.Text)
            {
                case "B64":
                    siteID = 24;
                    break;
                case "B66":
                    siteID = 25;
                    break;
                case "B67":
                    siteID = 26;
                    break;
                case "B68":
                    siteID = 27;
                    break;
                default:
                    siteID = Settings.Default.site_id;
                    break;
            }

            var response = await client.GetAsync(Settings.Default.fluke_reading_url +
                "?site_id=" + siteID);
            var responseString = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseString);
            try
            {
                FlukeReading flukeReading = JsonConvert.DeserializeObject<FlukeReading>(responseString);
                txtTemp.Text = flukeReading.ch1_temp.ToString("F1");
                txtHumidity.Text = flukeReading.ch1_humidity.ToString("F1");
                txtProbeID.Text = flukeReading.sensor1_id;
                if (flukeReading.sensor1_cal_due != null)
                {
                    string[] splitDate = flukeReading.sensor1_cal_due.Split('-');
                    txtProbeDate.Text = splitDate[1] + "/" + splitDate[2] + "/" + splitDate[0];
                }
            }
            catch
            {

            }
        }

        private async void EctronDueDates()
        {
            AssetInfo[] assetInfo;
            CalDueDatesRequestContent values = new CalDueDatesRequestContent();
            values.username = Settings.Default.username;
            values.password = Settings.Default.password;
            values.asset_ids = new string[] { txtEctronID.Text };
            var content = new StringContent(JsonConvert.SerializeObject(values), Encoding.UTF8, "application/json");
            var response = await client.PostAsync(Settings.Default.cal_due_dates_url, content);
            var responseString = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseString);
            try
            {
                assetInfo = JsonConvert.DeserializeObject<AssetInfo[]>(responseString);
            }
            catch
            {
                return;
            }

            
            if (assetInfo.Length > 0 && assetInfo[0].exists)
            {
                if (assetInfo[0].cal_due_date != null)
                {
                    string[] splitDate = assetInfo[0].cal_due_date.Split('-');
                    txtEctronDate.Text = splitDate[1] + "/" + splitDate[2] + "/" + splitDate[0];
                }
            }

        }

        private async void DAQDueDates()
        {
            AssetInfo[] assetInfo;
            CalDueDatesRequestContent values = new CalDueDatesRequestContent();
            values.username = Settings.Default.username;
            values.password = Settings.Default.password;
            values.asset_ids = new string[] { txtDAQID.Text };
            var content = new StringContent(JsonConvert.SerializeObject(values), Encoding.UTF8, "application/json");
            var response = await client.PostAsync(Settings.Default.cal_due_dates_url, content);
            var responseString = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseString);
            try
            {
                assetInfo = JsonConvert.DeserializeObject<AssetInfo[]>(responseString);
            }
            catch
            {
                return;
            }


            if (assetInfo.Length > 0 && assetInfo[0].exists)
            {
                if (assetInfo[0].cal_due_date != null)
                {
                    string[] splitDate = assetInfo[0].cal_due_date.Split('-');
                    txtDAQDate.Text = splitDate[1] + "/" + splitDate[2] + "/" + splitDate[0];
                }
            }

        }

        private async void ProbeDueDates()
        {
            AssetInfo[] assetInfo;
            CalDueDatesRequestContent values = new CalDueDatesRequestContent();
            values.username = Settings.Default.username;
            values.password = Settings.Default.password;
            values.asset_ids = new string[] { txtProbeID.Text };
            var content = new StringContent(JsonConvert.SerializeObject(values), Encoding.UTF8, "application/json");
            var response = await client.PostAsync(Settings.Default.cal_due_dates_url, content);
            var responseString = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseString);
            try
            {
                assetInfo = JsonConvert.DeserializeObject<AssetInfo[]>(responseString);
            }
            catch
            {
                return;
            }


            if (assetInfo.Length > 0 && assetInfo[0].exists)
            {
                if (assetInfo[0].cal_due_date != null)
                {
                    string[] splitDate = assetInfo[0].cal_due_date.Split('-');
                    txtProbeDate.Text = splitDate[1] + "/" + splitDate[2] + "/" + splitDate[0];
                }
            }

        }

        private async void GetUUTInfo()
        {
            AssetInfo[] assetInfo;
            CalDueDatesRequestContent values = new CalDueDatesRequestContent();
            values.username = Settings.Default.username;
            values.password = Settings.Default.password;
            values.asset_ids = new string[] { txtID.Text };
            var content = new StringContent(JsonConvert.SerializeObject(values), Encoding.UTF8, "application/json");
            var response = await client.PostAsync(Settings.Default.cal_due_dates_url, content);
            var responseString = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseString);
            try
            {
                assetInfo = JsonConvert.DeserializeObject<AssetInfo[]>(responseString);
            }
            catch
            {
                return;
            }


            if (assetInfo.Length > 0 && assetInfo[0].exists)
            {
                if (assetInfo[0].model != null)
                {
                    txtModel.Text = assetInfo[0].model;
                }
                if (assetInfo[0].serial != null)
                {
                    txtSerial.Text = assetInfo[0].serial;
                }
            }
        }

        private void GetUUTNotes()
        {
            Notes = new Dictionary<string, TextBox> { { txtID.Text, txtNotes } };

            StreamReader file;
            string path = Settings.Default.AppDataPath + @"\Notes.txt";

            if (File.Exists(path)) file = new StreamReader(path);
            else return;

            string line;
            string[] bline;
            while ((line = file.ReadLine()) != null)
            {
                bline = line.Split(',');
                if (Notes.ContainsKey(bline[0]))
                {
                    Notes.TryGetValue(bline[0], out TextBox t);
                    t.Text = bline[1];
                    originalNotes = bline[1];
                }
            }

            file.Close();
        }




        /*   Main Form functions   */

        //Automatically input date into Date textbox
        private void MainForm_Load(object sender, EventArgs e)
        {
            txtDate.Text = DateTime.Today.ToString("M/d/yyyy");
            TabHeader();
            ChannelSelect();
            GetTempHumidity();
            MakeDict();

            if (Users.ContainsKey(Environment.UserName))
            {
                PopulateUsers();
            }
        }

        //Actions to do when program exits
        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            //Stop all tests and threads
            if (RunningTests != null && RunningTests.IsAlive)
            {
                tests.Clear();
                AbortTests();
                AbortTestThread();
            }
            
            //Confirm exiting of program
            DialogResult result;
            result = MessageBox.Show("Are you sure you want to quit?", "Closing Application", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            
            if (result == DialogResult.Yes)
            {
                //Release all Excel objects
                if (DataWorksheet != null) Marshal.ReleaseComObject(DataWorksheet);
                if (TypeT5 != null) Marshal.ReleaseComObject(TypeT5);
                if (TypeT4 != null) Marshal.ReleaseComObject(TypeT4);
                if (TypeT3 != null) Marshal.ReleaseComObject(TypeT3);
                if (TypeT2 != null) Marshal.ReleaseComObject(TypeT2);
                if (TypeT1 != null) Marshal.ReleaseComObject(TypeT1);
                if (TypeK5 != null) Marshal.ReleaseComObject(TypeK5);
                if (TypeK4 != null) Marshal.ReleaseComObject(TypeK4);
                if (TypeK3 != null) Marshal.ReleaseComObject(TypeK3);
                if (TypeK2 != null) Marshal.ReleaseComObject(TypeK2);
                if (TypeK1 != null) Marshal.ReleaseComObject(TypeK1);
                if (TypeJ5 != null) Marshal.ReleaseComObject(TypeJ5);
                if (TypeJ4 != null) Marshal.ReleaseComObject(TypeJ4);
                if (TypeJ3 != null) Marshal.ReleaseComObject(TypeJ3);
                if (TypeJ2 != null) Marshal.ReleaseComObject(TypeJ2);
                if (TypeJ1 != null) Marshal.ReleaseComObject(TypeJ1);
                if (TypeE5 != null) Marshal.ReleaseComObject(TypeE5);
                if (TypeE4 != null) Marshal.ReleaseComObject(TypeE4);
                if (TypeE3 != null) Marshal.ReleaseComObject(TypeE3);
                if (TypeE2 != null) Marshal.ReleaseComObject(TypeE2);
                if (TypeE1 != null) Marshal.ReleaseComObject(TypeE1);

                if (DataWorkbook != null) Marshal.ReleaseComObject(DataWorkbook);
                if (eApp != null) Marshal.ReleaseComObject(eApp);
            }
            
            //Do not exit if 'No' is selected
            e.Cancel = (result == DialogResult.No);
        }

        //Main Form initializer
        public MainForm()
        {
            InitializeComponent();
            tests = new Queue<Test>();
            activeInstruments = new List<Instrument>();
        }




        /*   Main Form text box and button attributes   */

        //Initials text box actions
        private void txtInitials_Enter(object sender, EventArgs e)
        {
            txtInitials.SelectAll();
        }

        //Updat Button actions
        private void btnUpdate_Click(object sender, EventArgs e)
        {
            GetTempHumidity();
        }

        //Temperature text box actions
        private void txtTemp_Enter(object sender, EventArgs e)
        {
            txtTemp.SelectAll();
        }
        private void txtTemp_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!char.IsControl(e.KeyChar) && !char.IsDigit(e.KeyChar) &&
        (e.KeyChar != '.'))
            {
                e.Handled = true;
            }

            // only allow one decimal point
            if ((e.KeyChar == '.') && ((sender as TextBox).Text.IndexOf('.') > -1))
            {
                e.Handled = true;
            }
        }

        //Humidity text box actions
        private void txtHumidity_Enter(object sender, EventArgs e)
        {
            txtHumidity.SelectAll();
        }
        private void txtHumidity_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!char.IsControl(e.KeyChar) && !char.IsDigit(e.KeyChar) &&
                (e.KeyChar != '.'))
            {
                e.Handled = true;
            }
            
            // only allow one decimal point
            if ((e.KeyChar == '.') && ((sender as TextBox).Text.IndexOf('.') > -1))
            {
                e.Handled = true;
            }
        }

        //cmbDAQ box actions
        private void cmbDAQ_SelectedIndexChanged(object sender, EventArgs e)
        {
            switch (cmbDAQ.SelectedItem)
            {
                case "34970A":
                    txtDAQID.Text = Settings.Default.d34970_id;
                    break;
                case "34980A":
                    txtDAQID.Text = Settings.Default.d34980_id;
                    break;
                case "DAQ970A":
                    txtDAQID.Text = Settings.Default.daq970_id;
                    break;
            }

            DAQDueDates();
        }

        //Ecron ID text box actions
        private void txtEctronID_Leave(object sender, EventArgs e)
        {
            EctronDueDates();
        }

        //DAQ ID text box actions
        private void txtDAQID_Leave(object sender, EventArgs e)
        {
            DAQDueDates();
        }

        //Probe ID text box actions
        private void txtProbeID_Leave(object sender, EventArgs e)
        {
            GetTempHumidity();
        }

        //ID# text box actions
        private void txtID_Enter(object sender, EventArgs e)
        {
            txtID.SelectAll();
        }
        private void txtID_TextChanged(object sender, EventArgs e)
        {
            txtSerial.Text = string.Empty;
        }
        private void txtID_Leave(object sender, EventArgs e)
        {
            GetUUTInfo();
            GetUUTNotes();

            if (txtModel.Text.Contains("902")) cmbChannelT.SelectedIndex = 15;
        }

        //Serial# text box actions
        private void txtSerial_Enter(object sender, EventArgs e)
        {
            txtSerial.SelectAll();
        }

        //Temp Settle text box actions
        private void txtWait_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!char.IsControl(e.KeyChar) && !char.IsDigit(e.KeyChar) &&
                (e.KeyChar != '.'))
            {
                e.Handled = true;
            }

            // only allow one decimal point
            if ((e.KeyChar == '.') && ((sender as TextBox).Text.IndexOf('.') > -1))
            {
                e.Handled = true;
            }
        }



        //Intro tab Start/Skip Tutorial Button actions
        private void btnTutorial_Click(object sender, EventArgs e)
        {
            tabControl1.SelectedIndex++;
            skipped = false;
        }

        private void btnSkip_Click(object sender, EventArgs e)
        {
            skipped = true;
            tabControl1.SelectedIndex = 2;

            InstrumentPage();
        }

        //Tutorial tab Back/Next Button actions
        private void btnBackIntro_Click(object sender, EventArgs e)
        {
            tabControl1.SelectedIndex--;
        }
        private void btnNextInstr_Click(object sender, EventArgs e)
        {
            tabControl1.SelectedIndex++;

            InstrumentPage();
        }

        
        //Instruments tab Button actions
        private void btnRefresh_Click(object sender, EventArgs e)
        {
            txtEctronID.Text = string.Empty;
            txtDAQID.Text = string.Empty;
            txtEctronDate.Text = string.Empty;
            txtDAQDate.Text = string.Empty;
            ectron = null;
            daq = null;
            _34970 = null;
            _34980 = null;
            cmbDAQ.Items.Clear();

            InstrumentPage();
        }
        private void btnBackTut_Click(object sender, EventArgs e)
        {
            cmbDAQ.Items.Clear();
            if (skipped == true) tabControl1.SelectedIndex = 0;
            else tabControl1.SelectedIndex--;
        }
        private void btnNextInfo_Click(object sender, EventArgs e)
        {
            //Change channel numbers dependent on DAQ type
            if (cmbDAQ.Text == "34980A")
            {
                cmbChannelE.Items.Clear();
                cmbChannelJ.Items.Clear();
                cmbChannelK.Items.Clear();
                cmbChannelT.Items.Clear();
                for (int i = 0; i < 9; i++)
                {
                    cmbChannelE.Items.Add("200" + (i + 1).ToString());
                    cmbChannelJ.Items.Add("200" + (i + 1).ToString());
                    cmbChannelK.Items.Add("200" + (i + 1).ToString());
                    cmbChannelT.Items.Add("200" + (i + 1).ToString());
                }
                for (int i = 9; i < 20; i++)
                {
                    cmbChannelE.Items.Add("20" + (i + 1).ToString());
                    cmbChannelJ.Items.Add("20" + (i + 1).ToString());
                    cmbChannelK.Items.Add("20" + (i + 1).ToString());
                    cmbChannelT.Items.Add("20" + (i + 1).ToString());
                }

                cmbChannelE.SelectedIndex = 0;
                cmbChannelJ.SelectedIndex = 6;
                cmbChannelK.SelectedIndex = 10;
                cmbChannelT.SelectedIndex = 16;
            }
            else ChannelSelect();

            //Update Users if they are changed, or add Users if they do not exist
            if (!File.ReadAllText(Settings.Default.AppDataPath + @"\Users.txt").Contains(txtInitials.Text))
            {
                StreamWriter file = new StreamWriter(Settings.Default.AppDataPath + @"\Users.txt", true);
                file.WriteLine(Environment.UserName + "," + txtInitials.Text + "," + cmbLocation.SelectedIndex);
                file.Close();
            }

            if (cmbLocation.SelectedIndex != location)
            {
                File.WriteAllText(Settings.Default.AppDataPath + @"\Users.txt", File.ReadAllText(Settings.Default.AppDataPath + @"\Users.txt").Replace(
                    Environment.UserName + "," + txtInitials.Text + "," + location, Environment.UserName + "," + txtInitials.Text + "," + cmbLocation.SelectedIndex));
            }


            switch (cmbDAQ.Text)
            {
                case "34970A":
                    if (txtDAQID.Text != Settings.Default.d34970_id) Settings.Default.d34970_id = txtDAQID.Text;
                    break;
                case "34980A":
                    if (txtDAQID.Text != Settings.Default.d34980_id) Settings.Default.d34980_id = txtDAQID.Text;
                    break;
                case "DAQ970A":
                    if (txtDAQID.Text != Settings.Default.daq970_id) Settings.Default.daq970_id = txtDAQID.Text;
                    break;
            }

            

            if (InstrConnected()) tabControl1.SelectedIndex++;
            else MessageBox.Show("Missing Instruments.\nPlease check address and/or connections.");
        }

        //Info tab Back/Next Button actions
        private void btnBackInst_Click(object sender, EventArgs e)
        {
            tabControl1.SelectedIndex--;
        }

        private void cmbLocation_TextChanged(object sender, EventArgs e)
        {
            GetTempHumidity();
        }

        private void btnNextRun_Click(object sender, EventArgs e)
        {
            int.TryParse(cmbChannelE.Text, out channel[0]);
            int.TryParse(cmbChannelJ.Text, out channel[1]);
            int.TryParse(cmbChannelK.Text, out channel[2]);
            int.TryParse(cmbChannelT.Text, out channel[3]);

            double.TryParse(txtWait.Text, out double minutes);
            wait = (minutes * 60000);

            //Update Notes if they are changed, or add UUTs if they do not exist
            if (!File.ReadAllText(Settings.Default.AppDataPath + @"\Notes.txt").Contains(txtID.Text))
            {
                StreamWriter file = new StreamWriter(Settings.Default.AppDataPath + @"\Notes.txt", true);
                file.WriteLine(txtID.Text + "," + txtNotes.Text);
                file.Close();
            }

            if (File.ReadAllText(Settings.Default.AppDataPath + @"\Notes.txt").Contains(txtID.Text))
            {
                if (txtNotes.Text != originalNotes)
                {
                    File.WriteAllText(Settings.Default.AppDataPath + @"\Notes.txt", File.ReadAllText(Settings.Default.AppDataPath + @"\Notes.txt").Replace(
                        txtID.Text + "," + originalNotes, txtID.Text + "," + txtNotes.Text));
                }
            }

            tests.Clear();
            tabControl1.SelectedIndex++;
        }

        //Run Tests tab Start Over/Exit Button actions
        private void btnRestart_Click(object sender, EventArgs e)
        {
            if (complete == false) tabControl1.SelectedIndex--;
            else
            {
                foreach (int item in chbTests.CheckedIndices)
                {
                    SelectBox(item, false);
                }

                txtPrint.Text = string.Empty;
                txtID.Text = string.Empty;
                txtModel.Text = string.Empty;
                txtSerial.Text = string.Empty;
                txtNotes.Text = " ";

                tests.Clear();
                testManager = null;

                complete = false;
                btnRestart.Text = "Back";

                GetTempHumidity();
                tabControl1.SelectedIndex = 2;
            }

            
        }
        private void btnExit_Click(object sender, EventArgs e)
        {
            this.Close();
        }
        
        //Run Tests Start button/Stop Button actions 
        private void btnStart_Click(object sender, EventArgs e)
        {
            //If tests are running, warn user, otherwise start a new test thread
            if (RunningTests != null && RunningTests.IsAlive)
            {
                WriteToOutput("\n");
                WriteToOutput("  There are tests currently running!\n");
            }
            else
            {
                //Clear Print text box
                txtPrint.Text = string.Empty;

                ThreadStart Ref = new ThreadStart(RunTests);
                RunningTests = new Thread(Ref);
                RunningTests.SetApartmentState(ApartmentState.STA);
                RunningTests.Start();
            }
        }
        private void btnStop_Click(object sender, EventArgs e)
        {
            //Stops tests if any are running after asking user if they want to do so
            if (RunningTests != null && RunningTests.IsAlive)
            {
                DialogResult result;
                result = MessageBox.Show("Are you sure you want to stop testing?", "Stopping tests", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (result == DialogResult.Yes)
                {
                    closeExcelWarning();
                    tests.Clear();
                    AbortTests();
                    AbortTestThread();
                    testManager = null;

                    for (int i = Application.OpenForms.Count - 1; i >= 0; i--)
                    {
                        if (Application.OpenForms[i].Name != "MainForm")
                            Application.OpenForms[i].Close();
                    }

                    ectron.Temp(0);
                    ectron.Standby("ON");

                    //Kill all excel processes
                    foreach (var process in Process.GetProcessesByName("EXCEL"))
                        process.Kill();

                    WriteToOutput("  Tests aborted");
                    WriteToOutput("\n");
                }
            }
            else
            {
                WriteToOutput("  No tests currently running\n");
                WriteToOutput("\n");
            }
        }





        /*   Functions for testing   */

        //Check which radio button is selected, return Model for tests
        public int IsDAQM()
        {
            if (this.InvokeRequired) this.Invoke(new delCheckModel(IsDAQM));
            else
            {
                if (cmbDAQ.Text == "DAQ970A") daqm = 1;
                else if (cmbDAQ.Text == "34970A") daqm = 2;
                else daqm = 3;
            }

            return daqm;
        }

        //Change name on Reset Button
        public void ResetBtnName()
        {
            if (this.InvokeRequired) this.Invoke(new delResetButton(ResetBtnName));
            else
            {
                this.complete = true;
                this.btnRestart.Text = "Start Over";
            }
        }

        //Tab header properties for loading the form
        public void TabHeader()
        {
            tabControl1.Appearance = TabAppearance.FlatButtons;
            tabControl1.ItemSize = new Size(0, 1);
            tabControl1.SizeMode = TabSizeMode.Fixed;

            foreach (TabPage tab in tabControl1.TabPages) tab.Text = "";
        }

        //Initial channels auto selected
        public void ChannelSelect()
        {
            cmbChannelE.Items.Clear();
            cmbChannelJ.Items.Clear();
            cmbChannelK.Items.Clear();
            cmbChannelT.Items.Clear();
            for (int i = 0; i < 9; i++)
            {
                cmbChannelE.Items.Add("20" + (i + 1).ToString());
                cmbChannelJ.Items.Add("20" + (i + 1).ToString());
                cmbChannelK.Items.Add("20" + (i + 1).ToString());
                cmbChannelT.Items.Add("20" + (i + 1).ToString());
            }
            for (int i = 9; i < 20; i++)
            {
                cmbChannelE.Items.Add("2" + (i + 1).ToString());
                cmbChannelJ.Items.Add("2" + (i + 1).ToString());
                cmbChannelK.Items.Add("2" + (i + 1).ToString());
                cmbChannelT.Items.Add("2" + (i + 1).ToString());
            }

            cmbChannelE.SelectedIndex = 0;
            cmbChannelJ.SelectedIndex = 5;
            cmbChannelK.SelectedIndex = 10;
            cmbChannelT.SelectedIndex = 16;
        }

        //Create Dictionary to populate textboxes
        private void MakeDict()
        {
            Users = new Dictionary<string, TextBox>
            {
                { Environment.UserName, txtInitials }
            };

            Locations = new Dictionary<string, ComboBox>
            {
                { Environment.UserName, cmbLocation }
            };
        }

        //Populate Initials textbox with Dictionary items
        private void PopulateUsers()
        {

            StreamReader file;
            string path = Settings.Default.AppDataPath + @"\Users.txt";


            if (File.Exists(path))
                file = new System.IO.StreamReader(path);
            else
                return;

            string line;
            string[] bLine;
            while ((line = file.ReadLine()) != null)
            {
                bLine = line.Split(',');
                if (Users.ContainsKey(bLine[0]))
                {
                    Users.TryGetValue(bLine[0], out TextBox t);
                    t.Text = bLine[1];
                }
                if (Locations.ContainsKey(bLine[0]))
                {
                    Locations.TryGetValue(bLine[0], out ComboBox b);
                    b.SelectedIndex = int.Parse(bLine[2]);
                }
            }
            file.Close();

            location = cmbLocation.SelectedIndex;
        }

        //Temperature Settle Form function/delegate
        public void Timer()
        {
            if (this.InvokeRequired) this.Invoke(new delTimer(Timer));
            else
            {
                double timeout = wait - 1000;

                using (new CenterMessage(this))
                {
                    ts = new TempSettle(timeout);
                    ts.Show();
                }
            }
        }

        //Wrtie to Print text box delegate, text only
        public void WriteToOutput(string value)
        {
            if (this.InvokeRequired) this.Invoke(new delSetVal(WriteToOutput), value);
            else
            {
                this.txtPrint.AppendText(value);
                //Scroll to bottom
                this.txtPrint.Select(txtPrint.Text.Length, 0);
                this.txtPrint.ScrollToCaret();
            }
        }

        //Write to Print text box delegate, text and color
        public void WriteToOutput(string value, Color color)
        {
            if (this.InvokeRequired) this.Invoke(new delRichBox(WriteToOutput), value, color);
            else
            {
                this.txtPrint.AppendText(value, color);
                //Scroll to bottom
                this.txtPrint.Select(txtPrint.Text.Length, 0);
                this.txtPrint.ScrollToCaret();
            }
        }

        //Insert Connector message box delegate
        public void insertConnector(string connector)
        {
            if (this.InvokeRequired) this.Invoke(new delInsertConnector(insertConnector), connector);
            else
            {
                string message = String.Format("Insert Type {0} connector", connector);
                string caption = "Insert Connector";
                MessageBoxButtons buttons = MessageBoxButtons.OK;

                using (new CenterMessage(this)) { MessageBox.Show(message, caption, buttons); }
            }
        }

        //Save and close any open Excel files message box delegate
        public void closeExcelWarning()
        {
            if (this.InvokeRequired) this.Invoke(new delExcelWarning(closeExcelWarning));
            else
            {
                string message = "Save and close all open Excel files before continuing.";
                string caption = "Save Excel Files";
                MessageBoxButtons buttons = MessageBoxButtons.OK;
                MessageBoxIcon icon = MessageBoxIcon.Warning;

                MessageBox.Show(message, caption, buttons, icon);
            }
        }

        //Missing Template message box delegate
        public void missingTemplate()
        {
            if (this.InvokeRequired) this.Invoke(new delMissingTemplate(missingTemplate));
            else
            {
                DialogResult result;
                result = MessageBox.Show("Missing Template File", "Missing File", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                while (result != DialogResult.OK) Thread.Sleep(100);
            }
        }

        //Select tests in checkbox list
        public void SelectBox(int ind, bool val)
        {
            if (this.InvokeRequired) this.Invoke(new delListBox(SelectBox), ind, val);
            else this.chbTests.SetItemChecked(ind, val);
        }

        //Abort tests delegate
        public void AbortTests()
        {
            if (this.InvokeRequired) this.Invoke(new delAbortTests(AbortTests));
            else this.testManager.StopTests();
        }

        //Abort thread delegate
        public void AbortTestThread()
        {
            if (this.InvokeRequired) this.Invoke(new delAbortThread(AbortTestThread));
            else this.RunningTests.Abort();
        }

        //Open Excel functionality
        public bool OpenExcel()
        {
            //Kill all excel processes
            foreach (var process in Process.GetProcessesByName("EXCEL"))
                process.Kill();

            //Warn about missing template
            if (!File.Exists(DataPathOpen))
            {
                missingTemplate();
                return false;
            }

            //Open new instance of Excel
            eApp = new Excel.Application();
            eApp.DisplayAlerts = false;

            //Main Workbook
            DataWorkbook = (Excel.Workbook)(eApp.Workbooks.Open(DataPathOpen, System.Reflection.Missing.Value, System.Reflection.Missing.Value,
                System.Reflection.Missing.Value, System.Reflection.Missing.Value, System.Reflection.Missing.Value, System.Reflection.Missing.Value,
                System.Reflection.Missing.Value, System.Reflection.Missing.Value, System.Reflection.Missing.Value, System.Reflection.Missing.Value,
                System.Reflection.Missing.Value, System.Reflection.Missing.Value));

            //Main Datasheet
            DataWorksheet = (Excel.Worksheet)DataWorkbook.Worksheets[1];
            
            //Uncertainty Analysis sheets
            TypeE1 = (Excel.Worksheet)DataWorkbook.Worksheets[3];
            TypeE2 = (Excel.Worksheet)DataWorkbook.Worksheets[4];
            TypeE3 = (Excel.Worksheet)DataWorkbook.Worksheets[5];
            TypeE4 = (Excel.Worksheet)DataWorkbook.Worksheets[6];
            TypeE5 = (Excel.Worksheet)DataWorkbook.Worksheets[7];
            TypeJ1 = (Excel.Worksheet)DataWorkbook.Worksheets[8];
            TypeJ2 = (Excel.Worksheet)DataWorkbook.Worksheets[9];
            TypeJ3 = (Excel.Worksheet)DataWorkbook.Worksheets[10];
            TypeJ4 = (Excel.Worksheet)DataWorkbook.Worksheets[11];
            TypeJ5 = (Excel.Worksheet)DataWorkbook.Worksheets[12];
            TypeK1 = (Excel.Worksheet)DataWorkbook.Worksheets[13];
            TypeK2 = (Excel.Worksheet)DataWorkbook.Worksheets[14];
            TypeK3 = (Excel.Worksheet)DataWorkbook.Worksheets[15];
            TypeK4 = (Excel.Worksheet)DataWorkbook.Worksheets[16];
            TypeK5 = (Excel.Worksheet)DataWorkbook.Worksheets[17];
            TypeT1 = (Excel.Worksheet)DataWorkbook.Worksheets[18];
            TypeT2 = (Excel.Worksheet)DataWorkbook.Worksheets[19];
            TypeT3 = (Excel.Worksheet)DataWorkbook.Worksheets[20];
            TypeT4 = (Excel.Worksheet)DataWorkbook.Worksheets[21];
            TypeT5 = (Excel.Worksheet)DataWorkbook.Worksheets[22];
            
            return true;
        }

        //Populates excel workbook with necessary info & specs
        private void SetupExcel()
        {
            DataWorksheet.Cells[3, "J"] = txtDate.Text;
            DataWorksheet.Cells[4, "J"] = txtInitials.Text;
            DataWorksheet.Cells[6, "B"] = txtModel.Text;
            DataWorksheet.Cells[6, "E"] = txtID.Text;
            DataWorksheet.Cells[6, "J"] = txtTemp.Text;
            DataWorksheet.Cells[7, "B"] = txtSerial.Text;
            DataWorksheet.Cells[7, "J"] = txtHumidity.Text;
            DataWorksheet.Cells[10, "A"] = txtEctronID.Text;
            DataWorksheet.Cells[10, "H"] = txtEctronDate.Text;
            DataWorksheet.Cells[11, "H"] = txtDAQDate.Text;
            DataWorksheet.Cells[12, "A"] = txtProbeID.Text;
            DataWorksheet.Cells[12, "H"] = txtProbeDate.Text;
            DataWorksheet.Cells[41, "B"] = txtNotes.Text;
            DataWorksheet.Cells[17, "A"] = "Type E\n(Channel #" + channel[0].ToString().Substring(1) + ")";
            DataWorksheet.Cells[23, "A"] = "Type J\n(Channel #" + channel[1].ToString().Substring(1) + ")";
            DataWorksheet.Cells[29, "A"] = "Type K\n(Channel #" + channel[2].ToString().Substring(1) + ")";
            DataWorksheet.Cells[35, "A"] = "Type T\n(Channel #" + channel[3].ToString().Substring(1) + ")";
        }

        //Get Save location for Excel
        public void ExcelSavePath()
        {
            //Get save folder path for excel file
            saveFileDialog1 = new SaveFileDialog();
            saveFileDialog1.Title = "Select where you want to Save your file.";
            saveFileDialog1.InitialDirectory = Settings.Default.CalibrationReports;
            //saveFileDialog1.InitialDirectory = Environment.CurrentDirectory;

            //Output path and file name for when the tests are finished
            saveFileDialog1.FileName = txtID.Text + "-" + DateTime.Today.Year.ToString().Substring(2) + ".xlsx";
            using (new CenterMessage(this))
            {
                if (saveFileDialog1.ShowDialog() == DialogResult.Cancel)
                {
                    tests.Clear();
                    AbortTestThread();
                    testManager = null;

                    for (int i = Application.OpenForms.Count - 1; i >= 0; i--)
                    {
                        if (Application.OpenForms[i].Name != "MainForm")
                            Application.OpenForms[i].Close();
                    }
                }
            }
            SaveDataName = saveFileDialog1.FileName;
        }

        //Save file before closing Excel 
        public void CloseExcel()
        {
            //Save the datasheet
            try
            {
                DataWorkbook.SaveAs(SaveDataName, System.Reflection.Missing.Value, System.Reflection.Missing.Value, System.Reflection.Missing.Value,
                                               System.Reflection.Missing.Value, System.Reflection.Missing.Value, Excel.XlSaveAsAccessMode.xlNoChange,
                                               System.Reflection.Missing.Value, System.Reflection.Missing.Value, System.Reflection.Missing.Value,
                                               System.Reflection.Missing.Value, System.Reflection.Missing.Value);
                
                DataWorkbook.Close(true, DataPathOpen, System.Reflection.Missing.Value);
            }

            //Quit Excel within the program
            finally
            {
                if (eApp != null)
                {
                    eApp.Quit();
                }
            }
        }






        /*   Main function to run the tests   */

        private void RunTests()
        {
            //Warning to save any open Excel files before tests start
            closeExcelWarning();

            //Open file location
            ExcelSavePath();

            //Uses existing file in chosen save folder if exists. Otherwise uses template
            if (File.Exists(SaveDataName)) DataPathOpen = SaveDataName;
            else DataPathOpen = Settings.Default.AppDataPath + @"\Datasheet.xlsx";
            //DataPathOpen = @"C:\Users\andavis\Desktop\Datasheet.xlsx";

            if (OpenExcel()) SetupExcel();
            else return;

            //Populate tests in the queue
            foreach (int ctest in chbTests.CheckedIndices)
            {
                switch (ctest)
                {
                    case 0:
                        tests.Enqueue(new TypeE(ectron, daq, _34970, _34980, this, TypeE1, TypeE2, TypeE3, TypeE4, TypeE5));
                        break;
                    case 1:
                        tests.Enqueue(new TypeJ(ectron, daq, _34970, _34980, this, TypeJ1, TypeJ2, TypeJ3, TypeJ4, TypeJ5));
                        break;
                    case 2:
                        tests.Enqueue(new TypeK(ectron, daq, _34970, _34980, this, TypeK1, TypeK2, TypeK3, TypeK4, TypeK5));
                        break;
                    case 3:
                        tests.Enqueue(new TypeT(ectron, daq, _34970, _34980, this, TypeT1, TypeT2, TypeT3, TypeT4, TypeT5));
                        break;
                }
            }

            //Run all tests if none are selected
            if (tests.Count == 0)
            {
                SelectBox(0, true);
                SelectBox(1, true);
                SelectBox(2, true);
                SelectBox(3, true);
                tests.Enqueue(new TypeE(ectron, daq, _34970, _34980, this, TypeE1, TypeE2, TypeE3, TypeE4, TypeE5));
                tests.Enqueue(new TypeJ(ectron, daq, _34970, _34980, this, TypeJ1, TypeJ2, TypeJ3, TypeJ4, TypeJ5));
                tests.Enqueue(new TypeK(ectron, daq, _34970, _34980, this, TypeK1, TypeK2, TypeK3, TypeK4, TypeK5));
                tests.Enqueue(new TypeT(ectron, daq, _34970, _34980, this, TypeT1, TypeT2, TypeT3, TypeT4, TypeT5));
            }


            if (InstrConnected())
            {
                if (testManager == null)
                {
                    testManager = new TestManager(tests);
                    testManager.checkedListBox = chbTests;
                    testManager.ActiveInstruments = activeInstruments;

                    if (!testManager.RunTests())
                    {
                        CloseExcel();
                        AbortTestThread();
                    }
                }
            }

            //Clear queue and close excel after tests are done
            tests.Clear();
            testManager = null;
            foreach (int item in chbTests.CheckedIndices)
            {
                SelectBox(item, false);
            }
            CloseExcel();

            ResetBtnName();

            WriteToOutput("  Tests Completed.\n");
        } 
    }










    /*   Text box extension to allow text to change color   */

    public static class RichTextBoxExtensions
    {
        public static void AppendText(this RichTextBox box, string text, Color color)
        {
            box.SelectionStart = box.TextLength;
            box.SelectionLength = 0;

            box.SelectionColor = color;
            box.AppendText(text);
            box.SelectionColor = box.ForeColor;
        }
    }



    /*    Classes for APIs to work    */

    public class AssetInfo
    {
        public bool exists { get; set; }
        public string id { get; set; }
        public string serial { get; set; }
        public string manufacturer { get; set; }
        public string model { get; set; }
        public string description { get; set; }
        public string type { get; set; }
        public string subtype { get; set; }
        public string cal_lab { get; set; }
        public string cal_due_date { get; set; }
    }

    public class FlukeReading
    {
        public bool exists { get; set; }
        public int site_id { get; set; }
        public string ip { get; set; }
        public string dewk_serial { get; set; }
        public string sensor1_serial { get; set; }
        public double ch1_temp { get; set; }
        public double ch1_humidity { get; set; }
        public object sensor2_serial { get; set; }
        public object ch2_temp { get; set; }
        public object ch2_humidity { get; set; }
        public DateTime timestamp { get; set; }
        public string sensor1_id { get; set; }
        public string sensor1_cal_due { get; set; }
        public string sensor2_id { get; set; }
        public string sensor2_cal_due { get; set; }
    }

    public class CalDueDatesRequestContent
    {
        public string username { get; set; }
        public string password { get; set; }
        public string[] asset_ids { get; set; }
    }
}
