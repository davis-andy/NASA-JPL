
namespace DAQ_modules
{
    abstract class Test
    {
        abstract public bool RunTest();

        abstract public string Name { get; }
    }
}
