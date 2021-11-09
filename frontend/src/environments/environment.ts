/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://localhost:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-djfincy3.us', // the auth0 domain prefix
    audience: 'https://localhost:5000', // the audience set for the auth0 app
    clientId: 'XX0zerlWM9gAZO5MMTpi4KmPd127k9Je', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};


