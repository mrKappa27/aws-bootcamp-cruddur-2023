# Week 3 — Decentralized Authentication

## TL;DR
Followed all the class parts and Todo Checklist: \
Set up Cognito User Pool \
Implement Custom Sign-In Page \
Implement Custom Sign-Up Page \
Implement Custom Confirmation Page \
Implement Custom Recovery Page \
Implement Cognito JWT Server side Verify \
Adjusted tracing code for using real user_ids (connecting the dots)

I couldn't complete the stretched homeworks due to lack of time caused by the fact that I've a regular day to day job.

## Install AWS Amplify

In the frontend folder:
```sh
npm i aws-amplify --save
```

## Provision Cognito User Group

Using the AWS Console we create a Cognito User Group

![Cognito User Group Proof](assets/week3-cognito-user-pool-proof.png)

If you manually create a user it will be created in a state where it's necessary to change the password at first login.
If you wanto to force to pass this state follow this [thread](https://stackoverflow.com/questions/40287012/how-to-change-user-status-force-change-password):
```
aws cognito-idp admin-set-user-password \
  --user-pool-id <your-user-pool-id> \
  --username <username> \
  --password <password> \
  --permanent
```

## Configure Amplify

We need to hook up our cognito pool to our code in the `App.js`

[Link to documentation](https://www.npmjs.com/package/amazon-cognito-identity-js)

```js
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
  "aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_AWS_USER_POOLS_WEB_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
});
```

## Conditionally show components based on logged in or logged out

Show, hide or change components based on login status.

Inside our `HomeFeedPage.js`

```js
import { Auth } from 'aws-amplify';

// set a state
const [user, setUser] = React.useState(null);

// check if we are authenicated
const checkAuth = async () => {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    return Auth.currentAuthenticatedUser()
  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));
};

// check when the page loads if we are authenicated
React.useEffect(()=>{
  loadData();
  checkAuth();
}, [])
```

We'll want to pass user to the following components:

```js
<DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
<DesktopSidebar user={user} />
```

We'll rewrite `DesktopNavigation.js` so that it it conditionally shows links in the left hand column
on whether you are logged in or not.

Notice we are passing the user to ProfileInfo

```js
import './DesktopNavigation.css';
import {ReactComponent as Logo} from './svg/logo.svg';
import DesktopNavigationLink from '../components/DesktopNavigationLink';
import CrudButton from '../components/CrudButton';
import ProfileInfo from '../components/ProfileInfo';

export default function DesktopNavigation(props) {

  let button;
  let profile;
  let notificationsLink;
  let messagesLink;
  let profileLink;
  if (props.user) {
    button = <CrudButton setPopped={props.setPopped} />;
    profile = <ProfileInfo user={props.user} />;
    notificationsLink = <DesktopNavigationLink 
      url="/notifications" 
      name="Notifications" 
      handle="notifications" 
      active={props.active} />;
    messagesLink = <DesktopNavigationLink 
      url="/messages"
      name="Messages"
      handle="messages" 
      active={props.active} />
    profileLink = <DesktopNavigationLink 
      url="/@andrewbrown" 
      name="Profile"
      handle="profile"
      active={props.active} />
  }

  return (
    <nav>
      <Logo className='logo' />
      <DesktopNavigationLink url="/" 
        name="Home"
        handle="home"
        active={props.active} />
      {notificationsLink}
      {messagesLink}
      {profileLink}
      <DesktopNavigationLink url="/#" 
        name="More" 
        handle="more"
        active={props.active} />
      {button}
      {profile}
    </nav>
  );
}
```

We'll update `ProfileInfo.js`

```js
import { Auth } from 'aws-amplify';

const signOut = async () => {
  try {
      await Auth.signOut({ global: true });
      window.location.href = "/"
  } catch (error) {
      console.log('error signing out: ', error);
  }
}
```

We'll rewrite `DesktopSidebar.js` so that it conditionally shows components in case you are logged in or not.

```js
import './DesktopSidebar.css';
import Search from '../components/Search';
import TrendingSection from '../components/TrendingsSection'
import SuggestedUsersSection from '../components/SuggestedUsersSection'
import JoinSection from '../components/JoinSection'

export default function DesktopSidebar(props) {
  const trendings = [
    {"hashtag": "100DaysOfCloud", "count": 2053 },
    {"hashtag": "CloudProject", "count": 8253 },
    {"hashtag": "AWS", "count": 9053 },
    {"hashtag": "FreeWillyReboot", "count": 7753 }
  ]

  const users = [
    {"display_name": "Andrew Brown", "handle": "andrewbrown"}
  ]

  let trending;
  if (props.user) {
    trending = <TrendingSection trendings={trendings} />
  }

  let suggested;
  if (props.user) {
    suggested = <SuggestedUsersSection users={users} />
  }
  let join;
  if (props.user) {
  } else {
    join = <JoinSection />
  }

  return (
    <section>
      <Search />
      {trending}
      {suggested}
      {join}
      <footer>
        <a href="#">About</a>
        <a href="#">Terms of Service</a>
        <a href="#">Privacy Policy</a>
      </footer>
    </section>
  );
}
```

## Signin Page

```js
import { Auth } from 'aws-amplify';

const onsubmit = async (event) => {
  setErrors('')
  event.preventDefault();
  try {
    Auth.signIn(email, password)
      .then(user => {
        localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
        window.location.href = "/"
      })
      .catch(err => { console.log('Error!', err) });
  } catch (error) {
    if (error.code == 'UserNotConfirmedException') {
      window.location.href = "/confirm"
    }
    setErrors(error.message)
  }
  return false
}

let errors;
if (cognitoErrors){
  errors = <div className='errors'>{cognitoErrors}</div>;
}

// just before submit component
{errors}
```
Successful login with preferred_username + user logged on console:
![Week 3 login proof](assets/week3-cognito-pref-username-login-proof.png)

## Signup Page

```js
import { Auth } from 'aws-amplify';

const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
      const { user } = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
          name: name,
          email: email,
          preferred_username: username,
        },
        autoSignIn: { // optional - enables auto sign in after user is confirmed
            enabled: true,
        }
      });
      console.log(user);
      window.location.href = `/confirm?email=${email}`
  } catch (error) {
      console.log(error);
      setErrors(error.message)
  }
  return false
}

let errors;
if (cognitoErrors){
  errors = <div className='errors'>{cognitoErrors}</div>;
}

//before submit component
{errors}
```

## Confirmation Page

```js
import { Auth } from 'aws-amplify';

const resend_code = async (event) => {
  setErrors('')
  try {
    await Auth.resendSignUp(email);
    console.log('code resent successfully');
    setCodeSent(true)
  } catch (err) {
    // does not return a code
    // does cognito always return english
    // for this to be an okay match?
    console.log(err)
    if (err.message == 'Username cannot be empty'){
      setErrors("You need to provide an email in order to send Resend Activiation Code")   
    } else if (err.message == "Username/client id combination not found."){
      setErrors("Email is invalid or cannot be found.")   
    }
  }
}

const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
    await Auth.confirmSignUp(email, code);
    window.location.href = "/"
  } catch (error) {
    setErrors(error.message)
  }
  return false
}
```

Successful registration and code verification:
![Week 3 verification proof](assets/week3-registration-flow-proof.png)

## Recovery Page

```js
import { Auth } from 'aws-amplify';

const onsubmit_send_code = async (event) => {
  event.preventDefault();
  setErrors('')
  Auth.forgotPassword(username)
  .then((data) => setFormState('confirm_code') )
  .catch((err) => setErrors(err.message) );
  return false
}

const onsubmit_confirm_code = async (event) => {
  event.preventDefault();
  setErrors('')
  if (password == passwordAgain){
    Auth.forgotPasswordSubmit(username, code, password)
    .then((data) => setFormState('success'))
    .catch((err) => setErrors(err.message) );
  } else {
    setErrors('Passwords do not match')
  }
  return false
}
```

Here the password forgot screen:
![Week 3 forgot proof](assets/week3-forgot-flow-proof.png)
![Week 3 forgot 2 proof](assets/week3-forgot-flow-2-proof.png)

After that I logged in as usual.

## Authenticating Server Side

This is for verifing that the request is allowed, this is done by checking the Token we stored in the frontend local storage, sent to the server as `Authentication` header.

Add in the `HomeFeedPage.js` a header to be passed along the access token 

```js
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`
  }
```

For avoiding CORS issues place in the `app.py`:

```py
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)
```

In the `app.py` we add this code for checking if we can correctly grab the token from the request:
```py
  # Get out Auth Bearer Token
  app.logger.info('AUTH HEADER: ')
  app.logger.info(request.headers.get('Authorization'))
```

![Week 3 print auth token proof](assets/week3-print-auth-token-proof.png)

For validating our JWT token server side we create a new folder `lib` and we add `cognito_token_verification.py` file.

We'll take inspiration from [this project](https://github.com/cgauge/Flask-AWSCognito).

We've then adapted the code live. For further info about the process please follow the [video](https://www.youtube.com/watch?v=d079jccoG-M&t=1s).

After some tinkering we've been able to validate our JWT token on the server side:

![Week 3 jwt token serverside proof](assets/week3-success-auth-verification-proof.png)
Note: I didn't had the audience mismatch error.

Here the custom "extra" message returned for logged in users:
![Week 3 login api proof](assets/week3-custom-login-home-api-proof.png)

I added the real `user_id` to the traces we send to Honeycomb:
```py
span.set_attribute("app.user_id", cognito_user_id)
```
![Week 3 Honeycomb userid proof](assets/week3-honeycomb-id-proof.png)

## Required Homeworks/Tasks
- Completed all the todo and technical tasks ✅
- Set up Cognito User Pool ✅
- Implement Custom Sign-In Page ✅
- Implement Custom Sign-Up Page ✅
- Implement Custom Confirmation Page ✅
- Implement Custom Recovery Page ✅
- Implement Cognito JWT Server side Verify ✅
- Adjusted tracing code for using real user_ids ✅