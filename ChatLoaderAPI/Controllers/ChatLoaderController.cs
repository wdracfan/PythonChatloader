using ChatLoaderAPI.Business_Logic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Npgsql;

namespace ChatLoaderAPI.Controllers;

/// <summary>
/// ChatLoader controller
/// </summary>
[ApiController]
[Route("[controller]")]
public class ChatLoaderController : ControllerBase
{
    private readonly ILogger<ChatLoaderController> _logger;
    private readonly NpgsqlConnection _conn;
    private readonly int _delayMilliseconds;

    private const string UrlStart = "http://test-site.com/api/";

    public ChatLoaderController(
        ILogger<ChatLoaderController> logger, 
        IOptions<PostgresOptions> postgresOptions,
        IOptions<DelayOptions> delayOptions)
    {
        _logger = logger;
        _conn = new NpgsqlConnection(postgresOptions.Value.ConnectionString);
        _delayMilliseconds = delayOptions.Value.Milliseconds;
    }

    /// <summary>
    /// Add channel
    /// </summary>
    /// <param name="handle">channel handle</param>
    /// <returns>smth</returns>
    [HttpPost]
    [Route("add-channel")]
    public async Task<IResult> AddChannel([FromQuery] string? handle)
    {
        if (handle is null)
        {
            return Results.BadRequest("Handle cannot be empty! Your request has not been accepted.");
        }

        try
        {
            await RequestProcessing.ProcessRequest(UrlStart + $"add-channel/@{handle}", _conn);
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }
        
        return Results.Ok("Your request has been accepted.");
    }

    /// <summary>
    /// Get message
    /// </summary>
    /// <param name="channelId">channel id</param>
    /// <returns>smth</returns>
    [HttpPost]
    [Route("get-messages")]
    public async Task<IResult> DownloadMessageByChannelId([FromQuery] int? channelId)
    {
        if (channelId is null)
        {
            return Results.BadRequest("Message ID cannot be empty! Your request has not been accepted.");
        }
        
        try
        {
            await RequestProcessing.ProcessRequest(UrlStart + $"get-messages/{channelId}", _conn);
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }

        return Results.Ok("Your request has been accepted.");
    }

    //not required at the moment
    /*     
    [HttpPost]
    [Route("get-messages-date")]
    public async Task<IResult> DownloadMessageByDate(
        [FromQuery] string? channelHandle,
        [FromQuery] DateSpan? dateSpan,
        [FromQuery] DateTime date)
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
    */
    
    /// <summary>
    /// Show message
    /// </summary>
    /// <param name="channelId">channel id</param>
    /// <returns>smth</returns>
    [HttpGet]
    [Route("show-messages")]
    public async Task<IResult> ShowMessageByChannelId([FromQuery] int? channelId)
    {
        if (channelId is null)
        {
            return Results.BadRequest("Message ID cannot be empty! Your request has not been accepted.");
        }
        
        try
        {
            var reqId = await RequestProcessing.SendShowRequest(UrlStart + $"show-messages/{channelId}", _conn);

            //for the bot to update the response
            await Task.Delay(_delayMilliseconds);

            var response = await RequestProcessing.GetAnswer(_conn, reqId);
            if (response is not null)
            {
                return Results.Ok(response);
            }
            else
            {
                return Results.Ok("The response is not ready yet. Please try later.");
            }
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }
    }
}