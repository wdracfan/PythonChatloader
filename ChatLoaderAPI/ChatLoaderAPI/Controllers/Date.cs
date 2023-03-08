namespace ChatLoaderAPI.Controllers;

public class Date
{
    public int? Year { get; set; }
    public int? Month { get; set; }
    public int? Day { get; set; }

    public Date()
    {
        //
    }

    public override string ToString()
    {
        return new DateOnly((int)Year!, (int)Month!, (int)Day!).ToString();
    }
}