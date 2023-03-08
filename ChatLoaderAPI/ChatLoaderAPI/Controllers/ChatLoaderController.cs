using ChatLoaderAPI.Business_Logic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Npgsql;

namespace ChatLoaderAPI.Controllers;

[ApiController]
[Route("[controller]")]
public class ChatLoaderController : ControllerBase
{
    private readonly ILogger<ChatLoaderController> _logger;
    private readonly NpgsqlConnection _conn;

    public ChatLoaderController(ILogger<ChatLoaderController> logger, IOptions<PostgresOptions> postgresOptions)
    {
        _logger = logger;
        _conn = new NpgsqlConnection(postgresOptions.Value.ConnectionString);
    }

    [HttpPost]
    [Route("monitor")]
    public async Task<IResult> StartMonitoring([FromQuery] string? handle)
    {
        if (handle is null)
        {
            return Results.BadRequest("Handle cannot be empty! Your request has not been accepted.");
        }

        try
        {
            await RequestProcessing.ProcessRequest(Request.Path + Request.QueryString, _conn);
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }
        
        return Results.Ok("Your request has been accepted.");
    }

    [HttpPost]
    [Route("download/id")]
    public async Task<IResult> DownloadMessageById([FromQuery] string? channelHandle, [FromQuery] int? messageId)
    {
        if (channelHandle is null)
        {
            return Results.BadRequest("Handle cannot be empty! Your request has not been accepted.");
        }
        if (messageId is null)
        {
            return Results.BadRequest("Message ID cannot be empty! Your request has not been accepted.");
        }
        
        try
        {
            await RequestProcessing.ProcessRequest(Request.Path + Request.QueryString, _conn);
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }

        return Results.Ok("Your request has been accepted.");
    }

    [HttpPost]
    [Route("download/date")]
    public async Task<IResult> DownloadMessageByDate(
        [FromQuery] string? channelHandle,
        [FromQuery] DateSpan? dateSpan)
    {
        var startDate = dateSpan?.StartDate;
        var endDate = dateSpan?.EndDate;
        
        if (channelHandle is null)
        {
            return Results.BadRequest("Handle cannot be empty! Your request has not been accepted.");
        }

        if (startDate is null || startDate.Year is null || startDate.Month is null || startDate.Day is null)
        {
            return Results.BadRequest("Wrong start date format! Your request has not been accepted.");
        }
        
        if (endDate is null || endDate.Year is null || endDate.Month is null || endDate.Day is null)
        {
            return Results.BadRequest("Wrong end date format! Your request has not been accepted.");
        }
        
        try
        {
            await RequestProcessing.ProcessRequest(Request.Path + Request.QueryString, _conn);
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }
        
        return Results.Ok("Your request has been accepted.");
    }
    
    [HttpGet]
    [Route("show")]
    public async Task<IResult> ShowMessageById([FromQuery] string? channelHandle, [FromQuery] int? messageId)
    {
        if (channelHandle is null)
        {
            return Results.BadRequest("Handle cannot be empty! Your request has not been accepted.");
        }
        if (messageId is null)
        {
            return Results.BadRequest("Message ID cannot be empty! Your request has not been accepted.");
        }

        return Results.Ok(/* something here */);
    }
}