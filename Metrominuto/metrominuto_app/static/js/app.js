let url_widget = '';
function set_url_widget(string_url){
    url_widget = string_url;
}
let url_login = '';
function set_url_login(url_log){
    url_login = url_log;
}

/**
 * Redirects to the FirebaseUI widget.
 */
var signInWithRedirect = function() {
    window.location.assign(getWidgetUrl());
};


/**
 * Open a popup with the FirebaseUI widget.
 */
var signInWithPopup = function() {
    window.open(url_widget, 'Sign In', 'width=985,height=735');
};


/**
 * Displays the UI for a signed in user.
 * @param {!firebase.User} user
 */
var handleSignedInUser = function(user) {
    if (user) {
        var displayName = user.displayName;
        var email = user.email;
        var emailVerified = user.emailVerified;
        var photoURL = user.photoURL;
        var uid = user.uid;
        var phoneNumber = user.phoneNumber;
        var providerData = user.providerData;
        var data = {
            displayName: displayName,
            email: email,
            emailVerified: emailVerified,
            phoneNumber: phoneNumber,
            photoURL: photoURL,
            uid: uid,
            //accessToken: accessToken,
            providerData: providerData
        };
        const myForm = document.getElementById('myform');
        const user_data = document.createElement('input');
        user_data.type = 'hidden';
        user_data.name = 'user_data';
        user_data.value = JSON.stringify({data});
        myForm.appendChild(user_data);
        $('#myform').submit();
    }
    /*document.getElementById('user-signed-in').style.display = 'block';
    document.getElementById('user-signed-out').style.display = 'none';
    document.getElementById('name').textContent = user.displayName;
    document.getElementById('email').textContent = user.email;
    document.getElementById('phone').textContent = user.phoneNumber;
    if (user.photoURL) {
        var photoURL = user.photoURL;
        // Append size to the photo URL for Google hosted images to avoid requesting
        // the image with its original resolution (using more bandwidth than needed)
        // when it is going to be presented in smaller size.
        if ((photoURL.indexOf('googleusercontent.com') != -1) ||
            (photoURL.indexOf('ggpht.com') != -1)) {
            //photoURL = photoURL + '?sz=' +
                //document.getElementById('photo').clientHeight;
        }
        //document.getElementById('photo').src = photoURL;
        //document.getElementById('photo').style.display = 'block';
    } else {
        //document.getElementById('photo').style.display = 'none';
    }*/
};


/**
 * Displays the UI for a signed out user.
 */
var handleSignedOutUser = function() {
    //document.getElementById('user-signed-in').style.display = 'none';
    //document.getElementById('user-signed-out').style.display = 'block';
};


// Listen to change in auth state so it displays the correct UI for when
// the user is signed in or not.
firebase.auth().onAuthStateChanged(function(user) {
    //document.getElementById('loading').style.display = 'none';
    //document.getElementById('loaded').style.display = 'block';
    user ? handleSignedInUser(user) : handleSignedOutUser();
});

/**
 * Deletes the user's account.
 */
var deleteAccount = function() {
    firebase.auth().currentUser.delete().catch(function(error) {
        if (error.code == 'auth/requires-recent-login') {
            // The user's credential is too old. She needs to sign in again.
            firebase.auth().signOut().then(function() {
                // The timeout allows the message to be displayed after the UI has
                // changed to the signed out state.
                setTimeout(function() {
                    alert('Please sign in again to delete your account.');
                }, 1);
            });
        }
    });
};


/**
 * Initializes the app.
 */
var initApp = function() {
    document.getElementById('sign-in').addEventListener(
        'click', signInWithPopup);
    document.getElementById('sign-link').addEventListener(
        'click', signInWithPopup);
    /*document.getElementById('delete-account').addEventListener(
        'click', function() {
            deleteAccount();
        });*/
};

window.addEventListener('load', initApp);