using ChatLoaderAPI.Data_Access;
using Npgsql;

namespace ChatLoaderAPI.Business_Logic;

public static class RequestProcessing
{
    public static async Task ProcessRequest(string requestUrl, NpgsqlConnection conn)
    {
        var requestRow = new RequestRow(requestUrl, DateTime.Now);
        await DbMethods.Commit(requestRow, conn);
    }
}