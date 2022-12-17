using System;
using NationalInstruments.Visa;

namespace DAQ_modules
{
    public class Ectron
    {
        /*   Global variables for Ectron Instrument   */

        //Message Based Session and Resource Manager
        MessageBasedSession mbSession;
        ResourceManager rmSession = new ResourceManager();

        string idnString;




        /*   Ectron Functions   */

        //Ectron Initializer
        public Ectron()
        {
            //gpib = 16;
            //getIDN();
        }

        //Ectron Initializer with GPIB
        public Ectron(string address)
        {
            getIDN(address);
        }

        //Get Set variables
        public string IDN => idnString;
        
        //Retrieve Ectron's ID
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

        public string Serial() 
        {
            mbSession.RawIO.Write(":SYST:SER?");

            return mbSession.RawIO.ReadString().Trim();
        }

        public void Standby(string onoff) { mbSession.RawIO.Write(string.Format(":OUTP:STAN {0}", onoff)); } //ON, OFF

        public void Type(string type) { mbSession.RawIO.Write(string.Format(":INST:THER:TYPE {0}-MN175", type)); } //E, J, K, T

        public void Temp(int temp) { mbSession.RawIO.Write(string.Format(":SOUR:TEMP:VAL {0}", temp)); } //Temperature settings from the other instruments
    }
}
