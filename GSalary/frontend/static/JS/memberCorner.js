let countOwnPost = 0;
function ownPostsetCount(userInput1) {
  countOwnPost = userInput1;
  // console.log(`countOwnPost:${countOwnPost}`);
  if (countOwnPost === null) {
    let newLoadMorebtn = document.querySelector(".ownloadMore");
    newLoadMorebtn.remove();
  }
}

let count = 0;
function setCount(userInput) {
  count = userInput;
  // console.log(`count:${count}`);
  if (count === null) {
    let newLoadMorebtn = document.querySelector(".loadMore");
    newLoadMorebtn.remove();
  }
}

let isLoading = false;
function detectLoading(signal) {
  isLoading = signal;
  // console.log(isLoading);
}

function checkUserStatusAndMemberlInfo(urlUser) {
  fetch(urlUser)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // // The code below means the user already logged in system.
      // let logInAndRegisterbtn = document.getElementById("logInAndRegisterbtn");
      if (String(data) !== "null") {
        createNavLogInTag();
        let fullURL = `https://d19u9n2870afb4.cloudfront.net/${data["photoURL"]}`;

        let memberIdContent =
          document.getElementsByClassName("memberIdContent")[0];
        memberIdContent.innerHTML = data["id"];
        let memberNameContent =
          document.getElementsByClassName("memberNameContent")[0];
        memberNameContent.innerHTML = data["name"];
        let memberEmailContent =
          document.getElementsByClassName("memberEmailContent")[0];
        memberEmailContent.innerHTML = data["email"];

        let photoTag = document.getElementsByClassName("photo")[0];
        let imgTag = document.createElement("img");
        imgTag.className = "userimage";
        imgTag.src = fullURL;
        photoTag.append(imgTag);
        // This is to disable the cover.
        let cover = document.getElementById("cover");
        cover.style.display = "none";
      } else {
        window.location.href = "/";
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : checkUserStatus()"
      );
    });
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
  logOutButton.setAttribute("onclick", "logOutBackToHmPage(urlUser)");

  logInAndRegisterContainer.appendChild(logOutButton);
  logOutButton.innerHTML = "Log Out";
}

function logOutBackToHmPage(urlUser) {
  fetch(urlUser, {
    method: "DELETE",
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      // if (String(Object.keys(data)) === "ok")
      if (data["ok"]) {
        window.location.href = "/";
      } else {
        console.log(data);
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : logOutBackToHmPage(urlUser)"
      );
    });
}

// function memberlInfo(urlUser) {
//   fetch(urlUser)
//     .then((response) => {
//       return response.json();
//     })
//     .then((data) => {
//       // This url is to get the photo from S3
//       let fullURL = `https://d19u9n2870afb4.cloudfront.net/${data["photoURL"]}`;

//       let memberIdContent =
//         document.getElementsByClassName("memberIdContent")[0];
//       memberIdContent.innerHTML = data["id"];
//       let memberNameContent =
//         document.getElementsByClassName("memberNameContent")[0];
//       memberNameContent.innerHTML = data["name"];
//       let memberEmailContent =
//         document.getElementsByClassName("memberEmailContent")[0];
//       memberEmailContent.innerHTML = data["email"];

//       let photoTag = document.getElementsByClassName("photo")[0];
//       let imgTag = document.createElement("img");
//       imgTag.className = "userimage";
//       imgTag.src = fullURL;
//       photoTag.append(imgTag);
//     })
//     .catch((error) => {
//       console.log(
//         error,
//         "Something went wrong when fetching data via API, Check JS function : memberlInfo(urlUser)"
//       );
//     });
// }
function uploadPhoto(urlMember) {
  let input_file = document.querySelector("#my_file");
  let formData = new FormData();
  formData.append("file", input_file.files[0]);

  fetch(urlMember, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let photo = document.getElementsByClassName("photo")[0];
      let userimage = document.getElementsByClassName("userimage")[0];
      userimage.remove();
      let imgTag = document.createElement("img");
      imgTag.className = "userimage";
      imgTag.src = data["URL"];
      imgTag.alt = "Pls choose a pic";

      photo.append(imgTag);
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : uploadPhoto(urlMember)"
      );
    });
}

// =================

function createPostsBox(posts, continerNumber, postData) {
  const outerPostContainer1 = document.querySelector(
    `.outerPostContainer${continerNumber}`
  );
  let count = 1;
  // i 要改成數據的長度
  for (let i = 1; i < posts; i++) {
    singlePost = postData[i];
    let titleNameList = [
      ["Post Id", "Service Year"],
      ["Company Name", "Job Title"],
      ["Working Hours/week", "Annual Salary"],
      ["Member Id", "Post Time"],
    ];
    let innerPostContainer = document.createElement("div");
    innerPostContainer.className = `innerPostContainer${count}`;
    outerPostContainer1.append(innerPostContainer);
    count += 1;
    for (let j = 0; j < titleNameList.length; j++) {
      let keyLeft = titleNameList[j][0];
      let keyright = titleNameList[j][1];
      let leftText;
      let rightText;
      if (keyright === "Post Time") {
        rightText = singlePost[keyright].substr(0, 25);
      } else {
        rightText = singlePost[keyright];
      }
      leftText = singlePost[keyLeft];

      // =============
      const RowTemplate = document.querySelector("[row-template]");
      const cloneRowTemplate = RowTemplate.content.cloneNode(true).children[0];

      const leftContainer = cloneRowTemplate.querySelector("[left-container]");
      const leftName = leftContainer.querySelector("[left-name]");
      const leftContent = leftContainer.querySelector("[left-content]");
      leftName.textContent = keyLeft + ":";
      leftContent.textContent = leftText;

      const rightContainer =
        cloneRowTemplate.querySelector("[right-container]");
      const rightContent = rightContainer.querySelector("[right-content]");
      const rightName = rightContainer.querySelector("[right-name]");
      rightName.textContent = keyright + ":";
      rightContent.textContent = rightText;
      innerPostContainer.append(cloneRowTemplate);
    }
    let fifthRowTag = document.createElement("div");
    fifthRowTag.className = "fifthRow";
    let pTag = document.createElement("p");
    pTag.className = "shareContent";
    pTag.textContent = singlePost["Post content"];
    fifthRowTag.append(pTag);
    innerPostContainer.append(fifthRowTag);
  }
}

// ========================================================
// This is for Your post
function yourPosts(countOwnPost) {
  detectLoading(true);
  let urlPost = `/api/post?page=${countOwnPost}`;
  fetch(urlPost)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let posts = Object.keys(data).length;
      let continerNumber = 2;
      createPostsBox(posts, continerNumber, data);
      // This is to create a load more button
      let currentLoadBtn = document.querySelector(".ownloadMore");
      if (currentLoadBtn) {
        currentLoadBtn.remove();
      }
      let outerPostContainer1 = document.querySelector(".outerPostContainer2");
      let outButtonTag = document.createElement("div");
      outButtonTag.className = "ownloadMore";
      outButtonTag.style.cssText = "border: none; margin-top: 60px;";
      let innerButtonTag = document.createElement("button");
      innerButtonTag.className = "ownloadMorebtn";
      // Check the oadMorePosts(count) function below
      innerButtonTag.setAttribute("onclick", "loadMoreOwnPosts(count)");
      innerButtonTag.innerHTML = "Load More";
      outButtonTag.append(innerButtonTag);
      outerPostContainer1.append(outButtonTag);
      // ========================================
      ownPostsetCount(data["nextPage"]);
      detectLoading(false);
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : yourPosts(countOwnPost)"
      );
    });
}
// ========================================================
// This is for All post
function allPosts(count) {
  detectLoading(true);
  let urlPosts = `/api/posts?page=${count}`;

  fetch(urlPosts)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let posts = Object.keys(data).length;
      let continerNumber = 1;
      createPostsBox(posts, continerNumber, data);
      // This is to create a load more button
      let currentLoadBtn = document.querySelector(".loadMore");
      if (currentLoadBtn) {
        currentLoadBtn.remove();
      }
      let outerPostContainer1 = document.querySelector(".outerPostContainer1");
      let outButtonTag = document.createElement("div");
      outButtonTag.className = "loadMore";
      outButtonTag.style.cssText = "border: none; margin-top: 60px;";
      let innerButtonTag = document.createElement("button");
      innerButtonTag.className = "loadMorebtn";
      // Check the loadMorePosts(count) function below
      innerButtonTag.setAttribute("onclick", "loadMorePosts(count)");
      innerButtonTag.innerHTML = "Load More";
      outButtonTag.append(innerButtonTag);
      outerPostContainer1.append(outButtonTag);
      // ========================================
      setCount(data["nextPage"]);
      detectLoading(false);
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : allPosts(count)"
      );
    });
}
// ========================================================
// The code below is to post a new post.
let postInput = {};
$(document).ready(function () {
  $(document).on("submit", "#postForm", function () {
    const form = document.getElementById("postForm");
    let formElements = Array.from(form.elements);

    formElements.forEach((element) => {
      let testest = element.className;
      postInput[testest] = element.value;
    });
    // =========================
    fetch(urlForNewPost, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postInput),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(`check memberCorner.js line 316: ${data}`);
      })
      .catch((error) => {
        console.log(
          error,
          "Something went wrong when fetching data via API, Check JS function : check memberCorner.js line around 317"
        );
      });
    // ========================
    const inputs = document.querySelectorAll(
      ".companyNameContent, .avghrsContent, .serviceYearsContent, .positionTitleContent, .annualSalaryContent, #inputShareContent"
    );
    inputs.forEach((input) => {
      input.value = "";
    });
    // The code below is to reload the page after submitted
    // return false;
  });
});

// The two functions, loadMorePosts(count) and loadMoreOwnPosts(count), are to make sure the async fetching data working properly.
function loadMorePosts(count) {
  if (count && isLoading === false) allPosts(count);
}
function loadMoreOwnPosts(count) {
  if (countOwnPost && isLoading === false) yourPosts(countOwnPost);
}

// ========================================================
let urlUser = "/api/user";
let urlForNewPost = "/api/post?page=";
let urlMember = "/api/member";
checkUserStatusAndMemberlInfo(urlUser);
// memberlInfo(urlUser);
allPosts(count);
yourPosts(countOwnPost);
