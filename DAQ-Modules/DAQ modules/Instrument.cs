using NationalInstruments.Visa;

namespace DAQ_modules
{
    abstract public class Instrument
    {
        //Message Based Session and Resource Manager
        MessageBasedSession mbSession;
        ResourceManager rmSession = new ResourceManager();


        abstract public string IDN
        {
            get;
            set;
        }
        abstract public int GPIB
        {
            get;
            set;
        }
        public void getIDN(string address)
        {
            try
            {
                mbSession = (MessageBasedSession)rmSession.Open(address);
                mbSession.RawIO.Write("*IDN?");
                //idnS = mbSession.RawIO.ReadString();
            }
            catch
            {

            }
        }
    }
}
