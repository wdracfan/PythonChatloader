using Dapper;
using Npgsql;

namespace ChatLoaderAPI.Data_Access;

public static class DbMethods
{
    public static async Task Commit(RequestRow request, NpgsqlConnection conn)
    {
        const string tableName = "test.requests";
        var sqlQuery = @$"INSERT INTO {tableName} (url, request_time)
                               VALUES ('{request.url}', '{request.request_time}')";
        await conn.ExecuteAsync(sqlQuery);
    }
}