// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');
 
process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function welcome(agent) {
    agent.add(`Welcome to my agent!`);
  }
 
  function fallback(agent) {
    agent.add(`I didn't understand`);
    agent.add(`I'm sorry, can you try again?`);
  }


  // var data = [
  // [

  //   ['8:00:00', '8:31:00',  '9:02:00',  '9:33:00',  '10:04:00', '10:35:00', '11:21:00', '11:52:00', '12:23:00', '12:54:00', '13:25:00', '13:56:00', '14:57:00', '15:28:00', '16:02:00', '16:33:00', '17:13:00', '17:44:00', '18:28:00', '18:56:00', '19:24:00', '19:52:00', '20:20:00', '20:48:00', '21:44:00', '22:12:00', '22:39:00'],    ['8:07:00', '8:38:00',  '9:09:00',  '9:40:00',  '10:11:00', '10:42:00', '11:28:00', '11:59:00', '12:30:00', '13:01:00', '13:32:00', '14:03:00', '15:04:00', '15:35:00', '16:09:00', '16:40:00', '17:20:00', '17:51:00', '18:35:00', '19:03:00', '19:31:00', '19:59:00', '20:27:00', '20:55:00', '21:51:00', '22:19:00', '22:45:00'],    ['8:09:00', '8:40:00',  '9:11:00',  '9:42:00',  '10:13:00', '10:44:00', '11:30:00', '12:01:00', '12:32:00', '13:03:00', '13:34:00', '14:05:00', '15:06:00', '15:37:00', '16:11:00', '16:42:00', '17:22:00'],    ['8:17:00', '8:48:00',  '9:19:00',  '9:50:00',  '10:21:00', '10:52:00', '11:38:00', '12:09:00', '12:40:00', '13:11:00', '13:42:00', '14:13:00', '15:14:00', '15:45:00', '16:19:00', '16:50:00', '17:30:00', '17:58:00', '18:42:00', '19:10:00', '19:38:00', '20:06:00', '20:34:00', '21:02:00', '21:58:00', '22:26:00', '22:51:00'],    ['8:22:00', '8:53:00',  '9:24:00',  '9:55:00',  '10:26:00', '10:57:00', '11:43:00', '12:14:00', '12:45:00', '13:16:00', '13:47:00', '14:18:00', '15:19:00', '15:50:00', '16:24:00', '16:55:00', '17:35:00', '18:03:00', '18:47:00', '19:15:00', '19:43:00', '20:11:00', '20:39:00', '21:07:00', '22:03:00', '22:31:00'],    ['8:24:00', '8:55:00',  '9:26:00',  '9:57:00',  '10:28:00', '10:59:00', '11:45:00', '12:16:00', '12:47:00', '13:18:00', '13:49:00', '14:20:00', '15:21:00', '15:55:00', '16:26:00', '17:06:00', '17:37:00', '18:05:00', '18:49:00', '19:17:00', '19:45:00', '20:13:00', '20:41:00', '21:09:00', '22:05:00', '22:33:00']

  // ]
  // ];


  function getJS(agent) {
    const location = agent.parameters.tufts_locations;
    agent.add(location);
    agent.add(`This message is from Dialogflow's Cloud Functions for Firebase editor!`);

    var today = new Date();
    var date  = today.getDay();
    agent.add('today is' + today.getDay());
    var data = [[['a']]];
    agent.data(data[0][0][0]);
    console.log('data' + data[0][0][0]);
  }
  // // Uncomment and edit to make your own Google Assistant intent handler
  // // uncomment `intentMap.set('your intent name here', googleAssistantHandler);`
  // // below to get this function to be run when a Dialogflow intent is matched
  // function googleAssistantHandler(agent) {
  //   let conv = agent.conv(); // Get Actions on Google library conv instance
  //   conv.ask('Hello from the Actions on Google client library!') // Use Actions on Google library
  //   agent.add(conv); // Add Actions on Google library responses to your agent's response
  // }
  // // See https://github.com/dialogflow/dialogflow-fulfillment-nodejs/tree/master/samples/actions-on-google
  // // for a complete Dialogflow fulfillment library Actions on Google client library v2 integration sample

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('get_joey_specified', getJS);
  // intentMap.set('your intent name here', googleAssistantHandler);
  agent.handleRequest(intentMap);
});
