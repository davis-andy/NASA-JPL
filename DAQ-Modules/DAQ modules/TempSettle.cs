using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DAQ_modules
{
    public partial class TempSettle : Form
    {
        /*   Global variables for Temperature Settle Form   */

        //Calculated Time variables
        double timeLeft;
        int minutes, seconds;

        //Shown Time variables
        int timeShown, minutesShown, secondsShown;




        /*   Temperature Settle Form functions   */

        //Temp Settle Initializer with amount of time minus one second
        public TempSettle(double timeout)
        {
            InitializeComponent();
            timer1.Start();
            timeLeft = timeout/1000;

            //Convert milliseconds to show minutes and seconds plus one second
            timeShown = (int)(timeout / 1000) + 1;
            minutesShown = timeShown / 60;
            secondsShown = timeShown % 60;
        }
        
        //Timer tick, update form text
        private void timer1_Tick(object sender, EventArgs e)
        {
            minutes = (int)timeLeft / 60;
            seconds = (int)timeLeft % 60;

            if (timeLeft > 0)
            {
                timeLeft--;
                lblTimer.Text = string.Format("{0}:{1}", minutes.ToString().PadLeft(2, '0'), seconds.ToString().PadLeft(2, '0'));
            }

            else
            {
                timer1.Stop();
                this.Close();
            }
        }

        //Upon form shown, timer shows true time amount
        private void TempSettle_Shown(object sender, EventArgs e)
        {
            lblTimer.Text = string.Format("{0}:{1}", minutesShown.ToString().PadLeft(2, '0'), secondsShown.ToString().PadLeft(2, '0'));
        }
    }
}
