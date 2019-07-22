'use strict';

const functions = require('firebase-functions');

var rp = require('request-promise');


exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
    var options = '';
    if (request.body.queryResult.intent.displayName === 'getJoeySpecified'){
      	options = {
          url: 'https://tuftsjoeytracker.herokuapp.com/getJoeySpecified',
          headers: {
              'User-Agent': 'Request-Promise',
              'data' : request.body.queryResult.parameters.tufts_locations
          },
          json: true // Automatically parses the JSON string in the response
    	};
    } else if (request.body.queryResult.intent.displayName === 'getJoeyUnspecified') {
        options = {
          url: 'https://tuftsjoeytracker.herokuapp.com/getJoeyUnspecified',
          json: true // Automatically parses the JSON string in the response
    	};
    }
    
    var theResponse = 'default';
    rp(options).then( function (htmlString) {
        response.send(JSON.stringify(htmlString));
    }).catch(function (err) {
        response.send(JSON.stringify({"fulfillmentText": err}));
    });
});

