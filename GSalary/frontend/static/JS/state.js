const queryString = window.location.search;
let stateName = queryString.slice(7, 10);

function getStateSalary(urlSalary, stateName) {
  fetch(urlSalary)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const stateFullName = {
        ACT: "Australian Capital Territory",
        NSW: "New South Wales",
        QLD: "Queensland",
        VIC: "Victoria",
        SA: "South Australia",
        WA: "Western Australia",
      };
      for (i = 0; i < data["by_states"].length; i++) {
        let key = Object.keys(data["by_states"][i])[0];
        if (key === stateName) {
          let topimgZone = document.querySelector(".topimgZone");
          topimgZone.style.backgroundImage = `url('/static/pictures/${stateName}.jpeg')`;

          let salary = data["by_states"][i][stateName]["avg Salary"];
          let firstTxt = document.querySelector(".first-txt");
          firstTxt.innerHTML = stateFullName[stateName];
          let iNF = new Intl.NumberFormat("en-US");
          let secondTxt = document.querySelector(".second-txt");
          secondTxt.innerHTML = `$ ${iNF.format(salary)}`;
          break; //When the key matches stateName, run the code below, and break the for loop.
        }
      }
      const newTopimgZone = document.querySelector(".topimgZone");
      newTopimgZone.style.display = "flex";
      const loader5 = document.querySelector(".loader5");
      loader5.style.display = "none";
      console.log(loader5);
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : getStateSalary()"
      );
    });
}

function getMaxMinSalary(urlSalary, stateName) {
  fetch(urlSalary)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      for (i = 0; i < data["max_salary"].length; i++) {
        let maxKey = Object.keys(data["max_salary"][i])[0];
        let minKey = Object.keys(data["min_salary"][i])[0];
        let maximum = document.querySelector(".maximum");
        let minimum = document.querySelector(".minimum");
        let iNF = new Intl.NumberFormat("en-US");
        if (stateName === maxKey) {
          maximum.innerHTML = `$ ${iNF.format(
            data["max_salary"][i][stateName]
          )}`;
        }
        if (stateName === minKey) {
          minimum.innerHTML = `$ ${iNF.format(
            data["min_salary"][i][stateName]
          )}`;
        }
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : getMaxMinSalary(urlSalary, stateName)"
      );
    });
}

function getStatePopulation(stateName) {
  const urlPopulation = `/api/stateInfo?state=${stateName}`;
  fetch(urlPopulation)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let iNF = new Intl.NumberFormat("en-US");
      let statePopulation = document.querySelector(".statePopulation");
      statePopulation.innerHTML = iNF.format(data["population"]);
      let jobPosts = document.querySelector(".jobPosts");
      jobPosts.innerHTML = iNF.format(data["count_job_post"]);
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : getStatePopulation()"
      );
    });
}

let urlSalary = "/api/salary";
getStateSalary(urlSalary, stateName);
getStatePopulation(stateName);
getMaxMinSalary(urlSalary, stateName);
