using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using customerfeedback_web.Models;

using MongoDB.Bson;
using MongoDB.Driver;

using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Queue;
using Newtonsoft.Json;

namespace customerfeedback_web.Controllers
{
    public class HomeController : Controller
    {
        string mongoUrl;
        string speechKey;
        string storageAccountName;
        string storageAccountKey;

        protected static IMongoClient _client;
        protected static IMongoDatabase _database;
        


        public HomeController()
        {
            // Read env variables
            mongoUrl = Environment.GetEnvironmentVariable("MONGO_URL");
            speechKey = Environment.GetEnvironmentVariable("SPEECH_KEY");
            storageAccountName = Environment.GetEnvironmentVariable("STORAGEACCOUNT_NAME");
            storageAccountKey = Environment.GetEnvironmentVariable("STORAGEACCOUNT_KEY");

            _client = new MongoClient(new MongoUrl(mongoUrl));
            _database = _client.GetDatabase("crm");
        }
        public IActionResult Index()
        {
            ViewBag.SpeechKey = speechKey;
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Index(string feedback, string email)
        {
            var randomId = Guid.NewGuid();

            // Store in Cosmos DB (Mongo DB)
            var document = new BsonDocument
            {
                { "email", email },
                { "feedback", feedback },
                { "feedback_id",  randomId.ToString()}
            };

            var collection = _database.GetCollection<BsonDocument>("feedback");
            await collection.InsertOneAsync(document);

            // Send message to Queue
            var storageAccount = CloudStorageAccount.Parse(
                "DefaultEndpointsProtocol=http;AccountName=" + storageAccountName + ";AccountKey=" + storageAccountKey
            );

             var queueClient = storageAccount.CreateCloudQueueClient();
             var messageQueue = queueClient.GetQueueReference("feedbackqueue");
             await messageQueue.CreateIfNotExistsAsync();

             var feedbackDetails = new {
                email = email,
                feedback=feedback,
                feedback_id=randomId.ToString()
             };

             var queueMessage = new CloudQueueMessage(JsonConvert.SerializeObject(feedbackDetails));
             await messageQueue.AddMessageAsync(queueMessage);

            // Go back to index
            return RedirectToAction("Index"); 
        }  

        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
