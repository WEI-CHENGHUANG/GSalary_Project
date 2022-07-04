let allJobPostCount = 0;
function setCount(userInput) {
  allJobPostCount = userInput;
  // console.log(`count:${allJobPostCount}`);
}

let searchJobPostCount = 0;
function setCountBySearch(userInput) {
  searchJobPostCount = userInput;
  // console.log(`count:${searchJobPostCount}`);
}

let isLoading = false;
function detectLoading(signal) {
  isLoading = signal;
  // console.log(isLoading);
}

const dataJobtemplate = document.querySelector("[data-job-template]");
const dataJobContainer = document.querySelector("[data-job-container]");

function userQueryCompany(allJobPostCount) {
  let keywordInput = document.getElementsByClassName("querykeyword")[0].value;

  // This is set allJobPostCount to 0 after user searches by comapany name.
  // For this reason, I need to reset the allJobPostCount to be 0 again
  if (allJobPostCount === null) {
    let firstRecord = JobPosttbody.firstElementChild;
    while (firstRecord) {
      firstRecord.remove();
      firstRecord = JobPosttbody.firstElementChild;
    }
    document.querySelector(".MorePostbtn").innerHTML = "More Posts";
    allJobPostCount = 0;
    keywordInput = "";
  }

  let url;
  // This IF statement is to check wheather user has inputed keyword or not, and the first time render page should be keywordInput === "".
  if (keywordInput === "") {
    url = `/api/jobposts?page=${allJobPostCount}&keyword=`;
  } else {
    url = `/api/jobposts?keyword=${keywordInput}`;
  }

  let count = 0 + allJobPostCount * 100;
  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["query_job_posts"].length === 0) {
        createFailQuery(keywordInput);
      } else {
        if (data["nextPage"] === null) {
          document.querySelector(".MorePostbtn").innerHTML = "First 100 Posts";
        }
        data["query_job_posts"].forEach((jobPost) => {
          count += 1;
          // this is to clone all nodes from template and the content as well.
          const eachRecord =
            dataJobtemplate.content.cloneNode(true).children[0];
          const number_ = eachRecord.querySelector("[data-number]");
          const company = eachRecord.querySelector("[data-company-name]");
          const title = eachRecord.querySelector("[data-job-title]");
          const location = eachRecord.querySelector("[data-location]");
          const url = eachRecord.querySelector("[data-ulr]");
          const urlAtage = url.querySelector("[data-ulr_a]");
          number_.textContent = count;
          company.textContent = jobPost["Company Name"];
          title.textContent = jobPost["Job Title"];
          location.textContent = jobPost["Office Loaction"];
          urlAtage.href = jobPost["URL"];
          url.append(urlAtage);
          dataJobContainer.append(eachRecord);
        });
        setCount(data["nextPage"]);
      }
      const jobPostsTable = document.querySelector("#jobPostsTable");
      jobPostsTable.style.display = "block";

      const loadMorePosts = document.querySelector(".loadMorePosts");
      loadMorePosts.style.display = "flex";
      const loader1 = document.querySelector(".loader1");
      loader1.style.display = "none";
      if (document.getElementsByClassName("querykeyword")[0].value) {
        document.getElementsByClassName("querykeyword")[0].value = "";
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : userQueryCompany()"
      );
    });
}

// This is to check wheather there are a wrong msg tag or not, after user's query.
function querytagsCheck() {
  let JobPosttbody = document.getElementById("JobPosttbody");
  let firstRecord = JobPosttbody.firstElementChild;
  while (firstRecord) {
    firstRecord.remove();
    firstRecord = JobPosttbody.firstElementChild;
  }
  let wrongMessage = document.querySelector(".wrongMessage");

  if (wrongMessage) {
    wrongMessage.remove();
  }
  allJobPostCount = 0;
  userQueryCompany(allJobPostCount);
}

function createFailQuery(keywordInput) {
  let tbody = document.getElementById("JobPosttbody");
  let trTag = document.createElement("tr");
  trTag.className = "wrongMessage";
  let thTag = document.createElement("th");
  thTag.colSpan = "5";
  thTag.innerHTML =
    `"${keywordInput}"` + ` cannot be found, please retry again.`;
  trTag.append(thTag);
  tbody.append(trTag);
}

function createNewsBlock(newsUrl) {
  fetch(newsUrl)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let firstNews = document.querySelector(".firstNews");
      let image1 = document.createElement("img");
      image1.src = data["first_news"][2];
      let firstNewsContent = document.querySelector(".firstNewsContent");
      let a1 = document.createElement("a");
      a1.href = data["first_news"][1];
      a1.innerHTML = data["first_news"][0];

      firstNews.insertBefore(image1, firstNewsContent);
      firstNewsContent.append(a1);

      let secNews = document.querySelector(".secNews");
      let image2 = document.createElement("img");
      image2.src = data["second_news"][2];
      let secNewsContent = document.querySelector(".secNewsContent");
      let a2 = document.createElement("a");
      a2.href = data["second_news"][1];
      a2.innerHTML = data["second_news"][0];
      secNews.insertBefore(image2, secNewsContent);
      secNewsContent.append(a2);
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : createNewsBlock()"
      );
    });
}

function insertDataToBars(salaryUrl) {
  fetch(salaryUrl)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      //   let innerbar1 = document.getElementsByClassName("innerbar1")[0];
      // This is to capture the data and sort it in dec order.
      let states = {};
      for (let i = 0; i < data["by_states"].length; i++) {
        let name = Object.keys(data["by_states"][i])[0];
        let salary = Object.values(data["by_states"][i])[0]["avg Salary"];
        states[name] = salary;
      }
      let result = Object.keys(states).map((key) => {
        return [key, states[key]];
      });
      result
        .sort((first, second) => {
          return first[1] - second[1];
        })
        .reverse();
      let count = 0;
      result.forEach((state) => {
        let eachstate = document.getElementsByClassName("state")[count];
        eachstate.setAttribute("value", state[0]);
        eachstate.setAttribute("onclick", "redirectToStatePage(this.value)");
        // console.log(state[0]);
        let pecen = ((state[1] / 200000) * 100).toFixed(2);
        pecen += "%";
        let eachState = document.getElementsByClassName("stateDetail")[count];
        eachState.innerHTML = state[0];
        let innerbar1 = document.getElementsByClassName("innerbar1")[count];
        innerbar1.style.width = pecen;
        let iNF = new Intl.NumberFormat("en-US");
        let stateSalary =
          document.getElementsByClassName("stateAvgSalarytext")[count];
        stateSalary.innerHTML = `${pecen} / ${iNF.format(state[1])}`;
        count += 1;
        // console.log(state[0])
      });
      // console.log(states)
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : insertDataToBars()"
      );
    });
}

function createMidAvgSalary(salaryUrl) {
  fetch(salaryUrl)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let iNF = new Intl.NumberFormat("en-US");
      let midAvgSalary = document.querySelector(".innerMidAvgSalary");

      midAvgSalary.innerHTML = `$ ${iNF.format(data["total"]["avg Salary"])}`;
      let midCountSalary = document.querySelector(".innerMidCountSalary");
      midCountSalary.innerHTML = `Including salary info's posts:  ${iNF.format(
        data["total"]["count"]
      )}`;
      const loader2 = document.querySelector(".loader2");
      loader2.style.display = "none";
      const outertotalSalary = document.querySelector(".outertotalSalary");
      outertotalSalary.style.display = "block";
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : queryAttractions()"
      );
    });
}

function redirectToStatePage(state) {
  window.location.href = `state?state=${state}`;
}

const salaryUrl = "/api/salary";
userQueryCompany(allJobPostCount, "");
createMidAvgSalary(salaryUrl);
insertDataToBars(salaryUrl);

const newsUrl = "/api/news";
createNewsBlock(newsUrl);
