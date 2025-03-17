//
// config.js
//
// Web service configuration parameters, separate
// from our musicapp-config file that contains 
// AWS-specific configuration information.
//

const config = {
  musicapp_config: "musicapp-config.ini",
  musicapp_profile: "s3readwrite",
  service_port: 8080,
  page_size: 12
};

module.exports = config;
