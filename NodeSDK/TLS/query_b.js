var hfc = require('hfc');
var util = require('util');
var fs = require('fs');
const https = require('https');

// Create a client blockchin.
var chain = hfc.newChain("targetChain");

// Configure the KeyValStore which is used to store sensitive keys.
// This data needs to be located or accessible any time the users enrollmentID
// perform any functions on the blockchain.  The users are not usable without
// This data.
// Please ensure you have a /tmp directory prior to placing the keys there.
// If running on windows or mac please review the path setting.
chain.setKeyValStore(hfc.newFileKeyValStore('/tmp/keyValStore'));

// barryrat think about removing
process.env['GRPC_SSL_CIPHER_SUITES'] = 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES256-GCM-SHA384';

// Read and process the credentials.json
var network;
try {
  network = JSON.parse(fs.readFileSync('ServiceCredentials.json', 'utf8'));
} catch (err){
  console.log("ServiceCredentials.json is missing, Rerun once the file is available")
  process.exit();
}


var peers = network.credentials.peers;
var users = network.credentials.users;

// Determining if we are running on a startup or HSBN network based on the url
// of the discovery host name.  The HSBN will contain the string zone.
var isHSBN = peers[0].discovery_host.indexOf('zone') >= 0 ? true : false;
var peerAddress = [];
var network_id = Object.keys(network.credentials.ca);
var ca_url = "grpcs://" + network.credentials.ca[network_id].discovery_host + ":"+network.credentials.ca[network_id].discovery_port;

if (!isHSBN) {
    //HSBN uses RSA generated keys
    chain.setECDSAModeForGRPC(true)
}

var certFile = 'certificate.pem';
var certUrl = network.credentials.cert;
fs.access(certFile, (err) => {
    if (!err) {
        console.log("\nDeleting existing certificate ", certFile);
        fs.unlinkSync(certFile);
    }
    downloadCertificate();
    //enrollAndRegisterUsers();
});

function downloadCertificate(){
  https.get(certUrl, (res) => {
      console.log('\nDownloading certificate ', certFile);

      res.on('data', (d) => {
          fs.appendFile(certFile, d, (err) => {
              if (err) throw err;
          });
      });
      res.on('end', function() {
          fs.appendFile(certFile, "\n", (err) => {
              if (err) throw err;
              enrollAndRegisterUsers();
          });
      });
  }).on('error', (e) => {
      console.error(e);
      process.exit();
  });
}

function enrollAndRegisterUsers() {
    var cert = fs.readFileSync(certFile);
    chain.setMemberServicesUrl(ca_url, {
        pem: cert
    });

    // Adding all the peers to blockchain
    // this adds high availability for the client
    for (var i = 0; i < peers.length; i++) {
        chain.addPeer("grpcs://" + peers[i].discovery_host + ":" + peers[i].discovery_port, {
            pem: cert
        });
    }

    /*console.log("------------- peers and caserver information: -------------");
    console.log(chain.getPeers());
    console.log(chain.getMemberServices());
    console.log('-----------------------------------------------------------');*/
    var testChaincodeID;

    // Enroll a 'admin' who is already registered because it is
    // listed in fabric/membersrvc/membersrvc.yaml with it's one time password.
    chain.enroll(users[0].username, users[0].secret, function(err, admin) {
        if (err) throw Error("\nERROR: failed to enroll admin : %s", err);

        console.log("\nEnrolled admin sucecssfully");

        // Set this user as the chain's registrar which is authorized to register other users.
        chain.setRegistrar(admin);
        var userName = users[1].username;
        var userSecret = users[1].secret;

        chain.enroll(userName, userSecret, function(err, WebAppAdmin) {
            if (err) throw Error("\nERROR: failed to enroll WebAppAdmin : %s", err);
            //chain.setRegistrar(WebAppAdmin);

            console.log("\nEnrolled WebAppAdmin sucecssfully");
            var enrollName = users[1].username; // "JohnDoe";
            var registrationRequest = {
                enrollmentID: enrollName,
                //affiliation: "group1"
                account: "group1",
                affiliation: "00001"
            };
            chain.registerAndEnroll(registrationRequest, function(err, user) {
                if (err) throw Error(" Failed to register and enroll " + enrollName + ": " + err);

                console.log("\nEnrolled and registered "+enrollName+ " successfully");

                //setting timers for fabric waits
                //chain.setDeployWaitTime(80);
                chain.setInvokeWaitTime(2);
                //console.log("\nDeploying chaincode ...")
                //deployChaincode(user);
				queryUser(user);
            });
        });
    });
}

function queryUser(user) {
    // Construct the query request
    var queryRequest = {
        // Name (hash) required for query
        chaincodeID: "94314ca89392713f4a109a1d5524926b872ea9cdbe17c948b27c7989c0f6a65e",
        // Function to trigger
        fcn: "query",
        // Existing state variable to retrieve
        args: ["b"]
    };

    // Trigger the query transaction
    var queryTx = user.query(queryRequest);

    // Print the query results
    queryTx.on('complete', function(results) {
        // Query completed successfully
        console.log("\nSuccessfully queried  chaincode function: request=%j, value=%s", queryRequest, results.result.toString());
    });
    queryTx.on('error', function(err) {
        // Query failed
        console.log("\nFailed to query chaincode, function: request=%j, error=%j", queryRequest, err);
    });
}