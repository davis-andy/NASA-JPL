using System.Collections.Generic;
using System.Windows.Forms;

namespace DAQ_modules
{
    class TestManager
    {
        List<Instrument> activeInstruments;
        Queue<Test> testsToRun;
        bool testsRunning = false;
        CheckedListBox checkedList;
        Dictionary<string, int> getIndex;

        public TestManager(Queue<Test> tests)
        {
            testsToRun = tests;
            createDict();
        }

        public CheckedListBox checkedListBox { set => checkedList = value; }

        public List<Instrument> ActiveInstruments { get => activeInstruments; set => activeInstruments = value; }

        public bool isRunning()
        {
            return testsRunning;
        }

        //Take a wild guess
        public bool RunTests()
        {
            testsRunning = true;
            int tCount = testsToRun.Count;
            for (int i = 0; i < tCount; i++)
            {
                if (!testsRunning)
                    return false;
                if (!testsToRun.Dequeue().RunTest())
                    return false;
            }
            testsRunning = false;
            return true;
        }

        //Eventually will stop the tests
        public bool StopTests()
        {
            if (testsRunning)
            {
                testsRunning = false;
                return true;
            }
            else return false;
        }

        private void createDict()
        {
            getIndex = new Dictionary<string, int>
            {
                {"Type E",0},{"Type J",1},{"Type K",2},{"Type T",3}
            };
        }
    }
}
