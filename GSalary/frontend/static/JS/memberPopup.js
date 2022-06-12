// Check more insturction and explaination from this site: https://www.w3schools.com/howto/howto_css_modals.asp
let signInPopup = document.getElementById("signInPopup"); /*in index.html */
let registerPopup = document.getElementById("registerPopup"); /*in index.html */

// The variables below are to clear the text inside of the input field after the window colsed.
let clearNameBoxInput = document.getElementsByClassName("nameBox")[0];
let clearEmailBoxInputForSignIN =
  document.getElementsByClassName("emailBox")[0];
let clearEmailBoxInputForRegister =
  document.getElementsByClassName("emailBox")[1];
let clearPasswordBoxInputForSignIN =
  document.getElementsByClassName("passwordBox")[0];
let clearPasswordBoxInputForRegister =
  document.getElementsByClassName("passwordBox")[1];

// "in index.html" This function is all the log-in function source, which means if I want to use log-in box, I can just use this.
function btnPushItems_2() {
  signInPopup.style.display = "block";
}
function clearValue() {
  clearEmailBoxInputForSignIN.value = "";
  clearEmailBoxInputForRegister.value = "";
  clearPasswordBoxInputForSignIN.value = "";
  clearPasswordBoxInputForRegister.value = "";
  clearNameBoxInput.value = "";
}

/*in signIn.html */
function register() {
  registerPopup.style.display = "block";
  signInPopup.style.display = "none";
  clearValue();
  let existErrorMsgTag = document.getElementsByClassName("errorMsg")[0];
  if (existErrorMsgTag) {
    existErrorMsgTag.remove();
  }
}
function closeIconSignIn() {
  signInPopup.style.display = "none";
  clearValue();
  let existErrorMsgTag = document.getElementsByClassName("errorMsg")[0];
  if (existErrorMsgTag) {
    existErrorMsgTag.remove();
  }
}

/*in register.html */
function signIn() {
  registerPopup.style.display = "none";
  signInPopup.style.display = "block";
  clearValue();
  let existErrorMsgTag = document.getElementsByClassName("errorMsg")[0];
  if (existErrorMsgTag) {
    existErrorMsgTag.remove();
  }
  let existInformMsgTag = document.getElementsByClassName("successMsg")[0];
  if (existInformMsgTag) {
    existInformMsgTag.remove();
  }
}
function closeIconRegister() {
  registerPopup.style.display = "none";
  clearValue();
  let existInformMsgTag = document.getElementsByClassName("successMsg")[0];
  if (existInformMsgTag) {
    existInformMsgTag.remove();
  }
}

function validateEmail(email) {
  if (/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(email)) {
    return true;
  } else {
    return false;
  }
}
function validatePhone(phoneNumber) {
  if (/[0][0-9]{9}/.test(phoneNumber)) {
    return true;
  } else {
    return false;
  }
}

function createInformMsgTag(tagName, tagClassName, messages) {
  let bottomPopupBoxParentNode = document.getElementById(tagName).parentNode;
  let bottomPopupBox = document.getElementById(tagName);
  let existErrorMsgTag = document.getElementsByClassName("errorMsg")[0];
  let existInformMsgTag = document.getElementsByClassName("successMsg")[0];
  if (existErrorMsgTag) {
    existErrorMsgTag.remove();
  }
  if (existInformMsgTag) {
    existInformMsgTag.remove();
  }
  let errorMsg = document.createElement("div");
  errorMsg.className = tagClassName;

  let errorMsgTag = document.createElement("p");
  errorMsg.appendChild(errorMsgTag);

  bottomPopupBoxParentNode.insertBefore(errorMsg, bottomPopupBox);
  errorMsgTag.innerHTML = messages.join("<br>");
}

function createNavLogInTag() {
  let logInAndRegisterContainer = document.getElementById(
    "logInAndRegisterContainer"
  );
  let logInAndRegisterButton = document.getElementById("logInAndRegisterbtn");
  logInAndRegisterButton.remove();

  let logOutButton = document.createElement("button");
  logOutButton.id = "LogOut";
  logOutButton.className = "nav-link active";
  logOutButton.setAttribute("onclick", "deleteUserStatus(urlUser)");

  logInAndRegisterContainer.appendChild(logOutButton);
  logOutButton.innerHTML = "Log Out";
}

signInToSystem = document.getElementById("signInToSystem");
signInToSystem.addEventListener("click", (outcome) => {
  let messages = [];
  sigInEmailBox = document.getElementById("sigInEmailBox").value;

  sigInPasswordBox = document.getElementById("sigInPasswordBox").value;

  if (validateEmail(sigInEmailBox) === false) {
    messages.push("Invalid email");
  }
  if (sigInPasswordBox === "" || sigInPasswordBox == null) {
    messages.push("Enter password");
  }
  if (messages.length > 0) {
    outcome.preventDefault();
    tagClassName = "errorMsg";
    createInformMsgTag("bottomPopupBoxForSingIn", tagClassName, messages);
  } else {
    logInToSystem(urlUser);
  }
});

function logInToSystem(urlUser) {
  singInInput = document.getElementById("sigInEmailBox").value;
  sigInPasswordBox = document.getElementById("sigInPasswordBox").value;
  fetch(urlUser, {
    method: "PATCH",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: singInInput,
      password: sigInPasswordBox,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (String(Object.keys(data)) === "ok") {
        createNavLogInTag();

        signInPopup.style.display = "none";
        clearValue();
        window.location.replace("/memberCorner");
      } else {
        messages = [data["message"]];
        tagClassName = "errorMsg";
        createInformMsgTag("bottomPopupBoxForSingIn", tagClassName, messages);
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : logInToSystem(urlUser)"
      );
    });
}

// =============================
registerNewMeber = document.getElementById("registerNewMeber");
registerNewMeber.addEventListener("click", (outcome) => {
  let messages = [];
  registerName = document.getElementById("registerNameBox").value;
  registerEmail = document.getElementById("registerEmailBox").value;
  registerPassword = document.getElementById("registerPasswordBox").value;

  if (registerName === "" || registerName == null) {
    messages.push("Enter A Name");
  }
  if (validateEmail(registerEmail) === false) {
    messages.push("Invalid Email");
  }
  if (registerPassword.length <= 6) {
    messages.push("Password must have 6 length");
  }
  if (messages.length > 0) {
    outcome.preventDefault();
    tagClassName = "errorMsg";
    createInformMsgTag("bottomPopupBoxForRegister", tagClassName, messages);
  } else {
    registerToSystem(urlUser);
  }
});
function registerToSystem(urlUser) {
  fetch(urlUser, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: registerName,
      email: registerEmail,
      password: registerPassword,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (String(Object.keys(data)) === "ok") {
        messages = ["Registration Success"];
        tagClassName = "successMsg";
        createInformMsgTag("bottomPopupBoxForRegister", tagClassName, messages);
        clearValue();
      } else {
        messages = [data["message"]];
        tagClassName = "errorMsg";
        createInformMsgTag("bottomPopupBoxForRegister", tagClassName, messages);
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : registerToSystem(urlUser)"
      );
    });
}

function deleteUserStatus(urlUser) {
  fetch(urlUser, {
    method: "DELETE",
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (String(Object.keys(data)) === "ok") {
        let logInAndRegisterContainer = document.getElementById(
          "logInAndRegisterContainer"
        );
        let LogOut = document.getElementById("LogOut");
        LogOut.remove();

        let logInAndRegisterbtn = document.createElement("button");
        logInAndRegisterbtn.id = "logInAndRegisterbtn";
        logInAndRegisterbtn.className = "nav-link active";
        logInAndRegisterbtn.setAttribute("onclick", "btnPushItems_2()");
        logInAndRegisterContainer.appendChild(logInAndRegisterbtn);
        logInAndRegisterbtn.innerHTML = "Log In/Sign Up";
        logInAndRegisterbtn.style.display = "block";

        // This is to make sure the login box is empty.
        signInPopup.style.display = "none";
        clearValue();
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : deleteUserStatus(urlUser)"
      );
    });
}

function checkUserStatus(urlUser) {
  fetch(urlUser)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // The code below means the user already logged in system.
      let logInAndRegisterbtn = document.getElementById("logInAndRegisterbtn");
      if (String(data) !== "null") {
        createNavLogInTag();
      } else {
        logInAndRegisterbtn.style.display = "block";
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : checkUserStatus()"
      );
    });
}
// This will direct user to member page.
function memberCornerCheck() {
  fetch(urlUser)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (String(data) !== "null") {
        window.location.href = "/memberCorner";
      } else {
        btnPushItems_2();
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : memberCornerCheck()"
      );
    });
}

function handleCredentialResponse(response) {
  fetch(`/api/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_token: response.credential,
      signintype: "Google",
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["ok"]) {
        window.location.replace("/memberCorner");
      }
    });
}

let urlUser = "/api/user";
checkUserStatus(urlUser);
